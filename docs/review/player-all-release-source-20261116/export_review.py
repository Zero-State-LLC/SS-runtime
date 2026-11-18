#!/usr/bin/env python3
"""Publish source-only normal/quarter review after every generation guard passed."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
from build_source import TIMING, require, rgba, save, sha


def load_verified(root):
    manifest = json.loads((root/"manifest.json").read_text())
    require(manifest["timing"] == TIMING and manifest["inputsUnchanged"], "Unverified timing/input state")
    require([p["phase"] for p in manifest["phases"]] == list(range(1,17)), "Incomplete/reordered phases")
    for phase in manifest["phases"]:
        require(sha(root/phase["samplesPath"]) == phase["samplesSHA256"], "Source samples changed")
        require([f["pose"] for f in phase["frames"]] == list(range(17)), "Incomplete/reordered poses")
        for frame in phase["frames"]:
            path = root/frame["path"]
            require(sha(path) == frame["fileSHA256"], f"Frame bytes changed: {path}")
            require(hashlib.sha256(rgba(path)).hexdigest() == frame["rgbaSHA256"], f"Frame pixels changed: {path}")
    return manifest


def timeline():
    # Source comparison scaffold: .25s entry hold, then exact authored sequence,
    # then .5s neutral hold. This is not a simulated or captured gameplay clock.
    return [("entry hold",0)]*32 + [("settle",k) for k in range(17) for _ in range(3)] + [("neutral hold",16)]*64


def export(root, ffmpeg):
    manifest = load_verified(root)
    images = {p["phase"]:[Image.open(root/f["path"]).convert("RGBA") for f in p["frames"]] for p in manifest["phases"]}
    for p in manifest["phases"]:
        phase = p["phase"]
        samples = json.loads((root/p["samplesPath"]).read_text())
        keys = [0,1,8,9,15,16]
        plate = Image.new("RGB",(384*len(keys),464),"#283036")
        draw = ImageDraw.Draw(plate)
        for col,k in enumerate(keys):
            x=col*384
            plate.paste(images[phase][k],(x,48),images[phase][k])
            contacts = ",".join(q["side"] for q in samples[k]["legs"] if q["contact"]) or "none"
            draw.text((x+8,6),f"Phase {phase:02d} pose {k:02d} | {p['status']}",fill="white")
            draw.text((x+8,23),f"t={k*3}/128s | toe contact: {contacts}",fill="white")
        plate.save(root/f"phase-{phase:02d}/contact-plate.png")
    boards={}
    for stage,k in dict.fromkeys(timeline()):
        image=Image.new("RGB",(768,928),"#283036")
        draw=ImageDraw.Draw(image)
        for p in manifest["phases"]:
            phase=p["phase"];x=(phase-1)%4*192;y=(phase-1)//4*232
            sprite=images[phase][k].resize((192,208),Image.Resampling.LANCZOS)
            image.paste(sprite,(x,y+24),sprite)
            draw.text((x+4,y+2),f"{phase:02d} {p['status']} | {k:02d}",fill="white")
            draw.text((x+4,y+13),stage,fill="white")
        boards[(stage,k)]=image.tobytes()
    videos=[]
    for name,fps in (("normal",128),("quarter",32)):
        path=root/f"{name}-speed.mp4"
        command=[ffmpeg,"-y","-v","error","-f","rawvideo","-pixel_format","rgb24","-video_size","768x928","-framerate",str(fps),"-i","pipe:0","-an","-c:v","libx264","-crf","18","-pix_fmt","yuv420p",str(path)]
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            for item in timeline():
                process.stdin.write(boards[item])
            process.stdin.close()
            error=process.stderr.read().decode()
            require(process.wait()==0,f"{name} encode failed: {error}")
        finally:
            if process.poll() is None:
                process.kill();process.wait()
        videos.append({"path":path.name,"sha256":sha(path),"frameCount":len(timeline()),"fps":fps,"durationSeconds":len(timeline())/fps,"neutralBoundaryAfterReleaseSeconds":48/fps})
        cards=[]
        for p in manifest["phases"]:
            phase=p["phase"]
            cards.append(f'<section><h2>Phase {phase:02d} <small>{p["status"]}</small></h2><img data-phase="{phase}" width="384" height="416" src="phase-{phase:02d}/frames/00.png" alt="Phase {phase:02d} source pose"><p><a href="phase-{phase:02d}/contact-plate.png">Contact plate</a> | <a href="phase-{phase:02d}/samples.json">Source poses</a></p></section>')
        html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Player all-release source review</title>
<style>body{background:#20272c;color:#eee;font:16px system-ui;margin:24px}a{color:#bed9ee}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(384px,1fr));gap:16px}section{background:#283036;padding:12px}h2{font-size:18px}small{font-size:12px}img{display:block}button,input{font:inherit}nav{position:sticky;top:0;background:#20272c;padding:12px}video{max-width:100%;height:560px}</style>
<h1>Player south releases: SPEED speed</h1><p>PROPOSED source-only stationary-root review. Original phases 05/13 preserved. No native playback, live-cadence claim or visual acceptance.</p><p>Exact source timing: 17 poses, 3/128s each at normal speed. Neutral begins 0.375s after release, or 1.5s at quarter speed. Entry/neutral review holds and loop reset are not gameplay.</p><p><a href="normal-speed.html">Normal</a> | <a href="quarter-speed.html">Separate quarter speed</a> | <a href="manifest.json">Verified manifest</a> | <a href="geometry-contact-checks.json">Geometry/contact facts</a></p>
<details><summary>Encoded all-phase comparison</summary><video controls loop muted src="SPEED-speed.mp4"></video></details>
<nav><button id="toggle" disabled>Pause</button> <label>Pose <input id="pose" type="range" min="0" max="16" value="0" disabled></label> <output id="status">Loading all verified frames...</output></nav><main>CARDS</main>
<script>
const fps=FPS, schedule=SCHEDULE, nodes=[...document.querySelectorAll('[data-phase]')], status=document.getElementById('status'), slider=document.getElementById('pose'), toggle=document.getElementById('toggle');
let playing=true, start=null, current=-1;
const frames=nodes.map(node=>Array.from({length:17},(_,k)=>{const im=new Image();im.src=`phase-${String(node.dataset.phase).padStart(2,'0')}/frames/${String(k).padStart(2,'0')}.png`;return im}));
function show(k,label){if(k!==current){nodes.forEach((node,i)=>node.src=frames[i][k].src);current=k;slider.value=k}status.textContent=`${label} | pose ${k}/16 | source only`;}
toggle.onclick=()=>{playing=!playing;toggle.textContent=playing?'Pause':'Play';start=null};
slider.oninput=()=>{playing=false;toggle.textContent='Play';show(Number(slider.value),'manual contact inspection')};
function tick(now){if(playing){if(start===null)start=now;const item=schedule[Math.floor((now-start)*fps/1000)%schedule.length];show(item[1],item[0])}requestAnimationFrame(tick)}
function imageReady(im){return new Promise((resolve,reject)=>{function finish(){im.onload=null;im.onerror=null;if(im.naturalWidth===384&&im.naturalHeight===416)resolve();else reject(new Error('Invalid source image dimensions: '+im.src))}im.onload=finish;im.onerror=()=>{im.onload=null;im.onerror=null;reject(new Error('Source image failed: '+im.src))};if(im.complete)finish()})}
document.documentElement.dataset.reviewReady='loading';
Promise.all(frames.flat().map(imageReady)).then(()=>{show(0,'Ready: manual inspection available');toggle.disabled=false;slider.disabled=false;document.documentElement.dataset.reviewReady='true';requestAnimationFrame(tick)}).catch(error=>{document.documentElement.dataset.reviewReady='error';status.textContent='Failed to load source frames: '+error});
</script></html>'''
        html=html.replace("SPEED",name).replace("FPS",str(fps)).replace("SCHEDULE",json.dumps(timeline())).replace("CARDS","".join(cards))
        (root/f"{name}-speed.html").write_text(html)
    save(root/"review-export.json",{"status":"SOURCE_REVIEW_ONLY", "videos":videos,"contactPlates":16,"rgbaFrames":272,
         "timeline":timeline(),"rendering":"384x416 originals in browser; half-size tiles in encoded all-phase grid", "nativePlaybackClaim":False})


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts",required=True,type=Path)
    parser.add_argument("--ffmpeg",default=shutil.which("ffmpeg"))
    args=parser.parse_args()
    require(args.ffmpeg is not None,"Local ffmpeg required")
    export(args.artifacts.resolve(),args.ffmpeg)
