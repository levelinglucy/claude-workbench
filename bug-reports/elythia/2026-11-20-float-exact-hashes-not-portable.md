# Exact float-state hashes from the V8 harness fail on native Node by one ULP

- **Repo / files:** tests in ELY-0438, 0445, 0449, 0450, 0452, 0456 (and ELY-0472's recorded abort may be related)
- **@** `2bebcbcecb1cfe31f9f657fc83322e3ef870b174`
- **Severity:** fragile (results are sound, but the tests fail on any runtime except the one that produced them)
- **Status:** confirmed, issue-filed (Elythia#2)
- **Found:** 2026-11-20 by Claude (Opus 5.5)

## What happens

On native Node 22.23.5 these tests fail on SHA-256 state hashes, for example:

```
ELY-0449/0450  preserved early birth fingerprint
  expected 7d605eb9…  actual ed9f8c88…
ELY-0452       exact post-eight-tick state hash
ELY-0445       ELY-0444 first-tick mismatch
ELY-0456       eight-tick state commitment
```

## What I checked

1. **The engine is natively deterministic.** `node research/ELY-0439/verify.cjs` passes on Node 22, replaying all 180 worlds exactly. So Node 22 and the Node 24 that ELY-0439 used agree.
2. **The discrete outcomes match.** For all 10 recorded ELY-0448 births, the native birth tick and child ID match `results.json`, and only the hash differs.
3. **The harness's SHA-256 is correct.** Native SHA-256 of a stored ELY-0450 snapshot equals its stored `sha256`.
4. **The states differ by one ULP.** Regenerating seed 11039 `high` natively gives the same tick, but **77 numeric fields differ by at most 1.11e-16**, which is a single rounding step on the neural weights.

That matches the ELY-0439 README's own finding: `Math.tanh` / `Math.exp` are implementation-approximated, so the connector's V8 harness and native Node round them differently. Every test that pins a hash over raw float state therefore breaks off-harness.

## Suggested fix (for future experiments)

- Hash a **quantized** view of the state, e.g. round floats to 12 significant digits before `JSON.stringify`, and keep the raw-state hash as an informational field only.
- Or split the checks: exact equality for discrete facts (ticks, IDs, food, events) and a tolerance (say 1e-12) for weights.
- Record which runtime produced each pinned hash, so a mismatch can be told apart from real drift.

Old artifacts shouldn't be rewritten. This is a convention to adopt going forward, plus an explanation of why these tests fail.
