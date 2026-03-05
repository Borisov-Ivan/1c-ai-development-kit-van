---
name: /prerelease-review
id: prerelease-review
category: Quality
description: Pre-release code review for 1C extensions with severity escalation and openspec change creation
---

Провести предрелизное ревью расширения 1С.

**Input**: Опционально указать название расширения после `/prerelease-review` (например, `/prerelease-review pav_ИсключениеУчастниковПоУсловию`). Если не указано — определить из контекста или предложить выбор.

**FIRST AND ONLY action**: Read `.cursor/skills/prerelease-review/SKILL.md`.
Do NOT read any other files, traces, or modules in the same tool call.
After reading the skill, follow its instructions step by step before taking any other action.
