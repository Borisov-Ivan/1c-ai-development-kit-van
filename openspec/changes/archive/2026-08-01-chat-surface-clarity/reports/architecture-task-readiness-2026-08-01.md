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
  - reports/quality-control-2026-08-01.md
  - reports/architecture-new-2026-08-01.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Task Readiness — chat-surface-clarity

## Вердикт

**ГОТОВО С ЗАМЕЧАНИЯМИ**

Kit meta-change: правки chat-facing markdown/mdc выполнимы по артефактам. Срезы S1–S2 исполняются as-is без возврата к заказчику. Замечание по S3.2 (opaque «и смежные») — **не CRITICAL** для старта apply: целевые зоны восстанавливаются из `design.md` (S3: extend/explore ask paths) + точечный grep AskQuestion; остатки закрывает S3.4. Рекомендуется уточнить пути в S3.2 до/в начале S3, но это не блокирует реализацию S1→S2.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость текстовых задач kit | **GAP** (не CRITICAL) | S1.1–S1.5, S2.1–S2.5, S3.1, S3.3–S3.4: путь/якорь + ожидаемый эффект достаточны. **S3.2** — без явных путей файлов; «и смежные» несамодостаточно в заголовке задачи (см. отдельно). Остальные задачи редактирования текстов оркестратором исполнимы. |
| 2 | Реализуемость форм и метаданных | **OK** | `form_mode: n/a`. В tasks нет Form.xml / Template.xml / метаданных 1С; единственное «вручную» — продуктовый ярлык канона Mode Gate в S1.1 (не ручная конфигурация). |
| 3 | Разрешённость решений | **OK** | Option A выбран; Mode Gate 1/2/3, thin-chat vs файл, бан KB в брифе, бан slug агентов — зафиксированы в design § Decisions. «decision-block **или** brief-card B2» в S3.2 — не развилка реализации, а иерархия SSOT из Goals/Non-Goals (A/B vs 1/2/3 не сливать). Open Questions: P2 meta-docs опциональны, не блокер. |
| 4 | Полнота покрытия | **OK** | Все `#### Scenario` из spec привязаны к задачам/accept: Mode Gate + Good examples + preamble → S1; Slice acceptance / Review fix / Status·handoff → S2; Entry brief KB / Agent names → S3.1+accept; FAQ → S1.3. Gaps AskQuestion (explore/extend/verify new-req) — S3.2; кумулятивная grep-приёмка — S3.4. |
| 5 | Согласованность tasks↔design↔spec | **OK** | Срезы, файлы-ядра и Primary acceptance совпадают с design-таблицей. Spec ADDED-only; Impact proposal ⊆ задачи. Мелочь: тег Scenario у S2.1 («Status and handoff / AskQuestion hygiene») шире имени scenario — не ломает покрытие. |
| 6 | Связность и порядок | **OK** | Зависимости S1→S2→S3 явны; ровно один `S<N>.accept` на срез; `<!-- slice-gate: acceptance -->` на каждом срезе (маркеры thin — замечание QC, не ломает порядок). S3.4 может трогать зоны S1/S2 как кумулятивную приёмку change — риск rework уже в QC WARNING; для task-readiness порядок срезов валиден. |
| 7 | Архитектурная эстетика | **OK** | Четыре волны по существующим SSOT; Option C (параллельный гайд) отклонён. Нет лишнего третьего формата «спроси»; agent-facing слои verify/guards вне scope. Over-engineering не обнаружен. |
| 8 | User Task Contract / Precedent | **OK** | В `S<N>.M` нет user runtime-spike / ручной конфигурации метаданных — только правки текстов агентом. `S<N>.accept` — приёмка среза заказчиком (штатно). Precedent: ADDED-only capability, архивов нет, KB index отсутствует — конфликтов/Blast Radius не требуется. |

## S3.2 — CRITICAL для исполнимости as-is?

**Нет. GAP по критерию 1 (WARNING-класс), не CRITICAL.**

| Фактор | Оценка |
|--------|--------|
| Что не хватает в tasks | Явные пути: `openspec-extend-change/SKILL.md`, `openspec-explore/SKILL.md`, `openspec-verify-change/SKILL.md` (AskQuestion new-req / drift); «и смежные» без границ |
| Восстановление из design | Да: S3 «extend/explore ask paths»; Behavior Contract привязывает к decision-block / brief-card B2 |
| Обнаруживаемость | AskQuestion в verify (new-req), extend (drift / scope-violation), explore (ограниченные случаи) находятся grep’ом без уточнения у пользователя |
| Страховка | S3.4 — финальный grep chat-facing + правка остатков |
| Блокер apply S1/S2 | Нет |
| Нужен ли возврат заказчику | Нет; достаточно правки формулировки S3.2 (или следования design) исполнителем |

Итог: as-is ЗНИ **можно** вести через apply без паузы на уточнение scope у пользователя; желательно закрыть opaque title S3.2 до входа в S3 (как в remediation QC), чтобы срез не зависел от «памяти» design.

## Замечания (не блокируют вердикт «С ЗАМЕЧАНИЯМИ»)

1. **S3.2 task-opaque-title** — перечислить пути SKILL (extend / explore / verify) и критерий «русский текст вариантов по decision-block или brief-card B2 в зависимости от типа развилки».
2. **S3.4 rework-risk** (из QC) — зафиксировать в design/metadata, что финальный grep — кумулятивная приёмка change (правки остатков в файлах S1/S2 допустимы без повторного gate), либо сузить зону S3.4.
3. **Thin slice-gate markers** — косметика QC; на исполнимость задач не влияет.

## Карта scenario → задачи (coverage evidence)

| Scenario (spec) | Задачи |
|-----------------|--------|
| Mode Gate question is product language | S1.1, S1.accept |
| Good examples do not teach jargon | S1.2, S1.accept |
| Mode question has no process preamble | S1.5, S1.accept (optional bullet) |
| Slice acceptance prompt without gate names | S2.2, S2.accept |
| Review fix prompt without agent slugs | S2.4, S2.accept |
| Status and handoff separate chat from file | S2.2, S2.3, S2.5, S2.accept |
| Entry brief excludes KB list | S3.1, S3.accept |
| Agent names banned uniformly | S3.1, S3.accept |
| FAQ matches form-only Mode Gate | S1.3, S1.accept |

## Источники

- `proposal.md` — Why / What Changes / form_mode n/a / Impact
- `design.md` — Decisions, Slices S1–S3, Behavior Contract, Open Questions
- `tasks.md` — S1.1–S3.accept
- `specs/chat-surface-clarity/spec.md` — ADDED requirements + scenarios
- `reports/quality-control-2026-08-01.md` — WARNING S3.2 / S3.4 (контекст Layers 1–3)
