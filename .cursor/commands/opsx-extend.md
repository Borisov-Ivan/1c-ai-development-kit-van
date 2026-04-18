---
name: /opsx:extend
id: opsx-extend
category: Workflow
description: Контролируемое расширение scope существующего change (новые задачи/требования с обновлением артефактов и проверкой)
---

Контролируемо расширить scope активного change: пользователь описывает **новое требование**, команда обновляет `proposal.md` / `design.md` / `specs/` / `tasks.md` (при необходимости — с привязкой к существующим или новому срезу), фиксирует в `debug.md` секцию расширения и возвращает управление в `/opsx:verify` для валидации изменённого scope.

Отделена от `/opsx:verify` — verify не редактирует артефакты (read-only gate). Extend отвечает за изменение артефактов.

**FIRST AND ONLY action:** Read `.cursor/skills/openspec-continue-change/SKILL.md` и `.cursor/rules/vertical-slices.mdc` (секция «Поведение continue»). Не читать другие файлы в том же tool-call.

**Input:**
- `<change-name>` — обязательно.
- Текст расширения в сообщении пользователя (или AskQuestion при отсутствии).

**Поведение (кратко):**
1. Прочитать `openspec/changes/<name>/` (proposal, design, specs, tasks).
2. Проанализировать новое требование: относится ли к существующему сценарию (Requirement / Scenario в spec) или требует нового.
3. Обновить артефакты:
   - proposal.md — добавить в scope (секция `## Цель` или `## Scope`).
   - specs/*/spec.md — добавить Requirement/Scenario (через openspec delta-формат, см. `openspec-specs-gate.mdc`).
   - design.md — дополнить `## Slices` (новый срез `S<N+1>`, если новое требование не укладывается в существующие).
   - tasks.md — добавить задачи по правилам vertical-slices.mdc «Поведение continue» (вставка в существующий срез или новый срез).
4. Зафиксировать в `debug.md` секцию `## Extend — YYYY-MM-DD`: что добавлено, в какой срез, ссылка на сообщение пользователя.
5. Предложить пользователю запустить `/opsx:verify <name>` для валидации изменённого scope.

**Ограничения:**
- Не вызывает writer/reviewer — реализация остаётся за `/opsx:apply`.
- Не применяется к архивным change.
- При добавлении задач в **уже принятый** срез (`S<N>.T<M>` = `[x]`) — предупреждение: «Потребуется повторная приёмка; S<N>.T<M> будет открыт заново.»
