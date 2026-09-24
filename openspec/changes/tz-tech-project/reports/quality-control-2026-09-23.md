# Quality Control — Slice Coherence (design pre-tasks)

**Change:** `tz-tech-project`  
**Date:** 2026-09-23  
**Mode:** design-slices (до `tasks.md`)  
**Scope:** полный план срезов в `design.md` § Slices; `tasks.md` отсутствует — ожидаемо на этом шаге  
**Artifacts:** `design.md`, `proposal.md`, `specs/tz-tech-project/spec.md`

---

### Verdict

`WARNING`

Один вертикальный срез S1 с black-box Primary и полным графом «нет зависимостей» — структура здоровая. До генерации `tasks.md` есть пробелы в планировании чеклиста приёмки относительно всех Scenario из spec.

---

### Reused vs new

- **Reused:** нет (первый прогон QC по change).
- **New findings:** весь объём ниже.

---

### Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1: Техпроект по файлу задания | Primary: техпроект + лист по файлу; в coverage — все 4 Scenario | нет (`tasks.md` ещё нет) | план: `S1.accept` + Primary; optional «повторный запуск» | нет | план gate есть в design; маркер `<!-- slice-gate -->` и чекбокс — при генерации tasks |

**Примечание режима:** критерии 5 / 5b / 11 в части формата `S<N>.accept` и `S<N>.<M>` оцениваются по **плану** в `design.md` § «Чеклист приёмки» и § «Покрытие Scenarios», не по `tasks.md`.

---

### Scenario Coverage

| Scenario | Covered by (plan) | Status |
|---|---|---|
| Техпроект по файлу задания | S1 Primary acceptance | OK |
| В задании нет дыр | S1 Primary (фраза «дыр нет»); ветка «нет выдуманных объектов» в чеклисте не выписана явно | WARNING (частичное) |
| Повторный запуск с ответами | S1 optional / S1.M | OK |
| Обзор остаётся компилятором готовой задачи | таблица покрытия → S1; в Acceptance Checklist нет Primary / optional / S1.M | WARNING |

---

### Dependency Graph

```text
S1 (нет входящих / исходящих)
```

- Циклов нет.
- Forward-зависимостей нет.
- Undeclared edges: нет.

---

### Checklist evaluation (criteria)

| # | Criterion | Result | Notes |
|---|---|---|---|
| 1 | Scenario Coverage | WARNING | 4/4 заявлены в таблице покрытия; 1 не отражён в Acceptance Checklist; 1 покрыт Primary неполно |
| 2 | Slice Independence | OK | единственный срез |
| 3 | Slice Completeness | OK | для доменного стека (команда + навык + шаблоны) слои достаточны; cf/формы не требуются (`form_mode: n/a`) |
| 4 | Slice Dependency Graph | OK | `S1 → нет` |
| 5 | Slice Gate Integrity | DEFERRED | `S1.accept` + `<!-- slice-gate -->` обязательны при генерации `tasks.md`; в design план accept есть |
| 5b | Acceptance Checklist Coverage | WARNING | Primary в metadata среза есть; «Обзор…» не в чеклисте; см. alerts |
| 6 | Rework Risk | OK | один outcome, нет дублей срезов |
| 8 | Slice Verticality | OK | Primary — открыть оба файла и увидеть бизнес-результат (black-box) |
| 8b | Self-Achievable Acceptance | OK | нет S2; результат достижим силами S1 (команда/навык/шаблоны) |
| 9 | Foundation + gate | OK | S1 не preparatory-only: пользовательский outcome целиком в S1 |
| 10 | Acceptance Simplicity | OK | один mandatory journey |
| 11 | User Task Contract | N/A | нет `S1.<M>`; приёмка «прогнать команду» — граница среза, не mid-slice user-spike |
| 7 | Task Readability | N/A | `tasks.md` нет |

---

### Alerts

#### 1. `accept-bullets-missing-scenario` — WARNING

- **Affected:** S1 / Scenario «Обзор остаётся компилятором готовой задачи»
- **Evidence:** `spec.md` — Scenario под Requirement «Обзор задачи не меняется»; `design.md` § «Покрытие Scenarios» → S1; § «Чеклист приёмки» — только Primary и optional «Повторный запуск…»
- **Recommendation:** при генерации `tasks.md` добавить agent-задачу `S1.<M>` «верифицировать по коду / по файлам, что обзор задачи не изменён и не считает часы» **или** optional sub-bullet в `S1.accept` (не blocking Primary).

#### 2. `accept-bullets-missing-scenario` (частичное покрытие) — WARNING

- **Affected:** S1 / Scenario «В задании нет дыр»
- **Evidence:** Primary закрывает THEN «лист = фраза, что вопросов нет»; AND «техпроект не содержит выдуманных объектов и проводок» в плане чеклиста не назван
- **Recommendation:** расширить Primary одной наблюдаемой проверкой («в приложении нет имён объектов вне задания / без пометки дыры») **или** optional / `S1.<M>` static по тексту техпроекта.

#### 3. `slice-scenario-table-understated` — SUGGESTION

- **Affected:** S1, колонка «Scenarios из spec» в главной таблице § Slices
- **Evidence:** в таблице указан только сценарий «техпроект по файлу задания»; ниже coverage перечисляет четыре Scenario
- **Recommendation:** в главной таблице перечислить все четыре Scenario (как в coverage), чтобы metadata среза совпадала с spec до генерации tasks.

#### 4. Gate / accept format — DEFERRED (не CRITICAL на этом шаге)

- **Affected:** будущий `tasks.md` / S1
- **Evidence:** `tasks.md` отсутствует
- **Recommendation:** при генерации — ровно один `- [ ] S1.accept` с mandatory Primary sub-bullet, optional для повторного запуска и покрытие «Обзор…»; маркер `<!-- slice-gate: … -->`.

---

### Recommendations

**Automatic fix (при генерации `tasks.md` / правке design):**

- В `S1.accept`: один **Primary (обязательно)** из metadata; optional — «Повторный запуск с ответами».
- Добавить `S1.<M>` (или optional) для Scenario «Обзор остаётся компилятором готовой задачи».
- Явно закрыть AND Scenario «В задании нет дыр» (Primary или optional / static).
- Синхронизировать колонку «Scenarios из spec» главной таблицы с coverage (4 Scenario).

**Decision required:** нет (объединение срезов не требуется; foundation+consumer нет).

---

### Remediation (auto-repair)

```markdown
### Remediation (auto-repair)
- alert: accept-bullets-missing-scenario
- target: design.md § Чеклист приёмки → затем tasks.md S1
- action: в Optional / S1.M добавить покрытие Scenario «Обзор остаётся компилятором готовой задачи» (agent static: файлы обзора не менялись); в Primary или optional — наблюдаемый критерий «нет выдуманных объектов/проводок» для Scenario «В задании нет дыр»
```

```markdown
### Remediation (auto-repair)
- alert: slice-scenario-table-understated
- target: design.md § Slices (строка S1, колонка Scenarios из spec)
- action: перечислить все четыре Scenario из specs/tz-tech-project/spec.md буквально
```
