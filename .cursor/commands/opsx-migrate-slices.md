---
name: /opsx:migrate-slices
id: opsx-migrate-slices
category: Workflow
description: Миграция legacy/фазового tasks.md в вертикальные срезы (architect restructuring + подтверждение пользователя)
---

Миграция существующего `tasks.md` (плоский список задач или legacy `# Фаза N` / `<!-- phase-gate -->`) в модель **вертикальных срезов** по `.cursor/rules/vertical-slices.mdc`.

Отделена от `/opsx:verify` — это самостоятельная реструктурирующая операция с явным подтверждением diff пользователем. Verify при обнаружении `<!-- phase-gate -->` или плоских tasks.md в slice-совместимой ЗНИ предлагает запустить эту команду.

**Первое действие:** прочитать `.cursor/skills/openspec-migrate-slices/SKILL.md` и далее идти по шагам скилла. До прочтения — никаких других чтений.

**Input:**
- `<change-name>` — обязательно. Если не указано — AskUserQuestion по списку активных changes.

**Поведение:**
1. Архитектор (`Task(subagent_type="onec-code-architect")`) получает proposal.md / design.md / spec и плоский tasks.md, использует шаблон «Architect — slice restructuring» из `1c-agent-patterns/SKILL.md`.
2. Результат — предложенная структура срезов: таблица «старая задача → новый срез», список `S<N>.T<M>` приёмочных тестов, предупреждения о задачах, которые не удалось отнести к сценарию.
3. Пользователь подтверждает diff (или отклоняет / просит пересборку).
4. После подтверждения — `StrReplace`/`Write` для `tasks.md` и секции `## Slices` в `design.md`.
5. Отчёт миграции — `reports/migrate-to-slices-YYYY-MM-DD.md`.
6. Рекомендация: `/opsx:verify <name>` после миграции — прогон нового tasks.md через QC/Architect.

**Ограничения:**
- Не применяется к архивным change (`openspec/changes/archive/`) — они read-only (см. `vertical-slices.mdc`, «Обратная совместимость»).
- Не запускается автоматически — только по явной команде пользователя.
