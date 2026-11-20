# Some tests read uncompressed data files that are only committed compressed

- **Repo / files:** ELY-0252, 0275, 0343, 0344, 0349 tests
- **@** `2bebcbcecb1cfe31f9f657fc83322e3ef870b174`
- **Severity:** fragile
- **Status:** found, mentioned in Elythia#2
- **Found:** 2026-11-20 by Claude (Opus 5.5)

## What happens

The tests open files like `observations.json` that exist in the repo only as `observations.json.gz`, `.gz.base64` or `.zlib.base64`, so they fail with ENOENT on a fresh clone.

- ELY-0252's README documents the `gzip -dc` step, so this one is expected.
- ELY-0349's README describes `observations.json` as present, but only the base64 zlib copy was committed.
- ELY-0343 needs `research/ELY-0342/observations.json`, which exists only as `.gz.base64`. ELY-0344 then needs ELY-0343's output, so it fails in turn.

## Suggested fix

Have each test decompress its own input when the plain file is missing (Node's `zlib` handles gzip and zlib directly). Alternatively, one `tools/hydrate.cjs` at the repo root could expand every compressed artifact before a test run.
