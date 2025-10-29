#!/usr/bin/env python3
"""
Canon v2 Documentation Validator (Pointer Mode)
Validates frontmatter against kg-automation Canon v2 by fetching remote standards.
Respects validator-policy.json for blocking vs advisory checks.
"""
import os, re, sys, json
from pathlib import Path
from urllib.request import urlopen

try:
    import yaml
except ImportError:
    print('Missing deps: pip install pyyaml', file=sys.stderr)
    sys.exit(1)

ROOT = Path('.')
ERRORS = []
WARNINGS = []

# Canon v2 source (kg-automation pinned SHA)
KGA_SHA = '3e587fe'
KGA_BASE_URL = f'https://raw.githubusercontent.com/kentonium3/kg-automation/{KGA_SHA}/docs/standards'

# Check for local standards files first
LOCAL_ALLOWED_VALUES = ROOT / 'docs' / 'standards' / 'allowed-values.json'
LOCAL_SCHEMA = ROOT / 'docs' / 'standards' / 'frontmatter.schema.json'
LOCAL_POLICY = ROOT / 'docs' / 'standards' / 'validator-policy.json'

ALLOWED_VALUES = None
SCHEMA = None
POLICY = None

# Default policy
DEFAULT_POLICY = {
    'blockers': ['required_keys', 'enum_membership', 'formats', 'id_filename_match'],
    'advisories': ['key_order', 'whitespace', 'array_style', 'title_blankline', 'case_style'],
    'id_match_case_sensitive': False,
    'autofix_on_run': True
}


def fetch_remote_file(url):
    """Fetch file from remote URL."""
    try:
        with urlopen(url, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not fetch {url}: {e}", file=sys.stderr)
        return None


def load_canon_v2_standards():
    """Load Canon v2 standards from local files or remote kg-automation."""
    global ALLOWED_VALUES, SCHEMA, POLICY

    # Load policy from local file
    POLICY = DEFAULT_POLICY.copy()
    if LOCAL_POLICY.exists():
        try:
            with open(LOCAL_POLICY, 'r', encoding='utf-8') as f:
                loaded_policy = json.load(f)
                POLICY.update(loaded_policy)
                print(f"Using local validator-policy.json")
        except Exception as e:
            print(f"Warning: Could not load local validator-policy.json: {e}", file=sys.stderr)

    # Try local files first
    if LOCAL_ALLOWED_VALUES.exists():
        try:
            with open(LOCAL_ALLOWED_VALUES, 'r', encoding='utf-8') as f:
                ALLOWED_VALUES = json.load(f)
                print(f"Using local allowed-values.json")
        except Exception as e:
            print(f"Warning: Could not load local allowed-values.json: {e}", file=sys.stderr)

    # Fetch from kg-automation if not local
    if ALLOWED_VALUES is None:
        print(f"Using kg-automation Canon v2 @{KGA_SHA}")
        allowed_values_url = f"{KGA_BASE_URL}/allowed-values.json"
        content = fetch_remote_file(allowed_values_url)
        if content:
            try:
                ALLOWED_VALUES = json.loads(content)
            except Exception as e:
                print(f"Error parsing remote allowed-values.json: {e}", file=sys.stderr)

    # Convert lists to sets for validation
    if ALLOWED_VALUES:
        for key, values in ALLOWED_VALUES.items():
            if isinstance(values, list):
                ALLOWED_VALUES[key] = set(values)
    else:
        # Fallback defaults
        ALLOWED_VALUES = {
            'doc_type': {'strategy', 'charter', 'decision', 'policy', 'handbook', 'runbook', 'guide', 'reference', 'readme', 'index', 'project', 'note'},
            'level': {'overview', 'concept', 'howto', 'reference', 'policy'},
            'status': {'draft', 'in_review', 'approved', 'deprecated', 'archived'},
            'audience': {'agents', 'humans', 'agents_and_humans'}
        }


# Load standards on import
load_canon_v2_standards()


def err(msg, path=None, is_blocker=True):
    """Add error or warning based on blocker status."""
    if path: msg = f"{path}: {msg}"
    if is_blocker:
        ERRORS.append(msg)
    else:
        WARNINGS.append(msg)


def is_blocker(check_type):
    """Check if a validation type is a blocker based on policy."""
    return check_type in POLICY.get('blockers', [])


def front_matter(p):
    """Extract YAML frontmatter from markdown file."""
    txt = Path(p).read_text(encoding='utf-8', errors='ignore')
    if not txt.startswith('---'):
        err('Missing YAML front-matter', p)
        return None
    try:
        lines = txt.splitlines()
        end = None
        for i in range(1, min(len(lines), 500)):
            if lines[i].strip() == '---':
                end = i
                break
        if end is None:
            err("Front-matter closing '---' not found", p)
            return None
        fm_txt = '\n'.join(lines[1:end])
        return yaml.safe_load(fm_txt) or {}
    except Exception as e:
        err(f"Front-matter parse error: {e}", p)
        return None


def validate_iso_date(date_str):
    """Validate YYYY-MM-DD format."""
    if not isinstance(date_str, str):
        return False
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_str))


def validate_revision(rev_str):
    """Validate vMAJOR.MINOR format."""
    if not isinstance(rev_str, str):
        return False
    return bool(re.match(r'^v\d+\.\d+$', rev_str))


def validate_kebab_case(s):
    """Validate kebab-case format."""
    if not isinstance(s, str):
        return False
    return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', s))


def normalize_to_kebab(s):
    """Normalize string to kebab-case (lowercase with hyphens)."""
    if not isinstance(s, str):
        return s
    return re.sub(r'[_\s]+', '-', s.lower())


# Markdown front-matter validation (Canon v2)
ids = {}
for md in ROOT.rglob('*.md'):
    if any(seg in md.parts for seg in ['.git', 'node_modules', '.venv', '_templates']):
        continue

    fm = front_matter(md)
    if not isinstance(fm, dict):
        continue

    # Canon v2 required fields
    required = ['id', 'title', 'doc_type', 'level', 'status', 'owners', 'last_updated', 'revision', 'audience']
    for k in required:
        if k not in fm:
            err(f"Missing front-matter key '{k}'", md, is_blocker=is_blocker('required_keys'))

    # Validate doc_type against allowed values
    if 'doc_type' in fm:
        if fm['doc_type'] not in ALLOWED_VALUES.get('doc_type', set()):
            err(f"Invalid doc_type '{fm['doc_type']}' (allowed: {', '.join(sorted(ALLOWED_VALUES.get('doc_type', set())))})", md, is_blocker=is_blocker('enum_membership'))

    # Validate level against allowed values
    if 'level' in fm:
        if fm['level'] not in ALLOWED_VALUES.get('level', set()):
            err(f"Invalid level '{fm['level']}' (allowed: {', '.join(sorted(ALLOWED_VALUES.get('level', set())))})", md, is_blocker=is_blocker('enum_membership'))

    # Validate status against allowed values
    if 'status' in fm:
        if fm['status'] not in ALLOWED_VALUES.get('status', set()):
            err(f"Invalid status '{fm['status']}' (allowed: {', '.join(sorted(ALLOWED_VALUES.get('status', set())))})", md, is_blocker=is_blocker('enum_membership'))

    # Validate audience against allowed values
    if 'audience' in fm:
        if fm['audience'] not in ALLOWED_VALUES.get('audience', set()):
            err(f"Invalid audience '{fm['audience']}' (allowed: {', '.join(sorted(ALLOWED_VALUES.get('audience', set())))})", md, is_blocker=is_blocker('enum_membership'))

    # Validate owners is non-empty array
    if 'owners' in fm:
        if not isinstance(fm['owners'], list) or len(fm['owners']) == 0:
            err(f"'owners' must be a non-empty array", md, is_blocker=is_blocker('required_keys'))

    # Validate last_updated is ISO date
    if 'last_updated' in fm:
        if not validate_iso_date(fm['last_updated']):
            err(f"'last_updated' must be in YYYY-MM-DD format, got '{fm['last_updated']}'", md, is_blocker=is_blocker('formats'))

    # Validate revision is vMAJOR.MINOR
    if 'revision' in fm:
        if not validate_revision(fm['revision']):
            err(f"'revision' must be in vMAJOR.MINOR format, got '{fm['revision']}'", md, is_blocker=is_blocker('formats'))

    # Validate id is kebab-case and matches filename stem
    if 'id' in fm:
        if not validate_kebab_case(fm['id']):
            err(f"'id' must be kebab-case, got '{fm['id']}'", md, is_blocker=is_blocker('case_style'))

        # Check id matches filename stem
        filename_stem = md.stem
        id_val = fm['id']

        # Normalize for comparison if policy allows case-insensitive matching
        if not POLICY.get('id_match_case_sensitive', True):
            id_normalized = normalize_to_kebab(id_val)
            stem_normalized = normalize_to_kebab(filename_stem)

            if id_normalized != stem_normalized:
                err(f"'id' ('{id_val}') must match filename stem ('{filename_stem}' from '{md.stem}')", md, is_blocker=is_blocker('id_filename_match'))
        else:
            # Case-sensitive matching (strict)
            if id_val != filename_stem:
                err(f"'id' ('{id_val}') must match filename stem ('{filename_stem}' from '{md.stem}')", md, is_blocker=is_blocker('id_filename_match'))

        # Track for duplicate detection
        ids.setdefault(fm['id'], []).append(str(md))

# Check for duplicate IDs
for doc_id, paths in ids.items():
    if len(paths) > 1:
        err(f"Duplicate id '{doc_id}' across: {paths}", is_blocker=is_blocker('required_keys'))

# Report
if WARNINGS:
    print("Warnings (non-blocking):")
    print('\n'.join(f"  WARN: {w}" for w in WARNINGS))
    print()

if ERRORS:
    print('\n'.join(str(e) for e in ERRORS))
    sys.exit(1)
else:
    print('validate_docs: OK')
