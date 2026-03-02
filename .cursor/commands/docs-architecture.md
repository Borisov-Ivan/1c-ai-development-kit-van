---
name: /docs:architecture
id: docs-architecture
category: Documentation
description: "Сгенерировать документ «Архитектура» для заказчика из OpenSpec"
---

Сгенерируй документ «Архитектура (для заказчика)» на основе спецификаций OpenSpec.

**IMPORTANT:** Прочитай skill `.cursor/skills/openspec-docs/SKILL.md` и следуй его инструкциям для типа документа `architecture`.

Краткий алгоритм:

1. Прочитай `openspec/project.md` — контекст проекта.
2. Прочитай `openspec/architecture-extension.md` — выжимка (DR-суть, риски), без реестра перехватов.
3. Прочитай все `openspec/specs/*/spec.md` — спецификации (фильтрация по типу architecture).
4. Определи slug по имени продукта из project.md.
5. Прочитай промпт `.cursor/skills/openspec-docs/prompts/architecture.md` — правила генерации.
6. Примени промпт к собранным данным.
7. Покажи результат пользователю.
8. После подтверждения — запиши в `docs/<slug>/Архитектура.md`.
