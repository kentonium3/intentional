---
id: linter-alignment-report
title: Linter Alignment Report
doc_type: note
level: reference
owners: ["@kentonium3"]
revision: v1.0
audience: agents_and_humans
status: approved
last_updated: '2025-10-29'
---

# Linter Alignment Report

**Date:** 2025-10-25
**Branch:** docs/project-hub-updates

## Executive Summary

Successfully aligned Obsidian Linter plugin settings with markdownlint-cli2 to ensure local editing matches CI validation. Initial scan identified **163 errors** across **19 files** that need remediation.

---

## Phase 1: Configuration Alignment

### Changes Applied

Updated `docs/.obsidian/plugins/obsidian-linter/data.json` with 9 critical rules:

| Rule | Purpose | Status |
|------|---------|--------|
| `heading-blank-lines` | Blank lines around headings | ✅ Enabled |
| `trailing-spaces` | Remove trailing whitespace | ✅ Enabled |
| `consecutive-blank-lines` | Limit consecutive blanks | ✅ Enabled |
| `empty-line-around-code-fences` | Blank lines around code | ✅ Enabled |
| `empty-line-around-tables` | Blank lines around tables | ✅ Enabled |
| `empty-line-around-blockquotes` | Blank lines around quotes | ✅ Enabled |
| `unordered-list-style` | Consistent list markers | ✅ Enabled |
| `line-break-at-document-end` | Single newline at EOF | ✅ Enabled |
| `remove-trailing-punctuation-in-heading` | Clean heading format | ✅ Enabled |

**Total enabled rules:** 18 (up from 9)

---

## Current Violations Analysis

### By Rule Type

| Rule | Count | Description | Severity |
|------|-------|-------------|----------|
| **MD022** | 88 | Headings should be surrounded by blank lines | 🔴 High |
| **MD032** | 48 | Lists should be surrounded by blank lines | 🔴 High |
| **MD003** | 13 | Inconsistent heading style (ATX vs Setext) | 🟡 Medium |
| **MD036** | 5 | Emphasis used instead of heading | 🟡 Medium |
| **MD058** | 5 | Tables should be surrounded by blank lines | 🟡 Medium |
| **MD034** | 3 | Bare URLs without link markup | 🟢 Low |
| **MD012** | 1 | Multiple consecutive blank lines | 🟢 Low |

**Total:** 163 violations

### By File

| File | Errors | Priority |
|------|--------|----------|
| `docs/intentional_launch_project_hub.md` | 40 | 🔴 Critical |
| `docs/Kent_Gale_Resume.md` | 21 | 🔴 High |
| `docs/_templates/strategy_doc_template.md` | 20 | 🔴 High |
| `docs/_templates/project_plan_template.md` | 15 | 🟡 Medium |
| `docs/_index.md` | 12 | 🟡 Medium |
| `docs/sales/proposal_template.md` | 12 | 🟡 Medium |
| `docs/branding_tone.md` | 9 | 🟢 Low |
| `docs/web/website_plan.md` | 8 | 🟢 Low |
| Others (11 files) | 26 | 🟢 Low |

---

## Root Cause Analysis

### 1. MD022: Blanks Around Headings (88 errors)

**Problem:** Headings immediately follow content or YAML without blank lines.

**Example:**
```markdown
# Title
## Subtitle  ❌ Missing blank line above
Content here
```

**Fix:**
```markdown
# Title

## Subtitle  ✅ Blank line added
Content here
```

### 2. MD032: Blanks Around Lists (48 errors)

**Problem:** Lists start/end without surrounding blank lines.

**Example:**
```markdown
Some text
- Item 1  ❌ No blank line before list
- Item 2
Next paragraph  ❌ No blank line after list
```

**Fix:**
```markdown
Some text

- Item 1  ✅ Blank lines added
- Item 2

Next paragraph
```

### 3. MD003: Heading Style (13 errors)

**Problem:** Inconsistent heading styles (ATX `#` vs Setext underline).

**Context:** Template files use dynamic Templater syntax which confuses the linter.

**Recommendation:** Exclude template files from CI or add inline comments to disable this rule.

---

## Tooling Setup

### Test Scripts Created

1. **PowerShell:** `scripts/test-linters.ps1`
2. **Bash:** `scripts/test-linters.sh`

**Usage:**
```powershell
# Run comparison test
.\scripts\test-linters.ps1

# Test specific directory
.\scripts\test-linters.ps1 docs/web
```

**Output:**
- Summary of violations by type
- Files with most errors
- Obsidian Linter status verification
- Report saved to `linter-reports/`

---

## Next Steps

### Immediate Actions

1. **Fix Critical Files** (40+ errors):
   - [ ] `intentional_launch_project_hub.md`
   - [ ] `Kent_Gale_Resume.md`

2. **Fix Template Files**:
   - [ ] Add `.markdownlint-cli2.yaml` override for `_templates/`
   - [ ] Or manually fix template formatting

3. **Bulk Remediation**:
   - Run Obsidian Linter on all files (File Change mode is enabled)
   - Or use markdownlint-cli2 auto-fix: `npx markdownlint-cli2 --fix`

### Phase 2: YAML Standardization (Recommended)

Enable these rules for better YAML consistency:

```json
{
  "format-yaml-array": {
    "enabled": true,
    "default-array-style": "single-line"
  },
  "yaml-key-sort": {
    "enabled": true,
    "yaml-key-priority-sort-order": "id, doc_type, owner, status, last_updated, tags, aliases"
  },
  "escape-yaml-special-characters": {
    "enabled": true
  }
}
```

### Phase 3: Auto-Fix on Save (Optional)

Enable in `data.json`:
```json
{
  "lintOnSave": true
}
```

**Trade-off:** May cause unexpected changes during editing.

---

## Obsidian Linter vs markdownlint-cli2

### Rule Mapping

| markdownlint Rule | Obsidian Linter Equivalent | Status |
|-------------------|---------------------------|--------|
| MD022 (heading blanks) | `heading-blank-lines` | ✅ Aligned |
| MD032 (list blanks) | N/A - handled by multiple rules | ⚠️ Partial |
| MD009 (trailing spaces) | `trailing-spaces` | ✅ Aligned |
| MD012 (consecutive blanks) | `consecutive-blank-lines` | ✅ Aligned |
| MD031 (code fence blanks) | `empty-line-around-code-fences` | ✅ Aligned |
| MD058 (table blanks) | `empty-line-around-tables` | ✅ Aligned |
| MD047 (EOF newline) | `line-break-at-document-end` | ✅ Aligned |
| MD026 (heading punctuation) | `remove-trailing-punctuation-in-heading` | ✅ Aligned |
| MD004 (list style) | `unordered-list-style` | ✅ Aligned |

### Gaps & Limitations

1. **MD032 (List Blanks):** Obsidian Linter doesn't have a single equivalent rule. Covered partially by:
   - `empty-line-around-*` rules
   - Manual enforcement needed

2. **MD003 (Heading Style):** Not enforceable in Obsidian Linter. Consider:
   - Disabling MD003 in `.markdownlint-cli2.yaml`, OR
   - Manually enforce ATX style (`#` format)

3. **Template Files:** Templater syntax conflicts with linters. Options:
   - Exclude `_templates/` from CI
   - Add `.markdownlintignore` file

---

## Recommended `.markdownlintignore`

Create this file to exclude problematic paths:

```
docs/_templates/
docs/.obsidian/
node_modules/
```

---

## Commands Reference

### Run Linter Locally
```bash
# Check all docs
npx markdownlint-cli2

# Auto-fix violations
npx markdownlint-cli2 --fix

# Check specific files
npx markdownlint-cli2 docs/intentional_launch_project_hub.md
```

### Obsidian Linter
- **Manual:** Command Palette → "Linter: Lint current file"
- **Auto:** Enabled on file change (already configured)
- **Batch:** Not available in plugin (use markdownlint-cli2)

---

## Configuration Backup

**Backup location:** `docs/.obsidian/plugins/obsidian-linter/data.json.backup`

To restore:
```bash
cp docs/.obsidian/plugins/obsidian-linter/data.json.backup \
   docs/.obsidian/plugins/obsidian-linter/data.json
```

---

## Conclusion

✅ **Completed:**
- Obsidian Linter aligned with markdownlint-cli2 Phase 1 rules
- Test scripts created for ongoing validation
- 163 violations identified and categorized

⏭️ **Next:**
- Run auto-fix or manual remediation on critical files
- Consider excluding `_templates/` from CI
- Optionally enable Phase 2 YAML rules

🎯 **Expected Outcome:**
Local editing in Obsidian will now catch the same issues as CI, reducing PR feedback loops.
