---
verify_mode: pre-apply
change: model-tier-by-step
date: 2026-09-23
verdict: GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: WARNING
  layer_4_independent_challenge: SKIPPED-novelty
  layer_5_implementation_readiness: PASS
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions:
    - id: architect_step_model_table
      summary: "Исключения модели архитектора живут в одной таблице шагов. Строка роли, обычный вызов, чеклист вызова, запуск проверки и шаблон промпта только ссылаются на неё. Сбой состоявшегося вызова сверки задач останавливает продолжение. Переиспользование отчёта, когда вызов не запускался, сохраняется."
      closed_at: "2026-09-22"
      source: verify-user-answer
      confirmed_by: user
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: incremental
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-09-22T08:33:04Z"
    design.md: "2026-09-23T01:19:42Z"
    tasks.md: "2026-09-23T01:01:42Z"
    specs/subagent-model-mapping/spec.md: "2026-09-23T01:00:25Z"
  last_challenge_at: "2026-09-23T10:08:00+09:00"
  artifact_hashes:
    proposal.md: "2ab1f8511c94638ebac2fb2e4529b636d1c90b38628a40abf3f8f80732150a78"
    design.md: "237f44171e3628ccf5222168afc58a509958f8ad64ebc09631deca0b14042765"
    design-axis: "ff282a9e16864dda046514a8054c1c3a503ed83d6f33b4704d7388e449cfc025"
    tasks.md: "95cdc568a243f891a24d766566867af38bd28ee105696db40a97f6ba2e955eb6"
    specs/subagent-model-mapping/spec.md: "e07dcea3d10cbe97235455e706c20b855dff43ee3ace3596f1c512dba7d7c739"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints:
    architect_step_model_table: "cda751f499f2278b7aa9c9ba20264135eaaf06e5769163f5834f27aa571ca418"
  rules_versions:
    .cursor/rules/vertical-slices.mdc: "ae7299668199f606222fcb969922dfc821ccb95c38180b0099256864ec700978"
    .cursor/rules/openspec-specs-gate.mdc: "9724d7079e9630844d16bce0b5b664e29929da2136fb3a8f19f3b61e1a52c867"
    .cursor/rules/code-truth-gate.mdc: "bb7ecbbf53bd3b877b36b184eab851ca9f3f24db5f657f154df22029354ce579"
    .cursor/rules/precedent-regression-gate.mdc: "875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641"
    .cursor/rules/architect-gate.mdc: "ba2b3add96503d98649bd11c60f1f6be61cb74962a62811fcdd38961d8c6deae"
    .cursor/rules/model-selection.mdc: "6abe07aaa8986cd211e971c62e09d49fbc01626a2536e43f58b2502399bbaf84"
    .cursor/skills/openspec-verify-change/SKILL.md: "ff9ace29759aa5085b1d112917a69cacdfa0bc9709d6219db0e23521580977cd"
  check_cache:
    hygiene-checkboxes@tasks.md: "PASS|95cdc568a243f891a24d766566867af38bd28ee105696db40a97f6ba2e955eb6"
    slice-gate-markers@tasks.md: "PASS|95cdc568a243f891a24d766566867af38bd28ee105696db40a97f6ba2e955eb6"
    user-task-contract@tasks.md: "PASS|none"
    external-validity@none: "PASS|workflow-fork-no-ec"
    scenario-coverage@all: "PASS|qc-2026-09-23"
    code-truth@pre-apply: "OK|no-1c-symbols"
    precedent-regression@subagent-model-mapping: "INFO|precedent-documented"
    loop-detection@S1-S2: "PASS|closed-by-redesign-2026-09-23"
    problem-solution-trace@proposal-specs: "WARNING|scenario-orphan-slice-regression"
    design-challenge@axis: "SKIPPED-novelty|ff282a9e16864dda046514a8054c1c3a503ed83d6f33b4704d7388e449cfc025"
    task-readiness@all: "PASS|architecture-task-readiness-2026-09-23"
  invalidation_map:
    hygiene-checkboxes: "reused; tasks hash unchanged"
    slice-gate-markers: "reused; tasks hash unchanged"
    user-task-contract: "reused; tasks hash unchanged"
    external-validity: "rechecked; new extend has no EC fields"
    scenario-coverage: "reused; spec, tasks and Slices unchanged"
    code-truth: "reused"
    precedent-regression: "reused; spec hash unchanged"
    loop-detection: "rechecked; redesign accepted, tasks not changed"
    problem-solution-trace: "reused; proposal and spec hashes unchanged"
    design-challenge: "axis unchanged; only verify-decisions sentence added"
    task-readiness: "reused; tasks hash unchanged"
---

## Резюме для разработчика

model-tier-by-step — можно запускать apply. Повторные правки таблицы закрыты, текст задач остаётся как есть.

Уже зафиксировано: исключения модели архитектора живут в одной таблице шагов, соседние тексты только на неё ссылаются.

План правит правило назначения моделей. Сверка уже написанных задач идёт на модели чата. Сверка «правка расширяет прошлый договор или отменяет его» стоит на той же лестнице, что независимый разбор постановки.

В этой сборке самой сильной модели в перечне вызова нет, поэтому на экране эта сверка совпадёт с сегодняшней тяжёлой. Приёмка смотрит на текст лестницы в таблице.

**Следующий шаг:** `/opsx:apply model-tier-by-step`

Полный отчёт: openspec/changes/model-tier-by-step/reports/verification-2026-09-23-2.md

Код конфигурации этот план не трогает. Меняются тексты правил kit: одна таблица шагов архитектора и отсылки к ней из соседних правил.

## Что меняется в постановке

**Расширение / конфигурация:** нет. Меняются правила kit.

**Точки изменения:**

- `.cursor/rules/model-selection.mdc` — существующая таблица закрытой эскалации расширяется строками шагов, второй таблицы нет.
- `.cursor/skills/openspec-verify-change/SKILL.md` — запуск сверки задач без явной модели и отсылка вместо пересказа лестницы.
- `.cursor/rules/tool-name-guard.mdc`, `.cursor/rules/architect-gate.mdc`, `.cursor/rules/verified-cause-gate.mdc` — отсылки к той же таблице.
- `.cursor/skills/1c-agent-patterns/architect.md`, `.cursor/skills/1c-agent-patterns/SKILL.md`, `AGENTS.md` — свой перечень моделей заменяется отсылкой.

**Что остаётся как сейчас:** модель проверки кода, упрощения, обследования, разбора трассы, написания кода и согласованности срезов. Файлы бюджета чата не меняются.

**Связанные ADR / KB / архив:** архив `2026-08-18-kit-evolution-models-economy-profiles`. Отмена цели «не звать отсутствующий слаг» не заявляется. Базы знаний в kit нет.

### К сведению

- В описании второго куска плана в design не назван файл проверки постановки, хотя задача на него есть. На выполнение это не влияет.
- Самосверка слага описана в решении и в проверке по тексту, отдельной строки «переписать раздел самосверки» нет. Исполнитель читает решение вместе с задачей.
- Часть регрессионных сценариев названа в задачах и не продублирована в блоке срезов design. Покрытие приёмки от этого не теряется.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1:** PASS. Чекбоксы и маркеры срезов на месте. Автоправок нет. Хэш `tasks.md` совпал с `verification-2026-09-23.md`.
- **Layer 2:** PASS. QC переиспользован: `reports/quality-control-2026-09-23.md`, вердикт OK. Spec, задачи и блок `## Slices` не менялись. User Task Contract: none. External validity: секции реестра нет; новый `## Extend — 2026-09-23 (loop)` — ответ по форме записи без `authority` и `external_contract_id`, детектор молчит. Code-truth pre-apply: символов 1С нет. Precedent: INFO `precedent-documented`, хэш spec совпал.
- **Layer 2.5:** PASS. AcceptLoop = 0. PatchRounds = 3 (три секции Extend меняли задачи; четвёртая, loop, задачи не меняла). Порог 3 уже срабатывал в `verification-2026-09-23.md`. Закрытие: `reports/architecture-loop-redesign-2026-09-23.md` существует с прошлого прогона, записей `awaiting-acceptance` нет и после отчёта не появлялись, решение пользователя — minimal, текст задач не менять.
- **Layer 3:** WARNING. Why покрыт двумя MODIFIED requirements. У каждого requirement есть сценарии. `scenario-orphan-slice` сохранён: часть регрессионных сценариев есть в `tasks.md` и не все перечислены в `design.md` ## Slices. Хэши proposal и spec совпали, пересчёт не меняет предупреждение. Implementation-leak маркеров в THEN нет. `comment_suffix` пуст.
- **Layer 4:** SKIPPED-novelty. Единственная дельта `design.md` — предложение в «Решения verify (зафиксировано)» о закрытии повторных правок. Секции Decisions и Behavior Contract байт-в-байт прежние: снятие этого предложения возвращает хэш файла `cb98b658…` из прошлого снимка. Хэш оси `ff282a9e…` сохранён. Профильного триггера нет. Прошлый разбор `reports/design-challenge-2026-09-22-3.md` остаётся в силе; повторный форум не запускался.
- **Layer 5:** PASS. Хэш текста задач совпал. Переиспользован `reports/architecture-task-readiness-2026-09-23.md`, вердикт ГОТОВО. Новый вызов не запускался.

### Каскад дельты

- **verify_depth:** incremental. Решение пользователя по петле принято, ось не менялась, локальность доказана одним предложением вне оси и секцией debug.
- **recomputed:** внешняя валидность, петля приёмки, хэши входов.
- **reused:** гигиена, QC, code-truth, precedent, трассировка Why, design-challenge, task-readiness.
- **escalated:** нет.

### Авто-исправлено (Layer 1)

не применялось

### Universal policy self-check

Реестр внешнего контракта не создавался. Авторитет по прозе не угадывался. Поля `confirmed_by: user`, `open_decision_id` и `decision_round` этим прогоном не менялись. `repair_attempt` сброшен в 0 после решения пользователя и вердикта GO.

## Источники

- `openspec/changes/model-tier-by-step/reports/quality-control-2026-09-23.md` (reused)
- `openspec/changes/model-tier-by-step/reports/design-challenge-2026-09-22-3.md` (reused, axis unchanged)
- `openspec/changes/model-tier-by-step/reports/architecture-task-readiness-2026-09-23.md` (reused)
- `openspec/changes/model-tier-by-step/reports/architecture-loop-redesign-2026-09-23.md` (closure)
- `openspec/changes/model-tier-by-step/reports/verification-2026-09-23.md` (предыдущий снимок)
- Алерты: `scenario-orphan-slice`, `precedent-documented`
