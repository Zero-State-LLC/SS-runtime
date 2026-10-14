"""BP-007 source sampling audit. Run from repository root; no images modified."""
from pathlib import Path
from PIL import Image
import hashlib,json,math
root=Path('AppTests/BenchmarkAssets')
items={'player-south':(64,64),'player-north':(64,64),'player-east':(64,64),'player-west':(64,64),'camera-state-intact':(64,96),'camera-state-damaged':(64,96),'camera-state-critical':(64,96),'camera-state-destroyed':(64,96),'building-constrained':(1254*128*math.sqrt(2)/934,)*2,'newsbox':(20,40),'tree':(50,85)}
rows=[]
for name,draw in items.items():
 path=root/(name+'.png'); im=Image.open(path).convert('RGBA'); box=im.getchannel('A').getbbox()
 row={'asset':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_pixels':list(im.size),'alpha_bounds':box,'draw_points':draw,'views':[]}
 for zoom in [1,math.sqrt(2)]:
  out=[v*3*zoom for v in draw]; ratios=[im.size[i]/out[i] for i in range(2)]
  occupied=[(box[i+2]-box[i])*out[i]/im.size[i] for i in range(2)]
  row['views'].append({'zoom':zoom,'canvas_output_pixels':out,'occupied_output_pixels':occupied,'source_pixels_per_output_pixel':ratios,'occupied_height_fraction':occupied[1]/978,'magnified':min(ratios)<1})
 rows.append(row)
print(json.dumps({'runtime_base':'14abe4a','spec_pin':'00ce027209e6c233bcdd35295f35f0b9bfb9bbe5','output_pixels':[2112,978],'filter':'linear','scope':'test-only upright assets; excludes paving and intermediate targets; alpha bounds are not anatomy or collision','assets':rows},indent=2))
