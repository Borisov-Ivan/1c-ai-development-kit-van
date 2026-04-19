# Changelog — 1C Agent Ecosystem

## [4.1] - 2026-04-19

### Changed (AP-001, onec-code-reviewer, bsl-antipatterns)
- AP-001: расширена карточка — двуконтекстное использование одной модульной `Перем` (граф по директивам), маркеры false-negative в комментариях, ремедиация, контр-сигналы, второй пример BAD, ссылка на [ИТС 639](https://its.1c.ru/db/v8std/content/639/hdoc), явное «не HIGH» только для чисто серверной `Перем`; кейс: change `do2-cf-partial-repeat-params-do3-ui`
- `bsl-antipatterns.mdc`: уточнена колонка Детектирование для AP-001
- `onec-code-reviewer.md`: чеклист из 3 пунктов у строки AP-001 в category 10

## [4.0] - 2026-04-17

### Removed
- onec-form-generator: конфликт с запретом правки Form.xml (1c-xml-write-guard.mdc)
- onec-test-generator: автотесты в проекте не используются, 0 вызовов в changes
- onec-metadata-helper: MCP user-PROJECT-graph не развёрнут, функции поглощены onec-code-explorer
- onec-query-optimizer: 0 вызовов в changes, функции поглощены onec-code-architect и onec-code-reviewer (последний с загрузкой скилла 1c-query-optimization)

## [3.1] - 2026-03-20

### Changed (onec-code-reviewer, bsl-antipatterns)
- AP-031: мета-имена из постановки/оркестрации — доменный тест + эвристики; интеграция в Phase 0 Evaluation Checklist (вопрос 6), Medium severity, Phase 2 code cleanliness; диапазон ссылок на реестр AP-001..AP-031
- 1c-coding-standards.mdc: подсекция ИМЕНОВАНИЕ — «Доменная релевантность»
- bsl-antipatterns.mdc / bsl-antipatterns.md: полная карточка AP-031

## [3.0] - 2026-03-12

### Added (openspec-quality-controller)
- New agent: domain-agnostic OpenSpec Quality Controller (model: Opus, readonly)
- Phase classification (P0-P4), dependency graph, false start detection, rework risk assessment
- Called from `/opsx:verify` step 7.6 via `Task(subagent_type="openspec-quality-controller")`
- Replaces previous `generalPurpose` call with default model via agent file

## [2.0] - 2026-03-08

### Changed (onec-code-explorer)
- Added TASK CLASSIFICATION: Focused Investigation / Hypothesis Verification / Full Feature Exploration
- Added Phase 0: Process Caller Context (use trace-analyst findings, classify task before code reading)
- Added Extension Analysis (cf/cfe): annotation types, base contract, interplay mapping, risks
- Added Verified Facts / Hypotheses format in Output Guidance with explicit markers
- Added Hypothesis Verification Template (mini-template for hypothesis reports)
- Refined anti-pattern: "no design decisions" instead of blanket "no recommendations"; exploration facts (extension points, contracts) are allowed
- Renamed Recommendations → Extension Points / Modification Notes in output template
- Linked Report Levels to Task Classification (Compact / Hypothesis Template / Full)
- Marked Architecture Analysis and Phases 3-4 as optional (Full Exploration only)
- Replaced Example 2, added Example 3 with realistic cf/cfe scenarios

## [1.1] - 2026-02-27

### Changed
- All agents: BSL LSP marked as NOT_CONNECTED with MCP fallback
- All agents: RLM marked as NOT_CONNECTED
- sdd-workflow.mdc: reduced to navigation document
- onec-code-explorer: added depth control, report levels, anti-patterns
- onec-code-writer: added per-invocation scope limit, idempotency
- onec-code-architect: added OpenSpec integration, plan revision, realistic testing
- onec-code-reviewer: fixed SQL->1C examples, removed aspirational integrations
- onec-code-simplifier: fixed model metadata, added pipeline integration
- 1c-dispatch-gate.mdc, 1c-agent-delegation.mdc: added Light Mode (точечная правка)

## [1.0] - 2026-02-08
- Initial version of all agents
- Source: AndreevED/1c-ai-feature-dev-workflow + improvements
