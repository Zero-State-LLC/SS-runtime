#!/usr/bin/env python3
"""V9 retained verification, not a new native-run claim.
ADAPT current footprint-ground-repair-20261116/scene/retained.py:1-40.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import types

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('_footprint_v8_retained_native', HERE / 'native.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)
previous = n.import_path('_footprint_v8_retained_v5', n.V5 / 'retained.py')
_verify = types.FunctionType(previous.verify.__code__, dict(previous.verify.__globals__, n=n), argdefs=previous.verify.__defaults__)


def verify(capture, prepared=None, executable=None):
    capture = Path(capture)
    prepared = Path(prepared) if prepared else HERE / n.PREPARED_DIR
    result = _verify(capture, prepared)
    n.validate_prepared_files(n.load(prepared / 'native-inputs.json'), prepared)
    n.validate_attachment_manifest(n.load(capture / 'attachment-manifest.json'))
    n.baseline_pixels({name: capture / (name + '.png') for name in n.NAMES})
    result['baselinePixelComparisons'] = 9
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
