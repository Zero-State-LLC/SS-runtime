from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
new=Path(__file__).resolve().parent;base=new.parent/'SS-player-low-recovery';rows=[]
(new/'video-frames').mkdir(exist_ok=True)
for path in ['source/samples.json','boot/samples.json','source/body-rig.json','assemble.py','thigh.py','boot/source/boot_geometry.py','boot/source/orientation.py']:
 assert (base/path).read_bytes()==(new/path).read_bytes(),path
for i in range(16):
 a=np.array(Image.open(base/'frames'/f'{i:02d}.png').convert('RGBA'));b=np.array(Image.open(new/'frames'/f'{i:02d}.png').convert('RGBA'))
 assert np.array_equal(a[:,:,3],b[:,:,3]),f'alpha changed {i}'
 mask=np.zeros(a.shape[:2],dtype=bool)
 for side in ['left','right']:mask|=np.array(Image.open(base/'boot/frames'/f'{i:02d}-{side}.png'))[:,:,3]>0
 changed=np.any(a!=b,axis=2)
 assert not np.any(changed & ~mask),f'non-material part changed {i}'
 yy,xx=np.where(changed);rows.append({'frame':i,'changedPixels':len(xx),'changedBounds':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'sha256':hashlib.sha256((new/'frames'/f'{i:02d}.png').read_bytes()).hexdigest()})
 im=Image.fromarray(b);bg=Image.new('RGBA',im.size,'#283036');bg.alpha_composite(im);bg.convert('RGB').save(new/'video-frames'/f'{i:02d}.png')
report={'status':'PROPOSED_MATERIAL_ONLY_NOT_ADMITTED','baseline':'SS-player-low-recovery','geometryMotionAndUVsUnchanged':True,'allAlphaMasksIdentical':True,'changesWithinOriginalCalfBootMasksOnly':True,'changes':{'calfSourceContrast':[.38,.68],'vampSourceContrast':[.38,.65],'plainMaterialSourceContrast':[.18,.35]},'frames':rows,'limits':['Source preview, not renderer capture','No gait/contact improvement claimed','Not final material acceptance']}
(new/'material-only-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('16/16 identical alpha; changed pixels remain inside original calf/boot masks; pose/rig/geometry/assembly unchanged')
