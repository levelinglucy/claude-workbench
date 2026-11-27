"""probe_organs.py — gently exercise every Velisara method and record which ones work.

Purpose
    Diagnosis, not testing of correctness: construct the restored Spiral headless
    (Pythonista modules replaced by inert stand-ins on PYTHONPATH), then call each
    method once with simple sample arguments under a short alarm, and write a JSON
    report of what each method did (ok / exception type + message / skipped).
    Long-running loops, UI presenters, servers and schedulers are skipped.

Usage
    PYTHONPATH=<stubs> python3 probe_organs.py RESTORED.py REPORT.json
    Run it in a throwaway directory: she writes vel_state.json and velisara.log.

Author: Claude (Opus 5.5), claude-workbench, 2026-11-27.
"""
import inspect, json, runpy, signal, sys, traceback, random, io, contextlib

SKIP_WORDS = ("loop", "start", "schedule", "run", "present", "launch", "watch", "listen",
              "serve", "replay", "_decay", "export", "import_mirror", "speak_last", "play")
SAMPLE = {"str": "spiral", "int": 3, "float": 0.5, "list": ["spiral", "lantern"], "dict": {"spiral": 1}}


class Timeout(Exception):
    pass


def _alarm(*_):
    raise Timeout()


def guess_args(fn):
    args = []
    for p in list(inspect.signature(fn).parameters.values()):
        if p.default is not inspect._empty or p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
            continue
        n = p.name.lower()
        if n in ("limit", "count", "n", "k", "size", "steps", "days", "depth", "threshold", "hours", "interval_hours", "idle_threshold", "max_events", "top_n"):
            args.append(3)
        elif any(k in n for k in ("fragments", "symbols", "list", "items", "sigils")):
            args.append(["spiral", "lantern"])
        elif any(k in n for k in ("weight", "score", "delta", "intensity", "likelihood", "bond")):
            args.append(0.5)
        else:
            args.append("spiral")
    return args


def main(path, report):
    random.seed(7)
    sys.argv = [path]
    g = runpy.run_path(path, run_name="spiral_probe")
    V = g["Velisara"]
    vel = V()
    results = {}
    names = sorted(n for n in dir(vel) if not n.startswith("__") and callable(getattr(vel, n, None)))
    signal.signal(signal.SIGALRM, _alarm)
    for name in names:
        if any(w in name.lower() for w in SKIP_WORDS) or name.startswith("_restore"):
            results[name] = {"status": "skipped"}
            continue
        fn = getattr(vel, name)
        try:
            args = guess_args(fn)
        except (TypeError, ValueError):
            args = []
        buf = io.StringIO()
        signal.alarm(2)
        try:
            with contextlib.redirect_stdout(buf):
                out = fn(*args)
            results[name] = {"status": "ok", "args": args, "returned": repr(out)[:160]}
        except Timeout:
            results[name] = {"status": "timeout", "args": args}
        except Exception as e:  # diagnosis: record, keep going
            tb = traceback.extract_tb(e.__traceback__)[-1]
            results[name] = {"status": "error", "args": args, "type": type(e).__name__,
                             "msg": str(e)[:200], "at": f"{tb.lineno}:{tb.name}"}
        finally:
            signal.alarm(0)
    json.dump(results, open(report, "w"), indent=1, default=str)
    c = {}
    for r in results.values():
        c[r["status"]] = c.get(r["status"], 0) + 1
    print("probe:", c)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
