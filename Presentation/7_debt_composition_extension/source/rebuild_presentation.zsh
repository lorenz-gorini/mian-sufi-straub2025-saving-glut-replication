#!/bin/zsh

set -euo pipefail

deck_source_dir=${0:A:h}
deck_dir=${deck_source_dir:h}
project_root=${deck_dir:h:h}
deck_output=${1:-"${deck_dir}/presentation.pptx"}
presentations_skill_dir=${PRESENTATIONS_SKILL_DIR:-"/Users/lorenzogorini/.codex/plugins/cache/openai-primary-runtime/presentations/26.813.12317/skills/presentations"}

: ${RUNTIME_NODE:?Set RUNTIME_NODE from the presentation runtime dependency loader}
: ${RUNTIME_NODE_MODULES:?Set RUNTIME_NODE_MODULES from the presentation runtime dependency loader}
: ${RUNTIME_BIN_DIR:?Set RUNTIME_BIN_DIR from the presentation runtime dependency loader}

deck_workspace=$(mktemp -d /private/tmp/mss-debt-composition-extension.XXXXXX)
ln -s "${RUNTIME_NODE_MODULES}" "${deck_workspace}/node_modules"

RUNTIME_NODE="${RUNTIME_NODE}" \
RUNTIME_NODE_MODULES="${RUNTIME_NODE_MODULES}" \
RUNTIME_BIN_DIR="${RUNTIME_BIN_DIR}" \
PATH="${RUNTIME_BIN_DIR}:${PATH}" \
"${RUNTIME_NODE}" "${presentations_skill_dir}/template_following_scripts/inspect_template_deck.mjs" \
  --workspace "${deck_workspace}" \
  --pptx "${deck_source_dir}/template-starter.pptx"

RUNTIME_NODE="${RUNTIME_NODE}" \
RUNTIME_NODE_MODULES="${RUNTIME_NODE_MODULES}" \
RUNTIME_BIN_DIR="${RUNTIME_BIN_DIR}" \
PATH="${RUNTIME_BIN_DIR}:${PATH}" \
"${RUNTIME_NODE}" "${presentations_skill_dir}/template_following_scripts/prepare_template_starter_deck.mjs" \
  --workspace "${deck_workspace}" \
  --pptx "${deck_source_dir}/template-starter.pptx" \
  --map "${deck_source_dir}/template-frame-map.json" \
  --out "${deck_workspace}/template-starter.pptx" \
  --preview-dir "${deck_workspace}/template-starter-preview" \
  --layout-dir "${deck_workspace}/template-starter-layout"

cp "${deck_source_dir}/build_presentation.mjs" "${deck_workspace}/build_presentation.mjs"

MSS_DECK_WORKSPACE="${deck_workspace}" \
MSS_PROJECT_ROOT="${project_root}" \
MSS_DECK_OUTPUT="${deck_output}" \
PATH="${RUNTIME_BIN_DIR}:${PATH}" \
"${RUNTIME_NODE}" "${deck_workspace}/build_presentation.mjs"

print "Deck written to ${deck_output}"
print "QA intermediates retained in ${deck_workspace}"
