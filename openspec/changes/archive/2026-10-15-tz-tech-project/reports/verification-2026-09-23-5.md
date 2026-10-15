---
verify_mode: pre-apply
change: tz-tech-project
date: 2026-09-23
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: acceptance-loop-detected
  layer_3_problem_solution: not-started
  layer_4_independent_challenge: not-started
  layer_5_implementation_readiness: not-started
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions:
    - id: second-step-confirmation
      summary: "Техпроект пишется после подтверждения согласования часов в листе вопросов, не по отдельной просьбе его подготовить. Согласование на первом запуске выходит сразу."
      closed_at: "2026-09-23"
      source: verify-user-answer
      confirmed_by: user
      authority: customer-direct
      external_contract_id: EC-1
    - id: hours-surcharge-after-coefficient
      summary: "Часы из прозы: (нижняя граница × коэффициент) + надбавка. Надбавка на коэффициент не умножается."
      closed_at: "2026-09-23"
      source: verify-user-answer
      confirmed_by: user
      authority: customer-direct
      external_contract_id: EC-2
    - id: hours-round-up
      summary: "Дробный результат часов поднимается до следующего целого. Целое не меняется."
      closed_at: "2026-09-23"
      source: verify-user-answer
      confirmed_by: user
      authority: customer-direct
      external_contract_id: EC-3
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-09-23T13:36:28"
    design.md: "2026-09-23T13:36:26"
    tasks.md: "2026-09-23T13:36:40"
    specs/tz-tech-project/spec.md: "2026-09-23T13:35:56"
    debug.md: "2026-09-23T13:47:31"
  last_challenge_at: "2026-09-23T11:06:13"
  artifact_hashes:
    proposal.md: "b0c679dc172f1d0c4b7d1584a744c181a2476b7b9e9d17d3c900ee56eb24f7d2"
    design.md: "505d222e3437ab0edd777f984af5eb2c2678014db3c2faf402e150f3893dabda"
    design-axis: "282fa648cfec5e145af43fb510c16099c3590f3c76af715089d8a8555c5c2e2f"
    tasks.md: "be498cb996dd9159ae3d744ee7443335db4d041f513de19d6a9f893f4ff7ae54"
    specs/tz-tech-project/spec.md: "3787332ca1670ec53dc7dcab5763d788494b6d8a064e1a4612d2c339c5bc5e1d"
    debug.md: "2c3ad45513ddb4ba0948cbf5a614e61666e4554dc703ba3eb7996466b9e4fba0"
  external_contract_digest: "pending-ec-1-2-3-confirmed"
  decision_fingerprints: {}
  rules_versions: {}
  check_cache:
    scenario-coverage: "quality-control-2026-09-23-5 OK"
    user-task-contract: "none"
  invalidation_map:
    design-challenge: "ось design сменилась; вызов не запускался, петля приёмки остановила прогон"
    task-readiness: "текст задач изменился; вызов не запускался"
classifier:
  blocker: acceptance-loop-detected
  architect_recommendation: minimal
  repair_next: "не repair: выбор пользователя, затем extend по отчёту редизайна"
---

## Резюме для разработчика

tz-tech-project — до старта нужен ваш выбор: оставить текст среза или переписать его.

**Что решить: хватит ли уже записанных правил**

Срез «Техпроект по файлу задания» правили пять раз, команду ещё не запускали. Сейчас правила сходятся: сначала лист и согласование, техпроект после подтверждения в листе, часы — нижняя граница на коэффициент плюс надбавка, дробь вверх. Ещё одна переписка может снова сдвинуть эти правила.

- **A. Оставить текст** — дальше делать команду, не шестую правку постановки. В журнале прошлых правок останется старая фраза «по просьбе».
- **B. Переписать срез заново** — тот же смысл одним проходом. Легко снова разъехаться в часах и в моменте техпроекта.

**Следующий шаг:** `/opsx:extend tz-tech-project --from-architecture openspec/changes/tz-tech-project/reports/architecture-loop-redesign-2026-09-23.md`

Полный отчёт: openspec/changes/tz-tech-project/reports/verification-2026-09-23-5.md

Команды и навыка ещё нет. Конфигурация не меняется. Разбор предлагает вариант A: текст уже совпадает с выбранными правилами.

## Что доработать в постановке

### Развилки

#### 1. Пять правок одного среза до первого запуска

**Цель ЗНИ:** по файлу задания сначала согласовать часы, затем подготовить техпроект для технического задания.

**Что в коде сейчас.** Команды `/opsx:techproject` нет. В постановке пять последовательных правок одного среза: имена файлов, формула часов, два шага, округление, подтверждение в листе вместо просьбы. Приёмка среза не подписана, прогона на файле задания не было.

**Что предлагает план.** Оставить текущий текст: лист и согласование сразу, техпроект после подтверждения в листе, часы из нижней границы, коэффициента и надбавки с подъёмом дроби до целого часа.

**Почему это развилка.** Правила уже записаны одинаково в требованиях, описании и задачах. Переписывание среза заново не меняет смысл и может снова развести формулировки.

**Варианты решения.**

- **A. Оставить текст** — не править постановку до прогона команды на одном файле задания; **компромисс:** в журнале старых правок останется фраза «по просьбе».
- **B. Переписать срез заново** — собрать тот же смысл одним проходом; **компромисс:** легко снова сдвинуть часы или момент появления техпроекта.

**Влияет на:** начнётся ли реализация команды или постановку перепишут шестой раз.

**Что изменится после выбора.** При A текст не трогаем и идём к реализации. При B срез собирается заново с тем же смыслом.

**Источники** *(техническое):* `acceptance-loop-detected`; `reports/architecture-loop-redesign-2026-09-23.md` (рекомендация: оставить текст).

## Что меняется в постановке

Появляется обёртка команды и навык. Рядом с файлом задания — лист вопросов и согласование часов. Техпроект таблицами — после подтверждения согласования в листе. Модули конфигурации не меняются.

## К сведению

Связь среза с требованиями проверена: восемь сценариев покрыты, приёмка первого шага достижима без файла техпроекта. Независимый разбор плана и проверка исполнимости задач в этом прогоне не запускались: сначала нужно остановить круг правок.

## Технический аудит (для движка OpenSpec)

- Layer 1 Hygiene: PASS. Автоправок нет.
- External validity: PASS. `EC-1`, `EC-2`, `EC-3` confirmed, `confirmed_by: user`, парные `closed_decisions`, `open_decision_id: null`. Второго `source_fingerprint` нет. Extend (1)–(2) — repair, не события заказчика.
- Layer 2 Internal Coherence: PASS. `reports/quality-control-2026-09-23-5.md`, verdict OK. Критерии 1–6, 8, 8b, 9–11 PASS. User Task Contract: none. Code-Truth pre-apply: якорей процедур нет. Precedent: только ADDED, MODIFIED/REMOVED нет.
- Layer 2.5: FAIL `acceptance-loop-detected`. AcceptLoop(S1)=0, PatchRounds(S1)=5, порог 3. Отчёт `reports/architecture-loop-redesign-2026-09-23.md`: корень один, рекомендация minimal. Запись в `debug.md` § Loop Detection.
- Layer 3, Layer 4, Layer 5: not-started. Петля приёмки останавливает прогон до трассировки Why и профильной эскалации. `last_challenge_at` не обновлялся. Хэш оси отличается от снимка последнего challenge.
- verify_depth: full. repair_attempt: 0. decision_round: 1.

## Источники

- `reports/quality-control-2026-09-23-5.md`
- `reports/architecture-loop-redesign-2026-09-23.md`
- Алерты: `acceptance-loop-detected`
