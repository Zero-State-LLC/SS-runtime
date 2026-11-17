"""Freeze exact first-attempt source dependencies, once. No source recommendation."""
import json, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    path=HERE/'manifest.json'
    if path.exists():raise RuntimeError('Manifest frozen, cannot overwrite attempted evidence')
    files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.log' and p.name not in ('manifest.json','VALIDATION.md','validation.json')}
    result=dict(schema='blocked-base-curb-source-009',attempt=1,status='FIRST_PREVIEW_PENDING_COORDINATOR',files=files,baselineFiles=json.loads((HERE/'baseline-sha256.json').read_text()),sprites=json.loads((HERE/'attempt-01/registration.json').read_text()),nativeEvidence=False,sourceRecommendation=None,sourceReplay='PYTHONDONTWRITEBYTECODE=1 python3 replay.py --out EMPTY_DIRECTORY',validation='PYTHONDONTWRITEBYTECODE=1 python3 test_source.py',allowedAffectedRegions=dict(blockedBaseTriangle=[[512,640],[551,640],[512,679]],curb='Only existing V8 semantic ID2 within [452,572,984,796]',contactShading='Only bottom .75 world units of vertical faces'),limits=['No aesthetic acceptance inferred from tests','Native geometry depth requires scene verification','Nine historical offcrop contact contours remain unknown','No second attempt without coordinator bounded correction'])
    path.write_text(json.dumps(result,indent=2)+'\n');print('Frozen manifest SHA256',sha(path),len(files),'files')
if __name__=='__main__':main()
