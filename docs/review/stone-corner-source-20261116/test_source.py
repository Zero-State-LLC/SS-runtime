#!/usr/bin/env python3
"""Portable source/provenance guards. These do not establish visual fidelity."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from PIL import Image

HERE = Path(__file__).resolve().parent
SOURCE_SHA = '1226f74865aceafc0835501465e0be6aa94c8bbdad7f3b3e61af00a4af2ee475'
REFERENCE_SHA = '49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb'
UNKNOWN = ('observedWallContactLandmarks', 'hiddenWallContactLandmarks',
           'stairsAndApronLandmarks', 'groundContactAnchor',
           'worldFootprintCorrespondence', 'uniformDrawScale', 'registrationResiduals')


def validate(record):
    if record['status'] != 'PROPOSED_SOURCE_UNREGISTERED':
        raise ValueError('Historical first sample remains unregistered')
    if any(record[key] is not False for key in ('readyForNative', 'ownerAccepted', 'productionAdmitted')):
        raise ValueError('This source has no native readiness or acceptance')
    if any(record[key] is not None for key in UNKNOWN):
        raise ValueError('Do not silently replace unknown geometry in this retained first sample')
    if record['sourceSHA256'] != SOURCE_SHA or record['benchmarkSHA256'] != REFERENCE_SHA:
        raise ValueError('Fixed source/reference identity differs')
    if record['actualCanvas'] != [1254, 1254] or record['requestedCanvas'] != [1024, 1024]:
        raise ValueError('Actual source dimensions are not prompt dimensions')


class SourceGuards(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((HERE / 'registration.json').read_text())

    def test_manifest_preserves_unknown_geometry(self):
        validate(self.record)

    def test_source_bytes_and_actual_dimensions(self):
        path = HERE / self.record['source']
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), SOURCE_SHA)
        with Image.open(path) as im:
            self.assertEqual(im.size, (1254, 1254))
            self.assertEqual(im.mode, 'RGBA')
            self.assertEqual(im.getchannel('A').getextrema(), (0, 255))

    def test_generation_provenance(self):
        record = json.loads((HERE / self.record['provenance']).read_text())
        self.assertEqual(record['native_tool'], 'image_generation')
        self.assertEqual(record['response_item']['size'], '1254x1254')
        self.assertEqual(record['byte_count'], (HERE / self.record['source']).stat().st_size)
        self.assertIn('1024x1024', record['revised_prompt'])

    def test_rejects_unearned_admission(self):
        for key in ('readyForNative', 'ownerAccepted', 'productionAdmitted'):
            record = copy.deepcopy(self.record)
            record[key] = True
            with self.assertRaises(ValueError):
                validate(record)

    def test_rejects_prompt_coordinates_as_measured_landmarks(self):
        for key in UNKNOWN:
            record = copy.deepcopy(self.record)
            record[key] = record['requestedOnlyFootprint']
            with self.assertRaises(ValueError):
                validate(record)

    def test_rejects_dimension_and_identity_substitution(self):
        for key, value in [('actualCanvas', [1024, 1024]), ('sourceSHA256', '0' * 64),
                           ('benchmarkSHA256', '0' * 64)]:
            record = copy.deepcopy(self.record)
            record[key] = value
            with self.assertRaises(ValueError):
                validate(record)


if __name__ == '__main__':
    unittest.main(verbosity=2)
