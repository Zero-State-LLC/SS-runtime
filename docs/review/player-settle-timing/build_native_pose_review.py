"""Build a static native-pose review from xcresult-exported attachments."""
from pathlib import Path
import json, re, shutil, sys
source, target = map(Path, sys.argv[1:3])
manifest = json.loads((source / "manifest.json").read_text())
images = {}
for case in manifest:
    for attachment in case["attachments"]:
        match = re.search(r"midpoint-native-stop-(\d+)-pose-(\d+)", attachment.get("suggestedHumanReadableName", ""))
        if match:
            key = tuple(map(int, match.groups()))
            assert key not in images, key
            images[key] = source / attachment["exportedFileName"]
assert set(images) == {(phase, pose) for phase in (5, 13) for pose in range(17)}, "Incomplete native pose capture"
target.mkdir(parents=True, exist_ok=True)
for (phase, pose), path in images.items():
    shutil.copy2(path, target / f"stop-{phase:02d}-pose-{pose:02d}.png")
html = """<!doctype html><meta charset="utf-8"><title>Native settling poses</title>
<style>body{font:18px system-ui;background:#202326;color:#eee;margin:32px}button,input{font:inherit}section{display:flex;gap:32px;flex-wrap:wrap}img{width:384px;max-width:100%;background:#333}figure{margin:20px 0}small{display:block;max-width:850px;line-height:1.5}</style>
<h1>Native settling poses</h1><p>Static SpriteKit frame-step inspection · both stopping poses · 17 poses each</p>
<small>This diagnostic holds every pose for inspection. It does not demonstrate normal-speed delivery, shared-scene projection or moving ground contact. Images below are enlarged 2× from a 192×144-point crop. Review cadence in the separate normal-speed clips.</small>
<p><button id="previous">Previous</button> <input id="pose" aria-label="Pose" type="range" min="0" max="16" value="0"> <button id="next">Next</button> <output id="label"></output></p>
<section><figure><figcaption>Stopping pose 5</figcaption><img id="a" alt="Native pose from stop 5"></figure><figure><figcaption>Stopping pose 13</figcaption><img id="b" alt="Native pose from stop 13"></figure></section>
<script>const slider=document.querySelector('#pose');function show(){const p=Number(slider.value);document.querySelector('#label').textContent=`Pose ${p+1} / 17`;document.querySelector('#a').src=`stop-05-pose-${String(p).padStart(2,'0')}.png`;document.querySelector('#b').src=`stop-13-pose-${String(p).padStart(2,'0')}.png`;}slider.oninput=show;document.querySelector('#previous').onclick=()=>{slider.value=Math.max(0,Number(slider.value)-1);show()};document.querySelector('#next').onclick=()=>{slider.value=Math.min(16,Number(slider.value)+1);show()};show();</script>"""
(target / "index.html").write_text(html)
print(f"Exported {len(images)} native pose images to {target}")
