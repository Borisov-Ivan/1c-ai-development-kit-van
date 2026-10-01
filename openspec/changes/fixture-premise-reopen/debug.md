## Verify decision ledger

```yaml
closed_decisions:
  - id: usage_line_is_enough
    summary: "Соседняя строка использования значения достаточна как доказательство выбора."
    closed_at: "2026-09-21T10:05:00+09:00"
    source: verify-user-answer
    confirmed_by: user
    premise:
      claim: "Соседняя строка шаблона, где значение только используется, достаточна как доказательство выбора"
      anchor: ".cursor/docs/templates/decision-block.md:110"
    authority: customer-direct
    external_contract_id: EC-1
  - id: verdict_is_binary
    summary: "Итог проверки бывает только GO или NO-GO."
    closed_at: "2026-09-21T10:20:00+09:00"
    source: verify-user-answer
    confirmed_by: user
    premise:
      claim: "Итог проверки бывает только GO или NO-GO"
      anchor: ".cursor/skills/openspec-verify-change/templates/report-header.md:77"
open_decision_id: null
decision_round: 1
decision_round_max: 2
verify_depth: incremental
assumptions_accepted: []
```

## External Contract Ledger

```yaml
external_contract:
  - id: EC-1
    topic:
      capability: fixture-premise-reopen
      anchor: "Requirement: Место доказательства"
      axis: custom:proof-origin
      reference: accepted-ref-demo
    evidence:
      authority: customer-direct
      source: "openspec/changes/fixture-premise-reopen/design.md#Behavior-Contract"
      assertion: "Доказательством служит место возникновения значения"
    decision:
      parity: matches
      reason: "Закрыто ответом заказчика по usage_line_is_enough."
      confirmation: confirmed
      confirmed_at: "2026-09-21"
      confirmed_by: user
    signals:
      - id: fixture-premise-ec1
        kind: reference-evidence
        primary_event_id: fixture-premise-ec1
        primary_event_at: "2026-09-21T10:00:00+09:00"
        source_fingerprint: "f40aa63c5282f084b165c71f73cfe117194b7eb5afc1e3a8e61c7aa6c795b799"
```

## Extend — 2026-09-01

- Темы: EC-1 первое упоминание
- Architect Gate: не требовался

## Extend — 2026-09-15

- Темы: EC-1 переоткрыта (одно переоткрытие после первого упоминания; второго нет)
- Architect Gate: не требовался
