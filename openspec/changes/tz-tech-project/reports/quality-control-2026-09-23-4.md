# Quality Control — Slice Coherence

- **Change:** `tz-tech-project`
- **Date:** 2026-09-23
- **Scope:** delta — `changed_slices: S1` only
- **Mode:** slice (`# Срез S1` present)
- **Criteria:** 1–6, 8, 8b, 9–11 (+ task readability)
- **Reused checks:** none
- **New findings:** full evaluation of S1

## Verdict

`OK`

## Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1 | По файлу задания — лист вопросов и техпроект с часами | S1.1–S1.8 (8) | S1.accept (Primary + 6 optional / 7 scenarios) | нет | `<!-- slice-gate -->` present |

## Scenario Coverage

| Scenario | Covered by | Status |
|---|---|---|
| Техпроект по файлу задания | S1 Primary (metadata + mandatory accept bullet) | OK |
| В задании нет дыр | S1.accept optional | OK |
| Повторный запуск с ответами | S1.accept optional | OK |
| Часы собраны из прозы задания | S1.accept optional | OK |
| Папка шаблонов не меняет запуск | S1.accept optional | OK |
| В выгрузке нет названного объекта | S1.accept optional | OK |
| Обзор остаётся компилятором готовой задачи | S1.accept optional | OK |

Все 7 `#### Scenario:` из `specs/tz-tech-project/spec.md` покрыты в S1 (Primary или optional accept). Linked scenarios из delta совпадают со связью со spec.

## Dependency Graph

```text
S1 (Зависимости: нет)
```

- Срезов кроме S1 нет → циклов нет, forward-зависимостей нет, необъявленных рёбер нет.
- Критерий 9 (foundation + consumer) не применим: нет `S2` с `Зависимости: S1`.

## Checklist Evaluation (S1)

| # | Criterion | Result | Notes |
|---|---|---|---|
| 1 | Scenario Coverage | PASS | Все Scenario spec покрыты Primary / optional accept |
| 2 | Slice Independence | PASS | Один срез; приёмка не требует позднейших срезов |
| 3 | Slice Completeness | PASS | Команда + навык + перенос шаблонов/нормативов + сверка cf + accept; слои 1С (метаданные/формы/BSL) не требуются (`form_mode: n/a`, Impact: конфигурация не меняется) |
| 4 | Slice Dependency Graph | PASS | Объявлено «нет»; граф тривиален |
| 5 | Slice Gate Integrity | PASS | Ровно один `S1.accept`; маркер `<!-- slice-gate -->` есть |
| 5b | Acceptance Checklist Coverage | PASS | Есть `**Primary acceptance:**` и `**Primary (обязательно):**`; сценарии покрыты; чужих Scenario нет; тело accept не пусто |
| 6 | Rework Risk | PASS | Нет опоры на непринятый предыдущий; нет дубля сценария между срезами |
| 8 | Slice Verticality | PASS | Mandatory Primary — black-box: открыть два выходных файла и увидеть содержимое (лист/«дыр нет», этапы, приложение, часы без таблицы нормативов); не programmatic-only |
| 8b | Self-Achievable Acceptance | PASS | Primary достижим задачами S1.1–S1.8 (создание команды/навыка, перенос правил, сверка cf); нет S2 и нет дубля journey |
| 9 | Foundation + gate | PASS (N/A) | Нет зависимого consumer-среза |
| 10 | Acceptance Simplicity | PASS | Один mandatory black-box journey; остальные optional |
| 11 | User Task Contract | PASS | В `S1.1`–`S1.8` нет user runtime-spike (ИБ/консоль/отладчик/API) и нет условных цепочек «после verify/стенда»; DENY-подстроки не найдены. Прогон `/opsx:techproject` — в `S1.accept` / metadata Приёмка (допустимо пользователю на границе среза) |

## Task Readability

| Task | Pattern check | Alert |
|---|---|---|
| S1.1 | Глагол + путь файла + результат + (D1) | OK |
| S1.2 | Глагол + путь навыка + Entry Protocol / результат + (D1, D4) | OK |
| S1.3 | Путь навыка + каркас/голос + запрет правки overview + (D2) | OK |
| S1.4 | Навык + формат листа вопросов + (D1) | OK |
| S1.5 | Источник `template/Техпроект` → навык + результат + (D4) | OK |
| S1.6 | Файл нормативов → навык + правила часов + (D3) | OK |
| S1.7 | Навык + карта разделов ЧТЗ + (D4) | OK |
| S1.8 | Протокол навыка + сверка `src/КАСК/cf/` + (D5) | OK |
| S1.accept | Бизнес-результат в заголовке; Primary + optional Scenario по имени | OK |

Алертов `task-opaque-title` / `task-too-short` / `task-opaque-acceptance` нет.

## Alerts

Нет CRITICAL / WARNING / SUGGESTION по критериям 1–6, 8, 8b, 9–11 и task readability для S1.

## Recommendations

### Automatic fix

Нет.

### Decision required

Нет.

## Reused vs New

| Scope | Status |
|---|---|
| S1 (full criteria 1–6, 8, 8b, 9–11) | **new** evaluation this run |
| Other slices | none in change |
| `reused_checks` | none provided |

## Evidence anchors

- `tasks.md`: `# Срез S1`, metadata Primary/Связь со spec, `S1.1`–`S1.8`, `S1.accept`, `<!-- slice-gate: … -->`
- `specs/tz-tech-project/spec.md`: 6 Scenario under «Техпроект по файлу задания» + 1 under «Обзор задачи не меняется»
- `design.md` § Slices: S1 only, graph `S1 → нет`
- Repository state (prompt): template/Техпроект и labor_standards есть; команда/навык techproject ещё не созданы — **transient** для apply, не structural QC fail
