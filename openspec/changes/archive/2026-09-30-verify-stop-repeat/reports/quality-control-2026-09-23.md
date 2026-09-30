# Quality Control — verify-stop-repeat — 2026-09-23

**Mode:** pre-tasks (design `## Slices`); `tasks.md` отсутствует.  
**Scope:** changed_slices = all (первый прогон); reused_checks = none.  
**Criteria evaluated:** 1, 3, 5, 5b, 8, 8b, 9, 10, 11.  
**Out of scope:** исполнимость на ИБ 1С; критерий 2/4/6/7 — не в запросе (граф зависимостей и readability задач — кратко по факту отсутствия `tasks.md`).

### Verdict

`CRITICAL`

### Reused vs new

- **Reused:** нет.
- **New findings:** все алерты ниже — по предложенному срезу S1 в `design.md` и сценариям `specs/verify-stop-repeat/spec.md`.

### Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1 Остановка повторной проверки | 4 из 5 сценариев в «Связь со spec» (нет «Смена правила смотрится заново») | нет (`tasks.md` не создан) | Primary в design + чеклист из **трёх обязательных** пунктов (ещё не `S1.accept`) | нет | маркера `<!-- slice-gate -->` и `S1.accept` пока нет |

### Scenario Coverage

| Scenario | Covered by | Status |
|---|---|---|
| Прошлый контроль среза остаётся | design чеклист п.1; Связь со spec | OK (в design) |
| Уточнение той же темы | design чеклист п.2; Связь со spec | OK (в design) |
| Смена правила смотрится заново | ни Связь со spec, ни чеклист, ни заявленная задача | **MISSING** |
| Стоп на третьей правке | **Primary acceptance** + чеклист п.3; Связь со spec | OK (в design) |
| Ответ человека сохраняется | design чеклист п.3 (совмещён со стопом); Связь со spec | OK (в design) |

### Dependency Graph

```text
S1 (единственный срез, Зависимости: нет)
```

Циклов, forward-зависимостей и соседнего `S2` нет.

### Criteria notes (requested)

#### 1. Scenario Coverage

Пять `#### Scenario:` в spec. Четыре заявлены в design «Связь со spec». Сценарий **«Смена правила смотрится заново»** нигде не покрыт → WARNING `accept-bullets-missing-scenario`.

#### 3. Slice Completeness

ЗНИ — правила набора (verify + подсчёт правок), без слоёв метаданных/форм/BSL. В design указаны файлы: правила повторного прохода и подсчёта правок. Для kit-change этого достаточно как указания слоёв приёмки. Задач `S1.<M>` ещё нет — полнота стека задач не проверялась построчно; структурных дыр «нужен слой X для Primary, а его нет в срезе» по design не видно.

#### 5. Slice Gate Integrity

`tasks.md` нет → формальных `S1.accept` и `<!-- slice-gate -->` нет. На этапе design это ожидаемо; при генерации tasks **MUST** появиться ровно один `S1.accept` и маркер gate. SUGGESTION: зафиксировать при генерации (не CRITICAL до появления `# Срез` в tasks).

#### 5b. Acceptance Checklist Coverage

- `**Primary acceptance:**` в design **есть** → не `primary-acceptance-missing` на уровне постановки среза.
- Чеклист не пуст → не `accept-checklist-empty`.
- Сценарий «Смена правила смотрится заново» не покрыт → `accept-bullets-missing-scenario` (WARNING).
- Foreign-scenario в accept: N/A (один срез).

#### 8. Slice Verticality / Acceptance Observability (семантика, без keyword-grep)

Primary и пункты чеклиста описывают **наблюдаемое** поведение прохода проверки для человека: какая карточка вопроса появляется / не появляется, видна ли опора на прошлый контроль в отчёте, сохранён ли ответ в журнале. Это black-box journey оператора набора, не programmatic-only «вызвать функцию / сверить тип».

**Не** `slice-not-vertical`. Срез **не** фундамент без пользовательского исхода: исход — остановка на третьей правке и видимая опора на прошлый контроль.

#### 8b. Self-Achievable Acceptance

Один срез, зависимости нет, нет дубля Primary с `S2`. Наблюдаемый стоп достижим правками заявленных правил набора внутри S1. **Не** `slice-accept-not-self-achievable`. Приёмка своими задачами (когда появятся) структурно достижима.

#### 9. Foundation slice with gate

Нет зависимого `S2` с UX-приёмкой поверх programmatic S1. Условия `slice-foundation-with-gate` не выполнены. S1 сам несёт пользовательский исход (карточка стопа / опора в отчёте).

#### 10. Acceptance Simplicity

В design явно: **«Чеклист приёмки (все три обязательны)»** — три mandatory black-box journey:

1. опора на прошлый контроль среза;
2. узкий повтор после дописки той же темы;
3. стоп на третьей + сохранение ответа.

>1 mandatory journey → **CRITICAL** `acceptance-simplicity-overload`.

#### 11. User Task Contract

Задач `S1.<M>` нет → нарушений контракта в tasks нет. При генерации: runtime-spike пользователю на ИБ не применим; agent-проверки — «по тексту правил / отчёту», observable — в `S1.accept`.

### Alerts

1. **`acceptance-simplicity-overload`** — CRITICAL — S1  
   - **Evidence:** `design.md` ## Slices → «Чеклист приёмки (**все три обязательны**)» с тремя независимыми user-journey.  
   - **Recommendation:** один mandatory Primary (рекомендуется journey стопа на третьей правке — уже в `**Primary acceptance:**`); пункты 1–2 → optional sub-bullets или agent `S1.<M>` «верифицировать по правилам/отчёту».

2. **`accept-bullets-missing-scenario`** — WARNING — Scenario «Смена правила смотрится заново»  
   - **Evidence:** есть в `specs/verify-stop-repeat/spec.md`; отсутствует в «Связь со spec» и в чеклисте S1.  
   - **Recommendation:** добавить в связь со spec; покрыть optional accept («правка меняет формулу/момент файла → полный взгляд») или agent-задачей static по тексту правил.

3. **`slice-gate-pending-tasks`** — SUGGESTION — S1  
   - **Evidence:** нет `tasks.md`, нет `S1.accept` / `<!-- slice-gate -->`.  
   - **Recommendation:** при генерации tasks — ровно один `S1.accept` с mandatory Primary sub-bullet + optional по остальным Scenario + маркер slice-gate.

### Remediation (auto-repair)

```markdown
### Remediation (auto-repair)
- alert: acceptance-simplicity-overload
- target: design.md ## Slices → Срез S1 (затем tasks.md S1.accept)
- action: Оставить единственный mandatory «**Primary (обязательно):**» = текст текущего Primary (стоп на третьей правке без продуктовой карточки). Пункты чеклиста 1 и 2 пометить «(опционально)» или вынести в S1.<M> «верифицировать по правилам/отчёту». Убрать формулировку «все три обязательны».
```

```markdown
### Remediation (auto-repair)
- alert: accept-bullets-missing-scenario
- target: design.md ## Slices → Связь со spec + будущий S1.accept / S1.<M>
- action: Добавить Scenario «Смена правила смотрится заново» в «Связь со spec». Покрыть optional-буллетом accept или задачей S1.<M> static: при смене формулы/момента файла/нового сценария проход полный.
```

```markdown
### Remediation (auto-repair)
- alert: slice-gate-pending-tasks (SUGGESTION)
- target: tasks.md (при создании)
- action: Эмитировать `# Срез S1: …`, metadata с Primary, задачи по файлам правил, ровно один `- [ ] S1.accept …` с Primary + optional, `<!-- slice-gate: … -->`.
```

### Recommendations

**Авто-fix (при правке design / генерации tasks):**

- Свести mandatory accept к одному Primary (стоп на третьей).
- Добавить покрытие «Смена правила смотрится заново».
- Сгенерировать `S1.accept` + slice-gate.

**Decision required:** нет (критерий 8b/9 не сработали; merge срезов не нужен).

### Task readability

`tasks.md` отсутствует — критерии `task-opaque-title` / `task-too-short` не применялись.
