# -*- coding: utf-8 -*-
"""Precise framework pointer audit. No edits to kit sources."""
from __future__ import annotations

import json
import re
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

MD_LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
PATH_TOKEN = re.compile(
    r"(?:Read\s+)?`((?:\.cursor/|openspec/)[^`\n]+)`"
    r"|(?<!\()(?<!\[]\()(?<!\[)\b((?:\.cursor/|openspec/)[A-Za-z0-9_./\-]+(?:\.[A-Za-z0-9]+)?)"
)

PLACEHOLDER = re.compile(r"(YYYY|<[^>]+>|\{[^}]+\}|\*)")

ARTIFACT_NAMES = {
    "proposal.md",
    "design.md",
    "tasks.md",
    "debug.md",
    "spec.md",
    "schema.yaml",
    ".openspec.yaml",
    ".gate-override.yaml",
    "openspec.yaml",
    "Form.xml",
    "Template.xml",
    "Rights.xml",
    "Configuration.xml",
}

SKIP_EXT = {".bsl", ".xml", ".pff"}


def collect_sources() -> list[Path]:
    files, seen = [], set()
    for g in SOURCE_GLOBS:
        for p in ROOT.glob(g):
            if p.is_file():
                rp = p.resolve()
                if rp not in seen:
                    seen.add(rp)
                    files.append(p)
    return sorted(files)


def always_apply_names() -> set[str]:
    out = set()
    for p in (ROOT / ".cursor/rules").glob("*.mdc"):
        head = p.read_text(encoding="utf-8", errors="replace")[:800]
        if re.search(r"^alwaysApply:\s*true", head, re.M | re.I):
            out.add(p.name)
    return out


def clean_target(raw: str) -> str:
    t = (raw or "").strip().strip("`").strip()
    if not t:
        return t
    t = t.split()[0]
    t = t.split("#")[0]
    t = t.replace("\\", "/").rstrip(".,;:)")
    return t


def should_skip(t: str) -> bool:
    if not t:
        return True
    if t.startswith(("http://", "https://", "mailto:", "#")):
        return True
    if t.endswith("/") or "*" in t:
        return True
    if PLACEHOLDER.search(t) or "YYYY" in t or "MM-DD" in t:
        return True
    n = t.replace("\\", "/")
    name = Path(t).name
    if name in ARTIFACT_NAMES and ".cursor/" not in n:
        if "openspec/project.md" in n or n.endswith("/project.md") or n == "project.md":
            return False
        if "openspec/changes/" in n:
            return True
        if name in {"Form.xml", "Template.xml", "Rights.xml", "Configuration.xml"}:
            return True
        if name in {"proposal.md", "design.md", "tasks.md", "debug.md", "spec.md"}:
            return True
    if Path(t).suffix.lower() in SKIP_EXT and not n.startswith(".cursor/"):
        return True
    return False


def resolve_candidates(raw: str, src: Path) -> list[Path]:
    t = clean_target(raw)
    if not t:
        return []
    cands = [
        src.parent / t,
        ROOT / t,
    ]
    if t.startswith("./"):
        cands.append(src.parent / t[2:])
    if not t.startswith((".cursor/", "openspec/", "temp/")):
        cands.extend(
            [
                ROOT / ".cursor" / t,
                ROOT / ".cursor/rules" / Path(t).name,
                ROOT / ".cursor/docs" / Path(t).name,
                ROOT / ".cursor/docs/templates" / Path(t).name,
                ROOT / ".cursor/agents" / Path(t).name,
                ROOT / ".cursor/commands" / Path(t).name,
                ROOT / ".cursor/skills" / t,
            ]
        )
        if t.endswith("SKILL.md") and "/" in t:
            cands.append(ROOT / ".cursor/skills" / t)
    return cands


def exists_resolved(cands: list[Path]) -> tuple[bool, str | None]:
    for p in cands:
        try:
            rp = p.resolve()
        except Exception:
            rp = p
        if rp.exists() and rp.is_file():
            try:
                return True, str(rp.relative_to(ROOT)).replace("\\", "/")
            except Exception:
                return True, str(rp)
        if rp.exists() and rp.is_dir() and (rp / "SKILL.md").exists():
            try:
                return True, str((rp / "SKILL.md").relative_to(ROOT)).replace("\\", "/")
            except Exception:
                return True, str(rp / "SKILL.md")
    return False, None


def classify_missing(t: str) -> str:
    n = t.replace("\\", "/")
    if "openspec/project.md" in n or n.endswith("/project.md"):
        return "expected-kit-absent"
    if "openspec/knowledge/" in n or n.endswith("_index.yaml") or n.endswith("_taxonomy.yaml"):
        return "expected-kit-absent"
    if n.startswith("temp/") or "/temp/" in n:
        return "runtime-generated"
    return "broken"


def main():
    sources = collect_sources()
    aa = always_apply_names()
    findings = []

    for src in sources:
        rel = str(src.relative_to(ROOT)).replace("\\", "/")
        lines = src.read_text(encoding="utf-8", errors="replace").splitlines()
        seen_line = set()
        for i, line in enumerate(lines, 1):
            targets = []
            for m in MD_LINK.finditer(line):
                targets.append((m.group(2).strip(), "md-link"))
            for m in PATH_TOKEN.finditer(line):
                raw = m.group(1) or m.group(2)
                targets.append((raw, "path-token"))
            for raw, kind in targets:
                t = clean_target(raw)
                if should_skip(t) and "openspec/project.md" not in t.replace("\\", "/"):
                    continue
                if t.startswith(("http://", "https://", "mailto:")):
                    continue
                if not Path(t).suffix and not t.endswith("SKILL.md"):
                    pdir = ROOT / t if t.startswith((".cursor/", "openspec/")) else None
                    if pdir and pdir.exists() and pdir.is_dir():
                        continue
                    if Path(t).suffix == "":
                        continue
                key = (i, t)
                if key in seen_line:
                    continue
                seen_line.add(key)
                ok, found = exists_resolved(resolve_candidates(raw, src))
                status = "ok" if ok else classify_missing(t)
                if status != "ok":
                    findings.append(
                        {
                            "src": rel,
                            "line": i,
                            "raw": t,
                            "kind": kind,
                            "status": status,
                            "found": found,
                            "snippet": line.strip()[:200],
                        }
                    )

    broken = [f for f in findings if f["status"] == "broken"]
    expected = [f for f in findings if f["status"] == "expected-kit-absent"]
    runtime = [f for f in findings if f["status"] == "runtime-generated"]

    uniq = {}
    for f in broken:
        uniq[(f["src"], f["line"], f["raw"])] = f
    broken = sorted(uniq.values(), key=lambda x: (x["src"], x["line"]))

    out = {
        "source_count": len(sources),
        "always_apply": sorted(aa),
        "broken_count": len(broken),
        "expected_missing_count": len(expected),
        "runtime_count": len(runtime),
        "broken": broken,
        "expected_sample": expected[:40],
        "runtime_sample": runtime[:20],
    }
    (ROOT / "temp/_link-audit2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"sources={len(sources)} broken={len(broken)} expected-absent={len(expected)} runtime={len(runtime)}")
    print("ALWAYS_APPLY:", ", ".join(sorted(aa)))
    print("--- BROKEN ---")
    for f in broken:
        print(f"{f['src']}:{f['line']}\t{f['raw']}\t{f['kind']}")


if __name__ == "__main__":
    main()
