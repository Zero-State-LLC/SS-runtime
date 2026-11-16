"""Independent geometry checks against the compiled Swift review helper, no simulator.

Requires Python 3 and swiftc. Build artifacts go to JCODE_SCRATCH_DIR when set.
The point/box oracle uses ray/box interval intersection, not the helper's axis rules.
"""
import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
HELPER = ROOT / "AppTests/SceneQAReviewDepth.swift"
XCTEST = ROOT / "AppTests/SceneQAReviewDepthTests.swift"


def point(name, x, y, priority=None):
    result = {"name": name, "root": [x, y]}
    if priority is not None:
        result["priority"] = priority
    return result


def kiosk():
    return {"name": "kiosk", "root": [512, 640], "bounds": [512, 640, 640, 768]}


def pairs(result):
    return [(edge["back"], edge["front"]) for edge in result["edges"]]


class DepthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        compiler = shutil.which("swiftc")
        if compiler is None:
            raise RuntimeError("swiftc required: never silently skip the implementation checks")
        cls.work = tempfile.TemporaryDirectory(prefix="scene-depth-", dir=os.environ.get("JCODE_SCRATCH_DIR"))
        cls.addClassCleanup(cls.work.cleanup)
        cls.executable = str(Path(cls.work.name) / "depth-probe")
        subprocess.run([compiler, "-D", "DEBUG", "-D", "SS_SOURCE_SCENE_REVIEW",
                        str(HELPER), str(HERE / "DepthProbe.swift"), "-o", cls.executable], check=True, timeout=60)
        cls.compiler = compiler
        cls.xctest_flags = []
        if sys.platform == "darwin":
            platform = subprocess.check_output(
                ["xcrun", "--sdk", "macosx", "--show-sdk-platform-path"], text=True, timeout=10).strip()
            cls.xctest_flags = ["-F", str(Path(platform) / "Developer/Library/Frameworks"),
                                "-I", str(Path(platform) / "Developer/usr/lib")]

    def probe(self, requests):
        run = subprocess.run([self.executable], input=json.dumps(requests), text=True,
                             capture_output=True, check=True, timeout=20)
        return json.loads(run.stdout)

    def order(self, items):
        return self.probe([{"items": items}])[0]

    def test_old_root_regression_and_plane_explanation(self):
        items = [kiosk(), point("camera3", 496, 672)]
        old = sorted(items, key=lambda item: -sum(item["root"]))
        self.assertEqual([item["name"] for item in old], ["camera3", "kiosk"])
        result = self.order(items)
        self.assertEqual(result["names"], ["kiosk", "camera3"])
        self.assertEqual(result["edges"], [{"back": "kiosk", "front": "camera3", "separations": [
            {"axis": "x", "backMinimum": 512, "frontMaximum": 496}]}])

    def test_near_far_mixed_quadrants(self):
        cases = [(496, 672, [("kiosk", "p")]), (560, 624, [("kiosk", "p")]),
                 (656, 700, [("p", "kiosk")]), (560, 784, [("p", "kiosk")]),
                 (496, 624, [("kiosk", "p")]), (656, 784, [("p", "kiosk")]),
                 (496, 784, []), (656, 624, [])]
        results = self.probe([{"items": [kiosk(), point("p", x, y)]} for x, y, _ in cases])
        for (x, y, expected), result in zip(cases, results):
            with self.subTest(x=x, y=y):
                self.assertEqual(pairs(result), expected)

    def test_ray_box_oracle_1089_positions(self):
        positions = list(itertools.product(range(448, 705, 8), range(576, 833, 8)))
        results = self.probe([{"items": [kiosk(), point("p", x, y)]} for x, y in positions])
        self.assertEqual(len(results), 1089)
        for (x, y), result in zip(positions, results):
            # View ray p + t*(1,1). Positive t is farther from the viewer.
            enter = max(512 - x, 640 - y)
            leave = min(640 - x, 768 - y)
            expected = []
            if enter <= leave:
                if enter > 0:
                    expected = [("kiosk", "p")]
                elif leave < 0:
                    expected = [("p", "kiosk")]
            with self.subTest(point=(x, y)):
                self.assertEqual(pairs(result), expected)
                if expected:
                    self.assertLess(result["names"].index(expected[0][0]),
                                    result["names"].index(expected[0][1]))

    def test_equal_intersecting_and_contact(self):
        cases = [point("p", 512, 640), point("p", 576, 704), point("p", 640, 768),
                 {"name": "same", "root": [512, 640], "bounds": [512, 640, 640, 768]},
                 {"name": "overlap", "root": [600, 700], "bounds": [600, 700, 700, 800]},
                 {"name": "touch", "root": [480, 650], "bounds": [480, 650, 512, 700]}]
        for result in self.probe([{"items": [kiosk(), item]} for item in cases]):
            self.assertEqual(result["edges"], [])

    def test_solid_solid_and_disjoint_projected_spans(self):
        near = {"name": "near", "root": [480, 660], "bounds": [480, 660, 500, 700]}
        self.assertEqual(pairs(self.order([kiosk(), near])), [("kiosk", "near")])
        far = {"name": "far", "root": [656, 680], "bounds": [656, 680, 700, 750]}
        self.assertEqual(pairs(self.order([kiosk(), far])), [("far", "kiosk")])
        mixed = {"name": "mixed", "root": [480, 784], "bounds": [480, 784, 500, 800]}
        self.assertEqual(pairs(self.order([kiosk(), mixed])), [])

    def test_ready_node_priority_not_global_resort(self):
        near = {"name": "near", "root": [480, 660], "bounds": [480, 660, 500, 700], "priority": 9999}
        free = point("free", -1000, 1000, priority=2000)
        self.assertEqual(self.order([near, kiosk(), free])["names"], ["free", "kiosk", "near"])

    def test_stable_all_permutations(self):
        items = [kiosk(), point("camera3", 496, 672), point("a", 1, 9), point("z", 9, 1)]
        results = self.probe([{"items": list(order)} for order in itertools.permutations(items)])
        self.assertTrue(all(result == results[0] for result in results))
        self.assertEqual(self.order([point("z", 9, 1), point("a", 1, 9)])["names"], ["a", "z"])

    def test_same_projected_column_points_have_depth_edge(self):
        result = self.order([point("front", 1, 2), point("back", 3, 4)])
        self.assertEqual(result["names"], ["back", "front"])
        self.assertEqual(pairs(result), [("back", "front")])
        self.assertEqual(len(result["edges"][0]["separations"]), 2)

    def test_translation_and_positive_scale_preserve_relations(self):
        results = []
        for scale, dx, dy in [(1, 0, 0), (0.25, -100, 10), (3, 5000, -8000)]:
            b = {"name": "kiosk", "root": [512 * scale + dx, 640 * scale + dy],
                 "bounds": [512 * scale + dx, 640 * scale + dy, 640 * scale + dx, 768 * scale + dy]}
            results.append(self.order([b, point("camera3", 496 * scale + dx, 672 * scale + dy)]))
        for result in results:
            self.assertEqual(result["names"], ["kiosk", "camera3"])
            self.assertEqual(pairs(result), [("kiosk", "camera3")])

    def test_empty_single_and_invalid(self):
        self.assertEqual(self.order([]), {"names": [], "edges": []})
        self.assertEqual(self.order([point("one", 0, 0)])["names"], ["one"])
        self.assertEqual(self.order([point("a", 0, 0), point("a", 1, 1)])["error"], "duplicateName")
        self.assertEqual(self.order([point("", 0, 0)])["error"], "invalidItem")
        invalid = {"name": "bad", "root": [0, 0], "bounds": [1, 0, 0, 1]}
        self.assertEqual(self.order([invalid])["error"], "invalidItem")
        overflow = {"name": "overflow", "root": [0, 0], "bounds": [-1e308, -1e308, 1e308, 1e308]}
        self.assertEqual(self.order([overflow])["error"], "invalidItem")

    def test_explicit_synthetic_cycle_failure(self):
        request = {"items": [point(name, 0, 0) for name in "abc"], "syntheticCycle": True}
        result = self.probe([request])[0]
        self.assertEqual(result["error"], "cyclic")
        self.assertEqual(result["blockedNames"], ["a", "b", "c"])
        self.assertNotIn("names", result)
        self.assertEqual(pairs(result), [("a", "b"), ("b", "a"), ("b", "c")])

    def test_swift_xctest_typechecks(self):
        subprocess.run([self.compiler, "-typecheck", *self.xctest_flags,
                        "-D", "DEBUG", "-D", "SS_SOURCE_SCENE_REVIEW",
                        str(HELPER), str(XCTEST)], check=True, timeout=60)

    def test_review_gates_exclude_both_files(self):
        for flags in [[], ["-D", "DEBUG"], ["-D", "SS_SOURCE_SCENE_REVIEW"]]:
            subprocess.run([self.compiler, "-typecheck", *flags, str(HELPER), str(XCTEST)], check=True, timeout=60)
        for path in [HELPER, XCTEST]:
            self.assertTrue(path.read_text().startswith("#if DEBUG && SS_SOURCE_SCENE_REVIEW\n"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
