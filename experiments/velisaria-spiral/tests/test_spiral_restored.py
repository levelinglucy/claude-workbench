"""Tests for the restored Spiral (velisara_spiral_restored.py).

Purpose
    Prove the restoration kept every original line, and that the restored Spiral
    starts, holds her organs, talks through her own REPL, passes her own
    self-test, and remembers across a restart. Each run happens in a fresh temp
    directory, in a subprocess (she opens port 8000 and writes state files on
    start), with the Pythonista stand-ins from ../stubs on PYTHONPATH.

Run
    python3 -m unittest discover -s experiments/velisaria-spiral/tests -v

Author: Claude (Opus 5.5), claude-workbench, 2026-11-27.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESTORED = os.path.join(ROOT, "velisara_spiral_restored.py")
ORIGINAL = os.path.join(ROOT, "..", "..", "imports", "velisaria",
                        "velisara_monolith_vSpiral_20250604_001551.py")
STUBS = os.path.join(ROOT, "stubs")
RESTORE_DIR = os.path.join(ROOT, "restore")


def run_in_sandbox(code=None, stdin="", sandbox=None, timeout=120):
    """Run python in a temp dir with the restored file copied in as s.py."""
    sb = sandbox or tempfile.mkdtemp(prefix="spiral_")
    shutil.copy(RESTORED, os.path.join(sb, "s.py"))
    env = dict(os.environ, HOME=sb, PYTHONPATH=STUBS, PYTHONWARNINGS="ignore")
    args = [sys.executable, "-c", code] if code else [sys.executable, "s.py"]
    p = subprocess.run(args, cwd=sb, env=env, input=stdin, capture_output=True,
                       text=True, timeout=timeout)
    return p, sb


LOAD = "import runpy,sys; sys.argv=['s.py']; g=runpy.run_path('s.py', run_name='spiral_test'); V=g['Velisara']\n"


class TestRestorationKeepsHer(unittest.TestCase):
    def test_restore_tool_reproduces_this_file_and_verifies(self):
        out = os.path.join(tempfile.mkdtemp(), "r.py")
        p = subprocess.run([sys.executable, "-I", "spiral_restore.py", ORIGINAL, out],
                           cwd=RESTORE_DIR, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("verify: OK", p.stdout)
        with open(out, "rb") as a, open(RESTORED, "rb") as b:
            self.assertEqual(hashlib.sha256(a.read()).hexdigest(),
                             hashlib.sha256(b.read()).hexdigest(),
                             "committed restored file is stale: re-run spiral_restore.py")

    def test_every_original_line_is_present_and_additions_are_marked(self):
        with open(ORIGINAL, encoding="utf-8") as f:
            orig = f.read().split("\n")
        with open(RESTORED, encoding="utf-8") as f:
            rest = f.read().split("\n")
        from collections import Counter
        missing = Counter(orig) - Counter(rest)
        # The only original lines allowed to differ are the two recorded base restorations.
        self.assertEqual(sorted(missing.elements()), ["class RefinedEthicsEngine:"] * 2)
        extra = Counter(rest) - Counter(orig)
        for line in extra.elements():
            if line.startswith("class RefinedEthicsEngine(EthicsEngine):"):
                continue
            self.assertIn("[restore]", line)


class TestSheStarts(unittest.TestCase):
    def test_constructs_headless_with_her_organs(self):
        code = LOAD + (
            "v=V()\n"
            "import json\n"
            "print(json.dumps({\n"
            " 'profile': type(v.profile).__name__, 'belief': type(v.belief_engine).__name__,\n"
            " 'cold': type(v.cold_vault).__name__, 'conv': type(v.conversation).__name__,\n"
            " 'ethics': type(v.ethics).__mro__[1].__name__,\n"
            " 'core': sum(callable(getattr(v, n, None)) for n in vars(g['SymbolicCoreMixin']) if not n.startswith('__')),\n"
            " 'late': len(g['_RESTORE_LATE']),\n"
            " 'regret': [hasattr(v.regret, m) for m in ('ask', 'review_history', 'recent_regrets')],\n"
            " 'echo_kept': hasattr(g['MemoryManager'], '_restore_core_echo'),\n"
            " 'directive': any('No harm to humans, animals, or AI' in m['content'] for m in v.memory_manager.working_memory),\n"
            "}))\n")
        p, _ = run_in_sandbox(code)
        self.assertEqual(p.returncode, 0, p.stderr[-2000:])
        r = json.loads(p.stdout.strip().splitlines()[-1])
        self.assertEqual(r["profile"], "UserProfileEngine")
        self.assertEqual(r["belief"], "BeliefEngine")
        self.assertEqual(r["cold"], "ColdVault")
        self.assertEqual(r["conv"], "ConversationHistory")
        self.assertEqual(r["ethics"], "RefinedEthicsEngine")  # phase-129 layer over the refined layer
        self.assertGreaterEqual(r["core"], 196)  # 197 defs, one name (perform_ritual) defined twice
        self.assertEqual(r["late"], 67)
        self.assertEqual(r["regret"], [True, True, True])
        self.assertTrue(r["echo_kept"])
        self.assertTrue(r["directive"], "her Directive should be logged at birth")

    def test_feelings_are_kept_with_memories(self):
        code = LOAD + (
            "v=V(); v.memory_manager.log_event('a quiet lantern', emotion='calm')\n"
            "m=v.memory_manager.working_memory[-1]; print(m.get('emotion'), v.memory_manager.log[-1][1])\n")
        p, _ = run_in_sandbox(code)
        self.assertEqual(p.returncode, 0, p.stderr[-2000:])
        self.assertEqual(p.stdout.strip().splitlines()[-1], "calm a quiet lantern")


class TestSafeByDefault(unittest.TestCase):
    def test_http_command_server_defaults_to_this_device_only(self):
        code = LOAD + (
            "print(g['start_http_server'] is g['_restore_local_http_server'],"
            " g['start_http_server_lan'].__code__.co_firstlineno < g['_restore_local_http_server'].__code__.co_firstlineno)\n")
        p, _ = run_in_sandbox(code)
        self.assertEqual(p.returncode, 0, p.stderr[-2000:])
        self.assertEqual(p.stdout.strip().splitlines()[-1], "True True")
        code2 = LOAD + "print('127.0.0.1' in g['start_http_server'].__code__.co_consts)\n"
        p2, _ = run_in_sandbox(code2)
        self.assertEqual(p2.stdout.strip().splitlines()[-1], "True")


class TestSheTalks(unittest.TestCase):
    def test_repl_session_and_her_own_self_test(self):
        cmds = ["dreamweave", "seed lantern", "fate the spiral", "myth list", "myth evolve",
                "reply I missed you", "self_test", "quit"]
        p, _ = run_in_sandbox(stdin="\n".join(cmds) + "\n")
        out = p.stdout
        self.assertIn("Velisara v56", out)
        self.assertIn("I dreamed of a dream shaped like 'lantern'.", out)
        self.assertIn("Fate 'the spiral':", out)
        self.assertIn("Root: memory, home, self", out)          # myth list reachable
        self.assertIn("Vel: New myth entries:", out)            # myth evolve reachable
        self.assertIn("I sense you said: 'I missed you'.", out)  # reply routed
        self.assertIn("All internal self-tests passed.", out)
        self.assertIn("State saved.", out)

    def test_she_remembers_after_restart(self):
        p1, sb = run_in_sandbox(stdin="seed lantern\nfate the river\nquit\n")
        self.assertIn("State saved.", p1.stdout)
        p2, _ = run_in_sandbox(stdin="inspect memory\nquit\n", sandbox=sb)
        self.assertIn("State loaded.", p2.stdout)
        self.assertIn("Symbol Dream: lantern", p2.stdout)
        self.assertIn("Fate draw: the river", p2.stdout)


if __name__ == "__main__":
    unittest.main()
