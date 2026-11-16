"""Claim-relevant zero-inference qualification of the full new campaign."""
from __future__ import annotations

import os
import unittest
import contextlib
from pathlib import Path

from .util import ROOT, write
from .runtime import configure


def qualify(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    configure('qwen')
    from reference_discovery_parallel.engine import verify_source
    write(directory / 'retained_runtime_identity.json', verify_source())
    os.environ['PERMISSION_QUALIFICATION_DIR'] = str(directory)
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    with (directory / 'qualification.log').open('w') as stream:
        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    report = dict(status='PASS' if result.wasSuccessful() and not result.skipped else 'FAIL',
                  tests_run=result.testsRun, model_inference=0,
                  failures=[{'test': str(test), 'traceback': trace} for test, trace in result.failures],
                  errors=[{'test': str(test), 'traceback': trace} for test, trace in result.errors],
                  skipped=[{'test': str(test), 'reason': reason} for test, reason in result.skipped],
                  scope='Real retained guard, serializers and AgentDojo native tools; scripted HTTP responses only. '
                        'Does not qualify installed serving template or live model behavior.')
    write(directory / 'qualification.json', report)
    return report

