"""Create labeled logical-size inspection sheets from immutable native captures.
Derived review images only, never native evidence. Original PNG bytes unchanged.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
CAPTURES = HERE / 'scene/native-capture-v9'
OUTPUT = HERE / 'inspection-sheets'

if __name__ == '__main__':
    OUTPUT.mkdir(exist_ok=False)
    receipt = {'kind': 'DERIVED_LOGICAL_SIZE_INSPECTION_NOT_NATIVE_CAPTURE', 'inputs': {}, 'outputs': {}}
    for variant, width, height in [('native',704,326), ('half',352,163), ('grayscale',704,326)]:
        sheet = Image.new('RGB', (width*2, (height+26)*3), '#202020')
        draw = ImageDraw.Draw(sheet)
        for row, zoom in enumerate((100,125,140)):
            for column, arm in enumerate(('control','candidate')):
                path = CAPTURES / f'source-scene-{arm}-ordinary-z{zoom}-{variant}.png'
                receipt['inputs'][str(path.relative_to(HERE))] = hashlib.sha256(path.read_bytes()).hexdigest()
                with Image.open(path) as image:
                    display = image.convert('RGB').resize((width,height), Image.Resampling.LANCZOS)
                x, y = column*width, row*(height+26)
                label = 'BASELINE V8' if arm == 'control' else 'CANDIDATE V9'
                draw.text((x+5,y+6),f'{label} | zoom {zoom/100:g} | {variant} logical {width}x{height} | derived',fill='white')
                sheet.paste(display,(x,y+26))
        destination = OUTPUT / (variant + '.png')
        sheet.save(destination)
        receipt['outputs'][destination.name] = hashlib.sha256(destination.read_bytes()).hexdigest()
    (OUTPUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
