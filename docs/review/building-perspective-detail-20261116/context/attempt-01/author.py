"""One-time authoring of new context geometry, never edits production assets."""
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

def dump(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    inputs = HERE / 'inputs'
    inputs.mkdir(parents=True, exist_ok=True)
    sources = []
    def retain(relative, name):
        source = REPO / relative
        destination = inputs / name
        shutil.copyfile(source, destination)
        sources.append({'originalPath': relative, 'localPath': 'inputs/' + name, 'sha256': sha(source)})
    base = 'docs/review/stone-painted-facade-20261116/'
    for name in ('facade', 'door', 'roof'):
        retain(base + 'output/textures/' + name + '.png', name + '.png')
    retain(base + 'inputs/provider.json', 'stone-provider.json')
    retain(base + 'README.md', 'stone-source-provenance.md')
    capture = 'docs/review/scene-qa-framing-20261116/native-capture-v6/'
    retain(capture + 'source-scene-records.json', 'v6-records.json')
    retain(capture + 'source-scene-candidate-ordinary-z100-native.png', 'v6-z100-native.png')
    roles = ['solid-01-residential-west','solid-02-residential-north','solid-04-civic-west','solid-05-civic-dais']
    for role in roles:
        asset = 'env_' + role.replace('-', '_') + '@1x.png'
        retain('Sources/SurveillanceCore/Resources/RuntimeAssets/' + asset, asset)
    dump(HERE/'provenance.json', {'status':'NEW_REVIEW_SOURCE_NOT_ADMITTED', 'inputs':sources,
         'method':'New explicit axis-aligned world-space architectural geometry and per-face UVs. Existing independently generated painted atlas reused, not old isometric sprites stretched.',
         'residentialBrick':'New procedural mortar course layout over tinted painted stone pixels. Not original residential brick paint recovered.',
         'limits':['Windows contain baked painted recess and mullions. New geometric cornices, sills, pilasters, bays, roof caps and chimneys are actual relief.', 'Hidden faces reuse materials, not uniquely authored historical facades.', 'No provider generation performed in this packet. Existing provider metadata is inherited provenance, not a new generation receipt.']})
    materials = {
       'stone': {'input':'inputs/facade.png','crop':[228,250,270,500]},
       'foundation': {'input':'inputs/facade.png','crop':[0,605,523,774]},
       'window': {'input':'inputs/facade.png','crop':[82,213,211,542]},
       'cornice': {'input':'inputs/facade.png','crop':[0,0,523,53]},
       'frieze': {'input':'inputs/facade.png','crop':[0,50,523,171]},
       'door': {'input':'inputs/door.png','crop':[60,230,263,700]},
       'roof': {'input':'inputs/roof.png','crop':[0,0,552,548]},
       'brick': {'input':'inputs/facade.png','crop':[228,250,270,500], 'tint':[0.67,0.36,0.24], 'brickCourses':True},
       'teal': {'input':'inputs/facade.png','crop':[228,250,270,500], 'tint':[0.43,0.63,0.61]},
       'metal': {'input':'inputs/roof.png','crop':[0,0,552,548], 'tint':[0.65,0.70,0.72]},
       'terracotta': {'input':'inputs/facade.png','crop':[228,250,270,500], 'tint':[0.8,0.45,0.28]}}
    dump(HERE/'materials.json',materials)
    records=json.loads((inputs/'v6-records.json').read_text())
    capture=next(c for c in records['captures'] if c['arm']=='candidate' and c['zoom']==1)
    buildings=[]
    for role in roles:
        authority=next(s for s in capture['solids'] if s['id']==role)
        lo,hi=authority['minWorld'],authority['maxWorld']
        root=[(lo[i]+hi[i])/2 for i in range(2)]
        w,d=[hi[i]-lo[i] for i in range(2)]
        x0,y0,x1,y1=-w/2,-d/2,w/2,d/2
        residential='residential' in role
        dais='dais' in role
        height=112 if residential else 142
        faces=[]
        def box(name,x0,y0,x1,y1,z0,z1,material,top=None):
            if x1<=x0 or y1<=y0 or z1<=z0: raise ValueError(name)
            coordinates=[('south',[(x0,y0,z1),(x1,y0,z1),(x1,y0,z0),(x0,y0,z0)],[0,-1,0]),
             ('west',[(x0,y1,z1),(x0,y0,z1),(x0,y0,z0),(x0,y1,z0)],[-1,0,0]),
             ('north',[(x1,y1,z1),(x0,y1,z1),(x0,y1,z0),(x1,y1,z0)],[0,1,0]),
             ('east',[(x1,y0,z1),(x1,y1,z1),(x1,y1,z0),(x1,y0,z0)],[1,0,0]),
             ('roof',[(x0,y1,z1),(x1,y1,z1),(x1,y0,z1),(x0,y0,z1)],[0,0,1]),
             ('floor',[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)],[0,0,-1])]
            for side,vertices,normal in coordinates:
                faces.append({'name':name+'/'+side,'vertices':vertices,'normal':normal,'uv':[[0,0],[1,0],[1,1],[0,1]],'material':top if side=='roof' and top else material})
        def strip(name,z0,z1,inset,mat):
            # Four separate horizontal cornice/rail prisms, never a filled roof slab.
            thick=2
            box(name+'south',x0+inset,y0+inset,x1-inset,y0+inset+thick,z0,z1,mat)
            box(name+'north',x0+inset,y1-inset-thick,x1-inset,y1-inset,z0,z1,mat)
            box(name+'west',x0+inset,y0+inset,x0+inset+thick,y1-inset,z0,z1,mat)
            box(name+'east',x1-inset-thick,y0+inset,x1-inset,y1-inset,z0,z1,mat)
        box('authoritative-contact-plinth',x0,y0,x1,y1,0,5,'foundation','stone')
        if dais:
            box('step-2',x0+4,y0+4,x1-4,y1-4,5,9,'stone','roof')
            box('raised-paving',x0+8,y0+8,x1-8,y1-8,9,13,'cornice','roof')
            # Rails and actual balusters retain the civic platform identity.
            strip('balustrade-base',13,16,9,'cornice')
            strip('balustrade-top',31,34,9,'cornice')
            for side,length in [('south',w-22),('west',d-22),('north',w-22),('east',d-22)]:
                count=max(2,round(length/12))
                for i in range(count+1):
                    t=11+i*length/count
                    xx=x0+t if side in ('south','north') else (x0+10 if side=='west' else x1-10)
                    yy=y0+t if side in ('west','east') else (y0+10 if side=='south' else y1-10)
                    box(f'{side}-baluster-{i}',xx-1.2,yy-1.2,xx+1.2,yy+1.2,16,31,'stone')
            height=34
        else:
            box('masonry-shell',x0+3,y0+3,x1-3,y1-3,5,height,'brick' if residential else 'stone','roof')
            # Visible walls segmented into true bays instead of stretching a whole painted building.
            for side,length in [('south',w-8),('west',d-8)]:
                count=max(2,round(length/(38 if residential else 49)))
                pitch=length/count
                for i in range(count):
                    u0=4+i*pitch+3
                    u1=4+(i+1)*pitch-3
                    def panel(name,a,b,low,high,mat,depth=1.5):
                        if side=='south': box(name,x0+a,y0+1,x0+b,y0+1+depth,low,high,mat)
                        else: box(name,x0+1,y0+a,x0+1+depth,y0+b,low,high,mat)
                    for floor in range(2 if residential else 1):
                        low=13+floor*46
                        high=low+(37 if residential else 98)
                        panel(f'{side}-{i}-f{floor}-bay',u0,u1,low-2,high+3,'teal' if residential and i%3==0 else 'stone',3)
                        panel(f'{side}-{i}-f{floor}-glazing',u0+3,u1-3,low+2,high,'window',.55)
                        panel(f'{side}-{i}-f{floor}-sill',u0-1,u1+1,low-2,low,'cornice',4)
                        panel(f'{side}-{i}-f{floor}-lintel',u0-1,u1+1,high,high+3,'cornice',4)
                    if not residential:
                        panel(f'{side}-{i}-capital',u0-2,u0+3,113,119,'frieze',4)
                        panel(f'{side}-{i}-pilaster',u0-1,u0+2,10,113,'stone',4)
            strip('lower-stringcourse',7,10,0,'cornice')
            if residential: strip('floor-stringcourse',55,58,0,'cornice')
            strip('eaves',height-4,height+1,0,'cornice')
            strip('parapet',height+1,height+7,1,'frieze')
            strip('coping',height+7,height+9,0,'cornice')
            if residential:
                for i,(xx,yy) in enumerate([(x0+18,y1-19),(x1-24,y1-19)]):
                    box('chimney-'+str(i),xx,yy,xx+8,yy+9,height,height+22,'terracotta','metal')
                    box('chimney-cap-'+str(i),xx-1,yy-1,xx+9,yy+10,height+22,height+24,'cornice','metal')
            else:
                for i in range(3):
                    yy=y0+45+i*(d-90)/2
                    box('roof-lantern-base-'+str(i),-20,yy-14,20,yy+14,height,height+4,'stone','metal')
                    box('roof-lantern-'+str(i),-16,yy-10,16,yy+10,height+4,height+14,'window','roof')
        buildings.append({'solidID':role,'nodeName':'environment-upright-env_'+role.replace('-','_'),'worldPosition':root,'footprintWorld':authority,'faces':faces,'authoredHeight':height,'contactLocal':[[x0,y0,0],[x1,y0,0],[x1,y1,0],[x0,y1,0]],'character':'raised civic balustraded dais' if dais else ('two-storey brick residences with stone/teal bays and capped chimneys' if residential else 'tall civic masonry with pilasters, cornices and roof lanterns')})
    dump(HERE/'geometry.json',{'schema':'context-editable-geometry-001','projection':'D108: [(x-y)/sqrt(2),(x+y)/(2*sqrt(2))+z]','pixelsPerWorldUnit':4,'paddingPixels':24,'buildings':buildings})

if __name__=='__main__': main()
