#!/usr/bin/env python3
"""Portable artifact checks. Requires only Python + Pillow, never original masters.

An optional native-assets path is strictly verified when supplied, never skipped.
Archived input hashes establish provenance, not fresh access to original inputs.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re

from PIL import Image

PHASES = list(range(1,17))
PRESERVED = [5,13]
NEW = [p for p in PHASES if p not in PRESERVED]
DECISION = "167171d89f9dfdad550e1b3b95510fc84514d0b1"
TIMING = {"unitsPerSecond":128,"frameUnits":[3]*17,"neutralBoundaryUnits":48,
          "neutralBoundarySeconds":0.375,"totalUnitsIncludingNeutralHold":51}


def need(condition,message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def pixels(path):
    with Image.open(path) as image:
        need(image.size==(384,416),f"Wrong PNG dimensions: {path}")
        return image.convert("RGBA").tobytes()


def verify(artifacts, fixtures, native_assets=None):
    manifest=read_json(artifacts/"manifest.json")
    inventory=read_json(artifacts/"input-inventory.json")
    provenance=read_json(fixtures/"provenance.json")
    need(manifest["status"]=="PROPOSED_SOURCE_ONLY_NOT_LIVE_CADENCE","Source review status changed")
    need(manifest["projectionDecision"]==DECISION,"Projection provenance changed")
    need(manifest["timing"]==TIMING,"Exact timing changed")
    need(Fraction(sum(manifest["timing"]["frameUnits"][:16]),128)==Fraction(3,8),"Neutral boundary changed")
    need(manifest["newPhases"]==NEW and manifest["preservedPhases"]==PRESERVED,"Family provenance changed")
    need(manifest["inputsUnchanged"] is True,"Original input verification absent")
    need(len(inventory)==manifest["inputFileCount"]==1012,"Input inventory count changed")
    for path,digest in inventory.items():
        need(not Path(path).is_absolute() and ".." not in Path(path).parts,"Unsafe inventory path")
        need(re.fullmatch(r"[0-9a-f]{64}",digest) is not None,"Invalid inventory SHA256")
    expected_fixture_paths={"SS-player-bounded-proportions/source/samples.json","SS-player-bounded-proportions/assemble.py",
        "SS-player-bounded-neutral/source/samples.json",*[f"SS-player-settle-prototype/phase-{p:02d}/source/samples.json" for p in PRESERVED]}
    need(set(provenance["files"])==expected_fixture_paths,"Fixture provenance set changed")
    need(provenance["status"]=="EXACT_SOURCE_TEST_SUBSET_NOT_RENDER_MASTER","Fixture provenance status changed")
    for path,digest in provenance["files"].items():
        need(sha(fixtures/path)==digest==inventory[path],f"Fixture/input provenance mismatch: {path}")
    source=read_json(fixtures/"SS-player-bounded-proportions/source/samples.json")
    need(len(source)==16,"Source phase count changed")
    need([p["phase"] for p in manifest["phases"]]==PHASES,"Phase order/count changed")
    expected_files={f"phase-{p:02d}/frames/{k:02d}.png" for p in PHASES for k in range(17)}
    actual_files={str(p.relative_to(artifacts)) for p in artifacts.glob("phase-*/frames/*.png")}
    need(actual_files==expected_files,"Artifact PNG set is not exactly272 ordered-family files")
    all_pixels={}
    for p in manifest["phases"]:
        phase=p["phase"]
        need(p["status"]==("PRESERVED" if phase in PRESERVED else "PROPOSED"),f"Phase {phase} acceptance status changed")
        expected_samples=f"phase-{phase:02d}/samples.json"
        need(p["samplesPath"]==expected_samples,"Noncanonical samples path")
        need(sha(artifacts/expected_samples)==p["samplesSHA256"],f"Phase {phase} sample hash changed")
        samples=read_json(artifacts/expected_samples)
        need(len(samples)==17 and [s["settleProgress"] for s in samples]==[k/16 for k in range(17)],"Source pose order changed")
        need(samples[0]["legs"]==source[phase-1]["legs"],"Source entry provenance changed")
        need([f["pose"] for f in p["frames"]]==list(range(17)),"Frame order/count changed")
        need([e["pose"] for e in p["endpoints"]]==[0,16],"Endpoint order changed")
        digests=[]
        for f in p["frames"]:
            k=f["pose"];expected=f"phase-{phase:02d}/frames/{k:02d}.png"
            need(f["path"]==expected,"Noncanonical frame path")
            path=artifacts/expected
            need(sha(path)==f["fileSHA256"],f"Frame byte hash changed: {expected}")
            data=pixels(path);digest=hashlib.sha256(data).hexdigest()
            need(digest==f["rgbaSHA256"],f"RGBA hash changed: {expected}")
            if k in (0,16):
                all_pixels[(phase,k)]=data
            digests.append(digest)
            if phase in PRESERVED:
                original=f"SS-player-settle-prototype/phase-{phase:02d}/frames/{k:02d}.png"
                need(f["fileSHA256"]==inventory[original],"Preserved frame provenance changed")
        need(len(set(digests))==17,"Expected17 distinct RGBA poses")
        for e in p["endpoints"]:
            k=e["pose"]
            need(e["exactRGBA"] is True and e["rgbaSHA256"]==digests[k],"Endpoint pixel record changed")
            original=(f"SS-player-bounded-proportions/frames/{phase-1:02d}.png" if k==0 else "SS-player-bounded-neutral/frames/00.png")
            need(p["frames"][k]["fileSHA256"]==inventory[original],"Endpoint original-file provenance changed")
        if phase in PRESERVED:
            need(p["samplesSHA256"]==inventory[f"SS-player-settle-prototype/phase-{phase:02d}/source/samples.json"],"Preserved sample provenance changed")
    need(len({all_pixels[(p,16)] for p in PHASES})==1,"Neutral pixels diverge")
    result={"status":"PASS_REMAINS_PROPOSED","orderedFrames":272,"sourceSamples":272,"endpointProvenanceChecks":32,
            "archivedInputHashRecords":1012,"fixtureHashes":5,"preservedFrameHashes":34,
            "neutralBoundarySeconds":0.375,"originalMastersReopened":False,"nativeAssets":None}
    if native_assets is not None:
        need(native_assets.is_dir(),"Native assets directory missing")
        expected={f"player-allrelease-{p:02d}-{k:02d}.png" for p in NEW for k in range(1,16)}
        actual={p.name for p in native_assets.glob("player-allrelease-*.png")}
        need(actual==expected,"Native intermediates must be exactly210 expected files")
        for phase in NEW:
            for k in range(1,16):
                path=native_assets/f"player-allrelease-{phase:02d}-{k:02d}.png"
                need(sha(path)==manifest["phases"][phase-1]["frames"][k]["fileSHA256"],f"Native intermediate byte mismatch: {path.name}")
            for k,name in ((0,f"player-source-s-{phase-1:02d}.png"),(16,"player-source-s-neutral.png")):
                need(pixels(native_assets/name)==all_pixels[(phase,k)],f"Native endpoint RGBA mismatch: phase{phase} pose{k}")
        result["nativeAssets"]={"exactIntermediateFiles":210,"exactEndpointRGBAComparisons":28,"phases":NEW}
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts",type=Path,default=Path(__file__).resolve().parent/"artifacts")
    parser.add_argument("--fixtures",type=Path,default=Path(__file__).resolve().parent/"fixtures")
    parser.add_argument("--native-assets",type=Path)
    args=parser.parse_args()
    print(json.dumps(verify(args.artifacts,args.fixtures,args.native_assets),indent=2))
