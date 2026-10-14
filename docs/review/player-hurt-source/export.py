"""BP-002/BP-007 study export; uniform scale, annotated roots, no art admission."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json
ROOT=Path(__file__).resolve().parent
source=Image.open(ROOT/'source.png').convert('RGBA')
# Manually annotated approximate boot sole centers in full source coordinates.
# These are visual landmarks, not collision geometry or proven planted contacts.
contacts=[[(265,701),(408,799)],[(813,703),(980,801)],[(1398,702),(1518,801)]]
scale=312/706
records=[]; frames=[]
for i,pair in enumerate(contacts):
    left=i*source.width//3; right=(i+1)*source.width//3
    cell=source.crop((left,0,right,source.height))
    a=cell.getchannel('A'); cell.putalpha(a.point(lambda v:0 if v<=32 else 255 if v>=240 else round((v-32)*255/208)))
    root=(sum(p[0] for p in pair)/2-left,sum(p[1] for p in pair)/2)
    # One scale for all cells; no per-frame alpha-box normalization or deformation.
    scaled=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS)
    offset=(round(192-root[0]*scale),round(336-root[1]*scale))
    frame=Image.new('RGBA',(384,384));frame.alpha_composite(scaled,offset)
    path=ROOT/f'hurt-west-{i+1:02}.png';frame.save(path);frames.append(frame)
    landmarks=[[(p[0]-left)*scale+offset[0],p[1]*scale+offset[1]] for p in pair]
    records.append({'frame':path.name,'sourceCell':[left,0,right,source.height],
        'sourceSoleCentersApproximate':pair,'sourceRootInCell':root,'scale':scale,'offset':offset,
        'exportSoleCentersApproximate':landmarks,'alphaBounds':frame.getchannel('A').getbbox(),
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
plate=Image.new('RGBA',(1152,430),(43,45,48,255));d=ImageDraw.Draw(plate)
for i,frame in enumerate(frames):
    plate.alpha_composite(frame,(i*384,35));d.text((i*384+16,12),f'POSE {i+1} / 384 px export',fill='white')
    for x,y in records[i]['exportSoleCentersApproximate']:
        d.ellipse((i*384+x-3,y+32,i*384+x+3,y+38),outline='#ffd56a',width=1)
plate.convert('RGB').save(ROOT/'registered-plate.png')
record={'status':'CAPTURED source study; NOT ADMITTED','sourceSHA256':hashlib.sha256((ROOT/'source.png').read_bytes()).hexdigest(),
 'tool':'built-in image_gen; Pillow deterministic export','canvas':[384,384],
 'logicalCanvas':[64,64],'logicalAnchor':[32,56],'pixelAnchor':[192,336],
 'alphaCleanup':'<=32 transparent; >=240 opaque; linear between; RGB unchanged',
 'frames':records,'limitations':['manual approximate sole landmarks','flat raster source, no editable rig','not complete four-facing player family','not runtime capture']}
(ROOT/'export-records.json').write_text(json.dumps(record,indent=2)+'\n')
print('Three 384x384 candidates, one uniform scale; no production resources changed.')
