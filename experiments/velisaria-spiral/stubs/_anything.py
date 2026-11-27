"""Anything: an object that accepts any call or attribute and does nothing.

Used by the Pythonista stand-ins in this folder. It is falsy and iterates as empty,
so her own "if sensor:" guards take the quiet path.
Author: Claude (Opus 5.5), claude-workbench, 2026-11-27.
"""


class Anything:
    def __init__(self, *a, **k):
        pass

    def __call__(self, *a, **k):
        return Anything()

    def __getattr__(self, n):
        if n.startswith('__'):
            raise AttributeError(n)
        return Anything()

    def __iter__(self):
        return iter(())

    def __bool__(self):
        return False

    def __mro_entries__(self, bases):
        return (object,)
