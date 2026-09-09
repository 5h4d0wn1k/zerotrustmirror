# zerotrustmirror

Zero-trust readiness + correlation engine — ZTA pillars scoring with evidence, web/net/host multichannel correlation, metrics

## IMPORTANT: Read before use.

This is an **authorized security testing and education** tool. It is designed to be
used exclusively against systems, networks, and hardware that **you own** or for which
you have **explicit written authorization** to test.

### Authorization Requirements

- Only test targets you own, your own accounts, or systems you have written permission
  to assess (scope, duration, and limits in writing).
- This tool defaults to **offline / simulation mode**. Any action that could affect a
  real system, emit radio signals, or contact a real network requires an explicit
  confirmation flag **and** membership of the configured LAB allowlist.
- The demo/harness functionality runs entirely on localhost, fixtures, or your own lab.

### Legal Framework

Unauthorized security testing is a crime in most jurisdictions, including:

- **Computer Fraud and Abuse Act (CFAA), 18 U.S.C. § 1030** (US) — unauthorized
  access to computers is a federal crime, punishable by up to 20 years imprisonment.
- **Wiretap Act (18 U.S.C. § 2511)** (US) — intercepting electronic communications
  without consent is illegal.
- **EU Directive 2013/40/EU on attacks against information systems** — criminalises
  illegal access and interference.
- **State / local computer-crime statutes** — nearly all jurisdictions criminalise
  unauthorised access, data theft, or network disruption.
- **RF regulatory law** — transmitting on ISM bands without the appropriate
  authorisation may violate terms of your licence/regulatory regime in your country.

### Acceptable Use

- Learning and coursework in a controlled lab environment.
- Authorised penetration testing and red/blue-team exercises with written scope.
- Security research on systems you own.
- Building defensive detections and hardening your own infrastructure.

### Prohibited Use

- **Any** unauthorised access, interception, or disruption.
- Use against third-party networks, devices, or accounts at any time.
- Removing or weakening the safety gates, allowlists, or legal notices.
- Any activity that violates applicable law.

### No Warranty

This software is provided "AS IS", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability, fitness
for a particular purpose, and non-infringement. **In no event shall the authors or
copyright holders be liable** for any claim, damages or other liability arising
from, out of, or in connection with the software or the use or other dealings in
the software. **You are solely responsible for how you use this tool.**

### Responsible Disclosure

If you discover real vulnerabilities while learning with this tool, follow
responsible disclosure:

1. Report privately to the affected vendor/owner.
2. Give a reasonable remediation window.
3. Do not exploit beyond proof of concept.
4. Only publish with the vendor's consent.

## Quickstart

```bash
python3 -m pip install -e .
python3 -m zerotrustmirror --help
python3 -m zerotrustmirror --demo    # offline, exit 0
python3 -m unittest discover -s tests
```

## Architecture

```
zerotrustmirror/
├── cli.py              # argparse subcommands: score, correlate, demo
├── scoring.py          # weighted ZTA scoring + maturity levels
├── correlation.py      # multichannel correlation engine
├── report.py           # JSON/Markdown scorecards + remediation roadmap
├── loaders.py          # JSON/YAML fixture loaders
├── models.py           # data models (PillarResult, BehaviorRecord, etc.)
└── pillars/            # 7 NIST SP 800-207 pillar evaluators
    ├── identity.py
    ├── devices.py
    ├── network.py
    ├── apps.py
    ├── data.py
    ├── automation.py
    └── vis.py
```

## Subcommands

| Command | Description |
|---------|-------------|
| `zerotrustmirror score --pack weak` | Score weak environment pack |
| `zerotrustmirror score --pack strong --channel-dir logs/` | Score with correlation |
| `zerotrustmirror correlate --channel-dir logs/` | Standalone multichannel correlation |
| `zerotrustmirror demo` | Full demo with fixtures, exits 0 |

## Environment Packs

Fixture packs under `tests/fixtures/envs/`:
- **weak.json / weak.yaml** — no MFA, no device posture, flat network, no classification, no SOAR, no logs
- **strong.json / strong.yaml** — MFA everywhere, device compliance, micro-segmentation, classification, SOAR, SIEM

## Test Standard

- Weak pack overall < 40, strong pack > 75
- Identity: weak 0 vs strong 80 (delta 80 points)
- Evidence citations non-empty and traceable to fixture fields
- Correlation: alice@example.com correlated across web+network+host
- Score changes when a fixture field flips (parity test)
- Remediation roadmap: 29 items generated for weak pack

## Live Lab Test Plan

1. **Setup**: Install in a controlled lab VM (`python3 -m pip install -e .`)
2. **Weak baseline**: `zerotrustmirror score --pack weak` — verify score < 40
3. **Strong baseline**: `zerotrustmirror score --pack strong` — verify score > 75
4. **Field flip test**: Modify one fixture field (e.g., set `mfa_enabled: true` in weak), re-score, verify identity pillar increases
5. **Correlation test**: Place channel logs in a directory, run `zerotrustmirror correlate --channel-dir <dir>`, verify alice@example.com appears across 3 channels
6. **Demo validation**: `zerotrustmirror demo` exits 0, produces JSON+Markdown reports
7. **Full test suite**: `python3 -m unittest discover -s tests` — all tests green

## Metrics

| Metric | Value |
|--------|-------|
| Test count | 71 |
| Tests passing | 71 |
| Modules | 12 (7 pillar + 5 core) |
| Fixture packs | 2 (weak, strong) + 3 channel logs |
| Weak overall score | 2.8 / 100 |
| Strong overall score | 96.0 / 100 |
| Weak identity | 0 |
| Strong identity | 80 |
| Correlation events (alice) | 6 across web+network+host |
| Correlation risk score (alice) | 1.0 (CRITICAL) |
| Remediation items (weak) | 29 |
| py_compile | All modules compile cleanly |
| Demo exit code | 0 |
| Token literal scan | Clean — no AKIA/xoxb/ghp_/sk_live/eyJ patterns |
