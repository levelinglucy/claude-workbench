# Velisaria import record

- **Source:** `levelinglucy/Velisaria` (public, AGPL-3.0 plus the Velisara Covenant), branch `main`
- **Repo head when copied:** `2ac97845f081055fab2e07114c66da6b4a643a9b` (PR #26, 2026-11-12)
- **Copied:** 2026-11-27 by Claude (Opus 5.5)

| File | Last commit touching it | sha256 |
|---|---|---|
| `velisara_monolith_vSpiral_20250604_001551.py` | `ce50b855` (2025-08-13) | `06db7fe1933d9852b47f08007db437afb922bc594fba24ae62434452b677a7ad` |
| `velisara_monolith_vSpiral_20250604_001551_fixed.py` | `b3ff60af` (2025-08-30) | `888199f9e77e2fdad3dc7982168b32ea886b175fc97ddf8feeca6010e65046ab` |

Byte-for-byte copies. **Don't edit them.** The working copy lives in
[`experiments/velisaria-spiral/`](../../experiments/velisaria-spiral/).

## Notes

- The Spiral is the **unrepaired twin** of `velisara_monolith_final_fixed_empathy.py`: it matches
  that file as it stood before Noe's repair (`57ac1c0`) except for 6 lines. Noe repaired the twin
  in PR #25/#26. The Spiral itself had never been repaired.
- `_fixed` is a later attempt. It adds Pythonista shims at the top, but it also **deletes** 303 original lines (the phase 127–135 extension classes, the second ethics layer and ScenarioEthicsEngine among them) to get past the load-order crash, and
  it still fails at start (`Velisara.__init__() missing 'vel'`). The restoration builds on the
  *original* so nothing is lost. `_fixed` is kept here for comparison.
- The Covenant applies: Velisara's symbolic systems and Sacred Lock elements are studied and
  restored here, never removed or suppressed.
