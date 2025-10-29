---
id: canon-v2-pointer
title: Documentation Standards (Canon v2) - Pointer
doc_type: policy
level: reference
status: approved
owners:
  - "@kentonium3"
last_updated: "2024-10-28"
revision: v1.0
audience: agents_and_humans
tags:
  - standards
  - documentation
  - canon-v2
---

# Documentation Standards (Canon v2) - Pointer

This repository adopts **Canon v2** documentation standards from `kg-automation` by pinned SHA reference.

## Canon Source

**Repository**: kg-automation
**Commit SHA**: `a42f297`
**Commit**: docs(canon-v2): schema, allowlists, templates, validator, presets

## Canonical Files (Pinned URLs)

The following files define Canon v2 and are fetched by reference:

### Documentation Standards
**URL**: https://raw.githubusercontent.com/kentonium3/kg-automation/a42f297/docs/standards/doc-standards.md

Comprehensive documentation of all Canon v2 requirements, field specifications, allowed values, templates, and validation rules.

### Frontmatter Schema
**URL**: https://raw.githubusercontent.com/kentonium3/kg-automation/a42f297/docs/standards/frontmatter.schema.json

JSON Schema (Draft 2020-12) defining the structure and validation rules for document frontmatter.

### Allowed Values
**URL**: https://raw.githubusercontent.com/kentonium3/kg-automation/a42f297/docs/standards/allowed-values.json

Machine-readable enumeration of all allowed values for classification fields:
- `doc_type`: strategy, charter, decision, policy, handbook, runbook, guide, reference, readme, index, project, note
- `level`: overview, concept, howto, reference, policy
- `status`: draft, in_review, approved, deprecated, archived
- `audience`: agents, humans, agents_and_humans

## Local Implementation

This repository includes:
- **Validator**: `tooling/scripts/validate_docs.py` - Fetches and enforces Canon v2 rules
- **Templates**: `docs/_templates/` - Templater templates for creating Canon v2 compliant docs
- **Claude Code Preset**: `.claude/presets/new-doc.json` - Interactive doc creation workflow

## Updating the Canon Reference

To update to a newer version of Canon v2:
1. Identify the target commit SHA from kg-automation
2. Update the SHA references in this document
3. Update the pinned SHA in `tooling/scripts/validate_docs.py`
4. Run validation to ensure compatibility
5. Commit with message: `docs(canon-v2): update canon pointer to <new-sha>`

## Questions & Support

For Canon v2 questions:
- **Source Repository**: https://github.com/kentonium3/kg-automation
- **Canon v2 Commit**: https://github.com/kentonium3/kg-automation/commit/a42f297
- **Issues**: Create issue in kg-automation with `documentation` label