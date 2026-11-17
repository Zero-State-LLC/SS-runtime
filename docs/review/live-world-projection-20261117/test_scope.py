import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from verify_scope import verify


class ScopeGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get("JCODE_SCRATCH_DIR"))
        self.root = Path(self.temp.name).resolve()
        self.git("init", "-q")
        self.git("config", "user.name", "Scope guard fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        for name in ["Sources/frozen.swift", "AppTests/existing.swift", "RuntimeAssets/existing.png"]:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"frozen bytes\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture base")
        self.base = self.git("rev-parse", "HEAD").decode().strip()

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args])

    def test_unchanged_and_new_test_pass(self):
        self.assertEqual(verify(self.root, self.base)["trackedProtectedFiles"], 3)
        (self.root / "AppTests/new.swift").write_text("new regression\n")
        self.git("add", "AppTests/new.swift")
        verify(self.root, self.base)

    def test_modified_existing_test_rejected_before_and_after_staging(self):
        (self.root / "AppTests/existing.swift").write_text("weakened\n")
        with self.assertRaisesRegex(ValueError, "existing.swift"):
            verify(self.root, self.base)
        self.git("add", "AppTests/existing.swift")
        with self.assertRaisesRegex(ValueError, "existing.swift"):
            verify(self.root, self.base)

    def test_removed_asset_rejected(self):
        (self.root / "RuntimeAssets/existing.png").unlink()
        with self.assertRaisesRegex(ValueError, "existing.png"):
            verify(self.root, self.base)

    def test_new_authority_file_rejected(self):
        (self.root / "Sources/new.swift").write_text("new authority\n")
        self.git("add", "Sources/new.swift")
        with self.assertRaisesRegex(ValueError, "new.swift"):
            verify(self.root, self.base)

    def test_mode_change_rejected(self):
        path = self.root / "Sources/frozen.swift"
        path.chmod(0o755)
        self.git("update-index", "--chmod=+x", "Sources/frozen.swift")
        with self.assertRaisesRegex(ValueError, "frozen.swift"):
            verify(self.root, self.base)


if __name__ == "__main__":
    unittest.main(verbosity=2)
