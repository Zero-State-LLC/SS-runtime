"""Regression for #256: aliases must not mask missing-input assertions."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'scripts/run_review_tests.py'
SCENE = ROOT / 'docs/review/blocked-base-curb-relief-20261116/scene'


class CanonicalReviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR'))
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.real = self.root / 'real'
        self.real.mkdir()
        self.alias = self.root / 'alias'
        self.alias.symlink_to(self.real, target_is_directory=True)
        self.env = dict(os.environ, JCODE_SCRATCH_DIR=str(self.alias))

    def invoke(self, args, wrapped=True):
        command = [sys.executable] + ([str(RUNNER)] if wrapped else []) + args
        return subprocess.run(command, env=self.env, cwd=ROOT, capture_output=True, text=True)

    def test_real_missing_input_assertion_fails_under_alias_then_passes(self):
        args = ['-B', '-m', 'unittest', 'discover', '-s', str(SCENE),
                '-p', 'test_native.py', '-k', 'test_pending_no_outputs']
        red = self.invoke(args, wrapped=False)
        self.assertNotEqual(red.returncode, 0)
        self.assertIn('Symlinked assembly path forbidden', red.stderr)
        green = self.invoke(args)
        self.assertEqual(green.returncode, 0, green.stderr)
        self.assertIn('Ran 1 test', green.stderr)
        self.assertEqual(list(self.real.iterdir()), [])

    def test_actual_assembly_symlink_remains_forbidden(self):
        script = '''
import sys, os
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import native
root = Path(os.environ['JCODE_SCRATCH_DIR'])
target = root / 'manifest.json'
target.write_text('{}')
alias = root / 'alias.json'
alias.symlink_to(target)
try:
    native.expected_input(manifest=alias)
except ValueError as error:
    assert 'Symlinked assembly path forbidden' in str(error)
else:
    raise AssertionError('Assembly symlink accepted')
'''
        result = self.invoke(['-B', '-c', script, str(SCENE)])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_child_failure_status_is_preserved(self):
        result = self.invoke(['-c', 'raise SystemExit(7)'])
        self.assertEqual(result.returncode, 7)
        self.assertEqual(list(self.real.iterdir()), [])

    def test_all_temp_variables_are_canonical_and_isolated(self):
        script = '''
import os, tempfile
from pathlib import Path
root = Path(os.environ['JCODE_SCRATCH_DIR'])
assert root == root.resolve()
assert root.parent == Path(__import__('sys').argv[1])
assert all(os.environ[key] == str(root) for key in ('TMPDIR', 'TMP', 'TEMP'))
assert Path(tempfile.gettempdir()) == root
'''
        result = self.invoke(['-c', script, str(self.real)])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_ci_uses_runner_without_ignoring_status(self):
        workflow = (ROOT / '.github/workflows/ci.yml').read_text()
        line = next(line for line in workflow.splitlines()
                    if 'unittest discover -s docs/review/blocked-base-curb-relief-20261116/scene' in line)
        self.assertIn('scripts/run_review_tests.py -B', line)
        self.assertNotIn('||', line)
        self.assertIn('python3 -B scripts/test_review_test_runner.py', workflow)


if __name__ == '__main__':
    unittest.main(verbosity=2)
