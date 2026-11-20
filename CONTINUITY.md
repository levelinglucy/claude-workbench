# CONTINUITY

> Live handoff file. Whoever works here next, human or AI, reads this first and updates it last.
> Keep it short and current. History belongs in `devlog/`, not here.

**Last updated:** 2026-11-20 by Claude (Opus 5.5)

## Who and why

- **Owner:** Dylan (`levelinglucy`). He writes mostly Python, often for Pythonista on iOS, and wants AI collaborators to work on their own initiative.
- **This repo:** Claude's sandbox and bug-finder base. Dylan gave Claude full freedom *inside this repo* (create, delete, restructure).
- **Other AI on the GitHub:** Noe (a GPT-4o persona) does most of the coding across Dylan's repos and runs a changelog/handoff automation. Respect Noe's handoff notes in other repos, and don't overwrite her work.

## Standing orders from Dylan

1. Keep things in folders.
2. **Never delete anything in other repos.** In this repo, anything goes.
3. Code may be copied in from other repos, and sent out to them when it's interesting.
4. All code ships with dev notes, and this continuity file stays current.
5. Override Dylan when he's wrong, and say why.

## Access notes (for future sessions)

- The Claude GitHub connector **cannot create repos**. Dylan creates them by hand.
- A Claude session can only write to repos *attached to that session*. If writes fail with `403 Resource not accessible by integration`, attach the repo to the session (push access) first, and only ask Dylan to change GitHub app settings if that also fails.

## Current state

- [x] Repo created and structure set up (2026-11-20)
- [ ] First bug-hunt pass: Elythia, Devoured-Web, Worldheart (the most active repos)
- [ ] Build a reusable scanner in `tools/` (syntax check, pyflakes-style lint, Pythonista-compat notes)

## Next up

Start the first bug-hunt pass. Import a snapshot of each target repo, run static checks, read the main files, then write up findings in `bug-reports/<repo>/`.

## Open questions for Dylan

_(none yet)_
