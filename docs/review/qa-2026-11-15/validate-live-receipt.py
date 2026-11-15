#!/usr/bin/env python3
"""Reproduce the observed live-receipt contract failure without changing inputs."""
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

root = Path(__file__).resolve().parents[3]
folder = Path(__file__).resolve().parent
schema_path = root / "Sources/SurveillanceCore/Resources/contracts/run-receipt-001.schema.json"
receipt_path = folder / "live-run-receipt.json"
schema = json.loads(schema_path.read_text())
receipt = json.loads(receipt_path.read_text())
Draft202012Validator.check_schema(schema)
errors = sorted(
    Draft202012Validator(schema).iter_errors(receipt),
    key=lambda error: tuple(str(part) for part in error.path),
)
print(f"Schema: {schema_path.relative_to(root)}")
print(f"Receipt: {receipt_path.relative_to(root)}")
print(f"Live receipt schema violations: {len(errors)}")
for error in errors:
    location = ".".join(str(part) for part in error.path) or "<root>"
    print(f"{location}: {error.message}")
sys.exit(1 if errors else 0)
