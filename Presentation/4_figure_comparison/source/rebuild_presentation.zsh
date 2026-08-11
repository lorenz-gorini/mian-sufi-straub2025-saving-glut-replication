#!/bin/zsh

set -euo pipefail

deck_source_dir=${0:A:h}
deck_dir=${deck_source_dir:h}
project_root=${deck_dir:h:h}
deck_output=${1:-"${deck_dir}/presentation.pptx"}
presentations_skill_dir=${PRESENTATIONS_SKILL_DIR:-"/Users/lorenzogorini/.codex/plugins/cache/openai-primary-runtime/presentations/26.805.11740/skills/presentations"}

if [[ ! -f "${presentations_skill_dir}/container_tools/setup_artifact_tool_workspace.mjs" ]]; then
  print -u2 "Set PRESENTATIONS_SKILL_DIR to the installed presentations skill directory."
  exit 1
fi

deck_workspace=$(mktemp -d /private/tmp/mss-figure-comparison.XXXXXX)

node "${presentations_skill_dir}/container_tools/setup_artifact_tool_workspace.mjs" \
  --workspace "${deck_workspace}"
cp "${deck_source_dir}/build_presentation.mjs" "${deck_workspace}/build_presentation.mjs"

MSS_DECK_WORKSPACE="${deck_workspace}" \
MSS_PROJECT_ROOT="${project_root}" \
MSS_DECK_SOURCE_DIR="${deck_source_dir}" \
MSS_DECK_OUTPUT="${deck_output}" \
PRESENTATIONS_SKILL_DIR="${presentations_skill_dir}" \
node "${deck_workspace}/build_presentation.mjs"

print "Deck written to ${deck_output}"
print "QA intermediates retained in ${deck_workspace}"
