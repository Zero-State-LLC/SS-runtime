"""Binder mutation unit tests. In-memory recommendation stubs never leave tests.
Dependency reads are explicitly mocked here, not source/authority/semantic checks.
No assembly/preparation/native files are produced and no art is recommended.
"""
import copy
import unittest
from unittest.mock import patch
from test_native import n

p = n.plan_adapter


class BinderMutations(unittest.TestCase):
    def setUp(self):
        self.plan = n.load(p.PLAN / 'plan.json')
        self.manifest = n.load(p.PLAN / 'manifest.json')
        self.material = n.load(p.PLAN / 'materials.json')
        def dep(name):
            return dict(path=str((p.PLAN / name).relative_to(n.ROOT)), sha256=n.sha(p.PLAN / name))
        self.binding = dict(schema='footprint-ground-recommendations-008', plan=dep('plan.json'),
                            manifest=dep('manifest.json'), validator=dep('test_plan.py'),
                            recommendation=dict(reviewerRole='coordinator', decision='recommended',
                                scope='isolated-ordinary-scene', planSHA256=self.manifest['files']['plan.json'],
                                sourceSHA256=self.manifest['files']['ground.png'],
                                evidence=dict(path='SYNTHETIC-IN-MEMORY-ONLY', sha256='0' * 64)))

    def reject(self):
        original = p.load
        def read(path):
            if path == p.PLAN / 'plan.json': return self.plan
            if path == p.PLAN / 'manifest.json': return self.manifest
            if path == p.PLAN / 'materials.json': return self.material
            return original(path)
        with patch.object(p, 'dependency', side_effect=lambda dep, root: root / dep['path']), \
             patch.object(p, 'load', side_effect=read):
            with self.assertRaises(ValueError): p.validate(self.binding)

    def test_worker_cannot_recommend_source(self):
        self.binding['recommendation']['reviewerRole'] = 'worker'; self.reject()

    def test_rejected_source_cannot_bind(self):
        self.binding['recommendation']['decision'] = 'rejected'; self.reject()

    def test_missing_source_recommendation_fails(self):
        self.binding.pop('recommendation'); self.reject()

    def test_stale_ground_recommendation_fails(self):
        self.binding['recommendation']['sourceSHA256'] = '0' * 64; self.reject()

    def test_stale_plan_recommendation_fails(self):
        self.binding['recommendation']['planSHA256'] = '0' * 64; self.reject()

    def test_forged_authority_even_with_matching_plan_hash_stub(self):
        self.plan['protected']['cameraRoot'][0] += 1; self.reject()

    def test_forged_player_source_authority(self):
        self.plan['protected']['actors'][0]['worldRoot'][0] += 1; self.reject()

    def test_forged_baseline_prop_root(self):
        self.plan['props'][1]['oldWorldRoot'] = [858, 716]; self.reject()

    def test_actual_prop_collision_fails_source_semantics(self):
        self.plan['props'][1]['worldRoot'] = [858, 780]; self.reject()

    def test_forged_virtual_contact_fails_source_semantics(self):
        self.plan['buildings'][2]['actualContactWorld'][0] = [512, 640]; self.reject()

    def test_missing_visible_building_fails_source_semantics(self):
        self.plan['buildings'].pop(2); self.reject()

    def test_unknown_plan_version_fails(self):
        self.plan['schema'] = 'footprint-ground-plan-999'; self.reject()

    def test_third_source_attempt_fails(self):
        self.plan['attempt'] = self.manifest['attempt'] = 3; self.reject()

    def test_missing_semantic_raster_fails(self):
        self.manifest['files'].pop('material-ids.png'); self.reject()

    def test_correction_cannot_rehash_changed_semantic_ids(self):
        self.manifest['files']['material-ids.png'] = '0' * 64; self.reject()

    def test_correction_cannot_rehash_changed_geometry_origin(self):
        self.manifest['files']['attempt-01/plan.json'] = '0' * 64; self.reject()

    def test_unknown_material_correction_rejected(self):
        self.material['attempt'] = self.material['maximumAttempts'] = 3; self.reject()

    def test_recursive_manifest_escape_rejected(self):
        self.manifest['files']['attempt-01/../../outside'] = '0' * 64; self.reject()

    def test_exact_validator_path_required(self):
        self.binding['validator']['path'] = 'some-other-validator.py'; self.reject()


if __name__ == '__main__':
    unittest.main()
