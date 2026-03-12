# AGENTS.md — BSL Code Gate (навигационный индекс)

**Главный диспетчер:** `.cursor/rules/1c-agent-delegation.mdc` — HALT-условия + делегирование агентам.

## OpenSpec Workflow
`.cursor/rules/sdd-workflow.mdc` — explore → new/ff → verify → apply → verify → archive.
Команды: `/opsx:explore`, `/opsx:new`, `/opsx:ff`, `/opsx:apply`, `/opsx:verify`, `/opsx:archive`, `/opsx:debug`, `/opsx:estimate`, `/opsx:prerelease-review`.
Дополнительные: `/opsx:continue`, `/opsx:sync`, `/opsx:bulk-archive`, `/opsx:onboard`, `/init-project`.
Паттерны агентов: `.cursor/skills/1c-agent-patterns/SKILL.md`.
Документы: `/opsx:doc-tz <name>` (ТЗ по ЗНИ с архитектурным ревью и контролем качества артефактов) — `.cursor/skills/openspec-docs/SKILL.md`.

## BSL write guard
`.cursor/rules/1c-agent-delegation.mdc` — запрет прямого .bsl, APPLY GATE, DELEGATION GATE, LINT GATE.

## Tool Name Guard
`.cursor/rules/tool-name-guard.mdc` — инструмент вызова агентов только `Task`; при `Invalid enum value` не переключаться на generalPurpose.

## Запрет создания метаданных
`.cursor/rules/1c-no-metadata-creation.mdc` — СТОП, блокер пользователю.

## Анализ ошибок 1С
`.cursor/rules/1c-error-analysis.mdc` — trace-analyst → explorer/architect.

## Architect Gate
`.cursor/rules/architect-gate.mdc` — единые триггеры архитектурного ревью (объективные маркеры, семантические, структурные). Проверяется в explore (шаг Decide), verify (pre-apply, основной рубеж), apply (soft redirect на verify). Два рубежа: explore рекомендует, verify контролирует.

## Verify (универсальный quality gate)
`.cursor/skills/openspec-verify-change/SKILL.md` — `/opsx:verify`. Pre-apply: формат tasks (чекбоксы, нумерация), качество задач (конкретность, пути к файлам, критерии приёмки, маркеры размытости), Architect Gate, Design Review, ТЗ Review, project constraints. Post-apply: completeness, correctness, coherence. Авто-устранение замечаний.

## Verified Cause Gate
`.cursor/rules/verified-cause-gate.mdc` — root cause + impact перед фиксом.

## Приоритет существующих механизмов
`.cursor/rules/existing-mechanism-priority.mdc` — Preference Hierarchy, Mandatory Discovery, anti-patterns. Срабатывает при создании нового объекта или интеграции с базой. Обязательная секция Existing Mechanisms в design.md / architecture-отчёте.

## Сохранение отчётов субагентов
`.cursor/rules/preserve-subagent-reports.mdc` — полные отчёты в reports/.

## Утилитарные агенты
`.cursor/rules/1c-utility-agents.mdc` — формы, запросы, тесты, упрощение, метаданные, администрирование. Загружается по необходимости (не always-apply).

## Предрелизное ревью
`.cursor/skills/prerelease-review/SKILL.md` — `/opsx:prerelease-review`.

## Стандарты вендора 1С
`.cursor/skills/1c-vendor-standards/SKILL.md` — чеклисты для architect/reviewer.

## Delta Specs Gate
`.cursor/rules/openspec-specs-gate.mdc` — полнота артефакта specs.

## Command → Skill Read Gate
`.cursor/rules/command-skill-gate.mdc` — сначала Read скилла, потом файлы.

## Command Session Persistence
`.cursor/rules/command-session-persistence.mdc` — протокол команды действует на каждом ходе сессии, не только на первом.

## Architecture Decision Records (ADR)
`openspec/adrs/` — постоянное хранилище архитектурных решений проекта.
`.cursor/rules/adr-format.mdc` — формат, именование, критерии, жизненный цикл.
Индекс: `openspec/adrs/README.md`. Создаются при archive (шаг 5), обнаруживаются при explore/ff/new (ADR Discovery).
Интеграция: `architect-gate.mdc` (ADR Discovery при срабатывании), `1c-agent-patterns/SKILL.md` (шаблон extraction).

## Оценка трудозатрат
`.cursor/skills/openspec-estimate/SKILL.md` — `/opsx:estimate <name>`. Трёхточечная PERT-оценка по tasks.md. Авторежимы: первичная оценка / переоценка / калибровка по факту. Ставки встроены в скилл, опциональный оверрайд — `openspec/estimate-rates.md`.

## Стратегия анализа файлов
`.cursor/skills/context-strategy/SKILL.md` — планирование: прямое чтение vs субагенты.
`.cursor/rules/context-strategy-gate.mdc` — триггер при 3+ файлах, данных, крупных модулях.

## Стандарты BSL
`.cursor/rules/1c-coding-standards.mdc` — file-scoped (`**/*.bsl`): структура, именование, запросы, Попытка, защитные проверки, валидация имён метаданных по XML-выгрузке.

## Выбор модели
`.cursor/rules/model-selection.mdc` — Opus для критичных задач, Sonnet/fast для остального.

## Запрет ROI-оценок
`.cursor/rules/no-roi-estimates.mdc` — запрет на расчёт ROI и временных оценок (кроме `/opsx:estimate`).

## Инфраструктура 1С
`.cursor/docs/onec-infrastructure.md` — серверы 1С, PostgreSQL, HASP, Dev Container.

## Системные промпты агентов
`.cursor/agents/*.md` — промпты для onec-code-writer, onec-code-reviewer, onec-code-architect, onec-code-explorer, onec-trace-analyst, onec-code-simplifier, onec-form-generator, onec-metadata-helper, onec-query-optimizer, onec-test-generator, onec-admin, mcp-deploy.
Changelog: `.cursor/agents/CHANGELOG.md`.
