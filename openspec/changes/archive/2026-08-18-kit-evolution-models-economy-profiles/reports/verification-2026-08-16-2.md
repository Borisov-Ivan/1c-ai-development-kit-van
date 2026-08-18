---
verify_mode: pre-apply
change: kit-evolution-models-economy-profiles
date: 2026-08-16
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
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions:
    - id: independent_challenge_carrier
      summary: "Пока в описании Task нет слага самой дорогой эскалации, независимый разбор постановки идёт на Opus 5 (Primary обычного архитектора), не на GPT-5.6 и не без model=. Слаг Fable не передаётся и не угадывается; когда появится в enum — снова D1a."
      closed_at: "2026-08-16"
      source: verify-user-answer
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-08-16T13:07:21+09:00"
    design.md: "2026-08-16T13:06:26+09:00"
    tasks.md: "2026-08-16T13:07:37+09:00"
    specs/always-apply-context-budget/spec.md: "2026-08-16T13:07:17+09:00"
    specs/chat-model-profiles/spec.md: "2026-08-16T12:33:36+09:00"
    specs/delegation-safeguards/spec.md: "2026-08-16T11:28:50+09:00"
    specs/rules-hygiene/spec.md: "2026-08-16T11:15:07+09:00"
    specs/subagent-model-mapping/spec.md: "2026-08-16T12:33:32+09:00"
  last_challenge_at: "2026-08-16T13:06:26+09:00"
---

## Резюме для разработчика

kit-evolution-models-economy-profiles — можно запускать apply. Таблица ролей субагентов переезжает на живые модели, постоянный контекст худеет без снятия гейтов, чат команд остаётся на Grok.

План правит `.cursor/rules` (`model-selection.mdc`, сжатие always-apply) и промпт ревьювера; кода 1С нет.

**Следующий шаг:** `/opsx:apply kit-evolution-models-economy-profiles`

Полный отчёт: openspec/changes/kit-evolution-models-economy-profiles/reports/verification-2026-08-16-2.md

Пока в списке вызова нет самой дорогой модели, независимый разбор постановки идёт на Opus 5 — той же модели, что обычная постановка задач.

## Что меняется в постановке

**Расширение / конфигурация:** kit (`.cursor/**`, `AGENTS.md`); `src/` не затрагивается.

**Точки изменения:**

- `.cursor/rules/model-selection.mdc` — живая таблица ролей, самосверка списка моделей, двухшаговые цепочки, закрытая эскалация архитектора.
- `.cursor/rules/1c-agent-delegation.mdc` — сжатие always-apply, якоря write-guard / carve-out ревью / поверхности / KB CONTEXT.
- `.cursor/rules/chat-output-budget.mdc` — слияние стабов навигатора и дисциплины диалога.
- Новые `model-adaptation.mdc` и профили `model-grok4.mdc` / `model-fable5.mdc` / `model-gpt56.mdc` / `model-opus5.mdc`.
- `.cursor/agents/onec-code-reviewer.md` — диета промпта; эталон сравнения — фрагменты BSL в `.cursor/docs/standard/std-06-code-modules.md`.

**Что НЕ меняется:** состав агентов и OpenSpec workflow; запрет прямой правки BSL/XML, LINT GATE, обязательность ревьювера, HALT-триггеры; семантика ADR-0001 (чат vs агент) и ADR-0003 (disposition ревью) — упаковка, не отмена.

**Связанные ADR / KB / архив:** ADR-0001 (Load-Bearing), ADR-0003 (Load-bearing). Архивных delta specs с теми же capability нет.

### К сведению

- Независимый разбор этой проверки шёл на модели чата: выбранные модели вызова уперлись в лимит API.
- Таблица срезов маппит capabilities; привязка сценариев — в «Связь со spec» каждого среза и в списке «Scenarios из spec».
- Срез диеты ревьювера своей дельты spec не создаёт — расширяет `always-apply-context-budget`.
- `openspec/project.md` в kit-репо отсутствует по D12; `openspec/glossary.md` есть.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы, `<!-- slice-gate -->` у S1–S6, fences, `form_mode: n/a`. Авто-исправлений нет.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-16-3.md` verdict OK. 36/36 Scenario покрыты. UTC: none. 8b self-achievable: OK. Precedent 2.4: нет MODIFIED/REMOVED; invariant KB нет; Blast Radius ADR-0003 заполнен (`precedent-documented`). Code-Truth: kit-пути, не символы 1С; phantom-symbol не применялся. SUGGESTION leftover (Grok lead-in, named-bullet polish) — не блокирует.
- **Layer 2.5 (Loop Detection):** PASS. Нет Slice Gate Decisions; все `S<N>.accept` = `[ ]`; AcceptLoop = 0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт capabilities; у каждого Requirement есть Scenario; implementation-leak маркеров в THEN нет; `comment_suffix` пуст. Сценарии есть в `## Slices` и покрыты accept/task path.
- **Layer 4 (Independent Challenge):** APPROVE; отчёт: `reports/design-challenge-2026-08-16-3.md`. Gaps 1–5 предыдущего CHALLENGE закрыты repair-from-verify. `reopen-blocked: independent_challenge_carrier`. `last_challenge_at` обновлён.
- **Layer 5 (Implementation Readiness):** PASS; отчёт: `reports/architecture-task-readiness-2026-08-16-3.md` вердикт ГОТОВО.

### Авто-исправлено (Layer 1)

не применялось

### Repair Loop

- attempt 1: implementation_invariant из `design-challenge-2026-08-16-2.md` (якорь поверхности, carve-out write-guard, Gate check, эталон std-06, S1.10). Запись: `debug.md` § Extend — 2026-08-16 (repair-from-verify). После repair — full re-verify → GO.

### Post-challenge classifier

- Drop reopen: GPT-5.6 как носитель независимого разбора — `reopen-blocked: independent_challenge_carrier`.
- implementation_invariant: закрыты repair'ом до финального прогона.
- GO-saturated: не применяется (Layer 4 APPROVE).

## Источники

- `reports/quality-control-2026-08-16-3.md`
- `reports/design-challenge-2026-08-16-3.md`
- `reports/architecture-task-readiness-2026-08-16-3.md`
- `reports/design-challenge-2026-08-16-2.md` — CHALLENGE, закрыт repair
- `openspec/adrs/ADR-0001-chat-facing-vs-agent-facing.md`, `openspec/adrs/ADR-0003-review-quality-disposition.md`
- Verified runtime: enum `Task.model` этой сессии (без `claude-fable-5-thinking-high`)
