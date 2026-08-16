# Ссылки после удаления рудиментов (S6.9)

**Change:** kit-evolution-models-economy-profiles  
**Дата:** 2026-08-16  
**Критерий:** нет ссылок на **пути файлов**, удалённых в этом change. Исторический текст команд и журнал агентов — не живые входы.

## Удалённые / перенесённые пути

| Путь | Состояние на диске (`Test-Path`) |
|------|----------------------------------|
| `.cursor/commands/opsx-ff.md` | отсутствует |
| `.cursor/commands/opsx-continue.md` | отсутствует |
| `.cursor/rules/openspec-sessions.mdc` | отсутствует |
| `.cursor/agents/CHANGELOG.md` | отсутствует |
| `.cursor/docs/agents-CHANGELOG.md` | есть (перенос S6.6) |
| `.cursor/rules/bsl-write-guard.mdc` | отсутствует (S2) |
| `.cursor/rules/conversational-discipline.mdc` | отсутствует (S2) |
| `.cursor/rules/orchestrator-as-navigator.mdc` | отсутствует (S2) |

## Рантайм-поставка (`.cursor/**`, `AGENTS.md`)

- Индекс команд в `AGENTS.md` не содержит `/opsx:ff` и `/opsx:continue`.
- Журнал агентов указывает на `.cursor/docs/agents-CHANGELOG.md`.
- Поиск путей `opsx-ff.md`, `opsx-continue.md`, `openspec-sessions.mdc`, `agents/CHANGELOG.md` в живых `.md`/`.mdc` рантайма не даёт рабочих ссылок (индекс поиска Cursor может ещё показывать удалённые файлы — на диске их нет).
- Legacy-заголовок `## Для /opsx:ff` в скиллах `openspec-new-change` / `openspec-explore` — синоним блока постановки, не ссылка на удалённый файл команды (Non-Goals: read-only `openspec/sessions/` не трогали).
- Упоминания старых имён в `.cursor/docs/agents-CHANGELOG.md` — журнал истории, не маршрутизация.

## Артефакты этого change (`openspec/changes/kit-evolution-models-economy-profiles/**`)

`proposal.md`, `design.md`, `tasks.md`, `specs/rules-hygiene/spec.md` и отчёты архитектора **называют** удаляемые пути как работу среза S6 — это описание задачи, не живая ссылка поставки.

## Итог

Сценарий «Ссылки после удаления» для рантайм-поставки выполнен. Список команд в `AGENTS.md` совпадает с существующими файлами `.cursor/commands/` (без alias-стабов).
