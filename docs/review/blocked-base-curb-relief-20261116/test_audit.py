import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
import audit


class PreservationTests(unittest.TestCase):
    def test_actual_protected_bytes(self):
        self.assertEqual(audit.verify()['files'], 1766)

    def test_receipt_forgery_rejected(self):
        receipt = json.loads(audit.RECEIPT.read_text())
        for operation in ('delete', 'digest', 'reference', 'scope'):
            with self.subTest(operation=operation):
                r = copy.deepcopy(receipt)
                name = next(iter(r['files']))
                if operation == 'delete':
                    del r['files'][name]
                elif operation == 'digest':
                    r['files'][name] = '0' * 64
                elif operation == 'reference':
                    r['referenceCommit'] = '0' * 40
                else:
                    r['protectedPrefixes'] = []
                with self.assertRaisesRegex(ValueError, 'receipt changed'):
                    audit.verify(r)

    def test_explicit_empty_receipt_fails(self):
        with self.assertRaises(ValueError):
            audit.verify({})

    def test_changed_file_digest_fails(self):
        with patch.object(audit, 'digest', return_value='0' * 64):
            with self.assertRaisesRegex(ValueError, 'Protected bytes changed'):
                audit.verify()

    def test_snapshot_cannot_replace_receipt(self):
        with self.assertRaisesRegex(ValueError, 'Refuse to replace'):
            audit.snapshot()

    def test_unsafe_and_alias_paths_fail(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as d:
            root = Path(d).resolve()
            (root / 'actual').mkdir()
            (root / 'actual/file').write_text('fixture')
            (root / 'alias').symlink_to(root / 'actual', target_is_directory=True)
            (root / 'link').symlink_to(root / 'actual/file')
            self.assertEqual(audit.safe_file(root, 'actual/file'), root / 'actual/file')
            for name in ('../escape', '/absolute', 'missing', 'alias/file', 'link'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    audit.safe_file(root, name)

    def test_full_rgba_not_just_landmarks(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as d:
            old, new = Path(d) / 'old', Path(d) / 'new'
            old.mkdir()
            new.mkdir()
            for z in (100, 125, 140):
                for suffix in ('native', 'half', 'grayscale'):
                    image = Image.new('RGBA', (8, 8), (7, 8, 9, 255))
                    image.save(old / f'source-scene-candidate-ordinary-z{z}-{suffix}.png')
                    image.save(new / f'source-scene-control-ordinary-z{z}-{suffix}.png')
            self.assertEqual(len(audit.baseline_pixels(old, new)), 9)
            altered = new / 'source-scene-control-ordinary-z140-grayscale.png'
            with Image.open(altered) as source:
                image = source.convert('RGBA')
            image.putpixel((7, 7), (7, 8, 9, 254))
            image.save(altered)
            with self.assertRaisesRegex(ValueError, 'Baseline pixels differ'):
                audit.baseline_pixels(old, new)


if __name__ == '__main__':
    unittest.main()
