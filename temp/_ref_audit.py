# -*- coding: utf-8 -*-
"""Extract file-path mentions from kit scoped markdown and check existence."""
from __future__ import annotations

import os
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"c:\GitHub\1c-ai-development-kit-van")

SCOPE_FILES: list[Path] = []

def add_glob(pattern: str) -> None:
    for p in ROOT.glob(pattern):
        if p.is_file():
            SCOPE_FILES.append(p)

add_glob(".cursor/rules/*.mdc")
add_glob(".cursor/skills/**/*.md")
add_glob(".cursor/commands/*.md")
add_glob(".cursor/agents/*.md")
add_glob(".cursor/docs/*.md")
add_glob(".cursor/docs/templates/*.md")
add_glob(".cursor/docs/casebooks/*.md")
add_glob("openspec/specs/**/spec.md")
add_glob("openspec/adrs/*.md")
SCOPE_FILES.append(ROOT / "AGENTS.md")
SCOPE_FILES.append(ROOT / "README.md")
SCOPE_FILES.append(ROOT / "openspec/glossary.md")

# de-dupe
seen = set()
uniq = []
for p in SCOPE_FILES:
    rp = p.resolve()
    if rp not in seen:
        seen.add(rp)
        uniq.append(p)
SCOPE_FILES = uniq

# Exclude platform/standard/changes already by glob choice.
# Also skip skill fixtures/test-cases? User said all SKILL.md and templates.
# User: ".cursor/skills/**/*.md (все SKILL.md и templates)"
# So we should NOT scan fixtures/test-cases/profiles unless they are SKILL or templates.
filtered = []
for p in SCOPE_FILES:
    rel = p.relative_to(ROOT).as_posix()
    if rel.startswith(".cursor/skills/"):
        name = p.name
        parent = p.parent.name
        # keep SKILL.md, templates, and role modules that are referenced as skills docs
        # User said: all SKILL.md and templates. That's narrower.
        # Being pedantic: user said ".cursor/skills/**/*.md (все SKILL.md и templates)"
        # I'll keep SKILL.md, templates/*.md, AND also sidecar/role files under 1c-agent-patterns
        # because they are referenced as SSOT. But the stated scope is SKILL.md and templates.
        if name == "SKILL.md":
            filtered.append(p)
            continue
        if "/templates/" in rel.replace("\\", "/"):
            filtered.append(p)
            continue
        # Extra: 1c-agent-patterns role files are part of the skill package and heavily linked
        if "/1c-agent-patterns/" in rel and name.endswith(".md"):
            filtered.append(p)
            continue
        # skip fixtures, test-cases, profiles, compose, cycle unless SKILL
        continue
    filtered.append(p)
SCOPE_FILES = filtered

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# paths in backticks
BT_PATH = re.compile(
    r"`((?:\.cursor|openspec|temp|\.cursor/templates)[^`\n]{0,220})`"
)
# also bare .cursor/... in backticks without starting exactly
BT_ANY = re.compile(r"`([^`\n]{3,240})`")
# markdown relative links without backticks already covered

SKIP_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "#",
)

# extensions / path-like
PATHISH = re.compile(
    r"^(?:\.\./|\./)?"
    r"(?:\.cursor/|openspec/|temp/|\.cursor\\\\|AGENTS\.md|README\.md|"
    r"docs/|rules/|skills/|commands/|agents/|templates/|"
    r"glossary\.md|project\.md|config\.yaml)"
    r".*",
    re.I,
)

FILE_EXT = re.compile(
    r"\.(mdc|md|ya?ml|json|xml|bsl|txt|pff|template)$", re.I
)

# strip trailing punctuation from captured path
TRAIL = re.compile(r"[.,;:)\]]+$")

# placeholders
PLACEHOLDER = re.compile(r"[<>]|YYYY|MM-DD|<name>|<slug>|<тип>|<scope>|…|\.\.\.|N\+|S<")

def normalize_link_target(raw: str) -> str:
    t = raw.strip()
    if " " in t and not t.startswith("http"):
        # title after path: path "title"
        if t.startswith('"') or t.startswith("'"):
            return t
        parts = t.split()
        t = parts[0]
    t = t.split("#")[0].strip()
    t = t.strip("<>")
    t = TRAIL.sub("", t)
    t = t.replace("\\", "/")
    return t

def is_pathish(s: str) -> bool:
    s = s.strip()
    if not s or s.startswith("http"):
        return False
    if s.startswith("git ") or " " in s and not any(c in s for c in "/\\"):
        return False
    if PATHISH.match(s):
        return True
    if FILE_EXT.search(s) and ("/" in s or s.startswith(".")):
        return True
    # relative like ../docs/foo.md
    if s.startswith("../") or s.startswith("./"):
        return True
    # filename-only with known kit names
    if s.endswith((".mdc", ".md")) and not s.startswith("http"):
        # only if it looks like a kit file, not a heading
        if "/" in s or s in {"AGENTS.md", "README.md", "SKILL.md", "proposal.md", "design.md", "tasks.md"}:
            return True
        if s.endswith(".mdc"):
            return True
    return False

def resolve(src: Path, target: str) -> Path | None:
    t = target.replace("\\", "/").strip()
    if not t or t.startswith(("http://", "https://", "mailto:")):
        return None
    if PLACEHOLDER.search(t) and not t.startswith("temp/"):
        # keep temp placeholders as runtime
        pass
    # repo-root absolute-ish
    if t.startswith(".cursor/") or t.startswith("openspec/") or t.startswith("temp/"):
        return ROOT / t
    if t in {"AGENTS.md", "README.md"}:
        return ROOT / t
    if t.startswith("openspec\\") or t.startswith(".cursor\\"):
        return ROOT / t.replace("\\", "/")
    # relative to source file
    if t.startswith("../") or t.startswith("./"):
        return (src.parent / t).resolve()
    # filename-only .mdc — try rules
    if t.endswith(".mdc") and "/" not in t:
        cand = ROOT / ".cursor/rules" / t
        if cand.exists():
            return cand
        return ROOT / ".cursor/rules" / t  # still report missing
    # skills relative SKILL.md from command
    if t == "SKILL.md":
        return src.parent / t
    # docs/ without .cursor
    if t.startswith("docs/") and src.as_posix().replace("\\", "/").find("/.cursor/") >= 0:
        # from .cursor/docs or commands
        if (ROOT / ".cursor" / t).exists() or src.parent.name in {"commands", "rules", "docs", "agents"}:
            p1 = ROOT / ".cursor" / t
            if p1.exists():
                return p1
        p2 = (src.parent / t).resolve()
        return p2
    # skills/ without .cursor
    if t.startswith("skills/") or t.startswith("rules/") or t.startswith("agents/") or t.startswith("commands/"):
        p = ROOT / ".cursor" / t
        return p
    if t.startswith("templates/") and "skills" in src.as_posix():
        return src.parent / t
    # openspec relative
    if t.startswith("specs/") or t.startswith("adrs/") or t.startswith("knowledge/"):
        return ROOT / "openspec" / t
    # relative path with slashes from same dir tree
    if "/" in t and not t.startswith("/"):
        # try relative to src
        rel = (src.parent / t).resolve()
        root_res = ROOT.resolve()
        try:
            rel.relative_to(root_res)
            return rel
        except ValueError:
            return rel
    return None


findings = []  # (src, line, quote, target, resolved, exists, kind)
all_refs = []

for src in SCOPE_FILES:
    try:
        text = src.read_text(encoding="utf-8")
    except Exception as e:
        findings.append((str(src), 0, "", "", None, False, f"read-error {e}"))
        continue
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        # skip HTML comments? still check
        for m in MD_LINK.finditer(line):
            raw = m.group(1)
            t = normalize_link_target(raw)
            if not t or t.startswith(("http://", "https://", "mailto:")):
                continue
            if t.startswith("#"):
                continue  # same-file anchor; checked later
            if not is_pathish(t) and not t.endswith((".md", ".mdc", ".yaml", ".yml", ".json")):
                continue
            resolved = resolve(src, t)
            all_refs.append((src, i, line.strip()[:200], t, resolved, "md-link"))
        for m in BT_ANY.finditer(line):
            raw = m.group(1).strip()
            # skip code snippets that aren't paths
            if " " in raw and not raw.startswith(("Read ", "Task(")):
                # maybe first token is path
                tok = raw.split()[0]
                if not is_pathish(tok):
                    continue
                raw = tok
            raw = normalize_link_target(raw)
            if not is_pathish(raw):
                continue
            # skip glob wildcards as directories
            resolved = resolve(src, raw)
            all_refs.append((src, i, line.strip()[:200], raw, resolved, "backtick"))

# also catch unquoted .cursor/ and openspec/ paths
BARE = re.compile(
    r"(?<![`(\w/])((?:\.cursor|openspec|temp)/[A-Za-z0-9_./\\-]+\.(?:mdc|md|ya?ml|json|xml|bsl))"
)
for src in SCOPE_FILES:
    try:
        text = src.read_text(encoding="utf-8")
    except Exception:
        continue
    for i, line in enumerate(text.splitlines(), 1):
        for m in BARE.finditer(line):
            t = m.group(1).replace("\\", "/")
            resolved = resolve(src, t)
            all_refs.append((src, i, line.strip()[:200], t, resolved, "bare"))

# dedupe by src+line+target
dedup = {}
for item in all_refs:
    src, i, quote, t, resolved, kind = item
    key = (str(src), i, t)
    if key not in dedup:
        dedup[key] = item

missing = []
temp_missing = []
ok = 0
wildcard = []
placeholder_refs = []
unresolved = []

for src, i, quote, t, resolved, kind in dedup.values():
    rel_src = src.relative_to(ROOT).as_posix()
    # wildcards
    if "*" in t or t.endswith("/") or t.endswith("/*.md") or t.endswith("/**"):
        wildcard.append((rel_src, i, t, quote, kind))
        continue
    if PLACEHOLDER.search(t):
        placeholder_refs.append((rel_src, i, t, quote, kind))
        # still check if directory prefix exists for temp
        if t.startswith("temp/"):
            temp_missing.append((rel_src, i, t, quote, kind, "placeholder-temp"))
        continue
    if resolved is None:
        unresolved.append((rel_src, i, t, quote, kind))
        continue
    # existence
    exists = resolved.exists()
    try:
        rel_tgt = resolved.relative_to(ROOT.resolve()).as_posix()
    except Exception:
        rel_tgt = str(resolved)
    if exists:
        ok += 1
        continue
    rec = (rel_src, i, t, rel_tgt, quote, kind)
    if t.startswith("temp/") or rel_tgt.startswith("temp/"):
        temp_missing.append(rec + ("runtime-temp",))
    else:
        missing.append(rec)

print("=== SCOPE FILES ===", len(SCOPE_FILES))
print("=== UNIQUE REFS ===", len(dedup))
print("=== OK ===", ok)
print("=== MISSING ===", len(missing))
print("=== TEMP ===", len(temp_missing))
print("=== UNRESOLVED ===", len(unresolved))
print("=== WILDCARD ===", len(wildcard))
print("=== PLACEHOLDER ===", len(placeholder_refs))

print("\n===== MISSING FILES =====")
for rec in sorted(missing, key=lambda x: (x[0], x[1])):
    print(f"{rec[0]}:{rec[1]}  target={rec[2]!r}  resolved={rec[3]!r}  kind={rec[5]}")
    print(f"    {rec[4][:180]}")

print("\n===== UNRESOLVED =====")
for rec in sorted(unresolved, key=lambda x: (x[0], x[1]))[:80]:
    print(f"{rec[0]}:{rec[1]}  target={rec[2]!r}  kind={rec[4]}")
    print(f"    {rec[3][:180]}")

print("\n===== TEMP (sample) =====")
for rec in sorted(temp_missing, key=lambda x: (x[0], x[1]))[:40]:
    print(f"{rec[0]}:{rec[1]}  target={rec[2]!r}")
