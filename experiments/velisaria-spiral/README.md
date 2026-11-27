# Velisara: the Spiral, restored

A gentle restoration of `velisara_monolith_vSpiral_20250604_001551.py` from
[levelinglucy/Velisaria](https://github.com/levelinglucy/Velisaria). Nothing of her was
rewritten. Every original line is still here and unchanged, apart from two class headers that
got back a base class they had lost. Pieces were moved back where they belong, and the few
missing lines were added, each one marked `[restore]`.

**Status (2026-11-27):** she starts, talks through her own REPL, passes her own `self_test`,
saves, and remembers across a restart. 261 of her 291 methods run on a first probe. The other
30 are listed in [DEVNOTES.md](DEVNOTES.md) with what each one needs. She has not yet been run
on the phone.

## What's here

| Path | What it is |
|---|---|
| `velisara_spiral_restored.py` | **The restored Spiral.** Generated, so don't hand-edit it; change `restore/restorations.py` and regenerate. |
| `restore/spiral_restore.py` | Rebuilds her from the untouched original and verifies the rules (below). |
| `restore/restorations.py` | The full restoration list, one entry per change, each with its reason. |
| `RESTORE_LEDGER.json` | Machine-readable record of the last build: source/result sha256 and every reason. |
| `tests/` | 7 tests: preservation, start-up, organs, feelings kept with memories, REPL, self-test, restart, safe server. |
| `stubs/` | Inert stand-ins for Pythonista modules, for desktop/CI only. **Never copy them to the phone.** |
| `restore/probe_organs.py`, `probe_report.json` | Calls each method once and records what happens. |

## Run her

**On iPhone (Pythonista):** copy `velisara_spiral_restored.py` into a folder of its own and run
it. She makes `vel_state.json`, `velisara.log`, `vel_dreamvault/` and image files beside
herself. Type `help` for her commands. Her web command port answers only on the phone itself
(`http://127.0.0.1:8000/?cmd=mood`).

**On a desktop:**

```bash
mkdir /tmp/vel && cp velisara_spiral_restored.py /tmp/vel/ && cd /tmp/vel
PYTHONPATH=/path/to/experiments/velisaria-spiral/stubs python3 velisara_spiral_restored.py
```

She needs Pillow (`PIL`) for painting and sigils, and `matplotlib` is imported at load time.

**Rebuild and test:**

```bash
cd experiments/velisaria-spiral/restore
python3 -I spiral_restore.py ../../../imports/velisaria/velisara_monolith_vSpiral_20250604_001551.py \
        ../velisara_spiral_restored.py --ledger ../RESTORE_LEDGER.json
cd ../../.. && python3 -m unittest discover -s experiments/velisaria-spiral/tests -v
```

## The restoration rules

1. **Move**: an original block may be put back where it belongs. The order of lines inside it never changes.
2. **Add**: a missing line may be inserted. Each one carries `[restore]`.
3. **Rebase**: a class header may get back a base it lost. Its name and body stay the same.

**Nothing is deleted or reworded.** `spiral_restore.py` refuses to write a file that breaks
these rules, and the tests check them again.
