"""Revision02: corresponding-strip convex blending. Run from repository root."""
from pathlib import Path
import hashlib
import json
import math
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
SOURCE = Path('AppTests/WholeSceneAssets/whole-scene-muted-paving.png')
SOURCE_SHA = 'c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125'
BW = 20


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blend(a, b, distance):
    weight = (1 + math.cos(math.pi * distance / BW)) / 2
    return tuple(round(v + weight * ((v + z) / 2 - v)) for v, z in zip(a, b))


def stage(source, axis):
    result = source.copy()
    src, dst = source.load(), result.load()
    w, h = source.size
    for along in range(w if axis == 'y' else h):
        for d in range(BW):
            a = (along, d) if axis == 'y' else (d, along)
            b = (along, h-1-d) if axis == 'y' else (w-1-d, along)
            dst[a] = blend(src[a], src[b], d)
            dst[b] = blend(src[b], src[a], d)
    return result


def check_stage(source, result, axis):
    src, dst = source.load(), result.load()
    w, h = source.size
    for along in range(w if axis == 'y' else h):
        for d in range(BW):
            a = (along, d) if axis == 'y' else (d, along)
            b = (along, h-1-d) if axis == 'y' else (w-1-d, along)
            for c in range(3):
                lo, hi = sorted((src[a][c], src[b][c]))
                assert lo <= dst[a][c] <= hi, 'nonconvex strip blend'
                assert lo <= dst[b][c] <= hi, 'nonconvex strip blend'
                assert abs(dst[a][c] + dst[b][c] - src[a][c] - src[b][c]) <= 1, 'pair mean drift'
    # No edge0 propagation: each distance stays within its OWN paired bounds.
    # For every threshold a pair cannot acquire a new below-threshold value
    # unless at least one corresponding source pixel already was below it.
    # This is a local nonwidening guarantee, not an aesthetic acceptance test.


assert sha(SOURCE) == SOURCE_SHA
original = Image.open(SOURCE).convert('RGB')
assert original.size == (1254, 1254)
pass1 = stage(original, 'y')
candidate = stage(pass1, 'x')
check_stage(original, pass1, 'y')
check_stage(pass1, candidate, 'x')
assert candidate.crop((BW, BW, 1254-BW, 1254-BW)).tobytes() == original.crop((BW, BW, 1254-BW, 1254-BW)).tobytes()
p = candidate.load()
assert all(p[x, 0] == p[x, 1253] for x in range(1254))
assert all(p[0, y] == p[1253, y] for y in range(1254))
# Synthetic dark edge0 sentinel: values at distances 1..19 must not darken.
sentinel = Image.new('RGB', (64, 64), (150, 150, 150))
for x in range(64):
    sentinel.putpixel((x, 0), (20, 20, 20))
    sentinel.putpixel((x, 63), (40, 40, 40))
sentinel_out = stage(sentinel, 'y')
assert all(sentinel_out.getpixel((x, d)) == (150, 150, 150) for x in range(64) for d in range(1, BW)), 'dark edge widened'
# Reject the original edge0-smearing failure with the same bounds checker.
broken = pass1.copy()
broken.putpixel((100, 10), (0, 0, 0))
try:
    check_stage(original, broken, 'y')
except AssertionError:
    pass
else:
    raise AssertionError('nonconvex mutation escaped')
HERE.mkdir(parents=True, exist_ok=True)
candidate.save(HERE / 'paving-muted-candidate.png')
manifest = {'source_sha256': SOURCE_SHA, 'algorithm': 'paired strip RGB cosine blend, pass2 reads pass1 snapshot', 'bw': BW, 'tileUnits': 128, 'files': {}}
for label, tile in [('original', original), ('candidate', candidate)]:
    full = Image.new('RGB', (3762, 3762))
    for y in range(3):
        for x in range(3):
            full.paste(tile, (x*1254, y*1254))
    for kind, image in [('full', full), ('half', full.resize((1881, 1881), Image.Resampling.LANCZOS)), ('grayscale', ImageOps.grayscale(full))]:
        name = f'repeat-{label}-3x3-{kind}.png'
        image.save(HERE / name)
        manifest['files'][name] = {'sha256': sha(HERE / name), 'size': list(image.size)}
manifest['candidate_sha256'] = sha(HERE / 'paving-muted-candidate.png')
(HERE / 'provenance.json').write_text(json.dumps(manifest, indent=2) + '\n')
assert sha(SOURCE) == SOURCE_SHA
print('PASS: paired bounds both passes, pair-mean preservation within 1 RGB unit, unchanged interior, exact edges, dark-edge nonwidening sentinel, nonconvex mutation rejection, source hash')
print('Candidate SHA256:', manifest['candidate_sha256'])
