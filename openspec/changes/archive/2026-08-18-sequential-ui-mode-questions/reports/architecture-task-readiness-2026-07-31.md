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
  - reports/architecture-new-selfreview-2026-07-31.md
  - reports/quality-control-2026-07-31.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Task Readiness — sequential-ui-mode-questions

## Вердикт

**ГОТОВО С ЗАМЕЧАНИЯМИ**

Артефакты достаточны для mechanical apply по `.cursor/**` силами агента и учебной приёмки на `S1.accept` / `S2.accept`. Блокирующих пробелов нет. Есть два неблокирующих замечания: условная формулировка S2.5 («при необходимости») при уже известной необходимости правки `kit-template-workflow.md`, и Behavior Contract resume (не переспрашивать валидные режимы) не вынесен в текст задач.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | OK | S1.1–S1.3 и S2.1–S2.4 указывают файл/якорь + наблюдаемое изменение + ссылку на Decision. Исполнитель markdown/rules знает ЧТО и ГДЕ. Writer BSL не нужен. |
| 2 | Реализуемость форм и метаданных | OK (N/A) | Explicit Non-Goal: нет Form.xml / Template.xml / BSL прикладной конфигурации. `artifact_mode` / modes в proposal этой ЗНИ: `n/a`. Ручной конфигурации 1С нет. |
| 3 | Разрешённость решений | SUBOPTIMAL | Имена полей, END TURN, Mode Gate на design, legacy fallback, `[form:…]` out-of-Primary — закрыты в design. Открытая мягкая вилка: S2.5 «и при необходимости kit-template-workflow.md» — proposal Impact и текущий текст файла уже требуют согласования терминов (`artifact_mode: n/a`). |
| 4 | Полнота покрытия | OK | Req «One selection…» → S1.1–S1.3 + S1.accept. Req «Separate form…» + 5 scenarios → S2.1–S2.5 + S2.accept (Primary + optional). Follow-up F1/F2 вне Primary — согласовано с design. |
| 5 | Согласованность | SUBOPTIMAL | Срезы S1/S2, поля, порядок гейтов, STOP при пустом режиме — согласованы tasks↔design↔spec. Расхождение: design Behavior Contract «Resume: валидные form_mode/layout_mode не переспрашивать» не отражён в S2.2/S2.3 (в spec отдельного scenario нет). |
| 6 | Связность кода и порядок задач | OK | Граф: S1 → S2. Ровно один `S<N>.accept` и один `<!-- slice-gate -->` на срез. Primary S1 достижим задачами S1 без S2; Primary S2 — задачами S2 после S1. Mechanical apply. |
| 7 | Архитектурная эстетика (Design Smells) | OK | Нет Shadow Storage / Parallel Workflow / orphan hooks. Два вертикальных среза по наблюдаемому UX. Опциональный `[form:…]` отложен — без лишней симметрии. |
| 8 | User Task Contract | OK | В `S1.1–S1.3`, `S2.1–S2.5` нет runtime-spike (ИБ, консоль, отладчик, эмуляция API). «Учебный прогон» только в `S<N>.accept`. Follow-up F1/F2 — не `S<N>.<M>`. |

**Precedent Coherence (доп. к Layer 5):** OK — только ADDED capabilities; архивных MODIFIED/REMOVED для той же области нет; `project.md` отсутствует (допустимо per design Assumptions).

## Simplicity Check

- **Viable alternatives:** (A) один `artifact_mode` + текст в design; (B) split fields + sequential questions; (C) всегда два вопроса.
- **Selected simplest viable:** B — машиночитаемый split без шума без-UI.
- **Why not simpler:** A не даёт независимого apply Form vs Template.
- **Complexity budget:** 2 среза; ~8 implementable tasks; правки только `.cursor/**`; 0 hooks в cf/cfe.

## Пробелы (SUBOPTIMAL)

### 1. S2.5 — условное «при необходимости» для kit-template-workflow

- **Артефакт:** `tasks.md` → S2.5
- **Что отсутствует:** однозначное ТЗ: файл уже содержит `artifact_mode: n/a` (`.cursor/docs/kit-template-workflow.md`); proposal Impact требует согласовать термины.
- **Рекомендация:** убрать «при необходимости», сделать обязательную правку терминов в этом файле (и остальных перечисленных).
- **Сниппет:**

```markdown
- [ ] S2.5 Обновить ссылки/таблицы режимов на `form_mode`/`layout_mode` (+ legacy `artifact_mode` где нужен fallback) в `.cursor/skills/1c-forms/SKILL.md`, `.cursor/skills/1c-mxl/SKILL.md`, `.cursor/skills/openspec-explore/templates/handoff-block.md`, `.cursor/docs/kit-template-workflow.md`
```

### 2. Resume Behavior Contract не в задачах

- **Артефакт:** `design.md` § Behavior Contract vs `tasks.md` S2.2 (и при желании S2.3)
- **Что отсутствует:** явная строка «при resume не переспрашивать валидные `form_mode`/`layout_mode`; lone `artifact_mode` маппить на оба».
- **Рекомендация:** добавить в S2.2 (протокол new) одну фразу; опционально зеркало в S2.3 для apply-контекста чтения proposal.
- **Сниппет (добавить к S2.2):**

```markdown
; resume: валидные `form_mode`/`layout_mode` не переспрашивать; lone legacy `artifact_mode` → оба канала одинаково
```

*Не блокирует apply:* исполнитель, читая design Decisions + Behavior Contract рядом с задачей, может закрыть это без возврата к пользователю. Замечание — чтобы не потерять при точечном чтении только `tasks.md`.

## Источники

- `proposal.md`, `design.md`, `tasks.md`
- `specs/sequential-gate-questions/spec.md`, `specs/split-form-layout-modes/spec.md`
- Pre-screen verify: Layers 1–3 без замечаний; User Task Contract mechanical — none; Executability — none
- `reports/quality-control-2026-07-31.md`, `reports/architecture-new-selfreview-2026-07-31.md`
- Точечная сверка: `kit-template-workflow.md` (legacy `artifact_mode`), `handoff-block.md` (legacy ярлык)
