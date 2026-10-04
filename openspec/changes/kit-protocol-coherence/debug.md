## Verify decision ledger

```yaml
closed_decisions:
  - id: batch-on-sliced-change
    choice: run-all-slices-accept-at-end
    authority: customer-direct
    premise:
      claim: "иногда нужно прогнать все срезы и принять в конце"
      anchor: ".cursor/commands/opsx-apply.md:21"
    decided_at: "2026-10-04"
  - id: acceptance-one-journey
    choice: narrow-primary-keep-slices
    authority: customer-direct
    premise:
      claim: "обязательный ход приёмки среза один, остальные сценарии необязательны"
      anchor: "openspec/changes/kit-protocol-coherence/reports/quality-control-2026-10-04.md"
    decided_at: "2026-10-04"
  - id: batch-end-card
    summary: "В конце пакета одна карточка с главной проверкой каждого прогнанного среза; один ответ принимает их вместе или возвращает вместе."
    choice: all-slices-one-card
    closed_at: "2026-10-04"
    source: verify-user-answer
    confirmed_by: user
    premise:
      claim: "в конце пакета одна карточка на все прогнанные срезы"
      anchor: "openspec/changes/kit-protocol-coherence/debug.md#Extend — 2026-10-04"
    decided_at: "2026-10-04"
open_decision_id: null
decision_round: 3
decision_round_max: 2
verify_depth: full
assumptions_accepted: []
repair_attempt: 0
open_known_questions: []
```

## Extend — 2026-10-04

- Источник: `--from-verify` `reports/verification-2026-10-04.md`, ответ в чате: карточка на все прогнанные срезы.
- Что изменено: конец пакета записан как одна карточка с главной проверкой каждого прогнанного среза; правило срезов добавлено в копии этого стыка; источник «дополнение новее проверки» назван секцией журнала; граница новых стыков записана как вне заявки; замечание про строку диспетчера оставлено в рисках.
- Темы: G1 — accepted; G2 — accepted; G3 — accepted; G4 — deferred (решение о строке диспетчера уже записано, рецепта на удаление нет); G5 — accepted.
- Architect Gate: `reports/design-challenge-2026-10-04.md`
- Следующий шаг: `/opsx:verify kit-protocol-coherence`

## Extend — 2026-10-04 (2)

- Источник: repair-from-verify, `reports/design-challenge-2026-10-04-2.md`
- Что изменено: формат конечной карточки пакета записан строкой сводной таблицы правила срезов, команда её формулу не копирует; ответ на карточку — на следующем запуске; «принято» для записей одного пакета принимает их все; возврат вместе идёт по правилу размещения дефекта; внутри пакета зависимый срез не ждёт приёмку предшественника; пока пакет идёт, молчит только вопрос приёмки; «постановку меняли» читается по хэшам снимка отчёта, в том числе в тот же день; якорь предпосылки конца пакета указывает на секцию дополнения, а не на вопрос проверки.
- Темы: G2 — accepted; G3 — accepted; G6 — accepted; G7 — accepted; G8 — accepted; G4 — deferred (строка диспетчера уже в рисках, рецепта на удаление нет); G9 — accepted.
- Architect Gate: `reports/design-challenge-2026-10-04-2.md`
- Следующий шаг: проверка постановки продолжается в том же прогоне
