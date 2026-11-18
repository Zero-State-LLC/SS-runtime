#!/usr/bin/env python3
"""Portable v6 retained verification through unchanged v5 byte/provenance guards."""
import argparse
import importlib.util
import json
from pathlib import Path
import types

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('_scene_framing_retained_native_v6', HERE / 'native.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)
_previous = n.import_path('_scene_framing_retained_strict_v5', n.V5 / 'retained.py')
# Private function globals, not a mutation of v5's module, validator, or files.
_verify = types.FunctionType(_previous.verify.__code__, dict(_previous.verify.__globals__, n=n),
                             name='verify_v6_bytes', argdefs=_previous.verify.__defaults__)


def verify(capture, prepared=None):
    return _verify(Path(capture), Path(prepared) if prepared else HERE / n.PREPARED_DIR)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture', type=Path)
    parser.add_argument('--prepared', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.capture, args.prepared), indent=2))
