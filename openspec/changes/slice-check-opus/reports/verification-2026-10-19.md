---
verify_mode: pre-apply
change: slice-check-opus
date: 2026-10-19
verdict: GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: PASS
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions: []
  refuted_premises: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-10-19T15:23:29+09:00"
    design.md: "2026-10-19T15:51:13+09:00"
    tasks.md: "2026-10-19T15:51:04+09:00"
    debug.md: "2026-10-19T15:51:28+09:00"
    specs/subagent-model-mapping/spec.md: "2026-10-19T15:24:20+09:00"
  last_challenge_at: "2026-10-19T15:43:39+09:00"
  artifact_hashes:
    proposal.md: "3185748c479fd3493b376b15e403c8d051f4b61d56e60ce9b9bb4e13b72e77f6"
    design.md: "8f792b1dd679453f45f2b8ba4d86a33b96bdb4464d6c6ab517e94025c9adc734"
    design.md#axis: "a413f2d4e669f4da1cd5f3ceee5c895b3be9fd702d79e436fb4cb084927a2acf"
    tasks.md: "5fc2e90bd987b6c7f24c32e71849881cd170bf4d261c91b7bce45d49591f0d97"
    tasks.md#normalized: "5fc2e90bd987b6c7f24c32e71849881cd170bf4d261c91b7bce45d49591f0d97"
    specs/subagent-model-mapping/spec.md: "d17b90a5d8d5c98b1bb8cf944de324e56cc6eeca2a416a8f912570eec1b50e9c"
    debug.md#without-slice-gate: "cb9f0ff645dc3fe083be7ddbf0ad8382d980bc5b8e78d12f6a7a3a7c8c5d39a5"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints: {}
  rules_versions:
    .cursor/skills/openspec-verify-change/SKILL.md: "aa3c2f74b92e0b1e1119378e4dbd57a2c101336e93f6133bc3fef57827cc9de5"
    .cursor/skills/openspec-extend-change/SKILL.md: "a307c68b009b7857032d4aebb291db697dc3b4abddee5f6d9c3b82ce2cf3d1da"
    .cursor/rules/vertical-slices.mdc: "b587d2c2fc0b91f33b9f8eef577af47af0f861aef2fba6d5dac34e904061ca4c"
    .cursor/rules/openspec-specs-gate.mdc: "14459abbd63cdd7140cd58b8ac7d0321a563c29999d1e026805e37ec37a76610"
    .cursor/rules/code-truth-gate.mdc: "bf8b7f6e9695a9f36b513faff3d9ba78499f283ebf2aa0ef86cacec957b9754f"
    .cursor/rules/precedent-regression-gate.mdc: "875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641"
    .cursor/rules/architect-gate.mdc: "733c4498f4bcded131a12f0a44818254b5da077af3438a51240a1e8ab5e9f000"
  check_cache:
    hygiene-checkboxes@tasks: PASS
    slice-gate-markers@S1: PASS
    user-task-contract@S1: PASS
    external-validity@change: PASS
    scenario-coverage@S1: PASS
    code-truth@change: PASS
    precedent-regression@change: "INFO precedent-documented"
    loop-detection@S1: PASS
    problem-solution-trace@change: PASS
    design-challenge@axis: "CHALLENGE repaired G1-G4"
    task-readiness@S1: "PASS trigger-not-fired"
    premise-reconciliation@change: PASS
    simplicity-check@design-challenge: "not required"
  invalidation_map:
    hygiene-checkboxes: first-full
    slice-gate-markers: first-full
    user-task-contract: first-full
    external-validity: first-full
    scenario-coverage: first-full
    code-truth: first-full
    precedent-regression: first-full
    loop-detection: first-full
    problem-solution-trace: first-full
    design-challenge: first-full
    task-readiness: "D7 profile trigger did not fire"
  classifier_note: "Layer 4 CHALLENGE: G1-G4 implementation_invariant. Repair Loop attempt 1 wrote them into design.md and S1.2. Observable rule unchanged (multi-slice Opus 5, single-slice chat, empty Opus 5 stays on chat). Post-repair recheck did not reopen those themes and did not launch a second design-challenge. QC reused: scenario title set and Primary text unchanged. Verdict GO by the repair exception. repair_attempt reset to 0 on GO."
---

## Резюме для разработчика

slice-check-opus — можно запускать apply. Проверка заявки из нескольких срезов назначается на старшую модель семейства Opus, мажор 5.

Правило назначения: заявка из нескольких частей проверяется старшей моделью Opus 5, даже если в этот запуск попал один срез. Заявка из одной части остаётся на модели чата. Если Opus 5 в списке нет, проверка идёт на модели чата. Ревью кода остаётся на старшей модели Gemini.

Подправил в постановке: записал, зачем отдельная модель остаётся после ухода GPT, и оставил в профиле чата GPT прежнюю формулировку триггера — добавляется только строка, что правило назначения этот профиль не назначает.

**Следующий шаг:** `/opsx:apply slice-check-opus`

Если Opus 5 нет в списке вызова, проверка нескольких срезов пойдёт на модели чата.

Полный отчёт: openspec/changes/slice-check-opus/reports/verification-2026-10-19.md

Конфигурация 1С не меняется. Правки — в `.cursor/rules/model-selection.mdc` и `.cursor/rules/model-gpt56.mdc`.

## Что меняется в постановке

**Расширение / конфигурация:** kit, каталога `src/` нет.

**Точки изменения:**

- `.cursor/rules/model-selection.mdc` — пять мест: строка роли проверки срезов, абзац под таблицей ролей, строка «Контроль нескольких срезов» в таблице старшей модели, самосверка, цепочка этой проверки.
- `.cursor/rules/model-gpt56.mdc` — одна строка после «Когда загружать»: ни одна роль правила назначения этот профиль не назначает. Слова «Primary GPT-5.6» остаются.

**Что НЕ меняется:** заявка из одного среза на модели чата; ревью кода на Gemini; Fable только у архитектора; таблица шагов архитектора; ADR-0011; ADR-0004.

**Связанные ADR / KB / архив:** архив `2026-10-15-verify-model-bands` (клетка проверки нескольких срезов переносится с GPT на Opus явно). Базы знаний в репозитории нет.

### К сведению

- Вводная фраза таблицы старшей модели по-прежнему говорит про вызов архитектора. В таблице уже есть ревью, появится строка контроля срезов. Пять мест правки эту фразу не включают.
- Восемь прежних сценариев сверяются чтением правила, отдельной строки в приёмке у них нет.

## Технический аудит (для движка OpenSpec)

- **Layer 1 (Hygiene):** PASS. Чекбоксы у S1.1, S1.2, S1.3, S1.accept. Один `<!-- slice-gate -->`. Пустых буллетов и незакрытых fences нет. `form_mode: n/a`, задач на форму нет. `comment_suffix` пуст.
- **Layer 2 (Internal Coherence):** PASS. External validity: секции реестра нет, события из закрытого перечня нет. `## Extend —` — internal repair, не указание заказчика. User Task Contract: none (повтор после правки S1.2). Code-truth: технических имён процедур нет, `openspec/project.md` нет. Precedent: `precedent-documented` INFO — отмена GPT → Opus и снятие «Opus не подставляется» записаны в `## Blast Radius`; требование «Fable только как закрытая эскалация архитектора» в дельту не входит; Supersedes нет; `_index.yaml` нет. Опора на прошлый контроль среза: `reports/quality-control-2026-10-19.md` (OK, 12/12). Набор названий сценариев и текст Primary не менялись, новый полный контроль с нуля не создавался.
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` без `## Slice Gate Decisions`. `TopicReopen` и `PatchRounds` не сработали.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт требованием мэппинга. У обоих требований есть Scenario. Четыре изменённых сценария названы в `design.md` ## Slices; восемь прежних закрыты S1.3 (подобрано в Layer 2, не системный сирота). Маркеров implementation-leak в THEN нет. `process-only-marker-suffix` не сработал.
- **Layer 4 (Independent Challenge):** CHALLENGE, затем repair. Отчёт `reports/design-challenge-2026-10-19.md`. Триггер: первый прогон и конфликт с архивным контрактом. Ось `design.md#axis` — секции `## Decisions` и `## Behavior Contract`. Classifier: G1–G4 — `implementation_invariant` (дописать причину отдельной модели, заменить довод против Gemini, не расходиться с роутером профиля, фразу таблицы оставить в рисках). Развилка Opus/Gemini в чат не выносилась: текст закрывает её без смены наблюдаемого правила. Второго разбора нет. `last_challenge_at` обновлён. Секции Premise conflicts нет.
- **Layer 5 (Implementation Readiness):** PASS. Вызов task-readiness не запускался: задачи — правки текстов kit, без неизвестной композиции перехватов, ручной конфигурации, неизвестной сигнатуры и неподтверждённого API. Маркеров ручной конфигурации нет.
- **Simplicity:** для `mode: design-challenge` строка не требуется.
- **recomputed:** все контроли первого прогона; после repair заново hygiene, user-task-contract, precedent (Blast Radius уточнён, семантика отмены та же).
- **reused:** scenario-coverage и контроль среза S1 — `reports/quality-control-2026-10-19.md`.
- **escalated:** design-challenge (первый прогон, конфликт с архивом `2026-10-15-verify-model-bands`). QC без явной модели: в заявке один срез.

## Источники

- `openspec/changes/slice-check-opus/reports/quality-control-2026-10-19.md`
- `openspec/changes/slice-check-opus/reports/design-challenge-2026-10-19.md`
- Алерты: `precedent-documented` (INFO). Блокирующих нет.
- Классификатор: G1–G4 `implementation_invariant`, в чат не выносились
