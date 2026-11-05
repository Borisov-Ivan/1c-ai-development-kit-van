---
verify_mode: pre-apply
change: fix-route-from-analysis
date: 2026-11-05
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: FAIL
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: WARNING
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks:
    - S1.1
    - S1.2
    - S1.3
    - S1.4
    - S1.5
  closed_decisions:
    - id: card_rule_binding
      summary: "Правило карточки обязательно. Починка с прежней суммой и справкой остаётся в открытой приёмке, без вопроса о срезе и без отдельного шага проведения. Вариант, который проведение не выполняет, в карточку не ставится. Убрать это правило из текста можно только новым ответом."
      closed_at: "2026-11-05T14:12:00+09:00"
      source: verify-user-answer
      confirmed_by: user
      authority: customer-direct
      external_contract_id: EC-1
      premise:
        claim: "Правило уже стоит в тексте заявки; ответ делает его обязательным, чтобы снять его можно было только новым ответом."
        anchor: "openspec/changes/fix-route-from-analysis/debug.md#Extend — 2026-11-05"
  refuted_premises:
    - decision_id: card_rule_binding
      refuting_anchor: "openspec/changes/fix-route-from-analysis/debug.md:27"
      report: "openspec/changes/fix-route-from-analysis/reports/design-challenge-2026-11-05.md"
      detected_at: "2026-11-05T15:45:04+09:00"
      fingerprint: "f4628a6134ec0a040c684c985e197a09c6b5a0a0ff727e92cc0455c67d0be39a"
  open_decision_id: EC-1
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "подтвердить обязательность правила карточки: дополнение от 2026-11-05 не содержит фразы, что убрать правило можно только новым ответом"
  artifacts_mtime:
    proposal.md: "2026-11-05T13:34:57+09:00"
    design.md: "2026-11-05T14:14:55+09:00"
    tasks.md: "2026-11-05T13:35:40+09:00"
    debug.md: "2026-11-05T15:45:09+09:00"
    specs/pipeline-light-route/spec.md: "2026-11-05T13:35:31+09:00"
  last_challenge_at: "2026-11-05T15:45:04+09:00"
  artifact_hashes:
    proposal.md: "f052024f6d8a92238a499a5d1e98edc86a593658233a4666bdb4645e36bf02a8"
    design.md: "302a88e07c7097a1dd0bf82b51419a45fa8f77bbd711ead9939b31159f00fbdb"
    design.md#axis: "1ca6adf3b16f9de01afa10259d36b6a95f91ab4fe79405343ea01734efef071b"
    tasks.md: "9b904c68400811ca085f661378cad333ce16d9b92b595c4d29ffffdd3abfe9a1"
    tasks.md#normalized: "075a5a76a8c330da055e44bca0ee1fc9f4a0fcd6693e7122148979bb3390e903"
    specs/pipeline-light-route/spec.md: "d25af7fc7eaa2f9dcf1bc8ff96a365ff665bb5dec76ea9e2dd8bbdd06ae15463"
    debug.md#without-slice-gate: "880c58b73b2996167237bedb647c7715bb1766ff0950263bdb1be425f984b830"
  external_contract_digest: "fdc276f648e214129addf87a7cbfbe53736c3a958de6e29bace0da18ab677c4f"
  decision_fingerprints:
    card_rule_binding: "a75ac88cc6891d4196c37dda5c0ed971555d7c83ae5ec786dc8fbe119a1efedf"
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
    user-task-contract@S1: PASS
    scenario-coverage@S1: PASS
    code-truth@change: PASS
    precedent-regression@change: PASS
    loop-detection@S1: PASS
    problem-solution-trace@change: PASS
    design-challenge@axis: CHALLENGE
    task-readiness@S1: WARNING
    premise-reconciliation@card_rule_binding: REFUTED
  invalidation_map:
    external-validity: "EC-1 подтверждён, но closed_at раньше detected_at опровержения предпосылки; тема снова открыта"
    design-challenge: "ось 1ca6adf3 отличается от последнего успешного разбора e30e3a09; разбор выполнен"
    scenario-coverage: "набор сценариев вырос после quality-control-2026-10-16-2; контроль выполнен"
    task-readiness: "отчёта готовности на этот текст задач не было; оценка выполнена"
    premise-reconciliation: "design-challenge-2026-11-05 содержит Premise conflicts по card_rule_binding"
    problem-solution-trace: "пересчитан: дешёвый блокер прошлого прогона снят"
    code-truth: "пересчитан"
    precedent-regression: "пересчитан"
    user-task-contract: "пересчитан"
    loop-detection: "пересчитан по тем же двум дополнениям"
scope_gate_decision: silent
classifier:
  blocker: premise-refuted
  decision_id: card_rule_binding
  external_contract_id: EC-1
  gaps_deferred:
    - id: G9
      class: implementation_invariant
      reason: "вход не называет оставшийся шаг"
    - id: G10
      class: implementation_invariant
      reason: "образец пакета по-прежнему зовёт первую проверку"
    - id: G11
      class: implementation_invariant
      reason: "фраза про мёртвую ветвь в общем шаблоне не ограничена карточкой проверки"
    - id: G12
      class: implementation_invariant
      reason: "подтверждение без номера не стыкуется с запретом голого да"
  repair_next: "не в этом проходе: сначала ответ пользователя; затем user-extend --from-verify"
---

## Резюме для разработчика

fix-route-from-analysis — до старта нужен ваш выбор по логике обязательности правила карточки.

Уже зафиксировано: починка с прежней суммой и справкой остаётся в открытой приёмке, без вопроса, куда её положить, и без отдельного шага «проводится». Вариант, который проведение не выполняет, в карточку не ставится. Снять это правило из текста можно только новым ответом.

Новый вопрос: запись, на которую опирается этот ответ, самой фразы об обязательности не содержит. Текст правила в заявке остаётся как есть.

**Что решить: остаётся ли правило карточки обязательным**

Запись ответа говорит, что правило карточки обязательно, и указывает опору на дополнение от 5 ноября. В этом дополнении написано, что границу живой ветви дописали в заявку и что дальше нужна полная проверка. Фразы «убрать можно только новым ответом» там нет: она стоит в зеркале решений и в журнале, который ссылается на это дополнение (`openspec/changes/fix-route-from-analysis/debug.md:27`). Пока нет нового ответа, эта опора правило не закрепляет.

- **A. Правило остаётся обязательным** — починка с прежней суммой по-прежнему не спрашивает, куда её положить, и вариант без проведения в карточку не попадает. Убрать правило из текста позже без нового ответа будет нельзя.
- **B. Обязательность снимается** — текст правил пока не трогаем. Если правило потом выпадет из заявки, остановка с вопросом может не сработать.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify fix-route-from-analysis`.

Полный отчёт: openspec/changes/fix-route-from-analysis/reports/verification-2026-11-05-2.md

Модулей конфигурации эта заявка не касается. Меняются тексты правил набора: куда класть починку, какие варианты карточки спрашивать и откуда брать следующий шаг после ответа.

## Решения до apply

### 1. Опора обязательности правила карточки

**В чём проблема.** Ответ уже записан: правило карточки обязательно. Опора этого ответа — дополнение от 5 ноября. В самом дополнении нет фразы, что убрать правило можно только новым ответом.

**На что влияет.** Пока опора не подтверждена заново, правило не держит запрет вернуть в карточку вариант без проведения. Текст заявки от этого вопроса не переписывается.

**Если выбрать A / B.** A — правило остаётся обязательным, и убрать его из текста позже без нового ответа будет нельзя. B — обязательность снимается; если правило потом выпадет из заявки, остановка с вопросом может не сработать.

**Что в тексте сейчас.** `debug.md:27` — дополнение: границу живой ветви дописали, следующий шаг — полная проверка. `design.md`, раздел «Решения verify (зафиксировано)» — фраза об обязательности. Журнал решений ссылается на то же дополнение.

**Что предлагает план.** Правило уже вписано в контракт поведения: в пару попадают только варианты, которые выполняют уже сказанное. Отдельная фраза об обязательности в дополнении не стоит.

**Почему это развилка.** Ссылка опоры не доходит до места, где возникает обязательность. Закрыть это правкой проверки нельзя: нужен новый ответ.

**Варианты решения.**

- **A. Правило остаётся обязательным** — починка с прежней суммой не спрашивает, куда её положить; вариант без проведения в карточку не попадает. Компромисс: убрать правило из текста позже без нового ответа будет нельзя.
- **B. Обязательность снимается** — текст правил не трогаем. Компромисс: выпадение правила из текста может не остановить следующую проверку.

**Влияет на:** останется ли сегодняшний ответ обязательным, когда текст правил снова поменяют.

**Что изменится после выбора.** Новый ответ записывается поверх этой опоры. Тексты правил этим выбором не переписываются. Затем проверка запускается снова.

**Источники** *(техническое):* `premise-refuted`; `card_rule_binding`; `EC-1`; `reports/design-challenge-2026-11-05.md` § Premise conflicts. Поля ответа человека этим прогоном не менялись. `confirmed_by: user` заново не ставился.

## Что меняется в постановке

Починка с прежним проведением, суммой и справкой не становится отдельным шагом. Спрашивают, только когда оба варианта выполняют уже сказанное и расходятся в результате или в моменте, когда результат уже можно принять. Один живой вариант продолжается в том же запуске. После настоящего ответа следующий шаг берётся из таблицы глубины.

Точки правки, которые план ещё не закрыл задачами:

- `.cursor/skills/openspec-verify-change/SKILL.md` — состав карточки и вход проверки.
- `.cursor/docs/templates/decision-block.md` — та же граница пары и фраза следующего шага в образце пакета.
- `.cursor/skills/openspec-verify-change/templates/chat-summary.md` и `card-decision.md` — следующий шаг из таблицы глубины.
- `.cursor/skills/openspec-extend-change/SKILL.md` — подтверждение без номера, когда заявка и правило уже названы.

Уже записано и этим вопросом не переписывается: размещение починки в `.cursor/rules/vertical-slices.mdc`, строка таблицы глубины, исход дополнения «проверка не требуется».

Не меняется: уже подписанная приёмка, полная проверка при смене формулы, момента правила, порядка шагов или сценария, вопрос на втором возврате одной и той же темы. Разбор, создание, пошаговый разбор, реализация и архив в это правило не входят. Опора — ADR-0014, ADR-0013, ADR-0012.

## К сведению

Четыре стыка текста уже названы независимой проверкой плана и отдельным вопросом не стоят: вход должен назвать оставшийся шаг, образец пакета не должен звать первую проверку единственным шагом, фраза про мёртвую ветвь действует только в карточке проверки, подтверждение без номера не упирается в запрет голого «да». Их допишут после ответа. Приёмка среза «Маршрут починки с прежним результатом» открыта. Порог правок не сработал: два дополнения, порог три.

## Технический аудит (для движка OpenSpec)

- **verify_depth:** `full`. Ось `design.md#axis` `1ca6adf3…` совпала со снимком `verification-2026-11-05.md` и разошлась с последним успешным разбором `e30e3a09…` в `verification-2026-10-16-2.md`. Прошлый прогон остановился до разбора. Этот прогон разбор выполнил. Класс «замена значения» не присвоен. Первая строка таблицы глубины не применена: дельта этого прогона — запись ответа и зеркало, но отложенный разбор оси не был выполнен.
- **Layer 1 (Hygiene):** PASS. Автоправок нет. Чекбоксы у S1.1–S1.9 и S1.accept на месте. Один `<!-- slice-gate -->`. `form_mode: n/a`.
- **Layer 2 (Internal Coherence):** FAIL, класс decision. QC `reports/quality-control-2026-11-05.md`: OK, 13/13, 8b PASS, user-task-contract PASS, алертов нет. Code-truth: технических имён процедур нет, `openspec/project.md` нет. Precedent: в дельте только ADDED, пар `ADDED → MODIFIED/REMOVED` нет, Supersedes нет, `_index.yaml` нет. User Task Contract pre-check: none. Маркеров ручной конфигурации нет. Схема EC-1 валидна: `customer-direct`, `parity: matches`, `confirmation: confirmed`, `confirmed_by: user`, отпечаток сигнала совпал. Блокер: `premise-refuted` по `card_rule_binding`. `closed_at` 2026-11-05T14:12:00 раньше `detected_at` 2026-11-05T15:45:04, поэтому закрытие высокого авторитета недействительно, `open_decision_id: EC-1`. Поля `closed_decisions`, `confirmed_by`, `confirmation` не переписывались. Repair Loop не запускался: decision раньше repair.
- **Layer 2.5 (Loop Detection):** PASS. `AcceptLoop(S1)` = 1. `PatchRounds(S1)` = 2. `acceptance_loop_max` = 3. `TopicReopen` = 0. Возврат по опровергнутой предпосылке в `TopicReopen` не входит.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт двумя Requirement. У каждого Requirement есть Scenario. Все 13 Scenario названы в `## Slices`. У среза есть рабочие задачи и ровно одна приёмка. Маркеров implementation-leak в THEN нет. `comment_suffix` пуст.
- **Layer 4 (Independent Challenge):** CHALLENGE, `reports/design-challenge-2026-11-05.md`. Триггер: смена оси относительно последнего успешного разбора. G1–G8 закрыты текстом. Открыты G9–G12, все `implementation_invariant`. Classifier: repair, не развилка. В чат не выносились, потому что опровержение предпосылки имеет приоритет. `last_challenge_at` обновлён: разбор прошёл в чат через вопрос о подтверждении. Первый вызов на Opus оборвался лимитом; повтор на модели чата записал отчёт. `## Premise conflicts` сверен: якорь `debug.md:27` не содержит фразы обязательности.
- **Layer 5 (Implementation Readiness):** WARNING. `reports/architecture-task-readiness-2026-11-05.md`, вердикт «ГОТОВО С ЗАМЕЧАНИЯМИ». Критерий 4 GAP неблокирующий, якорь `отчёт#1` — тот же носитель, что G10. Критерий 7 OK, ремонта упрощения нет. Критерий 8 OK.
- **Сверка предпосылок:** в журнале есть `premise` у `card_rule_binding`. Новых отчётов после снимка `verification-2026-11-05.md`, кроме отчётов этого прогона, не было. Сверка отчётов этого прогона нашла опровержение. `refuted_premises[]` дописан. Тот же `fingerprint` после ответа не эскалировать.
- **recomputed:** hygiene, slice markers, external validity, user-task-contract, scenario-coverage, code-truth, precedent, loop, problem-solution-trace, design-challenge, task-readiness, premise-reconciliation.
- **reused:** нет. Прошлый QC и прошлый разбор покрывали прежний набор.
- **escalated:** quality-control, design-challenge, task-readiness.

## Источники

- `openspec/changes/fix-route-from-analysis/reports/verification-2026-11-05.md`
- `openspec/changes/fix-route-from-analysis/reports/quality-control-2026-11-05.md`
- `openspec/changes/fix-route-from-analysis/reports/design-challenge-2026-11-05.md`
- `openspec/changes/fix-route-from-analysis/reports/architecture-task-readiness-2026-11-05.md`
- Алерты: `premise-refuted`
