# test_sweep: dev notes

## Design decisions

- **Temp copy, not in place.** Elythia tests write SQLite files, checkpoints and logs next to themselves. Running them in place would dirty a repo we don't own.
- **One process per test file.** It's slower, but one test's global state or crash can't contaminate another.
- **Python runs from the test's own folder; Node runs from that folder too.** That turned out to be **wrong for Elythia's Node tests**: most Elythia READMEs say to run from the repo root (`node --test research/ELY-xxxx/test.cjs`), and tests that use root-relative paths fail otherwise. All failures were re-run from the root by hand before triage.

## Known gaps / next version

1. Add `--node-cwd root|dir` (default `root`), and try both before reporting a failure.
2. Write `sweep.json` incrementally. The first Elythia run hit a 10-minute tool limit and lost its JSON, though the log survived.
3. For `import-error`, automatically try `PYTHONPATH` entries for sibling folders the test mentions (`ELY-00xx` strings).
4. Add a `--repeat N` flag to separate flaky failures from deterministic ones.
5. Parse each README's "Reproduce" block and run the documented command, falling back to the heuristic only when there isn't one.
