"""Strict replay metadata comparison. Only truthful current Python may differ."""
import hashlib
import json
import sys

AUTHOR_FINAL_SHA256='42dd1d5f8f8a330e7790afdc4da59a8f33f4cb3595c1654a38e8ccc0d59889b2'
AUTHOR_CONTROL_SHA256='7b095e443924a409c9114c7d3993aac17cbc0d2b8a0163c6d215c1ebe8c9be1c'

def compare_manifest(author_path,replayed_path,author_sha256):
    author_bytes=author_path.read_bytes()
    if hashlib.sha256(author_bytes).hexdigest()!=author_sha256:
        raise AssertionError('Retained author manifest pin mismatch')
    author=json.loads(author_bytes)
    replayed=json.loads(replayed_path.read_bytes())
    if replayed.get('python')!=sys.version.split()[0]:
        raise AssertionError('Replayed interpreter does not match actual sys.version')
    author_without_python={k:v for k,v in author.items() if k!='python'}
    replayed_without_python={k:v for k,v in replayed.items() if k!='python'}
    if author_without_python!=replayed_without_python:
        raise AssertionError('Non-interpreter manifest field changed')
    return replayed
