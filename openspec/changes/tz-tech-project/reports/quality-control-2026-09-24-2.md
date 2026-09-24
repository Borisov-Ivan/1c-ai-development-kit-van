# Quality Control — Slice Coherence

- change: `tz-tech-project`
- date: 2026-09-24
- scope: invalidated only — **S1** (`changed_slices: S1`)
- reused_checks: none (набор Scenario titles сменился; прошлый контроль среза не переиспользован)
- deterministic_results (вход): User Task Contract pre-check — нарушений нет; manual config markers — none
- affected_contract_ids: EC-6 (новое); EC-5 уточнён составом блока постановки

## Verdict

`OK`

## Scope Notes

| Item | Status |
|---|---|
| Evaluated | S1 only (criteria 1–6, 8, 8b, 9–11) |
| Reused from prior QC | none |
| New findings | none CRITICAL / WARNING; S1 coherent after scenario-set change |

## Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1: Техпроект по файлу задания | Primary = «Согласование часов»; 10 optional Scenarios в accept | S1.1–S1.10 (4×[x], 6×[ ]) + S1.accept | S1.accept (11/11: Primary + 10 optional) | нет | `<!-- slice-gate -->` present |

## Scenario Coverage

| Scenario | Covered by | Status |
|---|---|---|
| Согласование часов | S1.accept **Primary (обязательно)** (содержание совпадает с Scenario; файлы вопросов+согласования, без техпроекта/постановки) | OK |
| Техпроект для технического задания | S1.accept optional | OK |
| Постановка для задачи на разработку | S1.accept optional | OK |
| В задании нет дыр | S1.accept optional | OK |
| Повторный запуск с ответами | S1.accept optional | OK |
| Часы собраны из прозы задания | S1.accept optional (+ S1.6 формула) | OK |
| Несколько факторов надбавки | S1.accept optional (+ S1.6) | OK |
| Нет подходящей строки справочника | S1.accept optional (+ S1.6) — **новый** Scenario в наборе | OK |
| Папка шаблонов не меняет запуск | S1.accept optional (+ S1.5) | OK |
| В конфигурации нет названного объекта | S1.accept optional (+ S1.8) | OK |
| Обзор остаётся компилятором готовой задачи | S1.accept optional (+ S1.3) | OK |

Все `#### Scenario:` из `specs/tz-tech-project/spec.md` покрыты Primary или optional accept в S1. Пропусков нет.

## Dependency Graph

```text
S1 (Зависимости: нет)
```

- Срезов кроме S1 нет → циклов, forward-зависимостей и незаявленных рёбер нет.
- Критерий 8b (пара S1/S2): N/A — соседнего среза нет.
- Критерий 9 (foundation + consumer): N/A — нет `S2` с `Зависимости: S1`.

## Checklist Evaluation (S1)

| # | Criterion | Result |
|---|---|---|
| 1 | Scenario Coverage | PASS — 11/11 Scenarios покрыты |
| 2 | Slice Independence | PASS — единственный срез, принимаем без следующих |
| 3 | Slice Completeness | PASS — команда, Entry Protocol, лист, согласование, формула часов, исследование дыр, техпроект, постановка — слои для Primary и optional на месте |
| 4 | Slice Dependency Graph | PASS — `Зависимости: нет`, граф тривиален |
| 5 | Slice Gate Integrity | PASS — ровно один `S1.accept` + `<!-- slice-gate -->` |
| 5b | Acceptance Checklist Coverage | PASS — есть `**Primary acceptance:**` и `**Primary (обязательно):**`; foreign Scenario нет; пустого чеклиста нет |
| 6 | Rework Risk | PASS — нет опоры на непринятый предыдущий; дублей Scenario между срезами нет |
| 8 | Slice Verticality | PASS — Primary = black-box: открыть выходные md, увидеть лист/согласование/отсутствие нормативов; не programmatic-only |
| 8b | Self-Achievable Acceptance | PASS — Primary достижим задачами S1.* (первый запуск: вопросы+согласование); второй фазовый путь — optional, не blocking |
| 9 | Foundation with gate | PASS (N/A) — нет зависимого consumer-среза |
| 10 | Acceptance Simplicity | PASS — один mandatory journey; остальные optional |
| 11 | User Task Contract | PASS — в `S1.<M>` нет user runtime-spike / DENY; приёмка на ИБ/прогоне команды только в `S1.accept` (согласуется с deterministic pre-check) |

## Task Readability (S1)

| Task | Readability |
|---|---|
| S1.1–S1.10 | PASS — глагол + файл/навык + результат + (D*) |
| S1.accept | PASS — бизнес-результат в заголовке; чеклист Scenario-имён совпадает со spec (буквально) |

Алертов `task-opaque-title` / `task-too-short` / `task-opaque-acceptance` нет.

## Alerts

Нет.

## Recommendations

### Automatic fix

Нет.

### Decision required

Нет.

## Remediation blocks

Нет (CRITICAL/WARNING отсутствуют).
