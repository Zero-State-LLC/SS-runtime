"""One-time authored mesh edits. Renderer consumes mesh.json directly, not this script.
Each pier/bay/moulding below is deliberately dimensioned, not a noise/procedural art retry.
Inherited base/steps preserve world registration. Closed back surfaces are authored.
"""
import copy
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'stone-editable-master-20261116'
base=json.loads((OLD/'mesh.json').read_text())
parts=[]

def prism(name,outline,low,high,paint,group='building'):
    n=len(outline)
    parts.append(dict(name=name,vertices=[[x,y,z] for z in (low,high) for x,y in outline],
        faces=[list(reversed(range(n))),list(range(n,2*n))]+[[i,(i+1)%n,(i+1)%n+n,i+n] for i in range(n)],
        material=paint,group=group,provenance='individually authored closed component'))

def box(name,x0,y0,x1,y1,z0,z1,paint):
    prism(name,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z0,z1,paint)

def side(name,axis,a,b,z0,z1,front,back,paint,bevel=0):
    if bevel:
        p=[(a+bevel,front),(b-bevel,front),(b,front+bevel),(b,back),
           (a,back),(a,front+bevel)]
    else:p=[(a,front),(b,front),(b,back),(a,back)]
    if axis=='west':p=[(y,x) for x,y in reversed(p)]
    prism(name,p,z0,z1,paint)

def diagonal(name,t0,t1,z0,z1,front,back,paint):
    # t is distance along x-y, front/back are x+y planes.
    p=[((front+t0)/2,(front-t0)/2),((front+t1)/2,(front-t1)/2),
       ((back+t1)/2,(back-t1)/2),((back+t0)/2,(back-t0)/2)]
    prism(name,p,z0,z1,paint)

# Original footprint vertices are retained as real base geometry at z=0.
foundation=copy.deepcopy(next(p for p in base if p['name']=='wall-mass-complete-hidden-back-and-floor'))
foundation['name']='registered-foundation'
foundation['material']='foundation'
for vertex in foundation['vertices']:
    if vertex[2]>0:vertex[2]=7.8
parts.append(foundation)
# The original filled upper shell is intentionally replaced with an inset closed core.
# Windows and entry now have actual six-unit cavities, not panels on a filled facade.
prism('authored-inset-core',[(28,7),(121,7),(121,121),(7,121),(7,28)],7.8,79,'hidden-stone')
box('hidden-back-east-wall',121,0,128,128,0,79,'hidden-stone')
box('hidden-back-north-wall',0,121,121,128,0,79,'hidden-stone')

# Individually dimensioned south and west face layouts, no mirrored bitmap.
piers=[('south-near','south',24,35,'south-near-stone'),('south-middle','south',70,79,'south-middle-stone'),
       ('south-far','south',119,128,'south-far-stone'),('west-near','west',24,36,'west-near-stone'),
       ('west-middle','west',72,82,'west-middle-stone'),('west-far','west',119,128,'west-far-stone')]
for name,axis,a,b,paint in piers:
    side(name+'-shaft',axis,a,b,18,66,-2.4,7,paint,1.1)
    side(name+'-plinth',axis,a-.5,b+.5,0,17,-2.8,7,'dark-'+name,.8)
    side(name+'-base-socle',axis,a-1,b+1,16,20,-3.4,7,'stone-edge',.7)
    side(name+'-capital-neck',axis,a-.4,b+.4,63,66,-3.2,7,'stone-shadow',.5)
    side(name+'-capital-top',axis,a-1.3,b+1.3,66,69,-4.5,7,'stone-edge',.8)
    side(name+'-inset',axis,a+1.5,b-1.5,22,62,-2.65,-2.3,paint)

bays=[('south-bay-a','south',35,70,'south-window-a'),('south-bay-b','south',79,119,'south-window-b'),
      ('west-bay-a','west',36,72,'west-window-a'),('west-bay-b','west',82,119,'west-window-b')]
for name,axis,a,b,paint in bays:
    side(name+'-lower-wall',axis,a,b,0,22,0,7,'plinth-'+name)
    side(name+'-back-glass',axis,a+1.5,b-1.5,23,64,5.6,6.1,paint)
    side(name+'-left-reveal',axis,a,a+1.5,22,65,-.5,6,'stone-shadow')
    side(name+'-right-reveal',axis,b-1.5,b,22,65,-.5,6,'stone-shadow')
    side(name+'-left-inner-frame',axis,a+1.5,a+2.4,23,64,4.4,6.2,'window-frame')
    side(name+'-right-inner-frame',axis,b-2.4,b-1.5,23,64,4.4,6.2,'window-frame')
    side(name+'-single-crossbar',axis,a+1.5,b-1.5,37,38.3,4.2,6.2,'window-frame')
    side(name+'-sill',axis,a-.6,b+.6,21,23,-3,7,'sill-'+name,.7)
    side(name+'-head-wall',axis,a,b,64,69,0,7,'stone-shadow')
    side(name+'-head-edge',axis,a-.5,b+.5,64,65.5,-2.8,7,'stone-edge')

# Stronger layered cornice, all extruded with closed returns.
for axis in ('south','west'):
    side(axis+'-frieze',axis,24,128,69,74,-1.8,7,axis+'-frieze-paint')
    side(axis+'-cornice-shadow',axis,24,128,73.2,74.3,-3.4,7,'stone-shadow')
    side(axis+'-cornice-bed',axis,24,128,74.3,76.2,-4.5,7,'stone-edge')
    side(axis+'-cornice-crown',axis,24,128,77,79,-5.2,7,'crown-'+axis,.6)
# Individually placed brackets, not an even repetitive tooth grid.
for name,axis,a,b in [('s1','south',28,33),('s2','south',71,77),('s3','south',120,126),
                      ('w1','west',27,34),('w2','west',74,80),('w3','west',121,126)]:
    side('bracket-'+name,axis,a,b,65,73,-4.4,-1.7,'stone-shadow',.6)
    side('bracket-cap-'+name,axis,a-.5,b+.5,71,73,-4.8,-1.2,'stone-edge',.4)

# Cut-back doorway is visibly recessed: columns at sum=18, door leaf at sum=31.
diagonal('entry-left-pier',-23,-13,8,65,18,35,'entry-left-stone')
diagonal('entry-right-pier',13,23,8,65,18,35,'entry-right-stone')
diagonal('entry-left-plinth',-23,-13,0,19,17,35,'entry-plinth')
diagonal('entry-right-plinth',13,23,0,19,17,35,'entry-plinth')
diagonal('entry-left-base',-24,-12,18,21,16,35,'stone-edge')
diagonal('entry-right-base',12,24,18,21,16,35,'stone-edge')
diagonal('entry-head',-23,23,63,74,19,35,'entry-head-stone')
diagonal('entry-lintel',-24,24,63,66,16,35,'stone-edge')
diagonal('entry-crown-bed',-25,25,74,76.2,14,35,'stone-edge')
diagonal('entry-crown-top',-26,26,77,79,13,35,'crown-south')
diagonal('door-recess-back',-13,13,8.5,63,32.5,34,'entry-dark')
diagonal('door-leaf',-11.5,11.5,9,60,31.3,32.5,'door-painted')
diagonal('door-left-stile',-11.5,-10,9,60,30.8,32,'door-frame')
diagonal('door-right-stile',10,11.5,9,60,30.8,32,'door-frame')
diagonal('door-upper-rail',-11.5,11.5,51,52.2,30.8,32,'door-frame')
diagonal('door-mid-rail',-11.5,11.5,28,29.2,30.8,32,'door-frame')
diagonal('door-bottom-rail',-11.5,11.5,13,14.2,30.8,32,'door-frame')
diagonal('door-mail-slot',-5,4,25,26.2,30.3,32,'brass')
diagonal('door-handle',7.8,8.6,32,38,30,32,'brass')
# Small amber entry lamp, an authored visible benchmark detail, not a new gameplay source.
diagonal('entry-lamp-housing',-3,3,61,65,14,20,'window-frame')
diagonal('entry-lamp-glass',-2,2,61.4,64.3,13.7,14.4,'amber')

for old in [p for p in base if p['group']=='stairs']:
    part=copy.deepcopy(old)
    part['material']='stair-'+part['name']
    # Extend upper backs to the newly inset threshold, not an inferred source contour.
    for v in part['vertices']:
        if v[0]+v[1]>24:
            v[0]+=4
            v[1]+=4
    part['provenance']='explicit inherited stair edited to authored inset door, collision unchanged'
    parts.append(part)
prism('authored-complete-roof',[(24,0),(128,0),(128,128),(0,128),(0,24)],78.9,79.1,'roof-authored')
box('roof-back-parapet-x',126,0,129,128,79,81,'hidden-stone')
box('roof-back-parapet-y',0,126,126,129,79,81,'hidden-stone')
(HERE/'mesh.json').write_text(json.dumps(parts,indent=2)+'\n')
print('Authored',len(parts),'closed parts')
