## Verify decision ledger

```yaml
closed_decisions:
  - id: ec_009_visible_result
    summary: "Ось видимого результата совпадает с референсом."
    closed_at: "2026-09-21T10:05:00+09:00"
    source: verify-user-answer
    confirmed_by: user
    authority: accepted-reference
    external_contract_id: EC-009
  - id: ec_010_error_recovery
    summary: "Ось восстановления после ошибки совпадает с референсом."
    closed_at: "2026-09-21T10:25:00+09:00"
    source: verify-user-answer
    confirmed_by: user
    authority: accepted-reference
    external_contract_id: EC-010
open_decision_id: null
decision_round: 1
decision_round_max: 2
verify_depth: incremental
assumptions_accepted: []
repair_attempt: 0
last_verification: reports/verification-2026-09-21.md
```

## External Contract Ledger

```yaml
external_contract:
  - id: EC-009
    topic:
      capability: fixture-ec-unclassified-axis
      anchor: "Requirement: Видимый результат действия"
      axis: visible-result
      reference: accepted-ref-demo
    evidence:
      authority: accepted-reference
      source: "openspec/changes/fixture-ec-unclassified-axis/design.md#Behavior-Contract"
      assertion: "После действия пользователя результат виден на форме"
    decision:
      parity: matches
      reason: "Ось совпадает с Behavior Contract п.1."
      confirmation: confirmed
      confirmed_at: "2026-09-21"
      confirmed_by: user
    signals:
      - id: fixture-ref-visible-2026-09-21
        kind: reference-evidence
        primary_event_id: fixture-ref-visible-2026-09-21
        primary_event_at: "2026-09-21T10:00:00+09:00"
        source_fingerprint: "52cec0e3fe03d193e109255dbb3866c6a687a210b5037f552768188c889b92d8"
  - id: EC-010
    topic:
      capability: fixture-ec-unclassified-axis
      anchor: "Requirement: Восстановление после ошибки"
      axis: error-recovery
      reference: accepted-ref-demo
    evidence:
      authority: accepted-reference
      source: "openspec/changes/fixture-ec-unclassified-axis/design.md#Behavior-Contract"
      assertion: "После ошибки состояние восстанавливается без ручной очистки"
    decision:
      parity: matches
      reason: "Ось совпадает с Behavior Contract п.2."
      confirmation: confirmed
      confirmed_at: "2026-09-21T10:25:00+09:00"
      confirmed_by: user
    signals:
      - id: fixture-ref-2026-09-21
        kind: reference-evidence
        primary_event_id: fixture-ref-2026-09-21
        primary_event_at: "2026-09-21T10:01:00+09:00"
        source_fingerprint: "6ab87735afc08104cccee4db9f7ceb796a1736585de8d3fe645d9ed310b5ef67"
```
