"""Inert stand-in for Pythonista's 'ui' module, for running the Spiral headless on a desktop/CI.

Never copy this onto the phone: Pythonista provides the real module. Every attribute
is a harmless no-op object; CALLS records which names were asked for, so a test can
see that she reached for a sensor without anything being sensed.
Author: Claude (Opus 5.5), claude-workbench, 2026-11-27.
"""
from _anything import Anything as _A
CALLS = []


def __getattr__(name):
    if name.startswith('__'):
        raise AttributeError(name)
    CALLS.append(name)
    return _A()


class View:
    """Base for her ui.View subclasses (LogViewer, HelpView, DreamIndexView ...)."""
    def __init__(self, *a, **k):
        pass

    def __getattr__(self, n):
        if n.startswith('__'):
            raise AttributeError(n)
        return _A()
