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

4. **Read context files + Architect Gate pre-flight check**

   Read the files listed in `contextFiles` from the apply instructions output.
   The files depend on the schema being used:
   - **spec-driven**: proposal, specs, design, tasks
   - Other schemas: follow the contextFiles from CLI output

   **Pre-flight check (после чтения контекста):**

   **A. Architect Gate (архитектурный подход):**
   - Проверить триггеры из `architect-gate.mdc` по содержимому design.md и наличию reports/
   - Glob `reports/architecture-*.md` в change dir и `temp/reports/`
   - Если триггеры сработали И `architecture-*.md` отсутствует → предупреждение:
     ```
     "Внимание: сработали маркеры архитектурной сложности
     ([перечисление]), но архитектурный анализ не найден.
     Продолжить реализацию? [Да / Запустить архитектора / Вернуться в explore]"
     ```

   **B. Design Review Gate (качество постановки):**
   - Проверить триггеры Design Review из `architect-gate.mdc` (секция DESIGN REVIEW ТРИГГЕРЫ):
     1. Glob `reports/trace-analysis-*.md`, `reports/exploration-*.md` — суммарно ≥ 2?
     2. Grep design.md / proposal.md на маркеры bug fix
     3. Grep design.md / proposal.md на `&ИзменениеИКонтроль`
     4. Grep tasks.md на паттерны ветвления
     5. Grep design.md на hypothesis-маркеры без `## Hypotheses`
   - Glob `reports/design-review-*.md` — ревью уже проводилось?
   - Если триггеры сработали И `design-review-*.md` не найден → мягкое предупреждение:
     ```
     "Дополнительно: сработали маркеры ревью постановки ([перечисление]),
     но ревью не проводилось. Это не блокирует реализацию.
     Запустить ревью? [Да / Нет, продолжить]"
     ```

   Оба check — последний рубеж, если explore и ff пропустили.

5. **Show current progress**

   Display:
   - Schema being used
   - Progress: "N/M tasks complete"
   - Remaining tasks overview
   - Dynamic instruction from CLI

5.5 **Analyze parallelization**

   Before starting implementation, group tasks by file dependencies:
   - Tasks touching different files = independent = can run in parallel
   - Tasks touching the same file = sequential

   Display groups, e.g.:
   - "Parallel group A: tasks 2.3, 3.1, 4.1 (different files)"
   - "Sequential: task 2.1 before 2.2 (same module)"

   Launch up to 3 independent tasks in parallel via Task tool when applicable.

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

   **Task loop:**

   For each pending task:
   - Show which task is being worked on
   - Make the code changes required
   - Keep changes minimal and focused
   - **Spot-check (post-verification):** After the agent reports completion, verify the change: Grep for a pattern that confirms the fix (e.g. after "replace ТекущаяДата with ТекущаяДатаСеанса" → Grep for `ТекущаяДата()` in that file must return 0 matches). For batch tasks (5+ files), spot-check at least 3 files (first, middle, last in the list). If the result does not match expectations → STOP, report to user, do NOT mark task complete.
   - Mark task complete in the tasks file: `- [ ]` → `- [x]`
   - **If this was a verification/decision task** (identified in Conditional Task Detection) → trigger ОБЯЗАТЕЛЬНАЯ ПАУЗА above before proceeding
   - Continue to next task

   **Pause if:**
   - Task is unclear → ask for clarification
   - Implementation reveals a design issue → suggest updating artifacts
   - Error or blocker encountered → report and wait for guidance
   - User interrupts
   - **Verification/decision task completed** → conditional task checkpoint (see above)

7. **On completion or pause, show status**

   Display:
   - Tasks completed this session
   - Overall progress: "N/M tasks complete"
   - If all done: suggest archive
   - If paused: explain why and wait for guidance

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
**Progress:** 7/7 tasks complete ✓

### Completed This Session
- [x] Task 1
- [x] Task 2
...

All tasks complete! Ready to archive this change.
```

**Output On Pause (Issue Encountered)**

```
## Implementation Paused

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 4/7 tasks complete

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

**Fluid Workflow Integration**

This skill supports the "actions on a change" model:

- **Can be invoked anytime**: Before all artifacts are done (if tasks exist), after partial implementation, interleaved with other actions
- **Allows artifact updates**: If implementation reveals design issues, suggest updating artifacts - not phase-locked, work fluidly
