# Runtime audit guard CI coverage

Tracking: SS-runtime #231. Follows the lifecycle reconciliation in #230.

## Change

The existing `spec-parity` job now runs
`python3 -B scripts/test_runtime_audit_guards.py` before contract parity.
All existing core, camera-placement, camera-fairness, Debug/Release app,
specification parity, and device-sitting checks remain unchanged.
No workflow or production dependency is added, and no gameplay or pin changes.

## Verification

- Before the change, a parsed-workflow assertion failed because the guard script
  was absent. After the change, it finds exactly one new guard step.
- Removing that step from the parsed new workflow reproduces the parsed baseline
  exactly, including all existing jobs, commands, and triggers.
- All five runtime source-wiring guards pass locally.
- GitHub execution of the new step must pass before this change is considered
  CI-validated. Local workflow inspection is not remote execution evidence.

The Python checks inspect source wiring, not native behavior. Native core and
Debug/Release app tests remain mandatory. No new physical-device, audio/haptic,
visual, or production acceptance is claimed by this change.
