import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import import_allrelease_native as capture


class NativeImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.rows = []
        self.items = []
        for phase, pose in sorted(capture.EXPECTED):
            self.items.append({"suggestedHumanReadableName": f"allrelease-native-{phase:02d}-pose-{pose:02d}_0.png",
                               "exportedFileName": f"{phase}-{pose}.png"})
            self.rows.append({"phase": phase, "pose": pose,
                              "tickOffset": (pose * 180 + 127) // 128,
                              "source": f"player-source-s-{phase-1:02d}" if pose == 0 else
                              "player-source-s-neutral" if pose == 16 else f"player-allrelease-{phase:02d}-{pose:02d}"})
        self.items.append({"suggestedHumanReadableName": "allrelease-native-pose-records_0.json",
                           "exportedFileName": "records.json"})
        self.save()

    def save(self):
        (self.root / "manifest.json").write_text(json.dumps([{"attachments": self.items}]))
        (self.root / "records.json").write_text(json.dumps(self.rows))

    def test_png_preservation_is_scoped_to_test_target(self):
        before, tests = (capture.ROOT / "project.yml").read_text().split("  SSRuntimeTests:\n", 1)
        for setting in ("COMPRESS_PNG_FILES", "STRIP_PNG_TEXT"):
            self.assertNotIn(setting, before)
            self.assertIn(f"        {setting}: NO", tests)

    def test_complete_census_and_exact_tick_samples(self):
        images, _, rows = capture.attachments(self.root)
        self.assertEqual(set(images), capture.EXPECTED)
        self.assertEqual(len(rows), 238)

    def test_missing_image_rejected(self):
        self.items.pop(0)
        self.save()
        with self.assertRaisesRegex(ValueError, "exactly238"):
            capture.attachments(self.root)

    def test_duplicate_image_rejected(self):
        self.items.append(copy.deepcopy(self.items[0]))
        self.save()
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            capture.attachments(self.root)

    def test_missing_record_rejected(self):
        self.rows.pop()
        self.save()
        with self.assertRaisesRegex(ValueError, "record census"):
            capture.attachments(self.root)

    def test_changed_tick_rejected(self):
        self.rows[16]["tickOffset"] = 24
        self.save()
        with self.assertRaisesRegex(ValueError, "tick sampling"):
            capture.attachments(self.root)

    def test_wrong_source_rejected(self):
        self.rows[1]["source"] = "player-source-s-neutral"
        self.save()
        with self.assertRaisesRegex(ValueError, "wrong source"):
            capture.attachments(self.root)

    def published_fixture(self):
        rows = copy.deepcopy(self.rows)
        for row in rows:
            row["sourceSHA256"] = "hash"
        (self.root / "pose-records.json").write_text(json.dumps(rows))
        report = {"status": "STATIC_NATIVE_SOURCE_CHECK_NOT_ADMISSION", "poses": 238,
                  "phases": capture.PHASES,
                  "summary": {"passedTests": 2, "failedTests": 0, "skippedTests": 0},
                  "attachmentHashes": {f"phase-{p:02d}-pose-{k:02d}.png": "hash" for p, k in capture.EXPECTED},
                  "sourceHashes": {f"AppTests/BenchmarkAssets/{r['source']}.png": "hash" for r in rows}}
        report["attachmentHashes"]["pose-records.json"] = "hash"
        report["sourceHashes"]["AppTests/AllReleaseSourceTests.swift"] = "hash"
        report["sourceHashes"]["project.yml"] = "hash"
        (self.root / "verification.json").write_text(json.dumps(report))
        return report

    def test_published_manifest_complete_and_hashes_checked(self):
        self.published_fixture()
        with patch.object(capture, "sha", return_value="hash") as digest:
            capture.verify_capture(self.root)
            self.assertEqual(digest.call_count, 239 + 227)
        with patch.object(capture, "sha", return_value="drift"):
            with self.assertRaisesRegex(ValueError, "evidence drift"):
                capture.verify_capture(self.root)

    def test_incomplete_published_manifest_rejected(self):
        report = self.published_fixture()
        report["attachmentHashes"].pop("phase-01-pose-00.png")
        (self.root / "verification.json").write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, "attachmentHashes census"):
            capture.verify_capture(self.root)

    def test_changed_native_source_bytes_rejected_before_publication(self):
        summary = {"passedTests": 2, "failedTests": 0, "skippedTests": 0}
        for row in self.rows:
            row["sourceSHA256"] = "captured-resource-hash"
        self.save()
        with patch("subprocess.check_output", return_value=json.dumps(summary)), \
                patch.object(capture, "sha", return_value="different-current-resource-hash"):
            with self.assertRaisesRegex(ValueError, "native source bytes differ"):
                capture.import_capture(self.root, self.root / "result", self.root / "new")
            self.assertFalse((self.root / "new").exists())

    def test_failed_or_skipped_native_run_rejected(self):
        for summary in [{"passedTests": 1, "failedTests": 1, "skippedTests": 0},
                        {"passedTests": 2, "failedTests": 0, "skippedTests": 1},
                        {"passedTests": 0, "failedTests": 0, "skippedTests": 0}]:
            with self.subTest(summary=summary), patch("subprocess.check_output", return_value=json.dumps(summary)):
                with self.assertRaisesRegex(ValueError, "successful two-test"):
                    capture.import_capture(self.root, self.root / "result", self.root / "new")
                self.assertFalse((self.root / "new").exists())


if __name__ == "__main__":
    unittest.main()
