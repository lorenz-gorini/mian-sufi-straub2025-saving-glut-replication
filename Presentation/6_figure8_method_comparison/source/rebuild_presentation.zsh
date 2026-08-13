#!/bin/zsh

set -euo pipefail

deck_source_dir=${0:A:h}
deck_dir=${deck_source_dir:h}
project_root=${deck_dir:h:h}
deck_output=${1:-"${deck_dir}/presentation.pptx"}

: ${RUNTIME_NODE:?Set RUNTIME_NODE from the presentation runtime dependency loader}
: ${RUNTIME_NODE_MODULES:?Set RUNTIME_NODE_MODULES from the presentation runtime dependency loader}

deck_workspace=$(mktemp -d /private/tmp/mss-figure8-method-comparison.XXXXXX)
ln -s "${RUNTIME_NODE_MODULES}" "${deck_workspace}/node_modules"
cp "${deck_source_dir}/build_presentation.mjs" "${deck_workspace}/build_presentation.mjs"
cp "${deck_source_dir}/template-starter.pptx" "${deck_workspace}/template-starter.pptx"

MSS_DECK_WORKSPACE="${deck_workspace}" \
MSS_PROJECT_ROOT="${project_root}" \
MSS_DECK_OUTPUT="${deck_output}" \
"${RUNTIME_NODE}" "${deck_workspace}/build_presentation.mjs"

print "Deck written to ${deck_output}"
print "QA intermediates retained in ${deck_workspace}"
