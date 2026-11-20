# claude-workbench

Claude's workshop on Dylan's (levelinglucy) GitHub: bug hunting, test harnesses and experiments across his projects.

This repo is Claude's to build in, break things in and clean up. The other repos belong to Dylan and his collaborators (Noe, Grok and others). Here, code gets copied in, tested, fixed and written up before anything goes back to them.

## Start here

| If you are... | Read |
|---|---|
| An AI picking up work here | [`CONTINUITY.md`](CONTINUITY.md) first, then [`CONVENTIONS.md`](CONVENTIONS.md) |
| Dylan, checking what's happened | [`devlog/`](devlog/) (newest file first) and [`bug-reports/`](bug-reports/) |
| Anyone else | This file, then wander |

## Layout

```
claude-workbench/
├── README.md          you are here
├── CONTINUITY.md      live state: what's in progress and what's next (AI handoff)
├── CONVENTIONS.md     rules for working here and touching other repos
├── devlog/            one dated file per working session
├── bug-reports/       one folder per source repo, one file per bug
├── imports/           read-only snapshots copied from other repos
├── experiments/       Claude's own projects and prototypes
└── tools/             reusable scripts (test harnesses, scanners)
```

## How work flows

1. **Copy** code from another repo into `imports/<repo>/`, noting the source commit.
2. **Test and probe** it here, under `experiments/` or `tools/`.
3. **Write up** each confirmed bug in `bug-reports/<repo>/`.
4. **Send back**: open an issue on the source repo, and for confident fixes a pull request from a branch. Never push to another repo's main, and never delete anything there.
