---
verify_mode: pre-apply
change: hardcode-justification-gate
date: 2026-08-08
verdict: GO
scope: slice-S1
snapshot:
  open_decision_id: null
  slice: S1
  working_tasks_complete: [S1.1, S1.1b, S1.2, S1.3, S1.4]
  accept_pending: S1.accept
---

## Incremental slice check — S1 «Реестр и запах»

| Check | Result |
|-------|--------|
| AP-055 в Writer bulletin + таблица `.cursor/rules/bsl-antipatterns.mdc` | OK |
| Полная карточка AP-055 в `.cursor/docs/antipatterns/bsl-antipatterns.md` | OK |
| Граница «не путать» с литералами протокола/enum | OK (bulletin + карточка § «Не путать») |
| Scope-as-literals в `existing-mechanism-priority.mdc` рядом с Substituted Authority | OK |
| SSOT шаблона `## Hardcode Justification` в том же файле | OK |
| Номер AP свободен (нет второго AP-055) | OK |

**Verdict:** GO — handoff на приёмку S1.
