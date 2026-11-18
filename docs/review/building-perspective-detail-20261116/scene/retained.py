#!/usr/bin/env python3
"""V7 retained bytes/contract check, never a new native-run claim.
ADAPT scene-qa-repair-20261116/retained.py:16-91 with private v7 globals.
Optionally recheck the actual built executable; otherwise report preserved import
agreement, never imply the historical build still exists on this machine.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import types

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('_building_v7_native_retained', HERE / 'native.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)
_previous = n.import_path('_building_v7_retained_v5', n.V5 / 'retained.py')
_verify = types.FunctionType(_previous.verify.__code__, dict(_previous.verify.__globals__, n=n),
                             name='verify_v7_bytes', argdefs=_previous.verify.__defaults__)


def verify(capture, prepared=None, executable=None):
    capture = Path(capture)
    result = _verify(capture, Path(prepared) if prepared else HERE / n.PREPARED_DIR)
    n.validate_attachment_manifest(n.load(capture / 'attachment-manifest.json'))
    if executable is not None:
        n.validate_executable(n.load(capture / 'source-scene-records.json'), Path(executable))
        result['binaryCheck'] = 'actual built executable rehashed and matched to retained loaded executable'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture', type=Path)
    parser.add_argument('--prepared', type=Path)
    parser.add_argument('--test-executable', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.capture, args.prepared, args.test_executable), indent=2))
