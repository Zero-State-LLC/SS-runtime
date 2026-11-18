"""One bounded correction authorized by SOURCE-REVIEW-01.md. Never writes attempt01."""
import json, hashlib, shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent
ROOT=SOURCE.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):
    path=HERE/name
    if path.exists():raise RuntimeError('Immutable correction authoring output exists: '+name)
    path.write_text(json.dumps(obj,indent=2)+'\n')
def main():
    # Freeze ALL first evidence, including original code/manifest snapshot, before any correction render.
    paths=[p for p in SOURCE.iterdir() if p.is_file()]+[p for p in (SOURCE/'attempt-01').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    write('attempt-01-frozen-sha256.json',{str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)})
    shutil.copyfile(SOURCE/'geometry.json',HERE/'geometry.json')
    write('materials.json',dict(schema='bounded-base-curb-material-correction-002',attempt=2,maximumAttempts=2,authorization=dict(path='docs/review/blocked-base-curb-relief-20261116/SOURCE-REVIEW-01.md',sha256=sha(SOURCE.parent/'SOURCE-REVIEW-01.md')),geometrySHA256=sha(HERE/'geometry.json'),input='docs/review/building-perspective-detail-20261116/context/inputs/facade.png',crop=[228,250,270,500],tilePixels=[144,72],masonryMeanRGB=[126,126,115],curbMeanRGB=[148,149,140],capMeanRGB=[137,137,126],textureContrast=.14,mortarRGB=[98,98,89],highlightRGB=[142,141,128],uvScale=[.5,.5],masonryCourseHeightWorld=9,masonryBlockWidthWorld=36,staggerFraction=.5,geometryChange=False,registrationChange=False))
    print('Frozen first attempt and authored one separate material correction')
if __name__=='__main__':main()
