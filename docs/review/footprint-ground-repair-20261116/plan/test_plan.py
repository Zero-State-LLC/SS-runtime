#!/usr/bin/env python3
"""Independent semantic oracle: does not import author.py or replay.py."""
import copy,hashlib,json,math,unittest
from pathlib import Path
from PIL import Image,ImageChops
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
V7=ROOT/'docs/review/building-perspective-detail-20261116'
def load(p):return json.loads(p.read_text())
def need(x,message):
    if not x:raise ValueError(message)
def inside(x,y,lo,hi,pad=0):return lo[0]-pad<=x<hi[0]+pad and lo[1]-pad<=y<hi[1]+pad
def expected_material(p,x,y):
    boxes=p['buildings'];plazas=p['layout']['plazas']
    if any(inside(x,y,b['minWorld'],b['maxWorld'],3) for b in boxes):return 4
    if any(inside(x,y,b['minWorld'],b['maxWorld'],24) for b in boxes) or any(inside(x,y,q['bounds'][:2],q['bounds'][2:]) for q in plazas):return 3
    if any(inside(x,y,b['minWorld'],b['maxWorld'],28) for b in boxes) or any(inside(x,y,q['bounds'][:2],q['bounds'][2:],4) for q in plazas):return 2
    return 1
def validate(p,ids=None):
    rows=load(V7/'scene/native-capture-v7/source-scene-records.json')['captures'];c=next(c for c in rows if c['arm']=='candidate' and c['zoom']==1)
    need(p['registration']==dict(canvasPixels=[4608,4608],rootPixelsTopLeft=[0,4608],worldPosition=[0,0],drawSizeWorld=[2304,2304],kind='ground',coordinates='WORLD_X_RIGHT_Y_UP_SOURCE_TOP_LEFT'),'ground registration drift')
    for k in ['solids','cameraRoot','cameraFieldOrigin','cameraFieldAngleMilli','cameraHeadingMilli','cameraRange','centerWorld','controlsRetained']:need(p['protected'][k]==c[k],'protected '+k)
    need(p['protected']['actors']==[a for a in c['preprojectionInventory'] if not a['name'].startswith('benchmark-prop-')],'protected actor art/root drift')
    solids=[s for s in c['solids'] if s['id'].startswith('solid-')]
    need([b['id'] for b in p['buildings']]==[s['id'] for s in solids],'all14 envelope census')
    geometry={g['solidID']:g for g in load(V7/'context/geometry.json')['buildings']}
    regs={r['solidID']:r for r in load(V7/'context/registration.json')}
    for b,s in zip(p['buildings'],solids):
        need(b['minWorld']==s['minWorld'] and b['maxWorld']==s['maxWorld'],'solid envelope drift')
        lo,hi=s['minWorld'],s['maxWorld'];rect=[lo,[hi[0],lo[1]],hi,[lo[0],hi[1]]]
        need(b['foundationWorld']==rect,'foundation must seal entire blocked envelope')
        need(b['sidewalkOutsetWorld']==24 and b['curbWidthWorld']==4,'meaningful sidewalk/curb widths')
        if b['id'] in geometry:
            g=geometry[b['id']];r=regs[b['id']];root=g['worldPosition'];scale=4;pixelroot=r['rootPixelsTopLeft']
            actual={tuple(v[:2]) for f in g['faces'] for v in f['vertices'] if abs(v[2])<1e-8}
            actual={(x+root[0],y+root[1]) for x,y in actual};expected=set(map(tuple,rect))
        elif b['id']=='solid-03-transit-kiosk':
            m=load(V7/'kiosk/output/mesh.json');root=[512,640];scale=5;pixelroot=[500,1160]
            actual={(v[0]+512,v[1]+640) for v in m['vertices'] if abs(v[2])<1e-8}
            expected={(551,640),(640,640),(640,768),(512,768),(512,679)}
            need(b['virtualCorners']==[dict(world=[512,640],reason='omitted by actual chamfer39; blocked authoritative corner, NOT mesh vertex')],'virtual corner provenance')
        else:
            need(b['meshContactStatus']=='unavailable-retained-raster-no-mesh' and not b['actualContactWorld'] and not b['contactLandmarks'],'invented legacy mesh contact')
            continue
        need(set(map(tuple,b['actualContactWorld']))==expected,'actual contour differs from mesh boundary')
        need(expected<=actual,'landmark is not actual z0 vertex')
        need(len(b['contactLandmarks'])==len(expected),'actual landmark census')
        for landmark in b['contactLandmarks']:
            x,y=landmark['world'];need((x,y) in expected,'virtual landmark passed as actual')
            sx,sy=landmark['sourcePixelsTopLeft'];dx=(sx-pixelroot[0])/scale;dy=(pixelroot[1]-sy)/scale
            recovered=(root[0]+(dx+2*dy)/math.sqrt(2),root[1]+(-dx+2*dy)/math.sqrt(2))
            need(math.dist(recovered,[x,y])<1e-8,'contact source registration')
    need([q['name'] for q in p['props']]==['benchmark-prop-0','benchmark-prop-1'],'prop census')
    for prop in p['props']:
        x,y=prop['worldRoot'];r=prop['shadowRadiusWorld']
        need(0<prop['contactRadiusWorld']<=r<=16 and 0<=prop['shadowAlphaMax']<=.22,'prop contact/shadow limits')
        for s in c['solids']:
            lo,hi=s['minWorld'],s['maxWorld'];dx=max(lo[0]-x,0,x-hi[0]);dy=max(lo[1]-y,0,y-hi[1])
            need(math.hypot(dx,dy)>r,'prop intersects authoritative solid')
        for angle in range(360):
            xx=x+r*math.cos(math.radians(angle));yy=y+r*math.sin(math.radians(angle))
            need(expected_material(p,xx,yy)==3,'prop shadow leaves compatible sidewalk')
    if ids is not None:
        need(ids.size==(4608,4608),'semantic canvas')
        # Every foundation pixel, including offcrop and chamfer infill, must be foundation.
        for b in p['buildings']:
            x0,y0=b['minWorld'];x1,y1=b['maxWorld'];region=ids.crop((2*x0,4608-2*y1,2*x1,4608-2*y0))
            need(region.getextrema()==(4,4),'road/curb/sidewalk overlaps blocked building')
        # Independent half-pixel sampling on every rect edge and each ground material district.
        xs={.25,2303.75};ys={.25,1535.75}
        for b in p['buildings']:
            for edge in (b['minWorld'][0],b['maxWorld'][0]):
                for offset in (-28,-24,-3,0,3,24,28):xs.update([edge+offset-.25,edge+offset+.25])
            for edge in (b['minWorld'][1],b['maxWorld'][1]):
                for offset in (-28,-24,-3,0,3,24,28):ys.update([edge+offset-.25,edge+offset+.25])
        for q in p['layout']['plazas']:
            for edge in (q['bounds'][0],q['bounds'][2]):xs.update([edge-4.25,edge-3.75,edge-.25,edge+.25,edge+3.75,edge+4.25])
            for edge in (q['bounds'][1],q['bounds'][3]):ys.update([edge-4.25,edge-3.75,edge-.25,edge+.25,edge+3.75,edge+4.25])
        for x in xs:
            for y in ys:
                if 0<x<2304 and 0<y<1536:need(ids.getpixel((int(2*x),int(4608-2*y)))==expected_material(p,x,y),'ground boundary semantics')
    return True
def validate_ground_pixels(p,image):
    need(image.size==(4608,4608),'ground image canvas')
    spec=load(HERE/'materials.json')
    with Image.open(ROOT/spec['retainedPaving']['path']) as src:
        paving=src.convert('RGB').resize((512,384),Image.Resampling.LANCZOS)
        stone=src.crop((6,6,122,122)).convert('L').resize((192,192),Image.Resampling.BICUBIC)
    with Image.open(HERE/'road-details.png') as src:details=src.copy()
    bases={1:(57,57,56),2:(164,156,139),4:(111,103,88)}
    checked=0
    for py in range(11,4608,37):
        for px in range(11,4608,37):
            x=(px+.5)/2;y=(4608-py-.5)/2
            if any(math.dist([x,y],q['worldRoot'])<=q['shadowRadiusWorld']+1 for q in p['props']):continue
            near=False
            for b in p['buildings']:
                vertices=b['actualContactWorld']
                for a,z in zip(vertices,vertices[1:]+vertices[:1]):
                    dx,dy=z[0]-a[0],z[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)))
                    if math.dist([x,y],[a[0]+t*dx,a[1]+t*dy])<2:near=True
            if near:continue
            kind=expected_material(p,x,y);tx,ty=px%192,py%192
            if kind==3:expected=paving.getpixel((px%512,py%384))
            else:
                natural=(stone.getpixel((tx,ty))-125)//(5 if kind==1 else 3)
                grit=((tx*31+ty*43+tx*ty%71)%11-5)//(2 if kind==1 else 3)
                joint=24 if kind==2 and (tx%48<2 or ty%48<2) else 17 if kind==4 and (ty%24<2 or (tx+(24 if (ty//24)%2 else 0))%48<2) else 0
                bevel=5 if kind==2 and (tx%48 in (2,47) or ty%48 in (2,47)) else 0
                expected=tuple(max(0,min(255,v+natural+grit-joint+bevel)) for v in bases[kind])
            overlay=details.getpixel((px,py));alpha=overlay[3]
            if alpha:expected=tuple((expected[i]*(255-alpha)+overlay[i]*alpha+127)//255 for i in range(3))
            need(image.getpixel((px,py))==expected,'rendered ground does not match semantic material')
            checked+=1
    need(checked>14000,'ground pixel sample coverage')
    return checked
def validate_details(p,ids,details):
    need(details.size==ids.size,'road details canvas')
    forbidden=ids.point(lambda v:0 if v==1 else 255)
    need(ImageChops.multiply(details.getchannel('A'),forbidden).getbbox() is None,'road decoration escaped road material')
    for row in load(HERE/'materials.json')['roadDetails']:
        x0,y0,x1,y1=row['bounds'];area=details.crop((2*x0,4608-2*y1,2*x1,4608-2*y0))
        need(area.getchannel('A').getbbox() is not None,'missing declared road detail')
    # Every painted pixel must belong to a declared detail box; no unlisted road paint.
    allowed=Image.new('L',ids.size)
    from PIL import ImageDraw
    draw=ImageDraw.Draw(allowed)
    for row in load(HERE/'materials.json')['roadDetails']:
        x0,y0,x1,y1=row['bounds'];draw.rectangle((2*x0,4608-2*y1,2*x1-1,4608-2*y0-1),fill=255)
    need(ImageChops.multiply(details.getchannel('A'),ImageChops.invert(allowed)).getbbox() is None,'undeclared road detail')
    # Crossing retained worn-paint semantics, not just some alpha in its box.
    for row in load(HERE/'materials.json')['roadDetails']:
        if row['kind'] not in ('crossing','lane'):continue
        x0,y0,x1,y1=row['bounds'];kind=row['kind'];color=(181,172,139,190) if kind=='crossing' else (170,153,111,130)
        for py in range(4608-2*y1,4608-2*y0):
            for px in range(2*x0,2*x1):
                expected=(0,0,0,0) if (px*19+py*37)%17==0 else color
                need(details.getpixel((px,py))==expected,'crossing/lane exact paint or wear drift')
    return True
class PlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.p=load(HERE/'plan.json');cls.ids=Image.open(HERE/'material-ids.png').copy()
    def mutation(self,fn):
        p=copy.deepcopy(self.p);fn(p)
        with self.assertRaises(ValueError):validate(p)
    def test_attempt01_all17_files_immutable(self):
        folder=HERE/'attempt-01';manifest=folder/'manifest.json'
        self.assertEqual(hashlib.sha256(manifest.read_bytes()).hexdigest(),'ecbf9f50cf9d4860f64520c7c8c2d4aac250b204a7c7131dc8f042ab75b8f463')
        for name,digest in load(manifest)['files'].items():self.assertEqual(hashlib.sha256((folder/name).read_bytes()).hexdigest(),digest,name)
    def test_shared_contract_and_material_ids_unchanged(self):
        for name in ('plan.json','material-ids.png','v7-immutable-sha256.json'):
            self.assertEqual((HERE/name).read_bytes(),(HERE/'attempt-01'/name).read_bytes())
    def test_retained_paving_source_hashes(self):
        spec=load(HERE/'materials.json')
        for key in ('retainedPaving','retainedOriginal'):
            row=spec[key];self.assertEqual(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest(),row['sha256'])
        self.assertEqual(hashlib.sha256((HERE/'plan.json').read_bytes()).hexdigest(),spec['sharedPlanSHA256'])
    def test_paving_tile_is_retained_source_resample(self):
        with Image.open(ROOT/load(HERE/'materials.json')['retainedPaving']['path']) as source:expected=source.convert('RGB').resize((512,384),Image.Resampling.LANCZOS)
        with Image.open(HERE/'material-3-tile.png') as actual:self.assertEqual(actual.tobytes(),expected.tobytes())
    def test_road_details_semantically_clipped(self):
        with Image.open(HERE/'road-details.png') as details:self.assertTrue(validate_details(self.p,self.ids,details))
    def test_mutation_crossing_on_foundation(self):
        with Image.open(HERE/'road-details.png') as source:details=source.copy()
        details.putpixel((1100,3200),(180,170,140,255))
        with self.assertRaises(ValueError):validate_details(self.p,self.ids,details)
    def test_mutation_missing_crossing(self):
        with Image.open(HERE/'road-details.png') as source:details=source.copy()
        details.paste((0,0,0,0),(1352,3520,1512,3536))
        with self.assertRaises(ValueError):validate_details(self.p,self.ids,details)
    def test_mutation_extra_road_detail(self):
        with Image.open(HERE/'road-details.png') as source:details=source.copy()
        details.putpixel((11,11),(180,170,140,255))
        with self.assertRaises(ValueError):validate_details(self.p,self.ids,details)
    def test_semantics_and_material_intersections(self):self.assertTrue(validate(self.p,self.ids))
    def test_all_v7_bytes_immutable(self):
        for path,digest in load(HERE/'v7-immutable-sha256.json').items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest,path)
    def test_ground_canvas(self):
        with Image.open(HERE/'ground.png') as image:self.assertEqual(image.size,(4608,4608))
    def test_rendered_ground_matches_semantics(self):
        with Image.open(HERE/'ground.png') as image:self.assertGreater(validate_ground_pixels(self.p,image),14000)
    def test_mutation_rendered_ground_disagrees(self):
        with Image.open(HERE/'ground.png') as source:image=source.copy()
        image.putpixel((11,11),(0,0,0))
        with self.assertRaises(ValueError):validate_ground_pixels(self.p,image)
    def test_mutation_missing_neighbor(self):self.mutation(lambda p:p['buildings'].pop(5))
    def test_mutation_solid_change(self):self.mutation(lambda p:p['buildings'][0]['minWorld'].__setitem__(0,1))
    def test_mutation_camera_root(self):self.mutation(lambda p:p['protected']['cameraRoot'].__setitem__(0,497))
    def test_mutation_field(self):self.mutation(lambda p:p['protected'].__setitem__('cameraRange',0))
    def test_mutation_registration(self):self.mutation(lambda p:p['registration'].__setitem__('drawSizeWorld',[2304,1536]))
    def test_mutation_foundation_hole(self):self.mutation(lambda p:p['buildings'][2]['foundationWorld'].pop())
    def test_mutation_virtual_as_actual(self):self.mutation(lambda p:p['buildings'][2]['actualContactWorld'].__setitem__(0,[512,640]))
    def test_mutation_source_landmark(self):self.mutation(lambda p:p['buildings'][2]['contactLandmarks'][0]['sourcePixelsTopLeft'].__setitem__(0,500))
    def test_mutation_invented_neighbor_contact(self):self.mutation(lambda p:p['buildings'][5]['actualContactWorld'].append([1056,1088]))
    def test_mutation_tree_old_interior(self):self.mutation(lambda p:p['props'][1].__setitem__('worldRoot',[858,780]))
    def test_mutation_tree_on_road(self):self.mutation(lambda p:p['props'][1].__setitem__('worldRoot',[858,500]))
    def test_mutation_excess_shadow(self):self.mutation(lambda p:p['props'][1].__setitem__('shadowRadiusWorld',80))
    def test_mutation_zero_sidewalk(self):self.mutation(lambda p:p['buildings'][5].__setitem__('sidewalkOutsetWorld',0))
    def test_mutation_painted_road_inside_solid(self):
        ids=self.ids.copy();ids.putpixel((1100,3200),1)
        with self.assertRaises(ValueError):validate(self.p,ids)
if __name__=='__main__':unittest.main(verbosity=2)
