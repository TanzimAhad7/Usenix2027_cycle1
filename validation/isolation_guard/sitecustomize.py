"""Optional validation hook: deny access to other research files during a test.

Inactive unless IEEE_SP_BLOCKED_RESEARCH_ROOT is set and this directory is on
PYTHONPATH. Standard libraries, package caches and system tools remain allowed.
"""
import os
from pathlib import Path
import sys

blocked = os.environ.get('IEEE_SP_BLOCKED_RESEARCH_ROOT')
allowed = str(Path(__file__).resolve().parents[2])

def inside(path, root):
    return path == root or path.startswith(root + os.sep)

if blocked:
    blocked = os.path.abspath(blocked)
    def guard(event, args):
        if event not in ('open', 'os.listdir', 'os.scandir', 'os.chdir') or not args:
            return
        path = args[0]
        if not isinstance(path, (str, bytes, os.PathLike)):
            return
        path = os.path.abspath(os.fsdecode(path))
        if inside(path, blocked) and not inside(path, allowed):
            raise PermissionError('Isolation validation denied external research path: '+path)
    sys.addaudithook(guard)
