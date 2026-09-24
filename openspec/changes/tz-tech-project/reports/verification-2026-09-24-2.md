---
verify_mode: pre-apply
change: tz-tech-project
date: 2026-09-24
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: WARNING
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks:
    - S1.1
    - S1.3
    - S1.7
    - S1.9
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
    - id: slice-text-freeze
      summary: "Снято 2026-09-24: заказчик выбрал переписать срез. Прежняя заморозка «не трогать до прогона» не действует."
      closed_at: "2026-09-23"
      source: verify-user-answer
      confirmed_by: user
      superseded_by: slice-rewrite-for-explore
    - id: hours-multi-factor-sum
      summary: "Несколько названных факторов надбавки: складываются их нижние границы. Каждый фактор на коэффициент не умножается. Правило одного фактора (EC-2) не отменяется."
      closed_at: "2026-09-24"
      source: verify-user-answer
      confirmed_by: user
      authority: customer-direct
      external_contract_id: EC-4
    - id: explore-protocol-for-gaps
      summary: "Дыры и связь с прошлыми изменениями ищутся тем же протоколом исследования, что перед созданием задачи на разработку. Отдельный чеклист дыр и отдельная сверка имён вторым источником не являются. После подтверждения в листе пишется файл постановки; каталог задачи команда не создаёт."
      closed_at: "2026-09-24"
      source: verify-user-answer
      confirmed_by: user
      authority: customer-direct
      external_contract_id: EC-5
    - id: slice-rewrite-for-explore
      summary: "Текст среза переписан под протокол исследования и сумму надбавок. Заморозка до прогона снята этим выбором."
      closed_at: "2026-09-24"
      source: verify-user-answer
      confirmed_by: user
  open_decision_id: null
  decision_round: 3
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-09-24T09:23:57"
    design.md: "2026-09-24T09:25:02"
    tasks.md: "2026-09-24T09:24:18"
    specs/tz-tech-project/spec.md: "2026-09-24T09:24:18"
    debug.md: "2026-09-24T09:58:27"
  last_challenge_at: "2026-09-24T09:53:49+09:00"
  artifact_hashes:
    proposal.md: "a4f0c5dcdf786b3a9f06bc4c329248bbae7f661f2d234d1802c6bdd6fd453071"
    design.md: "0c1bae11b9653a15b917d67eddcf66bbcc5b7e22f669154089289adf05eec7a8"
    design-axis: "c4b66e1f40896098fe8912d46e48961018da5c753c5f960a2579f9defc38290d"
    tasks.md: "62078ca9c7c465de376ad84627b1c1885e8c9dca34bfbc2121de12b37eceb1b9"
    specs/tz-tech-project/spec.md: "b0815ff368748c8f0447cd6cdd275b5a3eddd8f3a15dd72ac8fc5c98c99ae035"
    debug.md: "38f56604bce6e01c5b62cfc5f28d7aaa655caa04cb7e934e0cbd73c56ea04952"
  external_contract_digest: "c79e6903eaab49972ebbe78c9dd06ddb68fff6145defd7881e8d742cb0183a44"
  decision_fingerprints:
    second-step-confirmation: "ff98d9a073b5afaf7e5d5f9b0c8210aecd226f31642e6e54fa09fca1fb6ae75e"
    hours-surcharge-after-coefficient: "3d54bd0872ac7b2799dcc3e54ecc9d79a55aca710c7dd53cd4eb5a7f2e041ca4"
    hours-round-up: "7b7a14b283243d83475efb57f594279ce62bed74ac6cf6d07fdf1f116ce84e71"
    slice-text-freeze: "fe6fbdc306a44169f5f8daa2c018fbf515df84f388d8fec4b8c4eaf9e0fa15fb"
    hours-multi-factor-sum: "2c1ff96993b12b3ae1733a5b0efd766c45ae2641795cb58626c69554a9cc78ec"
    explore-protocol-for-gaps: "5620ae553e3a48f96fc3e12192673cc482be21bbaef0551e17d28e80ff069f46"
    slice-rewrite-for-explore: "53d438ef9fe002ef79ecfecded188d69a3ca960e6ac832f0c0e87231b1080cc3"
  rules_versions:
    .cursor/skills/openspec-verify-change/SKILL.md: "adc530902b558da6b6780eac220078315b3ce7bc1ed2bd94e55c679cc0230632"
    .cursor/rules/vertical-slices.mdc: "17615576ce482f01b9a286bb0206f22baddccd8f1f6045f14c35bfbbdab19e63"
    .cursor/rules/code-truth-gate.mdc: "20f25dae70359466cfeec4ac8ec1210867919c3b775f2cd8b597cd7ba7bd85f0"
    .cursor/rules/precedent-regression-gate.mdc: "3921384b52ed58bc1ffa0167b3c5d5ef6f1ca8e73976de9d7d8af06c35b7b148"
    .cursor/rules/architect-gate.mdc: "7927fe8d7d4c2ed61321dadf6cce0174fd1fa70fbf0ad717940f1ffeb7bb3813"
    .cursor/rules/openspec-specs-gate.mdc: "e97cf9ad3a76132a05c88bf183b44410320547c9b84cf07e6f73fcea7aced6d4"
  check_cache:
    scenario-coverage: "quality-control-2026-09-24 OK; 10 сценариев, Primary достижим задачами первого вывода"
    user-task-contract: "none"
    external-validity: "EC-1 EC-2 EC-3 EC-4 EC-5 confirmed"
    loop-detection: "resolved earlier; TopicReopen новых тем 0; запасной порог не для тем с номером"
    design-challenge: "design-challenge-2026-09-24 CHALLENGE"
    task-readiness: "architecture-task-readiness-2026-09-24 warning-level-gaps"
  invalidation_map:
    design-challenge: "хэш оси сменился; новые сценарии и новый файл постановки; полный разбор"
    scenario-coverage: "изменился текст Primary и набор названий сценариев"
    task-readiness: "изменился текст S1.2 S1.4 S1.5 S1.6 S1.8, добавлена S1.10"
    external-validity: "новые EC-4 и EC-5"
classifier:
  implementation_invariant:
    - postanovka-consumer-block
  decision:
    - zero-catalog-rows
  dropped: []
  supersedes: none
  repair_next: "сначала ответ, если строка справочника не нашлась; фраза, что файл постановки содержит блок для команды создания задачи, дописывается вместе с этим ответом, не отдельным вопросом"
---

## Резюме для разработчика

tz-tech-project — до старта нужен ваш выбор по логике часов, если работе не подходит ни одна строка справочника.

Уже зафиксировано: техпроект и текст для задачи на разработку пишутся после подтверждения в листе, согласование часов выходит сразу. Часы из прозы — нижняя граница работы на коэффициент плюс сумма надбавок, дробь поднимается до целого. Несколько названных надбавок складываются. Пробелы ищутся разбором кода и прошлых изменений.
Новый вопрос: что писать, если описанной работе не нашлась ни одна строка справочника часов. Прежние решения не пересматриваются.

**Что решить: часы, когда строка справочника не нашлась**

Для одной подходящей строки и для двух строк правило уже есть. Если не подходит ни одна, число часов взять не из чего, а выдумывать его нельзя. От этого зависит, уйдёт ли согласование сразу или останется ждать ответ в листе.

- **A. Спросить в листе** — по этой работе появляется пункт, часы не ставятся, пока нет ответа. Зато согласование само не закроется.
- **B. Отметить пробел без часов** — в листе фиксируется пробел, строки часов по этой работе нет, остальное согласование пишется сразу. Зато числа по этой работе не будет, пока пробел не закроют отдельно.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify tz-tech-project`.

Полный отчёт: openspec/changes/tz-tech-project/reports/verification-2026-09-24-2.md

Команда `/opsx:techproject` и навык уже частично собраны: обёртка, каркас согласования, карта разделов задания и описание техпроекта отмечены сделанными. В работу возвращены правила листа, часов, поиска пробелов и новый файл постановки. Конфигурация не меняется.

## Решения до apply

### Часы, когда строка справочника не нашлась

**Цель ЗНИ:** по файлу задания сначала согласовать часы, затем подготовить техпроект и текст для задачи на разработку.

**Что в постановке сейчас.** Если описанию подходят две строки справочника часов, в листе вопрос, более тяжёлая строка молча не выбирается. Если строка одна, часы считаются по формуле. Ветки «не подошла ни одна строка» нет.

**Что предлагает план.** Формулу для одной строки и вопрос для двух строк оставить. Для нуля строк правило не выбрано. Выдумывать часы общий запрет не позволяет.

**Почему это выбор.** В файле согласования либо появится пункт и число по этой работе подождёт, либо будет пробел без строки часов и остальной текст уйдёт сразу.

**Варианты.**

- **A. Спросить в листе** — пункт по этой работе, часы не ставятся до ответа; **компромисс:** согласование ждёт.
- **B. Отметить пробел без часов** — пробел в листе, строки часов по этой работе нет, остальное пишется сразу; **компромисс:** числа по этой работе нет, пока пробел не закроют отдельно.

**Влияет на:** строку часов в `<имя>-согласование.md` и состав `<имя>-вопросы.md`.

**Что изменится после выбора.** Правило для нуля строк будет теми же словами в описании поведения, в требованиях и в задаче про справочник часов.

## Что меняется в постановке

Команда по файлу задания пишет лист вопросов и согласование часов. После подтверждения в листе — техпроект таблицами и файл постановки для задачи на разработку. Каталог этой задачи команда не создаёт. Несколько факторов надбавки складываются. Пробелы ищутся разбором кода и прошлых изменений, не отдельным списком и не отдельной сверкой имён. Модули конфигурации не меняются. Файлы обзора задачи не правятся.

### К сведению

Срез покрывает десять сценариев. Обязательный пункт приёмки читает лист и согласование; техпроект и постановка на первом запуске не требуются. Задачи, возвращённые в работу, исполнимы по тексту. Точный путь к разбору задания и список полей файла постановки на запуск не влияют. Фраза, что этот файл содержит блок, который читает команда создания задачи, дописывается вместе с ответом по часам и отдельным вопросом не ставится.

## Технический аудит (для движка OpenSpec)

- Layer 1 Hygiene: PASS. Автоправок нет. Чекбоксы и `<!-- slice-gate -->` на месте. `form_mode: n/a`. Маркеров ручной конфигурации нет.
- External validity: PASS. `EC-1`…`EC-5` confirmed, `confirmed_by: user`, парные `closed_decisions`, отпечатки сигналов совпали, второго `source_fingerprint` нет. `open_decision_id: null`. Extend 2026-09-24 зарегистрирован темами EC-4 и EC-5.
- Layer 2 Internal Coherence: PASS. `reports/quality-control-2026-09-24.md`, verdict OK. Критерии 1–6, 8, 8b, 9–11 PASS. Прошлый контроль не переиспользован: сменились текст Primary и набор сценариев. User Task Contract: none. Code-Truth pre-apply: якорей процедур нет. Precedent: в spec только ADDED, MODIFIED/REMOVED нет; `invariant: true` в индексе знаний нет; Supersedes Load-Bearing нет.
- Layer 2.5: PASS. Прежняя остановка разобрана (`reports/architecture-loop-redesign-2026-09-23.md` и ответ переписать срез в Extend 2026-09-24). AcceptLoop(S1)=0. Новые темы EC-4 и EC-5: TopicReopen 0. Запасной счёт правок к темам с номером не применяется. Повторный вопрос «оставить текст или переписать срез» не задавался.
- Layer 3 Problem-Solution Trace: PASS. Why покрыт двумя Requirement. У каждого Requirement есть Scenario. Все 10 Scenario есть в `## Slices` и в чеклисте `S1.accept`. У среза есть рабочие задачи и одна `S1.accept`. THEN без маркеров implementation-leak. `comment_suffix` пустой при `marker_style: minimal`.
- Layer 4 Independent Challenge: CHALLENGE. `reports/design-challenge-2026-09-24.md`. Post-challenge classifier: G1–G7 повтор, закрыты текстом. G8 `implementation_invariant` (файл постановки должен содержать блок, который читает команда создания задачи) — repair, не развилка, ось EC-5 не отменяется. G9 — продуктовый выбор по видимым часам, когда не подошла ни одна строка справочника. Альтернативы с `reopen-blocked` без нового факта в чат не выносились. `last_challenge_at` обновлён. Насыщение развилок не применено: остаток — новый видимый исход часов, не отложенное допущение. Repair Loop не запускался: decision имеет приоритет, `repair_attempt` остаётся 0.
- Layer 5 Implementation Readiness: WARNING. `reports/architecture-task-readiness-2026-09-24.md`, overall `warning-level-gaps`, blocking gap нет. Manual-config: маркеров нет.
- verify_depth: full. Причина: хэш оси `c4b66e1f…` отличается от `282fa648…` последнего разбора; новые сценарии и новый файл постановки; ответы EC-4 и EC-5 меняют наблюдаемое правило. decision_round: 3.

## Источники

- `reports/quality-control-2026-09-24.md`
- `reports/design-challenge-2026-09-24.md`
- `reports/architecture-task-readiness-2026-09-24.md`
- `reports/architecture-loop-redesign-2026-09-23.md`
- Алерты: продуктовая развилка нуля строк справочника; repair отложен: блок постановки для команды создания задачи
