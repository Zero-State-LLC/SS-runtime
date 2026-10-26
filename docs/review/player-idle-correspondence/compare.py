from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
R=Path(__file__).resolve().parent; O=R.parent
neutral_path=O/'SS-painted-character-source/south.png'
move_paths=[O/'SS-player-material-detail/frames'/f'{i:02}.png' for i in [0,4,8,12]]
neutral=Image.new('RGBA',(384,416)); neutral.alpha_composite(Image.open(neutral_path).convert('RGBA'),(0,0))
images=[neutral]+[Image.open(p).convert('RGBA') for p in move_paths]
sheet=Image.new('RGB',(384*5,480),'#283036');d=ImageDraw.Draw(sheet)
for i,(label,im) in enumerate(zip(['Painted neutral','Movement 01','Movement 05','Movement 09','Movement 13'],images)):
 x=i*384;sheet.paste(im,(x,40),im);d.text((x+12,12),label,fill='white')
 d.line((x,376,x+383,376),fill='#d99848',width=1)
 d.line((x+192,360,x+192,392),fill='#d99848',width=1)
 d.text((x+12,460),'Root (192,336); no rescaling',fill='white')
sheet.save(R/'registered-comparison.png')
# Alternation is a diagnostic of source discontinuity, not a proposed transition.
frames=[]
for im in [images[0],images[1]]:
 bg=Image.new('RGB',(384,416),'#283036');bg.paste(im,(0,0),im);frames.append(bg)
frames[0].save(R/'source-switch-diagnostic.gif',save_all=True,append_images=frames[1:],duration=750,loop=0)
record={'status':'REUSE_REJECTED_PENDING_SOURCE_RECONCILIATION','canvas':[384,416],'root':[192,336],'neutralPadding':'32 transparent pixels below existing 384-square source; no translation/resampling','sources':[{'path':str(p.relative_to(O)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [neutral_path]+move_paths],'limits':['Shared root does not prove compatible anatomy or sole contact.','Movement phases are not neutral poses.','Alternation is not an animation proposal.','Existing root was manually approximate, not measured ground contact.']}
(R/'comparison.json').write_text(json.dumps(record,indent=2)+'\n')
