# Elythia bug index

Snapshot: `2bebcbcecb1cfe31f9f657fc83322e3ef870b174` (2026-11-20)

| Report | Severity | Status |
|---|---|---|
| [Git blob header trailing space](2026-11-20-git-blob-header-trailing-space.md) (ELY-0404 _fixed, ELY-0411) | wrong-result | issue #1, fix verified locally |
| [JSON preflight test inputs](2026-11-20-json-preflight-test-inputs.md) (ELY-0086, ELY-0078) | wrong-result | issue #1 |
| [Float-exact hashes not portable](2026-11-20-float-exact-hashes-not-portable.md) (ELY-0438/0445/0449/0450/0452/0456) | fragile | issue #2 |
| [Tests need uncommitted inputs](2026-11-20-tests-need-uncommitted-inputs.md) (ELY-0252/0275/0343/0344/0349) | fragile | mentioned in #2 |

## Triaged as not bugs (already known or documented)

- ELY-0078 whitespace allowlist: found and fixed by ELY-0080/0081.
- Original ELY-0404/0405/0407 tests (`"\\0"` header): superseded by `_fixed` files. 0405/0407 `_fixed` pass from the repo root.
- ELY-0472: abort recorded in its own `FAILURE.md`.
- ELY-0438: native failure already documented in ELY-0439's README.

## Not yet triaged

- **59 Python tests hit import errors** when run from their own folder. They need sibling experiments on `PYTHONPATH`. The next step is to rebuild each one's path from the CI workflows or READMEs and re-run.
- ELY-0137, 0141, 0143–0145, 0149 and 0163 failed in the sweep but passed when re-run by hand, so they're possibly flaky (subprocess or timing). Re-run them several times to confirm.
- ELY-0087, 0088, 0346, 0347, 0350, 0351, 0392 and 0395 failed in the sweep but haven't been examined yet.
