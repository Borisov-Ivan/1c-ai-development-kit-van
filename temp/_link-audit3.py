# -*- coding: utf-8 -*-
"""Full pointer integrity: md-links, bare files, sections, map, orphans."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"c:\GitHub\1c-ai-development-kit-van")

SRC_GLOBS = [
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
BARE_FILE = re.compile(
    r"`([A-Za-z0-9_./\-]+\.(?:mdc|md|yaml|yml|json))`"
)
READ_FILE = re.compile(
    r"(?:Read|читать)\s+`?([A-Za-z0-9_./\-]+\.(?:mdc|md))`?",
    re.I,
)
SEC_COMBO = re.compile(
    r"`?([A-Za-z0-9_./\-]+\.(?:mdc|md))`?\s*§+\s*`?([^`\n,;:)\]}]{1,80})`?"
)
STEP_REF = re.compile(
    r"`?([A-Za-z0-9_./\-]*SKILL\.md|[A-Za-z0-9_./\-]+\.md)`?[^.\n]{0,40}шаг(?:а|е|у)?\s+(\d+\.\d+)",
    re.I,
)

PLACEHOLDER = re.compile(r"(YYYY|<[^>]+>|\{[^}]+\}|\*|NNNN|MM-DD)")

SKIP_NAMES = {
    "proposal.md",
    "design.md",
    "tasks.md",
    "debug.md",
    "spec.md",
    "Form.xml",
    "schema.yaml",
    ".openspec.yaml",
    ".gate-override.yaml",
}

EXPECTED_ABSENT = {
    "openspec/project.md",
    "openspec/config.yaml",
    "openspec/specs/architecture.md",
}


def sources() -> list[Path]:
    files, seen = [], set()
    for g in SRC_GLOBS:
        for p in ROOT.glob(g):
            if p.is_file() and p.resolve() not in seen:
                seen.add(p.resolve())
                files.append(p)
    return sorted(files)


def always_apply() -> set[str]:
    out = set()
    for p in (ROOT / ".cursor/rules").glob("*.mdc"):
        head = p.read_text(encoding="utf-8", errors="replace")[:900]
        if re.search(r"^alwaysApply:\s*true", head, re.M | re.I):
            out.add(p.name)
    return out


def clean(raw: str) -> str:
    t = (raw or "").strip().strip("`").strip()
    t = t.split()[0] if t else t
    t = t.split("#")[0].replace("\\", "/").rstrip(".,;:)")
    return t


def skip_target(t: str) -> bool:
    if not t or t.startswith(("http://", "https://", "mailto:", "#")):
        return True
    if t.endswith("/") or "*" in t:
        return True
    if PLACEHOLDER.search(t) or "YYYY" in t:
        return True
    name = Path(t).name
    if name in SKIP_NAMES and ".cursor/" not in t:
        return True
    return False


def candidates(raw: str, src: Path) -> list[Path]:
    t = clean(raw)
    if not t:
        return []
    name = Path(t).name
    cands = [src.parent / t, ROOT / t]
    if t.startswith("./"):
        cands.append(src.parent / t[2:])
    cands.extend(
        [
            ROOT / ".cursor" / t,
            ROOT / ".cursor/rules" / name,
            ROOT / ".cursor/docs" / name,
            ROOT / ".cursor/docs/templates" / name,
            ROOT / ".cursor/docs/casebooks" / name,
            ROOT / ".cursor/docs/standard" / name,
            ROOT / ".cursor/docs/antipatterns" / name,
            ROOT / ".cursor/agents" / name,
            ROOT / ".cursor/commands" / name,
            ROOT / ".cursor/skills" / t,
            ROOT / ".cursor/skills" / name,
            src.parent / name,
            ROOT / "openspec" / t,
        ]
    )
    # review/SKILL.md
    if t.endswith("SKILL.md") or t.endswith("/SKILL.md"):
        cands.append(ROOT / ".cursor/skills" / t)
        if "/" in t:
            cands.append(ROOT / ".cursor/skills" / t)
    # relative from docs to skills
    cands.append((src.parent / t))
    return cands


def resolve(raw: str, src: Path) -> tuple[bool, str | None]:
    for p in candidates(raw, src):
        try:
            rp = p.resolve()
        except Exception:
            continue
        if rp.exists() and rp.is_file():
            try:
                return True, str(rp.relative_to(ROOT)).replace("\\", "/")
            except Exception:
                return True, str(rp)
        if rp.exists() and rp.is_dir() and (rp / "SKILL.md").exists():
            try:
                return True, str((rp / "SKILL.md").relative_to(ROOT)).replace("\\", "/")
            except Exception:
                return True, str(rp)
    return False, None


def classify(t: str) -> str:
    n = t.replace("\\", "/")
    for exp in EXPECTED_ABSENT:
        if n.endswith(exp) or exp in n:
            return "expected-kit-absent"
    if n.startswith("temp/") or "/temp/" in n:
        return "runtime"
    if "openspec/changes/" in n:
        return "example-or-archive"
    if "openspec/knowledge/" in n or n.endswith(("_index.yaml", "_taxonomy.yaml")):
        return "expected-kit-absent"
    if n.endswith("ADR-NNNN.md"):
        return "placeholder-pattern"
    return "broken"


def headings_and_text(path: Path) -> tuple[list[str], str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    heads = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            heads.append(m.group(2).strip())
    return heads, text


def section_exists(text: str, heads: list[str], needle: str) -> bool:
    n = needle.strip().strip("`").rstrip(".")
    n = re.sub(r"\s+", " ", n)
    if not n:
        return False
    # heading
    for h in heads:
        hn = re.sub(r"\s+", " ", h)
        if n.lower() in hn.lower() or hn.lower() in n.lower():
            return True
    if n in text:
        return True
    # numbered step 1.8 / ### 1.8 / ## Шаг 1.8
    if re.match(r"^\d+\.\d+", n):
        patterns = [
            n,
            f"### {n}",
            f"## {n}",
            f"шаг {n}",
            f"Шаг {n}",
            f"{n} ",
        ]
        for p in patterns:
            if p in text:
                return True
    # §5.1 as heading "5.1" or "§5.1"
    m = re.match(r"^§?\s*(\d+(?:\.\d+)*[a-z]?)\s*(.*)$", n, re.I)
    if m:
        num, rest = m.group(1), m.group(2)
        if num in text:
            return True
        for h in heads:
            if num in h:
                return True
    return False


PRIORITY_SECTIONS = [
    (".cursor/rules/1c-halt-triggers.mdc", ["LIGHT MODE", "MECHANICAL MODE", "ИСКЛЮЧЕНИЯ"]),
    (".cursor/rules/1c-writer-pipeline.mdc", ["LINT GATE", "ПРОМПТ WRITER", "IDENTIFIER HYGIENE CHECK"]),
    (".cursor/skills/review/SKILL.md", ["1.8", "1.9", "1.10", "3.5", "4.5", "6.4"]),
    (".cursor/docs/opsx-output-style.md", ["5.1", "2.6", "5.1a", "5.2"]),
    (".cursor/rules/chat-output-budget-full.mdc", ["1", "1b", "1c", "3a", "4", "5", "6", "7"]),
    (".cursor/skills/openspec-apply-change/templates/pause-wait-chat.md", []),
    (".cursor/skills/openspec-explain/templates/entry-brief.md", []),
    (".cursor/docs/templates/brief-card.md", []),
    (".cursor/docs/templates/decision-block.md", []),
    (".cursor/docs/marker-canon.md", []),
    (".cursor/docs/chat-lexicon.md", []),
    (".cursor/docs/kit-template-workflow.md", []),
    (".cursor/docs/delivery-integrity.md", []),
    (".cursor/docs/quick-start.md", []),
    (".cursor/docs/faq-kit.md", []),
]


def incoming_refs(all_text_blobs: list[str], filename: str) -> int:
    n = 0
    for blob in all_text_blobs:
        if filename in blob:
            n += 1
    return n


def main():
    srcs = sources()
    aa = always_apply()
    broken = []
    expected = []
    section_hits = []
    all_blobs = []
    cited_basenames = set()

    for src in srcs:
        rel = str(src.relative_to(ROOT)).replace("\\", "/")
        text = src.read_text(encoding="utf-8", errors="replace")
        all_blobs.append(text)
        lines = text.splitlines()
        seen = set()
        for i, line in enumerate(lines, 1):
            items = []
            for m in MD_LINK.finditer(line):
                items.append((m.group(2), "md-link"))
            for m in BARE_FILE.finditer(line):
                items.append((m.group(1), "backtick"))
            for m in READ_FILE.finditer(line):
                items.append((m.group(1), "read"))
            for raw, kind in items:
                t = clean(raw)
                if skip_target(t):
                    continue
                cited_basenames.add(Path(t).name)
                key = (i, t, kind)
                if key in seen:
                    continue
                seen.add(key)
                ok, found = resolve(raw, src)
                if ok:
                    continue
                st = classify(t)
                rec = {
                    "src": rel,
                    "line": i,
                    "raw": t,
                    "kind": kind,
                    "status": st,
                    "snippet": line.strip()[:220],
                }
                if st == "broken":
                    broken.append(rec)
                else:
                    expected.append(rec)
            for m in SEC_COMBO.finditer(line):
                fpart, sec = m.group(1), m.group(2).strip()
                ok, found = resolve(fpart, src)
                exists_file = ok
                exists_sec = None
                if found:
                    hp = ROOT / found
                    heads, body = headings_and_text(hp)
                    exists_sec = section_exists(body, heads, sec)
                section_hits.append(
                    {
                        "src": rel,
                        "line": i,
                        "file": fpart,
                        "section": sec[:80],
                        "file_ok": exists_file,
                        "resolved": found,
                        "section_ok": exists_sec,
                        "snippet": line.strip()[:220],
                    }
                )

    # priority files existence + sections
    priority_report = []
    for rel, secs in PRIORITY_SECTIONS:
        p = ROOT / rel
        exists = p.exists()
        item = {"file": rel, "exists": exists, "sections": []}
        if exists:
            heads, body = headings_and_text(p)
            item["headings_sample"] = heads[:25]
            for s in secs:
                item["sections"].append({"name": s, "ok": section_exists(body, heads, s)})
        priority_report.append(item)

    # review SKILL step scan
    review = ROOT / ".cursor/skills/review/SKILL.md"
    review_steps = []
    if review.exists():
        body = review.read_text(encoding="utf-8", errors="replace")
        review_steps = sorted(set(re.findall(r"(?:^|\n)#+\s*((?:\d+\.\d+)|Шаг\s+\d+(?:\.\d+)?)", body)))
        # also "### 1.8" and "шаг 1.8"
        review_steps += sorted(set(re.findall(r"\b(\d+\.\d+)\b", body)))

    # agents mentioned
    agent_files = {p.stem for p in (ROOT / ".cursor/agents").glob("*.md")}
    mention_re = re.compile(
        r"\b(onec-code-[a-z0-9\-]+|onec-trace-[a-z0-9\-]+|openspec-[a-z0-9\-]+)\b"
    )
    mentioned = defaultdict(list)
    for src in srcs:
        rel = str(src.relative_to(ROOT)).replace("\\", "/")
        for i, line in enumerate(src.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for m in mention_re.finditer(line):
                name = m.group(1)
                if name.startswith("openspec-") and name not in {
                    "openspec-quality-controller",
                    "openspec-doc-writer",
                }:
                    # skip skill folder names like openspec-explore
                    if (ROOT / ".cursor/skills" / name.replace("openspec-", "openspec-")).exists():
                        continue
                mentioned[name].append(f"{rel}:{i}")

    # commands vs skills
    cmd_map = []
    for p in sorted((ROOT / ".cursor/commands").glob("*.md")):
        head = "\n".join(p.read_text(encoding="utf-8", errors="replace").splitlines()[:40])
        names = re.findall(r"^name:\s*(.+)$", head, re.M)
        skill_refs = re.findall(r"\.cursor/skills/([^`\s\)]+/SKILL\.md)", head)
        cmd_map.append(
            {
                "file": p.name,
                "name": names[0].strip() if names else None,
                "skill_refs": skill_refs,
                "skill_ok": [(s, (ROOT / ".cursor/skills" / s).exists()) for s in skill_refs],
            }
        )

    # AGENTS.md commands
    agents_md = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
    agents_cmds = re.findall(r"`(/[a-z0-9:\-]+)`", agents_md)

    # orphans
    aa_names = always_apply()
    orphan_rules = []
    for p in sorted((ROOT / ".cursor/rules").glob("*.mdc")):
        if p.name in aa_names:
            continue
        # referenced if basename appears in any other source
        hits = 0
        for src in srcs:
            if src.resolve() == p.resolve():
                continue
            blob = src.read_text(encoding="utf-8", errors="replace")
            if p.name in blob or str(p.relative_to(ROOT)).replace("\\", "/") in blob:
                hits += 1
                break
        if hits == 0:
            orphan_rules.append(p.name)

    orphan_docs = []
    doc_files = list((ROOT / ".cursor/docs").glob("*.md")) + list(
        (ROOT / ".cursor/docs/templates").glob("*.md")
    )
    for p in sorted(doc_files):
        hits = 0
        for src in srcs:
            if src.resolve() == p.resolve():
                continue
            blob = src.read_text(encoding="utf-8", errors="replace")
            if p.name in blob:
                hits += 1
                break
        if hits == 0:
            orphan_docs.append(str(p.relative_to(ROOT)).replace("\\", "/"))

    # AGENTS.md file pointers
    agents_paths = re.findall(
        r"`?((?:\.cursor/[A-Za-z0-9_./\-]+\.(?:mdc|md))|(?:openspec/[A-Za-z0-9_./\-]+\.(?:mdc|md)))`?",
        agents_md,
    )
    agents_broken = []
    for t in agents_paths:
        t = clean(t)
        if skip_target(t) or t.endswith("/"):
            continue
        ok, found = resolve(t, ROOT / "AGENTS.md")
        if not ok:
            agents_broken.append({"raw": t, "status": classify(t)})

    out = {
        "source_count": len(srcs),
        "always_apply": sorted(aa),
        "broken": broken,
        "broken_count": len(broken),
        "expected": expected[:80],
        "expected_count": len(expected),
        "section_fail": [s for s in section_hits if s["file_ok"] and s["section_ok"] is False],
        "section_file_fail": [s for s in section_hits if not s["file_ok"]],
        "priority": priority_report,
        "review_step_tokens": sorted(set(review_steps))[:80],
        "agent_files": sorted(agent_files),
        "agent_mentions_missing_file": {
            k: v[:8] + ([f"...+{len(v)-8}"] if len(v) > 8 else [])
            for k, v in mentioned.items()
            if k not in agent_files
            and not (ROOT / ".cursor/skills" / k).exists()
            and not k.startswith("openspec-")
            or (
                k not in agent_files
                and k
                in {
                    "onec-code-architect-2nd",
                    "openspec-doc-writer",
                    "onec-code-writer",
                    "openspec-quality-controller",
                }
            )
        },
        "commands": cmd_map,
        "agents_md_commands": agents_cmds,
        "orphan_rules": orphan_rules,
        "orphan_docs": orphan_docs,
        "agents_md_broken_paths": agents_broken,
    }
    (ROOT / "temp/_link-audit3.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"sources={len(srcs)} broken={len(broken)} expected={len(expected)}")
    print("ALWAYS_APPLY", sorted(aa))
    print("--- BROKEN ---")
    for f in broken:
        print(f"{f['src']}:{f['line']}\t{f['raw']}\t{f['kind']}")
    print("--- SECTION FAIL (file ok, section missing) ---")
    for s in out["section_fail"][:60]:
        print(f"{s['src']}:{s['line']}\t{s['file']} § {s['section']}")
    print("--- PRIORITY ---")
    for p in priority_report:
        print(p["file"], "exists" if p["exists"] else "MISSING", p.get("sections"))
    print("--- ORPHAN RULES ---")
    print(orphan_rules)
    print("--- ORPHAN DOCS ---")
    print(orphan_docs)
    print("--- AGENTS.md broken ---")
    print(agents_broken)
    print("--- missing agent files ---")
    print(list(out["agent_mentions_missing_file"].keys()))


if __name__ == "__main__":
    main()
