# Elythia import record

- **Source:** `levelinglucy/Elythia` (private), branch `main`
- **Commit:** `2bebcbcecb1cfe31f9f657fc83322e3ef870b174` ("ELY-0475: preserve exact committed-file verification and runtime limits")
- **Date:** 2026-11-20
- **Size:** about 3,660 files and 88 MB, across 474 research experiments

## Why there are no file copies here

Elythia is **private** and this workbench is **public**. Copying its source here would publish Dylan's private research, so this folder records only the commit that was tested. Bug reports quote the minimum needed to explain each bug. If Dylan wants Elythia code mirrored here, he has to say so explicitly.

To reproduce the sweep: `git clone` Elythia, check out the commit above, then run
`python3 tools/test_sweep/test_sweep.py <path-to-elythia> --out <dir>`.
