"""One-time explicit geometry authoring. Replay consumes mesh.json, not this builder."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
outline=[(39,0),(128,0),(128,128),(0,128),(0,39)]
vertices=[[x,y,z] for z in (0,132) for x,y in outline]
faces=[]
for i,name in enumerate(['south','hidden-east','hidden-north','west','entry']):
    j=(i+1)%5
    # All copies keep the same upright left-to-right texture orientation viewed outside.
    faces.append(dict(name=name,indices=[i,j,j+5,i+5],uv=[[0,1],[1,1],[1,0],[0,0]],material='door' if i==4 else 'facade',hidden=i in (1,2)))
for name,indices in [('roof',list(range(5,10))),('floor',list(reversed(range(5))))]:
    faces.append(dict(name=name,indices=indices,uv=[[vertices[i][0]/128,vertices[i][1]/128] for i in indices],material='roof',hidden=name=='floor'))
mesh=dict(schema=1,vertices=vertices,faces=faces,units='world units',authoring='New closed chamfered prism, not reference-inferred geometry',height=132,chamfer=39)
(P/'mesh.json').write_text(json.dumps(mesh,indent=2)+'\n')
materials=dict(schema=1,rectConvention='Pillow half-open [left,top,right,bottom], explicitly authored, no inferred bounds',atlas='inputs/atlas.png',rects={'facade':[29,120,552,894],'door':[594,120,914,894],'roof':[956,248,1508,796]},reuse='Facade is copied upright onto south/west and hidden east/north, never silently mirrored. Hidden walls stretch the same full panel over 128 units.',relief='All pilasters, cornice, lamp, door trim and stairs are baked paint on flat faces. No extruded trim or tread geometry is claimed.')
(P/'materials.json').write_text(json.dumps(materials,indent=2)+'\n')
