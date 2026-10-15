# Quality Control — Slice Coherence

**Change:** `tz-tech-project`  
**Date:** 2026-09-23  
**Scope:** invalidated S1 (full); linked scenarios from delta  
**Mode:** slice  
**Reused checks:** none  
**New findings:** S1 full pass of criteria 1–6, 8, 8b, 9–11 + task readability

## Verdict

`OK`

## Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1: Техпроект по файлу задания | По файлу задания — лист вопросов и техпроект с часами | S1.1–S1.8 | S1.accept (5/5: Primary + 4 optional) | нет | `<!-- slice-gate -->` present |

## Scenario Coverage

| Scenario | Covered by | Status |
|---|---|---|
| Техпроект по файлу задания | S1 Primary (metadata + mandatory accept) | OK |
| В задании нет дыр | S1.accept optional | OK |
| Повторный запуск с ответами | S1.accept optional (+ S1.2 protocol) | OK |
| В выгрузке нет названного объекта | S1.accept optional (+ S1.8) | OK |
| Обзор остаётся компилятором готовой задачи | S1.accept optional (+ S1.3 «не менять overview») | OK |

Все `#### Scenario:` из `specs/tz-tech-project/spec.md` привязаны к S1; пропусков нет.

## Dependency Graph

```text
S1 (нет входящих / исходящих зависимостей)
```

Циклов нет. Forward-зависимостей нет (единственный срез).

## Checklist Results (S1)

| # | Criterion | Result | Notes |
|---|---|---|---|
| 1 | Scenario Coverage | PASS | 5/5 scenarios covered via Primary / optional accept / S1.M |
| 2 | Slice Independence | PASS | Единственный срез; приёмка не требует S2+ |
| 3 | Slice Completeness | PASS | Команда, навык, перенос шаблонов, сверка cf, каркас выхода — слои для Primary на месте (kit-change, не BSL/формы) |
| 4 | Slice Dependency Graph | PASS | `Зависимости: нет`; согласовано с design.md § Slices |
| 5 | Slice Gate Integrity | PASS | Ровно один `S1.accept` + маркер `<!-- slice-gate -->` |
| 5b | Acceptance Checklist Coverage | PASS | Primary metadata + mandatory bullet; scenarios covered; foreign bullets отсутствуют |
| 6 | Rework Risk | PASS | Нет опоры на непринятый соседний срез; дублей сценариев между срезами нет |
| 8 | Slice Verticality | PASS | Primary — black-box: открыть два файла рядом с заданием, проверить содержимое |
| 8b | Self-Achievable Acceptance | PASS | Primary достижим задачами S1.1–S1.8 (команда+навык пишут оба файла); нет S2 с дублем journey |
| 9 | Foundation + gate | PASS | Нет зависимого consumer-среза; foundation-with-gate не применим |
| 10 | Acceptance Simplicity | PASS | Один mandatory Primary; остальные optional |
| 11 | User Task Contract | PASS | В S1.1–S1.8 нет DENY runtime-spike / «после verify|стенда»; user runtime только в S1.accept. Pre-check evidence подтверждён семантически |

## Task Readability

| Task | Pattern | Status |
|---|---|---|
| S1.1 | Глагол + путь команды + результат + (D1) | OK |
| S1.2 | Глагол + путь навыка + контракт входа/выхода + (D1, D4) | OK |
| S1.3 | Глагол + каталог навыка + каркас + ограничение overview + (D2) | OK |
| S1.4 | Глагол + навык + контракт листа + (D1) | OK |
| S1.5 | Глагол + источник/приёмник + результат + (D4) | OK |
| S1.6 | Глагол + labor_standards + правила часов + (D3) | OK |
| S1.7 | Глагол + навык + карта разделов + (D4) | OK |
| S1.8 | Глагол + протокол сверки cf + дыра без выдумки + (D5) | OK |
| S1.accept | Бизнес-результат + Primary + optional Scenario-буллеты | OK |

Алертов `task-opaque-title` / `task-too-short` / `task-opaque-acceptance` нет.

## Alerts

Нет.

## Recommendations

### Automatic fix

Нет.

### Decision required

Нет.

## Reused vs new

- **Reused:** none (кэш инвалидирован; полный прогон S1).
- **New findings:** full S1 evaluation including Scenario «В выгрузке нет названного объекта» — PASS; overall verdict `OK`.
