---
name: /opsx:doc-tz
id: opsx-doc-tz
category: Documentation
description: "Сгенерировать ТЗ по ЗНИ с архитектурным ревью и контролем качества артефактов"
---

Сгенерируй документ «Техническое задание» по одному ЗНИ (change) на основе его артефактов, проведи архитектурное ревью и выведи замечания к артефактам.

**Input**:
- `/opsx:doc-tz <name>` — сгенерировать ТЗ по указанному ЗНИ. Имя ЗНИ (например: `pav-exclusion-two-level-settings`) — это имя каталога в `openspec/changes/`. Если имя не указано — запроси его.

**FIRST AND ONLY action**: Read `.cursor/skills/openspec-docs/SKILL.md`.
Do NOT read any other files in the same tool call.
After reading the skill, follow its instructions for document type `change-tz`.