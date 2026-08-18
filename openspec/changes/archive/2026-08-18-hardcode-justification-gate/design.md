## Context

В kit для Попытки / defensive cake уже работает четырёхслойный каркас (реестр AP + writer G14/G19/G20 + reviewer Phase 2.5 + architect Data Contract Gate). Для runtime-фильтра по строковым именам форм/метаданных (allow-list в хуке расширения) такого каркаса нет: architect сам рекомендует «тонкий» список имён, reviewer не имеет выделенного прохода, заказчик отклоняет на приёмке. Источник постановки и разбора: `reports/exploration-2026-08-08-hardcode-justification-gate.md` (копия из explore). Эволюция kit на ветке `kit-hardcode-justification-gate`, без прикладного кода 1С.

## Goals / Non-Goals

**Goals:**

- Каждый identity-filter (сравнение с полными именами форм/метаданных, литерал `ОткрытьФорму`, allow-list имён в хуке) **виноват**, пока в design нет секции Hardcode Justification или фильтр не делегирован callee/API/настройке.
- Четыре слоя зеркалят Попытку: AP-055 → architect Identity Filter Gate → writer G21 → reviewer Identity / Hardcode Audit (completeness).
- Existing Mechanisms покрывает запах Scope-as-literals (охват ADR сведён к литералам имён вместо критерия класса).

**Non-Goals:**

- Исправление allow-list в consumer-ЗНИ (`prerelease-fix-knopki-shablonov` и др.).
- Запрет литералов кодов отказа / ключей протокола / тестов / закрытых вендорских enum при явном обосновании.
- Обязательный grep post-apply в verify в первой поставке (см. Открытые вопросы).

## Decisions

1. **Каркас как у Попытки** — не одна фраза в standards, а реестр + HALT + выделенный проход + completeness.
2. **Номер AP** — следующий свободный после AP-054 → **AP-055** (Hardcoded Identity Filter). При конфликте с параллельной веткой — перенумеровать на apply.
3. **Reviewer Phase** — отдельный проход **Phase 2.6 Identity / Hardcode Audit** (не растворять только в Contract Map), по аналогии с Phase 2.5.
4. **Writer G21** — HALT до добавления identity-literals; design с allow-list без Hardcode Justification = конфликт G20-style → HALT к оркестратору.
5. **Precedent:** прикладной reject S3-B и archive `ssylka-tablitsa-knopok-dop-funkcii` — мотивация kit; код consumer вне scope.

## Implementation Options

- **Option A (выбран):** полный 4-слойный каркас (AP + architect + writer + reviewer) одним change, три вертикальных среза.
- **Option B (отклонён):** только architect-HALT + секция design — не ловит writer/reviewer на apply.
- **Option C (отклонён):** только запись в standards/AP без Phase — повторяет дыру «помни про антипаттерн».

## Behavior Contract

- Architect не выбирает Chosen «&После + список имён форм», пока в design нет ответов Identity Filter Gate (callee-фильтр? набор закрыт навсегда? план N+1?).
- Writer не добавляет `ИмяФормы = "…"`, литерал `ОткрытьФорму("…")`, allow-list имён метаданных в хуке без ссылки на Hardcode Justification или явного запрета (звать API без списка).
- Reviewer: N литералов-фильтров → N строк таблицы; contradiction с Why/Non-Goals «без хардкода» → CRITICAL / MUST_FIX AP-055.
- Легитимные литералы протокола/enum проходят только с Evidence (design-justified).

### Шаблон секции Hardcode Justification (для design прикладных ЗНИ)

**SSOT пути шаблона в kit:** `.cursor/rules/existing-mechanism-priority.mdc` (блок рядом с запахом Scope-as-literals). Прикладные ЗНИ копируют секцию оттуда в свой `design.md`. Черновик ниже — канон содержимого для S1.

```markdown
## Hardcode Justification (если есть identity-filter)
- Литералы: …
- Почему не фильтр callee/API/настройки:
- Почему набор закрыт навсегда (не «на первый релиз»):
- План при появлении N+1:
```

### Детекторы identity-filter (для карточки AP-055 и Phase 2.6 шаг A)

Считать **литералом-фильтром** (строка таблицы / кандидат AP-055), если выполняется хотя бы одно:

- сравнение `ИмяФормы` / полного имени формы с строковым литералом как guard охвата хука;
- литерал `ОткрытьФорму("…")` / аналог открытия по полному имени как фильтр «только эти формы»;
- allow-list / массив / условие по строковым именам объектов метаданных в точке расширения (хук), ограничивающий охват.

**Не** литерал-фильтр по умолчанию (Evidence / out of class): коды отказа и ключи протокола API, закрытые вендорские enum, тестовые фикстуры, имена из Non-Goals постановки при явной пометке «не identity-filter».

## Existing Mechanisms

### Найденные механизмы

| Механизм | Назначение | Можно использовать? |
|----------|-----------|---------------------|
| Preference Hierarchy + Shadow Storage / Parallel Workflow / Substituted Authority | Приоритет штатных механизмов | Да — база; не покрывает Scope-as-literals |
| Data Contract Gate / G14 / Phase 2.5 | Скепсис к guard/Попытке | Да — **эталон каркаса**, не замена для identity-filter |
| AP-031/054 allow-list | Язык идентификаторов/комментариев | Нет — другой класс (не runtime-фильтр метаданных) |

### Выбранный уровень Preference Hierarchy

**Уровень:** 2–3 (расширить точку kit) — добавить Identity Filter как запах рядом с Existing Mechanisms; не вводить новый «движок» настроек в kit.

**Обоснование:** дыра в процессе kit, не отсутствие API в 1С.

## Design Rationale

Точка правки — агенты и rules, которыми пользуются architect/writer/reviewer на каждом change. Правка только `existing-mechanism-priority` без G21/Phase 2.6 оставляет протекание на apply. Отчёт explore: `reports/exploration-2026-08-08-hardcode-justification-gate.md`.

## Slices

| Срез | Имя | Сценарий | Файлы (ядро) | Primary acceptance | Зависимости |
|------|-----|----------|--------------|--------------------|-------------|
| S1 | Реестр и запах | AP-055 + Scope-as-literals + шаблон Hardcode Justification в docs/rules | `bsl-antipatterns.mdc` (индекс + Writer bulletin) + `docs/antipatterns/bsl-antipatterns.md` (полная карточка); `existing-mechanism-priority` (запах + SSOT шаблона) | В индексе и полной карточке есть AP-055; в existing-mechanism — запах Scope-as-literals и SSOT шаблона Hardcode Justification | — |
| S2 | Architect HALT | Identity Filter Gate до Chosen allow-list | onec-code-architect, architect-gate | В agent/rules есть HALT из 3 вопросов; allow-list без секции не Chosen | S1 |
| S3 | Writer + Reviewer | G21 + Phase 2.6 completeness | onec-code-writer, onec-code-reviewer, reviewer-checks, `review/SKILL.md` (trivial-skip / порядок фаз), `1c-agent-patterns/writer.md` (Gate Results +G21) | G21 в writer; Phase 2.6 с таблицей N=N везде, где зеркалится 2.5; MUST_FIX при contradiction «без хардкода» | S2 |

### Матрица приёмки

| Scenario (capability) | S1 | S2 | S3 |
|----------------------|----|----|-----|
| AP-055 в реестре с детекторами | Primary | | |
| Scope-as-literals в Existing Mechanisms | (optional) | | |
| Protocol literals вне класса по умолчанию | (optional) | | |
| Architect HALT перед allow-list | | Primary | |
| Writer G21 блокирует литералы без design | | | Primary |
| Reviewer Phase 2.6 completeness | | | Primary |
| Contradiction Why «без хардкода» = MUST_FIX | | | Primary |

**Primary acceptance:**

- S1: открыть `bsl-antipatterns.mdc` (индекс + Writer bulletin) и `.cursor/docs/antipatterns/bsl-antipatterns.md` — AP-055 описывает Hardcoded Identity Filter, детекторы и remediation; в `existing-mechanism-priority` есть Scope-as-literals и SSOT шаблона Hardcode Justification.
- S2: в `onec-code-architect` / `architect-gate` — Identity Filter Gate (3 вопроса); без ответов вариант «список имён» не Chosen.
- S3: в writer есть G21; в reviewer + reviewer-checks + `review/SKILL.md` — Phase 2.6 с completeness; contradiction с «без хардкода» → MUST_FIX AP-055.

## Risks / Trade-offs

- [Риск] Ложные срабатывания на литералы протокола → Mitigation: явная граница «не путать» в AP-055 и Evidence-override в Phase 2.6.
- [Риск] Architect обходит Gate формулировкой «временный список» → Mitigation: вопрос «закрыт навсегда» + план N+1 обязательны.
- [Риск] Параллельная ветка займёт AP-055 → Mitigation: на apply сверить max AP и перенумеровать.

## Open Questions

- Нужен ли опциональный grep post-apply (`ИмяФормы = "`) в verify как сигнал hygiene — **не блокер** первой поставки; можно отдельным extend.
- Точное имя фазы в UI отчёта reviewer («Phase 2.6» vs «Identity Audit») — канон в этой ЗНИ: **Phase 2.6 Identity / Hardcode Audit**.
