---
name: /docs:functional
id: docs-functional
category: Documentation
description: "Сгенерировать функциональные требования из спецификаций OpenSpec"
---

Сгенерируй документ «Функциональные требования» на основе спецификаций OpenSpec.

**FIRST AND ONLY action**: Read `.cursor/skills/openspec-docs/SKILL.md`.
Do NOT read any other files in the same tool call.
After reading the skill, follow its instructions for document type `functional`.

Краткий алгоритм (подробности в скилле):

1. Прочитай `openspec/project.md` — контекст проекта (назначение, принципы, зависимости).
2. Прочитай все `openspec/specs/*/spec.md` — спецификации.
3. Прочитай промпт `.cursor/skills/openspec-docs/prompts/functional.md` — правила генерации.
4. Примени промпт к собранным данным.
5. Определи slug по имени продукта из project.md (см. SKILL.md, раздел «Определение slug»).
6. Покажи результат пользователю.
7. После подтверждения — запиши в `docs/<slug>/Функциональные требования.md`.
