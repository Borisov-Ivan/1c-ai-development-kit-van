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
  - reports/architecture-task-readiness-2026-08-01-2.md
  - reports/design-challenge-2026-08-01-2.md
  - reports/architecture-extend-coherence-2026-08-01-2.md
  - reports/quality-control-2026-08-01-2.md
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

После repair-from-verify (канон `forms:` map + ключ метаданных, enumeration Decision 3a, legacy×N, норма permission-on-apply) mechanical apply по `.cursor/**` возможен as-is. BSL / Form.xml / Template.xml в задачах нет; маркеров ручной конфигурации реквизитов нет. Gaps challenge `design-challenge-2026-08-01-2` (1–6, implementation_invariant) закрыты в design/specs/tasks. Блокирующих и suboptimal пробелов нет.

## Simplicity Check

- **Viable alternatives:** Only one viable option under closed axis (forms-only, per-form on design, макеты вне Mode Gate): Option D уже зафиксирован; reopen cascade / dual-channel layout — вне scope readiness.
- **Selected simplest viable design:** Правки протоколов kit (skills/rules/docs) без прикладного кода и без новых полей proposal сверх `form_mode` / map `forms:`.
- **Why not simpler:** Без канона map / enumeration / legacy×N / permission readers apply/verify разъедутся — repair как раз снял эту неоднозначность, не добавив новых объектов метаданных.
- **Complexity budget:** Files touched ≈12 `.cursor/**`; hooks/intercepts = 0; New BSL = 0; conditional feature flags = 0 (текстовые инварианты протокола).

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | OK | S1.1–S1.3, S2.1–S2.5: глагол + путь файла + наблюдаемое изменение + ссылка на Decision. Канон записи (`## Forms mode`, скаляр/`forms:` с ключом метаданных), enumeration (3a), legacy→весь form-scope, permission + `debug.md` § Apply permissions — в тексте задач/design, без возврата к заказчику. `**Режим apply:** mechanical`; writer BSL не нужен. |
| 2 | Реализуемость форм и метаданных | OK (N/A) | Explicit Non-Goal: нет Form.xml / Template.xml / прикладного BSL. Proposal `form_mode: n/a`. В tasks нет задач на метаданные/элементы формы. Primary — протоколы kit. |
| 3 | Разрешённость решений | OK | Decisions 1–9 и «Решения verify» закрыты. Repair явно зафиксировал: (2) канон ключа + YAML-пример; (3a) источник списка форм; (7) lone legacy = гомогенный режим на весь текущий form-scope при N≥1; (9) форма разрешения (чат/AskQuestion / `[mxl:…]` + запись в debug). Открытых «или/либо» в implementable tasks нет. F1/F2 вне Primary. |
| 4 | Порядок задач | OK | Граф S1 → S2. Только правки существующих `.cursor/**`. Ровно один `S<N>.accept` и один `<!-- slice-gate -->` на срез. Primary S1 достижим S1.1–S1.3; Primary S2 — S2.1–S2.5 после S1. S1 Primary согласован с design-stage Mode (допустимы сообщения без выбора между Metadata и Mode). |
| 5 | Data Contract Gate | OK (N/A) | Защитных проверок `Свойство()` / `ТипЗнч()` / стека guards в design/tasks нет (нет BSL). Контракты — текстовые инварианты протокола. |
| 6 | Symptom vs root | OK (N/A) | Не bug-fix: эволюция UX гейтов kit. |
| 7 | User Task Contract | OK | Pre-screen: none. В `S1.1–S1.3`, `S2.1–S2.5` нет runtime-spike (ИБ, консоль, отладчик, эмуляция API). «Учебный прогон» только в `S<N>.accept` / metadata приёмки. F1/F2 — не `S<N>.<M>`. |
| 8 | Manual config sufficiency | OK | Маркеров создания реквизитов/элементов/ролей в tasks нет (verify). «Вручную» — политика макета в accept / Behavior Contract / Decision 9, не чеклист Конфигуратора для этой ЗНИ. Таблица-доказательство в design не требуется. |

**Precedent Coherence (доп.):** OK — только ADDED capabilities; архивных MODIFIED/REMOVED для той же области нет; `## Blast Radius` не требуется. Closed decisions (макеты вне Mode Gate; per-form `form_mode` на design) согласованы proposal/design/specs/tasks после repair.

## Покрытие и согласованность (сводка, без GAP)

- Spec `sequential-gate-questions` (3 scenarios) → S1 + S1.accept.
- Spec `split-form-layout-modes` (**8** scenarios, + «Layout non-manual requires recorded apply permission») → S2.1–S2.5 + S2.accept (Primary + optional, включая новый Scenario).
- Итого `#### Scenario:`: **11** (3+8). Пропусков в tasks/accept не видно.
- QC `quality-control-2026-08-01-2.md` оценивал 10 scenarios (до repair); покрытие нового Scenario подтверждается текстами S2.1/S2.3/S2.5/S2.accept — отдельный QC-пересчёт не блокирует readiness.
- Gaps challenge-2 закрыты:
  1. Канон map / ключ метаданных / пример — Decision 2 + S2.1
  2. Enumeration — Decision 3a + S2.2
  3. Legacy×N — Decision 7 + spec Legacy + S2.2/S2.accept
  4. Permission-on-apply — Decision 9 + spec + S2.1/S2.3/S2.accept
  5. Имя секции / legacy-заголовок — Decision 2 + S2.4
  6. S1 ↔ design-stage Mode — S1 Primary/accept

## Пробелы

*(нет GAP / SUBOPTIMAL)*

Неблокирующая гигиена (не меняет вердикт):

- Имя capability `split-form-layout-modes` историческое; содержание согласовано с Decision 9.
- QC Layer 2 после repair ещё не перезапущен на счётчик 11 Scenario — оркестратору при полном re-verify обновить QC; на реализуемость as-is не влияет.

## Delta vs previous (`architecture-task-readiness-2026-08-01-2.md`)

| Замечание | Было (−2, post forms-only extend) | Сейчас (после repair-from-verify) |
|-----------|-----------------------------------|-------------------------------------|
| Канон per-form записи / ключ | Не в фокусе −2 (ещё gap challenge-2) | Закрыто Decision 2 + S2.1 |
| Enumeration «формы в scope» | Не зафиксирован | Закрыто Decision 3a + S2.2 |
| Legacy при N>1 | Неявный (a) | Явно: гомогенный режим на весь form-scope |
| Форма permission макета | Общая фраза | Норма (a)/(b) + `debug.md` § Apply permissions + Scenario |
| Вердикт | ГОТОВО | **ГОТОВО** (подтверждено после repair) |

## Источники

- `proposal.md`, `design.md`, `tasks.md`
- `specs/sequential-gate-questions/spec.md`, `specs/split-form-layout-modes/spec.md`
- Pre-screen: Manual config — маркеров создания реквизитов нет; Mechanical — none; User Task Contract — none; kit meta-change, mechanical apply `.cursor/**`
- `debug.md` § Extend — 2026-08-01 (repair-from-verify)
- `reports/design-challenge-2026-08-01-2.md` (gaps 1–6)
- `reports/architecture-task-readiness-2026-08-01-2.md` (предыдущий прогон)
- `reports/architecture-extend-coherence-2026-08-01-2.md`
- `reports/quality-control-2026-08-01-2.md` (OK; 10/10 до repair — см. гигиену выше)
- Closed decisions: макеты вне Mode Gate; per-form `form_mode` на design
