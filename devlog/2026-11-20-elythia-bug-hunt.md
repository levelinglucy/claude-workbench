# 2026-11-20: First bug hunt, Elythia

**Who:** Claude (Opus 5.5), autonomous pass that Dylan approved ("go for it")
**Target:** `levelinglucy/Elythia` @ `2bebcbc` (474 experiments, 436 test files)

## Done

- Syntax-checked all 331 `.py` files and 624 `.cjs`/`.mjs`/`.js` files: **all clean**.
- Built `tools/test_sweep/` and ran every test file on native Node 22.23.5 and Python 3.13. Before triage: **340 passed, 37 failed, 59 import errors**.
- Triaged the failures against each experiment's README and git history, re-running from the repo root as documented.
- Filed **Elythia#1** (concrete test bugs with verified one-line fixes) and **Elythia#2** (cross-runtime float-hash fragility).

## Findings worth remembering

- **Most of the Elythia research written since mid-November was never run on native Node.** It was produced in the AI connector's V8 harness. Discrete outcomes reproduce natively, but exact float hashes are off by one ULP, so any test pinning a raw-state hash breaks off-harness.
- **Double-escaping is a recurring defect**: `"\\0"` instead of `"\0"`, and `'\\t'` instead of tab. The likely cause is code passing through a JSON/string layer in the generating tool. It's worth grepping for in new experiments.
- **Elythia's culture is to preserve history and append fixes**, never edit. That's why fixes went out as issues, not PRs that edit files.

## Decisions

- **No source copied into `imports/`**, because Elythia is private and this repo is public.

## Left

See `bug-reports/elythia/INDEX.md` → "Not yet triaged": 59 import-error tests, possibly flaky subprocess tests, and 8 unexamined failures.
