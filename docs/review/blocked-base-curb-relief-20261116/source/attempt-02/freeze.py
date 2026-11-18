"""Freeze final correction once. Does not alter first manifest or recommend source."""
import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent
ROOT=SOURCE.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    path=HERE/'manifest.json'
    if path.exists():raise RuntimeError('Final correction manifest already frozen')
    files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.log' and p.name not in ('manifest.json','VALIDATION.md','validation.json')}
    baseline=json.loads((SOURCE/'baseline-sha256.json').read_text())
    added=['docs/review/scene-qa-repair-20261116/native.py','docs/review/scene-source-assembly-20261116/assemble.py','AppTests/SceneQAReviewDepth.swift','AppTests/BenchmarkAssets/newsbox.png','AppTests/BenchmarkAssets/tree.png','docs/review/building-perspective-detail-20261116/context/materials.json','docs/review/blocked-base-curb-relief-20261116/SOURCE-REVIEW-01.md']
    baseline.update({name:sha(ROOT/name) for name in added})
    result=dict(schema='blocked-base-curb-source-009',attempt=2,maximumAttempts=2,status='FINAL_CORRECTION_PENDING_COORDINATOR',files=files,baselineFiles=baseline,firstAttemptFiles=json.loads((HERE/'attempt-01-frozen-sha256.json').read_text()),sprites=json.loads((HERE/'output/registration.json').read_text()),nativeEvidence=False,sourceRecommendation=None,sourceReplay='PYTHONDONTWRITEBYTECODE=1 python3 replay.py --out EMPTY_DIRECTORY',validation='PYTHONDONTWRITEBYTECODE=1 python3 test_source.py',allowedAffectedRegions=dict(blockedBaseTriangle=[[512,640],[551,640],[512,679]],curb='Only unchanged V8 semantic ID2 within [452,572,984,796]',contactShading='Unchanged from attempt01'),limits=['One correction only, no third aesthetic attempt','Geometry/registration/alpha identical to first attempt','Native depth and final visual outcome remain coordinator judged'])
    path.write_text(json.dumps(result,indent=2)+'\n');print('Frozen final manifest',sha(path),len(files),'files')
if __name__=='__main__':main()
