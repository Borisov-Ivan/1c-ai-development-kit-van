# Quality Control — Slice Coherence

- change: `techproject-after-answers`
- date: 2026-09-24
- mode: slice
- scope: delta — `changed_slices: S1` (полный контроль с нуля); `reused_checks: none`
- previous QC: `quality-control-2026-09-24-3.md` **не** переиспользован (набор сценариев и текст задач/Primary переписаны)
- artifacts: `tasks.md`, `design.md`, `proposal.md`, `specs/techproject-after-answers/spec.md`
- repo check: `.cursor/skills/openspec-techproject/SKILL.md` — существует; `.cursor/commands/opsx-techproject.md` — существует; `openspec/project.md` — нет (ожидаемо для kit)

## Verdict

`OK`

## Reused vs new findings

| Scope | Status |
|---|---|
| S1 + 14 linked scenarios | **new findings** (полный прогон) |
| reused_checks | none |
| deterministic coverage cache | не переиспользован; покрытие пересчитано |

## Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1 Лист аналитику и оценка в проекте | 14 Scenario из spec (см. coverage) | S1.1–S1.5 (skill + command) | `S1.accept` (Primary + 12 optional = **14/14**) | срезов нет; внешнее предусловие `tz-tech-project` S1.accept | `<!-- slice-gate -->` есть |

## Scenario Coverage

Подтверждено: **14** `#### Scenario:` в spec; **14** в `## Slices` / таблице покрытия design; **14** в `**Связь со spec:**` и чеклисте `S1.accept` (2 через Primary + 12 optional bullets).

| Scenario | Covered by | Status |
|---|---|---|
| Лист только по существу | S1 Primary (metadata + mandatory sub-bullet) | OK |
| Предварительная оценка с листом | S1 Primary (metadata + mandatory sub-bullet) | OK |
| Часы не в листе | S1.accept optional | OK |
| Нет подходящей строки справочника | S1.accept optional | OK |
| Часы из чата сохраняются | S1.accept optional | OK |
| Без пометки техпроекта нет | S1.accept optional | OK |
| Уточнённая оценка в техническом проекте | S1.accept optional | OK |
| Расхождение оценки в техническом проекте | S1.accept optional | OK |
| Пробел при записи проекта | S1.accept optional | OK |
| Внедрение и откат без вопроса | S1.accept optional | OK |
| ЗНИ как задание | S1.accept optional | OK |
| Вход из существующей задачи без постановки | S1.accept optional | OK |
| Пробел закрыт решением задачи | S1.accept optional | OK |
| Задача из архива | S1.accept optional | OK |

Agent verification path: implementation-only сценариев без UX нет; все Scenario — наблюдаемое поведение команды. Задачи S1.1–S1.5 — правка навыка/команды (не user-spike).

## Dependency Graph

```text
(external) tz-tech-project S1.accept ──precondition──► S1
S1 ──(no slice deps)──► (end)
```

- Циклов нет.
- Forward-зависимостей приёмки нет (один срез).
- Объявленная зависимость: «срезов внутри задачи нет; внешнее предусловие — приёмка `tz-tech-project`» — согласовано с design `## Slices`.
- Факт среды (не дефект постановки): в `openspec/changes/tz-tech-project/tasks.md` сейчас `S1.accept` = `[ ]`. По правилу tasks.md навык не переписывается до отметки — блокер apply/транзиент, не CRITICAL QC.

## Criteria checklist (1–6, 8, 8b, 9–11)

| # | Criterion | Result | Notes |
|---|---|---|---|
| 1 | Scenario Coverage | PASS | 14/14 покрыты Primary или optional accept |
| 2 | Slice Independence | PASS | единственный срез; принимаем без следующих |
| 3 | Slice Completeness | PASS | слои для outcome — skill + command; оба в S1.1–S1.5; BSL/формы/XML не требуются (`form_mode: n/a`) |
| 4 | Slice Dependency Graph | PASS | нет slice-to-slice; внешнее предусловие объявлено |
| 5 | Slice Gate Integrity | PASS | ровно один `S1.accept`; маркер `<!-- slice-gate -->` есть; phase-gate нет |
| 5b | Acceptance Checklist Coverage | PASS | Primary metadata + mandatory sub-bullet есть; чеклист не пуст; foreign Scenario нет |
| 6 | Rework Risk | PASS | дублей Scenario между срезами нет; внешнее предусловие явно |
| 8 | Slice Verticality | PASS | Primary — black-box: передать задание → лист без часов-вопросов + предварительная оценка; техпроекта нет |
| 8b | Self-Achievable Acceptance | PASS | Primary достижим силами S1.1–S1.5 (нет S2 / forward journey) |
| 9 | Foundation + gate | PASS | нет S2 consumer; антипаттерн foundation-with-gate не применим |
| 10 | Acceptance Simplicity | PASS | один mandatory Primary; остальные 12 — «(опционально)» |
| 11 | User Task Contract | PASS | S1.1–S1.5 без DENY (ИБ/стенд/runtime-spike/консоль/отладчик); без «после verify/стенда»; orchestrator pre-check подтверждён семантикой |

## Task Readability

| Task | Pattern | Status |
|---|---|---|
| S1.1–S1.5 | Глагол + путь файла (SKILL.md / opsx-techproject.md) + что менять + (решения N) | OK |
| S1.accept | Бизнес-результат в заголовке + чеклист Scenario | OK |

Алертов `task-opaque-title` / `task-too-short` / `task-opaque-acceptance` нет. Формулировки длинные (skill-rewrite), но самодостаточны для исполнителя.

## Alerts

Нет CRITICAL / WARNING / SUGGESTION по критериям Slice Coherence.

Informational (не alert): внешнее предусловие `tz-tech-project` S1.accept ещё `[ ]` — apply по собственному правилу change отложен до отметки; это не нарушение независимости срезов внутри change.

## Recommendations

### Automatic fix

Нет.

### Decision required

Нет.

## Gate / mechanical notes (from orchestrator + confirm)

- Manual config checklist: none (маркеров Конфигуратор/реквизит/роль/элемент формы нет).
- Mechanical: чекбоксы есть; один `S1.accept`; `<!-- slice-gate -->` есть; `<!-- phase-gate -->` нет; `form_mode: n/a`.
- User Task Contract pre-check (verify 2.1a): DENY-подстрок в S1.1–S1.5 нет — подтверждено.
