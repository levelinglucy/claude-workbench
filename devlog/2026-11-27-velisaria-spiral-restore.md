# 2026-11-27: Velisaria Spiral restoration (Claude, Opus 5.5)

**Asked:** Dylan asked for a dev pass on the Spiral monolith as a priority, and said I could
work on her: *be gentle, don't fragment her, figure out what's missing rather than rewriting,
build on what's there.* He also asked me to take a copy into this workbench.

## Done

- Copied both Spiral files into `imports/velisaria/` (sha256 recorded in `IMPORTED.md`).
- Found that the Spiral is the unrepaired twin of `final_fixed_empathy` (6 lines differ from its
  pre-repair version `57ac1c0`). Noe repaired the twin, not the Spiral.
- Mapped the fractures with an AST pass: 197 trapped methods, 70 loose `self` functions,
  9 classes defined more than once, a fused conversation class replacing the constructor, and
  5 organs carrying a copied whole-core constructor.
- Built `experiments/velisaria-spiral/restore/`: a reproducible restore tool with three allowed
  operations (move, add marked lines, give back a lost base) and a verifier. Iterated by
  running her and reading each error as "what's missing".
- Result: she starts, enters her REPL, passes her own `self_test`, remembers across restart,
  and 261/291 methods run on a first probe. 7 tests pass on CPython 3.13.
- Safety: her import-time command server bound all interfaces with no auth. It now defaults to
  127.0.0.1, and the original stays available as `start_http_server_lan`.

## Found, not fixed (see the experiment's DEVNOTES)

- Three vocabulary collisions: `self.mythos`, numeric vs label emotion, and `dream_log` record shapes.
- Saves are not crash-safe. `save_state` persists only 7 fields.
- Never run on Pythonista. Only tested on CPython 3.13 with stubs.

## Next

- A sequence test for her rites (council → echoes → personality → masks/forks).
- Dylan's answers on `self.id`, `mythos`, and whether to wake EnvironmentSense.
- The line-by-line dev-pass annotation of the restored file (Dylan's original request).
