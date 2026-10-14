#!/usr/bin/env python3
"""BP-003: export a mechanical v1→v2 candidate to stdout; never admit art.

Requires jsonschema and the target schema from the pinned SS-specs checkout.
Usage: python3 scripts/convert_clip_timing.py INPUT --schema SCHEMA > CANDIDATE
Runtime semantic validation and coordinated admission remain mandatory.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, ValidationError

MAX_INT = (1 << 63) - 1


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_object)


def convert(document, schema):
    if not isinstance(document, dict) or document.get('schemaVersion') != 'clip-metadata-001':
        raise ValueError('expected clip-metadata-001 source')
    if not isinstance(document.get('clips'), list) or not document['clips']:
        raise ValueError('expected nonempty clips array')
    result = deepcopy(document)
    result['schemaVersion'] = 'clip-metadata-002'
    for clip in result['clips']:
        if not isinstance(clip, dict) or 'timing' in clip:
            raise ValueError('expected v1 clip without timing')
        fps = clip.pop('framesPerSecond', None)
        if type(fps) is not int or not 1 <= fps <= MAX_INT:
            raise ValueError('framesPerSecond must be a positive signed-64-bit integer')
        frames = clip.get('frameIds')
        if not isinstance(frames, list) or not frames:
            raise ValueError('expected nonempty frameIds array')
        clip['timing'] = {'unitsPerSecond': fps, 'frameUnits': [1] * len(frames)}
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(result)
    for clip in result['clips']:
        for direction in clip['directions'] or [None]:
            count = sum(direction is None or f'_{direction}_' in frame
                        for frame in clip['frameIds'])
            if not count or count * 60 > MAX_INT:
                raise ValueError('empty facing or tick numerator overflow')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--schema', required=True, type=Path)
    args = parser.parse_args()
    try:
        result = convert(read_json(args.input), read_json(args.schema))
    except (OSError, ValueError, ValidationError) as error:
        parser.exit(1, f'conversion rejected: {error}\n')
    sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
