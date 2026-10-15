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
    - S1.2
    - S1.3
    - S1.4
    - S1.5
    - S1.6
    - S1.7
    - S1.8
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
      summary: "Текст среза не переписывать. Дальше реализация команды, не новая правка постановки, пока её не прогонят на файле задания."
      closed_at: "2026-09-23"
      source: verify-user-answer
      confirmed_by: user
  open_decision_id: null
  decision_round: 2
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "несколько названных факторов надбавки: вопрос в листе или сумма нижних границ"
  artifacts_mtime:
    proposal.md: "2026-09-23T13:36:28"
    design.md: "2026-09-23T13:53:11"
    tasks.md: "2026-09-23T14:48:05"
    specs/tz-tech-project/spec.md: "2026-09-23T13:35:56"
    debug.md: "2026-09-24T08:49:52"
  last_challenge_at: "2026-09-24T08:48:00+09:00"
  artifact_hashes:
    proposal.md: "b0c679dc172f1d0c4b7d1584a744c181a2476b7b9e9d17d3c900ee56eb24f7d2"
    design.md: "cacf715926abb386fa26d146a6df1a6b507b14d105f515ce0127220ce0bb1b4e"
    design-axis: "282fa648cfec5e145af43fb510c16099c3590f3c76af715089d8a8555c5c2e2f"
    tasks.md: "4ef0df6d8446e15f803a6ba88d595ca0021f777ff05b68d57b45c9a2fe9becbf"
    specs/tz-tech-project/spec.md: "3787332ca1670ec53dc7dcab5763d788494b6d8a064e1a4612d2c339c5bc5e1d"
    debug.md: "35e73ea5bde5c76db791efe03db381886fb06601134f11cb8637260be3093b4b"
  external_contract_digest: "b35b11f5dfebc06f8c9e82fd8bea2e5bb4998d0d12301b8f7f682df448cb776b"
  decision_fingerprints:
    second-step-confirmation: "ff98d9a073b5afaf7e5d5f9b0c8210aecd226f31642e6e54fa09fca1fb6ae75e"
    hours-surcharge-after-coefficient: "3d54bd0872ac7b2799dcc3e54ecc9d79a55aca710c7dd53cd4eb5a7f2e041ca4"
    hours-round-up: "7b7a14b283243d83475efb57f594279ce62bed74ac6cf6d07fdf1f116ce84e71"
    slice-text-freeze: "fe6fbdc306a44169f5f8daa2c018fbf515df84f388d8fec4b8c4eaf9e0fa15fb"
  rules_versions:
    .cursor/skills/openspec-verify-change/SKILL.md: "adc530902b558da6b6780eac220078315b3ce7bc1ed2bd94e55c679cc0230632"
    .cursor/rules/vertical-slices.mdc: "17615576ce482f01b9a286bb0206f22baddccd8f1f6045f14c35bfbbdab19e63"
    .cursor/rules/code-truth-gate.mdc: "20f25dae70359466cfeec4ac8ec1210867919c3b775f2cd8b597cd7ba7bd85f0"
    .cursor/rules/precedent-regression-gate.mdc: "3921384b52ed58bc1ffa0167b3c5d5ef6f1ca8e73976de9d7d8af06c35b7b148"
    .cursor/rules/architect-gate.mdc: "7927fe8d7d4c2ed61321dadf6cce0174fd1fa70fbf0ad717940f1ffeb7bb3813"
    .cursor/rules/openspec-specs-gate.mdc: "e97cf9ad3a76132a05c88bf183b44410320547c9b84cf07e6f73fcea7aced6d4"
  check_cache:
    scenario-coverage: "опора на quality-control-2026-09-23-5 OK; набор сценариев и текст Primary не менялись"
    user-task-contract: "none"
    external-validity: "EC-1 EC-2 EC-3 confirmed"
    loop-detection: "resolved by user leave-text plus architecture-loop-redesign-2026-09-23"
    design-challenge: "design-challenge-2026-09-23-4 CHALLENGE"
    task-readiness: "architecture-task-readiness-2026-09-23 warning-level-gaps"
  invalidation_map:
    design-challenge: "хэш оси отличается от последнего успешного разбора; полный разбор выполнен"
    task-readiness: "отложенный вызов после петли правок выполнен; отметки задач текст не меняли"
classifier:
  implementation_invariant:
    - confirmation-line-on-empty-sheet
  decision:
    - multiple-surcharge-factors
  dropped: []
  supersedes: none
  repair_next: "сначала ответ по нескольким факторам надбавки; место подтверждения в пустом листе дописывается вместе с этим ответом, не отдельным вопросом"
---

## Резюме для разработчика

tz-tech-project — до старта нужен ваш выбор по логике надбавки, если в задании названо несколько факторов.

Уже зафиксировано: техпроект появляется после подтверждения согласования в листе вопросов, а согласование часов пишется сразу. Часы из прозы считаются как нижняя граница строки, умноженная на коэффициент, плюс надбавка, и дробь поднимается до целого часа. Надбавка на коэффициент не умножается. Текст среза до прогона команды не переписываем.
Новый вопрос: что делать, если в задании названо сразу несколько факторов надбавки. Прежние решения не пересматриваются.

**Что решить: часы, когда факторов надбавки больше одного**

Справочник часов может дать несколько надбавок, если в задании названо несколько факторов. Сейчас формула говорит про один фактор: если он назван, к часам прибавляется его нижняя граница. При двух факторах исполнитель не знает, складывать ли надбавки или спросить. От этого зависит число часов в согласовании.

- **A. Спросить в листе** — в листе вопросов появляется пункт с вариантами, часы не выбираются молча. Зато согласование не уйдёт, пока нет ответа.
- **B. Сложить нижние границы** — часы считаются сразу, каждая названная надбавка прибавляется один раз. Зато сумма может выйти тяжелее, чем если бы выбрали один фактор.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify tz-tech-project`.

Полный отчёт: openspec/changes/tz-tech-project/reports/verification-2026-09-24.md

Команда `/opsx:techproject` и навык `openspec-techproject` по тексту задач уже отмечены сделанными. Приёмка среза на одном файле задания ещё открыта. Конфигурация не меняется. Выгрузка `src/КАСК/cf/` нужна только чтобы сверить имена, а не чтобы писать модули.

## Что доработать в постановке

### Развилки

#### 1. Несколько факторов надбавки

**Цель ЗНИ:** по файлу задания сначала согласовать часы, затем подготовить техпроект для технического задания.

**Что в коде сейчас.** Команда ещё не прогонялась на файле задания. В `design.md` и в требованиях часы из прозы заданы для одного фактора: нижняя граница строки умножается на коэффициент, затем прибавляется нижняя граница надбавки. Если фактор не назван, надбавка нулевая.

**Что предлагает план.** Ту же формулу оставить для одного фактора. Для двух и более названных факторов правило в тексте не выбрано.

**Почему это развилка.** От выбора зависит число часов в `<имя>-согласование.md`. Молча сложить или молча взять один фактор постановка не разрешает.

**Варианты решения.**

- **A. Спросить в листе** — пункт в `<имя>-вопросы.md` с не меньше чем двумя вариантами; **компромисс:** согласование ждёт ответа.
- **B. Сложить нижние границы** — каждая названная надбавка прибавляется один раз после умножения нижней границы строки на коэффициент; **компромисс:** сумма может быть тяжелее одного фактора.

**Влияет на:** строку часов, которую отдают на согласование.

**Что изменится после выбора.** Формула для нескольких факторов будет записана теми же словами в описании поведения, в требованиях и в задаче про справочник часов.

**Источники** *(техническое):* `reports/design-challenge-2026-09-23-4.md` (G7).

## Что меняется в постановке

Появляется команда `/opsx:techproject` и навык рядом с обзором задачи. Рядом с файлом задания пишутся лист вопросов и согласование часов. Техпроект таблицами — после подтверждения согласования в листе. Модули конфигурации не меняются. Файлы `.cursor/skills/openspec-overview/**` не правятся.

## К сведению

Связь среза с требованиями взята из прошлого контроля: восемь сценариев покрыты, обязательный пункт приёмки читает лист и согласование, файл техпроекта на первом запуске не требуется. Задачи S1.1–S1.9 исполнимы по тексту; точная фраза маркера подтверждения и имена файлов внутри навыка на запуск не влияют. Место, куда вписать подтверждение, когда лист сведён к фразе «вопросов нет», дописывается вместе с ответом по надбавке, отдельным вопросом не ставится.

## Технический аудит (для движка OpenSpec)

- Layer 1 Hygiene: PASS. Автоправок нет. Чекбоксы и `<!-- slice-gate -->` на месте. `form_mode: n/a`. Маркеров ручной конфигурации нет.
- External validity: PASS. `EC-1`, `EC-2`, `EC-3` confirmed, `confirmed_by: user`, парные `closed_decisions`, `open_decision_id: null`. Второго `source_fingerprint` нет. Extend (6) фиксирует ответ «оставить текст» внутри уже выбранного подхода; наблюдаемое правило D1–D5 / Behavior Contract не менялось, новая ось не заводилась.
- Layer 2 Internal Coherence: PASS. Опора на прошлый контроль среза S1: взят `reports/quality-control-2026-09-23-5.md`, verdict OK. Упорядоченный набор названий сценариев и нормализованный текст Primary не изменились (у задач S1.1–S1.9 сменилась только отметка `[x]`). Новый полный контроль с нуля не создавался. User Task Contract: none. Code-Truth pre-apply: якорей процедур нет. Precedent: в spec только ADDED, MODIFIED/REMOVED нет; invariant KB нет; Load-Bearing ADR не снимается.
- Layer 2.5: PASS. Остановка разобрана: `reports/architecture-loop-redesign-2026-09-23.md` и ответ человека «оставить текст» в `debug.md` § Loop Detection и Extend (6). Повторный вопрос «переписать срез» не задавался. AcceptLoop(S1)=0, PatchRounds(S1)=5, порог уже закрыт этим ответом.
- Layer 3 Problem-Solution Trace: PASS. Why покрыт двумя Requirement. У каждого Requirement есть Scenario. Все 8 Scenario есть в `## Slices` и в чеклисте `S1.accept`. У среза есть S1.1–S1.9 и одна `S1.accept`. THEN наблюдаемые. `comment_suffix` пустой при `marker_style: minimal` — `process-only-marker-suffix` не сработал.
- Layer 4 Independent Challenge: CHALLENGE. `reports/design-challenge-2026-09-23-4.md`. Post-challenge classifier: G1–G5 повтор, закрыты текстом. G6 `implementation_invariant` (строка подтверждения остаётся в листе и при фразе «вопросов нет») — repair, не развилка. G7 — продуктовый выбор по видимым часам при нескольких факторах надбавки, ось EC-2 не отменяет. Альтернативы с `reopen-blocked` без нового факта в чат не выносились. `last_challenge_at` обновлён. Repair Loop не запускался: decision имеет приоритет, `repair_attempt` остаётся 0.
- Layer 5 Implementation Readiness: WARNING. `reports/architecture-task-readiness-2026-09-23.md`, overall `warning-level-gaps`, blocking gap нет. Manual-config: маркеров нет.
- verify_depth: full. Причина: хэш оси `282fa648…` совпал со снимком verification-2026-09-23-5, но отличался от оси последнего успешного разбора (verification-2026-09-23-3). decision_round: 2. Насыщение развилок не применено: остаток — новый видимый исход часов, не отложенное допущение.

## Источники

- `reports/quality-control-2026-09-23-5.md` (опора, новый файл не создавался)
- `reports/design-challenge-2026-09-23-4.md`
- `reports/architecture-task-readiness-2026-09-23.md`
- `reports/architecture-loop-redesign-2026-09-23.md`
- Алерты: продуктовая развилка нескольких факторов надбавки; repair отложен: место подтверждения при фразе «вопросов нет»
