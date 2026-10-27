---
verify_mode: pre-apply
change: slice-handoff-final-tests
date: 2026-10-27
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: WARNING
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: WARNING
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
  open_known_questions:
    - "Когда сдаётся последний срез, а у более раннего ещё открыты доработки: финальный тест после закрытия этих работ или последний срез в списке уже финал"
  artifacts_mtime:
    proposal.md: "2026-10-27T09:39:05"
    design.md: "2026-10-27T09:54:00"
    tasks.md: "2026-10-27T09:53:57"
    specs/chat-surface-clarity/spec.md: "2026-10-27T09:40:29"
    specs/kit-protocol-coherence/spec.md: "2026-10-27T09:40:46"
    debug.md: "2026-10-27T10:21:46"
  last_challenge_at: "2026-10-27T10:14:00"
  artifact_hashes:
    proposal.md: "f02e798f7f52870d8c1738f6c96ffd96d9089a32d00683c66296a3f8a9cbf814"
    design.md: "f2622e5903d589a7a27e7943fc0bd8bb1f5d2be1a480bf242ccbfd86adcd1168"
    design.md#axis: "84f88fb8cd42efb19c7b8054e40d078ec6e191061966322df31d0f2d575b03b2"
    tasks.md: "bea634752620bcbf01b2ab3838da4044e762748c869aea27941196cab4bd074a"
    tasks.md#normalized: "bea634752620bcbf01b2ab3838da4044e762748c869aea27941196cab4bd074a"
    specs/chat-surface-clarity/spec.md: "0e2540a0186ec1ba0bd8922583c058159f56de5ecb382e5c7ed297029f665540"
    specs/kit-protocol-coherence/spec.md: "7ea6808d3a39a99c0ce47c4d15efe9d13b99cdb5ac07f00ac16762a403f8782a"
    debug.md: "59ed2f7e80e2db951954681859cc23a8e6ae3f077bbe434bdc4f0cd82654b59b"
    debug.md#without-slice-gate: "59ed2f7e80e2db951954681859cc23a8e6ae3f077bbe434bdc4f0cd82654b59b"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints: {}
  rules_versions:
    .cursor/rules/vertical-slices.mdc: "0d47a83ca6e82756dc19bd9fbb0571522d65a5df0ea34d30109433993f62ab48"
    .cursor/rules/code-truth-gate.mdc: "bf8b7f6e9695a9f36b513faff3d9ba78499f283ebf2aa0ef86cacec957b9754f"
    .cursor/rules/precedent-regression-gate.mdc: "875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641"
    .cursor/rules/openspec-specs-gate.mdc: "14459abbd63cdd7140cd58b8ac7d0321a563c29999d1e026805e37ec37a76610"
    .cursor/rules/architect-gate.mdc: "733c4498f4bcded131a12f0a44818254b5da077af3438a51240a1e8ab5e9f000"
    .cursor/skills/openspec-verify-change/SKILL.md: "aa3c2f74b92e0b1e1119378e4dbd57a2c101336e93f6133bc3fef57827cc9de5"
  check_cache:
    hygiene-checkboxes|tasks.md|bea634752620bcbf01b2ab3838da4044e762748c869aea27941196cab4bd074a: PASS
    slice-gate-markers|tasks.md|bea634752620bcbf01b2ab3838da4044e762748c869aea27941196cab4bd074a: PASS
    user-task-contract|tasks.md|bea634752620bcbf01b2ab3838da4044e762748c869aea27941196cab4bd074a: PASS
    external-validity|none: PASS
    scenario-coverage|S1: WARNING
    code-truth|pre-apply|no-bsl-symbols: PASS
    precedent-regression|chat-surface-clarity+kit-protocol-coherence: INFO
    loop-detection|S1: PASS
    problem-solution-trace|S1: WARNING
    design-challenge|axis|84f88fb8cd42efb19c7b8054e40d078ec6e191061966322df31d0f2d575b03b2: CHALLENGE
    task-readiness|tasks.md|bea634752620bcbf01b2ab3838da4044e762748c869aea27941196cab4bd074a: skipped-no-trigger
    premise-reconciliation|none: PASS
    simplicity-check|architecture-new-2026-10-27: missing
  invalidation_map:
    hygiene-checkboxes: first-run
    slice-gate-markers: first-run
    user-task-contract: first-run
    external-validity: first-run
    scenario-coverage: first-run
    code-truth: first-run
    precedent-regression: first-run
    loop-detection: first-run
    problem-solution-trace: first-run
    design-challenge: first-run
    task-readiness: skipped-no-trigger
    premise-reconciliation: first-run
    simplicity-check: recalculated
---

## Резюме для разработчика

slice-handoff-final-tests — до старта нужен ваш выбор по логике финального теста.

**Что решить: называть ли сдачу последнего среза финальным тестом, если у более раннего среза ещё идут доработки**

План считает финальным тестом последний срез в списке. В сообщении будет сказано, что это финальный тест, и ответа «отложить до финального теста» не будет. Если по замечанию у раннего среза снова открыты задачи, эта фраза обещает, что проверять больше нечего, хотя доработки ещё впереди. От выбора зависит, останется ли третий ответ на такой карточке.

- **A. Финал после доработок** — пока у раннего среза открыты задачи, сообщение говорит, что финальный тест будет после них, и ответ «отложить до финального теста» остаётся. Пока работы идут, слово «финальный» на этой карточке не появляется.
- **B. Финал — последний срез в списке** — сообщение говорит, что это финальный тест, даже когда у раннего среза открыты доработки. Ответа «отложить» нет. Слово «финальный» значит место среза в списке.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify slice-handoff-final-tests`.

Полный отчёт: openspec/changes/slice-handoff-final-tests/reports/verification-2026-10-27.md

План меняет текст сдачи среза в правилах чата: словами, какой это срез и финальный ли тест, в том же сообщении — что вошло и основные тесты. Конфигурация 1С не меняется. Вопрос архива после принятия последнего среза остаётся отдельным сообщением.

## Решения до apply

### 1. Когда сдача последнего среза — финальный тест

**В чём проблема.** План называет финальным тестом последний срез по порядку в списке. Если у более раннего среза после замечания снова открыты задачи, карточка всё равно скажет, что это финальный тест, и уберёт ответ «отложить до финального теста».

**На что влияет.** Разработчик на сдаче либо видит, что проверять больше нечего, либо видит, что доработки раннего среза ещё впереди и финальный тест будет после них.

**Если выбрать A / B.** A — финальный тест только когда этот срез последний и у ранних срезов задачи закрыты; иначе в сообщении сказано, что финал после доработок, и третий ответ остаётся. B — финальный тест это последний срез в списке, даже при открытых доработках раннего; третьего ответа нет, и это записывается как осознанное допущение.

**Что в текстах сейчас.** Скилл разработки уже понимает «последний срез» как отсутствие следующего заголовка среза. План переносит это в фразу «это финальный тест» и снимает третий ответ на единственном и на последнем срезе.

**Что предлагает план.** На последнем срезе два ответа: принять или дать замечание. «Принять» закрывает этот срез и более ранние, чьи основные тесты стоят в том же сообщении. Случай открытых доработок раннего среза план не разбирает.

**Почему это развилка.** Оба варианта сохраняют состав сообщения, но по-разному отвечают на вопрос, можно ли ещё отложить тест. Это разный текст карточки, его нельзя дописать молча.

**Варианты решения.**

- **A. Финал после доработок** — финальный тест, когда срез последний по списку и у всех ранних срезов задачи закрыты. Иначе фраза говорит, что у раннего среза открыты доработки и финальный тест после них; ответ «отложить до финального теста» остаётся. Компромисс: на последнем по списку срезе третьего ответа может не быть, пока ранние доработки открыты.
- **B. Финал — последний срез в списке** — «финальный» значит место в списке. Сообщение говорит, что это финальный тест, третьего ответа нет, даже если у раннего среза открыты доработки. Компромисс: слово «финальный» не обещает, что работ больше нет.

**Влияет на:** текст сдачи и набор ответов под сообщением.

**Что изменится после выбора.** В постановке будет одно правило, когда карточка называет финальный тест и когда на ней остаётся ответ «отложить до финального теста». Уточнения, которые не меняют этот выбор, допишутся вместе с ним.

## Что меняется в постановке

**Расширение / конфигурация:** нет. Меняются тексты kit, не выгрузка 1С.

**Точки изменения:**

- Абзац правила чата у передачи на приёмку — фраза места словами, состав сообщения, набор ответов.
- Правило лимита чата — блок основных тестов не сжимается до одной фразы.
- Правило срезов, скилл разработки, карточка проверки, снимок состояния и сценарии изолированного чата — ссылки на этот абзац вместо своей копии трёх ответов и дроби «N из M».

**Что НЕ меняется:** вопрос архива и предрелизного ревью после принятия последнего среза; необязательные сценарии и таблица задач остаются в файле сдачи; пауза, пока объекты ещё не созданы, не называется финальным тестом.

**Связанные ADR / архив:** ADR-0001 (в чате коротко, таблицы в файле; блок основных тестов выводится за короткий потолок и это расширение, не отмена). Архив `2026-10-15-slice-pause-verify-clarity`: дробь «N из M», оборот «принять сейчас или позже, следом архив» и третий ответ на каждой сдаче заменяются осознанно, цель «не открывать список задач, чтобы понять место» сохраняется.

### К сведению

- В отчёте разбора плана нет сравнения более простого варианта с обоснованием. На запуск это не влияет: выбранный путь — один абзац-хозяин и ссылки вместо копий.
- В разделе срезов названы четыре требования, а не каждый заголовок сценария. Все 26 сценариев закрыты задачами или приёмкой этого среза.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы есть, один `slice-gate`, пустых буллетов и незакрытых блоков нет, `form_mode: n/a`, задач на форму нет.
- **Layer 2 (Internal Coherence):** WARNING. QC: `reports/quality-control-2026-10-27.md`, вердикт OK, алертов нет, 26/26. Оркестратор: `scenario-orphan-design` — в `design.md` ## Slices нет строки «Scenarios из spec» с заголовками сценариев. `precedent-regression`: INFO `precedent-documented` (Blast Radius закрывает отмену дроби, третьего ответа на финале, уточнения «какой срез» и «после трёх ответов»; ADR-0001 не Supersedes). `code-truth`: имен процедур нет, `openspec/project.md` в kit нет. User Task Contract: нарушений нет. Внешней валидности: секции External Contract Ledger нет, событий из закрытого перечня нет.
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` без Slice Gate Decisions и без `## Extend —`. AcceptLoop 0, PatchRounds 0, TopicReopen нет.
- **Layer 3 (Problem-Solution Trace):** WARNING. Why покрыт четырьмя требованиями; у каждого требования есть сценарий; у среза есть рабочие задачи и один `S1.accept`. `scenario-orphan-slice` — те же заголовки не перечислены в ## Slices, покрытие задачами есть, системного разрыва нет. Маркеров implementation-leak в THEN нет. `comment_suffix` пуст.
- **Layer 4 (Independent Challenge):** CHALLENGE. Отчёт: `reports/design-challenge-2026-10-27.md`. Триггер: первый pre-apply и риск прецедента (смена архивного контракта сдачи при заполненном Blast Radius). `last_challenge_at` обновлён.
- **Layer 5 (Implementation Readiness):** PASS. Вызов не запускался: нет неизвестной композиции перехватов, ручной настройки, неизвестной сигнатуры, новой межмодульной связи и неподтверждённого API. Маркеров ручной конфигурации нет.

### Post-challenge classifier

- **G1** — decision. Два наблюдаемых исхода: финал только после закрытия ранних работ либо финал = позиция в списке. В чат.
- **G2** — `implementation_invariant`. Карточку финала не отправлять, если набор показанных блоков ранних тестов не совпадает с ранними срезами, у которых работы закрыты, а приёмка открыта. Дописать в D3, требование «Конец среза один», S1.6 и S1.8.
- **G3** — `implementation_invariant`. «Принять» на финале для каждого закрытого им раннего среза пишет те же записи, что обычная приёмка: отметка приёмки, `## Slice Gate Decisions`, файл сдачи среза. Дописать в D3 и S1.8.
- **G4** — `implementation_invariant`. В затронутые тексты и задачи добавить копии, которые пережили бы сверку: `openspec-verify-change/templates/chat-summary.md` (три ответа на границе сдачи), `chat-output-budget-full.mdc` (форма из трёх пунктов у вопроса), `openspec-apply-change/SKILL.md` (pre-flight «после трёх ответов»), `openspec-status/SKILL.md` (второй список ответов).
- **G5** — `implementation_invariant`. Для снимка состояния при уже открытой приёмке задать третью форму фразы места: место словами и «ждёт приёмки», без «это финальный тест» (признак финала только на передаче, карточке проверки и конечной карточке пакета). Дописать в D1 и S1.11.
- **G6, G7** — закрыты текстом. Не эскалировать.
- Смешанный отчёт: decision первым. Repair G2–G5 и `scenario-orphan-design` после ответа, вместе с записью выбора. В этом проходе не применялись. `repair_attempt: 0`.

### Каскад дельты

- **verify_depth:** full. Первого `verification-*.md` не было.
- **recomputed:** все `check_id` первого прогона.
- **reused:** нет.
- **escalated:** quality-controller (один срез, без явной модели); design-challenge (Fable, риск прецедента). task-readiness не запускался.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

Единственная развилка чата — G1, секция «Решения до apply». Закрытых решений нет, опровержений предпосылок нет. `open_decision_id` остаётся null: это не запись внешнего контракта.

### Контроль простоты

`reports/architecture-new-2026-10-27.md`, `mode: plan-review`: секции `## Simplicity Check` нет. Строка «к сведению», в постановку не писалась.

## Источники

- `openspec/changes/slice-handoff-final-tests/reports/quality-control-2026-10-27.md`
- `openspec/changes/slice-handoff-final-tests/reports/design-challenge-2026-10-27.md`
- Алерты: `scenario-orphan-design`, `scenario-orphan-slice`, `precedent-documented`
