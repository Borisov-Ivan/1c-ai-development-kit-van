---
name: /docs:technical
id: docs-technical
category: Documentation
description: "Сгенерировать технический проект из OpenSpec"
---

Сгенерируй документ «Технический проект» на основе спецификаций OpenSpec.

**FIRST AND ONLY action**: Read `.cursor/skills/openspec-docs/SKILL.md`.
Do NOT read any other files in the same tool call.
After reading the skill, follow its instructions for document type `technical`.

Краткий алгоритм (подробности в скилле):

1. Прочитай `openspec/project.md` — контекст проекта.
2. Прочитай `openspec/architecture-extension.md` — полностью (включая реестр перехватов).
3. Прочитай все `openspec/specs/*/spec.md` — спецификации.
4. Определи slug по имени продукта из project.md.
5. Прочитай промпт `.cursor/skills/openspec-docs/prompts/technical.md` — правила генерации.
6. Примени промпт к собранным данным.
7. Покажи результат пользователю.
8. После подтверждения — запиши в `docs/<slug>/Технический проект.md`.
