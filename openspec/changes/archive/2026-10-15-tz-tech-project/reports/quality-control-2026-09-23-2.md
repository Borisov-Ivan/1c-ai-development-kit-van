# Quality Control — Slice Coherence

- **Change:** `tz-tech-project`
- **Date:** 2026-09-23
- **Mode:** slice
- **Scope:** full current plan (cache miss; `changed_slices: all`)
- **Reused checks:** none
- **Invalidated / evaluated:** S1 only (единственный срез)
- **Prior report:** `reports/quality-control-2026-09-23.md` не переиспользован

### Verdict

`OK`

### Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1: Техпроект по файлу задания | По файлу задания — лист вопросов и техпроект с часами | S1.1–S1.8 (8) | S1.accept (Primary + 3 optional; 4/4 Scenario покрыты) | нет | `<!-- slice-gate -->` present |

### Scenario Coverage

| Scenario | Covered by | Status |
|---|---|---|
| Техпроект по файлу задания | S1.accept **Primary** (metadata + mandatory bullet) | OK |
| В задании нет дыр | S1.accept optional + S1.4 / S1.5 / S1.8 (агент) | OK |
| Повторный запуск с ответами | S1.accept optional + S1.2 / S1.6 | OK |
| Обзор остаётся компилятором готовой задачи | S1.accept optional + S1.3 (файлы overview не менять) | OK |

### Dependency Graph

```text
S1 (нет входящих / исходящих зависимостей)
```

Циклов нет. Forward-зависимостей нет. Объявленные зависимости соответствуют метаданным (`**Зависимости:** нет`).

### Criteria Checklist (S1)

| # | Criterion | Result |
|---|---|---|
| 1 | Scenario Coverage | PASS — все 4 `#### Scenario:` из `specs/tz-tech-project/spec.md` покрыты Primary / optional accept / задачами |
| 2 | Slice Independence | PASS — один срез; приёмка не требует следующего |
| 3 | Slice Completeness | PASS — команда, навык, каркас, перенос шаблонов/нормативов, сверка с конфигурацией — достаточно для Primary |
| 4 | Slice Dependency Graph | PASS |
| 5 | Slice Gate Integrity | PASS — ровно один `S1.accept` + `<!-- slice-gate -->` |
| 5b | Acceptance Checklist Coverage | PASS — есть `**Primary acceptance:**` и `**Primary (обязательно):**`; сценарии покрыты; чужих Scenario нет |
| 6 | Rework Risk | PASS — нет опоры на непринятый соседний срез; дублей Scenario между срезами нет |
| 8 | Slice Verticality | PASS — Primary: открыть оба выходных файла и увидеть содержимое (black-box), не programmatic-only |
| 8b | Self-Achievable Acceptance | PASS — Primary достижим задачами S1.1–S1.8 (создание команды/навыка → два файла) |
| 9 | Foundation slice with gate | PASS — нет S2 / consumer-среза |
| 10 | Acceptance Simplicity | PASS — один mandatory journey; остальные optional |
| 11 | User Task Contract | PASS — DENY-фраз в `S1.<M>` нет (подтверждено pre-check verify 2.1a); runtime-spike пользователю не назначен |

### Task Readability

| Task | Pattern (глагол + объект + результат + ссылка) | Alert |
|---|---|---|
| S1.1 | OK — путь команды + зачем + (D1) | — |
| S1.2 | OK — путь навыка + Entry Protocol / выход + (D1, D4) | — |
| S1.3 | OK — каркас в навыке, запрет правок overview + (D2) | — |
| S1.4 | OK — лист вопросов в навыке + (D1) | — |
| S1.5 | OK — источник `template/Техпроект` → навык + (D4) | — |
| S1.6 | OK — `labor_standards.md` → закрытый справочник + (D3) | — |
| S1.7 | OK — карта разделов входящего + (D4) | — |
| S1.8 | OK — сверка объектов/счетов + (D5) | — |
| S1.accept | OK — бизнес-результат в заголовке; имена Scenario буквально совпадают со spec | — |

### Alerts

Нет.

### Recommendations

**Automatic fix:** нет.

**Decision required:** нет.

### Notes (non-blocking)

- Manual config checklist (verify 5.1): маркеров ручной конфигурации в `tasks.md` нет — согласуется с change без метаданных 1С.
- Mechanical check issues: none.
- User Task Contract pre-check evidence: DENY / «после verify» / «после стенда» — не найдены.
- Repository state из промпта (наличие `template/Техпроект`, отсутствие ещё не созданных `opsx-techproject.md` / `SKILL.md`) — transient для apply; на structural QC не влияет.
- В `design.md` § Slices колонка «Scenarios из spec» для S1 перечисляет только один сценарий; покрытие в `tasks.md` и таблице «Покрытие Scenarios» design — полное (4/4). Расхождение design↔tasks не эмитируется как alert Slice Coherence (оценка — tasks vs specs).
