#!/usr/bin/env bash
# Validate only the staged tracked tree, never unrelated untracked work.
set -euo pipefail
SOURCE=$(git rev-parse --show-toplevel)
SCRATCH=$(cd "${JCODE_SCRATCH_DIR:?Set an external scratch directory}" && pwd -P)
case "$SCRATCH/" in "$SOURCE/"*) echo 'Scratch must be outside source checkout' >&2; exit 1;; esac
BASE=$(git rev-parse HEAD)
TREE=$(git write-tree)
COMMIT=$(printf 'Temporary staged preservation validation snapshot\n' | git commit-tree "$TREE" -p "$BASE")
EXPORT=$(mktemp -d "$SCRATCH/ss-preservation-export.XXXXXX")
STEP=$(mktemp "$SCRATCH/ss-preservation-step.XXXXXX")
OBJECTS=$(git rev-parse --path-format=absolute --git-path objects)
SHALLOW=$(git rev-parse --path-format=absolute --git-path shallow)
git init -q "$EXPORT"
printf '%s\n' "$OBJECTS" > "$EXPORT/.git/objects/info/alternates"
if test -f "$SHALLOW"; then cp "$SHALLOW" "$EXPORT/.git/shallow"; fi
git -C "$EXPORT" update-ref HEAD "$COMMIT"
git -C "$EXPORT" read-tree "$COMMIT"
git -C "$EXPORT" checkout-index --all
test -z "$(git -C "$EXPORT" status --porcelain)"
printf 'BASE=%s\nTREE=%s\nSNAPSHOT=%s\nEXPORT=%s\n' "$BASE" "$TREE" "$COMMIT" "$EXPORT"
printf 'JCODE_PROGRESS {"message":"Tracked-only snapshot ready; starting exact affected CI step"}\n'
cd "$EXPORT"
ruby -ryaml -e '
  workflow = YAML.load_file(".github/workflows/ci.yml")
  job = workflow.fetch("jobs").fetch("spec-parity")
  raise "Historical objects unavailable" unless job.fetch("steps").first.fetch("with").fetch("fetch-depth") == 0
  step = job.fetch("steps").find { |value| value["name"] == "Verify bounded base and curb comparison without admission" }
  puts step.fetch("run")
' > "$STEP"
RUNNER_TEMP="$SCRATCH" JCODE_SCRATCH_DIR="$SCRATCH" bash -ex "$STEP"
printf 'JCODE_PROGRESS {"message":"Exact affected CI step passed; checking downstream steps"}\n'
python3 -B scripts/test_runtime_audit_guards.py
python3 -B -W error::ResourceWarning -m unittest discover -s docs/review/playback237-diagnosis-20261116 -p 'test_trace_probe.py' -v
python3 -B scripts/test_spec_parity_isolation.py
bash scripts/spec_parity.sh
test -z "$(git status --porcelain)"
printf 'TRACKED_EXPORT_VALIDATION_PASSED snapshot=%s\n' "$COMMIT"
# Retain owned scratch export and extracted commands for independent inspection.
