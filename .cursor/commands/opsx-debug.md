---
name: /opsx-debug
id: opsx-debug
category: Workflow
description: "Investigate a bug in context of an OpenSpec change — trace analysis, RCA, fix plan and apply"
---

Investigate a test-found bug and produce a root-cause analysis and a fix plan captured inside an OpenSpec change.

**Alias:** `/debug`

**Input**: The user may provide any combination of:
- Trace file path (`.pff`, `*_TRACE_*.txt`)
- Textual remark / expected vs actual behavior
- Screenshots (attached images)
- Optional OpenSpec change id (e.g. `fix-exclude-participants-v2`)
- Optional task number/id (e.g. `4.3`)

**FIRST AND ONLY action**: Read `.cursor/skills/openspec-debug/SKILL.md`.
Do NOT read any other files, traces, or modules in the same tool call.
After reading the skill, follow its instructions step by step before taking any other action.
