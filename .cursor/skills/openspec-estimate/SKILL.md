---
name: openspec-estimate
description: Estimate man-hours for an OpenSpec change using three-point PERT method. Auto-detects mode (initial estimate, re-estimate, calibration). Use when the user wants to evaluate effort for a change.
license: MIT
compatibility: Requires openspec CLI and tasks.md artifact.
metadata:
  author: openspec
  version: "1.0"
---

Estimate man-hours for an OpenSpec change. Method: three-point PERT. Target: human 1C developer effort (not AI).

**Input**: Change name (kebab-case), any search context (path, module name, keyword), or omit to auto-detect.

## Steps

### 1. Select the change

Resolution paths, checked in order:

#### 1a. Direct change name

If input exactly matches a directory in `openspec/changes/<input>/` or `openspec/changes/archive/<input>/` — use it directly.

#### 1b. Contextual search (input provided, but not a direct change name)

The input can be anything: a path (`src\ДО3\cfe\pav_ИсключениеУчастниковПоУсловию`), a module name (`ДействияСервер`), a keyword (`исключение участников`), an extension name, etc.

**Build search terms:** extract meaningful keywords from the input. If the input is a path — use the last segment and its recognizable fragments. Otherwise use the input as-is.

**Search for related changes:**

1. Glob `openspec/changes/*/tasks.md` (active) + `openspec/changes/archive/*/tasks.md` (archived).
2. For each found change directory — Grep `proposal.md` and `tasks.md` for the search terms. A match in either file counts.
3. Collect results: change name, location (active / archive), one-line summary (first sentence from `## Why` in proposal.md).

**Present results:**

- **0 found** — "ЗНИ не найдены по запросу `<input>`. Создать: `/opsx:ff <change-name>`."
- **1 found** — announce and continue with standard flow (step 2).
- **N found** — display table and **AskQuestion** "Какие ЗНИ оценить?":
  - **Все** — batch mode (step 1c)
  - **Выбрать** — user specifies numbers from the table
  - A specific change name

Table format:

```
| # | Change | Статус | Описание |
|---|--------|--------|----------|
| 1 | pav-exclusion-bp-sync | archive | Синхронизация БП Согласование с действием... |
| 2 | ... | ... | ... |
```

#### 1c. Batch mode (multiple changes selected)

When user selects "Все" or multiple changes:

1. For each selected change — run steps 2–7 sequentially (determine mode, classify, calculate, generate estimate.md).
2. After all individual estimates are done — display a **summary table** (chat only, not saved to file):

```
| Change | PERT | Итого (с буфером) |
|---|---|---|
| pav-exclusion-bp-sync | 12.3 ч/ч | 14.1 ч/ч |
| ... | ... | ... |
| **Итого** | **X.X ч/ч** | **Y.Y ч/ч** |
```

3. Skip step 7a (per-change "Скорректировать?") in batch mode — ask once at the end for the batch as a whole.
4. **End.** Do not proceed to step 8 (calibration) in batch mode.

#### 1d. Auto-detect

If no input provided:
- Infer from conversation context if the user mentioned a change
- Auto-select if only one active change exists
- If multiple active changes: run `openspec list --json`, show options, use **AskQuestion** to let user select

Always announce: "Оценка трудозатрат: <name>".

### 2. Determine mode

Check the change directory for existing artifacts:

1. Read `tasks.md` from change directory. If **not found** — STOP: "Для оценки необходим артефакт tasks.md. Создайте его: `/opsx:new <name>` или `/opsx:ff <name>`."
2. Check if `estimate.md` exists in the change directory (Glob).

**Decision tree:**

| estimate.md exists? | All tasks completed? | Mode |
|---|---|---|
| No | — | **Initial Estimate** (step 3) |
| Yes | No (`[ ]` found in tasks.md) | **Re-estimate** (step 3, with diff) |
| Yes | Yes (all `[x]`, no `[ ]`) | **Calibration** (step 8) |

"All tasks completed" = every checkbox in tasks.md is `[x]`, no `[ ]` remains.

Announce the mode to the user.

### 3. Load artifacts

- **Required**: `tasks.md`
- **Context**: `proposal.md`, `design.md` (read if present, for understanding complexity)
- For **re-estimate**: also read existing `estimate.md` to compute diff later

### 4. Classify each task

For every task item in tasks.md (lines matching `- [ ]` or `- [x]` with a task number like `1.1`, `2.3`, etc.), determine:

- **Activity type**: one of the types from the Reference Rates table (step 5)
- **Complexity**: Простая / Средняя / Сложная

**Classification criteria:**

#### Activity types

| Type | Trigger keywords / patterns in task |
|---|---|
| Кодирование | File path to `.bsl`, "реализовать", "создать процедуру/функцию", "добавить", "изменить", правка кода |
| Анализ | "аудит", "обследование", "зафиксировать", "маппинг", "верификация API", "трассировка" |
| Тестирование | Section "Ручная верификация", "сценарий проверки", "проверить", "убедиться" |
| Ревью | "onec-code-reviewer", "ревью", "code review" |
| Проектирование | "архитектура", "контракт", "Decision", design decisions |

Each task has **exactly one type**. When mixed — pick the dominant activity (>50% of effort).

#### Complexity

| Level | Criteria |
|---|---|
| Простая | 1 procedure/function, clear pattern to follow, no dependencies on other tasks, mechanical change (rename, delete, add guard) |
| Средняя | 1 module, non-trivial logic (loop refactoring, condition restructuring), dependencies on other tasks, moderate business logic |
| Сложная | Multiple modules, integration points, &ИзменениеИКонтроль, side effects on other subsystems, complex business process logic, contract design |

#### Examples from real tasks

| Task description | Type | Complexity | Rationale |
|---|---|---|---|
| "убрать или перевести на Отладка вызов ЗаписьЖурналаРегистрации" | Кодирование | Простая | 1 line, 1 procedure, clear pattern |
| "вынести ЗаписьЖурналаРегистрации из цикла: один вызов после цикла с агрегированным сообщением" | Кодирование | Средняя | Refactoring within module, aggregation logic |
| "Создать экспортную процедуру pavIU_СинхронизироватьБПСогласованияПоДействию" with 7-step algorithm, multiple API calls, comparison logic | Кодирование | Сложная | Multiple APIs, integration with BP, side effects |
| "Аудит CommonModules/ДействияСервер — маппинг процедур против целевой архитектуры" | Анализ | Средняя | One module, but requires understanding architecture |
| "Единая функция получения предмета для проверки условия (Decision 2)" | Кодирование | Средняя | One function, but requires verification of all call sites |
| "Добавить &После("ПриЗаписи") процедуру с 3 ранними возвратами и одним вызовом" | Кодирование | Простая | Thin wrapper, no business logic |
| "Code review изменений (onec-code-reviewer)" | Ревью | — | Complexity N/A for reviews (flat rate per module) |
| "Финальное ревью расширения целиком" | Ревью | — | Rate multiplied by module count |
| "переименовать процедуру, обновить вызов" | Кодирование | Простая | Mechanical find-replace |
| "Реализовать пересчёт пав_Исключен действия и запись при изменении" across 3 files with flags and anti-recursion | Кодирование | Сложная | Multiple files, flags, anti-recursion contract |

### 5. Reference rates (built-in defaults)

PERT formula: **E = (O + 4M + P) / 6**

Where O = optimistic, M = most likely, P = pessimistic (all in man-hours).

#### Кодирование

| Complexity | O | M | P |
|---|---|---|---|
| Простая | 0.5 | 1 | 2 |
| Средняя | 1.5 | 3 | 5 |
| Сложная | 3 | 6 | 10 |

#### Анализ / Обследование

| Complexity | O | M | P |
|---|---|---|---|
| Простая | 0.5 | 1 | 2 |
| Средняя | 1 | 2 | 4 |
| Сложная | 2 | 4 | 8 |

#### Тестирование (per scenario)

| O | M | P |
|---|---|---|
| 0.3 | 0.75 | 1.5 |

#### Ревью (per module)

| O | M | P |
|---|---|---|
| 0.5 | 1 | 1.5 |

#### Проектирование

| Complexity | O | M | P |
|---|---|---|---|
| Средняя | 1 | 2 | 4 |
| Сложная | 2 | 4 | 8 |

#### Buffer

**15%** of total PERT. Rationale: standard contingency for well-decomposed tasks with known technology stack. Covers minor unknowns (environment issues, merge conflicts, minor scope clarifications).

#### Rate override

If `openspec/estimate-rates.md` exists — read it and use its values **instead of** the built-in defaults above. The file must follow the same table format (Type / Complexity / O / M / P). If the override file is malformed or incomplete, fall back to built-in rates for missing entries and warn.

### 6. Calculate

For each classified task:
1. Look up O, M, P from rates by (type, complexity)
2. Compute PERT = (O + 4×M + P) / 6, round to 1 decimal place
3. Sum all O values → Total O
4. Sum all PERT values → Total PERT
5. Sum all P values → Total P
6. Buffer = Total PERT × buffer% (round to 1 decimal)
7. Grand Total = Total PERT + Buffer (round to 1 decimal)

### 7. Generate estimate.md

Save to the change directory: `openspec/changes/<name>/estimate.md` for active changes, `openspec/changes/archive/<name>/estimate.md` for archived ones. Always use the actual path resolved in step 1.

Format:

```markdown
# Оценка трудозатрат: <change-name>

Дата оценки: YYYY-MM-DD
Метод: трёхточечная PERT

## Сводка

| Показатель | Значение |
|---|---|
| Оптимистичная (О) | X.X ч/ч |
| PERT (взвешенная) | Y.Y ч/ч |
| Пессимистичная (П) | Z.Z ч/ч |
| Буфер | N% (B.B ч/ч) |
| **Итого (PERT + буфер)** | **W.W ч/ч** |

## Детализация

| # | Задача | Тип | Сложность | Оптим. | Вероятн. | Пессим. | PERT |
|---|---|---|---|---|---|---|---|
| 1.1 | Описание задачи | Кодирование | Средняя | 1.5 | 3.0 | 5.0 | 3.2 |
| ... | ... | ... | ... | ... | ... | ... | ... |
| | **Итого** | | | X.X | | Z.Z | Y.Y |

## Допущения

(Generate from change context — do NOT hardcode. Examples of what to include:)
- Assumptions about developer familiarity with the domain
- Assumptions about environment availability
- Assumptions about dependency availability (base module APIs, etc.)
- Whether tasks include code review iterations

## Риски, влияющие на оценку

(Generate from change context. Examples:)
- Complexity of base module integration not fully known
- Potential need for additional research
- Dependency on tasks not yet completed
```

**For re-estimate mode**: before overwriting estimate.md, read the previous totals and append a `## История оценок` section:

```markdown
## История оценок

| Дата | PERT | Итого | Причина переоценки |
|---|---|---|---|
| YYYY-MM-DD | Y1 ч/ч | W1 ч/ч | Первичная оценка |
| YYYY-MM-DD | Y2 ч/ч | W2 ч/ч | Изменение tasks.md |
```

If the previous estimate already had a history section, preserve all rows and append the new one.

### 7a. Present to user

Show the summary table and grand total. Then:

**AskQuestion**: "Скорректировать оценку?" with options:
- **Принять** — keep as is
- **Скорректировать** — user provides feedback, adjust classification or override specific task estimates, regenerate

### 8. Calibration mode

Entered automatically when estimate.md exists and all tasks in tasks.md are completed.

1. Read existing estimate.md, extract PERT total and Grand Total.
2. Show to user:
   ```
   Оценка PERT: Y.Y ч/ч (итого с буфером: W.W ч/ч)
   Все задачи выполнены.
   ```
3. **AskQuestion**: "Укажите фактические трудозатраты для калибровки (ч/ч)" with options:
   - Specific values (text input)
   - **Пропустить** — exit without calibration
4. If user provides actual hours:
   - Compute deviation: `(actual - PERT) / PERT × 100%`
   - Append `## Факт` section to estimate.md:

   ```markdown
   ## Факт

   | Показатель | Значение |
   |---|---|
   | Фактические трудозатраты | F.F ч/ч |
   | Отклонение от PERT | +/-N.N% |
   | Дата фиксации | YYYY-MM-DD |
   ```

   - If deviation > 30% (absolute value): advise user:
     "Отклонение значительное (N%). Рекомендую скорректировать ставки — создайте `openspec/estimate-rates.md` на основе встроенных ставок и подстройте значения."
   - If deviation <= 30%: "Отклонение в пределах нормы. Ставки адекватны."
5. If user skips — exit with message: "Калибровка пропущена. Можно вернуться позже: `/opsx:estimate <name>`."

## Constraints

- **tasks.md is required.** No estimation without task decomposition.
- **One type per task.** No splitting a single task line into multiple activity types.
- **Rates are guidelines.** The model may adjust O/M/P for a specific task if the task description clearly warrants it (e.g., a "simple" coding task that touches a very large file), but must document the override in the Допущения section.
- **No automatic rate adjustment.** Calibration only advises; rates are the user's responsibility.
- **estimate.md is not an OpenSpec schema artifact.** It lives in the change directory alongside other files but is not tracked by `openspec status`.
