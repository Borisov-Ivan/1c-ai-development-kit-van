---
report_type: task-readiness
generated_at: 2026-07-31
agent: onec-code-architect
mode: task-readiness
scope:
  change: sequential-ui-mode-questions
  slices: [S1, S2]
  files:
    - .cursor/skills/openspec-new-change/SKILL.md
    - .cursor/docs/templates/brief-card.md
    - .cursor/rules/forms-mxl-mode-gate.mdc
    - .cursor/skills/openspec-apply-change/SKILL.md
    - .cursor/skills/openspec-verify-change/SKILL.md
    - .cursor/skills/1c-forms/SKILL.md
    - .cursor/skills/1c-mxl/SKILL.md
    - .cursor/skills/openspec-explore/templates/handoff-block.md
    - .cursor/docs/kit-template-workflow.md
  capabilities:
    - sequential-gate-questions
    - split-form-layout-modes
related_reports:
  - reports/architecture-task-readiness-2026-07-31.md
  - reports/architecture-new-selfreview-2026-07-31.md
  - reports/quality-control-2026-07-31-2.md
  - reports/design-challenge-2026-07-31.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Task Readiness — sequential-ui-mode-questions (re-run)

## Вердикт

**ГОТОВО**

Артефакты достаточны для mechanical apply as-is: только правки `.cursor/**` (skills, rules, templates, docs). Writer BSL / Form.xml / Template.xml не нужны. Блокирующих и suboptimal пробелов после repair нет.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | OK | S1.1–S1.3 и S2.1–S2.5: файл/якорь + наблюдаемое изменение + ссылка на Decision. Исполнитель markdown/rules знает ЧТО и ГДЕ. BSL-writer не требуется. |
| 2 | Реализуемость форм и метаданных | OK (N/A) | Explicit Non-Goal: нет Form.xml / Template.xml / прикладного BSL. Modes этой ЗНИ: `n/a`. Маркеров ручной конфигурации нет. |
| 3 | Разрешённость решений | OK | Decisions 1–8 закрыты (имена полей, запись proposal без `artifact_mode`, SSOT формулировок, последовательность new, END TURN, resume, extend/поздний UI-scope, empty-mode STOP). S2.5 без условного «при необходимости» — обязательный список файлов. Открытых «или» в implementable tasks нет; F2 вне Primary. |
| 4 | Полнота покрытия | OK | Req «One selection…» (3 scenarios) → S1.1–S1.3 + S1.accept. Req «Separate form…» (6 scenarios, в т.ч. Empty mode) → S2.1–S2.5 + S2.accept (Primary + optional). F1/F2 вне Primary — согласовано с design. |
| 5 | Согласованность | OK | tasks ↔ design ↔ specs согласованы: split fields, Mode на design, legacy fallback, empty-mode STOP, resume/не переспрашивать, extend late UI-scope в S2.2. Предыдущий пробел (Behavior Contract resume только в design) закрыт текстом S2.2. |
| 6 | Связность кода и порядок задач | OK | Граф S1 → S2. Ровно один `S<N>.accept` и один `<!-- slice-gate -->` на срез. Primary S1 достижим без S2; Primary S2 — после S1 задачами S2. Mechanical apply. |
| 7 | Архитектурная эстетика (Design Smells) | OK | Нет Shadow Storage / Parallel Workflow / orphan hooks. Два вертикальных среза по UX протокола. `[form:…]` отложен (F2) — без лишней симметрии. |
| 8 | User Task Contract | OK | В `S1.1–S1.3`, `S2.1–S2.5` нет runtime-spike (ИБ, консоль, отладчик, эмуляция API). «Учебный прогон» только в `S<N>.accept`. F1/F2 — не `S<N>.<M>`. Pre-screen: none. |

**Precedent Coherence (доп. к Layer 5):** OK — только ADDED capabilities; архивных MODIFIED/REMOVED для той же области нет; Blast Radius не требуется. `project.md` отсутствует (допустимо per design Assumptions).

## Simplicity Check

- **Viable alternatives:** (A) один `artifact_mode` + текст в design; (B) `form_mode` + `layout_mode` + sequential questions; (C) всегда два вопроса без UI.
- **Selected simplest viable:** B — машиночитаемый split без шума без-UI.
- **Why not simpler:** A не даёт независимого apply Form vs Template при смешанных режимах.
- **Complexity budget:** 2 среза; 8 implementable tasks + 2 accept; правки только `.cursor/**`; 0 hooks в cf/cfe.

## Пробелы

*(нет GAP / SUBOPTIMAL)*

Неблокирующая гигиена из QC-2 (не влияет на as-is apply): optional bullets S2.accept и `**Связь со spec:**` используют paraphrases имён Scenario вместо literal `#### Scenario:` — покрытие есть; выравнивание названий опционально.

## Delta vs previous (`architecture-task-readiness-2026-07-31.md`)

| Замечание | Было | Сейчас |
|-----------|------|--------|
| S2.5 «при необходимости» для kit-template-workflow | SUBOPTIMAL (крит. 3) | Закрыто — обязательный список файлов |
| Resume Behavior Contract не в задачах | SUBOPTIMAL (крит. 5) | Закрыто — явная фраза в S2.2 (+ extend late UI-scope) |
| Empty mode scenario | не в scope того прогона | В spec + S2.1/S2.3/S2.4 + S2.accept optional |
| Decisions 6–8 | отсутствовали / тоньше | Зафиксированы; отражены в S2.1–S2.5 |
| Вердикт | ГОТОВО С ЗАМЕЧАНИЯМИ | **ГОТОВО** |

## Источники

- `proposal.md`, `design.md`, `tasks.md`
- `specs/sequential-gate-questions/spec.md`, `specs/split-form-layout-modes/spec.md`
- Pre-screen: Layers 1–3 без замечаний; User Task Contract — none; Executability — none; чеклист ручной конфигурации — маркеров не найдено
- `reports/quality-control-2026-07-31-2.md` (OK)
- `reports/architecture-task-readiness-2026-07-31.md` (предыдущий прогон)
- Точечная сверка: `kit-template-workflow.md` всё ещё с legacy `artifact_mode` — входит в обязательный S2.5
