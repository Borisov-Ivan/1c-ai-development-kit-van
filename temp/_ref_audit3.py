# -*- coding: utf-8 -*-
"""Resolve kit shorthand paths; report only true missing after alias search."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"c:\GitHub\1c-ai-development-kit-van")
OUT = ROOT / "temp" / "_ref_true_missing.txt"

SCOPE: list[Path] = []
def add(pat):
    SCOPE.extend(p for p in ROOT.glob(pat) if p.is_file())
add(".cursor/rules/*.mdc")
add(".cursor/commands/*.md")
add(".cursor/agents/*.md")
add(".cursor/docs/*.md")
add(".cursor/docs/templates/*.md")
add(".cursor/docs/casebooks/*.md")
add("openspec/specs/**/spec.md")
add("openspec/adrs/*.md")
SCOPE += [ROOT/"AGENTS.md", ROOT/"README.md", ROOT/"openspec/glossary.md"]
for p in ROOT.glob(".cursor/skills/**/*.md"):
    rel = p.as_posix().replace("\\", "/")
    if p.name == "SKILL.md" or "/templates/" in rel or "/1c-agent-patterns/" in rel:
        SCOPE.append(p)

seen=set(); files=[]
for p in SCOPE:
    r=p.resolve()
    if r not in seen:
        seen.add(r); files.append(p)

SKILL_DIRS = [p.name for p in (ROOT/".cursor/skills").iterdir() if p.is_dir()]
RULE_FILES = {p.name for p in (ROOT/".cursor/rules").glob("*.mdc")}
DOC_FILES = {p.name for p in (ROOT/".cursor/docs").glob("*.md")}
AGENT_FILES = {p.name for p in (ROOT/".cursor/agents").glob("*.md")}

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BT = re.compile(r"`([^`]+)`")
BARE = re.compile(r"(?<![`(\w])((?:\.cursor|openspec)/[A-Za-z0-9_./\-]+(?:\.(?:mdc|md|ya?ml|json))?)")
TRAIL = re.compile(r"[.,;:)\]\"']+$")

SKIP_SUBSTR = (
    "YYYY", "MM-DD", "<name>", "<slug>", "<тип>", "<scope>", "<id>",
    "<capability>", "<domain>", "<date>", "<archive", "<change",
    "src/cf/", "src/cfe/", "path/to/", "…", "...", "Глава ",
    "std-NN-", "my-change", "do2-roli", "pavlik",
)

def clean(s: str) -> str:
    s = s.strip()
    if not s: return s
    s = s.split("#")[0].strip()
    s = TRAIL.sub("", s)
    return s.replace("\\", "/")

def try_exist(cands: list[Path]) -> Path | None:
    for c in cands:
        try:
            if c.exists():
                return c
        except Exception:
            continue
    return None

def candidates(src: Path, t: str) -> list[Path]:
    t = t.replace("\\", "/")
    out = []
    # repo-root
    if t.startswith(".cursor/") or t.startswith("openspec/") or t.startswith("temp/") or t in {"AGENTS.md","README.md"}:
        out.append(ROOT / t)
    if t.startswith("../") or t.startswith("./"):
        out.append((src.parent / t).resolve())
    # filename .mdc
    if t.endswith(".mdc") and "/" not in t:
        out.append(ROOT / ".cursor/rules" / t)
    # skill shorthand foo/SKILL.md or foo/bar.md
    parts = t.split("/")
    if parts and parts[0] in SKILL_DIRS:
        out.append(ROOT / ".cursor/skills" / t)
    if t.startswith("1c-") and "/" in t:
        out.append(ROOT / ".cursor/skills" / t)
    if t.startswith("openspec-") and "/" in t:
        out.append(ROOT / ".cursor/skills" / t)
    if t.startswith("review/"):
        out.append(ROOT / ".cursor/skills" / t)
    if t.startswith("stop-slop/"):
        out.append(ROOT / ".cursor/skills" / t)
    if t.startswith("context-strategy/"):
        out.append(ROOT / ".cursor/skills" / t)
    if t.startswith("session-"):
        out.append(ROOT / ".cursor/skills" / t)
    # docs shorthand
    if t in DOC_FILES:
        out.append(ROOT / ".cursor/docs" / t)
    if t.startswith("docs/"):
        out.append(ROOT / ".cursor" / t)
        out.append(ROOT / t)
    # templates from skill
    if t.startswith("templates/"):
        out.append(src.parent / t)
        out.append(src.parent.parent / t)
        # verify templates
        out.append(ROOT / ".cursor/skills/openspec-verify-change" / t)
        out.append(ROOT / ".cursor/skills/openspec-explain" / t)
        out.append(ROOT / ".cursor/docs" / t)
        out.append(ROOT / ".cursor/docs/templates" / t.replace("templates/", ""))
    if t.startswith("fixtures/"):
        out.append(src.parent / t)
        out.append(src.parent.parent / t)
        out.append(ROOT / ".cursor/skills/openspec-overview" / t)
        out.append(ROOT / ".cursor/skills/openspec-explain" / t)
    # agents
    if t.startswith("agents/"):
        out.append(ROOT / ".cursor" / t)
    if t.startswith("rules/"):
        out.append(ROOT / ".cursor" / t)
    if t.startswith("skills/"):
        out.append(ROOT / ".cursor" / t)
    if t.startswith("commands/"):
        out.append(ROOT / ".cursor" / t)
    # relative next to src
    if "/" in t and not t.startswith((".cursor/", "openspec/", "temp/", "http")):
        out.append(src.parent / t)
        # sibling skill
        if "skills" in src.as_posix():
            # from templates/ go up
            out.append(src.parent.parent / t)
            out.append(src.parent.parent.parent / t)
    if t == "SKILL.md":
        # from command file, SKILL is in matching skill dir — don't invent
        out.append(src.parent / t)
    return out

def is_interesting(t: str) -> bool:
    if not t or t.startswith(("http://","https://","mailto:","#")):
        return False
    if "*" in t or t.endswith("/"):
        return False
    if any(s in t for s in SKIP_SUBSTR):
        return False
    if t.startswith(".cursor/") or t.startswith("openspec/") or t.startswith("temp/"):
        return True
    if t.endswith((".md",".mdc",".yaml",".yml")):
        return True
    if t.startswith(("skills/","rules/","docs/","agents/","commands/","templates/","fixtures/")):
        return True
    if "/" in t and t.split("/")[0] in SKILL_DIRS:
        return True
    if t.endswith(".mdc"):
        return True
    return False

RUNTIME_PREFIX = (
    "temp/",
    "openspec/knowledge/",
    "openspec/project.md",
    "openspec/config.yaml",
    "openspec/specs/architecture.md",
    "openspec/reports/",
    "openspec/docs/",
)

rows=[]
for src in files:
    rel_src = src.relative_to(ROOT).as_posix()
    text = src.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        items=[]
        for m in MD_LINK.finditer(line):
            items.append(("md-link", clean(m.group(1))))
        for m in BT.finditer(line):
            raw=m.group(1).strip()
            tok=clean(raw.split()[0] if raw else raw)
            items.append(("backtick", tok))
        for m in BARE.finditer(line):
            items.append(("bare", clean(m.group(1))))
        seen_t=set()
        for kind,t in items:
            if not t or t in seen_t: continue
            seen_t.add(t)
            if not is_interesting(t): continue
            cands = candidates(src, t)
            found = try_exist(cands)
            if found:
                continue
            # classify
            status="missing"
            if t.startswith("temp/") or any(str(c).replace("\\","/").find("/temp/")>=0 for c in cands[:1]):
                status="temp"
            if t.startswith(RUNTIME_PREFIX) or any(t.startswith(p) for p in RUNTIME_PREFIX):
                status="runtime-expected"
            if t in {"proposal.md","design.md","tasks.md","debug.md","spec.md","SKILL.md"}:
                status="generic-name"
            if t.startswith("reports/"):
                status="change-runtime"
            rows.append((status, rel_src, i, kind, t, line.strip()[:200]))

from collections import Counter
c=Counter(r[0] for r in rows)
lines=["STATUS "+str(dict(c)), ""]
for status in ["missing","runtime-expected","temp","change-runtime","generic-name"]:
    subset=[r for r in rows if r[0]==status]
    lines.append(f"===== {status} n={len(subset)} =====")
    for r in sorted(subset, key=lambda x:(x[1],x[2])):
        lines.append(f"{r[1]}:{r[2]}  [{r[3]}] {r[4]}")
        lines.append(f"    {r[5]}")
    lines.append("")

OUT.write_text("\n".join(lines), encoding="utf-8")
print("wrote", OUT, dict(c))
