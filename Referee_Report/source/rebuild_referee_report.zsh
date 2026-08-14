#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
PROJECT_ROOT="${SCRIPT_DIR:h:h}"
SOURCE_MD="$PROJECT_ROOT/Referee_Report/referee_report.md"
OUTPUT_DIR="$PROJECT_ROOT/Referee_Report/output"
TMP_DIR="$PROJECT_ROOT/tmp/referee_report"
PYTHON_BIN="${PYTHON_BIN:-/Users/lorenzogorini/anaconda3/envs/general/bin/python}"

mkdir -p "$OUTPUT_DIR" "$TMP_DIR"

pandoc --print-default-data-file reference.docx > "$TMP_DIR/reference-default.docx"
"$PYTHON_BIN" "$SCRIPT_DIR/style_docx.py" \
  "$TMP_DIR/reference-default.docx" \
  "$TMP_DIR/reference-referee.docx"

pandoc "$SOURCE_MD" \
  --from=markdown+smart+tex_math_dollars+implicit_figures \
  --resource-path="$PROJECT_ROOT/Referee_Report:$PROJECT_ROOT" \
  --reference-doc="$TMP_DIR/reference-referee.docx" \
  --output="$TMP_DIR/referee_report_unstyled.docx"

"$PYTHON_BIN" "$SCRIPT_DIR/style_docx.py" \
  "$TMP_DIR/referee_report_unstyled.docx" \
  "$OUTPUT_DIR/referee_report.docx"

pandoc "$SOURCE_MD" \
  --from=markdown+smart+tex_math_dollars+implicit_figures \
  --resource-path="$PROJECT_ROOT/Referee_Report:$PROJECT_ROOT" \
  --pdf-engine=xelatex \
  --output="$OUTPUT_DIR/referee_report.pdf"

printf '%s\n' \
  "$OUTPUT_DIR/referee_report.docx" \
  "$OUTPUT_DIR/referee_report.pdf"
