#!/usr/bin/env python3
"""Read-only artifact audit: geometry facts, hashes and independent video PTS.

This is source review, not live presentation acceptance. Numerical constraints
are inherited from the prototype. Knee flexion/step and landing drop are facts,
not newly invented aesthetic thresholds.
"""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import shutil
import subprocess

import build_source as b
from export_review import load_verified, timeline


def audit(root, source_root, ffprobe):
    manifest = load_verified(root)
    before = json.loads((root/"input-inventory.json").read_text())
    b.require(b.inventory(source_root) == before,"Original inputs changed")
    sources = json.loads((source_root/b.NAMES[0]/"source/samples.json").read_text())
    neutral = json.loads((source_root/b.NAMES[1]/"source/samples.json").read_text())[0]
    facts=[]
    for p in manifest["phases"]:
        phase=p["phase"]
        samples=json.loads((root/p["samplesPath"]).read_text())
        checked=b.validate(samples,sources[phase-1],neutral,phase)
        b.endpoint_checks(root/f"phase-{phase:02d}/frames",source_root/b.NAMES[0]/f"frames/{phase-1:02d}.png",source_root/b.NAMES[1]/"frames/00.png",phase)
        if phase in b.PRESERVED:
            original=source_root/b.NAMES[2]/f"phase-{phase:02d}"
            b.require((root/p["samplesPath"]).read_bytes()==(original/"source/samples.json").read_bytes(),f"phase{phase}: original samples changed")
            for frame in p["frames"]:
                b.require((root/frame["path"]).read_bytes()==(original/f'frames/{frame["pose"]:02d}.png').read_bytes(),f"phase{phase}: original frame changed")
        angles=[]
        for pose in samples:
            for q in pose["legs"]:
                a=[x-y for x,y in zip(q["hip"],q["knee"])];c=[x-y for x,y in zip(q["ankle"],q["knee"])]
                dot=sum(x*y for x,y in zip(a,c))/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(x*x for x in c)))
                angles.append(math.degrees(math.acos(max(-1,min(1,dot)))))
        measures=checked["measurements"]
        facts.append({"phase":phase,"status":p["status"],"supportSide":checked["supportSide"],
             "contactIntervals":checked["contactIntervals"],"maxUpperLengthError":max(abs(q["upperLength"]-12.5) for q in measures),
             "maxLowerLengthError":max(abs(q["lowerLength"]-14.5) for q in measures),
             "minReach":min(q["reach"] for q in measures),"maxReach":max(q["reach"] for q in measures),
             "minToeHeight":min(q["toeHeight"] for q in measures),"minHeelHeight":min(q["heelHeight"] for q in measures),
             "maxKneeMinusHipHeight":max(q["kneeMinusHipHeight"] for q in measures),
             "kneeInteriorAngleDegreesRange":[min(angles),max(angles)],
             "maxAdjacentKneeStep":max(math.dist(b.legs(samples[k])[s]["knee"],b.legs(samples[k-1])[s]["knee"]) for s in ("left","right") for k in range(1,17)),
             "supportEntryToeDrop":b.legs(samples[0])[checked["supportSide"]]["toe"][2]-b.legs(samples[1])[checked["supportSide"]]["toe"][2],
             "uniqueRGBAPoses":len({f["rgbaSHA256"] for f in p["frames"]}),"exactEntryNeutralPixels":True})
    videos=[]
    for speed,fps in (("normal",128),("quarter",32)):
        path=root/f"{speed}-speed.mp4"
        raw=subprocess.check_output([ffprobe,"-v","error","-select_streams","v:0","-show_entries","stream=nb_frames,r_frame_rate,duration,width,height,time_base:frame=best_effort_timestamp","-of","json",str(path)],text=True)
        info=json.loads(raw);stream=info["streams"][0];frames=info["frames"]
        b.require(int(stream["nb_frames"])==len(timeline())==len(frames),f"{speed}: encoded frame count")
        b.require(Fraction(stream["r_frame_rate"])==fps,f"{speed}: encoded frame rate")
        time_base=Fraction(stream["time_base"])
        exact_pts=[Fraction(f["best_effort_timestamp"])*time_base==Fraction(k,fps) for k,f in enumerate(frames)]
        b.require(all(exact_pts),f"{speed}: encoded presentation timestamps")
        b.require((stream["width"],stream["height"])==(768,928),f"{speed}: encoded dimensions")
        videos.append({"speed":speed,"fileSHA256":b.sha(path),"frames":len(frames),"fps":fps,"exactPTSCount":len(exact_pts),"timeBase":str(time_base),"neutralAfterReleaseSeconds":48/fps})
    result={"status":"CHECKS_PASS_REMAINS_PROPOSED", "inputFilesUnchanged":len(before),"phases":facts,"encodedSourceVideos":videos,
            "newFrames":14*17,"preservedFrames":2*17,"exactEndpointComparisons":32,
            "nativePlaybackOrLiveCadenceVerified":False,"fullSoleContactVerified":False,
            "continuouslyInterpolatedGeometryVerified":False,"browserVisualReview":"coordinator-owned, pending"}
    b.save(root/"audit.json",result)
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts",required=True,type=Path)
    parser.add_argument("--source-root",required=True,type=Path)
    parser.add_argument("--ffprobe",default=shutil.which("ffprobe"))
    args=parser.parse_args()
    b.require(args.ffprobe is not None,"Local ffprobe required")
    result=audit(args.artifacts,args.source_root,args.ffprobe)
    print(json.dumps({"status":result["status"],"inputFilesUnchanged":result["inputFilesUnchanged"],"newFrames":238,"preservedFrames":34,"endpointComparisons":32}))
