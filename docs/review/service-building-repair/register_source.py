"""Review-only source re-authoring. Keeps runtime collision and assets untouched."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,math
P=Path(__file__).resolve().parent
source=P/'service-building-v2.png'
im=Image.open(source).convert('RGBA')
a=im.getchannel('A');a=a.point(lambda v:0 if v<16 else v);im.putalpha(a)
f=(580.,1066.); endpoints={'left':(214.,831.),'right':(1016.,835.)}
guide=json.loads((P/'guide.json').read_text()); target=guide['basePixelsTopLeft']; t=target['SW']; vertical=.8
regions={}; images={}
for name,key in [('left','NW'),('right','SE')]:
    e=endpoints[name];q=target[key]
    sx=(q[0]-t[0])/(e[0]-f[0]); shear=(q[1]-t[1]-vertical*(e[1]-f[1]))/(e[0]-f[0])
    inverse=(1/sx,0,f[0]-t[0]/sx,-shear/(sx*vertical),1/vertical,f[1]-t[1]/vertical+shear*t[0]/(sx*vertical))
    transformed=im.convert('RGBa').transform((1024,1024),Image.Transform.AFFINE,inverse,Image.Resampling.BICUBIC).convert('RGBA')
    images[name]=transformed
    def forward(p): return (t[0]+sx*(p[0]-f[0]),t[1]+vertical*(p[1]-f[1])+shear*(p[0]-f[0]))
    errors=[math.dist(forward(p),q) for p,q in [(f,t),(e,target[key])]]
    assert max(errors)<1e-9
    # Shared seam and vertical-preservation assertions independent of endpoint fits.
    assert abs(forward((f[0],f[1]-100))[0]-t[0])<1e-9
    regions[name]={'scaleX':sx,'scaleY':vertical,'shearYFromX':shear,'inverseAffine':inverse,'landmarkErrorsPixels':errors}
result=Image.new('RGBA',(1024,1024)); split=round(t[0]);result.paste(images['left'].crop((0,0,split,1024)),(0,0));result.paste(images['right'].crop((split,0,1024,1024)),(split,0))
out=P/'service-building-v3-registered.png';result.save(out)
record={'status':'SOURCE_REAUTHORING_CANDIDATE_NOT_ADMITTED','sourceHash':hashlib.sha256(source.read_bytes()).hexdigest(),'deliveryHash':hashlib.sha256(out.read_bytes()).hexdigest(),'canvas':[1024,1024],'sourceFront':f,'sourceEndpoints':endpoints,'outputBase':target,'alphaNoiseThreshold':16,'sourcePixelsPerWorldUnit':2,'drawSizeLogical':[512,512],'frontAnchorNormalizedSpriteKit':[t[0]/1024,1-t[1]/1024],'worldAnchor':'solid-07-service-yard-b SW corner (1408,1248), projected by shared transform','regions':regions,'limitations':['Hand-marked base points remain review observations','Piecewise correction may alter roof/equipment; inspect before adoption','No source rear-base pixels reconstructed','No runtime integration or traversal evidence yet']}
(P/'registration-v3.json').write_text(json.dumps(record,indent=2)+'\n')
bg=Image.new('RGBA',result.size,'#20242a');bg.alpha_composite(result);d=ImageDraw.Draw(bg);d.line([tuple(target[k]) for k in ['NW','SW','SE']],fill='#00ffff',width=2);bg.convert('RGB').save(P/'registered-base-overlay.jpg')
print(json.dumps({'output':str(out),'regions':regions,'anchor':record['frontAnchorNormalizedSpriteKit']},indent=2))
