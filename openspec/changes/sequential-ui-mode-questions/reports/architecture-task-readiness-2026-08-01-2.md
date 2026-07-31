---
report_type: task-readiness
generated_at: 2026-08-01
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
    - .cursor/skills/1c-forms/compile/SKILL.md
    - .cursor/skills/1c-forms/edit/SKILL.md
    - .cursor/rules/1c-xml-write-guard.mdc
    - .cursor/skills/1c-mxl/SKILL.md
    - .cursor/skills/openspec-explore/templates/handoff-block.md
    - .cursor/docs/kit-template-workflow.md
  capabilities:
    - sequential-gate-questions
    - split-form-layout-modes
related_reports:
  - reports/architecture-task-readiness-2026-08-01.md
  - reports/architecture-extend-coherence-2026-08-01-2.md
  - reports/quality-control-2026-08-01.md
  - reports/design-challenge-2026-08-01.md
confidence: high
open_questions_count: 0
verdict: ГОТОВО
superseded_by: null
---

# Task Readiness — sequential-ui-mode-questions

## KB references

- Discovery выполнен, совпадений нет — секция Existing Knowledge пуста; конфликтов KB нет.

## Вердикт

**ГОТОВО**

Метапроект kit после сужения (forms-only, per-form `form_mode`, макеты вне Mode Gate): mechanical apply по `.cursor/**` возможен as-is. BSL / Form.xml / Template.xml в задачах нет; ручная конфигурация для Primary этой ЗНИ не требуется. Блокирующих и suboptimal пробелов нет; замечания прошлого прогона (`architecture-task-readiness-2026-08-01.md`) закрыты артефактами после extend.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | OK | S1.1–S1.3, S2.1–S2.5: глагол + путь файла + наблюдаемое изменение + ссылка на Decision. Исполнитель markdown/rules знает ЧТО и ГДЕ. `**Режим apply:** mechanical`; writer BSL не нужен. Канонический синтаксис multi-form списка («путь → mode») задаётся в S2.1 (SSOT gate) и переиспользуется readers — без возврата к заказчику. |
| 2 | Реализуемость форм и метаданных | OK (N/A) | Explicit Non-Goal: нет Form.xml / Template.xml / прикладного BSL. Proposal `form_mode: n/a`. В tasks нет задач на метаданные/элементы формы. Primary этой ЗНИ — протоколы kit. |
| 3 | Разрешённость решений | OK | Decisions 1–9 и блок «Решения verify» закрыты: `form_mode` enum, per-form на design, END TURN, legacy→form_mode, макеты вне Mode Gate (manual default / permission on apply). Открытых развилок «или/либо» в implementable tasks нет; «Mode Gate / дизайн» в S1.2 — перечень запрещённых соседей, не выбор пути. F1/F2 вне Primary. |
| 4 | Порядок задач | OK | Граф S1 → S2. Нет ссылок на ещё не созданные объекты (только правки существующих `.cursor/**`). Ровно один `S<N>.accept` и один `<!-- slice-gate -->` на срез. Primary S1 достижим S1.1–S1.3; Primary S2 — S2.1–S2.5 после S1. |
| 5 | Data Contract Gate | OK (N/A) | Защитных проверок `Свойство()` / `ТипЗнч()` / стека guards в design/tasks нет (нет BSL). Контракты — текстовые инварианты протокола (один вопрос, per-form запись, STOP при empty/`n/a`). |
| 6 | Symptom vs root | OK (N/A) | Не bug-fix: эволюция UX гейтов kit, не устранение дефекта прикладного кода. |
| 7 | User Task Contract | OK | В `S1.1–S1.3`, `S2.1–S2.5` нет runtime-spike (ИБ, консоль, отладчик, эмуляция API). «Учебный прогон» только в `S<N>.accept` / metadata приёмки. F1/F2 — не `S<N>.<M>`. Pre-screen: none. |
| 8 | Manual config sufficiency | OK | Маркеров создания реквизитов/элементов/ролей в tasks нет (verify). «Вручную» встречается только как политика макета в accept / Behavior Contract — не чеклист Конфигуратора для этой ЗНИ. Таблица-доказательство в design не требуется. |

**Precedent Coherence (доп.):** OK — только ADDED capabilities; архивных MODIFIED/REMOVED для той же области нет; `## Blast Radius` не требуется. Closed decisions (макеты вне Mode Gate; per-form `form_mode` на design) согласованы proposal/design/specs/tasks.

## Покрытие и согласованность (сводка, без GAP)

- Spec `sequential-gate-questions` (3 scenarios) → S1 + S1.accept.
- Spec `split-form-layout-modes` (7 scenarios: form Mode on design, multi-form, no layout Mode, layout manual unless permission, legacy, kit n/a, empty form mode) → S2.1–S2.5 + S2.accept (Primary + optional).
- QC Slice Coherence: OK (10/10 scenarios) — принято как вход; противоречий tasks↔design↔specs после extend не видно.
- S2.5 включает operational readers (`1c-forms`, `compile`, `edit`, `1c-xml-write-guard`, handoff, kit-template-workflow) + политика `1c-mxl` без resurrect Mode Gate макета.

## Пробелы

*(нет GAP / SUBOPTIMAL)*

Неблокирующая гигиена (не меняет вердикт):

- Имя capability `split-form-layout-modes` историческое (после сужения макеты вне Mode Gate); содержание spec/tasks согласовано с Decision 9.
- S1.accept формулировка «следующий выбор про режим формы» читается вместе со Scenario «на этапе design» и S2.2 (Mode не в том же ходе, что Metadata, и не до design) — уточнение литерала опционально.

## Delta vs previous (`architecture-task-readiness-2026-08-01.md`)

| Замечание | Было (2026-08-01) | Сейчас (после forms-only / per-form extend) |
|-----------|-------------------|-----------------------------------------------|
| Наследник Template-`bsl-only` / dual `layout_mode` | SUBOPTIMAL | Закрыто Decision 9: макеты вне Mode Gate; manual default + permission on apply; поля `layout_mode` нет |
| S2.5 без compile/edit/xml-write-guard | SUBOPTIMAL | Закрыто — пути в S2.5 обязательны |
| Вердикт | ГОТОВО С ЗАМЕЧАНИЯМИ | **ГОТОВО** |

## Источники

- `proposal.md`, `design.md`, `tasks.md`
- `specs/sequential-gate-questions/spec.md`, `specs/split-form-layout-modes/spec.md`
- Pre-screen: Layers 1–3 без замечаний; User Task Contract — none; Executability — none; чеклист ручной конфигурации — маркеров создания реквизитов/элементов не найдено
- `reports/architecture-task-readiness-2026-08-01.md` (предыдущий прогон)
- `reports/architecture-extend-coherence-2026-08-01-2.md`
- `reports/quality-control-2026-08-01.md` (OK; 10/10 scenarios)
- Closed decisions: макеты вне Mode Gate; per-form `form_mode` на design
