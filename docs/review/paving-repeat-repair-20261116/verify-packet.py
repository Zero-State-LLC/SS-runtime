"""Portable review-packet checks. Run from repository root with Python + Pillow."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
SOURCE = Path('AppTests/WholeSceneAssets/whole-scene-muted-paving.png')
SHA = 'c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_source(data):
    assert digest(data) == SHA, 'source hash mismatch'


def validate_candidate(original, candidate):
    assert candidate.size == original.size == (1254, 1254), 'size mismatch'
    assert candidate.crop((20, 20, 1234, 1234)).tobytes() == original.crop((20, 20, 1234, 1234)).tobytes(), 'interior/orientation mismatch'
    assert candidate.crop((0, 0, 1254, 1)).tobytes() == candidate.crop((0, 1253, 1254, 1254)).tobytes(), 'top/bottom mismatch'
    assert candidate.crop((0, 0, 1, 1254)).tobytes() == candidate.crop((1253, 0, 1254, 1254)).tobytes(), 'left/right mismatch'


def rejects(fn):
    try:
        fn()
    except AssertionError:
        return
    raise AssertionError('mutation escaped guard')


raw = SOURCE.read_bytes()
validate_source(raw)
with Image.open(SOURCE) as image:
    original = image.convert('RGB')
with Image.open(ROOT / 'paving-muted-candidate.png') as image:
    candidate = image.convert('RGB')
validate_candidate(original, candidate)
rejects(lambda: validate_source(raw + b'mutation'))
changed = candidate.copy()
changed.putpixel((100, 100), (255, 0, 255))
rejects(lambda: validate_candidate(original, changed))
changed = candidate.copy()
changed.putpixel((100, 0), (255, 0, 255))
rejects(lambda: validate_candidate(original, changed))
rejects(lambda: validate_candidate(original, ImageOps.mirror(candidate)))
rejects(lambda: validate_candidate(original, candidate.resize((627, 627))))
manifest = json.loads((ROOT / 'provenance.json').read_text())
for name, record in manifest['repeat_previews'].items():
    path = ROOT / name
    assert digest(path.read_bytes()) == record['sha256'], name
    with Image.open(path) as image:
        assert list(image.size) == record['dimensions'], name
    if name.endswith('-full.png'):
        tile = original if 'original' in name else candidate
        with Image.open(path) as image:
            preview = image.convert('RGB')
        for y in range(3):
            for x in range(3):
                assert preview.crop((1254*x, 1254*y, 1254*(x+1), 1254*(y+1))).tobytes() == tile.tobytes(), 'repeat placement/orientation mismatch'
print('PASS: source, dimensions, exhaustive interior/orientation, exact boundaries, six attachment hashes/sizes, full 3x3 placement; five mutation rejection cases')
