---
name: openspec-apply-change
description: Implement tasks from an OpenSpec change. Use when the user wants to start implementing, continue implementation, or work through tasks.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.1.1"
---

Implement tasks from an OpenSpec change.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If ambiguous, run `openspec list --json` to get available changes and use the **AskUserQuestion tool** to let the user select

   Always announce: "Using change: <name>" and how to override (e.g., `/opsx:apply <other>`).

2. **Check status to understand the schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand:
   - `schemaName`: The workflow being used (e.g., "spec-driven")
   - Which artifact contains the tasks (typically "tasks" for spec-driven, check status for others)

3. **Get apply instructions**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   This returns:
   - Context file paths (varies by schema - could be proposal/specs/design/tasks or spec/tests/implementation/docs)
   - Progress (total, complete, remaining)
   - Task list with status
   - Dynamic instruction based on current state

   **Handle states:**
   - If `state: "blocked"` (missing artifacts): show message, suggest using openspec-continue-change
   - If `state: "all_done"`: congratulate, suggest archive
   - Otherwise: proceed to implementation

4. **Read tasks + minimal context (lazy loading) + verify pre-flight**

   **Mandatory read:** tasks.md (navigation, progress, dependencies) + `openspec/project.md` (project-level constraints: allowed directories, editing rules).
   
   **Lazy reads (по необходимости):**
   - proposal.md — only on first run (for overview), skip on resume
   - design.md — only if current task references an architectural decision
   - specs/ — only when verifying acceptance criteria
   
   Writer subagents receive **paths** to design.md and specs/ in their prompt and read needed sections independently. This keeps orchestrator context lean.

   **Pre-flight: verify check**

   Glob `reports/verification-pre-*.md` or `reports/verification-mixed-*.md` in change dir.
   - **If found** → show summary line from report (first CRITICAL/WARNING counts). Continue.
   - **If NOT found** → soft warning:
     ```
     "Pre-apply verify не проводился. Рекомендуется `/opsx:verify <name>`
     для проверки качества артефактов (формат tasks, gates, конкретность задач).
     [Запустить verify / Продолжить без]"
     ```
     - Option 1 → STOP apply, suggest running `/opsx:verify <name>` first
     - Option 2 → continue implementation

   Verify check is advisory — does not block apply.

5. **Show current progress**

   Display:
   - Schema being used
   - Progress: "N/M tasks complete"
   - **Phase progress (if phase gates detected):** For each phase, show task count and status:
     ```
     Фаза 1: Подготовка — 4/4 done
     Фаза 2: Реализация — 0/5 pending  ← текущая
     Фаза 3: Интеграция — 0/3 pending
     ```
   - Remaining tasks overview
   - Dynamic instruction from CLI
   - **Phase Gate Decisions (if debug.md contains them):** Show previous phase gate decisions from `debug.md` section `## Phase Gate Decisions` — helps orient after session breaks

5.5 **Analyze parallelization (file + phase dependencies)**

   Before starting implementation:

   **Phase-aware ordering:**
   1. Glob `reports/quality-control-*.md` in change dir
   2. If found — read the phase classification table and dependency graph from the most recent report
   3. Group tasks by phase AND file dependencies:
      - **Phase dependencies** (from Quality Controller report): P0 tasks before P1, P1 before P2, P2 before P3, P3 before P4. Tasks in phase P(N) cannot start until their dependencies in P(N-1) are complete.
      - **File dependencies** (existing logic): tasks touching different files within the same phase = independent = can run in parallel; tasks touching the same file = sequential
   4. Display groups with phase annotations:
      - "P0: tasks 1.1, 1.2 (infrastructure, run first)"
      - "P1: task 2.1 (form spec, after P0)"
      - "P2: tasks 2.2-2.5, 3.1-3.2 (implementation, after P1; parallel by file)"
      - "P3: tasks 3.3-3.6 (integration, after P2)"
      - "P4: tasks 4.1-4.4 (verification, last)"

   **If no Quality Controller report found** — fall back to file-only parallelization:
   - Tasks touching different files = independent = can run in parallel
   - Tasks touching the same file = sequential

   **Phase Gate Detection:**
   Grep tasks.md for `<!-- phase-gate` markers.
   If found:
   - Parse phase boundaries (tasks between consecutive markers or between `# Фаза N` headers)
   - Display phase plan:
     "Phase Gates обнаружены. Задачи разбиты на N фаз:
     - Фаза 1 (задачи X.Y–Z.W): <название из заголовка или маркера>
     - --- Phase Gate ---
     - Фаза 2 (задачи ...): ...
     Реализация будет останавливаться на каждом phase gate."
   Ref: `.cursor/rules/phase-gates.mdc`.

   **5.6 Determine execution mode**

   **Step-by-step mode** activates when ANY of:
   - User explicitly requests: «по одной», «step-by-step», «пошагово», «по шагам», «одну задачу»
   - Debug session: debug.md exists AND was modified today (current session is actively debugging)
   - Current batch has P4 (test) tasks intermixed with P2/P3 (implementation) tasks in the execution order

   **Batch mode** (default): current behavior — sequential execution with pauses only on errors/gates/conditionals.

   Announce mode: "Режим: пошаговый (подтверждение после каждой задачи)" or "Режим: последовательный (пауза на gate/ошибке/условии)".

   Launch up to 3 independent tasks in parallel via **Task** tool when applicable. Делегирование субагентам — через инструмент **Task** (см. `.cursor/rules/tool-name-guard.mdc`).

6. **Implement tasks (loop until done or blocked)**

   **Conditional Task Detection (перед началом loop):**
   Просканировать tasks.md на паттерны условного ветвления (ссылки между задачами вида `Если в п.`, `При отрицательн`, `Альтернатив`, `workaround`, `Иначе →`, `Иначе —`).

   Если обнаружены:
   - Идентифицировать **задачу-верификацию** (определяет ветку) и **зависимые задачи-ветки**.
   - После выполнения задачи-верификации — **ОБЯЗАТЕЛЬНАЯ ПАУЗА:**
     ```
     "Задача N (верификация) выполнена. Результат: [краткий итог].
     Следующие задачи зависят от этого результата:
     - Задача X: [при положительном результате]
     - Задача Y: [при отрицательном результате]
     Какую ветку выполнять?"
     ```
   - НЕ выбирать ветку автоматически. Решает пользователь.

   **Task Dispatch (для каждой задачи перед реализацией):**

   Классифицировать задачу по типу и назначить исполнителя:

   | Тип задачи | Маркеры в тексте задачи | Исполнитель |
   |---|---|---|
   | BSL-код (новая логика, правка процедур) | «реализовать», «добавить», «доработать» + путь к .bsl | **onec-code-writer** + **onec-code-reviewer** после |
   | Форма (Form.xml) | «форму», «реквизиты формы», «элементы формы», «Form.xml» | **СТОП.** Инструкция ручного конфигурирования (1c-xml-write-guard.mdc). WAIT — не продолжать до выгрузки |
   | Запрос 1С | «запрос», «оптимизировать запрос» | **onec-query-optimizer** |
   | Верификация метаданных | «проверить соответствие», «проверить наличие» | Оркестратор (Glob/Grep/Read — только проверка, не реализация) |
   | Ручной тест | «ручной тест», «убедиться» | **Step-by-step:** показать сценарий, ждать результат (Пройден/Не пройден/Отложить). **Batch:** пропустить с предупреждением; включить в Session Summary секцию "Отложенные ручные тесты" |
   | Создание метаданных | «создать регистр», «создать справочник», «создать форму» (scaffold) | **СТОП** — блокер пользователю (`1c-no-metadata-creation.mdc`) |

   **HALT:** Оркестратор НЕ реализует задачи типов BSL-код и Форма самостоятельно. Оркестратор готовит промпт и делегирует. Прямое использование Write/StrReplace для .bsl, **прямая правка Form.xml** и прямая генерация JSON-спецификаций форм для form-compile — запрещены. Для форм: СТОП — сформировать инструкцию ручного конфигурирования (1c-xml-write-guard.mdc); не продолжать до выгрузки пользователем. Ref: `1c-agent-delegation.mdc`, `1c-utility-agents.mdc`.

   **Investigation Loop при apply.** Если reviewer в отчёте включил секцию `## Investigation Request`:
   1. Вызвать explorer (contract resolution deep) по таблице из Investigation Request. Шаблон: «Explorer — contract resolution (deep)» из `1c-agent-patterns/SKILL.md`.
   2. Сохранить вывод в `reports/resolved-contract-<slug>-YYYY-MM-DD.md` (артифакт ЗНИ).
   3. Повторно вызвать reviewer с Resolved Contracts в промпте.
   4. При последующем устранении замечаний — передать Resolved Contracts в промпт writer.
   Протокол: см. `1c-agent-delegation.mdc`, секция CONTRACT RESOLUTION; шаблоны: `1c-agent-patterns/SKILL.md`.

   **Task loop:**

   For each pending task:
   - **Phase Gate check:** If this task is the first task after a `<!-- phase-gate -->` marker (i.e. all tasks before the gate are [x]), trigger ОБЯЗАТЕЛЬНАЯ ПАУЗА:
     ```
     === Phase Gate ===
     Фаза N завершена. K/M задач выполнено.
     Критерий приёмки фазы: <текст из phase-gate маркера>

     Задачи следующей фазы:
     - N+1.1: <краткое описание>
     - N+1.2: ...

     [1. Продолжить к следующей фазе]
     [2. Запустить phase-transition verify (рекомендуется)]
     [3. Пересмотреть задачи следующей фазы]
     [4. Стоп]
     ```
     - Option 1 → continue to next task
     - Option 2 → suggest `/opsx:verify <name>` in phase-transition mode; STOP apply until user has run verify and confirms resume
     - Option 3 → **Post-architect task restructuring flow:**
       1. Delegate to **onec-code-architect** with prompt from `1c-agent-patterns/SKILL.md` "Architect — phase transition review": пересмотреть задачи следующей фазы с учётом реализации текущей; передать путь к debug.md и reports/.
       2. Architect returns: recommendations + full text of updated task sections for the next phase.
       3. Show user a summary of changes: which tasks added/removed/modified, what rationale.
       4. AskQuestion: "Применить изменения к tasks.md? [Да / Нет / Скорректировать]"
       5. On "Да" → apply changes to tasks.md via StrReplace (preserve `[x]` status of completed tasks, new tasks get `[ ]`). Re-read tasks.md. Recalculate phase progress.
       6. On "Нет" → keep original tasks, continue to Phase Gate log.
       7. On "Скорректировать" → ask user for specific corrections, apply, re-read.
       8. After tasks update: AskQuestion "Продолжить apply?"
     - Option 4 → STOP apply
   - **Phase Gate log (mandatory for all options):** After the user's decision at a phase gate, append a record to `debug.md` (create section `## Phase Gate Decisions` if absent):
     ```
     ### Phase Gate N (YYYY-MM-DD)
     Фаза: N — <phase name>
     Решение: <продолжить / пересмотр / verify / стоп>
     Обоснование: <user's rationale or "без замечаний">
     Изменения tasks: <"нет" / "N задач добавлено, M удалено, K переформулировано">
     ```
   - Show which task is being worked on
   - **Classify** (Task Dispatch table above) — announce type and executor
   - **Delegate** to the designated executor (agent or skill)
   - Orchestrator role: prepare prompt with context, delegate, spot-check result
   - **Spot-check (post-verification):** After the agent reports completion, verify the change: Grep for a pattern that confirms the fix (e.g. after "replace ТекущаяДата with ТекущаяДатаСеанса" → Grep for `ТекущаяДата()` in that file must return 0 matches). For batch tasks (5+ files), spot-check at least 3 files (first, middle, last in the list). If the result does not match expectations → STOP, report to user, do NOT mark task complete.
   - Mark task complete in the tasks file: `- [ ]` → `- [x]`
   - **Step-by-step checkpoint (if step-by-step mode):** After marking task complete, ОБЯЗАТЕЛЬНАЯ ПАУЗА. For **code/form tasks** (completed by agent): show "Задача N.M выполнена", "Что изменено" (path, строки, описание), "Что проверить" (из критериев приёмки). Options: [Подтвердить / Проблема / Пропустить]. Подтвердить → proceed; Проблема → user describes issue, create follow-up task in tasks.md (phase-gates.mdc for phased insertion), do NOT proceed until resolved or "Пропустить"; Пропустить → proceed, add "(не проверено пользователем)" note, include in Session Summary as unverified. For **manual test tasks** (P4): show "Задача N.M — ручной тест (ваше действие)", "Сценарий" (шаги из задачи), "Зависимости: M.K [x], M.L [x]" or "M.K [ ] — НЕ выполнена". Options: [Тест пройден / Тест не пройден / Отложить]. Тест пройден → mark [x]; Тест не пройден → debug flow (tasks.md or debug.md); Отложить → leave [ ], proceed.
   - **If this was a verification/decision task** (identified in Conditional Task Detection) → trigger ОБЯЗАТЕЛЬНАЯ ПАУЗА above before proceeding
   - Continue to next task

   **Pause if:**
   - **Step-by-step mode:** after every task completion (step-by-step checkpoint above)
   - Task is unclear → ask for clarification
   - Implementation reveals a design issue → suggest updating artifacts
   - Error or blocker encountered → report and wait for guidance
   - User interrupts
   - **Verification/decision task completed** → conditional task checkpoint (see above)
   - **Phase Gate reached** → before first task of next phase (see Phase Gate check above)

7. **On completion or pause — Session Handoff Summary**

   Generate three-section summary:

   **Section 1 — "Выполнено агентами":**
   For each task completed this session:
   - [x] N.M — краткое описание
     - Файл: `path`, строки X-Y
     - Что изменено: одно предложение (было → стало)
     - Авто-проверка: результат spot-check (OK / расхождение)

   **Section 2 — "Что проверить СЕЙЧАС":**
   For each completed task that has acceptance criteria with user-facing actions (markers: `убедиться`, `проверить`, `критерий приёмки`, `Критерий приёмки`):
   - Extract the acceptance criteria from the task description
   - Rewrite as concrete user steps (imperative mood): 1. Открыть ... → Выполнить ... → Ожидаемый результат: ...
   - If task type was "Ручной тест" (dispatched as manual) — include the full test scenario with expected results

   If no acceptance criteria require user action → "Ручная проверка не требуется для задач этого сеанса."

   **Section 3 — "Следующие задачи":**
   | Задача | Тип | Исполнитель | Зависит от | Статус зависимости |
   Show only the next 3-5 tasks. For each: Type (BSL / Form / Manual test / Metadata / etc.), Executor (agent / user), Dependencies and their status ([x] / [ ]). If dependency is [ ] → flag "невыполнима до N.M"

   **Blockers (if any):**
   List tasks that cannot proceed and why.

   If all done: suggest archive. If paused: explain why and wait for guidance.

**Output During Implementation**

```
## Implementing: <change-name> (schema: <schema-name>)

Working on task 3/7: <task description>
[...implementation happening...]
✓ Task complete

Working on task 4/7: <task description>
[...implementation happening...]
✓ Task complete
```

**Output On Completion**

```
## Implementation Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** N/M tasks complete ✓

### 1. Выполнено агентами
- [x] N.M — <краткое описание>
  - Файл: `path`, строки X-Y
  - Что изменено: <одно предложение>
  - Авто-проверка: OK / расхождение

### 2. Что проверить СЕЙЧАС
1. <конкретный шаг из критериев приёмки> → Ожидаемый результат: ...
(или: Ручная проверка не требуется для задач этого сеанса.)

### 3. Следующие задачи
| Задача | Тип | Исполнитель | Зависит от | Статус |
|--------|-----|-------------|------------|--------|
| ...    | ... | ...         | ...        | [x]/[ ] |

### Blockers (если есть)
<список>

All tasks complete! Ready to archive this change.
```

**Output On Pause (Issue Encountered)**

```
## Implementation Paused

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** N/M tasks complete

### 1. Выполнено агентами (этот сеанс)
<как в Output On Completion>

### 2. Что проверить СЕЙЧАС
<шаги для пользователя>

### 3. Следующие задачи
<таблица>

### Issue Encountered
<description of the issue>

**Options:**
1. <option 1>
2. <option 2>
3. Other approach

What would you like to do?
```

**Guardrails**
- Keep going through tasks until done or blocked
- Always read context files before starting (from the apply instructions output)
- **Spot-check after each task:** Grep (or Read) to confirm the change; for 5+ files, check at least 3. Do not mark task complete if verification fails.
- If task is ambiguous, pause and ask before implementing
- If implementation reveals issues, pause and suggest artifact updates
- Keep code changes minimal and scoped to each task
- Update task checkbox immediately after completing each task
- Pause on errors, blockers, or unclear requirements - don't guess
- Use contextFiles from CLI output, don't assume specific file names
- **Task Dispatch:** classify each task before implementation; delegate to the correct executor per dispatch table. Orchestrator MUST NOT implement BSL or Form tasks directly — only prepare context and delegate.
- **Form tasks:** STOP — produce manual configuration instructions (1c-xml-write-guard.mdc); do not edit Form.xml or continue until user has performed configuration and re-exported.
- Reference: `1c-agent-delegation.mdc` (BSL gate), `1c-utility-agents.mdc` (forms, queries, tests).

**Fluid Workflow Integration**

This skill supports the "actions on a change" model:

- **Can be invoked anytime**: Before all artifacts are done (if tasks exist), after partial implementation, interleaved with other actions
- **Allows artifact updates**: If implementation reveals design issues, suggest updating artifacts - not phase-locked, work fluidly
