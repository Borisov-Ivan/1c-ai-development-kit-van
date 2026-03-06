---
name: /opsx-verify
id: opsx-verify
category: Workflow
description: Verify implementation matches change artifacts before archiving
---

Verify that an implementation matches the change artifacts (specs, tasks, design).

**FIRST AND ONLY action**: Read `.cursor/skills/openspec-verify-change/SKILL.md`.
Do NOT read any other files, traces, or modules in the same tool call.
After reading the skill, follow its instructions step by step before taking any other action.

Input: optionally specify a change name (e.g., `/opsx:verify add-auth`). If omitted, the skill will prompt for selection.
