# -*- coding: utf-8 -*-
"""Extract and validate file/section pointers from kit framework sources."""
from __future__ import annotations

import os
import re
import json
from pathlib import Path

ROOT = Path(r"c:\GitHub\1c-ai-development-kit-van")

SOURCE_GLOBS = [
    "AGENTS.md",
    "README.md",
    ".cursor/rules/*.mdc",
    ".cursor/commands/*.md",
    ".cursor/skills/**/SKILL.md",
    ".cursor/skills/**/templates/*.md",
    ".cursor/agents/*.md",
    ".cursor/docs/*.md",
    ".cursor/docs/templates/*.md",
    ".cursor/skills/1c-agent-patterns/*.md",
]

SKIP_URL = re.compile(r"^(https?://|mailto:|#)")
# Markdown links [text](target)
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
# Backtick-enclosed paths that look like files
BT_PATH = re.compile(
    r"`((?:\.cursor/|openspec/|temp/|docs/)[^`\s]+|(?:[A-Za-z0-9_\-./]+)\.(?:mdc|md|yaml|yml|json|bsl|xml)|AGENTS\.md|README\.md)`"
)
# Read <path>
READ_REF = re.compile(
    r"(?:Read|читать|прочитать)\s+`?((?:\.cursor/|openspec/)[^`\s]+|[A-Za-z0-9_\-./]+\.(?:mdc|md))`?",
    re.I,
)
# file § SECTION
SEC_REF = re.compile(
    r"`?((?:[\w.\-/]+\.(?:mdc|md))|(?:\.cursor/[\w.\-/]+\.(?:mdc|md)))`?\s*§+\s*`?([^`\n,;:)\]}]+?)`?(?=\s*(?:[,;:)\]}]|$|\s{2,}| — | – ))",
)

FILE_EXT = {".mdc", ".md", ".yaml", ".yml", ".json"}

# Things that look like files but are not repo files
FALSE_POS = {
    "Form.xml",
    "Template.xml",
    "Rights.xml",
    "Configuration.xml",
    "proposal.md",
    "design.md",
    "tasks.md",
    "debug.md",
    "schema.yaml",
    ".openspec.yaml",
    ".gate-override.yaml",
    "openspec.yaml",
    "project.md",  # may be missing in kit — special
}

ALWAYS_APPLY_RULES = set()


def collect_sources() -> list[Path]:
    files = []
    for g in SOURCE_GLOBS:
        files.extend(ROOT.glob(g))
    # unique, files only
    out = []
    seen = set()
    for p in files:
        if p.is_file() and p.resolve() not in seen:
            seen.add(p.resolve())
            out.append(p)
    return sorted(out)


def parse_always_apply():
    for p in (ROOT / ".cursor/rules").glob("*.mdc"):
        text = p.read_text(encoding="utf-8", errors="replace")[:800]
        if re.search(r"^alwaysApply:\s*true", text, re.M):
            ALWAYS_APPLY_RULES.add(p.name)


def try_resolve(raw: str, src: Path) -> list[Path]:
    """Return candidate absolute paths to try."""
    t = raw.strip().strip("`").strip()
    t = t.split("#")[0].strip()
    t = t.replace("\\", "/")
    # drop trailing punctuation
    t = t.rstrip(".,;:)")
    if not t or SKIP_URL.match(t):
        return []
    # skip globs
    if "*" in t or t.endswith("/"):
        return []
    cands = []

    def add(p: Path):
        cands.append(p)

    # repo-relative if starts with known roots
    if t.startswith(".cursor/") or t.startswith("openspec/") or t.startswith("temp/") or t in (
        "AGENTS.md",
        "README.md",
    ):
        add(ROOT / t)
    elif t.startswith("docs/") and not t.startswith(".cursor/"):
        # sometimes docs/ means .cursor/docs/
        add(ROOT / ".cursor" / t)
        add(ROOT / t)

    # relative to source file
    add((src.parent / t).resolve())

    # relative to .cursor/
    add(ROOT / ".cursor" / t)

    # if only filename
    name = Path(t).name
    if name.endswith(".mdc"):
        add(ROOT / ".cursor/rules" / name)
    if name.endswith(".md"):
        add(ROOT / ".cursor/docs" / name)
        add(ROOT / ".cursor/docs/templates" / name)
        add(ROOT / ".cursor/agents" / name)
        add(ROOT / ".cursor/commands" / name)

    # skills shorthand like review/SKILL.md
    if "/" in t and not t.startswith("."):
        add(ROOT / ".cursor/skills" / t)
        add(ROOT / ".cursor" / t)

    # de-dupe
    uniq = []
    seen = set()
    for p in cands:
        try:
            rp = p.resolve()
        except Exception:
            continue
        if rp not in seen:
            seen.add(rp)
            uniq.append(p)
    return uniq


def exists_any(cands: list[Path]) -> tuple[bool, str | None]:
    for p in cands:
        try:
            if p.exists() and p.is_file():
                return True, str(p.relative_to(ROOT)).replace("\\", "/")
        except Exception:
            if p.exists() and p.is_file():
                return True, str(p)
    return False, None


def looks_like_file_ref(raw: str) -> bool:
    t = raw.strip().strip("`")
    if not t or "*" in t:
        return False
    if t.startswith("http"):
        return False
    # skip too generic artifact names without directory when they're clearly change artifacts
    low = t.lower()
    if t in FALSE_POS:
        return False
    # skip code identifiers
    if t.endswith(".bsl") and "/" not in t and "\\" not in t:
        return False
    ext = Path(t).suffix.lower()
    if ext in FILE_EXT or t.endswith("SKILL.md"):
        return True
    if t.startswith(".cursor/") or t.startswith("openspec/"):
        # directories ok to skip unless they have extension
        if Path(t).suffix:
            return True
        # directory references — skip existence as file
        return False
    return False


def extract_from_file(src: Path) -> dict:
    text = src.read_text(encoding="utf-8", errors="replace")
    rel = str(src.relative_to(ROOT)).replace("\\", "/")
    links = []  # (line, raw, kind)
    lines = text.splitlines()
    # markdown links
    for i, line in enumerate(lines, 1):
        for m in MD_LINK.finditer(line):
            target = m.group(2).strip()
            if SKIP_URL.match(target) or target.startswith("#"):
                continue
            links.append((i, target, "md-link", line.strip()[:200]))
        for m in BT_PATH.finditer(line):
            target = m.group(1)
            links.append((i, target, "backtick", line.strip()[:200]))
        for m in READ_REF.finditer(line):
            target = m.group(1)
            links.append((i, target, "read", line.strip()[:200]))
        for m in SEC_REF.finditer(line):
            links.append((i, f"{m.group(1)} § {m.group(2).strip()}", "section-combo", line.strip()[:240]))
    return {"file": rel, "links": links, "text": text, "lines": lines}


def main():
    parse_always_apply()
    sources = collect_sources()
    all_refs = []
    section_refs = []

    for src in sources:
        data = extract_from_file(src)
        seen_here = set()
        for line, raw, kind, snippet in data["links"]:
            key = (line, raw, kind)
            if key in seen_here:
                continue
            seen_here.add(key)
            if kind == "section-combo":
                section_refs.append(
                    {
                        "src": data["file"],
                        "line": line,
                        "raw": raw,
                        "snippet": snippet,
                    }
                )
                # also check file part
                filepart = raw.split(" § ")[0].strip()
                if looks_like_file_ref(filepart):
                    cands = try_resolve(filepart, src)
                    ok, found = exists_any(cands)
                    all_refs.append(
                        {
                            "src": data["file"],
                            "line": line,
                            "raw": filepart,
                            "kind": "section-file",
                            "ok": ok,
                            "found": found,
                            "snippet": snippet,
                        }
                    )
                continue
            if not looks_like_file_ref(raw):
                continue
            cands = try_resolve(raw, src)
            ok, found = exists_any(cands)
            all_refs.append(
                {
                    "src": data["file"],
                    "line": line,
                    "raw": raw,
                    "kind": kind,
                    "ok": ok,
                    "found": found,
                    "snippet": snippet[:180],
                }
            )

    broken = [r for r in all_refs if not r["ok"]]
    # extra: mention of files that look like paths but failed
    out = {
        "source_count": len(sources),
        "ref_count": len(all_refs),
        "broken_count": len(broken),
        "always_apply": sorted(ALWAYS_APPLY_RULES),
        "sources": [str(p.relative_to(ROOT)).replace("\\", "/") for p in sources],
        "broken": broken,
        "section_refs": section_refs,
        "ok_sample": [r for r in all_refs if r["ok"]][:5],
    }
    (ROOT / "temp/_link-audit.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"sources={len(sources)} refs={len(all_refs)} broken={len(broken)} sections={len(section_refs)}")
    print("ALWAYS_APPLY:", ", ".join(sorted(ALWAYS_APPLY_RULES)))
    print("--- BROKEN ---")
    for r in broken:
        print(f"{r['src']}:{r['line']}\t{r['raw']}\t{r['kind']}")


if __name__ == "__main__":
    main()
