"""Controlled material transfer: laced source exclusively on forward tongue."""
from pathlib import Path
from types import SimpleNamespace
import sys,json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;S=R/'source';sys.path.insert(0,str(S))
geometry=(S/'boot_geometry.py').read_text().split("with (R/'recovery-leg.obj')")[0].replace("leg=json.loads((R/'authored-key.json').read_text());","leg=POSE;")
owned=(S/'orientation.py').read_text();prefix=owned.split("with (R/'recovery-leg-owned.obj')")[0].replace('import boot_geometry as b','')
renderer='def render('+owned.split('def render(',1)[1].split("plate=Image.new('RGB',(840,840))",1)[0]
renderer=renderer.replace('for face,col in zip(faces,colors):','for fi,(face,col) in enumerate(zip(faces,colors)):')
renderer=renderer.replace('rgb[sl][mask]=np.array(col)*light','''uv=np.array(face_uv[fi])[[0,j,j+1]]
   uvx=u*uv[0,0]+w*uv[1,0]+t*uv[2,0];uvy=u*uv[0,1]+w*uv[1,1]+t*uv[2,1]
   sx=np.clip(np.rint((uvx-tx)/source_scale).astype(int),0,texture.shape[1]-1)
   sy=np.clip(np.rint((uvy-ty)/source_scale).astype(int),0,texture.shape[0]-1)
   if face_zones[fi]=='rearPaint':
    sx=np.clip(np.rint((uvx-192)/(312/459)+462).astype(int),0,north_texture.shape[1]-1)
    sy=np.clip(np.rint((uvy-336)/(312/459)+971).astype(int),0,north_texture.shape[0]-1)
    sampled=north_texture[sy,sx,:3][mask].astype(float)
   else:sampled=texture[sy,sx,:3][mask].astype(float)
   if face_zones[fi] not in ['lacedTongue','trouser','vampFront','rearPaint']:
    sampled=material_base[face_zones[fi]]+(sampled-material_mean[face_zones[fi]])*.35
   zone=face_zones[fi]
   # Preserve surface ownership and stable UVs; reduce baked highlights rather than
   # adding screen-space noise that would crawl during playback.
   xxuv=uvx[mask]; yyuv=uvy[mask]
   if zone=='trouser':
    old=sampled.copy(); lum=old.mean(axis=1,keepdims=True)
    sampled=np.array([59.,58.,53.])+(old-np.array([65.,62.,56.]))*.68
    width=(xxuv-169)/11
    sampled+= (5*(1-np.clip(width*width,0,1)))[:,None]
    # Two restrained compression creases near cuff; no repeated full-shin bands.
    crease=np.exp(-((yyuv-304.5-.12*(xxuv-169))/0.65)**2)
    sampled-=crease[:,None]*7
   elif zone=='vampFront':
    sampled=np.array([91.,77.,58.])+(sampled-np.array([137.,112.,77.]))*.65
   elif zone=='plainLeather':
    sampled=np.array([81.,69.,53.])+(sampled-np.array([101.,80.,54.]))*.7
    sampled+= (2*np.sin(xxuv*.65)+1.2*np.sin(yyuv*.8))[:,None]
   elif zone=='rearPaint':
    sampled=np.array([78.,67.,52.])+(sampled-sampled.mean(axis=1,keepdims=True))*.35+(sampled.mean(axis=1,keepdims=True)-90)*.45
   elif zone=='lacedTongue':
    sampled=sampled*.82
   rgb[sl][mask]=np.clip(sampled*(.7+.3*light),0,255)''')
north_texture=np.array(Image.open(R/'four-facing-source.png').convert('RGBA'));tex=np.array(Image.open(R/'source.png').convert('RGBA'));reg=json.loads((R/'registration.json').read_text())
# Explicit source zones, in the retained registered 384px canvas.
zones={'lacedTongue':[160,321,178,346],'plainLeather':[162,353,175,361],'trouser':[158,289,180,307],'sole':[159,370,177,373],'vampFront':[155,335,184,374],'rearPaint':[204,282,233,338]}
def uvrect(rect,n):
 x0,y0,x1,y1=rect
 if n==4:return [(x0,y1),(x1,y1),(x1,y0),(x0,y0)]
 return [((x0+x1)/2+(x1-x0)*.45*np.cos(i*2*np.pi/n),(y0+y1)/2+(y1-y0)*.45*np.sin(i*2*np.pi/n)) for i in range(n)]
material_base={'plainLeather':np.array([101,80,54]),'trouser':np.array([65,62,56]),'sole':np.array([43,37,29])}
material_mean={}
for name,rect in zones.items():
 x0,y0,x1,y1=rect;tx,ty=reg['translation'];sc=reg['uniformScale']
 crop=tex[round((y0-ty)/sc):round((y1-ty)/sc),round((x0-tx)/sc):round((x1-tx)/sc),:3]
 material_mean[name]=np.mean(crop,axis=(0,1))
frames=[];records=[];(R/'frames').mkdir(exist_ok=True)
for i,sample in enumerate(json.loads((R/'samples.json').read_text())):
 combined=Image.new('RGBA',(384,416));enlarged=[]
 for pose in sample['legs']:
  g={'__file__':str(S/'boot_geometry.py'),'POSE':pose};exec(compile(geometry,'boot_geometry.py','exec'),g)
  ns={'__file__':str(S/'orientation.py'),'b':SimpleNamespace(**g)};exec(compile(prefix,'orientation.py','exec'),ns)
  faces=[];colors=[];uvs=[];owners=[]
  for idx,(face,color,group) in enumerate(zip(ns['faces'],ns['colors'],ns['groups'])):
   if 'laces' in group:continue # source tongue already contains laces; never double them
   zone='trouser' if group=='trouser' else 'plainLeather'
   if group=='boot_sole':zone='sole'
   if group=='tongue_shaft_front':zone='lacedTongue'
   if group in ['boot_upper','shaft']:
    points=np.array([ns['verts'][i] for i in face]);normal=np.cross(points[1]-points[0],points[2]-points[0]);normal/=np.linalg.norm(normal)
    angle=np.radians(pose['angle']);ny=normal[1]*np.cos(angle)-normal[2]*np.sin(angle);nz=normal[1]*np.sin(angle)+normal[2]*np.cos(angle)
    center=points.mean(axis=0)-np.array(pose['toe']);local_center_y=center[1]*np.cos(angle)-center[2]*np.sin(angle)
    if group=='boot_upper' and local_center_y>-3.5 and (nz>.4 or ny>.6):zone='vampFront'
    if ny<-.25:zone='rearPaint'
   faces.append(face);colors.append(color);owners.append(zone)
   if zone=='lacedTongue':uvs.append(uvrect(zones[zone],len(face)))
   else:
    # Shared vertex coordinates provide continuous mapping across adjacent faces.
    coords=[];angle=np.radians(pose['angle']);toe=np.array(pose['toe'])
    for vi in face:
     v=np.array(ns['verts'][vi])-toe
     local_y=v[1]*np.cos(angle)-v[2]*np.sin(angle)
     x0,y0,x1,y1=zones[zone]
     if zone=='rearPaint':
      local_z=v[1]*np.sin(angle)+v[2]*np.cos(angle)
      coords.append((np.clip(218-6*v[0],204,233),np.clip(307-3*local_y-6*np.sqrt(.75)*local_z,282,338)))
     elif zone=='vampFront':
      local_z=v[1]*np.sin(angle)+v[2]*np.cos(angle)
      coords.append((169+6*v[0],np.clip(374+3*local_y-6*np.sqrt(.75)*local_z,350,374)))
     elif zone=='trouser':
      rel=np.array(ns['verts'][vi])-np.array(pose['ankle']);dist=np.dot(rel,ns['axis'])
      coords.append((x0+np.clip((rel[0]+2.55)/5.1,0,1)*(x1-x0),y1-np.clip((dist-3.45)/(np.linalg.norm(np.array(pose['knee'])-np.array(pose['ankle']))-3.45),0,1)*(y1-y0)))
     else:coords.append((x0+np.clip((v[0]+2)/4,0,1)*(x1-x0),y0+np.clip((local_y+10)/10,0,1)*(y1-y0)))
    uvs.append(coords)
  ns.update(faces=faces,colors=colors,face_uv=uvs,face_zones=owners,north_texture=north_texture,material_base=material_base,material_mean=material_mean,texture=tex,source_scale=reg['uniformScale'],tx=reg['translation'][0],ty=reg['translation'][1])
  exec(compile(renderer,'material-render.py','exec'),ns)
  rendered=ns['render'](0,'',30,True);rendered.save(R/'frames'/f'{i:02d}-{pose["side"]}.png');np.save(R/'frames'/f'{i:02d}-{pose["side"]}-depth.npy',ns['last_depth']);combined.alpha_composite(rendered)
  if i==0:
   enlarged.extend([ns['render'](0,'FORWARD TONGUE MATERIAL'),ns['render'](180,'REAR: RETAINED NORTH BOOT PAINT')])
  assert owners.count('lacedTongue')==1
  records.append({'frame':i,'side':pose['side'],'lacedSourceFaces':1,'materialOwners':owners})
 combined.save(R/'frames'/f'{i:02d}-both.png')
 background=Image.new('RGB',(384,416),'#283036');background.paste(combined,(0,0),combined);frames.append(background)
 if i==0:
  plate=Image.new('RGB',(840,840))
  for n,p in enumerate(enlarged):plate.paste(p,(n%2*420,n//2*420))
  plate.save(R/'material-surfaces.png')
frames[0].save(R/'material-cycle.gif',save_all=True,append_images=frames[1:],duration=125,loop=0)
# Compare one assembled key without replacing any retained body pixel.
old=Image.open(R/'retained-body-contact.png').convert('RGBA');rear=Image.open(R/'frames'/'00-left.png').convert('RGBA');assembly=Image.alpha_composite(rear,old)
plate=Image.new('RGB',(768,448),'#283036');d=ImageDraw.Draw(plate)
for i,(im,label) in enumerate([(old,'Retained key'),(assembly,'Material candidate behind retained key')]):plate.paste(im,(i*384,32),im);d.text((i*384+12,12),label,fill='white')
plate.save(R/'assembled-key.png')
(R/'material-record.json').write_text(json.dumps({'status':'SOURCE_MATERIAL_CANDIDATE_NOT_FINAL_ART','sourceZonesRegisteredCanvas':zones,'sourceRegistration':reg,'records':records,'hiddenSurfaces':'Rear boot paint reused from retained north-facing source; placement onto the authored mesh remains proposed','limitations':['Faceted geometry','Authored normalized swatch material, not final paint','No full-character animated assembly','Source lighting is baked into retained forward boot paint']},indent=2)+'\n')
print('32 material renders exported; laced source restricted to one forward tongue face per boot.')
