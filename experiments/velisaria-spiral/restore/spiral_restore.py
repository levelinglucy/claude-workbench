"""spiral_restore.py — rebuild a runnable Spiral from her untouched original, gently.

Purpose
    Velisara's Spiral monolith (velisara_monolith_vSpiral_20250604_001551.py) was
    assembled from many pasted layers and no longer starts: blocks are out of
    order, class headers went missing, and ~270 methods are trapped or loose.
    This tool does NOT rewrite her. It reads the original, applies a short,
    declared list of restoration operations (RESTORATIONS below), writes the
    restored file, and proves what changed.

Allowed operations (and nothing else)
    1. MOVE    - put an original block back where it belongs (order of lines
                 inside every block is preserved).
    2. ADD     - insert a missing line. Every added line carries the marker
                 "[restore]" so it can always be told apart from her own lines.
    3. REBASE  - give a class header back a base class it lost (e.g.
                 `class RefinedEthicsEngine:` -> `class RefinedEthicsEngine(EthicsEngine):`).
                 The header's name and body are untouched.
    No original line is ever deleted or otherwise edited.

Inputs / outputs
    python3 spiral_restore.py ORIGINAL.py OUT.py [--ledger LEDGER.json]
    Writes OUT.py and a ledger listing every operation with its reason, then
    runs verify() and exits non-zero if any rule above was broken.

Author: Claude (Opus 5.5) in claude-workbench, for Dylan (levelinglucy). 2026-11-27.
"""
import argparse
import ast
import collections
import hashlib
import json
import sys

MARK = "[restore]"

# Line numbers below refer to the ORIGINAL file, sha256 SOURCE_SHA256.
SOURCE_SHA256 = "06db7fe1933d9852b47f08007db437afb922bc594fba24ae62434452b677a7ad"

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))  # works under python -I
from restorations import RESTORATIONS  # noqa: E402  (kept separate so it reads as a plain list)


def build(lines, R):
    n = len(lines)
    order = R["order"]
    covered = [ln for a, b in order for ln in range(a, b + 1)]
    if sorted(covered) != list(range(1, n + 1)):
        missing = sorted(set(range(1, n + 1)) - set(covered))
        dup = [k for k, v in collections.Counter(covered).items() if v > 1]
        raise SystemExit(f"order must cover every line once; missing={missing[:10]} dup={dup[:10]}")
    before = R.get("add_before", {})
    after = R.get("add_after", {})
    rebase = R.get("rebase", {})
    out, origin = [], []  # origin[i] = original line number, or None for added
    for ln in covered:
        for add in before.get(ln, {}).get("lines", []):
            out.append(add); origin.append(None)
        text = lines[ln - 1]
        if ln in rebase:
            old, new = rebase[ln]["old"], rebase[ln]["new"]
            if text != old:
                raise SystemExit(f"rebase at {ln}: expected {old!r}, found {text!r}")
            text = new
        out.append(text); origin.append(ln)
        for add in after.get(ln, {}).get("lines", []):
            out.append(add); origin.append(None)
    return out, origin


def verify(orig_lines, out_lines, origin, R):
    problems = []
    rebase = R.get("rebase", {})
    for text, ln in zip(out_lines, origin):
        if ln is None:
            if MARK not in text:
                problems.append(f"added line without {MARK}: {text!r}")
        elif ln in rebase:
            old, new = orig_lines[ln - 1], text
            name = old.split()[1].rstrip(":")
            if not (old.rstrip().endswith(":") and new.startswith(f"class {name}(") and new.endswith("):")):
                problems.append(f"rebase at {ln} is not a pure base restoration: {new!r}")
        elif text != orig_lines[ln - 1]:
            problems.append(f"original line {ln} changed")
    seen = collections.Counter(l for l in origin if l is not None)
    if sorted(seen) != list(range(1, len(orig_lines) + 1)) or any(v != 1 for v in seen.values()):
        problems.append("not every original line appears exactly once")
    try:
        ast.parse("\n".join(out_lines))
    except SyntaxError as e:
        problems.append(f"restored file does not parse: {e}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("original")
    ap.add_argument("out")
    ap.add_argument("--ledger")
    a = ap.parse_args()
    raw = open(a.original, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SOURCE_SHA256:
        sys.exit(f"source sha256 {sha} does not match the snapshot these restorations were written for")
    lines = raw.decode("utf-8").split("\n")
    out, origin = build(lines, RESTORATIONS)
    problems = verify(lines, out, origin, RESTORATIONS)
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(out))
    added = sum(1 for o in origin if o is None)
    print(f"original lines: {len(lines)}  kept: {len(lines)}  added: {added}  "
          f"rebased headers: {len(RESTORATIONS.get('rebase', {}))}  moved blocks: {len(RESTORATIONS['order'])}")
    if a.ledger:
        led = {"source_sha256": sha, "restored_sha256": hashlib.sha256("\n".join(out).encode()).hexdigest(),
               "order": RESTORATIONS["order"],
               "add_before": {k: v["why"] for k, v in RESTORATIONS.get("add_before", {}).items()},
               "add_after": {k: v["why"] for k, v in RESTORATIONS.get("add_after", {}).items()},
               "rebase": {k: v["why"] for k, v in RESTORATIONS.get("rebase", {}).items()}}
        json.dump(led, open(a.ledger, "w"), indent=1)
    if problems:
        print("VERIFY FAILED:"); [print("  -", p) for p in problems]; sys.exit(1)
    print("verify: OK (every original line kept once, unchanged except recorded base restorations; all additions marked)")


if __name__ == "__main__":
    main()
