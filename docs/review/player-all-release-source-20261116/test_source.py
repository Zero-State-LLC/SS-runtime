#!/usr/bin/env python3
"""Regression tests against actual editable inputs, with mutation-based failures.

Run: python test_source.py --source-root /path/to/outputs [--artifacts /path/to/artifacts]
No missing-input skips. Artifact checks are a separate explicit suite after build.
"""
import argparse
import copy
import json
import math
from pathlib import Path
import tempfile
import unittest
from fractions import Fraction

import numpy as np
from PIL import Image
import build_source as b

ROOT = None
ARTIFACTS = None


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        provenance=ROOT/"provenance.json"
        if provenance.exists():
            for relative,expected in json.loads(provenance.read_text())["files"].items():
                b.require(b.sha(ROOT/relative)==expected,f"Portable fixture hash changed: {relative}")
        cls.sources = json.loads((ROOT / b.NAMES[0] / "source/samples.json").read_text())
        cls.neutral = json.loads((ROOT / b.NAMES[1] / "source/samples.json").read_text())[0]

    def candidate(self, phase=1):
        return b.generate(self.sources[phase-1], self.neutral)

    def test_all_fourteen_geometry_and_contact_paths(self):
        for phase in range(1,17):
            if phase not in b.PRESERVED:
                with self.subTest(phase=phase):
                    result = b.validate(self.candidate(phase), self.sources[phase-1], self.neutral, phase)
                    self.assertEqual(len(result["measurements"]),34)
                    self.assertEqual(result["simultaneousHorizontalToeMoves"],[])

    def test_independent_segment_and_knee_measurements(self):
        for phase in range(1,17):
            for pose in self.candidate(phase):
                for q in pose["legs"]:
                    self.assertAlmostEqual(math.dist(q["hip"],q["knee"]),12.5,places=10)
                    self.assertAlmostEqual(math.dist(q["knee"],q["ankle"]),14.5,places=10)
                    self.assertLess(q["knee"][2],q["hip"][2])
                    self.assertGreaterEqual(min(q["toe"][2],q["heel"][2]),-1e-8)

    def test_export_timeline_exact_order_and_holds(self):
        from export_review import timeline
        sequence=timeline()
        self.assertEqual(len(sequence),147)
        settling=sequence[32:83]
        self.assertEqual(settling,[("settle",k) for k in range(17) for _ in range(3)])
        self.assertEqual(sequence[79],("settle",15))
        self.assertEqual(sequence[80],("settle",16))
        self.assertEqual(Fraction(80-32,128),Fraction(3,8))
        self.assertEqual(Fraction(80-32,32),Fraction(3,2))

    def test_source_output_overlap_rejected_before_write(self):
        with self.assertRaisesRegex(ValueError,"must not overlap"):
            b.build(ROOT,ROOT,1)

    def test_incomplete_checkpoint_never_reused(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertFalse(b.completed_work(ROOT,Path(directory),self.candidate()))

    def test_checkpoint_sample_change_rejected_before_reuse(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            b.save(root/"assembly-record.json",{"frames":[]})
            changed=self.candidate()
            changed[3]["legs"][0]["toe"][0] += 1
            b.save(root/"source/samples.json",changed)
            with self.assertRaisesRegex(ValueError,"Checkpoint source mismatch"):
                b.completed_work(ROOT,root,self.candidate())

    def test_actual_support_selection_not_half_cycle(self):
        expected = ["right"]*6 + ["left"]*8 + ["right"]*2
        self.assertEqual([b.support_side(p) for p in self.sources], expected)

    def test_planted_metadata_precedes_height_tie(self):
        source = copy.deepcopy(self.sources[0])
        b.legs(source)["left"]["toe"][2] = 0
        self.assertEqual(b.support_side(source),"right")

    def test_ambiguous_airborne_rejected(self):
        source = copy.deepcopy(self.sources[4])
        for q in source["legs"]:
            q["toe"][2] = 1
        with self.assertRaisesRegex(ValueError,"Equal airborne"):
            b.support_side(source)

    def test_side_identity_not_array_zip(self):
        neutral = copy.deepcopy(self.neutral)
        neutral["legs"].reverse()
        self.assertEqual(self.candidate(7), b.generate(self.sources[6], neutral))

    def test_generator_leaves_inputs_unchanged(self):
        before = copy.deepcopy((self.sources,self.neutral))
        for source in self.sources:
            b.generate(source,self.neutral)
        self.assertEqual((self.sources,self.neutral),before)

    def test_reach_boundaries_fail_closed(self):
        for distance in (0,2,27,28):
            with self.subTest(distance=distance), self.assertRaisesRegex(ValueError,"Unreachable"):
                b.solve(np.zeros(3),np.array([0.,0.,distance]))

    def test_bad_limb_rejected(self):
        poses = self.candidate()
        poses[3]["legs"][0]["knee"][0] += 0.1
        with self.assertRaisesRegex(ValueError,"segment lengths"):
            b.validate(poses,self.sources[0],self.neutral,1)

    def test_ground_penetration_rejected(self):
        poses = self.candidate()
        poses[3]["legs"][0]["heel"][2] = -0.01
        with self.assertRaisesRegex(ValueError,"ground clearance"):
            b.validate(poses,self.sources[0],self.neutral,1)

    def test_knee_above_hip_rejected_even_with_exact_lengths(self):
        poses = self.candidate()
        q = poses[3]["legs"][0]
        # Rigidly rotate a valid whole leg 180 degrees about horizontal x.
        # This preserves both lengths and keeps foot geometry above ground.
        for key in ("hip","knee","ankle","toe","heel"):
            q[key] = [q[key][0],-q[key][1],100-q[key][2]]
        with self.assertRaisesRegex(ValueError,"knee above hip"):
            b.validate(poses,self.sources[0],self.neutral,1)

    def test_nonfinite_geometry_rejected(self):
        poses = self.candidate()
        poses[3]["legs"][0]["knee"][0] = float("nan")
        with self.assertRaisesRegex(ValueError,"nonfinite"):
            b.validate(poses,self.sources[0],self.neutral,1)

    def test_contact_schedule_rejected(self):
        poses = self.candidate()
        poses[3]["legs"][0]["contact"] = False
        with self.assertRaisesRegex(ValueError,"contact schedule"):
            b.validate(poses,self.sources[0],self.neutral,1)

    def test_world_contact_drift_rejected(self):
        poses = self.candidate(2)
        b.legs(poses[4])["right"]["contactWorld"][1] += 0.1
        with self.assertRaisesRegex(ValueError,"world contact drift"):
            b.validate(poses,self.sources[1],self.neutral,2)

    def test_toe_contact_drift_rejected_with_lengths_preserved(self):
        poses = self.candidate()
        q = b.legs(poses[4])["right"]
        for key in ("hip","knee","ankle","toe","heel","contactWorld"):
            q[key][0] += 0.01
        with self.assertRaisesRegex(ValueError,"contact toe drift"):
            b.validate(poses,self.sources[0],self.neutral,1)

    def test_sample_order_rejected(self):
        poses = self.candidate()
        poses[3],poses[4] = poses[4],poses[3]
        with self.assertRaisesRegex(ValueError,"sample order"):
            b.validate(poses,self.sources[0],self.neutral,1)

    def test_entry_geometry_exact(self):
        for phase in range(1,17):
            self.assertEqual(self.candidate(phase)[0]["legs"], self.sources[phase-1]["legs"])

    def test_neutral_geometry_mutation_rejected(self):
        poses = self.candidate()
        q = poses[16]["legs"][0]
        for key in ("hip","knee","ankle","toe","heel","contactWorld"):
            q[key][0] += 0.01
        with self.assertRaisesRegex(ValueError,"neutral hip"):
            b.validate(poses,self.sources[0],self.neutral,1)

    def test_preserved_extremes_validate_without_rewriting(self):
        for phase in b.PRESERVED:
            path = ROOT / b.NAMES[2] / f"phase-{phase:02d}/source/samples.json"
            original = path.read_bytes()
            b.validate(json.loads(original),self.sources[phase-1],self.neutral,phase)
            self.assertEqual(path.read_bytes(),original)

    def test_exact_timing_neutral_boundary_not_total_duration(self):
        t = b.TIMING
        self.assertEqual(Fraction(sum(t["frameUnits"][:16]),t["unitsPerSecond"]),Fraction(3,8))
        self.assertEqual(Fraction(sum(t["frameUnits"]),t["unitsPerSecond"]),Fraction(51,128))
        for phase in (1,7,15):
            self.assertEqual([p["settleSeconds"] for p in self.candidate(phase)],[k*3/128 for k in range(17)])

    def test_assembly_recipe_drift_rejected(self):
        text = (ROOT / b.NAMES[0] / "assemble.py").read_text()
        self.assertIn("settle_weight",b.adapt_assembly(text))
        with self.assertRaisesRegex(ValueError,"Assembly recipe drift"):
            b.adapt_assembly(text.replace("swing=sign*math.cos(phase)","swing=0"))

    def test_endpoint_pixel_mutation_rejected(self):
        # Endpoint guard must compare pixels, not trust metadata/hashes alone.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            im = Image.new("RGBA",(384,416),(1,2,3,255))
            for name in ("00.png","16.png","source.png","neutral.png"):
                im.save(root/name)
            b.endpoint_checks(root,root/"source.png",root/"neutral.png",1)
            im.putpixel((100,100),(2,2,3,255));im.save(root/"16.png")
            with self.assertRaisesRegex(ValueError,"1 RGBA pixels differ"):
                b.endpoint_checks(root,root/"source.png",root/"neutral.png",1)


class ArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ARTIFACTS/"manifest.json").read_text())

    def test_status_is_proposed_except_preserved_extremes(self):
        self.assertEqual(self.manifest["preservedPhases"],[5,13])
        self.assertEqual(self.manifest["newPhases"],[p for p in range(1,17) if p not in (5,13)])
        for phase in self.manifest["phases"]:
            self.assertEqual(phase["status"],"PRESERVED" if phase["phase"] in (5,13) else "PROPOSED")

    def test_input_inventory_still_exact(self):
        self.assertEqual(b.inventory(ROOT),json.loads((ARTIFACTS/"input-inventory.json").read_text()))

    def test_complete_ordered_family_and_file_hashes(self):
        records = self.manifest["phases"]
        self.assertEqual([p["phase"] for p in records],list(range(1,17)))
        for p in records:
            self.assertEqual([f["pose"] for f in p["frames"]],list(range(17)))
            self.assertEqual(b.sha(ARTIFACTS/p["samplesPath"]),p["samplesSHA256"])
            for f in p["frames"]:
                self.assertEqual(b.sha(ARTIFACTS/f["path"]),f["fileSHA256"])

    def test_all_actual_rgba_endpoints(self):
        for phase in range(1,17):
            b.endpoint_checks(ARTIFACTS/f"phase-{phase:02d}/frames", ROOT/b.NAMES[0]/f"frames/{phase-1:02d}.png",ROOT/b.NAMES[1]/"frames/00.png",phase)

    def test_preserved_extreme_source_and_every_png_byte(self):
        for phase in b.PRESERVED:
            original = ROOT/b.NAMES[2]/f"phase-{phase:02d}"
            delivered = ARTIFACTS/f"phase-{phase:02d}"
            self.assertEqual((original/"source/samples.json").read_bytes(),(delivered/"samples.json").read_bytes())
            for k in range(17):
                name = f"frames/{k:02d}.png"
                self.assertEqual((original/name).read_bytes(),(delivered/name).read_bytes())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root",type=Path,required=True)
    parser.add_argument("--artifacts",type=Path)
    args = parser.parse_args()
    ROOT,ARTIFACTS = args.source_root,args.artifacts
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SourceTests)
    if ARTIFACTS is not None:
        suite.addTests(loader.loadTestsFromTestCase(ArtifactTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
