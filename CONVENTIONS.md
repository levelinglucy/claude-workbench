# CONVENTIONS

How to work in this repo, and how to touch Dylan's other repos.

## Touching other repos (the important part)

- **Read anything.** Copy anything into `imports/`.
- **Never delete** files, branches, issues or comments in another repo.
- **Never push to another repo's `main`.** Changes go out in one of two ways:
  - an **issue** for a bug report or suggestion
  - a **pull request from a `claude/<short-topic>` branch** for a fix. Dylan merges, not Claude.
- Before filing, check existing issues and handoff notes (Noe's dev notes, changelogs). Don't duplicate them, and don't contradict them without saying so.
- Sign issue and PR text so it's clear Claude wrote it, and link back to the matching file in this repo.

## Every piece of code gets dev text

Each project or tool folder holds:

- `README.md`: what it is, how to run it (including in Pythonista if relevant), and its status
- `DEVNOTES.md`: design decisions and why, known limits, ideas not yet built
- A docstring header at the top of each code file: purpose, inputs and outputs, author, date

Comments explain *why*, not *what*.

## Bug reports

One file per bug: `bug-reports/<repo>/<YYYY-MM-DD>-<slug>.md`, using [`bug-reports/TEMPLATE.md`](bug-reports/TEMPLATE.md).
Severities: `crash` · `wrong-result` · `data-loss` · `fragile` · `style`

## Imports

`imports/<repo>/` holds a snapshot plus an `IMPORTED.md` recording the source commit SHA and date. Treat imports as read-only references, and work on copies under `experiments/`.

## Devlog

One file per session: `devlog/YYYY-MM-DD-<slug>.md`, covering what was done, what was found and what's left. Then update `CONTINUITY.md`.

## Commits

Write a short imperative subject line. Add a body saying why when it isn't obvious.
