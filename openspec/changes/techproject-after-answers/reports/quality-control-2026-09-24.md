# Quality Control — Slice Coherence

- change: `techproject-after-answers`
- date: 2026-09-24
- mode: design-pre-tasks (tasks.md отсутствует; оценка среза по `design.md` § Slices)
- delta: cache miss — full plan; `changed_slices: all`
- scope note: правка навыка/команды (`.cursor/skills/openspec-techproject/SKILL.md`, `.cursor/commands/opsx-techproject.md`); кода 1С нет
- criteria evaluated: 1, 3, 5, 5b, 8, 8b, 9, 10, 11
- criteria skipped this run: 2 (independence multi-slice), 4 (multi-slice graph), 6 (rework multi-slice), 7 task-readability (нет `tasks.md`)
- reused_checks: none
- new findings: full evaluation below

### Verdict

`WARNING`

### Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1: Лист аналитику и оценка в проекте (design plan) | 6 Scenario из spec (все) | ещё не написаны | Planned `S1.accept`: Primary + optional (см. design § Чеклист приёмки); явных буллетов по именам Scenario нет | нет | `<!-- slice-gate -->` ещё нет (ожидается в `tasks.md`) |

### Scenario Coverage

| Scenario | Covered by | Status |
|---|---|---|
| Лист только по существу | S1 Primary (design): лист с вопросом по существу / без часов | OK (plan) |
| Предварительная оценка с листом | S1 Primary (design): предварительная оценка рядом с листом, ТП нет | OK (plan) |
| Уточнённая оценка в техническом проекте | S1 Optional (design): после пометки — ТП с уточнённой оценкой | OK (plan) |
| Часы не в листе | S1 Primary косвенно («нет вопросов про часы»); WHEN «две строки справочника» не выделен | WARNING — см. alerts |
| Техпроект после пометки | S1 Primary частично («ТП нет» на первом запуске); WHEN «ответы есть, пометка пустая» не выделен | WARNING — см. alerts |
| ЗНИ как задание | S1 Optional (design): «если указана ЗНИ — цепочка та же» | OK (plan) |

### Dependency Graph

```text
S1 (лист + предварительная оценка + ТП после пометки)
  └── dependencies: none
```

Циклов нет. Forward-зависимостей нет. Единственный срез — дробить на foundation без видимого outcome **не рекомендуется** (критерий 9 не срабатывает; anti-split per prompt).

### Alerts

1. **accept-bullets-missing-scenario** — WARNING  
   - affected: S1 / Scenario «Часы не в листе»  
   - evidence: в design § Чеклист приёмки Primary говорит «в листе нет вопросов про часы», но не фиксирует WHEN spec («две подходящие строки справочника → вопроса о выборе в листе нет, предварительная оценка названа»). Матрица «Покрытие Scenarios» относит Scenario к S1, отдельного optional / пути `S1.M` нет.  
   - recommendation: при генерации `tasks.md` добавить optional-буллет `Scenario «Часы не в листе»` или agent-задачу `S1.M` «верифицировать по тексту навыка/команды», что выбор из двух строк справочника не попадает в лист.

2. **accept-bullets-missing-scenario** — WARNING  
   - affected: S1 / Scenario «Техпроект после пометки»  
   - evidence: Primary описывает первый запуск без ТП; Optional — путь «после пометки появляется ТП». Spec WHEN: ответы есть, пометка подтверждения **пустая** → ТП нет, оценка остаётся предварительной. Этот негативный путь в чеклисте design не назван отдельным буллетом.  
   - recommendation: в `S1.accept` optional (или Primary, если считать blocking): `Scenario «Техпроект после пометки»: …` буквально по WHEN/THEN spec.

3. **slice-gate-deferred** — SUGGESTION (pre-tasks)  
   - affected: S1  
   - evidence: нет `tasks.md`, нет `- [ ] S1.accept`, нет `<!-- slice-gate -->`. В design запланированы Primary + optional и критерии SHALL для S1. Критерий 5 (CRITICAL при `# Срез` в tasks) пока не применим как CRITICAL.  
   - recommendation: при декомпозиции задач эмитировать ровно один `S1.accept` с `**Primary (обязательно):**` из metadata и маркер `<!-- slice-gate: … -->`.

4. **primary-acceptance-present-in-design** — informational (не алерт блокировки)  
   - `**Primary acceptance:**` в таблице Slices и mandatory Primary в § Чеклист приёмки согласованы по смыслу (один journey первого запуска). `primary-acceptance-missing` / `accept-checklist-empty` на уровне design **не** срабатывают.

### Criterion results (requested)

| # | Criterion | Result |
|---|---|---|
| 1 | Scenario Coverage | WARNING — 4/6 явно; 2 Scenario только косвенно в чеклисте |
| 3 | Slice Completeness | OK — для skill/command достаточно слоёв «навык + команда + прогон команды»; слои 1С (метаданные/формы/BSL) не требуются |
| 5 | Slice Gate Integrity | deferred SUGGESTION — gate ещё не в `tasks.md` |
| 5b | Acceptance Checklist Coverage | WARNING — см. alerts 1–2; Primary в design есть |
| 8 | Slice Verticality | OK — Primary black-box: передать задание → увидеть лист и предварительную оценку (не code-review / не вызов API) |
| 8b | Self-Achievable Acceptance | OK — один срез; Primary достижим правкой навыка/команды и прогоном `/opsx:techproject` без следующего среза |
| 9 | Foundation slice with gate | OK — нет S2-consumer; **не** предлагать foundation-срез без видимого результата |
| 10 | Acceptance Simplicity | OK — один mandatory journey (первый запуск); уточнённая оценка / ЗНИ — optional |
| 11 | User Task Contract | OK (pre-tasks) — runtime-spike в `S1.M` отсутствует; приёмка «прогнать команду» относится к границе среза (`accept`), не к mid-slice user-spike |

### Task readability

Не оценивалось: `tasks.md` ещё не создан. При генерации — паттерн «глагол + файл + результат» для `S1.M` (цели: `SKILL.md`, `opsx-techproject.md`).

### Recommendations

**Automatic fix (при написании tasks.md):**

### Remediation (auto-repair)
- alert: accept-bullets-missing-scenario
- target: `tasks.md` slice S1
- action: в теле `S1.accept` добавить optional-буллеты с буквальными именами `Scenario «Часы не в листе»` и `Scenario «Техпроект после пометки»` (WHEN/THEN из spec); Primary оставить одним mandatory journey первого запуска; эмитировать `<!-- slice-gate: лист по существу + предварительная оценка; ТП только после пометки -->`.

**Decision required:** нет. Объединение/дробление срезов не требуется. Не создавать foundation-срез «только правка навыка» с отдельным gate.

### Reused vs new

- reused: none  
- new: полный прогон design-pre-tasks по S1 и шести Scenario
