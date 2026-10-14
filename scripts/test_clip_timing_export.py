#!/usr/bin/env python3
"""BP-003 export regression checks. Pass --schema from the pinned specs."""
import argparse
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator
from convert_clip_timing import convert, read_json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Sources/SurveillanceCore/Resources/contracts/clip-metadata-001.json'


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.source = read_json(SOURCE)
        self.schema = read_json(SCHEMA)

    def test_complete_round_trip(self):
        original = deepcopy(self.source)
        result = convert(self.source, self.schema)
        self.assertEqual(self.source, original)
        Draft202012Validator(self.schema).validate(result)
        restored = deepcopy(result)
        restored['schemaVersion'] = 'clip-metadata-001'
        facings = 0
        for before, after, back in zip(original['clips'], result['clips'], restored['clips']):
            self.assertEqual(after['timing']['frameUnits'], [1] * len(before['frameIds']))
            back['framesPerSecond'] = back.pop('timing')['unitsPerSecond']
            for direction in before['directions'] or [None]:
                indices = [i for i, frame in enumerate(before['frameIds'])
                           if direction is None or f'_{direction}_' in frame]
                old = Fraction(len(indices), before['framesPerSecond'])
                new = Fraction(sum(after['timing']['frameUnits'][i] for i in indices),
                               after['timing']['unitsPerSecond'])
                self.assertEqual(old, new)
                self.assertEqual((old * 60).__ceil__(), (new * 60).__ceil__())
                facings += 1
        self.assertEqual(restored, original)
        print(f'Parity: {len(original["clips"])} clips; {facings} facing selections')

    def test_cli_repeatable_and_fail_closed(self):
        command = [sys.executable, str(ROOT / 'scripts/convert_clip_timing.py')]
        args = ['--schema', str(SCHEMA)]
        first = subprocess.run(command + [str(SOURCE)] + args, capture_output=True, check=True)
        second = subprocess.run(command + [str(SOURCE)] + args, capture_output=True, check=True)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout), convert(self.source, self.schema))
        bad_documents = []
        for fps in [None, True, False, 1.5, 0, -1, 2**63, '12']:
            bad = deepcopy(self.source)
            bad['clips'][0]['framesPerSecond'] = fps
            bad_documents.append(json.dumps(bad))
        for key, value in [('timing', {}), ('frameIds', []), ('directions', ['invalid']),
                           ('unknown', 1), ('directions', ['n', 'n'])]:
            bad = deepcopy(self.source)
            bad['clips'][0][key] = value
            bad_documents.append(json.dumps(bad))
        bad = deepcopy(self.source)
        bad['clips'][0]['directions'] = ['n']
        bad['clips'][0]['frameIds'] = ['only_s_01']
        bad_documents.append(json.dumps(bad))
        bad_documents += ['{"schemaVersion":"clip-metadata-001","schemaVersion":"clip-metadata-002"}',
                          json.dumps(convert(self.source, self.schema)), '{', 'null']
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'invalid.json'
            for payload in bad_documents:
                with self.subTest(payload=payload[:80]):
                    path.write_text(payload)
                    rejected = subprocess.run(command + [str(path)] + args, capture_output=True)
                    self.assertNotEqual(rejected.returncode, 0)
                    self.assertEqual(rejected.stdout, b'')
        print(f'CLI: deterministic bytes; {len(bad_documents)} rejected inputs emit no candidate')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--schema', required=True, type=Path)
    SCHEMA = parser.parse_args().schema.resolve()
    unittest.main(argv=[sys.argv[0]])
