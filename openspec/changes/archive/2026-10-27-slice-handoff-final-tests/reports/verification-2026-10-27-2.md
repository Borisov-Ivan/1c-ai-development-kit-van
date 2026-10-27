---
verify_mode: pre-apply
change: slice-handoff-final-tests
date: 2026-10-27
verdict: GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: APPROVE
  layer_5_implementation_readiness: PASS
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions:
    - id: final_test_when_no_open_work
      summary: "Финальный тест — сдача, после которой ни у одного среза не остаётся открытых рабочих задач. Пока у раннего открыты доработки, на последнем по порядку сказано, что финал после них, и ответ «отложить» остаётся. Если эти доработки закрыли последние работы, финальной становится сдача раннего среза."
      closed_at: "2026-10-27"
      source: verify-user-answer
      confirmed_by: user
  refuted_premises: []
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-10-27T11:38:17"
    design.md: "2026-10-27T11:53:19"
    tasks.md: "2026-10-27T11:53:31"
    specs/chat-surface-clarity/spec.md: "2026-10-27T11:53:18"
    specs/kit-protocol-coherence/spec.md: "2026-10-27T11:38:59"
    debug.md: "2026-10-27T11:53:36"
  last_challenge_at: "2026-10-27T11:50:00"
  artifact_hashes:
    proposal.md: "a7d14610a5ab2a1d15c09bb66d34b9bdcc9aea5483d241752be4455a89d233c7"
    design.md: "dc3339f8d9f7a6d92a2e9eecfe61bb20270a63c2067d4bba3224a1d552553028"
    design.md#axis: "323603ff07637df1dd92891dd23cd21a5e483aec05484d4c46c85213ad7674d0"
    tasks.md: "b61f1e26be1f76a5b3d3fcefc25843caaafdfaba6b6964834022874b14f87c24"
    tasks.md#normalized: "b61f1e26be1f76a5b3d3fcefc25843caaafdfaba6b6964834022874b14f87c24"
    specs/chat-surface-clarity/spec.md: "c0ab46bc7331afdbc3248845a8d80b4e8db70339fd8fc9b6ac8a0ab08096faf3"
    specs/kit-protocol-coherence/spec.md: "19207f94a2f62e562e1ff2474d894a55e31aad2b50a7b97e59cc263ac21cab8c"
    debug.md: "8d94aff4fe69f8e6c667e418aae8a5b43fa6f513b04fcc76c0f11b039eed1ff1"
    debug.md#without-slice-gate: "8d94aff4fe69f8e6c667e418aae8a5b43fa6f513b04fcc76c0f11b039eed1ff1"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints:
    final_test_when_no_open_work: "e6c5132958cc21e5381beb201f741f5011b458597b75ba6eff68ad010f096563"
  rules_versions:
    .cursor/rules/vertical-slices.mdc: "0d47a83ca6e82756dc19bd9fbb0571522d65a5df0ea34d30109433993f62ab48"
    .cursor/rules/code-truth-gate.mdc: "bf8b7f6e9695a9f36b513faff3d9ba78499f283ebf2aa0ef86cacec957b9754f"
    .cursor/rules/precedent-regression-gate.mdc: "875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641"
    .cursor/rules/openspec-specs-gate.mdc: "14459abbd63cdd7140cd58b8ac7d0321a563c29999d1e026805e37ec37a76610"
    .cursor/rules/architect-gate.mdc: "733c4498f4bcded131a12f0a44818254b5da077af3438a51240a1e8ab5e9f000"
    .cursor/skills/openspec-verify-change/SKILL.md: "aa3c2f74b92e0b1e1119378e4dbd57a2c101336e93f6133bc3fef57827cc9de5"
  check_cache:
    hygiene-checkboxes|tasks.md|b61f1e26be1f76a5b3d3fcefc25843caaafdfaba6b6964834022874b14f87c24: PASS
    slice-gate-markers|tasks.md|b61f1e26be1f76a5b3d3fcefc25843caaafdfaba6b6964834022874b14f87c24: PASS
    user-task-contract|tasks.md|b61f1e26be1f76a5b3d3fcefc25843caaafdfaba6b6964834022874b14f87c24: PASS
    external-validity|none: PASS
    scenario-coverage|S1: PASS
    code-truth|pre-apply|no-bsl-symbols: PASS
    precedent-regression|chat-surface-clarity+kit-protocol-coherence: INFO
    loop-detection|S1: PASS
    problem-solution-trace|S1: PASS
    design-challenge|axis|323603ff07637df1dd92891dd23cd21a5e483aec05484d4c46c85213ad7674d0: APPROVE
    task-readiness|tasks.md|b61f1e26be1f76a5b3d3fcefc25843caaafdfaba6b6964834022874b14f87c24: skipped-no-trigger
    premise-reconciliation|design-challenge-2026-10-27-3: PASS
    simplicity-check|architecture-new-2026-10-27: missing
  invalidation_map:
    hygiene-checkboxes: recomputed
    slice-gate-markers: recomputed
    user-task-contract: recomputed
    external-validity: recomputed
    scenario-coverage: recomputed
    code-truth: recomputed
    precedent-regression: recomputed
    loop-detection: recomputed
    problem-solution-trace: recomputed
    design-challenge: repaired-same-rule
    task-readiness: skipped-no-trigger
    premise-reconciliation: recomputed
    simplicity-check: recalculated
---

## Резюме для разработчика

slice-handoff-final-tests — можно запускать apply.

Уже зафиксировано: финальный тест — это сдача, после которой по срезам не остаётся открытых работ. Пока у более раннего среза идут доработки, на последнем в списке остаётся ответ «отложить до финального теста».

На сдаче в чате видно, какой это срез и идёт ли финальный тест. В том же сообщении — что вошло и основные тесты. Вопрос про архив в этом ходе не задаётся, если у раннего среза ещё открыты работы. Меняются тексты kit.

**Следующий шаг:** `/opsx:apply slice-handoff-final-tests`

Если последние работы закрыл срез без своей сдачи, отдельной карточки финального теста не будет. Слова вопроса про архив прежние: он приходит после принятия, когда открытых работ и открытых приёмок уже нет. Задачи вне срезов этот момент не откладывают.

Полный отчёт: openspec/changes/slice-handoff-final-tests/reports/verification-2026-10-27-2.md

План правит абзац сдачи в правиле чата и ссылки на него в скилле разработки, правиле срезов, проверке и снимке состояния. Объектов конфигурации нет.

## Что меняется в постановке

**Расширение / конфигурация:** нет. Меняются тексты kit.

**Точки изменения:**

- Абзац правила чата у передачи на приёмку — фраза места, состав сообщения, набор ответов, определение финального теста.
- Скилл разработки — расчёт этого определения, разбор ответа, вопрос архива после принятия, возобновление финальной карточки, шаблон файла сдачи.
- Правило лимита чата — блок основных тестов не сжимается до одной фразы.
- Проверка, снимок состояния и сценарии изолированного чата — ссылки на тот же абзац.

**Что НЕ меняется:** слова вопроса про архив и предрелизное ревью; необязательные сценарии остаются в файле сдачи; пауза, пока объекты ещё не созданы, не называется финальным тестом.

**Связанные ADR / архив:** ADR-0001 расширяется: блок основных тестов выводится за короткий потолок, таблицы остаются в файле. Архив `2026-10-15-slice-pause-verify-clarity`: дробь «N из M», оборот «принять позже, следом архив», третий ответ на финале, вопрос «какой срез» на финале и строка о принятии без проверки на последнем по порядку заменяются осознанно. Цель «не открывать список задач, чтобы понять место» сохраняется.

### К сведению

- В отчёте разбора плана при создании заявки нет сравнения более простого варианта. На запуск это не влияет: выбран один абзац-хозяин и ссылки вместо копий.
- В шапке приёмки сказано «ручная сверка трёх карточек», образцов в задаче пять. Закрывает срез только карточка одного среза.
- Якорь предпосылки в журнале решений по-прежнему указывает на прошлый разбор. Живой текст скилла разработки эту предпосылку подтверждает. Запись ответа заказчика не переписывалась.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы есть, один `slice-gate`, незакрытых блоков нет, `form_mode: n/a`.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-10-27-4.md`, вердикт OK, алертов нет, 39/39. Заголовки сценариев есть в `design.md` ## Slices. `precedent-regression`: INFO `precedent-documented` (Blast Radius закрывает отмену дроби, третьего ответа на финале, «какой срез», «после трёх», позиционный триггер архива и строку предупреждения без прогона на последнем по порядку; ADR-0001 не Supersedes). `code-truth`: имён процедур нет, `openspec/project.md` в kit нет. User Task Contract: нарушений нет. Внешней валидности: секции External Contract Ledger нет; записи Extend сохраняют уже данный ответ и внутренние дописки, нового события высокого авторитета нет.
- **Layer 2.5 (Loop Detection):** PASS. AcceptLoop 0. PatchRounds 3 (три секции Extend, все с идентичностью G*). TopicReopen < 2. Стоп «оставить текст или переписать срез» не сработал.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт требованиями. У каждого требования есть сценарий. У среза есть рабочие задачи и один `S1.accept`. 39 сценариев названы в ## Slices. Маркеров implementation-leak в THEN нет. `comment_suffix` пуст.
- **Layer 4 (Independent Challenge):** файл `reports/design-challenge-2026-10-27-3.md` имеет вердикт CHALLENGE. Равноправных развилок нет, закрытая ось держится. Все открытые пункты классификатор отнёс к дописке без смены правила. Дописки внесены в этом прогоне (сценарии под старыми именами, строка Blast Radius, область предиката, возобновление финала). Повторный независимый разбор после этой дописки не назначался: наблюдаемый исход карточки финала тот же. Для вердикта слой не блокирует apply. `last_challenge_at` обновлён.
- **Layer 5 (Implementation Readiness):** PASS. Вызов не запускался: нет неизвестной композиции перехватов, ручной настройки метаданных, неизвестной сигнатуры и неподтверждённого API. Маркеров ручной конфигурации нет.

### Post-challenge classifier

- **G1–G12** предыдущих прогонов — закрыты текстом либо сужение дописано. G11 отложен: якорь внутри записи ответа заказчика, предпосылка не опровергнута.
- **G13, G14** — `implementation_invariant`. Дописаны в tasks, design и delta spec. В чат не выносились.
- Альтернатива «финал по позиции» — `reopen-blocked`, без нового факта против закрытого решения. Drop.
- `repair_attempt` в этом прогоне дошёл до 2 и сброшен в 0 вместе с вердиктом GO.

### Каскад дельты

- **verify_depth:** full. Ось и сценарии изменились относительно `verification-2026-10-27.md`.
- **recomputed:** гигиена, покрытие сценариев, внешняя валидность, прецедент, трассировка Why, петля, предпосылка.
- **reused:** нет прошлого контроля среза: набор сценариев вырос с 26 до 39.
- **escalated:** quality-controller без явной модели (один срез); design-challenge на Fable из-за риска прецедента, два прогона. task-readiness не запускался. После второй дописки новый design-challenge не запускался.

### Авто-исправлено (Layer 1)

не применялось

### Контроль простоты

`reports/architecture-new-2026-10-27.md`, `mode: plan-review`: секции `## Simplicity Check` нет. Строка «к сведению». Отчёты `design-challenge` и `scope-coherence-audit` эту секцию не требуют.

### Сверка предпосылок

`reports/architecture-extend-coherence-2026-10-27.md` и `reports/design-challenge-2026-10-27-3.md` упоминают якорь предпосылки. Секции `## Premise conflicts` нет. Код подтверждает предпосылку. `refuted_premises` пуст.

## Источники

- `openspec/changes/slice-handoff-final-tests/reports/quality-control-2026-10-27-4.md`
- `openspec/changes/slice-handoff-final-tests/reports/design-challenge-2026-10-27-3.md`
- `openspec/changes/slice-handoff-final-tests/reports/design-challenge-2026-10-27-2.md`
- `openspec/changes/slice-handoff-final-tests/reports/verification-2026-10-27.md`
- Алерты: `precedent-documented`
