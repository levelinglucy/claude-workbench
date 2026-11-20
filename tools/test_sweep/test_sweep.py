"""
test_sweep.py - run every test file in a repo and report which ones fail.

Purpose:
    First-pass bug finder. Walks a checked-out repo, finds Python
    (test_*.py) and Node (test*.cjs / test*.mjs / test.cjs) test files,
    runs each one in isolation with a timeout, and writes a JSON + Markdown
    summary of passes, failures, errors and timeouts.

Inputs:
    repo          path to a checkout (never modified: tests run in a temp copy)
    --out DIR     where to write sweep.json and sweep.md (default: cwd)
    --timeout S   per-test timeout in seconds (default: 120)
    --only GLOB   restrict to test files whose repo-relative path matches GLOB

Outputs:
    DIR/sweep.json   one record per test file: path, runner, status, seconds, tail of output
    DIR/sweep.md     human summary, failures first

Why a temp copy: many research tests write SQLite files, checkpoints and logs
next to themselves. Running in place would dirty someone else's repo.

Why each Python test runs from its own directory with that directory on
PYTHONPATH: that's how the repos' READMEs and CI tend to run them. Tests
that need extra PYTHONPATH entries (another experiment's source) will show as
import errors. Those are triaged by hand against the CI workflow before
anything is called a bug.

Author: Claude (Opus 5.5) for levelinglucy/claude-workbench, 2026-11-20
"""

import argparse
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PY_PATTERNS = ("test_*.py",)
NODE_PATTERNS = ("test_*.cjs", "test_*.mjs", "test.cjs", "test.mjs", "test-*.cjs")
SKIP_DIRS = {".git", "node_modules", "__pycache__"}


def find_tests(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            p = Path(dirpath) / name
            if any(fnmatch.fnmatch(name, pat) for pat in PY_PATTERNS):
                yield p, "python"
            elif any(fnmatch.fnmatch(name, pat) for pat in NODE_PATTERNS):
                yield p, "node"


def run_one(path: Path, runner: str, timeout: int):
    cwd = path.parent
    env = dict(os.environ)
    if runner == "python":
        env["PYTHONPATH"] = str(cwd) + os.pathsep + env.get("PYTHONPATH", "")
        cmd = [sys.executable, "-m", "unittest", "-q", path.stem]
    else:
        # Prefer node's built-in test runner when the file uses node:test;
        # plain scripts just run and signal failure by exit code.
        text = path.read_text(errors="replace")
        cmd = ["node", "--test", path.name] if "node:test" in text else ["node", path.name]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                           text=True, timeout=timeout)
        out = (r.stdout + "\n" + r.stderr).strip()
        if r.returncode == 0:
            status = "pass"
        elif "ModuleNotFoundError" in out or "Cannot find module" in out \
                or "ImportError" in out:
            status = "import-error"
        else:
            status = "fail"
    except subprocess.TimeoutExpired as e:
        out = ((e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes)
               else (e.stdout or ""))
        status = "timeout"
    return status, round(time.time() - t0, 1), out[-2500:]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    ap.add_argument("repo")
    ap.add_argument("--out", default=".")
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    src = Path(args.repo).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="sweep_") as tmp:
        work = Path(tmp) / src.name
        shutil.copytree(src, work, ignore=shutil.ignore_patterns(".git"))
        tests = sorted(find_tests(work))
        if args.only:
            tests = [(p, r) for p, r in tests
                     if fnmatch.fnmatch(str(p.relative_to(work)), args.only)]
        results = []
        for i, (p, runner) in enumerate(tests, 1):
            rel = str(p.relative_to(work))
            status, secs, tail = run_one(p, runner, args.timeout)
            results.append({"path": rel, "runner": runner, "status": status,
                            "seconds": secs, "tail": tail})
            print(f"[{i}/{len(tests)}] {status:12} {secs:6.1f}s  {rel}", flush=True)

    (out_dir / "sweep.json").write_text(json.dumps(results, indent=2))
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    order = {"fail": 0, "timeout": 1, "import-error": 2, "pass": 3}
    lines = [f"# Test sweep: {src.name}", "",
             "| status | count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(counts.items(), key=lambda kv: order.get(kv[0], 9))]
    lines += ["", "## Not passing", ""]
    for r in sorted(results, key=lambda r: order.get(r["status"], 9)):
        if r["status"] != "pass":
            lines.append(f"- **{r['status']}** `{r['path']}` ({r['seconds']}s)")
    (out_dir / "sweep.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
