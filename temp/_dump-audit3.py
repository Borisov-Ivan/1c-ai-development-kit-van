# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path(r"c:\GitHub\1c-ai-development-kit-van\temp\_link-audit3.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = []
out.append(f"keys={list(d.keys())}")
out.append(f"broken={d.get('broken_count')} expected={d.get('expected_count')}")
out.append(f"ALWAYS {d.get('always_apply')}")
out.append("--- section_fail ---")
for s in d.get("section_fail") or d.get("section_hits_fail") or []:
    out.append(f"{s.get('src')}:{s.get('line')} | {s.get('file')} | {s.get('section','')[:90]}")
out.append(f"section_fail_n={len(d.get('section_fail') or [])}")
out.append(f"section_file_fail_n={len(d.get('section_file_fail') or [])}")
out.append("--- section_file_fail sample ---")
for s in (d.get("section_file_fail") or [])[:25]:
    out.append(f"{s.get('src')}:{s.get('line')} | {s.get('file')} | {s.get('section','')[:70]}")
out.append("--- PRIORITY ---")
for item in d.get("priority") or []:
    out.append(f"{item.get('file')} exists={item.get('exists')}")
    for s in item.get("sections") or []:
        out.append(f"  {s}")
    hs = item.get("headings_sample") or item.get("headings") or []
    if hs:
        out.append("  heads: " + " | ".join(hs[:15]))
out.append("--- ORPHAN RULES ---")
out.append(str(d.get("orphan_rules")))
out.append("--- ORPHAN DOCS ---")
out.append(str(d.get("orphan_docs")))
out.append("--- AGENTS.md broken ---")
out.append(str(d.get("agents_md_broken_paths")))
out.append("--- missing agents ---")
out.append(str(list((d.get("agent_mentions_missing_file") or {}).keys())))
out.append("--- commands ---")
for c in d.get("commands") or []:
    out.append(str(c))
out.append("--- agents_md_commands ---")
out.append(str(d.get("agents_md_commands")))
out.append("--- review tokens ---")
out.append(str((d.get("review_step_tokens") or [])[:50]))
Path(r"c:\GitHub\1c-ai-development-kit-van\temp\_link-audit3-dump.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("wrote dump", len(out), "lines")
