---
name: /opsx:doc-tz
id: opsx-doc-tz
category: Documentation
description: "Сгенерировать ТЗ по ЗНИ с архитектурным ревью и контролем качества артефактов"
---

Сгенерируй документ «Техническое задание» по одному ЗНИ (change) на основе его артефактов, проведи архитектурное ревью и выведи замечания к артефактам.

**Имя ЗНИ** пользователь указывает в сообщении (например: `pav-exclusion-two-level-settings`). Если имя не указано — запроси его.

**FIRST AND ONLY action**: Read `.cursor/skills/openspec-docs/SKILL.md`.
Do NOT read any other files in the same tool call.
After reading the skill, follow its instructions for document type `change-tz`.

Краткий алгоритм (подробности в скилле):

1. Определи имя change из сообщения пользователя; проверь наличие каталога `openspec/changes/<name>/`.
2. Прочитай артефакты: proposal.md, design.md, specs/*/spec.md, при наличии reports/architecture-*.md и exploration-*.md.
3. Прочитай промпт `.cursor/skills/openspec-docs/prompts/change-tz.md`.
4. Примени промпт к собранным данным — сгенерируй ТЗ с верификацией артефактов.
5. Делегируй ревью ТЗ субагенту `Task(subagent_type="onec-code-architect")` по шаблону «Architect — ТЗ quality review» из `1c-agent-patterns/SKILL.md`.
6. Примени замечания к ТЗ (document-level), объедини замечания к артефактам (artifact-level) в бриф.
7. Покажи результат пользователю: финальный текст ТЗ + бриф замечаний к артефактам (если есть).
8. После подтверждения — запиши ТЗ в `openspec/changes/<name>/ТЗ.md`, отчёт ревью — в `reports/tz-review-YYYY-MM-DD.md`.
