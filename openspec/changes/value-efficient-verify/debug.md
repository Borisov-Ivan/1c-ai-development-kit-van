## Verify decision ledger

```yaml
closed_decisions:
  - id: unregistered_external_evidence
    summary: "Внешний контракт не обязателен для каждой ЗНИ; при явных условиях заказа незарегистрированное условие требует классификации, а отклонение закрывается только решением заказчика."
    closed_at: "2026-09-20"
    source: verify-user-answer
    confirmed_by: user
    authority: customer-direct
    external_contract_id: EC-001
open_decision_id: null
decision_round: 1
decision_round_max: 2
verify_depth: incremental
assumptions_accepted: []
repair_attempt: 0
last_challenge_at: "2026-09-20T13:55:15Z"
last_verification: reports/verification-2026-09-21-2.md
```

## External Contract Ledger

```yaml
external_contract:
  - id: EC-001
    topic:
      capability: value-efficient-verify
      anchor: "Requirement: Внешний контракт участвует в проверке"
      axis: custom:customer-acceptance-authority
      reference: n/a
    evidence:
      authority: customer-direct
      source: "entry-point:/opsx:verify@2026-09-20T22:25:00+09:00"
      assertion: "Явные требования могут отсутствовать; если конкретный заказ их содержит, они имеют повышенный вес для приёмки. Отклонение допустимо только после явного разбора и решения заказчика."
    decision:
      parity: matches
      reason: "Принцип включён в proposal, design, spec и tasks."
      confirmation: confirmed
      confirmed_at: "2026-09-20"
      confirmed_by: user
    signals:
      - id: verify-2026-09-20-authority-principle
        kind: customer-correction
        primary_event_id: verify-2026-09-20-authority-principle
        primary_event_at: "2026-09-20T22:25:00+09:00"
        source_fingerprint: ff2d011e5c3375642418ec236c022f844cac92c6d764407a42edca55627da2b6
```

## Extend — 2026-09-20

- Источник: ответ пользователя на развилку verify и уточнение принципа приёмки заказа.
- Что изменено: отсутствие внешних условий закреплено как нормальный случай; явное условие заказа получило повышенный авторитет; отклонение требует аргументов и решения заказчика; добавлены регистрация в new/extend и сценарии проверки.
- Disposition: accepted.
- Architect Gate: `reports/architecture-extend-coherence-2026-09-20.md`.
- Следующий шаг: incremental verify.

## Slice Gate Decisions

### Slice S1 — Внешний контракт и ранняя остановка повторной темы (2026-09-21)
Срез: S1 — Внешний контракт и ранняя остановка повторной темы
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: нет (S1.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S1-2026-09-21.md

### Slice S1 — Внешний контракт и ранняя остановка повторной темы (2026-09-21, вердикт)
Срез: S1 — Внешний контракт и ранняя остановка повторной темы
Решение: принят (manual shortcut)
Обоснование: без замечаний; Primary воспроизведён на фикстуре `fixture-ec-unclassified-axis`.
Изменения tasks: S1.accept [x]
Связанный отчёт: reports/slice-acceptance-S1-2026-09-21.md

### Slice S2 — Дельта-проверка и профильная эскалация (2026-09-21)
Срез: S2 — Дельта-проверка и профильная эскалация
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручное сравнение двух итогов проверки.
Изменения tasks: нет (S2.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S2-2026-09-21.md


