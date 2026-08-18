---
verify_mode: pre-apply
change: explain-after-review-apply-scope
date: 2026-08-09
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
  repair_attempt: 2
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "Обогащение procedures из Code-Truth — later"
  artifacts_mtime:
    proposal.md: "2026-08-09T11:23:34"
    design.md: "2026-08-09T14:46:49"
    tasks.md: "2026-08-09T14:41:04"
    specs/explain-post-implementation-scope/spec.md: "2026-08-09T14:46:47"
  last_challenge_at: "2026-08-09T14:46:49"
---

## Резюме для разработчика

explain-after-review-apply-scope — можно запускать apply. План дописывает kit: после ревью и apply появляется предложение `/opsx:explain`, а в первом брифе уже виден охват обработанного кода.

**Следующий шаг:** `/opsx:apply explain-after-review-apply-scope`

Меняются skills и команды kit (`review`, `openspec-apply-change`, `openspec-explain`, guide/commands) — продуктовый BSL не трогаем. Режим apply: mechanical. В постановке автоматически уточнены канон `code-map` как источника охвата, приоритет propose относительно MUST_FIX и разделение слотов Охват/Контекст.

### Подправил в постановке

- Закрыл правила propose vs «одна команда» / MUST_FIX, SSOT apply = `code-map`, MVP без эвристики старых отчётов.
- Согласовал норматив HALT: UX в Охвате, список path только в Контексте.

### К сведению

- Опциональные пункты приёмки названы чуть короче, чем заголовки сценариев в spec — на покрытие не влияет.
- Параллельная ЗНИ `independent-review-disposition` вне scope (disposition не трогаем).

## Что меняется в постановке

**Область:** `.cursor/skills` + `.cursor/commands` + `.cursor/docs` (kit), не `src/` продукта.

**Точки изменения:**

- Секция `## Explain scope` в review-отчётах и в `code-map` после apply с BSL.
- Propose `/opsx:explain` в финалах review/release-review/apply ниже fix/extend.
- Prefill B-explain из handoff с подтверждением до карты точек.

**Не меняется:** explore-shortcut explain; disposition as-designed/queue-fix; продуктовый код 1С.

## Технический аудит (для движка OpenSpec)

| Layer | Status | Notes |
|-------|--------|-------|
| Layer 1 Hygiene | PASS | checkboxes, slice-gate, fences OK; form_mode n/a |
| Layer 2 Internal Coherence | PASS | QC OK (`quality-control-2026-08-09-3.md`); User Task Contract none; precedent n/a (ADDED-only, no archive); code-truth kit paths exist (pre-apply) |
| Layer 2.5 Loop Detection | PASS | no debug accept-loop history |
| Layer 3 Problem-Solution Trace | PASS | Why↔Requirements↔Scenarios↔S1; no implementation-leak; marker_suffix empty |
| Layer 4 Independent Challenge | APPROVE | `design-challenge-2026-08-09-3.md` after repair-2; axis handoff+prefill |
| Layer 5 Implementation Readiness | PASS | `architecture-task-readiness-2026-08-09-2.md` readiness: ready; no blocking gaps |

Repair Loop: attempt 1 — gaps D1/D2/D2a/D4/D5 from `design-challenge-2026-08-09.md`; attempt 2 — Spec Brief HALT vs D4 from `design-challenge-2026-08-09-2.md`. Final challenge APPROVE.

## Источники

- `reports/quality-control-2026-08-09-3.md`
- `reports/design-challenge-2026-08-09.md` (CHALLENGE → repair-1)
- `reports/design-challenge-2026-08-09-2.md` (CHALLENGE → repair-2)
- `reports/design-challenge-2026-08-09-3.md` (APPROVE)
- `reports/architecture-task-readiness-2026-08-09-2.md`
- alerts: none blocking; info SUGGESTION accept-scenario-name-alignment (QC)
