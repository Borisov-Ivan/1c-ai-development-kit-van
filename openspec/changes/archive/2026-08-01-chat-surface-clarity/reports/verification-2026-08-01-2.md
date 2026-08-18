---
verify_mode: pre-apply
change: chat-surface-clarity
date: 2026-08-01
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
  repair_attempt: 1
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-08-01T05:42:17Z"
    design.md: "2026-08-01T05:51:25Z"
    tasks.md: "2026-08-01T05:51:20Z"
    specs/chat-surface-clarity/spec.md: "2026-08-01T05:51:09Z"
  last_challenge_at: "2026-08-01T05:51:25Z"
---

# Verification — chat-surface-clarity (2026-08-01, после repair)

## Резюме для разработчика

chat-surface-clarity — можно запускать apply. План правит только тексты kit в чате (канон режима формы, AskQuestion, opsx), без кода 1С.

**Следующий шаг:** `/opsx:apply chat-surface-clarity`

Три волны: канон Mode Gate и зеркала → copy-paste команд → сверка SSOT и финальный grep. Приёмка — по отсутствию жаргона kit в текстах для чата.

Подправил в постановке: зафиксировал список grep-приёмки и границу «что копировать в чат»; уточнил задачи S3 и покрытие ярлыка паузы в apply.

## Что меняется в постановке

| Область | Что |
|---------|-----|
| Канон вопроса режима формы | `.cursor/rules/forms-mxl-mode-gate.mdc` (секция чата), decision-block, lexicon, faq/quick-start |
| Команды | AskQuestion/thin-chat в new/apply/status/review/verify |
| SSOT | opsx-output-style vs brief-card/lexicon; финальный grep по зонам из design |
| Не меняется | тела слоёв verify в отчётах, XML/BSL guards, промпты Task, код конфигурации 1С |

### Подправил в постановке

- Добавил в design операциональный список grep-приёмки и границу chat-facing для Mode Gate.
- Уточнил S3.2 путями SKILL; S3.4 — правило closure без повторной приёмки S1/S2.
- Добавил в spec сценарий про ярлык паузы apply; связал с S2.

### К сведению

- Первый прогон зафиксирован в `verification-2026-08-01.md` (до automatic repair).
- P2 meta-docs (`delivery-integrity`, `kit-template-workflow`) остаются опциональными.

## Технический аудит (для движка OpenSpec)

| Layer | Status | Notes |
|-------|--------|-------|
| Layer 1 | PASS | hygiene OK after repair |
| Layer 2 | PASS | QC `quality-control-2026-08-01-2.md` verdict OK; 10/10 scenarios |
| Layer 2.5 | PASS | no acceptance loop |
| Layer 3 | PASS | Why→Req→Scenario; new Scenario Apply pause covered; no implementation-leak |
| Layer 4 | APPROVE | `design-challenge-2026-08-01-2.md`; prior CHALLENGE gaps closed by repair |
| Layer 5 | PASS | `architecture-task-readiness-2026-08-01-2.md` ГОТОВО |

Precedent 2.4: ADDED-only, no archive capability, no knowledge index — OK.
Code-truth: no 1C procedure symbols — N/A / OK.
User Task Contract: none.

Repair Loop: attempt 1 applied (`debug.md` § Verify repair); re-verify full → GO.

## Источники

- `reports/quality-control-2026-08-01-2.md`
- `reports/design-challenge-2026-08-01-2.md`
- `reports/architecture-task-readiness-2026-08-01-2.md`
- Prior: `verification-2026-08-01.md`, `design-challenge-2026-08-01.md`, `quality-control-2026-08-01.md`
