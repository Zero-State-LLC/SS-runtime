#!/usr/bin/env python3
"""Compare actual v7 baseline pixels with immutable v6 candidate, without rewriting either."""
import json
from pathlib import Path
from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
V6 = HERE.parent / 'scene-qa-framing-20261116/native-capture-v6'
V7 = HERE / 'scene/native-capture-v7'


def verify():
    comparisons = []
    for zoom in (100, 125, 140):
        for suffix in ('native', 'half', 'grayscale'):
            old = V6 / f'source-scene-candidate-ordinary-z{zoom}-{suffix}.png'
            new = V7 / f'source-scene-control-ordinary-z{zoom}-{suffix}.png'
            with Image.open(old) as previous, Image.open(new) as current:
                if previous.size != current.size:
                    raise ValueError(f'Baseline dimensions changed: {zoom}/{suffix}')
                # Explicit RGBA comparison avoids RGB conversion concealing alpha drift.
                diff = ImageChops.difference(previous.convert('RGBA'), current.convert('RGBA'))
                if any(channel.getbbox() is not None for channel in diff.split()):
                    raise ValueError(f'Baseline pixels changed: {zoom}/{suffix}')
            comparisons.append(f'{zoom}/{suffix}')
    return dict(status='EXACT_BASELINE_PIXELS_VERIFIED', comparisons=comparisons,
                count=len(comparisons), newNativeRun=False, visualAcceptance=False)


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
