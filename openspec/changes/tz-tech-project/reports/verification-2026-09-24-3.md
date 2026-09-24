---
verify_mode: pre-apply
change: tz-tech-project
date: 2026-09-24
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
    - id: hours-zero-catalog-row-question
      summary: "Если описанной работе не подходит ни одна строка справочника, в листе вопрос. Часы по этой работе не выдумываются и не ставятся, пока нет ответа."
      closed_at: "2026-09-24"
      source: verify-user-answer
      confirmed_by: user
      authority: customer-direct
      external_contract_id: EC-6
  open_decision_id: null
  decision_round: 4
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-09-24T10:02:42"
    design.md: "2026-09-24T10:02:53"
    tasks.md: "2026-09-24T10:19:25"
    specs/tz-tech-project/spec.md: "2026-09-24T10:03:07"
    debug.md: "2026-09-24T10:23:11"
  last_challenge_at: "2026-09-24T10:22:44+09:00"
  artifact_hashes:
    proposal.md: "69aa7afa7ca53341b2d1395dec7fee3fcd12eaabcff613530fccd2fba3bbea58"
    design.md: "688987d939e547cffa9a7e50a28f694727af7de5899c9b340ae8e38bce38d5fa"
    design-axis: "71874693a0199ee64b2e08ea21161bd90a14c1c65f7307086aab7b01780fbdbe"
    tasks.md: "7c01c669114eaefa6ab48a81d10ab4c4cc7c4318e15114780a6194cbacce30b8"
    specs/tz-tech-project/spec.md: "c70c76dfb682bf5a3c951ed48dfbf74f0d0883ab2f4b766f9fb408897beb0039"
    debug.md: "53a5de8ca65746c2ef2c7b1b5fd998d37c3a44687c0308dd44590c932b5c95a2"
  external_contract_digest: "5ad96bea1533fd2f01e37d211ec2350a2cb11988c4576883beb79e5f902435b1"
  decision_fingerprints:
    second-step-confirmation: "ff98d9a073b5afaf7e5d5f9b0c8210aecd226f31642e6e54fa09fca1fb6ae75e"
    hours-surcharge-after-coefficient: "3d54bd0872ac7b2799dcc3e54ecc9d79a55aca710c7dd53cd4eb5a7f2e041ca4"
    hours-round-up: "7b7a14b283243d83475efb57f594279ce62bed74ac6cf6d07fdf1f116ce84e71"
    slice-text-freeze: "fe6fbdc306a44169f5f8daa2c018fbf515df84f388d8fec4b8c4eaf9e0fa15fb"
    hours-multi-factor-sum: "2c1ff96993b12b3ae1733a5b0efd766c45ae2641795cb58626c69554a9cc78ec"
    explore-protocol-for-gaps: "5620ae553e3a48f96fc3e12192673cc482be21bbaef0551e17d28e80ff069f46"
    slice-rewrite-for-explore: "53d438ef9fe002ef79ecfecded188d69a3ca960e6ac832f0c0e87231b1080cc3"
    hours-zero-catalog-row-question: "c3a73f267374c63efff6b9a559179dbaa8c40334ef0f04f436c45f636e14d943"
  rules_versions:
    .cursor/skills/openspec-verify-change/SKILL.md: "adc530902b558da6b6780eac220078315b3ce7bc1ed2bd94e55c679cc0230632"
    .cursor/rules/vertical-slices.mdc: "17615576ce482f01b9a286bb0206f22baddccd8f1f6045f14c35bfbbdab19e63"
    .cursor/rules/code-truth-gate.mdc: "20f25dae70359466cfeec4ac8ec1210867919c3b775f2cd8b597cd7ba7bd85f0"
    .cursor/rules/precedent-regression-gate.mdc: "3921384b52ed58bc1ffa0167b3c5d5ef6f1ca8e73976de9d7d8af06c35b7b148"
    .cursor/rules/architect-gate.mdc: "7927fe8d7d4c2ed61321dadf6cce0174fd1fa70fbf0ad717940f1ffeb7bb3813"
    .cursor/rules/openspec-specs-gate.mdc: "e97cf9ad3a76132a05c88bf183b44410320547c9b84cf07e6f73fcea7aced6d4"
  check_cache:
    scenario-coverage: "quality-control-2026-09-24-2 OK; 11 сценариев; после дописки задач набор названий и текст Primary не менялись, контроль не повторялся"
    user-task-contract: "none"
    external-validity: "EC-1 EC-2 EC-3 EC-4 EC-5 EC-6 confirmed"
    loop-detection: "прежняя остановка разобрана; TopicReopen G10 G11 = 0; запасной порог не для тем с номером"
    design-challenge: "design-challenge-2026-09-24-2 APPROVE; G10 G11 закрыты текстом задач"
    task-readiness: "architecture-task-readiness-2026-09-24-3 ready"
  invalidation_map:
    design-challenge: "хэш оси сменился относительно verification-2026-09-24-2; новый сценарий и EC-6; полный разбор"
    scenario-coverage: "добавился сценарий «Нет подходящей строки справочника»"
    task-readiness: "сначала S1.6 и S1.10, затем дописка S1.2 S1.4 S1.6 S1.10"
    external-validity: "новый EC-6"
classifier:
  implementation_invariant:
    - confirmation-nonempty
    - hours-question-open-still-writes-techproject
  decision: []
  dropped: []
  supersedes: none
  repair_next: null
---

## Резюме для разработчика

tz-tech-project — можно запускать apply.

По файлу задания команда пишет лист вопросов и согласование часов. После непустой пометки в строке подтверждения повторный запуск пишет техпроект и файл постановки. Если работе не нашлась строка справочника, в листе вопрос и часы не ставятся, пока нет ответа. Если подтверждение уже стоит, а вопрос ещё пустой, эта работа попадает в техпроект без часов. Конфигурация не меняется, каталог задачи на разработку команда не создаёт.

В задачах навыка записано, когда строка подтверждения считается заполненной и что пустой вопрос о часах оставляет работу в техпроекте без часов.

**Следующий шаг:** `/opsx:apply tz-tech-project`

Полный отчёт: openspec/changes/tz-tech-project/reports/verification-2026-09-24-3.md

## Что меняется в постановке

Команда по файлу задания пишет лист вопросов и согласование часов. После подтверждения в листе — техпроект таблицами и файл постановки для задачи на разработку. Если описанной работе не подходит ни одна строка справочника, в листе вопрос, часы не выдумываются. Несколько факторов надбавки складываются. Пробелы ищутся разбором кода и прошлых изменений. Модули конфигурации не меняются.

### Подправил в постановке

В задачах про протокол входа, лист вопросов, формулу часов и файл постановки записано: строка подтверждения заполнена, когда в ней есть непустая пометка; при уже заполненном подтверждении и ещё пустом вопросе о часах работа попадает в техпроект без часов, вопрос в листе остаётся.

### К сведению

Обязательный пункт приёмки читает лист и согласование. Техпроект и постановка на первом запуске не требуются. Маркеров ручной настройки в Конфигураторе нет.

## Технический аудит (для движка OpenSpec)

- Layer 1 Hygiene: PASS. Автоправок формы нет. Чекбоксы и `<!-- slice-gate -->` на месте. `form_mode: n/a`.
- External validity: PASS. `EC-1`…`EC-6` confirmed, `confirmed_by: user`, парные `closed_decisions`, отпечатки сигналов совпали, второго `source_fingerprint` нет. `open_decision_id: null`. Extend 2026-09-24 (2) зарегистрирован как EC-6. Дописка Extend 2026-09-24 (3) — внутреннее уточнение, нового контракта не создаёт.
- Layer 2 Internal Coherence: PASS. `reports/quality-control-2026-09-24-2.md`, verdict OK. Критерии 1–6, 8, 8b, 9–11 PASS. Набор сценариев сменился до контроля, прошлый контроль не переиспользован. После дописки задач названия сценариев и текст Primary не менялись, контроль повторно не запускался. User Task Contract: none. Code-Truth pre-apply: якорей процедур нет. Precedent: в spec только ADDED, MODIFIED/REMOVED нет; `invariant: true` в индексе знаний нет; Supersedes Load-Bearing нет.
- Layer 2.5: PASS. Прежняя остановка разобрана (`reports/architecture-loop-redesign-2026-09-23.md`). AcceptLoop(S1)=0. G10 и G11: первое упоминание, TopicReopen 0. Запасной счёт правок к темам с номером не применяется.
- Layer 3 Problem-Solution Trace: PASS. Why покрыт двумя Requirement. У каждого Requirement есть Scenario. Все 11 Scenario есть в `## Slices` и в чеклисте `S1.accept`. У среза есть рабочие задачи и одна `S1.accept`. THEN без маркеров implementation-leak. `comment_suffix` пустой при `marker_style: minimal`.
- Layer 4 Independent Challenge: APPROVE. `reports/design-challenge-2026-09-24-2.md`. G1–G9 закрыты текстом. G10 и G11 — implementation_invariant, Repair Loop attempt 1, закрыты текстом задач, ось не менялась, повторный разбор не запускался. `last_challenge_at` обновлён.
- Layer 5 Implementation Readiness: PASS. Сначала `reports/architecture-task-readiness-2026-09-24-2.md` (S1.6, S1.10, ready). После дописки — `reports/architecture-task-readiness-2026-09-24-3.md`, overall ready, blocking gap нет. Manual-config: маркеров нет.
- verify_depth: full. Причина первого прохода: хэш оси `71874693…` отличается от `c4b66e1f…`; новый сценарий; EC-6 меняет наблюдаемое правило. decision_round: 4. repair_attempt в снимке сброшен в 0 после GO.

## Источники

- `reports/quality-control-2026-09-24-2.md`
- `reports/design-challenge-2026-09-24-2.md`
- `reports/architecture-task-readiness-2026-09-24-2.md`
- `reports/architecture-task-readiness-2026-09-24-3.md`
- `reports/architecture-loop-redesign-2026-09-23.md`
- Алерты: нет блокирующих; G10 и G11 закрыты допиской задач
