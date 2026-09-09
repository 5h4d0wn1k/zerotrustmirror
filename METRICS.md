# Metrics

Last updated: 2026-09-09

## Test Results

- **Total tests**: 71
- **Passing**: 71
- **Failures**: 0
- **Run time**: 0.019s

## Scores

| Environment | Overall | Identity | Devices | Network | Apps | Data | Automation | Vis |
|-------------|---------|----------|---------|---------|------|------|------------|-----|
| Weak | 2.8 | 0 | 0 | 0 | 0 | 15 | 0 | 5 |
| Strong | 96.0 | 80 | 100 | 100 | 100 | 100 | 100 | 100 |

## Correlation

- alice@example.com: 6 events across web+network+host, risk 1.0 (CRITICAL)
- Bob: 1 event (web only), no cross-channel correlation
- Charlie: 1 event (network only), no cross-channel correlation
- Dave: 1 event (host only), no cross-channel correlation

## Remediation

- Weak pack: 29 remediation items generated
- Strong pack: 0 remediation items (all pillars optimal)

## Build Verification

- py_compile: All 12 modules compile cleanly
- Demo: Exits 0, produces JSON+Markdown reports
- Token literal scan: No AKIA/xoxb/ghp_/sk_live/eyJ patterns found

## File Counts

- Source modules: 12
- Test files: 9
- Fixture files: 7 (2 weak + 2 strong + 3 channel logs)
