# -*- coding: utf-8 -*-
"""Strict kit-internal path existence audit. Writes UTF-8 JSON/text."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"c:\GitHub\1c-ai-development-kit-van")
OUT = ROOT / "temp" / "_ref_audit_out.txt"

SCOPE: list[Path] = []

def g(pat: str) -> None:
    SCOPE.extend(p for p in ROOT.glob(pat) if p.is_file())

g(".cursor/rules/*.mdc")
g(".cursor/commands/*.md")
g(".cursor/agents/*.md")
g(".cursor/docs/*.md")
g(".cursor/docs/templates/*.md")
g(".cursor/docs/casebooks/*.md")
g("openspec/specs/**/spec.md")
g("openspec/adrs/*.md")
SCOPE.append(ROOT / "AGENTS.md")
SCOPE.append(ROOT / "README.md")
SCOPE.append(ROOT / "openspec/glossary.md")

# skills: SKILL.md + templates + 1c-agent-patterns role files
for p in ROOT.glob(".cursor/skills/**/*.md"):
    rel = p.as_posix()
    if p.name == "SKILL.md":
        SCOPE.append(p)
    elif "/templates/" in rel.replace("\\", "/"):
        SCOPE.append(p)
    elif "/1c-agent-patterns/" in rel.replace("\\", "/") and p.suffix == ".md":
        SCOPE.append(p)

# unique
seen = set()
files = []
for p in SCOPE:
    r = p.resolve()
    if r not in seen:
        seen.add(r)
        files.append(p)

# Known runtime / generated / kit-absent (note, don't count as broken kit file)
KIT_ABSENT_OK = {
    "openspec/project.md",
    "openspec/config.yaml",
    "openspec/specs/architecture.md",
}

# Example / template paths — not real files
EXAMPLE_RE = re.compile(
    r"(?:"
    r"src/cf/|"
    r"src/cfe/|"
    r"path/to/|"
    r"Catalogs/.*/Ext/|"
    r"<name>|<slug>|<тип>|<scope>|<change>|"
    r"YYYY|MM-DD|"
    r"\*\.|"
    r"…|\.\.\."
    r")"
)

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BT = re.compile(r"`([^`]+)`")
BARE_KIT = re.compile(
    r"(?<![`(\w])((?:\.cursor|openspec)/[A-Za-z0-9_./\-]+(?:\.(?:mdc|md|ya?ml|json))?)"
)

TRAIL = re.compile(r"[.,;:)\]\"']+$")

def clean(s: str) -> str:
    s = s.strip().split()[0] if s.strip() else s
    s = s.split("#")[0].strip()
    s = s.strip("<>")
    s = TRAIL.sub("", s)
    s = s.replace("\\", "/")
    return s

def alias_resolve(src: Path, t: str) -> Path | None:
    t = t.replace("\\", "/")
    if t.startswith(".cursor/") or t.startswith("openspec/") or t.startswith("temp/"):
        return ROOT / t
    if t in {"AGENTS.md", "README.md"}:
        return ROOT / t
    # relative from file
    if t.startswith("../") or t.startswith("./"):
        return (src.parent / t).resolve()
    # well-known aliases used without .cursor/
    ALIAS = {
        "review/SKILL.md": ".cursor/skills/review/SKILL.md",
        "1c-agent-delegation.mdc": ".cursor/rules/1c-agent-delegation.mdc",
        "model-selection.mdc": ".cursor/rules/model-selection.mdc",
        "chat-output-budget.mdc": ".cursor/rules/chat-output-budget.mdc",
        "chat-output-budget-full.mdc": ".cursor/rules/chat-output-budget-full.mdc",
        "1c-halt-triggers.mdc": ".cursor/rules/1c-halt-triggers.mdc",
        "1c-writer-pipeline.mdc": ".cursor/rules/1c-writer-pipeline.mdc",
        "1c-xml-write-guard.mdc": ".cursor/rules/1c-xml-write-guard.mdc",
        "1c-no-metadata-creation.mdc": ".cursor/rules/1c-no-metadata-creation.mdc",
        "verify-user-communication.mdc": ".cursor/rules/verify-user-communication.mdc",
        "tool-name-guard.mdc": ".cursor/rules/tool-name-guard.mdc",
        "gate-dispatcher.mdc": ".cursor/rules/gate-dispatcher.mdc",
        "session-discipline.mdc": ".cursor/rules/session-discipline.mdc",
        "command-skill-gate.mdc": ".cursor/rules/command-skill-gate.mdc",
        "command-session-persistence.mdc": ".cursor/rules/command-session-persistence.mdc",
        "context-strategy-gate.mdc": ".cursor/rules/context-strategy-gate.mdc",
        "model-adaptation.mdc": ".cursor/rules/model-adaptation.mdc",
        "model-grok4.mdc": ".cursor/rules/model-grok4.mdc",
        "model-fable5.mdc": ".cursor/rules/model-fable5.mdc",
        "model-gpt56.mdc": ".cursor/rules/model-gpt56.mdc",
        "model-opus5.mdc": ".cursor/rules/model-opus5.mdc",
        "brief-card.md": ".cursor/docs/templates/brief-card.md",
        "decision-block.md": ".cursor/docs/templates/decision-block.md",
        "opsx-output-style.md": ".cursor/docs/opsx-output-style.md",
        "chat-lexicon.md": ".cursor/docs/chat-lexicon.md",
        "marker-canon.md": ".cursor/docs/marker-canon.md",
        "1c-coding-standards.md": ".cursor/docs/1c-coding-standards.md",
        "bsl-antipatterns.mdc": ".cursor/rules/bsl-antipatterns.mdc",
        "project.md": "openspec/project.md",
        "glossary.md": "openspec/glossary.md",
    }
    if t in ALIAS:
        return ROOT / ALIAS[t]
    if t.endswith(".mdc") and "/" not in t:
        return ROOT / ".cursor/rules" / t
    if t.startswith("skills/"):
        return ROOT / ".cursor" / t
    if t.startswith("rules/"):
        return ROOT / ".cursor" / t
    if t.startswith("docs/"):
        return ROOT / ".cursor" / t
    if t.startswith("agents/"):
        return ROOT / ".cursor" / t
    if t.startswith("commands/"):
        return ROOT / ".cursor" / t
    if t.startswith("templates/") and "skills" in src.as_posix().replace("\\", "/"):
        return src.parent / t
    # relative file next to source
    if "/" in t and not t.startswith("/"):
        cand = (src.parent / t)
        if cand.exists():
            return cand.resolve()
        # from .cursor/skills/foo/SKILL.md linking to templates/x.md
        cand2 = src.parent / t
        return cand2.resolve()
    if t == "SKILL.md":
        return src.parent / t
    return None

def is_kit_path(t: str) -> bool:
    if not t:
        return False
    if t.startswith(("http://", "https://", "mailto:")):
        return False
    if t.startswith("temp/"):
        return True
    if t.startswith(".cursor/") or t.startswith("openspec/"):
        return True
    if t in {"AGENTS.md", "README.md"}:
        return True
    if t.startswith("../") or t.startswith("./"):
        return True
    if t.endswith(".mdc"):
        return True
    if t.startswith(("skills/", "rules/", "docs/", "agents/", "commands/", "templates/")):
        return True
    if t.endswith((".md", ".yaml", ".yml")) and ("/" in t or t in {"SKILL.md", "proposal.md"}):
        return True
    return False

rows = []
for src in files:
    text = src.read_text(encoding="utf-8")
    rel_src = src.relative_to(ROOT).as_posix()
    for i, line in enumerate(text.splitlines(), 1):
        cands = []
        for m in MD_LINK.finditer(line):
            cands.append(("md-link", clean(m.group(1))))
        for m in BT.finditer(line):
            raw = m.group(1).strip()
            # first token if command-like
            tok = raw.split()[0] if raw else raw
            tok = clean(tok)
            cands.append(("backtick", tok))
        for m in BARE_KIT.finditer(line):
            cands.append(("bare", clean(m.group(1))))
        seen_t = set()
        for kind, t in cands:
            if not t or t in seen_t:
                continue
            seen_t.add(t)
            if not is_kit_path(t):
                continue
            if t.startswith("#"):
                continue
            if "*" in t or t.endswith("/"):
                rows.append(dict(src=rel_src, line=i, target=t, kind=kind, status="wildcard-or-dir", quote=line.strip()[:220]))
                continue
            if EXAMPLE_RE.search(t) and not t.startswith(".cursor/") and not t.startswith("openspec/specs/") and not t.startswith("openspec/adrs/"):
                # still check .cursor and openspec/specs even if they have YYYY in name? skip examples
                if t.startswith("src/") or "path/to" in t or "<" in t:
                    rows.append(dict(src=rel_src, line=i, target=t, kind=kind, status="example", quote=line.strip()[:220]))
                    continue
            resolved = alias_resolve(src, t)
            if resolved is None:
                rows.append(dict(src=rel_src, line=i, target=t, kind=kind, status="unresolved", quote=line.strip()[:220]))
                continue
            try:
                rel_tgt = Path(resolved).resolve().relative_to(ROOT.resolve()).as_posix()
            except Exception:
                rel_tgt = str(resolved)
            exists = Path(resolved).exists()
            status = "ok" if exists else "missing"
            if not exists:
                if t.startswith("temp/") or rel_tgt.startswith("temp/"):
                    status = "temp-absent"
                elif rel_tgt in KIT_ABSENT_OK or t in KIT_ABSENT_OK:
                    status = "kit-absent-expected"
                elif t.startswith("src/") or rel_tgt.startswith("src/"):
                    status = "example"
            rows.append(dict(src=rel_src, line=i, target=t, resolved=rel_tgt, kind=kind, status=status, quote=line.strip()[:220]))

# collapse missing unique
from collections import Counter
st = Counter(r["status"] for r in rows)

missing = [r for r in rows if r["status"] == "missing"]
unresolved = [r for r in rows if r["status"] == "unresolved"]
temp_abs = [r for r in rows if r["status"] == "temp-absent"]
kit_abs = [r for r in rows if r["status"] == "kit-absent-expected"]

lines_out = []
def w(s=""):
    lines_out.append(s)

w(f"SCOPE_FILES={len(files)}")
w(f"REFS={len(rows)}")
w(f"STATUS={dict(st)}")
w("")
w("========== MISSING ==========")
for r in sorted(missing, key=lambda x: (x["src"], x["line"])):
    w(f"{r['src']}:{r['line']}  [{r['kind']}] {r['target']}  -> {r.get('resolved','')}")
    w(f"    {r['quote']}")

w("")
w("========== UNRESOLVED (filename-only / ambiguous) ==========")
# filter noise: skip proposal.md, design.md, tasks.md as change-relative
noise = {"proposal.md", "design.md", "tasks.md", "debug.md", "spec.md", "SKILL.md"}
unr_f = [r for r in unresolved if r["target"] not in noise and not r["target"].endswith("/spec.md")]
w(f"count_raw={len(unresolved)} filtered={len(unr_f)}")
for r in sorted(unr_f, key=lambda x: (x["src"], x["line"])):
    w(f"{r['src']}:{r['line']}  [{r['kind']}] {r['target']}")
    w(f"    {r['quote']}")

w("")
w("========== KIT-ABSENT-EXPECTED ==========")
for r in sorted(kit_abs, key=lambda x: (x["src"], x["line"])):
    w(f"{r['src']}:{r['line']}  {r['target']}")

w("")
w("========== TEMP-ABSENT unique targets ==========")
ut = sorted({r["target"] for r in temp_abs})
for t in ut:
    w(t)

OUT.write_text("\n".join(lines_out), encoding="utf-8")
print("wrote", OUT, "missing", len(missing), "unresolved_f", len(unr_f), "temp", len(temp_abs))
