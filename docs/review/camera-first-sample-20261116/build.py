"""Deterministic diagnostic crops only. No alpha recovery or production asset export."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageChops, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'approved-concept.png': '49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb',
    'proposal-01.png': '2f1f77902dcc3266ef17f0a0e9dc92f191e03442aaf61f38250b90a01a10219b',
    'proposal-02.png': 'b5daa26fc45974bfa3a6ddf2c82738b7ada9b11e34866401029f47d806eb8de3',
}

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def proposal_bounds(im):
    # White-background diagnostic threshold, NOT an accepted silhouette or alpha mask.
    r, g, b = im.convert('RGB').split()
    minimum = ImageChops.darker(ImageChops.darker(r, g), b)
    bounds = minimum.point(lambda value: 255 if value < 220 else 0).getbbox()
    if bounds is None:
        raise ValueError('No device pixels found')
    return bounds

def main():
    review = HERE / 'review'
    review.mkdir(exist_ok=True)
    plate = Image.new('RGB', (750, 510), '#343434')
    draw = ImageDraw.Draw(plate)
    records = []
    for idx, name in enumerate(EXPECTED):
        p = HERE / 'source' / name
        if digest(p) != EXPECTED[name]:
            raise ValueError(f'Immutable source changed: {name}')
        with Image.open(p) as original:
            im = original.convert('RGB')
            box = (880, 20, 1060, 470) if idx == 0 else proposal_bounds(im)
            crop = im.crop(box)
            # Original crop stays at 1:1, including 34px context around 416px device.
            height = 450 if idx == 0 else 416
            scale = height / crop.height
            shown = crop.resize((round(crop.width * scale), height), Image.Resampling.LANCZOS)
            x = idx * 250 + (250 - shown.width) // 2
            y = 42 if idx == 0 else 53
            plate.paste(shown, (x, y))
            draw.text((idx * 250 + 10, 12), ('FIXED REFERENCE', '01 NOT RECOMMENDED', '02 NOT RECOMMENDED')[idx], fill='white')
            records.append(dict(file=f'source/{name}', sha256=digest(p), dimensions=list(original.size), mode=original.mode,
                                diagnosticCrop=list(box), uniformPreviewScale=scale,
                                cropWidthHeightRatio=crop.width / crop.height,
                                nativeAlpha=('A' in original.getbands())))
    plate.save(review / 'same-height.png')
    ImageOps.grayscale(plate).save(review / 'same-height-gray.png')
    plate.resize((375, 255), Image.Resampling.LANCZOS).save(review / 'same-height-half.png')
    record = dict(status='COORDINATOR_REJECTED_SOURCE_PROPOSALS', ownerAccepted=False, productionAdmitted=False,
                  readyForNative=False, editableMasterComplete=False, stateExpansionAllowed=False,
                  sources=records, generatedBy='provider-native image generation, two sequential attempts',
                  comparison='Generated diagnostic occupied height 416px matches reference device height from prior observed rows31..446. Original crop retains scenery. Same height is not scene-scale registration.',
                  outcomes=dict(technical='Diagnostic source hashes and equal-height preview verified only',
                                coordinatorVisual='Not recommended: proportions, head/bracket, finial/base and highlights drift from original',
                                ownerAcceptance='NOT REQUESTED / NOT GRANTED', productionAdmission='BLOCKED'),
                  limitations=['Both outputs are RGB with textured near-white backgrounds, not requested transparent PNGs',
                               'Threshold bounding box is for preview only, not a usable alpha contour or ground anchor',
                               'Neither flattened proposal supplies editable hidden underpaint',
                               'No crop, recolor, nonuniform warp or third retry is used to disguise fidelity drift',
                               'Attempts01-03 in the earlier packet remain immutable owner-rejected history',
                               'No production, clip/state, collision, field or scene fixture substitution'],
                  nextAction='Use an explicitly layered artist-authored source matching reference landmarks before native integration. Do not expand rejected art.')
    (HERE / 'source-record.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))

if __name__ == '__main__':
    main()
