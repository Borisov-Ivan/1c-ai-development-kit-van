---
verify_mode: pre-apply
change: chat-surface-clarity
date: 2026-08-01
verdict: GO
scope: slice-S1-boundary
snapshot:
  open_decision_id: null
  accepted_tasks: []
---

# Verification — chat-surface-clarity (граница S1, 2026-08-01)

## Резюме

Срез S1 («Канон Mode Gate и зеркала») готов к ручной приёмке. Рабочие задачи S1.1–S1.5 закрыты. Канон вопроса режима формы и зеркала (decision-block, lexicon, faq, quick-start, handoff-block) без skill/compile/«через skill»/«уже в поставке» в chat-facing; в new SKILL есть HALT процессных преамбул.

**Следующий шаг:** приёмка S1 → `/opsx:apply chat-surface-clarity` после вердикта.

## Primary S1 (spot-check)

| Критерий | Результат |
|----------|-----------|
| Канон Mode Gate: 3 варианта без skill/compile/поставки | OK (`forms-mxl-mode-gate.mdc` § Формулировка вопроса) |
| decision-block / lexicon не учат «через skill» как эталон | OK («через skill» только в anti-example «Плохо») |
| faq/quick-start на `form_mode`, макет в new не обещают | OK |
| HALT преамбул в openspec-new-change 5.d.1 | OK |

Код 1С / BSL — вне scope среза.
