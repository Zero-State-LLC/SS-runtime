import contextlib
import io
from pathlib import Path
import tempfile
import unittest
import audit


class PreservationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        (self.root / 'prior.txt').write_text('immutable')
        self.record = {'schema': 'architectural-protection-001',
                       'files': {'prior.txt': audit.digest(self.root / 'prior.txt')}}

    def test_valid_bytes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            audit.check(self.root, self.record)

    def test_changed_bytes_rejected(self):
        (self.root / 'prior.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'byte drift'):
            audit.check(self.root, self.record)

    def test_missing_bytes_rejected(self):
        (self.root / 'prior.txt').unlink()
        with self.assertRaisesRegex(ValueError, 'byte drift'):
            audit.check(self.root, self.record)

    def test_empty_census_rejected(self):
        with self.assertRaisesRegex(ValueError, 'census'):
            audit.check(self.root, {'schema': 'architectural-protection-001', 'files': {}})

    def test_wrong_schema_rejected(self):
        self.record['schema'] = 'other'
        with self.assertRaisesRegex(ValueError, 'census'):
            audit.check(self.root, self.record)

    def test_traversal_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Outward'):
            audit.resolve(self.root, '../outside')

    def test_outward_symlink_rejected(self):
        (self.root / 'escape').symlink_to(self.root.parent)
        with self.assertRaisesRegex(ValueError, 'Outward'):
            audit.resolve(self.root, 'escape/anything')

    def test_inward_root_alias_accepted(self):
        (self.root / 'alias').symlink_to(self.root, target_is_directory=True)
        self.assertEqual(audit.resolve(self.root / 'alias', 'prior.txt'), self.root / 'prior.txt')


if __name__ == '__main__':
    unittest.main(verbosity=2)
