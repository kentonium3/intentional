#!/usr/bin/env python3
import sys, re, os, json, datetime
from pathlib import Path

REQUIRED_KEYS = ["id","doc_type","owner","status","last_updated"]

def has_frontmatter(text):
    return text.strip().startswith("---")

def parse_frontmatter(text):
    if not has_frontmatter(text):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_text = parts[1]
    body = parts[2]
    fm = {}
    for line in fm_text.splitlines():
        line=line.strip()
        if not line or line.startswith("#"): continue
        if ":" in line:
            k,v = line.split(":",1)
            fm[k.strip()] = v.strip()
    return fm, body

def main():
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("No docs/ directory found.")
        sys.exit(1)

    bad = []
    for p in docs_dir.rglob("*.md"):
        # Skip template files and Obsidian internal files
        if "_templates" in p.parts or ".obsidian" in p.parts:
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        fm, body = parse_frontmatter(txt)
        if not fm:
            bad.append((str(p), "missing front-matter"))
            continue
        missing = [k for k in REQUIRED_KEYS if k not in fm or not fm[k]]
        if missing:
            bad.append((str(p), f"missing keys: {', '.join(missing)}"))
            continue
        # Basic date sanity check
        try:
            datetime.date.fromisoformat(fm["last_updated"])
        except Exception:
            bad.append((str(p), "last_updated not ISO date (YYYY-MM-DD)"))

    if bad:
        print("Doc front-matter validation FAILED:")
        for path, reason in bad:
            print(f" - {path}: {reason}")
        sys.exit(2)
    print("Doc front-matter validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
