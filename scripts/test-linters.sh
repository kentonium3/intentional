#!/bin/bash
# Script to compare Obsidian Linter and markdownlint-cli2 outputs
# Usage: ./scripts/test-linters.sh [file_or_directory]

set -e

TARGET="${1:-docs}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="linter-reports"

# Create report directory
mkdir -p "$REPORT_DIR"

echo "========================================"
echo "Linter Comparison Test"
echo "========================================"
echo "Target: $TARGET"
echo "Timestamp: $TIMESTAMP"
echo ""

# Run markdownlint-cli2
echo "Running markdownlint-cli2..."
npx markdownlint-cli2 "$TARGET/**/*.md" > "$REPORT_DIR/markdownlint-${TIMESTAMP}.txt" 2>&1 || true

# Count errors by rule
echo ""
echo "========================================"
echo "markdownlint-cli2 Summary"
echo "========================================"

if [ -f "$REPORT_DIR/markdownlint-${TIMESTAMP}.txt" ]; then
    TOTAL_ERRORS=$(grep -c "MD[0-9]" "$REPORT_DIR/markdownlint-${TIMESTAMP}.txt" || echo "0")
    echo "Total errors: $TOTAL_ERRORS"
    echo ""

    echo "Top 10 violations:"
    grep -oP 'MD[0-9]+/[a-z-]+' "$REPORT_DIR/markdownlint-${TIMESTAMP}.txt" | sort | uniq -c | sort -rn | head -10
    echo ""

    echo "Files with most errors:"
    grep -oP 'docs/[^:]+' "$REPORT_DIR/markdownlint-${TIMESTAMP}.txt" | sort | uniq -c | sort -rn | head -10
    echo ""
fi

echo "========================================"
echo "Obsidian Linter Status"
echo "========================================"
echo "Current enabled rules (Phase 1):"
grep -E '"enabled": true' docs/.obsidian/plugins/obsidian-linter/data.json | wc -l
echo ""

echo "Phase 1 critical rules:"
echo "  - heading-blank-lines: $(grep -A1 '"heading-blank-lines"' docs/.obsidian/plugins/obsidian-linter/data.json | grep enabled | grep -q true && echo 'ENABLED' || echo 'DISABLED')"
echo "  - trailing-spaces: $(grep -A1 '"trailing-spaces"' docs/.obsidian/plugins/obsidian-linter/data.json | grep enabled | grep -q true && echo 'ENABLED' || echo 'DISABLED')"
echo "  - consecutive-blank-lines: $(grep -A1 '"consecutive-blank-lines"' docs/.obsidian/plugins/obsidian-linter/data.json | grep enabled | grep -q true && echo 'ENABLED' || echo 'DISABLED')"
echo "  - empty-line-around-code-fences: $(grep -A1 '"empty-line-around-code-fences"' docs/.obsidian/plugins/obsidian-linter/data.json | grep enabled | grep -q true && echo 'ENABLED' || echo 'DISABLED')"
echo "  - empty-line-around-tables: $(grep -A1 '"empty-line-around-tables"' docs/.obsidian/plugins/obsidian-linter/data.json | grep enabled | grep -q true && echo 'ENABLED' || echo 'DISABLED')"
echo ""

echo "========================================"
echo "Reports saved to:"
echo "  $REPORT_DIR/markdownlint-${TIMESTAMP}.txt"
echo "========================================"
