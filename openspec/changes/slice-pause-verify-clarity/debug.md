## Verify decision ledger

```yaml
closed_decisions:
  - id: package_joint_answer
    summary: "Пакет срезов по-прежнему закрывается одним ответом: принять все вместе или вернуть все вместе. Срез, которому нужен уже прогнанный в пакете, стартует не дожидаясь приёмки. Названия срезов на конечной карточке остаются."
    closed_at: "2026-10-14"
    source: verify-user-answer
    confirmed_by: user
    authority: customer-direct
    external_contract_id: EC-2
    premise:
      claim: "Один ответ принимает срезы пакета вместе или возвращает их вместе, зависимый срез стартует не дожидаясь приёмки."
      anchor: "openspec/specs/kit-protocol-coherence/spec.md:10"
  - id: refutation_after_answer
    summary: "После ответа на несовпадение выбора с модулем тот же факт не спрашивают. Пока выбор не подтверждён, он не довод против других вариантов. «Оставляю» — следующая проверка только по затронутому. «Меняю» — весь план. Пустое основание у выбора, который меняет результат, по-прежнему не пропускается."
    closed_at: "2026-10-14"
    source: verify-user-answer
    confirmed_by: user
    authority: customer-direct
    external_contract_id: EC-3
    premise:
      claim: "После ответа тот же факт не спрашивают снова; неподтверждённый выбор не довод; подтверждение сужает следующую проверку, смена читает план целиком."
      anchor: "openspec/specs/verify-stop-repeat/spec.md:113"
  - id: estimate_mark_same_card
    summary: "Расчёт в карточке помечен как оценка. Дыра в доказательстве — вопрос в той же карточке, отдельная проверка не стартует. Оговорка «объекта ещё нет, вопрос о тексте плана» остаётся."
    closed_at: "2026-10-14"
    source: verify-user-answer
    confirmed_by: user
    authority: customer-direct
    external_contract_id: EC-4
    premise:
      claim: "Утверждение без места возникновения становится вопросом о факте в той же карточке без отдельного разбора; расчёт помечен как оценка."
      anchor: "openspec/specs/verify-stop-repeat/spec.md:37"
  - id: repeat_only_on_change
    summary: "После ответа тот же вопрос не возвращается. Запись, которая только сохраняет уже данный ответ, вопрос не открывает. Если с того ответа результат изменился, карточка показывает, что было и что стало, и спрашивает только про это изменение. Новое указание без ответа по-прежнему спрашивается."
    closed_at: "2026-10-14T15:33:00+09:00"
    source: verify-user-answer
    confirmed_by: user
    authority: customer-direct
    external_contract_id: EC-1
    premise:
      claim: "Повтор того же ответа не даёт отличить смену факта от механического подтверждения и снижает контроль."
      anchor: "openspec/changes/slice-pause-verify-clarity/reports/verification-2026-10-14-2.md"
open_decision_id: null
decision_round: 2
verify_depth: incremental
assumptions_accepted: []
```

## Extend — 2026-10-14

- Источник: `--from-verify` `reports/verification-2026-10-14.md`, ответ пользователя на пакет: пакет одним ответом оставить, последствия ответа на несовпадение с модулем оставить, пометку «оценка» и вопрос в той же карточке оставить.
- Что изменено: в дельты требований возвращены три уже работающих правила рядом с новыми фразами паузы. В решения и контракт поведения дописаны те же предложения. В задачах явно не переписывать абзацы, где эти правила уже живут. Строку отмены в обосновании замен не добавляли.
- Темы: без номера разрыва и без контракта заказчика. Три ответа одной карточки, идентичность по решению человека, не слияние по близости текста.
- Architect Gate: `reports/architecture-extend-coherence-2026-10-14.md`
- Вердикт сверки цельности: заявка остаётся одной.
- Следующий шаг: `/opsx:verify slice-pause-verify-clarity`

## Extend Coherence Audit — 2026-10-14

- Триггер: semantic
- Drift-check из брифа: drift-warning
- Вердикт архитектора: coherent
- Отчёт: `reports/architecture-extend-coherence-2026-10-14.md`
- Решение пользователя: accepted recommendations — три правила вписаны в требования и задачи

## External Contract Ledger

```yaml
external_contract:
  - id: EC-1
    topic:
      capability: verify-stop-repeat
      anchor: "повтор уже данного ответа"
      axis: visible-result
      reference: "тот же вопрос не возвращается; при смене результата карточка показывает, что было и что стало"
    axis: visible-result
    source: "entry-point:/opsx:extend@2026-10-14T15:33:00+09:00"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-10-14T15:33:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec1
        kind: customer-correction
        primary_event_id: verify-answer-2026-10-14T15:33:00+09:00
        primary_event_at: "2026-10-14T15:33:00+09:00"
        source_fingerprint: "b4a5acdd439ce58755b17c8f18c11e2d3a631e57b9adda71991db5cfad6449e3"
  - id: EC-2
    topic:
      capability: kit-protocol-coherence
      anchor: "один ответ на сдачу срезов"
      axis: visible-result
      reference: "один ответ принимает срезы пакета вместе или возвращает их вместе, зависимый срез стартует сразу"
    axis: visible-result
    source: "debug.md#Extend — 2026-10-14"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-10-14T14:41:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec2
        kind: customer-return
        primary_event_id: verify-answer-2026-10-14T14:41:00+09:00
        primary_event_at: "2026-10-14T14:41:00+09:00"
        source_fingerprint: "b72e9e0887396518f3d16864e80aa80774d9520db8f5b8b83ffbbf8dd03c1f69"
  - id: EC-3
    topic:
      capability: verify-stop-repeat
      anchor: "последствия ответа про несовпадение с модулем"
      axis: visible-result
      reference: "после ответа тот же факт не спрашивают; оставляю смотрит только затронутое; меняю читает весь план"
    axis: visible-result
    source: "debug.md#Extend — 2026-10-14"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-10-14T14:41:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec3
        kind: customer-return
        primary_event_id: verify-answer-2026-10-14T14:41:00+09:00
        primary_event_at: "2026-10-14T14:41:00+09:00"
        source_fingerprint: "a7189941f7fb29d177883eabfd735551414ac41c9d5c9978d825d159b254e9d3"
  - id: EC-4
    topic:
      capability: verify-stop-repeat
      anchor: "оценка в той же карточке"
      axis: visible-result
      reference: "расчёт помечен как оценка, дыра доказательства не запускает вторую проверку"
    axis: visible-result
    source: "debug.md#Extend — 2026-10-14"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-10-14T14:41:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec4
        kind: customer-return
        primary_event_id: verify-answer-2026-10-14T14:41:00+09:00
        primary_event_at: "2026-10-14T14:41:00+09:00"
        source_fingerprint: "579f31b9cc285b6acf7242be6f31a28a7ccfbd0c73d04d9eac922faf1f4a07a5"
```

## Extend — 2026-10-14 (2)

- Источник: подтверждение брифа, вариант 1. Человек: после ответа тот же вопрос не возвращается; если результат изменился, карточка показывает, что было и что стало.
- Что изменено: в требования добавлены сценарии «Сохранение ответа не открывает вопрос» и «С ответа изменился результат». В решения и контракт поведения дописаны те же фразы, без нового абзаца контракта и без строки отмены. В срез S2 добавлены две задачи до приёмки и два необязательных пункта приёмки. Сценарий «Слова указания в плане не закрывают указание» не переписан: указание без ответа человека остаётся вопросом.
- Темы: EC-1. Три ранее данных ответа остаются EC-2, EC-3, EC-4 и повторно не спрашиваются.
- Architect Gate: `reports/architecture-extend-coherence-2026-10-14-2.md`
- Вердикт сверки цельности: drift-warning, заявка остаётся одной.
- Следующий шаг: `/opsx:verify slice-pause-verify-clarity`

## Extend Coherence Audit — 2026-10-14 (2)

- Триггер: semantic
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-10-14-2.md`
- Решение пользователя: accepted recommendations — вариант 1, вопрос только про изменение результата
