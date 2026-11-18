"""Deterministic crop/translation/uniform-scale assembly. No image synthesis."""
from pathlib import Path
import hashlib, json, shutil
from PIL import Image, ImageDraw, __version__ as pillow_version
HERE = Path(__file__).resolve().parent
ORIGINAL = Path('/Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs')
GEN = Path('/Users/appliedalchemylabs/.jcode/generated-images')
SHEET = GEN / '1794798956933-ig_07cd661172aa2162016afa7548d1d087d0a302a894cfd91028.png'
SOUTH = ORIGINAL / 'SS-player-bounded-neutral/frames/00.png'
RIG = ORIGINAL / 'SS-player-bounded-proportions/source/body-rig.json'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
# Source regions are separated by alpha-zero gaps, never semantic masks.
# Anatomical right is screen-right in a back view.
# Active selection: attempt 01, uniform 0.4 (owner prefers baggy legs).
# Attempt 02 per-part slimming is immutable history in attempts/.
PARTS = [
 ('left_thigh',(560,710,720,950),(147,220),'left_hip',.4),
 ('right_thigh',(720,710,890,950),(195,220),'right_hip',.4),
 ('left_shin_boot',(940,735,1110,1010),(146,260),'left_knee',.4),
 ('right_shin_boot',(1130,735,1300,1010),(195,260),'right_knee',.4),
 ('left_coat_tail',(910,545,1100,730),(139,207),'left_hip',.4),
 ('right_coat_tail',(1110,545,1300,730),(193,207),'right_hip',.4),
 ('left_upper_arm',(930,90,1110,350),(112,100),'left_shoulder',.4),
 ('right_upper_arm',(1140,90,1310,350),(226,100),'right_shoulder',.4),
 ('torso_coat_equipment',(570,265,900,600),(135,101),'torso',.4),
 ('right_satchel',(1310,535,1510,760),(211,183),'right_hip',.4),
 ('left_forearm_hand',(940,350,1100,545),(110,164),'left_elbow',.4),
 ('right_forearm_hand',(1170,350,1310,545),(238,164),'right_elbow',.4),
 ('hood',(570,0,900,265),(145,39),'head',.4),
]
def build():
 for d in ('source','components','layers'): (HERE/d).mkdir(parents=True,exist_ok=True)
 for src,dest in [(SHEET,'source/revised-sheet.png'),(SHEET.with_suffix('.json'),'source/metadata.json'),(SOUTH,'source/south-neutral-unchanged.png'),(RIG,'source/original-body-rig.json')]: shutil.copyfile(src,HERE/dest)
 sheet=Image.open(SHEET).convert('RGBA')
 canvas=Image.new('RGBA',(384,416)); entries=[]
 for name,region,xy,bone,scale in PARTS:
  crop=sheet.crop(region); b=crop.getchannel('A').getbbox()
  assert b, (name,b)  # Preserve even isolated low-alpha pixels, no threshold cleanup.
  bounds=[b[0]+region[0],b[1]+region[1],b[2]+region[0],b[3]+region[1]]
  part=sheet.crop(bounds); part.save(HERE/'components'/f'{name}.png')
  size=tuple(round(v*scale) for v in part.size)
  scaled=part.resize(size,Image.Resampling.LANCZOS)
  layer=Image.new('RGBA',canvas.size); layer.paste(scaled,xy)
  layer.save(HERE/'layers'/f'{name}.png'); canvas=Image.alpha_composite(canvas,layer)
  entries.append(dict(name=name,bone=bone,region=list(region),alphaBounds=bounds,translation=list(xy),uniformScale=scale,activeAttempt='01-uniform-0.4',resampledSize=list(size),componentSHA256=sha(HERE/'components'/f'{name}.png'),layerSHA256=sha(HERE/'layers'/f'{name}.png')))
 canvas.save(HERE/'north-neutral.png')
 south=Image.open(SOUTH).convert('RGBA'); pair=Image.new('RGBA',(768,416)); pair.paste(south,(0,0)); pair.paste(canvas,(384,0)); pair.save(HERE/'south-north.png')
 manifest=dict(status='PROPOSED',kind='SAME_MASTER_EXTENSION_PROPOSAL_NOT_ADMISSION',contractIDs=['BP-002','BP-007','BP-008','BP-012','T1045'],canvas=[384,416],groundRoot=[192,336],logicalCanvas=[64,416/6],logicalRoot=[32,56],facing='north',anatomicalRight='screen-right',strap='painted left shoulder to anatomical right hip, retained from generated torso',master=dict(path=str(RIG),sha256=sha(RIG),bindingType='semantic extension only, not original paint or validated anatomical continuity'),provenance=dict(sheet=str(SHEET),sheetSHA256=sha(SHEET),metadataSHA256=sha(SHEET.with_suffix('.json')),south=str(SOUTH),southSHA256=sha(SOUTH),generator='native image_generation, see source/metadata.json',priorAttempt='1794798865937-ig_07cd661172aa2162016afa74e4f19087d089e00f6d009c0970.png, history only, not admitted',generatedHiddenSurfaces=True),tool=dict(name='Pillow',version=pillow_version),layerOrderBottomToTop=[e['name'] for e in entries],parts=entries,outputSHA256=sha(HERE/'north-neutral.png'),alphaBounds=list(canvas.getchannel('A').getbbox()),limits=['Neutral only. No joint-range, anatomical continuity, elevated-view fidelity, heel/toe or runtime acceptance.','Original rig pivots are south annotations, not copied into north as physical anatomy.','Shin and boot are combined generated parts. No separate boot control claimed.','All new back paint is generated, not recovered original master paint.'])
 (HERE/'north-extension.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'preview':str(HERE/'south-north.png'),'bounds':manifest['alphaBounds'],'parts':[(e['name'],e['alphaBounds'],e['resampledSize']) for e in entries]},indent=2))
if __name__=='__main__': build()
