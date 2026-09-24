## Verify decision ledger

```yaml
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
```

## External Contract Ledger

```yaml
external_contract:
  - id: EC-1
    topic:
      capability: tz-tech-project
      anchor: "второй вывод техпроекта"
      axis: trigger
      reference: "подтверждение согласования в листе, не просьба подготовить техпроект"
    axis: trigger
    source: "entry-point:/opsx:verify@2026-09-23T13:30:00+09:00"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-09-23T13:30:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec1
        kind: customer-correction
        primary_event_id: verify-answer-2026-09-23T13:30:00+09:00
        primary_event_at: "2026-09-23T13:30:00+09:00"
        source_fingerprint: "8adc4edf5832c579341d313ed75907ac1b7dc4ca96b39eb3a45d09cb030375cd"
  - id: EC-2
    topic:
      capability: tz-tech-project
      anchor: "часы из прозы"
      axis: visible-result
      reference: "надбавка после умножения нижней границы на коэффициент и сама на коэффициент не умножается"
    axis: visible-result
    source: "entry-point:/opsx:verify@2026-09-23T13:30:00+09:00"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-09-23T13:30:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec2
        kind: customer-return
        primary_event_id: verify-answer-2026-09-23T13:30:00+09:00
        primary_event_at: "2026-09-23T13:30:00+09:00"
        source_fingerprint: "01e6ca72010078b06debbf1aef030b051762535b9310f5e07359bdc1eca27cdc"
  - id: EC-3
    topic:
      capability: tz-tech-project
      anchor: "округление часов"
      axis: visible-result
      reference: "дробный результат поднимается до следующего целого часа"
    axis: visible-result
    source: "entry-point:/opsx:verify@2026-09-23T13:30:00+09:00"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-09-23T13:30:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec3
        kind: customer-return
        primary_event_id: verify-answer-2026-09-23T13:30:00+09:00
        primary_event_at: "2026-09-23T13:30:00+09:00"
        source_fingerprint: "41e44509f908bacb28b3a397f12d24358b886b9d4f9197de4258f0ab08d20529"
  - id: EC-4
    topic:
      capability: tz-tech-project
      anchor: "несколько факторов надбавки"
      axis: visible-result
      reference: "нижние границы названных факторов складываются и на коэффициент не умножаются"
    axis: visible-result
    source: "entry-point:/opsx:extend@2026-09-24T09:16:00+09:00"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-09-24T09:16:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec4
        kind: customer-return
        primary_event_id: extend-surcharge-sum-2026-09-24T09:16:00+09:00
        primary_event_at: "2026-09-24T09:16:00+09:00"
        source_fingerprint: "9853729530e172057f6ec74edbdcde7ab6473dc3b23bb37a551ebad01c5b91fa"
  - id: EC-5
    topic:
      capability: tz-tech-project
      anchor: "дыры и постановка"
      axis: visible-result
      reference: "дыры и связь с прошлыми изменениями через протокол исследования; после подтверждения файл постановки, каталог задачи не создаётся"
    axis: visible-result
    source: "entry-point:/opsx:extend@2026-09-24T09:16:00+09:00"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-09-24T09:16:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec5
        kind: customer-return
        primary_event_id: extend-explore-protocol-2026-09-24T09:16:00+09:00
        primary_event_at: "2026-09-24T09:16:00+09:00"
        source_fingerprint: "8f432c8e55e60b46b2125003d8543ff4d7e98099a21e5ae777c3629448c48554"
  - id: EC-6
    topic:
      capability: tz-tech-project
      anchor: "нет подходящей строки справочника"
      axis: visible-result
      reference: "в листе вопрос, часы по этой работе не выдумываются и не ставятся, пока нет ответа"
    axis: visible-result
    source: "entry-point:/opsx:verify@2026-09-24T10:00:00+09:00"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-09-24T10:00:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec6
        kind: customer-return
        primary_event_id: verify-answer-zero-row-2026-09-24T10:00:00+09:00
        primary_event_at: "2026-09-24T10:00:00+09:00"
        source_fingerprint: "a3ff2238d8230e5bb3fb14fb8b7bbde54db522d0e2e4258ecd457989b9d2fa99"
```

## Extend — 2026-09-23

- Источник: `--from-verify` `reports/verification-2026-09-23.md` (repair-from-verify, attempt 1)
- Что изменено: в постановке зафиксированы имена `<имя>-вопросы.md` и `<имя>-техпроект.md`, чтение ответов из листа, дыра если имени нет в `src/КАСК/cf/`, форма пункта листа, сбор часов из прозы, папка шаблонов не второй источник. Ось команды (два файла, копии правил в навыке) не менялась.
- Disposition: answer-protocol accepted; output-paths accepted; missing-object-hole accepted; question-item-shape accepted; hours-from-prose accepted; template-not-second-source accepted. one-file-output rejected (ломает отдельный лист). template-runtime-ssot rejected (ось копий в навыке сохранена, в миграцию добавлено предупреждение).
- Architect Gate: не требовался
- Отчёт: `reports/design-challenge-2026-09-23.md`, `reports/verification-2026-09-23.md`
- Следующий шаг: повторная проверка постановки

## Extend — 2026-09-23 (2)

- Источник: `--from-verify` повторный разбор `reports/design-challenge-2026-09-23-2.md` (repair-from-verify, attempt 2)
- Что изменено: в требованиях зафиксированы два варианта у вопроса, часы как нижняя граница строки справочника на коэффициент, надбавка только за названный в задании фактор, сохранение ответов при той же формулировке, папка шаблонов не меняет следующий запуск, в навык не копируется ожидание подтверждения в чате. Ось двух файлов и копий в навыке не менялась.
- Disposition: spec-hours-range accepted; answer-preserve accepted; template-not-runtime accepted; overview-entry-not-copied accepted; two-phase-output rejected (один запуск по-прежнему пишет оба файла).
- Architect Gate: не требовался
- Отчёт: `reports/design-challenge-2026-09-23-2.md`
- Следующий шаг: повторная проверка постановки

## Extend Coherence Audit — 2026-09-23

- Триггер: semantic
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-09-23.md`
- Решение пользователя: accepted recommendations — вариант 1 по надбавке и два последовательных вывода

## Extend — 2026-09-23 (3)

- Источник: подтверждение брифа, вариант 1, плюс требование двух последовательных выводов
- Что изменено: первый вывод — `<имя>-вопросы.md` и `<имя>-согласование.md` языком обзора с часами и предложением подготовить техпроект. Второй вывод — `<имя>-техпроект.md` таблицами без кода процедур, только по этой просьбе. Надбавка прибавляется после умножения нижней границы на коэффициент и сама на коэффициент не умножается. Входящий файл задания не заменяется бланком. Две строки справочника — вопрос в листе. Пустой лист — фраза «вопросов нет».
- Disposition: surcharge-after-coefficient accepted; two-sequential-outputs accepted; chtz-as-output-table accepted; two-phase-output (прежний отказ «один запуск пишет оба файла сразу») superseded этим подтверждением. input-file-rewrite rejected.
- Architect Gate: `reports/architecture-extend-coherence-2026-09-23.md`
- Отчёт: `reports/architecture-extend-coherence-2026-09-23.md`
- Следующий шаг: `/opsx:verify tz-tech-project`

## Extend — 2026-09-23 (4)

- Источник: подтверждение брифа, вариант 2
- Что изменено: после формулы часов дробный результат поднимается до следующего целого часа; целое число не меняется. Уже заполненные в задании строки часов по-прежнему не затираются.
- Disposition: round-hours-up accepted
- Architect Gate: не требовался
- Следующий шаг: `/opsx:verify tz-tech-project`

## Extend — 2026-09-23 (5)

- Источник: ответ на проверку `reports/verification-2026-09-23-4.md` — вариант A и уточнение: второй шаг подтверждать, не просить
- Что изменено: техпроект пишется, когда в листе вопросов есть подтверждение согласования и команду запускают снова. Отдельная просьба подготовить техпроект снята. Согласование на первом запуске по-прежнему пишется сразу. Часы: (нижняя граница × коэффициент) + надбавка, дробь вверх до целого, надбавка на коэффициент не умножается.
- Disposition: second-step-confirmation accepted; hours-surcharge-after-coefficient accepted; hours-round-up accepted. Триггер «по просьбе подготовить техпроект» superseded подтверждением в листе.
- Architect Gate: не требовался
- Следующий шаг: `/opsx:verify tz-tech-project`

## Loop Detection — 2026-09-23

- Триггер: verify Layer 2.5
- Срез: S1
- AcceptLoop / PatchRounds: 0 / 5 (порог acceptance_loop_max=3)
- Отчёт редизайна: `reports/architecture-loop-redesign-2026-09-23.md`
- Рекомендация архитектора: minimal
- Решение пользователя: accepted minimum — текст среза не переписывать до прогона команды на файле задания

## Extend — 2026-09-23 (6)

- Источник: ответ на проверку `reports/verification-2026-09-23-5.md` — оставить текст среза
- Что изменено: в зеркало решений добавлен стоп переписки среза до прогона команды на файле задания. Задачи, требования и описание поведения не переписывались.
- Disposition: slice-text-freeze accepted. Переписать срез заново — rejected.
- Architect Gate: `reports/architecture-loop-redesign-2026-09-23.md`
- Следующий шаг: `/opsx:verify tz-tech-project`

## Extend Coherence Audit — 2026-09-24

- Триггер: semantic
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-09-24.md`
- Решение пользователя: accepted recommendations — протокол исследования вместо чеклиста, сумма надбавок, файл постановки, перепись среза

## Extend — 2026-09-24

- Источник: ответ на проверку `reports/verification-2026-09-24.md` (сложить нижние границы надбавок) и подтверждённый бриф, вариант 1 (протокол исследования внутри команды)
- Что изменено: дыры и связь с прошлыми изменениями берутся протоколом исследования, отдельный чеклист и отдельная сверка имён сняты. После подтверждения в листе пишется `<имя>-постановка.md`, каталог задачи не создаётся. Несколько факторов надбавки складываются. В листе всегда есть строка подтверждения. Заморозка текста среза снята, срез переписан. Задачи S1.2, S1.4, S1.5, S1.6, S1.8 возвращены в работу, добавлена S1.10.
- Темы: G7 → EC-4; G6 закрыт текстом (строка подтверждения и при фразе «вопросов нет»); EC-5 новая.
- Disposition: explore-protocol-for-gaps accepted; own-checklist-removed accepted; separate-export-check-removed accepted; multi-surcharge-sum accepted; постановка-as-output accepted; slice-text-freeze superseded; create-change rejected.
- Architect Gate: `reports/architecture-extend-coherence-2026-09-24.md`
- Следующий шаг: `/opsx:verify tz-tech-project`

## Extend — 2026-09-24 (2)

- Источник: `--from-verify` `reports/verification-2026-09-24-2.md` — ответ A
- Что изменено: если описанной работе не подходит ни одна строка справочника, в листе вопрос, часы по этой работе не выдумываются и не ставятся, пока нет ответа. Файл постановки пишется блоком «Постановка ЗНИ» (симптом, корневая причина, что менять, файлы, приёмка, связь с уже сделанными изменениями). Каталог задачи по-прежнему не создаётся.
- Темы: G9 → EC-6; G8 закрыт текстом (блок постановки).
- Disposition: hours-zero-catalog-row-question accepted; postanovka-consumer-block accepted. Вариант «пробел без часов» — rejected.
- Architect Gate: не требовался
- Отчёт: `reports/verification-2026-09-24-2.md`, `reports/design-challenge-2026-09-24.md`
- Следующий шаг: `/opsx:verify tz-tech-project`

## Extend — 2026-09-24 (3)

- Источник: `--from-verify` `reports/design-challenge-2026-09-24-2.md` (repair-from-verify, attempt 1)
- Что изменено: в задачах навыка зафиксировано, что строка подтверждения заполнена, когда в ней есть непустая пометка, и что при уже заполненном подтверждении неотвеченный вопрос о часах оставляет работу в техпроекте без часов. Ось решений и требования не менялись.
- Темы: G10; G11.
- Disposition: confirmation-nonempty accepted; hours-question-open-still-writes-techproject accepted.
- Architect Gate: не требовался
- Отчёт: `reports/design-challenge-2026-09-24-2.md`
- Следующий шаг: повторная проверка постановки

## Slice Gate Decisions

### Slice S1 — Техпроект по файлу задания (2026-09-24)
Срез: S1 — Техпроект по файлу задания
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: нет (S1.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S1-2026-09-24.md
