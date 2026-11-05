---
verify_mode: pre-apply
change: fix-route-from-analysis
date: 2026-11-05
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: FAIL
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: SKIPPED-early-stop
  layer_4_independent_challenge: SKIPPED-early-stop
  layer_5_implementation_readiness: SKIPPED-early-stop
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks:
    - S1.1
    - S1.2
    - S1.3
    - S1.4
    - S1.5
  closed_decisions: []
  refuted_premises: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "дополнение 2026-11-05 с принятым брифом не записано как указание заказчика"
  artifacts_mtime:
    proposal.md: "2026-11-05T13:34:57+09:00"
    design.md: "2026-11-05T13:35:23+09:00"
    tasks.md: "2026-11-05T13:35:40+09:00"
    debug.md: "2026-11-05T13:35:42+09:00"
    specs/pipeline-light-route/spec.md: "2026-11-05T13:35:31+09:00"
  last_challenge_at: "2026-10-16T15:18:13+09:00"
  artifact_hashes:
    proposal.md: "f052024f6d8a92238a499a5d1e98edc86a593658233a4666bdb4645e36bf02a8"
    design.md: "171f40aa00b8204997e3210fee45b3467c9d63685166e12de7469f1a30a78321"
    design.md#axis: "1ca6adf3b16f9de01afa10259d36b6a95f91ab4fe79405343ea01734efef071b"
    tasks.md: "9b904c68400811ca085f661378cad333ce16d9b92b595c4d29ffffdd3abfe9a1"
    tasks.md#normalized: "075a5a76a8c330da055e44bca0ee1fc9f4a0fcd6693e7122148979bb3390e903"
    specs/pipeline-light-route/spec.md: "d25af7fc7eaa2f9dcf1bc8ff96a365ff665bb5dec76ea9e2dd8bbdd06ae15463"
    debug.md#without-slice-gate: "b998d43d08d8abc8755b3367c8e66ad3f59611c31fa00f478ba6f32ffcc6be9b"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints: {}
  rules_versions:
    .cursor/skills/openspec-verify-change/SKILL.md: "b650e6a2021b1d359c49b169a488cd7235d99ceb8f43eb62cae3e17a71d7e720"
    .cursor/skills/openspec-extend-change/SKILL.md: "a307c68b009b7857032d4aebb291db697dc3b4abddee5f6d9c3b82ce2cf3d1da"
    .cursor/rules/vertical-slices.mdc: "2c819ad1565f9a4817c1528c1340f99c33e2429a0d335415f564f21043446bd9"
    .cursor/rules/openspec-specs-gate.mdc: "14459abbd63cdd7140cd58b8ac7d0321a563c29999d1e026805e37ec37a76610"
    .cursor/rules/code-truth-gate.mdc: "bf8b7f6e9695a9f36b513faff3d9ba78499f283ebf2aa0ef86cacec957b9754f"
    .cursor/rules/precedent-regression-gate.mdc: "875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641"
    .cursor/rules/architect-gate.mdc: "733c4498f4bcded131a12f0a44818254b5da077af3438a51240a1e8ab5e9f000"
  check_cache:
    hygiene-checkboxes@tasks: PASS
    slice-gate-markers@S1: PASS
    external-validity@change: FAIL
    loop-detection@S1: PASS
  invalidation_map:
    external-validity: "debug.md § Extend — 2026-11-05: источник — подтверждённый бриф, записи EC нет"
    design-challenge: "design.md#axis сменился (e30e3a09 → 1ca6adf3); не запускался из-за дешёвого блокера"
    scenario-coverage: "spec и tasks получили новые сценарии; QC не запускался"
    task-readiness: "tasks.md изменился; вызов не запускался"
    precedent-regression: "не запускался: дешёвый блокер раньше"
    problem-solution-trace: "не запускался: дешёвый блокер раньше"
    code-truth: "не запускался: дешёвый блокер раньше"
    premise-reconciliation: "в журнале нет решений с полем premise; сверка не запускалась"
    user-task-contract: "не запускался: дешёвый блокер раньше"
scope_gate_decision: silent
early_stop: external-contract-unregistered
classifier:
  blocker: external-contract-unregistered
  events:
    - source: "debug.md#Extend — 2026-11-05"
      topic: "принятый бриф про живую ветвь записан в план, списка указаний заказчика нет"
      axis: visible-result
  proposed_on_A:
    authority: customer-direct
    parity: matches
    confirmation: confirmed
    note: "одна запись на бриф 2026-11-05; confirmed_by ставит только ответ пользователя"
  proposed_on_B:
    authority: internal
    parity: not-applicable
    confirmation: waived
  repair_next: "не repair: ответ пользователя, затем user-extend"
---

## Резюме для разработчика

fix-route-from-analysis — до старта нужен ваш выбор по логике записи правила карточки.

**Что решить: записать правило живой ветви как ваше указание**

Заметки заявки фиксируют принятый бриф: в пару попадают только варианты, которые выполняют уже записанный результат, и один такой вариант продолжается в том же запуске (`openspec/changes/fix-route-from-analysis/debug.md:29`). Списка указаний в этом файле нет, поэтому разбор задач не начинается. Текст правил в плане от выбора не меняется.

- **A. Записать как указание** — правило остаётся обязательным, следующая проверка разбирает задачи. Позже убрать его из текста без нового вопроса будет нельзя.
- **B. Оставить заметкой плана** — текст правил не трогаем, отдельную запись указания не создаём. Следующая проверка тоже разбирает задачи, но если правило потом выпадет из текста, остановка с вопросом может не сработать.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify fix-route-from-analysis`.

Полный отчёт: openspec/changes/fix-route-from-analysis/reports/verification-2026-11-05.md

Модулей конфигурации эта заявка не касается. Меняются тексты правил набора: куда класть починку, какие варианты карточки спрашивать и откуда брать следующий шаг после ответа.

## Решения до apply

### 1. Запись принятого брифа

**В чём проблема.** Принятый бриф уже лежит в заметках заявки, а списка указаний заказчика в том же файле нет. Проверка не ставит эту отметку сама.

**На что влияет.** Пока списка нет, разбор задач не начинается. Текст правила в плане от выбора не зависит: в пару попадают только варианты, которые выполняют уже записанный результат, один такой вариант продолжается сразу.

**Если выбрать A / B.** A — правило остаётся обязательным, и убрать его из текста позже без нового вопроса будет нельзя. B — текст правила остаётся заметкой плана; если правило потом выпадет из текста, остановка с вопросом может не сработать.

**Что в тексте сейчас.** `debug.md:25` — решение человека принять рекомендации аудита согласованности. `debug.md:29` — дополнение с источником «подтверждённый бриф». Секции списка указаний нет. Журнала ответов с пометкой человека нет.

**Что предлагает план.** Правило уже вписано в контракт поведения и в требования: карточка проверки, карточка дополнения и вход проверки оставляют только живую ветвь; следующий шаг после настоящего ответа берётся из таблицы глубины. Отдельной записи указания план не добавлял.

**Почему это развилка.** Дополнение передано человеком и новее прошлого прогона от 2026-10-16. Записи указания на него нет. Закрыть пробел отметкой проверки нельзя.

**Варианты решения.**

- **A. Записать как указание** — принятый бриф становится указанием; текст правил не переписывается. Компромисс: позже убрать правило из текста без нового вопроса будет нельзя.
- **B. Оставить заметкой плана** — список указаний не создаётся, дополнение помечается как внутренняя заметка. Компромисс: выпадение правила из текста может не остановить следующую проверку.

**Влияет на:** останется ли сегодняшний бриф обязательным, когда текст правил снова поменяют.

**Что изменится после выбора.** Ответ вписывается в список указаний. Тексты правил и задачи не переписываются этим выбором. Затем проверка запускается снова и доходит до разбора задач.

**Источники** *(техническое):* `external-contract-unregistered`; `debug.md` § Extend — 2026-11-05. Предложение при A: `authority: customer-direct`, `parity: matches`, одна запись на бриф. При B: `authority: internal`, `parity: not-applicable`, `confirmation: waived`. `confirmed_by: user` этот прогон не ставит.

## Что меняется в постановке

Починка с прежним проведением, суммой и справкой по-прежнему не становится отдельным шагом. К этому добавлено правило карточки: спрашивают, только когда оба варианта выполняют уже сказанное и расходятся в результате или в моменте, когда результат уже можно принять. Один живой вариант продолжается в том же запуске. После настоящего ответа следующий шаг берётся из таблицы глубины.

Точки правки, которые план ещё не закрыл задачами:

- `.cursor/skills/openspec-verify-change/SKILL.md` — состав карточки и вход проверки.
- `.cursor/docs/templates/decision-block.md` — та же граница пары.
- `.cursor/skills/openspec-verify-change/templates/chat-summary.md` и `card-decision.md` — следующий шаг из таблицы глубины.
- `.cursor/skills/openspec-extend-change/SKILL.md` — карточка дополнения без пары «не делать», когда заявка и правило уже названы.

Уже записано прошлым прогоном и этим выбором не переписывается: размещение починки в `.cursor/rules/vertical-slices.mdc`, строка таблицы глубины, исход дополнения «проверка не требуется».

Не меняется: уже подписанная приёмка, полная проверка при смене формулы, момента правила, порядка шагов или сценария, вопрос на втором возврате одной и той же темы. Разбор, создание, пошаговый разбор, реализация и архив в это правило не входят. Опора — ADR-0014, ADR-0013, ADR-0012.

## К сведению

Разбор задач и независимая проверка плана в этом прогоне не запускались: сначала нужна запись указания. Порог правок среза «Маршрут починки с прежним результатом» не сработал: два дополнения, порог три, темы с номерами не переоткрывались. Приёмка этого среза всё ещё открыта, рабочие задачи правила карточки ещё не отмечены. Предпосылки не сверялись: в журнале нет решений с полем предпосылки.

## Технический аудит (для движка OpenSpec)

- **verify_depth:** `full`. Новые сценарии и § Decisions / Behavior Contract (решение 6) меняют ось. Хэш `design.md#axis`: `e30e3a09…` в `reports/verification-2026-10-16-2.md` → `1ca6adf3…`. Первая строка таблицы глубины не применена: новый сценарий добавлен. Класс «замена значения» не присвоен. `last_challenge_at` не обновлялся.
- **Layer 1 (Hygiene):** PASS. Автоправок нет. Чекбоксы у S1.1–S1.9 и S1.accept на месте. Один `<!-- slice-gate -->`. Пустых буллетов, `<!-- phase-gate -->` и незакрытых fences нет. `form_mode: n/a`, задач на форму нет.
- **Layer 2 (Internal Coherence):** FAIL, класс decision, алерт `external-contract-unregistered`. Секции `## External Contract Ledger` нет. Событие закрытого перечня: `debug.md` § Extend — 2026-11-05, источник — подтверждённый бриф. Записи `EC-*` нет. § Extend — 2026-10-16 — `repair-from-verify`, не указание заказчика. § Slice Gate Decisions — `awaiting-acceptance`, не `не принят` / `inside-slice rework` / `стоп`. Журнала `verify-user-answer` нет, поэтому исключение «абзац только сохраняет уже данный ответ» не срабатывает. Repair Loop не запускался: агент не ставит `confirmed_by: user` и не меняет `closed_decisions` / `open_decision_id` / `decision_round`. Пустой журнал в `debug.md` не создавался: секции не было, снимок держит пустой ledger, запись секции сдвинула бы хэш входа до ответа.
- **Layer 2.5 (Loop Detection):** PASS. `AcceptLoop(S1)` = 1 (`awaiting-acceptance`, `S1.accept` = `[ ]`). `PatchRounds(S1)` = 2 (две секции `## Extend —`, обе меняли задачи S1). `acceptance_loop_max` = 3. `TopicReopen(G1…G8)` = 0, `TopicReopen(G9)` = 0. Запасной порог для тем без идентичности не применялся. `architecture-loop-redesign-*.md` не требуется.
- **Сверка предпосылок:** решений с полем `premise` нет. Новые `reports/` после `verification-2026-10-16-2.md` есть и в сверку не читались.
- QC, Code-Truth, precedent, User Task Contract, Layer 3, Layer 4, Layer 5: SKIPPED-early-stop. Дешёвый блокер внешней валидности завершает прогон до QC и профильной эскалации.
- **recomputed:** hygiene, slice markers, external validity, loop.
- **reused:** нет.
- **escalated:** нет.

## Источники

- `openspec/changes/fix-route-from-analysis/reports/verification-2026-10-16-2.md` (прошлый снимок)
- `openspec/changes/fix-route-from-analysis/debug.md` § Extend — 2026-11-05
- Алерты: `external-contract-unregistered`
