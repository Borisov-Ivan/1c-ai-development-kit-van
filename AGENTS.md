# AGENTS.md — BSL Code Gate (навигационный индекс)

**Главный диспетчер:** `.cursor/rules/1c-agent-delegation.mdc` — HALT-условия + делегирование агентам.

## OpenSpec Workflow
`.cursor/rules/sdd-workflow.mdc` — explore → new/ff → apply → verify → archive.
Команды: `/opsx:explore`, `/opsx:new`, `/opsx:ff`, `/opsx:apply`, `/opsx:verify`, `/opsx:archive`, `/opsx:debug`, `/opsx:prerelease-review`.
Дополнительные: continue, sync, bulk-archive. Паттерны агентов: `.cursor/skills/1c-agent-patterns/SKILL.md`.
Документы из OpenSpec: `/docs:functional`, `/docs:architecture`, `/docs:technical` — `.cursor/skills/openspec-docs/SKILL.md`.

## BSL write guard
`.cursor/rules/1c-agent-delegation.mdc` — запрет прямого .bsl, APPLY GATE, DELEGATION GATE, LINT GATE.

## Запрет создания метаданных
`.cursor/rules/1c-no-metadata-creation.mdc` — СТОП, блокер пользователю.

## Анализ ошибок 1С
`.cursor/rules/1c-error-analysis.mdc` — trace-analyst → explorer/architect.

## Verified Cause Gate
`.cursor/rules/verified-cause-gate.mdc` — root cause + impact перед фиксом.

## Сохранение отчётов субагентов
`.cursor/rules/preserve-subagent-reports.mdc` — полные отчёты в reports/.

## Администрирование 1С
`.cursor/agents/onec-admin.md` — серверы, базы, PostgreSQL, ibcmd.

## Предрелизное ревью
`.cursor/skills/prerelease-review/SKILL.md` — `/opsx:prerelease-review`.

## Стандарты вендора 1С
`.cursor/skills/1c-vendor-standards/SKILL.md` — чеклисты для architect/reviewer.

## Delta Specs Gate
`.cursor/rules/openspec-specs-gate.mdc` — полнота артефакта specs.

## Command → Skill Read Gate
`.cursor/rules/command-skill-gate.mdc` — сначала Read скилла, потом файлы.

## Стратегия анализа файлов
`.cursor/skills/context-strategy/SKILL.md` — планирование: прямое чтение vs субагенты.
`.cursor/rules/context-strategy-gate.mdc` — триггер при 3+ файлах, данных, крупных модулях.
