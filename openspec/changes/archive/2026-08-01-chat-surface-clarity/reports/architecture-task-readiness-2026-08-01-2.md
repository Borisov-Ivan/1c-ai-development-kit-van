---
report_type: task-readiness
generated_at: 2026-08-01
agent: onec-code-architect
mode: task-readiness
scope:
  change: chat-surface-clarity
  slices: [S1, S2, S3]
  files:
    - openspec/changes/chat-surface-clarity/proposal.md
    - openspec/changes/chat-surface-clarity/design.md
    - openspec/changes/chat-surface-clarity/tasks.md
    - openspec/changes/chat-surface-clarity/specs/chat-surface-clarity/spec.md
  modules: []
  capabilities: [chat-surface-clarity]
related_reports:
  - reports/quality-control-2026-08-01-2.md
  - reports/architecture-task-readiness-2026-08-01.md
  - reports/architecture-new-2026-08-01.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Task Readiness — chat-surface-clarity (после Repair Loop 1)

## Вердикт

**ГОТОВО**

Kit meta-change: chat-facing правки `.cursor/**` исполнимы as-is по `tasks.md` + `design.md` § «Список grep-приёмки». GAP S3.2 (opaque title) закрыт явными путями SKILL. S3.4 содержит closure-правило без повторного slice-gate S1/S2. Grep-список в design достаточен для финальной приёмки. Возврат к заказчику не требуется.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость текстовых задач kit | **OK** | Все `S<N>.M` имеют путь/якорь + ожидаемый эффект. **S3.2** перечисляет `.cursor/skills/openspec-extend-change/SKILL.md`, `openspec-explore/SKILL.md`, `openspec-verify-change/SKILL.md` + критерий decision-block (A/B) / brief-card B2 (1/2/3). Opaque «и смежные» убран. |
| 2 | Реализуемость форм и метаданных | **OK** | `form_mode: n/a`. Нет Form.xml / Template.xml / метаданных 1С. «Вручную» в S1.1 — ярлык канона Mode Gate, не ручная конфигурация. |
| 3 | Разрешённость решений | **OK** | Option A выбран; Decisions 1–5 зафиксированы. «decision-block или brief-card B2» — иерархия SSOT (Non-Goals: не сливать A/B и 1/2/3), не развилка реализации. Open Questions: P2 meta-docs опциональны. |
| 4 | Полнота покрытия | **OK** | 10/10 Scenario из spec привязаны (согласовано с QC re-verify): S1 — Mode Gate / Good examples / FAQ / preamble; S2 — Slice acceptance / Apply pause / Review fix / Status·handoff; S3 — Entry brief KB / Agent names + финальный grep. |
| 5 | Согласованность tasks↔design↔spec | **OK** | Срезы, ядро файлов и Primary совпадают с design § Slices / матрицей приёмки. Spec ADDED-only; Impact proposal ⊆ задачи. S3.4 ссылается на design § «Список grep-приёмки»; Behavior Contract фиксирует кумулятивную приёмку. |
| 6 | Связность и порядок | **OK** | S1→S2→S3; один `S<N>.accept` + `<!-- slice-gate -->` на срез. S3.4: точечный closure в файлах S1/S2 без переоткрытия оси и без повторного gate — rework-risk закрыт. |
| 7 | Архитектурная эстетика | **OK** | Волны по существующим SSOT; Option B/C отклонены. Agent-facing Layer/guards вне scope. Over-engineering нет. |
| 8 | User Task Contract / Precedent Coherence | **OK** | В `S<N>.M` нет user runtime-spike / ручной конфигурации метаданных — только правки текстов. Precedent: ADDED-only capability, архивов той же области нет, KB index отсутствует — Blast Radius / precedent-coherence не требуются. |

## Закрытие GAP Repair Loop 1

| Prior gap / alert | Status | Evidence |
|-------------------|--------|----------|
| S3.2 opaque title («и смежные») | **Closed** | `tasks.md` S3.2: три явных пути SKILL + формат A/B или 1/2/3 |
| S3.4 rework-risk vs файлы S1/S2 | **Closed** | `tasks.md` S3.4 closure-правило; `design.md` Behavior Contract: кумулятивная приёмка change |
| Grep-список недостаточен для apply | **Closed** | `design.md` § «Список grep-приёмки»: токены, зоны (S3.4), исключения agent-only |
| Thin slice-gate markers (QC SUGGESTION) | **Closed** (QC) | Markers содержат одно предложение критерия из Primary |

**S3.2 as-is:** достаточно для apply без восстановления путей из «памяти» design.

## Simplicity Check

- **Viable alternatives:** (A) четыре волны + grep — выбран; (B) только Mode Gate; (C) параллельный гайд стиля.
- **Selected simplest viable:** A — минимальный набор SSOT без четвёртого документа.
- **Why not simpler:** B не закрывает apply/status/review (proposal Why).
- **Complexity budget:** ~15–20 chat-facing файлов; hooks/intercepts 0; новый BSL/метаданные 0.

## Карта scenario → задачи

| Scenario (spec) | Задачи |
|-----------------|--------|
| Mode Gate question is product language | S1.1, S1.accept |
| Good examples do not teach jargon | S1.2, S1.accept |
| Mode question has no process preamble | S1.5, S1.accept (optional) |
| Slice acceptance prompt without gate names | S2.2, S2.accept |
| Apply pause label is product language | S2.2, S2.accept |
| Review fix prompt without agent slugs | S2.4, S2.accept |
| Status and handoff separate chat from file | S2.2, S2.3, S2.5, S2.accept |
| Entry brief excludes KB list | S3.1, S3.accept |
| Agent names banned uniformly | S3.1, S3.accept |
| FAQ matches form-only Mode Gate | S1.3, S1.accept |

## Замечания (не блокируют)

- Позиция `<!-- slice-gate -->` до списка задач (не после `S<N>.accept`) — стилистика QC Notes; на исполнимость не влияет.
- Исполнимость grep на текущем диффе ИБ/runtime — out of scope (по промпту).

## Источники

- `proposal.md` — Why / What Changes / form_mode n/a
- `design.md` (mtime ~2026-08-01T14:51+09) — Decisions, Behavior Contract, Список grep-приёмки, Slices
- `tasks.md` (mtime ~2026-08-01T14:51+09) — S1.1–S3.accept после Repair Loop 1
- `specs/chat-surface-clarity/spec.md` — 10 ADDED scenarios
- `reports/quality-control-2026-08-01-2.md` — Verdict OK; prior WARNING closed
- `reports/architecture-task-readiness-2026-08-01.md` — baseline до repair (ГОТОВО С ЗАМЕЧАНИЯМИ)
