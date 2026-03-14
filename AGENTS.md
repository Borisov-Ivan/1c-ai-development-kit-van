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

## XML write guard
`.cursor/rules/1c-xml-write-guard.mdc` — запрет прямой правки Form.xml, Template.xml, Rights.xml и прочих XML в src/; только через скиллы 1c-forms, 1c-mxl, 1c-roles.

## Tool Name Guard
`.cursor/rules/tool-name-guard.mdc` — инструмент вызова агентов только `Task`; при `Invalid enum value` не переключаться на generalPurpose.

## Запрет создания метаданных
`.cursor/rules/1c-no-metadata-creation.mdc` — СТОП, блокер пользователю.

## Анализ ошибок 1С
`.cursor/rules/1c-error-analysis.mdc` — trace-analyst → explorer/architect.

## Architect Gate
`.cursor/rules/architect-gate.mdc` — единые триггеры архитектурного ревью (объективные маркеры, семантические, структурные). Проверяется в explore (шаг Decide), verify (pre-apply, основной рубеж), apply (soft redirect на verify). Два рубежа: explore рекомендует, verify контролирует.

## Verify (универсальный quality gate)
`.cursor/skills/openspec-verify-change/SKILL.md` — `/opsx:verify`. Pre-apply: формат tasks, качество задач, полнота ручной конфигурации, **фазовая когерентность (Quality Controller — generalPurpose, домен-агностичный)**, **реализуемость (Architect)**, **генерация ТЗ (обязательный шаг)**, Architect Gate, Design Review, ТЗ Review, project constraints. Post-apply: completeness, correctness, coherence. Авто-устранение замечаний.
Quality Controller (шаг 7.6): фазовая классификация задач P0-P4, граф зависимостей, false start detection, rework risk. Шаблон промпта: `1c-agent-patterns/SKILL.md` (секция «Quality Controller — phase coherence review»). ТЗ (шаг 7.8): генерация функциональных требований по промпту `openspec-docs/prompts/change-tz.md`, сохранение в `ТЗ.md` change.
Коммуникация с пользователем: `.cursor/rules/verify-user-communication.mdc` — Executive Summary в отчёте, Before/After scorecard после remediation, расшифровка каждого замечания, явное указание решений от пользователя. Голые счётчики без расшифровки запрещены.

## Verified Cause Gate
`.cursor/rules/verified-cause-gate.mdc` — root cause + impact перед фиксом.

## Приоритет существующих механизмов
`.cursor/rules/existing-mechanism-priority.mdc` — Preference Hierarchy, Mandatory Discovery, anti-patterns. Срабатывает при создании нового объекта или интеграции с базой. Обязательная секция Existing Mechanisms в design.md / architecture-отчёте.

## Quality Controller (OpenSpec)
`.cursor/agents/openspec-quality-controller.md` — домен-агностичный агент (Opus, readonly). Фазовая классификация задач (P0-P4), граф зависимостей, false start detection, rework risk. Вызывается из `/opsx:verify` шаг 7.6 через `Task(subagent_type="openspec-quality-controller")`. Шаблон промпта: `1c-agent-patterns/SKILL.md` (секция «Quality Controller — phase coherence review»).

## Phase Gates (фазовое исполнение больших ЗНИ)
`.cursor/rules/phase-gates.mdc` — формат маркеров в tasks.md (`# Фаза N`, `<!-- phase-gate -->`), поведение apply (СТОП на gate, confirmation, phase gate log в debug.md, фазовый прогресс, post-architect flow), verify (phase-transition mode с **автодетектом**: phase gates + [x] перед gate + [ ] после → предложение phase-transition), ff (генерация gates архитектором), QC (alert missing-phase-gate — **always-on** критерий 5b, не только phase-transition). Правила вставки задач в phased tasks (ДОБАВЛЕНИЕ ЗАДАЧ В PHASED TASKS). Debug: phase-aware вставка задач в правильную фазу. Промпт реструктуризации плоских задач: `1c-agent-patterns/SKILL.md` (секция «Architect — phase gate restructuring»). Триггер рекомендации: 10+ задач spanning P0–P3+. Хинт: `/opsx:ff` — только для новых changes; добавление задач к существующему — через `/opsx:debug`, `/opsx:explore`, apply Phase Gate Option 3.

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

## Реестр антипаттернов BSL
`.cursor/rules/bsl-antipatterns.mdc` — краткий индекс (AP-NNN ID, detection rule, severity). **Reviewer-only** (`alwaysApply: false`, без `globs`), не загружается для writer. Writer не должен видеть антипаттерны — они могут быть неверно интерпретированы как паттерны.
`.cursor/docs/antipatterns/bsl-antipatterns.md` — полные карточки с примерами BAD/GOOD, ссылками на стандарты.
Пополняется из `/opsx:debug` (шаг 7.5 — Anti-pattern detection) по подтверждению пользователя.
Ревьювер читает индекс динамически (Phase 2, step 16 в `onec-code-reviewer.md`). Новые AP подхватываются автоматически без правки агентских промптов.

## Словарь лексики ТЗ
`.cursor/docs/tz-lexicon-dictionary.md` — запрещённые слова (англицизмы, жаргон, опечатки) с заменами и Grep-паттернами. Единый источник для генерации (`change-tz.md`, п.2 и п.11), ревью архитектора (`1c-agent-patterns/SKILL.md`, пункт 6), механической проверки (`verify`, шаги 7.8 и 11). Пополняется из `/opsx:doc-tz` (ревью архитектора → предложение → подтверждение пользователя).

## Выбор модели
`.cursor/rules/model-selection.mdc` — Opus для критичных задач, Sonnet/fast для остального.

## Запрет ROI-оценок
`.cursor/rules/no-roi-estimates.mdc` — запрет на расчёт ROI и временных оценок (кроме `/opsx:estimate`).

## Инфраструктура 1С
`.cursor/docs/onec-infrastructure.md` — серверы 1С, PostgreSQL, HASP, Dev Container.

## Доменные навыки 1С
Навыки доступны через `available_skills`; вызываются из правил и агентов по типу задачи.
- **1c-bsp** — `.cursor/skills/1c-bsp/SKILL.md` (и подскиллы command, patterns, registration): регистрация в БСП «Дополнительные отчёты и обработки», команды, паттерны подсистем.
- **1c-extensions** — `.cursor/skills/1c-extensions/SKILL.md`: аннотации расширений (&Перед/&После, &ИзменениеИКонтроль, &Вместо), синтаксис директив.
- **1c-forms** — `.cursor/skills/1c-forms/SKILL.md` (и подскиллы compile, edit, info, patterns, scaffold, validate): управляемые формы — создание, редактирование, анализ, валидация, компиляция из JSON DSL.
- **1c-mxl** — `.cursor/skills/1c-mxl/SKILL.md` (и подскиллы compile, decompile, info, validate): табличные макеты (MXL) — компиляция, декомпиляция, анализ.
- **1c-roles** — `.cursor/skills/1c-roles/SKILL.md` (и подскиллы compile, info): роли и права доступа — создание из JSON, анализ Rights.xml.
- **1c-query-optimization** — `.cursor/skills/1c-query-optimization/SKILL.md`: продвинутые паттерны запросов (временные таблицы, DCS).
- **1c-help-mcp**, **mcp-tools** — `.cursor/skills/1c-help-mcp/SKILL.md`, `.cursor/skills/mcp-tools/SKILL.md`: справка и MCP-инструменты.

## Справочная документация
`.cursor/docs/` — справочники для агентов и генерации документов.
- **platform/** — документация платформы 1С (оглавление, главы по формам, запросам, расширению конфигурации и др.). Используется в 1c-coding-standards, onec-code-explorer.
- **standard/** — `.cursor/docs/standard/1c-standards-navigator.md`, `std-01-metadata.md` … `std-11-general.md`: вендорские стандарты 1С. Ссылается `1c-vendor-standards/SKILL.md`.

## Системные промпты агентов
`.cursor/agents/*.md` — промпты для onec-code-writer, onec-code-reviewer, onec-code-architect, onec-code-explorer, onec-trace-analyst, onec-code-simplifier, onec-form-generator, onec-metadata-helper, onec-query-optimizer, onec-test-generator, onec-admin, mcp-deploy, openspec-quality-controller.
Changelog: `.cursor/agents/CHANGELOG.md`.
