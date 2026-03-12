---
name: /opsx-verify
id: opsx-verify
category: Workflow
description: Universal quality gate — pre-apply (artifact quality, task specificity, gates) and post-apply (implementation completeness, correctness, coherence)
---

Universal quality gate for OpenSpec changes. Automatically determines mode:
- **Pre-apply**: artifact format, task quality and specificity, Architect Gate, Design Review, TZ Review, project constraints
- **Post-apply**: implementation completeness, correctness, coherence

Offers auto-remediation of found issues.

**FIRST AND ONLY action**: Read `.cursor/skills/openspec-verify-change/SKILL.md`.
Do NOT read any other files, traces, or modules in the same tool call.
After reading the skill, follow its instructions step by step before taking any other action.

Input: optionally specify a change name (e.g., `/opsx:verify add-auth`). If omitted, the skill will prompt for selection.
