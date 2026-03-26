# AGENTS.md — BSL Code Gate (навигационный индекс)

**Главный диспетчер:** `.cursor/rules/1c-agent-delegation.mdc` — HALT-условия + делегирование агентам.

## OpenSpec Workflow
`.cursor/rules/sdd-workflow.mdc` — explore → new/ff → verify → apply → verify → archive.
Команды: `/opsx:explore`, `/opsx:new`, `/opsx:ff`, `/opsx:apply`, `/opsx:verify`, `/opsx:archive`, `/opsx:debug`, `/opsx:estimate`, `/opsx:prerelease-review`, `/review`.
`/review` — полное ревью по контексту запроса (модуль/файлы/расширение) с опцией устранения замечаний; скилл `.cursor/skills/review/SKILL.md`.
Дополнительные: `/opsx:continue`, `/opsx:sync`, `/opsx:bulk-archive`, `/opsx:onboard`, `/init-project`.
Паттерны агентов: `.cursor/skills/1c-agent-patterns/SKILL.md`.
Документы: `/opsx:doc-tz <name>` (ТЗ по ЗНИ с архитектурным ревью и контролем качества артефактов) — `.cursor/skills/openspec-docs/SKILL.md`.

## Фиксация договорённостей
`.cursor/rules/capture-to-project.mdc` — «зафиксируй в проекте» → Read `openspec/project.md` → адаптация под формат секции → подтверждение → запись.

## BSL write guard
`.cursor/rules/bsl-write-guard.mdc` — глобальный инвариант: правка .bsl только через onec-code-writer + обязательный onec-code-reviewer (любой диалог). `.cursor/rules/1c-agent-delegation.mdc` — детальная диспетчеризация: APPLY GATE, DELEGATION GATE, LINT GATE, API CHECK, EXTENSION GATE.

## Пути к выгрузке
Базовая конфигурация и расширения заданы в `openspec/project.md` (секция «Структура репозитория»). При поиске кода в src/ и проверке выгрузки использовать эти пути; не предполагать `src/cf/` и `src/cfe/`. См. `.cursor/rules/project-paths.mdc`.

## Code reviewer (onec-code-reviewer)
`.cursor/agents/onec-code-reviewer.md` — ревью кода BSL. **Приоритет рассуждения над каталогом:** сначала Phase 0 (Intent & Reasoning Analysis) — артефакты Intent Map, Contract Map, Knowledge Assessment; замечания по логике (DISPROPORTIONATE_COMPLEXITY, CONTRACT_INCONSISTENCY, CONTRACT_INFERENCE, KNOWLEDGE_DEFICIT, CLARITY_DEFICIT). Каталог антипаттернов (AP-NNN) — вспомогательный шаг. Мета-имена (постановка вместо домена): AP-031. Отчёт: секция Reasoning Analysis (Phase 0), затем Standards & Patterns. **Формат замечаний:** каждое замечание содержит стабильные якоря (Procedure, Anchor — для поиска после правок) и поле Action (MUST_FIX / VERIFIED_OK / OPTIONAL); при устранении через /review writer получает только MUST_FIX. **Investigation Request:** ревьювер может запросить резолв контрактов через секцию `## Investigation Request` в отчёте (Phase 2.5 шаг D); оркестратор делегирует explorer и перезапускает ревью с Resolved Contracts (шаг 3.5 review/SKILL.md). **Resolved Contracts (артифакт ЗНИ):** результат investigation loop сохраняется в `reports/resolved-contract-<scope-slug>-YYYY-MM-DD.md`. Содержит верифицированные контракты (тип, ключи, fixed/dynamic, Evidence). Передаётся writer при review-fix и reviewer при повторном ревью. Writer и reviewer знают формат и правила использования (см. агентские промпты). При отсутствии блока в промпте reviewer проверяет `reports/resolved-contract-*.md` по change (fallback). **Принцип «Уточни, не защищайся»:** Свойство()/ТипЗнч() при невыясненном контракте без попытки резолва = AP-004 (компенсация незнания). Writer обязан сначала установить контракт; reviewer проверяет наличие обоснования. См. 1c-coding-standards.mdc rule 14. **Unverified API:** информационная секция в отчёте — вызовы, определение которых не найдено в src/.

## API Existence Check
`.cursor/rules/1c-agent-delegation.mdc` (секция API EXISTENCE CHECK) — проверка существования вызываемых методов общих модулей в src/ (cf + cfe) после writer, до reviewer. AskQuestion при ненайденном методе.

## XML write guard
`.cursor/rules/1c-xml-write-guard.mdc` — запрет прямой правки Form.xml, Template.xml, Rights.xml и прочих XML в src/. Form.xml → только инструкция ручного конфигурирования (не через скиллы/агентов). Template.xml, Rights.xml — через скиллы 1c-mxl, 1c-roles.

## Tool Name Guard
`.cursor/rules/tool-name-guard.mdc` — для вызова субагентов использовать инструмент **Task**. При `Invalid enum value` проверить имя инструмента (должен быть Task) и subagent_type; не переключаться на generalPurpose.

## Запрет создания метаданных
`.cursor/rules/1c-no-metadata-creation.mdc` — СТОП, блокер пользователю.

## Анализ ошибок 1С
`.cursor/rules/1c-error-analysis.mdc` — trace-analyst → explorer/architect.

## Architect Gate
`.cursor/rules/architect-gate.mdc` — единые триггеры архитектурного ревью (объективные маркеры, семантические, структурные). **UX-значимый фикс** (меняет что видит/делает пользователь) — семантический триггер; **debug:** при срабатывании триггеров architect обязателен до шага 7 (не AskQuestion), шаблон «Architect — fix quality review» в `1c-agent-patterns/SKILL.md`. Проверяется в explore (шаг Decide, Fix Quality check при bug fix), verify (pre-apply, шаг 9 + Debug fix check), apply (soft redirect на verify).

## Verify (универсальный quality gate)
`.cursor/skills/openspec-verify-change/SKILL.md` — `/opsx:verify`. Pre-apply: формат tasks, качество задач, полнота ручной конфигурации, **фазовая когерентность (Quality Controller)** — **строго до** шага реализуемости (Architect 7.7), **реализуемость (Architect)**, **генерация ТЗ (шаг 7.8, при пороге 4+ задач с чекбоксами или явном запросе ТЗ)**, Architect Gate, Design Review, ТЗ Review, project constraints. Post-apply: completeness, correctness, coherence. Авто-устранение замечаний; **после remediation** — обязательная повторная верификация затронутых проверок и при необходимости повторный QC/Architect (шаг 17a).

**Scope Gate (шаг 1b):** verify не расширяет scope сам по себе; если в запросе есть новое требование помимо команды verify — AskQuestion: дополнить артефакты → verify / verify as-is / TODO в отчёте.

**Порядок субагентов:** QC (7.6) и Architect task readiness (7.7) **не** запускать параллельно — Architect получает результат QC.

**Отчёт:** `reports/verification-<mode>-YYYY-MM-DD.md` — полный артефакт, включая секцию **«Развёрнутые объяснения замечаний»** (дублируется в сообщении пользователю). См. шаг 16 скилла.

**Executability Analysis (тройная проверка):** verify шаг 7F (механическая), QC критерий 5d (семантическая), Architect критерий 6 (холистическая). Покрывает ВСЕ задачи (P0-P4): функциональные зависимости из описаний, порядок в файле vs граф зависимостей, итерационный дрифт (задачи из debug ломают порядок ранних секций), валидация текста «Порядок выполнения», именованные задачи в phase gate маркерах.

Quality Controller (шаг 7.6): фазовая классификация задач P0-P4, граф зависимостей, false start detection, rework risk, executability analysis (5d). Шаблон промпта: `1c-agent-patterns/SKILL.md` (секция «Quality Controller — phase coherence review»). ТЗ (шаг 7.8): генерация по `openspec-docs/prompts/change-tz.md` при выполнении порога или явном запросе; иначе пропуск с сохранением существующего `ТЗ.md`.

Коммуникация с пользователем: `.cursor/rules/verify-user-communication.mdc` — Executive Summary, развёрнутые абзацы для WARNING/CRITICAL в первом сообщении, Before/After scorecard после remediation, явное указание решений от пользователя. Голые счётчики без таблицы и развёрнутых объяснений запрещены.

## Verified Cause Gate
`.cursor/rules/verified-cause-gate.mdc` — root cause + impact перед фиксом. Масштаб: точечный (не меняет UX) / **UX-значимый** (меняет сценарий пользователя) / системный; UX-значимый и системный → architect обязателен. Fix Quality Gate: анти-паттерн «фикс симптома»; verify шаг 7.7 — критерий 6 (качество фиксов), шаг 9 — Debug fix check (задачи из debug без architecture-*.md → CRITICAL).

## Приоритет существующих механизмов
`.cursor/rules/existing-mechanism-priority.mdc` — Preference Hierarchy, Mandatory Discovery, anti-patterns. Срабатывает при создании нового объекта или интеграции с базой. Обязательная секция Existing Mechanisms в design.md / architecture-отчёте.

## Quality Controller (OpenSpec)
`.cursor/agents/openspec-quality-controller.md` — домен-агностичный агент (Opus, readonly). Фазовая классификация задач (P0-P4), граф зависимостей, false start detection, rework risk. Вызывается из `/opsx:verify` шаг 7.6 через `Task(subagent_type="openspec-quality-controller")`. Шаблон промпта: `1c-agent-patterns/SKILL.md` (секция «Quality Controller — phase coherence review»).

## Phase Gates (фазовое исполнение больших ЗНИ)
`.cursor/rules/phase-gates.mdc` — формат маркеров в tasks.md (`# Фаза N`, `<!-- phase-gate -->`), поведение apply (СТОП на gate, confirmation, phase gate log в debug.md, фазовый прогресс, post-architect flow), verify (phase-transition mode с **автодетектом**: phase gates + [x] перед gate + [ ] после → предложение phase-transition), ff (генерация gates архитектором), QC (alert missing-phase-gate — **always-on** критерий 5b, не только phase-transition). **5c enrichment:** именованные задачи в маркере gate проверяются поимённо; валидация текста «Порядок выполнения» при apply. Правила вставки задач в phased tasks (ДОБАВЛЕНИЕ ЗАДАЧ В PHASED TASKS). Debug: phase-aware вставка задач в правильную фазу. Промпт реструктуризации плоских задач: `1c-agent-patterns/SKILL.md` (секция «Architect — phase gate restructuring»). Триггер рекомендации: 10+ задач spanning P0–P3+. Хинт: `/opsx:ff` — только для новых changes; добавление задач к существующему — через `/opsx:debug`, `/opsx:explore`, apply Phase Gate Option 3.

## Session Handoff и Step-by-step mode
`.cursor/skills/openspec-apply-change/SKILL.md` (шаги 5.6, 6, 7) — Session Handoff Summary (три секции: код / действия пользователя / следующие задачи), Step-by-step mode (пауза после каждой задачи с подтверждением, обработка ручных тестов с ожиданием результата). Триггеры step-by-step: явный запрос, debug-сессия, P4 задачи в текущей пачке.

## Сохранение отчётов субагентов
`.cursor/rules/preserve-subagent-reports.mdc` — полные отчёты в reports/.

## Утилитарные агенты
`.cursor/rules/1c-utility-agents.mdc` — инструкции по формам (Form.xml), запросы, тесты, упрощение, метаданные, администрирование. Загружается по необходимости (не always-apply).

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
