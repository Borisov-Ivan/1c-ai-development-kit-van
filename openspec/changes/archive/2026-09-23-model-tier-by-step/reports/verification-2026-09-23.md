---
verify_mode: pre-apply
change: model-tier-by-step
date: 2026-09-23
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: acceptance-loop-detected
  layer_3_problem_solution: WARNING
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: PASS
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 2
  accepted_tasks: []
  closed_decisions:
    - id: architect_step_model_table
      summary: "Исключения модели архитектора живут в одной таблице шагов. Строка роли и соседние тексты только ссылаются на неё."
      closed_at: "2026-09-22"
      source: verify-user-answer
      confirmed_by: user
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "Зафиксировать итог повторных правок постановки: оставить текст как есть."
  artifacts_mtime:
    proposal.md: "2026-09-22T08:33:04Z"
    design.md: "2026-09-23T01:00:21Z"
    tasks.md: "2026-09-23T01:01:42Z"
    specs/subagent-model-mapping/spec.md: "2026-09-23T01:00:25Z"
  last_challenge_at: "2026-09-23T10:08:00+09:00"
  artifact_hashes:
    proposal.md: "2ab1f8511c94638ebac2fb2e4529b636d1c90b38628a40abf3f8f80732150a78"
    design.md: "cb98b658416cf8127e4aa3f3ab67f495783870017d60d37c98d42928676e333f"
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
    loop-detection@S1-S2: "FAIL|patch-rounds-3"
    problem-solution-trace@proposal-specs: "WARNING|scenario-orphan-slice-regression"
    design-challenge@axis: "CHALLENGE-repaired|ff282a9e16864dda046514a8054c1c3a503ed83d6f33b4704d7388e449cfc025"
    task-readiness@all: "PASS|architecture-task-readiness-2026-09-23"
  invalidation_map:
    hygiene-checkboxes: "tasks rewritten"
    slice-gate-markers: "tasks rewritten"
    user-task-contract: "tasks rewritten"
    external-validity: "extend sections, no EC fields"
    scenario-coverage: "tasks and spec rewritten"
    code-truth: "full"
    precedent-regression: "spec modified"
    loop-detection: "three Extend sections changed tasks"
    problem-solution-trace: "proposal and spec rewritten"
    design-challenge: "axis hash changed after user choice"
    task-readiness: "task text changed"
---

## Резюме для разработчика

model-tier-by-step — до старта нужно зафиксировать итог повторных правок.

Уже зафиксировано: исключения модели архитектора живут в одной таблице шагов, соседние тексты только на неё ссылаются.
Новый вопрос: не переписывать эту таблицу ещё раз. Прежний выбор формы не пересматривается.

Оба куска плана правились три раза, и ни один ещё не принят. Каждый проход находил ещё одну фразу, которая снова отправляла сверку уже написанных задач на тяжёлую модель. Сейчас задачи можно выполнять как написано. Собирать их заново в один шаг не нужно: это перепишет уже согласованный текст без нового факта.

**Следующий шаг:** `/opsx:extend model-tier-by-step --from-architecture reports/architecture-loop-redesign-2026-09-23.md`

План правит правило назначения моделей: сверка уже написанных задач идёт на модели чата, а сверка «правка не отменяет прошлый договор» — по той же лестнице, что независимый разбор постановки. Код конфигурации не затрагивается.

В этой сборке самой сильной модели в перечне вызова нет, поэтому лестница сверки с прошлым договором на экране совпадёт с сегодняшней тяжёлой моделью. Приёмка смотрит на текст лестницы.

## Что меняется в постановке

**Расширение / конфигурация:** нет. Меняются правила kit.

**Точки изменения:**

- `.cursor/rules/model-selection.mdc` — существующая таблица закрытой эскалации расширяется строками шагов, второй таблицы нет.
- `.cursor/skills/openspec-verify-change/SKILL.md` — запуск сверки задач без явной модели и отсылка вместо пересказа лестницы.
- `.cursor/rules/tool-name-guard.mdc`, `.cursor/rules/architect-gate.mdc`, `.cursor/rules/verified-cause-gate.mdc` — отсылки к той же таблице.
- `.cursor/skills/1c-agent-patterns/architect.md`, `.cursor/skills/1c-agent-patterns/SKILL.md`, `AGENTS.md` — свой перечень моделей заменяется отсылкой.

**Что НЕ меняется:** модель проверки кода, упрощения, обследования, разбора трассы, написания кода и согласованности срезов. Файлы бюджета чата не меняются.

**Связанные ADR / KB / архив:** архив `2026-08-18-kit-evolution-models-economy-profiles`. Отмена цели «не звать отсутствующий слаг» не заявляется. Базы знаний в kit нет.

### К сведению

- В описании второго куска плана в design не назван файл проверки постановки, хотя задача на него есть. На выполнение это не влияет.
- Самосверка слага описана в решении и в проверке по тексту, отдельной строки «переписать раздел самосверки» нет. Исполнитель читает решение вместе с задачей.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1:** PASS. Чекбоксы и маркеры срезов на месте. Автоправок гигиены нет.
- **Layer 2:** PASS. QC: `reports/quality-control-2026-09-23.md`, вердикт OK, критерии 1–6, 8, 8b, 9–11 PASS. User Task Contract: none. External validity: секции реестра нет; ответы в журнале без `authority` и `external_contract_id` — обычная workflow-развилка, детектор молчит. Code-truth pre-apply: символов 1С нет. Precedent: два архива capability, `## Blast Radius` есть — INFO `precedent-documented`.
- **Layer 2.5:** `acceptance-loop-detected`. AcceptLoop = 0. PatchRounds = 3 по секциям `## Extend —` для обоих срезов, порог 3. Отчёт: `reports/architecture-loop-redesign-2026-09-23.md`. Рекомендация: minimal. Записи `awaiting-acceptance` нет, поэтому закрытие отчётом на этом прогоне не применялось: отчёт создан этим же прогоном.
- **Layer 3:** WARNING. Why покрыт двумя MODIFIED requirements. У каждого requirement есть сценарии. `scenario-orphan-slice`: часть регрессионных сценариев названа в `tasks.md`, в `design.md` ## Slices перечислены не все. Implementation-leak маркеров в THEN нет. `comment_suffix` пуст.
- **Layer 4:** CHALLENGE в `reports/design-challenge-2026-09-22-3.md`. Classifier: все пункты `implementation_invariant`, архитектурных развилок нет, `reopen-blocked` без нового факта отфильтрован. Repair attempt 2 внёс текст. Повторный полный разбор после repair не запускался: класс repair запрещает новый форум гипотез. Остатка развилки нет. `last_challenge_at` обновлён, потому что CHALLENGE ушёл в repair.
- **Layer 5:** PASS. `reports/architecture-task-readiness-2026-09-23.md`, вердикт ГОТОВО. Критических дыр нет. INFO-1 и INFO-2 не блокируют. Первый вызов с Primary архитектора вернул ошибку выбора модели; повтор без `model=` сохранил отчёт. Режим сессии после этого — без платной модели.

### Каскад дельты

- **verify_depth:** full после user-extend и двух repair (repair сбрасывает incremental).
- **recomputed:** гигиена, срезы, трассировка, готовность задач, петля.
- **reused:** нет.
- **escalated:** QC; design-challenge; task-readiness; deep-analysis петли.

### Авто-исправлено (Layer 1)

не применялось

### Universal policy self-check

Реестр внешнего контракта не создавался. Авторитет по прозе не угадывался. Поля `confirmed_by: user` и `decision_round` repair не менял.

## Источники

- `openspec/changes/model-tier-by-step/reports/quality-control-2026-09-23.md`
- `openspec/changes/model-tier-by-step/reports/design-challenge-2026-09-22-3.md`
- `openspec/changes/model-tier-by-step/reports/architecture-task-readiness-2026-09-23.md`
- `openspec/changes/model-tier-by-step/reports/architecture-loop-redesign-2026-09-23.md`
- Алерты: `acceptance-loop-detected`, `scenario-orphan-slice`, `precedent-documented`
