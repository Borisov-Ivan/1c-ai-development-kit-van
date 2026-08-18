---
report_type: task-readiness
generated_at: 2026-08-09
agent: onec-code-architect
mode: task-readiness
scope:
  change: explain-after-review-apply-scope
  slices: [S1]
  files:
    - .cursor/skills/review/SKILL.md
    - .cursor/skills/openspec-apply-change/SKILL.md
    - .cursor/skills/openspec-explain/SKILL.md
    - .cursor/skills/openspec-explain/templates/entry-brief.md
    - .cursor/skills/openspec-explain/fixtures/voice-good-brief.md
    - .cursor/docs/opsx-output-style.md
    - .cursor/docs/templates/brief-card.md
    - .cursor/docs/review-guide.md
    - .cursor/commands/review.md
    - .cursor/commands/release-review.md
    - .cursor/commands/opsx-explain.md
  modules: []
  capabilities: [explain-post-implementation-scope]
related_reports:
  - reports/architecture-new-2026-08-09.md
  - reports/architecture-task-readiness-2026-08-09.md
  - reports/quality-control-2026-08-09-3.md
  - reports/design-challenge-2026-08-09-2.md
confidence: high
open_questions_count: 1
readiness: ready
blocking_gaps: []
superseded_by: null
---

# Task Readiness — explain-after-review-apply-scope (re-verify after repair)

## Контекст оценки

Kit meta-change; apply mechanical; правки markdown skills/commands/docs. Продуктовый BSL не меняется; `form_mode: n/a`; маркеров ручной конфигурации нет.

Оценено по актуальным `proposal.md`, `design.md`, `tasks.md`, `specs/explain-post-implementation-scope/spec.md` после repair-from-verify (закрыты D2a, D1 SSOT code-map, D4 Охват/Контекст, D5 MVP-only; обновлены S1.2–S1.4). Учтены: hygiene без замечаний; executability: none; QC re-run OK (`quality-control-2026-08-09-3.md`). Предыдущий отчёт `architecture-task-readiness-2026-08-09.md` — база сравнения; не источник Chosen.

## Simplicity Check

- **Viable alternatives:** (1) секция `## Explain scope` внутри review/code-map/handoff + propose/prefill; (2) отдельный `temp/explain-handoff-*.md` (Non-Goal).
- **Selected simplest viable design:** вариант (1) — один срез, без новой сущности handoff, mechanical правки существующих skills.
- **Why not simpler:** без секции и без ветки entry explain нельзя закрыть Why (автозаполнение Охвата) и Scenario prefill; без propose — нет перехода из review/apply.
- **Complexity budget:** ~11 kit-файлов; 0 hooks BSL; 0 новых метаданных; условные ветки только в тексте skill (D2/D2a/D5).

### Вердикт

**ГОТОВО** (`readiness: ready`)

Исполнитель (оркестратор / mechanical apply по markdown) может закрыть S1.1–S1.9 и `S1.accept` по design Decisions + spec без возврата на уточнение заказчику. Замечания прошлого task-readiness (OQ1, точки S1.4, SSOT S1.2) закрыты repair. Остаточный polish optional accept (имена Scenario) и косметика формулировки Requirement HALT — **не** блокируют apply.

---

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | **OK** | Каждая S1.1–S1.9 указывает файл(ы) kit и опору на D1–D5 / D2a; что писать и куда — однозначно для mechanical apply |
| 2 | Реализуемость форм и метаданных | **OK (n/a)** | `form_mode: n/a`; cf/cfe вне scope; маркеров ручной конфигурации нет |
| 3 | Разрешённость решений | **OK** | D1–D5 + D2a Chosen; OQ1–OQ2 зачёркнуты; OQ3 later; «или» в задачах = UX XOR / copy-or-link, не развилка реализации |
| 4 | Полнота покрытия | **OK** | Все 5 Requirements и 10 Scenario покрыты Primary / S1.\<M\> / optional accept (QC 10/10) |
| 5 | Согласованность | **OK** | tasks ↔ design ↔ поведение Scenario согласованы; лёгкая рыхлость текста Requirement HALT vs D4 не создаёт двух путей для исполнителя (см. ниже) |
| 6 | Связность и порядок задач | **OK** | S1.1→S1.9 → S1.accept; один slice-gate; **Зависимости:** нет |
| 7 | Архитектурная эстетика | **OK** | Handoff в существующих отчётах; без отдельного explain-handoff; propose ниже блокеров |
| 8 | User Task Contract (+ precedent) | **OK** | Нет user runtime-spike в `S1.<M>`; S1.9 ALLOW-agent; precedent n/a (новая capability) |

---

## Разбор по критериям

### 1. Реализуемость кодовых задач — OK

| Задача | Вердикт | Обоснование |
|--------|---------|-------------|
| S1.1 | OK | `review/SKILL.md`; формат = design D1; self-check |
| S1.2 | OK | `openspec-apply-change/SKILL.md`; SSOT = `code-map.md`; handoff = копия среза **или** ссылка + `focus: slice-S<N>` (D1); запрет отдельного explain-handoff |
| S1.3 | OK | Финал review/release-review; D2+D2a (не занимает слот при MUST_FIX/extend); skip trivial light-review |
| S1.4 | OK | Явно оба якоря: `opsx-output-style` §5.2 **и** T-HANDOFF next-step в `openspec-apply-change/SKILL.md`; приоритет ниже verify/extend |
| S1.5 | OK | `review.md`, `release-review.md`, `review-guide.md` |
| S1.6 | OK | `openspec-explain/SKILL.md`; source=review\|apply; Read ≤3; prefill; карта после «да» |
| S1.7 | OK | `entry-brief.md` эталон C; HALT по D4 (dump запрещён; UX Охват + path в Контекст); fixture опц. |
| S1.8 | OK | `brief-card.md` § B-explain + примеры `opsx-explain.md` |
| S1.9 | OK | Static verify kit (explore-propose; grep; disposition не трогать) — ALLOW-agent |

Целевые якоря существуют (`entry-brief.md` эталоны A/B → добавить C; `opsx-output-style.md` §5.2 T-HANDOFF на месте).

### 2. Формы и метаданные — OK (n/a)

Критерий не применяется.

### 3. Разрешённость решений — OK

| Ось | Статус |
|-----|--------|
| D1 формат + SSOT code-map | Chosen после repair |
| D2 триггеры / приоритет; ≤12 = guidance | Chosen |
| D2a propose vs MUST_FIX/extend | Chosen; OQ1 закрыт |
| D3 prefill слотов | Chosen |
| D4 Охват UX / path только в Контекст | Chosen |
| D5 MVP только `## Explain scope` | Chosen; OQ2 закрыт |
| OQ3 procedures из Code-Truth | later; procedures «желательно» |

Copy-or-link для handoff — продуктовая гибкость внутри одного канона (секция обязательна в code-map), не A/B без выбора.

### 4. Полнота покрытия — OK

| Requirement | Сценарии | Задачи / accept |
|-------------|----------|-----------------|
| Explain scope section… | Review report…; Apply artifacts… | S1.1, S1.2, Primary |
| Propose explain after review and apply | Review offers…; Apply offers…; Trivial skip… | S1.3, S1.4, S1.5; optional accept |
| B-explain prefill from handoff | Prefill…; Huge release…; No mass Read… | S1.6–S1.8, Primary |
| Brief HALT allows compact… | Compact paths allowed | S1.7; Primary (path в Контекст) |
| Explore propose remains intact | Explore still suggests… | S1.9; optional accept |

Дыр «requirement без задачи» нет. Имена optional accept paraphrased (QC SUGGESTION) — coverage через S1.3/S1.4/S1.9 сохранена; не GAP.

### 5. Согласованность — OK

- **tasks ↔ design:** S1.2↔D1 SSOT; S1.3↔D2+D2a; S1.4↔apply propose; S1.6–S1.7↔D3/D4/D5.
- **tasks ↔ spec Scenario:** поведение совпадает (MUST/MAY/MUST NOT).
- **Requirement HALT vs D4:** тело Requirement допускает «пути … в слотах Охват и Контекст», тогда как D4 / Scenario «Compact paths allowed» / Primary фиксируют path только в Контекст, UX в Охват. Для apply Chosen = D4 + Primary + S1.7; второй путь реализации не возникает. **Не GAP.** Желательная гигиена (не блокер): сузить формулировку Requirement до «UX в Охват; маркированный path в Контекст» при следующем касании spec (extend или apply-doc polish).

### 6. Связность и порядок — OK

Порядок: handoff (S1.1–S1.2) → propose (S1.3–S1.5) → prefill/эталон (S1.6–S1.8) → static verify (S1.9) → `S1.accept` + `<!-- slice-gate -->`. Один срез; зависимостей между срезами нет. Executability pre-screen: замечаний нет.

### 7. Архитектурная эстетика — OK

Минимальный kit-handoff без новой сущности файла; explore shortcut сохраняется; disposition вне scope. Over-engineering / inventiveness не обнаружены.

### 8. User Task Contract / Precedent Coherence — OK

**User Task Contract — OK:** mechanical DENY-фразы в S1.1–S1.9 отсутствуют; S1.9 — «по коду kit» (ALLOW-agent); runtime black-box только в `S1.accept` («без обязательной ИБ продукта»). Structural user-spike нет.

**Precedent Coherence — OK (n/a):** новая capability; `openspec/specs/` для области пуст; граница с `independent-review-disposition` в proposal/design; Blast Radius не требуется. S1.9 проверяет, что disposition не затронут.

---

## Пробелы

Блокирующих GAP нет.

### Неблокирующие замечания

1. **Optional accept Scenario names** (QC SUGGESTION): привести «ёлочки» к литералам `#### Scenario:` или опереться только на S1.3–S1.4 / S1.9.
2. **Requirement HALT wording:** выровнять тело Requirement с D4/Scenario (path только в Контекст) — косметика spec, Chosen для apply уже ясен.

---

## Рекомендация оркестратору

Можно запускать `/opsx:apply explain-after-review-apply-scope` (mechanical). Предыдущие blocking-notes из `architecture-task-readiness-2026-08-09.md` сняты repair.

---

## Источники

- `openspec/changes/explain-after-review-apply-scope/proposal.md`
- `openspec/changes/explain-after-review-apply-scope/design.md` (D1–D5, D2a, Slices, Открытые вопросы)
- `openspec/changes/explain-after-review-apply-scope/tasks.md` (S1.1–S1.9, S1.accept)
- `openspec/changes/explain-after-review-apply-scope/specs/explain-post-implementation-scope/spec.md`
- `openspec/changes/explain-after-review-apply-scope/reports/architecture-task-readiness-2026-08-09.md`
- `openspec/changes/explain-after-review-apply-scope/reports/quality-control-2026-08-09-3.md`
- `openspec/changes/explain-after-review-apply-scope/reports/design-challenge-2026-08-09-2.md` (контекст закрытия gaps; не источник истины Chosen)
- Kit fact-check: `entry-brief.md` (A/B + HALT), `opsx-output-style.md` §5.2
