# test_sweep

Runs every Python (`test_*.py`) and Node (`test_*.cjs`, `test.cjs`, …) test file in a repo, each on its own with a timeout, and writes `sweep.json` and `sweep.md` summaries. Tests run in a **temporary copy**, so the target repo is never modified.

## Run

```sh
python3 tools/test_sweep/test_sweep.py /path/to/repo --out results/ --timeout 60
python3 tools/test_sweep/test_sweep.py /path/to/repo --only 'research/ELY-04*'
```

It needs Python 3.8+ and, for JS tests, Node 18+. It has no dependencies. It isn't meant for Pythonista, because it shells out to `node` and `subprocess`.

## Reading results

| status | meaning |
|---|---|
| pass | exit code 0 |
| fail | non-zero exit. **Not automatically a bug**: check the README's run instructions first |
| import-error | missing module or path. Usually the test needs a different `PYTHONPATH` or working directory |
| timeout | exceeded `--timeout` |

`results/` holds logs from past sweeps.

## Status

v1 works. See [DEVNOTES.md](DEVNOTES.md) for known gaps.
