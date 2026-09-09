"""CLI entry point — argparse subcommands."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from zerotrustmirror import __version__
from zerotrustmirror.correlation import correlate
from zerotrustmirror.loaders import load_channel_logs, load_env
from zerotrustmirror.models import PILLAR_NAMES
from zerotrustmirror.report import build_result, to_json, to_markdown, write_report
from zerotrustmirror.scoring import compute_weighted_score, determine_maturity, evaluate_all


def _resolve_env(path: str | None, pack: str | None) -> dict:
    if path:
        return load_env(path)
    if pack in ("weak", "strong"):
        base = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "envs"
        env_path = base / f"{pack}.json"
        if env_path.exists():
            return load_env(env_path)
        # Fall back to python module
        if pack == "weak":
            from tests.fixtures.envs.weak import WEAK_ENV
            return WEAK_ENV
        from tests.fixtures.envs.strong import STRONG_ENV
        return STRONG_ENV
    return {}


def _resolve_channels(channel_dir: str | None) -> list[list[dict]]:
    if not channel_dir:
        return []
    d = Path(channel_dir)
    logs = []
    for ch in ("web.json", "network.json", "host.json"):
        p = d / ch
        if p.exists():
            logs.extend([load_channel_logs(p)])
    return logs


def cmd_score(args: argparse.Namespace) -> int:
    cfg = _resolve_env(args.env, args.pack)
    if not cfg:
        print("ERROR: No environment specified. Use --env <path> or --pack weak|strong", file=sys.stderr)
        return 1
    pillars = evaluate_all(cfg)
    overall = compute_weighted_score(pillars)
    maturity = determine_maturity(overall)
    behaviors = []
    if args.channel_dir:
        channel_logs = _resolve_channels(args.channel_dir)
        if channel_logs:
            behaviors = correlate(channel_logs)
    result = build_result(pillars, overall, maturity, behaviors)
    if args.out_dir:
        paths = write_report(result, args.out_dir, prefix=args.prefix)
        print(json.dumps(paths, indent=2))
    else:
        print(to_markdown(result))
    return 0


def cmd_correlate(args: argparse.Namespace) -> int:
    channel_logs = _resolve_channels(args.channel_dir)
    if not channel_logs:
        print("ERROR: No channel logs found. Use --channel-dir <path>", file=sys.stderr)
        return 1
    behaviors = correlate(channel_logs, window=args.window)
    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        data = []
        for b in behaviors:
            data.append({
                "user": b.user,
                "risk_score": b.risk_score,
                "policy_finding": b.policy_finding,
                "event_count": len(b.events),
                "channels": list(set(e.channel for e in b.events)),
            })
        p = out / "correlation.json"
        p.write_text(json.dumps(data, indent=2))
        print(json.dumps({"correlation": str(p)}, indent=2))
    else:
        for b in behaviors:
            print(f"[{b.risk_score}] {b.user}: {b.policy_finding}")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    print("=== ZeroTrustMirror Demo ===\n")

    # Weak environment
    print("--- WEAK ENVIRONMENT ---")
    from tests.fixtures.envs.weak import WEAK_ENV
    weak_pillars = evaluate_all(WEAK_ENV)
    weak_overall = compute_weighted_score(weak_pillars)
    weak_maturity = determine_maturity(weak_overall)
    weak_result = build_result(weak_pillars, weak_overall, weak_maturity)
    print(to_markdown(weak_result))

    # Strong environment
    print("\n--- STRONG ENVIRONMENT ---")
    from tests.fixtures.envs.strong import STRONG_ENV
    strong_pillars = evaluate_all(STRONG_ENV)
    strong_overall = compute_weighted_score(strong_pillars)
    strong_maturity = determine_maturity(strong_overall)
    strong_result = build_result(strong_pillars, strong_overall, strong_maturity)
    print(to_markdown(strong_result))

    # Correlation demo
    from tests.fixtures.channels import WEB_LOGS, NETWORK_LOGS, HOST_LOGS
    behaviors = correlate([WEB_LOGS, NETWORK_LOGS, HOST_LOGS])
    print("\n--- CORRELATION FINDINGS ---")
    for b in behaviors:
        print(f"[risk={b.risk_score}] {b.user}: {b.policy_finding}")
        print(f"  Events: {len(b.events)}, Channels: {sorted(set(e.channel for e in b.events))}")

    # Write reports
    out_dir = args.out_dir or "demo_output"
    write_report(weak_result, out_dir, prefix="weak")
    write_report(strong_result, out_dir, prefix="strong")
    print(f"\nReports written to {out_dir}/")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="zerotrustmirror",
        description="Zero-trust readiness + correlation engine",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command")

    # score
    p_score = sub.add_parser("score", help="Score environment against ZTA pillars")
    p_score.add_argument("--env", help="Path to environment JSON/YAML")
    p_score.add_argument("--pack", choices=["weak", "strong"], help="Built-in fixture pack")
    p_score.add_argument("--channel-dir", help="Directory with web.json/network.json/host.json")
    p_score.add_argument("--out-dir", help="Output directory for reports")
    p_score.add_argument("--prefix", default="zta", help="Report file prefix")

    # correlate
    p_corr = sub.add_parser("correlate", help="Multi-channel correlation")
    p_corr.add_argument("--channel-dir", required=True, help="Directory with channel log files")
    p_corr.add_argument("--window", type=float, default=120.0, help="Correlation window (seconds)")
    p_corr.add_argument("--out-dir", help="Output directory")

    # demo
    p_demo = sub.add_parser("demo", help="Run offline demo with fixtures")
    p_demo.add_argument("--out-dir", help="Output directory for demo reports")

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0

    if args.command == "score":
        return cmd_score(args)
    if args.command == "correlate":
        return cmd_correlate(args)
    if args.command == "demo":
        return cmd_demo(args)
    return 0
