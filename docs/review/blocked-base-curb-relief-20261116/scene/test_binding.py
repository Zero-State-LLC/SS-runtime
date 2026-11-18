"""In-memory synthetic recommendation tests only. Never bind/prepare or recommend art."""
import copy
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('_v9_binding_tests',HERE/'supplement_binding.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)


def envelope():
    manifest=b.SOURCE/'manifest.json'
    source=b.load(manifest)
    evidence=HERE.parent/'CONTRACT.md'
    return dict(schema='blocked-base-curb-recommendations-009',manifest=dict(path=str(manifest.relative_to(b.ROOT)),sha256=b.sha(manifest)),
                dependencies=[dict(path=str((b.SOURCE/name).relative_to(b.ROOT)),sha256=digest) for name,digest in sorted(source['files'].items())],
                recommendation=dict(reviewerRole='coordinator',decision='recommended',scope='isolated-ordinary-scene',manifestSHA256=b.sha(manifest),evidence=dict(path=str(evidence.relative_to(b.ROOT)),sha256=b.sha(evidence))))


class Bindings(unittest.TestCase):
    def setUp(self):self.rec=envelope()

    def test_source_replay_and_independent_semantics_in_memory_only(self):
        # Synthetic role/evidence wrapper only, deliberately no assembly/preparation output.
        self.assertEqual(len(b.validate(self.rec)['supplements']),53)

    def test_pending_rejected_worker_and_wrong_scope_fail(self):
        for key,value in [('decision','pending'),('decision','rejected'),('reviewerRole','source-worker'),('scope','production')]:
            bad=copy.deepcopy(self.rec);bad['recommendation'][key]=value
            with self.assertRaises(ValueError):b.validate(bad)

    def test_stale_final_manifest_recommendation(self):
        self.rec['recommendation']['manifestSHA256']='0'*64
        with self.assertRaises(ValueError):b.validate(self.rec)

    def test_source_cannot_supply_own_evidence(self):
        for path in (b.SOURCE/'API.md',b.SOURCE_ROOT/'API.md',b.SOURCE_ROOT/'attempt-01/registration.json',b.SOURCE_ROOT/'attempt-01/source-snapshot/API.md'):
            with self.subTest(path=path):
                self.rec['recommendation']['evidence']=dict(path=str(path.relative_to(b.ROOT)),sha256=b.sha(path))
                with self.assertRaisesRegex(ValueError,'source descendant'):b.validate(self.rec)

    def test_first_attempt_manifest_cannot_substitute_final(self):
        first=b.SOURCE_ROOT/'manifest.json'
        self.rec['manifest']=dict(path=str(first.relative_to(b.ROOT)),sha256=b.sha(first))
        self.rec['recommendation']['manifestSHA256']=b.sha(first)
        with self.assertRaisesRegex(ValueError,'Exact final manifest path'):b.validate(self.rec)

    def test_rehashed_final_manifest_cannot_change_pin(self):
        path=b.SOURCE/'manifest.json';real_sha=b.sha
        self.rec['manifest']['sha256']=self.rec['recommendation']['manifestSHA256']='f'*64
        with patch.object(b,'sha',side_effect=lambda p:'f'*64 if Path(p)==path else real_sha(p)):
            with self.assertRaisesRegex(ValueError,'Pinned final attempt02'):b.validate(self.rec)

    def test_final_dependency_bytes_rehashed_even_if_replay_cached(self):
        import json
        path=b.SOURCE/'materials.json';real_sha=b.sha
        key=json.dumps(self.rec,sort_keys=True)
        b._VERIFIED.add(key)
        try:
            with patch.object(b,'sha',side_effect=lambda p:'f'*64 if Path(p)==path else real_sha(p)):
                with self.assertRaisesRegex(ValueError,'stale dependency'):b.validate(self.rec)
        finally:b._VERIFIED.discard(key)

    def test_first_attempt_dependency_bytes_remain_immutable(self):
        path=b.SOURCE_ROOT/'attempt-01/registration.json';real_sha=b.sha
        with patch.object(b,'sha',side_effect=lambda p:'f'*64 if Path(p)==path else real_sha(p)):
            with self.assertRaisesRegex(ValueError,'stale dependency'):b.validate(self.rec)

    def test_first_source_image_cannot_substitute_final_image(self):
        path=b.SOURCE/'manifest.json';manifest=b.load(path);real_load=b.load
        manifest['sprites'][0]['image']=b.load(b.SOURCE_ROOT/'attempt-01/registration.json')[0]['image']
        with patch.object(b,'load',side_effect=lambda p:manifest if Path(p)==path else real_load(p)):
            with self.assertRaisesRegex(ValueError,'Final output registration'):b.validate(self.rec)

    def test_dependency_missing_or_rehashed(self):
        for mutate in (lambda r:r['dependencies'].pop(),lambda r:r['dependencies'][0].update(sha256='0'*64)):
            bad=copy.deepcopy(self.rec);mutate(bad)
            with self.assertRaises(ValueError):b.validate(bad)

    def test_semantic_forgery_with_rehashed_manifest_rejected(self):
        original=b.load(b.SOURCE/'geometry.json')
        original['sprites'][0]['faces'][0]['vertices'][0][2]=0
        real_load=b.load
        def altered(path):
            return original if Path(path)==b.SOURCE/'geometry.json' else real_load(path)
        with patch.object(b,'load',side_effect=altered):
            with self.assertRaises(ValueError):b.validate(self.rec)

    def test_unknown_envelope_fields_rejected(self):
        self.rec['autoRecommend']=True
        with self.assertRaises(ValueError):b.validate(self.rec)

if __name__=='__main__':unittest.main()
