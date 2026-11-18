#!/usr/bin/env python3
"""Record the only model changes authorized for the padding correction."""
import copy
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def padded_model():
    prior=json.loads((HERE/'control/assembly.json').read_text())
    model=copy.deepcopy(prior)
    model['canvas'][0]+=24
    model['root'][0]+=12
    for layer in model['layers']:
        layer['position'][0]+=12
    return model

if __name__=='__main__':
    (HERE/'assembly.json').write_text(json.dumps(padded_model(),indent=2)+'\n')
