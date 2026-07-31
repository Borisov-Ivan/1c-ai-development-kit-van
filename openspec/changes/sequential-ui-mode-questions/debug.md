## Slice Gate Decisions

### Slice S1 — Один вопрос за ход (2026-08-01)
Срез: S1 — Один вопрос за ход
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: нет (S1.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S1-2026-08-01.md

## Verify decision ledger

```yaml
closed_decisions:
  - id: acceptance_loop_s2_path
    summary: "Не замораживать dual-channel постановку S2 — сузить ЗНИ до форм (Mode Gate только form_mode per-form); макеты вне Mode Gate"
    closed_at: "2026-08-01"
    source: verify-user-answer
  - id: forms_only_no_layout_mode_gate
    summary: "Макеты вне Mode Gate new; default manual; programmatic только с явного разрешения на apply; поле layout_mode как выбор не вводим"
    closed_at: "2026-08-01"
    source: verify-user-answer
  - id: per_form_mode_on_design
    summary: "Вопрос режима формы на design по каждой форме в scope (не один режим на всю ЗНИ); END TURN между вопросами"
    closed_at: "2026-08-01"
    source: verify-user-answer
decision_round: 1
open_decision_id: null
verify_depth: full
assumptions_accepted: []
```

## Extend — 2026-07-31

- Источник: repair-from-verify (internal, design-challenge-2026-07-31 + architecture-task-readiness-2026-07-31)
- Что изменено:
  - `design.md` — Decisions 3 уточнён (Mode до Design Gate); Decisions 6–8 (SSOT формулировок, запись proposal без `artifact_mode`, extend/поздний UI-scope); Behavior Contract (пустой режим, стык с Design Gate); матрица приёмки + сценарий empty mode
  - `specs/split-form-layout-modes/spec.md` — Scenario «Empty mode blocks apply for in-scope artifact»
  - `tasks.md` — S2.1–S2.5 уточнены (формулировки вопросов, resume, kit-template-workflow обязательно, empty-mode STOP); optional bullet в S2.accept
- Disposition: accepted (implementation_invariant)
- Architect Gate: не требовался (repair по отчёту challenge/task-readiness без смены оси B)
- Следующий шаг: повторный полный verify (repair_attempt=1)

## Extend — 2026-07-31 (repair 2)

- Источник: repair-from-verify (design-challenge-2026-07-31-2)
- Что изменено:
  - `specs/split-form-layout-modes/spec.md` — Empty включает `n/a`+UI-in-scope; Scenario «Pair fields override legacy artifact_mode»; Legacy WHEN уточнён (оба новых поля отсутствуют)
  - `design.md` — Decision 7 приоритет пары; Behavior Contract пустой/`n/a`; матрица/Slices
  - `tasks.md` — S2.3/S2.4 приоритет пары + `n/a`; optional bullets S2.accept
- Disposition: accepted (implementation_invariant)
- Architect Gate: не требовался
- Следующий шаг: re-verify (repair_attempt=2, max)

## Extend Coherence Audit — 2026-08-01

- Триггер: semantic (drift-warning из брифа)
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-08-01.md`
- Решение пользователя: accepted recommendations (вариант 1; без AskQuestion MXL/СКД; legacy bsl-only + Template → Mode-вопрос/STOP по макету, не silent manual)

## Extend — 2026-08-01

- Источник: user-extend после Scope Gate verify (вариант 1 брифа)
- Что изменено:
  - `proposal.md` — асимметричные enum form/layout
  - `design.md` — Non-Goals, Decisions 6–7 уточнены, Decision 9 (MXL/СКД), Behavior Contract, матрица, Risks
  - `specs/split-form-layout-modes/spec.md` — Requirement + scenarios Layout rejects bsl-only / Legacy bsl-only ≠ layout
  - `tasks.md` — S2.1, S2.3, S2.4, optional bullets S2.accept
- Disposition: accepted
- Architect Gate: `reports/architecture-extend-coherence-2026-08-01.md`
- Следующий шаг: `/opsx:verify sequential-ui-mode-questions`

## Loop Detection — 2026-08-01

- Триггер: verify Layer 2.5
- Срез: S2
- AcceptLoop / PatchRounds: 0 / 3 (порог acceptance_loop_max=3)
- Отчёт редизайна: `reports/architecture-loop-redesign-2026-08-01.md`
- Рекомендация архитектора: minimal (заморозка; AcceptLoop=0, state space после extend 2026-08-01 согласован с QC)
- Уточнение оркестратора verify: upgrade minimal→consolidation рекомендован в чат — Layer 4 CHALLENGE нашёл новый край того же dual-channel state space (наследник Template-`bsl-only` / fill-only без XML)
- Решение пользователя: accepted path A → сужение до forms-only / per-form (dual-channel layout Mode Gate снят; см. Extend — 2026-08-01 (forms-only))

## Extend Coherence Audit — 2026-08-01 (2)

- Триггер: semantic (drift-warning из брифа сужения forms-only / per-form)
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-08-01-2.md`
- Решение пользователя: accepted recommendations (полная перепись артефактов; `layout_mode` как выбор не вводим — вариант a из OQ1 аудита)

## Extend — 2026-08-01 (forms-only)

- Источник: user-extend `--from-verify` после decision (A) + брифы сужения (макеты вне ЗНИ; per-form Mode на design)
- Что изменено:
  - `proposal.md` — Why/What Changes/Capabilities/Impact под forms-only; секция `## Forms mode`; без выбора `layout_mode`
  - `design.md` — Goals/Non-Goals, Decisions 1–9, Behavior Contract, Slices/матрица, Risks, § Решения verify
  - `specs/sequential-gate-questions/spec.md` — формулировки про режим формы
  - `specs/split-form-layout-modes/spec.md` — Requirement per-form; сценарии multi-form / no layout Mode / layout policy on apply; без dual-channel Primary
  - `tasks.md` — S1/S2 переписаны под form-delivery per-form; S2.5 readers расширены
- Disposition: accepted
- Architect Gate: `reports/architecture-extend-coherence-2026-08-01-2.md`
- Следующий шаг: `/opsx:verify sequential-ui-mode-questions`

## Extend — 2026-08-01 (repair-from-verify)

- Источник: repair-from-verify (internal) — `reports/design-challenge-2026-08-01-2.md` gaps 1–6 (implementation_invariant)
- Что изменено:
  - `design.md` — Decision 2 (канон `## Forms mode` / map `forms:` / ключ метаданных + пример); Decision 3/3a (timing + enumeration scope); Decision 7 (lone legacy → весь form-scope); Decision 9 (норма разрешения apply + debug § Apply permissions); Behavior Contract; матрица Scenario layout permission
  - `specs/split-form-layout-modes/spec.md` — Requirement уточнён; Legacy WHEN/THEN для N>1; Scenario «Layout non-manual requires recorded apply permission»
  - `tasks.md` — S1 Primary/accept (Mode на design); S2.1–S2.5 и S2.accept под канон записи / permission / новый Scenario
- Disposition: accepted (implementation_invariant)
- Architect Gate: не требовался (repair по gaps challenge без смены closed axis)
- Следующий шаг: re-verify (repair_attempt=1)
