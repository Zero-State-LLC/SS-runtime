#!/usr/bin/env python3
"""Copy the exact small source-test fixtures, never modify recovered inputs."""
import argparse
from pathlib import Path
import shutil

from build_source import NAMES, require, save, sha


def copy_fixtures(source, destination):
    require(not destination.exists(), "Fixture destination exists")
    require(not destination.resolve().is_relative_to(source.resolve()), "Fixtures must not overlap original inputs")
    paths = [f"{NAMES[0]}/source/samples.json", f"{NAMES[0]}/assemble.py",
             f"{NAMES[1]}/source/samples.json"]
    paths += [f"{NAMES[2]}/phase-{p:02d}/source/samples.json" for p in (5,13)]
    hashes = {relative: sha(source/relative) for relative in paths}
    for relative in paths:
        target=destination/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source/relative,target)
        require(sha(target)==hashes[relative],f"Fixture copy changed: {relative}")
        require(sha(source/relative)==hashes[relative],f"Original changed: {relative}")
    save(destination/"provenance.json",{"status":"EXACT_SOURCE_TEST_SUBSET_NOT_RENDER_MASTER", "files":hashes,
         "authority":"Recovered current bounded authoring workspace. Runtime recipe docs/review/player-settle-prototype/build_source.py:6-52.",
         "limits":["Only geometry/contact/order/timing/source-preservation tests are portable from this subset", "Full render and original-input inventory audit still require the complete read-only source root"]})


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    copy_fixtures(args.source_root,args.output)
