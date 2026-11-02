#!/usr/bin/env bash
# Headless device-sitting probe.
#
# Plays the UTC 2026-11-02 daily seed four ways (first-run lower bound,
# natural, sneaky, loud) with Ricochet Pulse, and checks outcome, time,
# Integrity, Court, medals, and damage sources.
#
# It does not see the phone, the opening lines, or the art. Issue #117,
# T903, and T904 stay open.
set -euo pipefail
cd "$(dirname "$0")/.."
export SS_DEVICE_SITTING=1
exec swift test --filter DeviceSittingQA --skip CameraPlacementTests --skip CameraFairnessTests --parallel --num-workers 1
