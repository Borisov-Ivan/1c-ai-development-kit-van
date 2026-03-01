---
name: /docs:functional
id: docs-functional
category: Documentation
description: "Сгенерировать функциональные требования из спецификаций OpenSpec"
---

Сгенерируй документ «Функциональные требования» на основе спецификаций OpenSpec.

**IMPORTANT:** Прочитай skill `.cursor/skills/openspec-docs/SKILL.md` и следуй его инструкциям для типа документа `functional`.

Краткий алгоритм:

1. Прочитай `openspec/project.md` — контекст проекта (назначение, принципы, зависимости).
2. Прочитай все `openspec/specs/*/spec.md` — спецификации.
3. Прочитай промпт `.cursor/skills/openspec-docs/prompts/functional.md` — правила генерации.
4. Примени промпт к собранным данным.
5. Покажи результат пользователю.
6. После подтверждения — запиши в `docs/Функциональные требования.md`.
