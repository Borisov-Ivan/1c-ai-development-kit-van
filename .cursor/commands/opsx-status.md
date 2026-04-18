---
name: /opsx:status
id: opsx-status
category: Workflow
description: Снимок текущего состояния OpenSpec change — срезы, отчёты, слайс-гейты, рекомендуемая следующая команда
---

Прочитать и показать **текущее состояние** активного change: имя, schema, структура срезов и их статус приёмки, последние отчёты в `reports/`, открытые `awaiting-acceptance` решения в `debug.md`, рекомендуемая следующая команда. Полностью read-only, без правок артефактов и без субагентов.

Полезно для:
- быстрого возврата к change после паузы/переключения задач;
- понимания, где мы в workflow без запуска тяжёлого `/opsx:verify`;
- сверки перед `/opsx:apply`, `/opsx:archive`, `/opsx:extend`.

**FIRST AND ONLY action:** Read `.cursor/skills/openspec-status/SKILL.md`. Не читать другие файлы в том же tool-call.

**Input:**
- `<change-name>` — опционально. Если не указано — AskUserQuestion по списку активных changes (`openspec list --json`).

**Флаги:**
- `--short` — только заголовок: имя, режим (slice-pre / slice-post / legacy), прогресс по срезам одной строкой, рекомендация.
- `--reports` — таблица последних отчётов в `reports/` (тип, дата, размер, first-line summary).
