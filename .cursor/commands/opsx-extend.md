---
name: /opsx:extend
id: opsx-extend
category: Workflow
description: Контролируемое расширение scope существующего change (новые задачи/требования с обновлением артефактов и проверкой)
---

Контролируемо расширить scope активного change: пользователь описывает **новое требование**, команда обновляет `proposal.md` / `design.md` / `specs/` / `tasks.md` (при необходимости — с привязкой к существующим или новому срезу), фиксирует в `debug.md` секцию расширения и возвращает управление в `/opsx:verify` для валидации изменённого scope.

Отделена от `/opsx:verify` — verify не редактирует артефакты (read-only gate). Extend отвечает за изменение артефактов.

**Первое действие:** прочитать `.cursor/skills/openspec-extend-change/SKILL.md` и далее идти по его шагам. До прочтения скилла — никаких других чтений артефактов, отчётов, трасс или модулей.

**Input:**
- `<change-name>` — обязательно.
- Текст расширения в сообщении пользователя (или AskQuestion при отсутствии).
- Опционально — ссылка на файл/отчёт, который нужно проанализировать как основание для правки ЗНИ:
  - `@path/to/file.md`
  - `--from-review <path>` — отчёт `/review`
  - `--from-debug <path>` — `debug.md` / RCA-отчёт
  - `--from-verify <path>` — отчёт `/opsx:verify`
  - `--from-architecture <path>` — отчёт архитектора
  - `--from-explore <path>` — Explore Summary

**Примеры:**

- `/opsx:extend do2-roli-avtopodstanovka-gate --from-review openspec/changes/do2-roli-avtopodstanovka-gate/reports/review-do2-roli-avtopodstanovka-gate-2026-04-29-subagent-raw.md "Пересмотреть решение по представлению роли"`
- `/opsx:extend add-auth @temp/explore-summary-2026-04-29.md "Добавить требование по ротации токенов"`

**Поведение (кратко):**
1. Прочитать `openspec/changes/<name>/` (proposal, design, specs, tasks).
2. Прочитать явно переданные файлы/отчёты и извлечь из них факты, findings, recommendations, open questions.
3. Показать обязательный бриф (T-BRIEF в скилле), включая блок **«Соответствие исходному scope»** и при необходимости Scope Coherence Audit (`architecture-extend-coherence-*.md`). До подтверждения пользователя — никаких правок.
4. Проанализировать новое требование: относится ли к существующему сценарию (Requirement / Scenario в spec) или требует нового.
5. Обновить артефакты:
   - proposal.md — добавить в scope (секция `## Цель` или `## Scope`).
   - specs/*/spec.md — добавить Requirement/Scenario (через openspec delta-формат, см. `openspec-specs-gate.mdc`).
   - design.md — дополнить `## Slices` (новый срез `S<N+1>`, если новое требование не укладывается в существующие).
   - tasks.md — добавить задачи по правилам vertical-slices.mdc «Поведение continue» (вставка в существующий срез или новый срез).
6. Зафиксировать в `debug.md` секцию `## Extend — YYYY-MM-DD`: источник (`--from-review`/`--from-debug`/...), что добавлено, в какой срез, disposition по findings.
7. Предложить пользователю запустить `/opsx:verify <name>` для валидации изменённого scope.

**Ограничения:**
- Не вызывает writer/reviewer — реализация остаётся за `/opsx:apply`.
- Не применяется к архивным change.
- При добавлении задач в **уже принятый** срез (`S<N>.T<M>` = `[x]`) — предупреждение: «Потребуется повторная приёмка; S<N>.T<M> будет открыт заново.»
