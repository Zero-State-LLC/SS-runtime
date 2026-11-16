#!/usr/bin/env python3
"""RC-001...RC-008: validate actual Swift serializer/archive output, not templates.

Requires the repository's existing jsonschema validation dependency. The Swift
scenario hooks exercise serialization, not full-play, pacing or device gates.
"""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "Sources/SurveillanceCore/Resources/contracts"
SCHEMA = json.loads((CONTRACTS / "run-receipt-002.schema.json").read_text())
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)
V1_SHA256 = "b163b06de53e56bdc93610ac463eacc9c3af8eca97c51c38187d430b405bb325"
OBSERVED_V1_SHA256 = "b569df86fceca5b62edcf4946e322a28d71c73c1f19edb907fba7b97a4854fb1"
MAX_UINT64 = (1 << 64) - 1
PHASES = ["publicSafety", "civilLiberties", "temporarySafeguard", "independentReview"]


def validate_receipt(receipt):
    """Structural schema plus the ordering/projection rules schema cannot express."""
    VALIDATOR.validate(receipt)
    destructions = receipt["cameraDestructions"]
    for record in destructions:
        if int(record["cameraId"]) > MAX_UINT64:
            raise ValueError("Camera ID exceeds UInt64")
    keys = [(record["tick"], int(record["cameraId"])) for record in destructions]
    if keys != sorted(keys):
        raise ValueError("Destructions are not ordered by tick then numeric Camera ID")
    sockets = receipt["cameraPlacement"]["selectedSockets"]
    socket_keys = [socket["socketId"].encode("utf-8") for socket in sockets]
    if socket_keys != sorted(socket_keys):
        raise ValueError("Sockets are not UTF-8 ordered")
    count = len(destructions)
    network = receipt["objectives"]["networkBlackout"]
    camera = receipt["cameraObjective"]
    if not (count == receipt["camerasDestroyed"] == network["camerasDestroyed"] == camera["destroyed"]):
        raise ValueError("Camera destruction projections disagree")
    if not (network["complete"] == camera["complete"] == (count == 8)):
        raise ValueError("Network Blackout completion disagrees")
    tamper = sum(max(0, item["exposureAfter"] - item["exposureBefore"]) for item in destructions)
    if receipt["tamperExposureApplied"] != tamper:
        raise ValueError("Tamper summary disagrees with destruction records")
    boss = receipt["boss"]
    authority_boss = receipt["objectives"]["combatAuthority"]["boss"]
    if boss["defeated"] != authority_boss["defeated"] or boss["phasesReached"] != authority_boss["phasesReached"]:
        raise ValueError("Boss projections disagree")
    phases = boss["phasesReached"]
    if phases != [phase for phase in PHASES if phase in phases]:
        raise ValueError("Boss phases are not in canonical order")


def produce(directory):
    environment = dict(os.environ, SS_RECEIPT_SCHEMA_OUTPUT=str(directory))
    subprocess.run([
        "swift", "test", "--filter", "ReceiptSchemaOutputTests",
        "--parallel", "--num-workers", "1",
    ], cwd=ROOT, env=environment, check=True)
    files = sorted(directory.glob("*.json"))
    expected = {
        f"{outcome}-{upgrade}.json"
        for outcome in ("success", "failure", "invalid")
        for upgrade in ("none", "signalJammer", "ricochetPulse", "ghostStep")
        if not (outcome == "success" and upgrade == "none")
    }
    if {path.name for path in files} != expected:
        raise AssertionError("Swift exporter did not produce the exact eleven terminal cases")
    return {path.name: path.read_bytes() for path in files}


def get_path(document, path):
    for key in path:
        document = document[key]
    return document


class RunReceiptSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="ss-receipt-schema-")
        base = Path(cls.temporary.name)
        cls.outputs = produce(base / "first")
        cls.repeated = produce(base / "second")
        cls.receipts = {name: json.loads(raw) for name, raw in cls.outputs.items()}

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_actual_serialization_and_repeatable_bytes(self):
        self.assertEqual(self.outputs, self.repeated)
        for name, receipt in self.receipts.items():
            with self.subTest(case=name):
                validate_receipt(receipt)
                outcome, selection = name.removesuffix(".json").split("-", 1)
                self.assertEqual(receipt["outcome"], outcome)
                expected_upgrade = None if selection == "none" else {
                    "id": selection, "contractVersion": "upgrades-003"
                }
                self.assertEqual(receipt["upgrade"], expected_upgrade)
        self.assertEqual({item["camerasDestroyed"] for item in self.receipts.values()}, {0, 1, 7, 8})
        self.assertTrue(any(item["seed"] == MAX_UINT64 for item in self.receipts.values()))
        self.assertTrue(any(item["diagnostics"] for item in self.receipts.values()))
        print("Receipt v2: 11 actual archived cases validate with repeatable canonical bytes")

    def test_required_evidence_and_malformed_shapes_fail_closed(self):
        original = self.receipts["success-ricochetPulse.json"]
        mutations = []
        # Every fixed object field in the emitted envelope is required by v2.
        paths = [(), ("identity",), ("player",), ("exposure",), ("combat",),
                 ("objectives",), ("objectives", "combatAuthority"),
                 ("objectives", "combatAuthority", "elite"),
                 ("objectives", "combatAuthority", "boss"),
                 ("objectives", "networkBlackout"), ("cameraPlacement",),
                 ("cameraPlacement", "selectedSockets", 0),
                 ("cameraObjective",), ("upgrade",), ("boss",), ("presentation",)]
        for path in paths:
            for key in get_path(original, path):
                changed = deepcopy(original)
                del get_path(changed, path)[key]
                mutations.append((f"missing {path}.{key}", changed))
            changed = deepcopy(original)
            get_path(changed, path)["unexpected"] = 1
            mutations.append((f"extra field {path}", changed))
        wrong_values = [
            (("schemaVersion",), "run-receipt-001"), (("schemaVersion",), "run-receipt-999"),
            (("identity", "rulesetVersion"), "ss-rules-unknown"),
            (("identity", "contentVersion"), "unknown"), (("identity", "arenaVersion"), "unknown"),
            (("identity", "replaySchemaVersion"), "unknown"),
            (("upgrade",), "ricochetPulse"), (("upgrade", "id"), "unknown"),
            (("upgrade", "contractVersion"), "upgrades-999"),
            (("seed",), MAX_UINT64 + 1), (("seed",), -1), (("seed",), True),
            (("elapsedTicks",), MAX_UINT64 + 1), (("finalDigest",), "not-a-digest"),
            (("finalDigest",), "a" * 64 + "\n"),
            (("outcome",), "playing"), (("exposure", "finalState"), "unknown"),
            (("objectives", "extractionArmed"), "true"),
            (("objectives", "combatAuthority", "currentNode"), "unknown"),
            (("cameraObjective", "total"), 9), (("cameraObjective", "destroyed"), 9),
            (("cameraPlacement", "selectedSockets", 0, "housingFamily"), "unknown"),
            (("cameraPlacement", "selectedSockets", 0, "cameraEntityId"), "2"),
            (("presentation", "hudScale"), 1001), (("presentation", "handedness"), "unknown"),
            (("diagnostics",), ["unknown"]),
            (("boss", "phasesReached"), ["publicSafety", "publicSafety"]),
            (("boss", "phasesReached"), ["unknown"]),
        ]
        for path, value in wrong_values:
            changed = deepcopy(original)
            get_path(changed, path[:-1])[path[-1]] = value
            mutations.append((f"invalid {path}={value!r}", changed))
        destruction_case = self.receipts["failure-ricochetPulse.json"]
        for key in destruction_case["cameraDestructions"][0]:
            changed = deepcopy(destruction_case)
            del changed["cameraDestructions"][0][key]
            mutations.append((f"missing destruction {key}", changed))
        for field, value in [("cameraId", str(MAX_UINT64 + 1)), ("cameraId", "01"),
                             ("cameraId", "1\n"), ("tick", MAX_UINT64 + 1), ("wasDetectingPlayer", "false"),
                             ("source", ""), ("unexpected", 1)]:
            changed = deepcopy(destruction_case)
            changed["cameraDestructions"][0][field] = value
            mutations.append((f"invalid destruction {field}", changed))
        for label, mutate in [
            ("destruction order", lambda item: item["cameraDestructions"].reverse()),
            ("socket order", lambda item: item["cameraPlacement"]["selectedSockets"].reverse()),
            ("Tamper projection", lambda item: item.update(tamperExposureApplied=99999)),
            ("boss projection", lambda item: item["boss"].update(defeated=True)),
        ]:
            changed = deepcopy(destruction_case)
            mutate(changed)
            mutations.append((label, changed))
        for label, receipt in mutations:
            with self.subTest(case=label):
                with self.assertRaises((ValidationError, ValueError)):
                    validate_receipt(receipt)
        print(f"Receipt v2: {len(mutations)} missing/malformed/identity/order mutations rejected")

    def test_recorded_complete_run_preserves_every_gameplay_projection(self):
        raw = (ROOT / "docs/review/receipt-v2-live-20261115.json").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         "3718a3233a3429949ecfa20b33b59d2dee03c9e79d80cced3caf1854a57a9316")
        current = json.loads(raw)
        validate_receipt(current)
        historical = json.loads((ROOT / "scripts/fixtures/receipt-v1-observed.json").read_bytes())
        historical["schemaVersion"] = "run-receipt-002"
        historical["upgrade"] = {"id": historical["upgrade"], "contractVersion": "upgrades-003"}
        self.assertEqual(historical, current)
        self.assertEqual(current["outcome"], "success")
        self.assertEqual(current["elapsedTicks"], 17776)

    def test_historical_schema_and_observed_receipt_are_not_rewritten(self):
        raw_schema = (CONTRACTS / "run-receipt-001.schema.json").read_bytes()
        self.assertEqual(hashlib.sha256(raw_schema).hexdigest(), V1_SHA256)
        observed = (ROOT / "scripts/fixtures/receipt-v1-observed.json").read_bytes()
        self.assertEqual(hashlib.sha256(observed).hexdigest(), OBSERVED_V1_SHA256)
        receipt = json.loads(observed)
        self.assertEqual(receipt["schemaVersion"], "run-receipt-001")
        self.assertEqual(len(list(Draft202012Validator(json.loads(raw_schema)).iter_errors(receipt))), 3)
        with self.assertRaises(ValidationError):
            VALIDATOR.validate(receipt)
        registry = json.loads((CONTRACTS / "versions.json").read_text())
        self.assertEqual(registry["componentContracts"]["runReceipt"], "run-receipt-002")
        print("Historical v1 schema and observed invalid receipt retain exact original SHA-256 bytes")


if __name__ == "__main__":
    unittest.main()
