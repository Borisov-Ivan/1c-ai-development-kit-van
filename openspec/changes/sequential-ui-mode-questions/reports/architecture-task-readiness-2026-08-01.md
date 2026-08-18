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
    - .cursor/skills/1c-mxl/SKILL.md
    - .cursor/skills/openspec-explore/templates/handoff-block.md
    - .cursor/docs/kit-template-workflow.md
  capabilities:
    - sequential-gate-questions
    - split-form-layout-modes
related_reports:
  - reports/quality-control-2026-08-01.md
  - reports/architecture-task-readiness-2026-07-31-2.md
  - reports/architecture-extend-coherence-2026-08-01.md
  - reports/design-challenge-2026-08-01.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Task Readiness — sequential-ui-mode-questions

## Вердикт

**ГОТОВО С ЗАМЕЧАНИЯМИ**

Метапроект kit: mechanical apply по `.cursor/**` возможен as-is (BSL/Form.xml/Template.xml не в scope; `form_mode`/`layout_mode: n/a`). Блокирующих пробелов нет. После extend 2026-08-01 (асимметрия enum layout) артефакты proposal/design/specs/tasks согласованы; QC `OK`. Остаются неблокирующие замечания: не зафиксирован наследник бывшего Template-пути `bsl-only` (код заполнения без правки Template.xml) и неполный список operational readers в S2.5.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | OK | S1.1–S1.3, S2.1–S2.5: глагол + путь файла + наблюдаемое изменение + ссылка на Decision. Исполнитель markdown/rules знает ЧТО и ГДЕ. Writer BSL не требуется (`**Режим apply:** mechanical`). |
| 2 | Реализуемость форм и метаданных | OK (N/A) | Explicit Non-Goal + proposal `form_mode: n/a` / `layout_mode: n/a`. Маркеров ручной конфигурации в tasks нет. Чеклист verify: маркеров не найдено. |
| 3 | Разрешённость решений | SUBOPTIMAL | Decisions 1–9 и асимметрия `layout_mode` (без `bsl-only`) закрыты; открытых «или» в implementable tasks нет; F1/F2 вне Primary. Не дожат implementation_invariant из challenge: куда девается легитимный сценарий «только код заполнения макета, Template.xml вне правок» после запрета `layout_mode: bsl-only` — в design/Behavior Contract / S2.3 нет явной строки-наследника (см. пробел 1). |
| 4 | Полнота покрытия | SUBOPTIMAL | Req «One selection…» (3 scenarios) → S1; Req «Separate form…» (9 scenarios, в т.ч. Layout bsl-only / Legacy bsl-only ≠ layout / Empty / Pair) → S2 + accept; QC Scenario Coverage Pass (12/12). Неполный blast по operational consumers `artifact_mode`: S2.5 не включает `1c-xml-write-guard.mdc`, `1c-forms/compile|edit` (жёсткие гейты `artifact_mode: assisted`) — риск рассинхрона после записи пары без legacy (см. пробел 2). User-facing `faq-kit`/`quick-start` вне Impact — гигиена, не блокер Primary. |
| 5 | Согласованность | OK | tasks ↔ design ↔ specs после extend: split fields, Mode на design, Decision 7 (пара / legacy / bsl-only≠layout), Decision 9 (MXL/СКД без AskQuestion), empty/`n/a` STOP, resume/extend late UI в S2.2. Предыдущие SUBOPTIMAL (S2.5 «при необходимости», resume) закрыты. |
| 6 | Связность кода и порядок задач | OK | Граф S1 → S2. Ровно один `S<N>.accept` и один `<!-- slice-gate -->` на срез. Primary S1 достижим S1.1–S1.3; Primary S2 — S2.1–S2.5 после S1. Петли/несуществующих объектов нет (только правки существующих `.cursor/**`). |
| 7 | Архитектурная эстетика (Design Smells) | OK | Нет Shadow Storage / Parallel Workflow / orphan hooks. Два вертикальных среза по UX протокола. `[form:…]` отложен (F2). Over-engineering нет. |
| 8 | User Task Contract | OK | В `S1.1–S1.3`, `S2.1–S2.5` нет runtime-spike (ИБ, консоль, отладчик, эмуляция API). «Учебный прогон» только в `S<N>.accept` / metadata приёмки. F1/F2 — не `S<N>.<M>`. Pre-screen evidence: none. Structural user-spike отсутствует. |

**Precedent Coherence (доп. к критерию 8 / Layer 5):** OK — только ADDED capabilities; архивных MODIFIED/REMOVED для той же области нет; `## Blast Radius` не требуется. `project.md` отсутствует (допустимо per design Assumptions).

## Simplicity Check

- **Viable alternatives:** (A) один `artifact_mode` + текст в design; (B) `form_mode` + `layout_mode` + sequential questions; (C) всегда два вопроса без UI.
- **Selected simplest viable:** B — машиночитаемый split + асимметрия layout без нового AskQuestion MXL/СКД.
- **Why not simpler:** A не даёт независимого apply Form vs Template при смешанных режимах; C — шум без UI.
- **Complexity budget:** 2 среза; 8 implementable tasks + 2 accept; правки только `.cursor/**`; 0 hooks в cf/cfe.

## Пробелы (SUBOPTIMAL)

### 1. Наследник Template-пути `bsl-only` (код заполнения без Template.xml)

- **Артефакт:** `design.md` (Decision 9 / Behavior Contract), отразить в `tasks.md` S2.3
- **Что отсутствует:** явная строка: после запрета `layout_mode: bsl-only` сценарий «только BSL заполнения макета, Template.xml не трогаем» = Template **не** в scope Mode Gate → `layout_mode: n/a` (и apply не ждёт compile/manual XML); при Template in scope допустимы только `manual`/`assisted`; ответ «программно» на вопрос макета → STOP/переспрос (уже есть), без silent coerce.
- **Рекомендация:** одна фраза в Behavior Contract + уточнение S2.3 («убрать/не оставлять ветку Template←`bsl-only` в apply; fill-only без XML = layout out of scope / `n/a`»).
- **Сниппет (design.md, Behavior Contract, после буллета про Template never bsl-only):**

```markdown
- Наследник бывшего Template-`bsl-only` («код заполнения без правки Template.xml»): Template **не** входит в scope Mode Gate → `layout_mode: n/a`; apply не направляет макет в compile/assisted/manual-XML. При Template in scope — только `manual`/`assisted`; ветки apply «Template ← bsl-only» не оставлять.
```

### 2. Operational readers вне списка S2.5

- **Артефакт:** `tasks.md` → S2.5 (и при желании design Impact / Slices files)
- **Что отсутствует:** обязательная синхронизация терминов в файлах, которые **жёстко** гейтят по `artifact_mode: assisted`: `.cursor/rules/1c-xml-write-guard.mdc`, `.cursor/skills/1c-forms/compile/SKILL.md`, `.cursor/skills/1c-forms/edit/SKILL.md`.
- **Рекомендация:** расширить S2.5 (или добавить S2.6) этими путями; читать `form_mode`/`layout_mode` + legacy fallback по Decision 7.
- **Сниппет (замена тела S2.5):**

```markdown
- [ ] S2.5 Обновить ссылки/таблицы режимов на `form_mode`/`layout_mode` (+ legacy `artifact_mode` где нужен fallback по Decision 7) в `.cursor/skills/1c-forms/SKILL.md`, `.cursor/skills/1c-forms/compile/SKILL.md`, `.cursor/skills/1c-forms/edit/SKILL.md`, `.cursor/skills/1c-mxl/SKILL.md`, `.cursor/rules/1c-xml-write-guard.mdc`, `.cursor/skills/openspec-explore/templates/handoff-block.md`, `.cursor/docs/kit-template-workflow.md`
```

### Неблокирующая гигиена (не меняет вердикт)

- QC SUGGESTION: optional bullets S2.accept с paraphrase имён Scenario («Form-only / Layout-only», «Kit evolution») — покрытие через tasks есть; выравнивание литералов опционально.
- S1.accept Primary: уточнить «вопрос режима — отдельным сообщением **на этапе design** (не раньше scaffold)», чтобы не читалось как «Mode сразу следующим сообщением после Metadata» (согласовано с Decision 3; S2.2 уже переносит Mode на design).

## Delta vs previous (`architecture-task-readiness-2026-07-31-2.md`)

| Замечание | Было (2026-07-31-2) | Сейчас (после extend 2026-08-01) |
|-----------|---------------------|----------------------------------|
| Асимметрия layout enum / Decision 9 | не в scope | В proposal/design/specs/tasks; S2.1–S2.4 |
| Scenarios Layout bsl-only / Legacy bsl-only ≠ layout | нет | в spec + S2.accept / tasks |
| Вердикт | ГОТОВО | **ГОТОВО С ЗАМЕЧАНИЯМИ** (наследник Template-bsl-only + S2.5 readers) |
| S2.5 / resume gaps | закрыты | остаются закрытыми |

## Источники

- `proposal.md`, `design.md`, `tasks.md`
- `specs/sequential-gate-questions/spec.md`, `specs/split-form-layout-modes/spec.md`
- Pre-screen: Layers 1–3 без замечаний; User Task Contract — none; Executability — none; чеклист ручной конфигурации — маркеров не найдено
- `reports/quality-control-2026-08-01.md` (OK; SUGGESTION paraphrase — гигиена)
- `reports/architecture-extend-coherence-2026-08-01.md` (drift закрыт синхронизацией артефактов)
- `reports/design-challenge-2026-08-01.md` (CHALLENGE → gaps 1–2 выше как SUBOPTIMAL)
- `reports/architecture-task-readiness-2026-07-31-2.md` (предыдущий ГОТОВО)
- Точечная сверка: `.cursor/rules/forms-mxl-mode-gate.mdc`, `1c-xml-write-guard.mdc`, `1c-forms/compile|edit` всё ещё на `artifact_mode` — ожидаемо до apply; должны войти в задачи readers
