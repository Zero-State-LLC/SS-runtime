#!/usr/bin/env python3
"""Portable verifier regressions using copies of the real delivered source frames."""
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

from PIL import Image, PngImagePlugin
import verify_artifacts as v

ROOT=Path(__file__).resolve().parent


class ArtifactVerifierTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="release-check-",dir=os.environ.get("JCODE_SCRATCH_DIR",str(ROOT)))
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.artifacts=self.base/"artifacts";self.artifacts.mkdir()
        self.fixtures=self.base/"fixtures"
        shutil.copytree(ROOT/"fixtures",self.fixtures)
        for name in ("manifest.json","input-inventory.json"):
            shutil.copy2(ROOT/"artifacts"/name,self.artifacts/name)
        for phase in v.PHASES:
            target=self.artifacts/f"phase-{phase:02d}"
            target.mkdir()
            shutil.copy2(ROOT/"artifacts"/target.name/"samples.json",target/"samples.json")
            shutil.copytree(ROOT/"artifacts"/target.name/"frames",target/"frames")

    def change(self,name,mutate):
        path=self.artifacts/name
        data=v.read_json(path);mutate(data)
        path.write_text(json.dumps(data))

    def verify(self,native=None):
        return v.verify(self.artifacts,self.fixtures,native)

    def native(self):
        root=self.base/"native";root.mkdir()
        for phase in v.NEW:
            for pose in range(1,16):
                shutil.copy2(self.artifacts/f"phase-{phase:02d}/frames/{pose:02d}.png",root/f"player-allrelease-{phase:02d}-{pose:02d}.png")
            shutil.copy2(self.artifacts/f"phase-{phase:02d}/frames/00.png",root/f"player-source-s-{phase-1:02d}.png")
        shutil.copy2(self.artifacts/"phase-01/frames/16.png",root/"player-source-s-neutral.png")
        return root

    def test_complete_portable_artifacts(self):
        result=self.verify()
        self.assertEqual(result["orderedFrames"],272)
        self.assertEqual(result["endpointProvenanceChecks"],32)
        self.assertFalse(result["originalMastersReopened"])
        self.assertIsNone(result["nativeAssets"])

    def test_missing_frame_rejected(self):
        (self.artifacts/"phase-01/frames/04.png").unlink()
        with self.assertRaisesRegex(ValueError,"exactly272"):
            self.verify()

    def test_extra_frame_rejected(self):
        shutil.copy2(self.artifacts/"phase-01/frames/04.png",self.artifacts/"phase-01/frames/17.png")
        with self.assertRaisesRegex(ValueError,"exactly272"):
            self.verify()

    def test_phase_reorder_rejected(self):
        self.change("manifest.json",lambda m:m["phases"].reverse())
        with self.assertRaisesRegex(ValueError,"Phase order"):
            self.verify()

    def test_frame_reorder_rejected(self):
        self.change("manifest.json",lambda m:m["phases"][0]["frames"].reverse())
        with self.assertRaisesRegex(ValueError,"Frame order"):
            self.verify()

    def test_timing_mutation_rejected(self):
        self.change("manifest.json",lambda m:m["timing"]["frameUnits"].__setitem__(3,4))
        with self.assertRaisesRegex(ValueError,"Exact timing"):
            self.verify()

    def test_noncanonical_frame_path_rejected(self):
        self.change("manifest.json",lambda m:m["phases"][0]["frames"][0].__setitem__("path","../outside.png"))
        with self.assertRaisesRegex(ValueError,"Noncanonical frame"):
            self.verify()

    def test_file_hash_mutation_rejected(self):
        path=self.artifacts/"phase-01/frames/01.png";path.write_bytes(path.read_bytes()+b"changed")
        with self.assertRaisesRegex(ValueError,"Frame byte hash"):
            self.verify()

    def test_rgba_mutation_even_with_updated_file_hash_rejected(self):
        path=self.artifacts/"phase-01/frames/01.png"
        with Image.open(path) as im:
            im=im.convert("RGBA");im.putpixel((0,0),(255,0,0,255));im.save(path)
        self.change("manifest.json",lambda m:m["phases"][0]["frames"][1].__setitem__("fileSHA256",v.sha(path)))
        with self.assertRaisesRegex(ValueError,"RGBA hash"):
            self.verify()

    def test_fixture_hash_mutation_rejected(self):
        path=self.fixtures/"SS-player-bounded-proportions/source/samples.json"
        path.write_text(path.read_text()+" ")
        with self.assertRaisesRegex(ValueError,"Fixture/input provenance"):
            self.verify()

    def test_preserved_frame_provenance_rejected(self):
        self.change("input-inventory.json",lambda m:m.__setitem__("SS-player-settle-prototype/phase-05/frames/02.png","0"*64))
        with self.assertRaisesRegex(ValueError,"Preserved frame provenance"):
            self.verify()

    def test_original_endpoint_provenance_rejected(self):
        self.change("input-inventory.json",lambda m:m.__setitem__("SS-player-bounded-proportions/frames/00.png","0"*64))
        with self.assertRaisesRegex(ValueError,"Endpoint original-file provenance"):
            self.verify()

    def test_acceptance_lift_rejected(self):
        self.change("manifest.json",lambda m:m["phases"][0].__setitem__("status","ACCEPTED"))
        with self.assertRaisesRegex(ValueError,"acceptance status"):
            self.verify()

    def test_native_complete_exact(self):
        result=self.verify(self.native())["nativeAssets"]
        self.assertEqual(result["exactIntermediateFiles"],210)
        self.assertEqual(result["exactEndpointRGBAComparisons"],28)

    def test_native_missing_directory_fails_not_skips(self):
        with self.assertRaisesRegex(ValueError,"Native assets directory missing"):
            self.verify(self.base/"absent")

    def test_native_missing_intermediate_fails(self):
        native=self.native();(native/"player-allrelease-01-03.png").unlink()
        with self.assertRaisesRegex(ValueError,"exactly210"):
            self.verify(native)

    def test_native_extra_intermediate_fails(self):
        native=self.native();shutil.copy2(native/"player-allrelease-01-03.png",native/"player-allrelease-05-03.png")
        with self.assertRaisesRegex(ValueError,"exactly210"):
            self.verify(native)

    def test_native_changed_bytes_fail(self):
        native=self.native();path=native/"player-allrelease-01-03.png"
        path.write_bytes(path.read_bytes()+b"changed")
        with self.assertRaisesRegex(ValueError,"Native intermediate byte mismatch"):
            self.verify(native)

    def test_native_endpoint_pixels_fail(self):
        native=self.native();path=native/"player-source-s-neutral.png"
        with Image.open(path) as im:
            im=im.convert("RGBA");im.putpixel((0,0),(255,0,0,255));im.save(path)
        with self.assertRaisesRegex(ValueError,"Native endpoint RGBA mismatch"):
            self.verify(native)

    def test_native_endpoint_metadata_allowed_when_pixels_exact(self):
        native=self.native();path=native/"player-source-s-neutral.png"
        original=v.sha(path)
        with Image.open(path) as im:
            metadata=PngImagePlugin.PngInfo();metadata.add_text("test","same pixels, different PNG metadata")
            im.save(path,pnginfo=metadata)
        self.assertNotEqual(v.sha(path),original)
        self.assertEqual(self.verify(native)["nativeAssets"]["exactEndpointRGBAComparisons"],28)


if __name__=="__main__":
    unittest.main(verbosity=2)
