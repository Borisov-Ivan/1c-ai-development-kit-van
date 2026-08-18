---
report_type: architecture
generated_at: 2026-08-08
agent: onec-code-architect
mode: task-decomposition
scope:
  change: hardcode-justification-gate
  slices: [S1, S2, S3]
  files:
    - .cursor/rules/bsl-antipatterns.mdc
    - .cursor/rules/existing-mechanism-priority.mdc
    - .cursor/rules/architect-gate.mdc
    - .cursor/agents/onec-code-architect.md
    - .cursor/agents/onec-code-writer.md
    - .cursor/agents/onec-code-reviewer.md
    - .cursor/docs/standard/reviewer-checks.md
  capabilities: [hardcode-justification-gate]
related_reports:
  - reports/exploration-2026-08-08-hardcode-justification-gate.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Task Decomposition — hardcode-justification-gate

## Task

Сформировать полный `tasks.md` по утверждённым срезам design.md для kit-эволюции (только `.cursor/rules`, `.cursor/agents`, `.cursor/docs`), без прикладного BSL.

## Complexity

Simple (документы kit; 7 целевых файлов; три независимых outcome по слоям каркаса).

## Chosen Approach

**Approach:** один файл `tasks.md` с тремя H1-срезами S1→S2→S3 строго по `design.md## Slices`; внутри — атомарные `S<N>.<M>` (1 файл / 1 аспект), финал среза — `S<N>.accept` с **Primary (обязательно):** и optional Scenario из spec.

**Rationale:**

- Каркас Попытки (AP → architect HALT → writer gate → reviewer Phase) уже задан design как три вертикальных outcome; дробить иначе = foundation-slice или фазы.
- Primary взяты из `design.md## Primary acceptance` (матрица: AP-055 / Architect HALT / Writer G21 как blocking; completeness и contradiction — optional в accept или покрыты текстом Primary S3 по design).
- User Task Contract: приёмка = чтение/grep канона (как archive `chat-surface-clarity`); нет user-spike на ИБ / runtime.

## Decomposition Map

| Срез | Outcome | Задачи | Spec coverage |
|------|---------|--------|---------------|
| S1 | Реестр AP-055 + запах Scope-as-literals + шаблон Hardcode Justification | S1.1–S1.4 + accept | Registry (Primary); Protocol literals (optional accept); Smell (optional accept; также в Primary design) |
| S2 | Identity Filter Gate у architect | S2.1–S2.3 + accept | Thin allow-list not Chosen (Primary) |
| S3 | G21 + Phase 2.6 completeness + MUST_FIX contradiction | S3.1–S3.5 + accept | Writer halt (Primary); Completeness / Contradiction (optional accept; включены в Primary design S3) |

**Зависимости срезов:** S1 → S2 → S3 (как design). Циклов нет.

**Режим apply:** не `mechanical` — содержательные тексты gates; slice-gate после каждого среза обязателен.

## Self-Achievable Primary

- S1 Primary достижим задачами S1.1–S1.4 (файлы antipatterns + existing-mechanism).
- S2 Primary достижим S2.1–S2.3 (architect agent + architect-gate); ссылки на AP-055/шаблон — после принятого S1.
- S3 Primary достижим S3.1–S3.5 (writer + reviewer + reviewer-checks); номер AP и имя фазы зафиксированы design.

## Out of scope (не в задачах срезов)

- Правка consumer-ЗНИ / прикладного allow-list.
- Обязательный grep post-apply в verify → `## Follow-up` в tasks.md.
- Перенумерация AP при коллизии — mitigation на apply (Risks), не отдельная задача.

## Deliverables

- `openspec/changes/hardcode-justification-gate/tasks.md` — полный чеклист к `/opsx:apply`.
- Этот отчёт — rationale декомпозиции.
