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
  - reports/quality-control-2026-08-09.md
confidence: high
open_questions_count: 3
readiness: ready-with-notes
blocking_gaps: []
superseded_by: null
---

# Task Readiness — explain-after-review-apply-scope

## Контекст оценки

Kit meta-change: режим apply mechanical; правки markdown skills/commands/docs в `.cursor/`. Продуктовый BSL не меняется; writer BSL не нужен. Формы/метаданные: `form_mode: n/a`. Маркеров ручной конфигурации нет.

Оценено по: `proposal.md`, `design.md`, `tasks.md`, `specs/explain-post-implementation-scope/spec.md`. Учтены: hygiene без замечаний; User Task Contract pre-check: none; QC verdict OK; executability pre-screen: none. Открытые вопросы design (1–3) не блокируют сами по себе — проверено, создают ли неоднозначность задач.

### Вердикт

**ГОТОВО С ЗАМЕЧАНИЯМИ** (`readiness: ready-with-notes`)

Агенты (оркестратор/apply по markdown) и пользователь (приёмка протокола kit в `S1.accept`) могут реализовать ЗНИ без возврата на уточнение заказчику. Decisions D1–D5 + сценарии spec задают достаточной Chosen для всех задач S1.1–S1.9. Замечания — документальная гигиена (закрыть формулировку открытого вопроса №1 в design; уточнить точки правки для propose в apply-handoff) — **не** блокируют старт apply.

---

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | **OK** | Каждая S1.1–S1.9 указывает файл(ы) kit и ссылку на D1–D5 / формат; что писать и куда — однозначно для mechanical apply |
| 2 | Реализуемость форм и метаданных | **OK (n/a)** | `form_mode: n/a`; cf/cfe вне scope; маркеров ручной конфигурации нет |
| 3 | Разрешённость решений | **OK** | D1–D5 Chosen; «или» в задачах — продуктовая гибкость (Охват XOR Варианты; code-map и/или handoff), не развилка реализации; OQ закрыты правилом или out of MVP |
| 4 | Полнота покрытия | **OK** | Все 5 Requirements и 10 Scenario spec покрыты Primary / S1.<M> / optional accept |
| 5 | Согласованность | **OK** | tasks ↔ design Decisions и tasks ↔ spec без противоречий поведения |
| 6 | Связность и порядок задач | **OK** | S1.1→S1.9 → S1.accept; handoff → propose → prefill → verify; один slice-gate; зависимостей между срезами нет |
| 7 | Архитектурная эстетика | **OK** | Handoff внутри существующих отчётов; без отдельного explain-handoff; один срез; бюджет брифа сохранён — без over-engineering |
| 8 | User Task Contract (+ precedent) | **OK** | Нет user runtime-spike в `S1.<M>`; приёмка только в `S1.accept`; precedent n/a (новая capability) |

---

## Разбор по критериям

### 1. Реализуемость кодовых задач — OK

| Задача | Вердикт | Обоснование |
|--------|---------|-------------|
| S1.1 | OK | Файл `review/SKILL.md`; формат секции = design D1; self-check — достаточно для правки skill |
| S1.2 | OK | Файл `openspec-apply-change/SKILL.md`; место = `code-map` и/или `handoff-acceptance` при BSL; запрет отдельного handoff-файла явен. «и/или» = inclusive OR из spec (достаточно одного артефакта; при записи обоих — писать секцию в оба) |
| S1.3 | OK | Финал review/release-review («Куда дальше» / шаг 7); условия и приоритет = D2 + Scenario «нет нерешённого MUST_FIX ask»; skip trivial light-review |
| S1.4 | OK* | Якорь `opsx-output-style` §5.2 (T-HANDOFF / short-cut) + условие D2 (BSL acceptance/final). *SUGGESTION: при apply также добавить одну строку next-step в `openspec-apply-change/SKILL.md` шаг 7, если short-cut живёт и там — см. замечания |
| S1.5 | OK | Три пути: `review.md`, `release-review.md`, `review-guide.md` — существуют |
| S1.6 | OK | `openspec-explain/SKILL.md`; ветка source=review\|apply; Read ≤3; prefill Охват/Варианты; карта после «да» — совпадает со spec |
| S1.7 | OK | `entry-brief.md` сейчас имеет эталоны A/B → добавить эталон C по D3; HALT: сырой dump запрещён, компактный охват разрешён; fixture опционален |
| S1.8 | OK | `brief-card.md` § B-explain + примеры в `opsx-explain.md` |
| S1.9 | OK | Статическая верификация kit (explore-propose на месте; grep; disposition не трогать) — ALLOW-agent |

**Итог C1: OK** — непонятного «что / где» для исполнителя нет.

### 2. Формы и метаданные — OK (n/a)

Критерий не применяется к kit meta-change.

### 3. Разрешённость решений — OK

**Закрытые оси (OK):** D1 формат секции; D2 таблица триггеров/приоритета; D3 таблица слотов B-explain; D4 HALT vs компактный охват; D5 MVP = только новый формат для автозаполнения; Non-Goals (отдельный handoff-файл, автостарт без «да»).

**Открытые вопросы design — влияние на apply:**

| # | Вопрос | Вердикт | Почему не блокер |
|---|--------|---------|------------------|
| 1 | fix ask vs explain: вторичный hint vs только после отказа от fix | **не GAP** | Spec Scenario «Review offers explain»: предложение **когда нет нерешённого MUST_FIX ask**; D2 — приоритет ниже fix/extend. Исполнитель: не предлагать explain как default, пока открыт MUST_FIX ask; после закрытия/отсутствия — MAY propose. Вторичный hint «также можно» **не** требуется ни одним Scenario → безопасный Chosen = не показывать параллельно с активным fix ask |
| 2 | Fallback старых отчётов без секции | **не GAP** | D5 + формулировка «prefer только новый формат» / MVP only new format — Chosen для первой итерации ясен; эвристика later |
| 3 | Обогащение procedures из Code-Truth | **не GAP** | Явно later; D1: procedures опциональны («желательно») |

Прочие «или»/«/»: Охват XOR Варианты (D3, платформенный UX); code-map и/или handoff (spec MUST на появление секции, не на exclusive-or файл); trivial «не предлагать (или мягкий hint)» → spec MUST NOT требовать default propose → skip достаточен.

### 4. Полнота покрытия — OK

| Requirement | Сценарии | Задачи / accept |
|-------------|----------|-----------------|
| Explain scope section… | Review report…; Apply artifacts… | S1.1, S1.2, Primary |
| Propose explain after review and apply | Review offers…; Apply offers…; Trivial skip… | S1.3, S1.4, S1.5; optional accept |
| B-explain prefill from handoff | Prefill Охват…; Huge release Варианты; No mass Read… | S1.6, S1.7, S1.8, Primary |
| Brief HALT allows compact… | Compact paths allowed | S1.7 |
| Explore propose remains intact | Explore still suggests… | S1.9; optional accept |

Дыр «requirement/scenario без задачи» нет. Матрица приёмки design («все scenarios → Primary или S1.<M> / optional») соблюдена.

### 5. Согласованность — OK

- **tasks ↔ design:** S1.1–S1.2 ↔ D1/D5; S1.3–S1.5 ↔ D2; S1.6–S1.8 ↔ D3/D4; S1.9 ↔ Non-Goals / границы с disposition.
- **tasks ↔ spec:** формулировки MUST/MAY/MUST NOT согласованы с текстом задач и optional accept.
- **proposal Impact** (explain + review + apply + guide/commands) ↔ список файлов в задачах — полный.
- Противоречий «отдельный handoff vs секция» нет (везде запрет отдельного файла).

### 6. Связность и порядок — OK

Логика: сначала обязать писать секцию (S1.1–S1.2), затем propose (S1.3–S1.5), затем чтение/prefill/эталон (S1.6–S1.8), затем статическая сверка (S1.9), затем `S1.accept` + `<!-- slice-gate -->`. Один срез; **Зависимости:** нет. Pre-screen executability: замечаний нет.

### 7. Архитектурная эстетика — OK

Минимальный handoff для kit: секция в уже существующих артефактах, propose ниже блокеров, prefill без автостарта карты, без новой сущности `temp/explain-handoff-*.md`. Варианты рамки только для huge release — уместно. Over-engineering не обнаружен.

### 8. User Task Contract / Precedent Coherence — OK

**User Task Contract — OK:** S1.1–S1.9 — правки markdown оркестратором; нет DENY/user runtime-spike в нумерованных шагах. Runtime black-box приёмка протокола kit — только `S1.accept` (допустимо).

**Precedent Coherence — OK (n/a evidence):** Cross-Archive / KB в промпт не передавались; capability новая (`openspec/specs/` для области пуст). Конфликта с архивным контрактом по артефактам change нет; Blast Radius не требуется. Граница с `independent-review-disposition` зафиксирована (не пересекать disposition) — S1.9 это проверяет.

---

## Замечания (не блокируют apply)

1. **Закрыть текст OQ1 в design** (гигиена): в Decisions добавить одну строку Chosen — «`/opsx:explain` в финале review предлагать только при отсутствии нерешённого MUST_FIX ask; параллельный secondary hint во время fix ask не входит в MVP». Снижает риск, что исполнитель изобретёт «также можно» в карточке 4 слотов.
2. **S1.4 точки правки:** явно упомянуть в задаче оба места при необходимости: `opsx-output-style.md` §5.2 **и** next-step блок T-HANDOFF в `openspec-apply-change/SKILL.md` (шаг 7), чтобы propose не остался только в style-доке.
3. **S1.2 при обоих артефактах:** рекомендовать писать `## Explain scope` и в `code-map.md`, и в `handoff-acceptance-*`, когда оба создаются на acceptance (spec допускает один; дубль дешёв и упрощает вход `@`).

Блокирующих GAP / SUBOPTIMAL, требующих правки до apply, **нет**.

---

## Рекомендация оркестратору

Можно запускать `/opsx:apply explain-after-review-apply-scope` (mechanical). Желательно перед или в ходе S1.3 одной строкой закрыть OQ1 в `design.md` (замечание 1) — без отдельного extend, если правка чисто документальная Chosen = уже текст spec Scenario.

---

## Источники

- `openspec/changes/explain-after-review-apply-scope/proposal.md`
- `openspec/changes/explain-after-review-apply-scope/design.md` (§ Decisions D1–D5, § Открытые вопросы, § Slices)
- `openspec/changes/explain-after-review-apply-scope/tasks.md` (S1.1–S1.9, S1.accept, slice-gate)
- `openspec/changes/explain-after-review-apply-scope/specs/explain-post-implementation-scope/spec.md` (5 Requirements, 10 Scenario)
- `openspec/changes/explain-after-review-apply-scope/reports/architecture-new-2026-08-09.md`
- `openspec/changes/explain-after-review-apply-scope/reports/quality-control-2026-08-09.md`
- Kit fact-check: `entry-brief.md` (эталоны A/B), `brief-card.md` § B-explain, `opsx-output-style.md` §5.2, `review/SKILL.md` («Куда дальше»), `openspec-apply-change/SKILL.md` (code-map / handoff-acceptance)
