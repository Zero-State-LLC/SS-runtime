#!/usr/bin/env python3
"""Replay editable plan into full registered ground, SVG, semantic IDs and first preview.
Deterministic material texture, no external services and no historical writes.
"""
import hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw
import material
HERE=Path(__file__).resolve().parent
COLORS={1:(69,76,76),2:(151,149,132),3:(122,128,118),4:(82,91,88)}
def main():
    p=json.loads((HERE/'plan.json').read_text());n=4608
    ids=Image.new('L',(n,n),1);d=ImageDraw.Draw(ids)
    def box(bounds,out=0):
        x0,y0,x1,y1=bounds
        return [round(2*(x0-out)),round(n-2*(y1+out)),round(2*(x1+out))-1,round(n-2*(y0-out))-1]
    rects=[[*b['minWorld'],*b['maxWorld']] for b in p['buildings']]
    plazas=[q['bounds'] for q in p['layout']['plazas']]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="4608" height="4608" viewBox="0 0 4608 4608">','<title>Bounded correction02. Shared plan unchanged. Presentation only.</title>','<defs>']
    for key,width,height in [(1,192,192),(2,192,192),(3,512,384),(4,192,192)]:
        svg.append(f'<pattern id="material-{key}" patternUnits="userSpaceOnUse" width="{width}" height="{height}"><image href="material-{key}-tile.png" width="{width}" height="{height}"/></pattern>')
    svg.extend(['<mask id="road-only"><image href="road-mask.png" width="4608" height="4608"/></mask>','</defs>'])
    def draw_rect(r,out,material):
        q=box(r,out);d.rectangle(q,fill=material)
        svg.append(f'<rect x="{q[0]}" y="{q[1]}" width="{q[2]-q[0]+1}" height="{q[3]-q[1]+1}" fill="url(#material-{material})"/>')
    draw_rect([0,0,2304,2304],0,1)
    for r in rects:draw_rect(r,28,2)
    for r in plazas:draw_rect(r,4,2)
    for r in rects:draw_rect(r,24,3)
    for r in plazas:draw_rect(r,0,3)
    for r in rects:draw_rect(r,3,4)
    ids.save(HERE/'material-ids.png')
    image=material.paint(ids)
    svg.append('<g mask="url(#road-only)">')
    svg.append((HERE/'road-details.svg-fragment').read_text());svg.append('</g>')
    ink=ImageDraw.Draw(image)
    for b in p['buildings']:
        contour=b['actualContactWorld']
        if contour:
            pts=[(round(2*x),round(n-2*y)) for x,y in contour]
            ink.line(pts+[pts[0]],fill=(47,57,54),width=3)
            svg.append('<polygon points="'+' '.join(f'{2*x},{n-2*y}' for x,y in contour)+'" fill="none" stroke="#2f3936" stroke-width="3"/>')
    # Contact-only baked shadows, bounded by explicit radius. Source prop art unchanged.
    overlay=Image.new('RGBA',(n,n));sd=ImageDraw.Draw(overlay)
    for prop in p['props']:
        x,y=prop['worldRoot'];r=prop['shadowRadiusWorld']
        sd.ellipse(box([x-r,y-r*.5,x+r,y+r*.5]),fill=(26,34,29,round(255*prop['shadowAlphaMax'])))
        svg.append(f'<ellipse cx="{2*x}" cy="{n-2*y}" rx="{2*r}" ry="{r}" fill="#1a221d" opacity="{prop["shadowAlphaMax"]}"/>')
    image=Image.alpha_composite(image.convert('RGBA'),overlay).convert('RGB');image.save(HERE/'ground.png')
    svg.append('</svg>');(HERE/'ground.svg').write_text('\n'.join(svg)+'\n')
    # Plan preview contains material art plus honest diagnostic overlays, not native scene.
    preview=image.crop((0,n-2*1536,n,n)).resize((1152,768),Image.Resampling.LANCZOS)
    pd=ImageDraw.Draw(preview)
    def pv(q):return (q[0]/2,(1536-q[1])/2)
    for b in p['buildings']:
        pts=[pv(q) for q in b['foundationWorld']];pd.line(pts+[pts[0]],fill='#d6a96c',width=1)
        pd.text(pv([b['minWorld'][0]+5,b['maxWorld'][1]-8]),b['id'].split('-')[1],fill='white')
        if b['actualContactWorld']:
            for q in b['actualContactWorld']:
                xx,yy=pv(q);pd.ellipse((xx-2,yy-2,xx+2,yy+2),fill='#67dcce')
        for q in b['virtualCorners']:
            xx,yy=pv(q['world']);pd.line((xx-4,yy-4,xx+4,yy+4),fill='#ff5050',width=2);pd.line((xx-4,yy+4,xx+4,yy-4),fill='#ff5050',width=2)
    for prop in p['props']:
        xx,yy=pv(prop['worldRoot']);pd.ellipse((xx-4,yy-4,xx+4,yy+4),outline='#98e66f',width=2)
    pd.rectangle((8,8,840,46),fill='#20282a');pd.text((16,14),'FINAL CORRECTION 02 | cyan: actual mesh contacts | red X: virtual corner | amber: blocked envelope',fill='white');pd.text((16,29),'14 foundations + shared sidewalks/curbs. Raster-neighbor contacts unknown. NOT visual acceptance.',fill='white')
    preview.save(HERE/'final-plan-preview.png')
    image.crop((2*360,n-2*1024,2*1240,n-2*520)).resize((1100,630)).save(HERE/'final-source-detail.png')
    hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in HERE.iterdir() if f.is_file() and f.name not in ('manifest.json','validation.json')}
    (HERE/'manifest.json').write_text(json.dumps(dict(status='FINAL_CORRECTION_NOT_VISUALLY_ACCEPTED',attempt=2,files=hashes),indent=2)+'\n')
    print('Final correction preview generated. ground.png 4608x4608. One correction; no third art pass.')
if __name__=='__main__':main()
