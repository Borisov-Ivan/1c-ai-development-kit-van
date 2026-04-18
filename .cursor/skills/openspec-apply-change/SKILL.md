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

5. **Resume with pending verdict & Show current progress**

   **Resume with pending verdict (FIRST ACTION, before any work):**

   1. Grep последнюю запись в `debug.md` `## Slice Gate Decisions` для каждого среза.
   2. Найти самую раннюю по порядку запись с `Решение: awaiting-acceptance`, где:
      - все non-test задачи среза S<N> = [x],
      - S<N>.T<M> = [ ].
   3. Если найдено — НИЧЕГО не реализовывать, сразу AskQuestion:

      Slice Gate S<N> — <имя> — ожидает вердикта

      Ты вернулся с проверки. Что по результату прогона S<N>.T<M>?

      [1] Принят — отметить S<N>.T<M> [x], перейти к S<N+1>
      [2] Не принят — опишу что не работает, rework внутри S<N>
      [3] Дефект в предыдущем срезе S<K> — создать мини-срез S<K>.fix

   4. По ответу:
      - [1] → mark [x], append debug.md "решение: принят", сгенерировать reports/slice-acceptance-S<N>-YYYY-MM-DD.md, перейти к задачам S<N+1>.
      - [2] → запросить описание проблемы; append debug.md "решение: не принят" + секция ## Debug — S<N>; создать fix-задачи перед S<N>.T<M>; начать их выполнение.
      - [3] → запросить описание дефекта; создать S<K>.fix срез (по правилу vertical-slices.mdc); снять [x] с S<K>.T<M>.

   5. Если awaiting-acceptance не обнаружено — перейти к обычному "Show current progress" ниже.

   **Show current progress:**

   Display:
   - Schema being used
   - Progress: "N/M tasks complete"
   - **Slice progress (if slices detected):** For each slice, show task count and acceptance status:
     ```
     Срез S1: Флажок в шаблоне — 3/3 done, S1.T1 [x] ПРИНЯТ
     Срез S2: Копирование флага в БП — 2/4 done, S2.T1 [ ]  ← текущий
     Срез S3: Индикатор на форме параметров — 0/3 pending
     ```
   - Remaining tasks overview
   - Dynamic instruction from CLI
   - **Slice Gate Decisions (if debug.md contains them):** Show previous slice gate decisions from `debug.md` section `## Slice Gate Decisions` — helps orient after session breaks

5.5 **Analyze parallelization (slices + file dependencies)**

   Before starting implementation:

   **Slice-aware ordering:**
   1. Grep `tasks.md` for `^# Срез S\d+` — if found, ЗНИ is in **slice mode** (default).
   2. Read slice metadata blocks (Сценарий, Приёмка, Связь со spec, Зависимости) for each slice.
   3. Glob `reports/quality-control-*.md` in change dir — if found, use slice dependency graph and coverage matrix from it.
   4. Order slices by dependency graph: S<N> can start only when all slices in `**Зависимости:**` have `S<K>.T<M>` = `[x]`.
   5. Within a slice, group tasks by layer/file:
      - Tasks touching different files = independent = can run in parallel (up to 3 concurrent via Task tool).
      - Tasks touching the same file = sequential.
      - Layer ordering inside slice is guidance only (метаданные → форма → код → приёмка); enforce via task-level dependency graph from tasks.md.
   6. Display plan:
     ```
     Срезы для выполнения:
     - S1: Флажок в шаблоне (3 задачи + S1.T1)
     - --- Slice Gate S1 ---
     - S2: Копирование флага в БП (4 задачи + S2.T1), зависит от S1
     - --- Slice Gate S2 ---
     - S3: ...
     Реализация будет останавливаться на каждом slice gate для приёмки.
     ```
   Ref: `.cursor/rules/vertical-slices.mdc`.

   **Legacy mode (no slices in tasks.md):**
   - Warn: "ЗНИ без срезов. Рекомендуется `/opsx:verify <name> --migrate-to-slices` перед продолжением."
   - AskQuestion: `[Продолжить без срезов] / [Мигрировать на срезы (verify)] / [Стоп]`.
   - `Продолжить` → fall back to file-only parallelization (tasks touching different files = independent; same file = sequential). Нет slice-gate пауз.
   - `Мигрировать` → STOP apply, предложить запустить `/opsx:verify <name> --migrate-to-slices`.
   - `Стоп` → завершить apply.

   **5.6 Determine execution mode**

   **Step-by-slice mode** (DEFAULT for slice mode):
   - Выполнять задачи одного среза подряд (параллелизация по файлам внутри среза допустима).
   - После последней non-test задачи среза — ОБЯЗАТЕЛЬНАЯ ПАУЗА на slice-gate (карточка приёмки, см. шаг 6).
   - Не начинать следующий срез до принятия (или явного пропуска) текущего.

   **Step-by-step mode** — более жёсткий режим, активируется когда:
   - User explicitly requests: «по одной», «step-by-step», «пошагово», «по шагам», «одну задачу».
   - Debug session: debug.md exists AND was modified today (current session is actively debugging).
   - В режиме step-by-step — пауза также после КАЖДОЙ завершённой задачи (не только на slice-gate).

   **Batch mode** активируется ТОЛЬКО в legacy mode (без срезов) и по явному запросу пользователя — sequential execution с паузами только на ошибках/условных задачах.

   Announce mode: "Режим: step-by-slice (пауза на каждом slice-gate)" / "Режим: step-by-step (пауза после каждой задачи и на slice-gate)" / "Режим: batch/legacy (пауза только на ошибках)".

   Launch up to 3 independent tasks in parallel via **Task** tool when applicable внутри одного среза. Делегирование субагентам — через инструмент **Task** (см. `.cursor/rules/tool-name-guard.mdc`).

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
   | Верификация метаданных | «проверить соответствие», «проверить наличие» | Оркестратор (Glob/Grep/Read — только проверка, не реализация) |
   | Приёмочный тест (`S<N>.T<M>`) или ручной тест | «ручной тест», «убедиться», `S<N>.T<M>` | **Step-by-slice / step-by-step:** trigger Slice Gate (см. шаг 6). **Legacy batch:** пропустить с предупреждением; включить в Session Summary секцию "Отложенные ручные тесты" |
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
   - **Slice Gate (после последней non-test задачи среза):**
     Детектор: все задачи S<N>.<M> = [x], S<N>.T<M> = [ ].

     Действие — сгенерировать Acceptance Handoff Card (НЕ вызывать AskQuestion):

     ```
     === Acceptance Handoff — S<N>: <имя среза> ===

     Что реализовано:
     - Задачи: N/N non-test done (S<N>.1, S<N>.2, ..., всё [x])
     - Файлы: <список с краткой пометкой "что изменилось">
     - Автопроверки: линтер чист / reviewer PASS (или замечания перечислить)

     Что я прошу проверить — СЦЕНАРИЙ S<N>.T<M>:
     <переписать критерии приёмки из S<N>.T<M> в императиве, по пунктам>
     1. Открыть <что>
     2. Выполнить <действие>
     3. Убедиться <ожидаемый результат>
     (R1/R2/R3 или другие ссылки — развернуть человечески)

     Как вернуться:
       /opsx:apply <change-name>
     В начале новой сессии я сразу спрошу вердикт (принят / не принят / дефект в предыдущем срезе).
     Пока ты проверяешь — я ничего не делаю.

     Если сейчас уже всё проверено и принято — напиши "принято S<N>" / "accept S<N>", я отмечу без handoff.
     ```

     Параллельно:
     1. Append в `debug.md` `## Slice Gate Decisions`:
        ```markdown
        ### Slice S<N> — <имя> (YYYY-MM-DD)
        Срез: S<N> — <имя>
        Решение: awaiting-acceptance
        Обоснование: все non-test задачи реализованы и прошли автопроверки; приёмочный тест S<N>.T<M> передан пользователю на ручной прогон.
        Изменения tasks: нет (S<N>.T<M> остаётся [ ])
        Связанный отчёт: —
        ```
     2. Session Handoff Summary по шаблону шага 7 — но с заголовком "## Paused for Acceptance — S<N>". Секция "Что проверить СЕЙЧАС" заполняется сценарием из S<N>.T<M> (та же информация, что в Acceptance Handoff Card).
     3. Завершить сессию.
   - **Manual acceptance shortcut:**
     Если пользователь в любой момент сессии явно говорит "принято S<N>" / "accept S<N>" / "S<N> принят" (для среза, у которого все non-test задачи [x] и T<M> [ ]):
     1. Не генерировать Acceptance Handoff Card.
     2. Отметить S<N>.T<M> = [x].
     3. Append в debug.md "решение: принят (manual shortcut)".
     4. Continue к S<N+1>.

   - **Ранний выход ("стоп" в любой момент):**
     Пользователь явно: "стоп" / "stop" / "прекрати" / "прерви" / "пока хватит".
     1. Завершить текущий task/subagent.
     2. Append debug.md "решение: стоп" (если прерван на Slice Gate) или просто запись в debug.md секции "Interrupted sessions" (если в середине).
     3. Session Handoff Summary.
     4. Завершить apply.

   - **Slice Gate log (mandatory for all options):** After the user's decision at a slice gate, append a record to `debug.md` (create section `## Slice Gate Decisions` if absent):
     ```
     ### Slice S<N> — <имя> (YYYY-MM-DD)
     Срез: S<N> — <slice name>
     Решение: awaiting-acceptance / принят / принят (manual shortcut) / не принят / fix предыдущего S<K> / стоп
     Обоснование: <user's rationale or "без замечаний">
     Изменения tasks: <"нет" / "N задач добавлено" / "создан S<K>.fix">
     Связанный отчёт: reports/slice-acceptance-S<N>-YYYY-MM-DD.md (если принят)
     ```
   - Show which task is being worked on
   - **Classify** (Task Dispatch table above) — announce type and executor
   - **Delegate** to the designated executor (agent or skill)
   - Orchestrator role: prepare prompt with context, delegate, spot-check result
   - **Spot-check (post-verification):** After the agent reports completion, verify the change: Grep for a pattern that confirms the fix (e.g. after "replace ТекущаяДата with ТекущаяДатаСеанса" → Grep for `ТекущаяДата()` in that file must return 0 matches). For batch tasks (5+ files), spot-check at least 3 files (first, middle, last in the list). If the result does not match expectations → STOP, report to user, do NOT mark task complete.
   - Mark task complete in the tasks file: `- [ ]` → `- [x]`
   - **Step-by-step checkpoint (if step-by-step mode):** After marking task complete, ОБЯЗАТЕЛЬНАЯ ПАУЗА. For **code/form tasks** (completed by agent): show "Задача S<N>.<M> выполнена", "Что изменено" (path, строки, описание), "Что проверить" (из критериев приёмки). Options: [Подтвердить / Проблема / Пропустить]. Подтвердить → proceed; Проблема → user describes issue, create follow-up task in the same slice (before `S<N>.T<M>`), do NOT proceed until resolved or "Пропустить"; Пропустить → proceed, add "(не проверено пользователем)" note, include in Session Summary as unverified. For **acceptance tasks** (`S<N>.T<M>`): show "Срез S<N>.T<M> — ручной тест (ваше действие)", "Сценарий" (шаги из задачи), "Зависимости: S<N>.<M> [x]...". Options: [Тест пройден → Slice Gate [1] / Тест не пройден → Slice Gate [2] / Отложить]. Это эквивалент Slice Gate; шаги описаны выше.
   - **If this was a verification/decision task** (identified in Conditional Task Detection) → trigger ОБЯЗАТЕЛЬНАЯ ПАУЗА above before proceeding
   - Continue to next task

   **Pause if:**
   - **Slice Gate reached** (все non-test задачи среза `[x]`, остался только `S<N>.T<M>` или первый task следующего среза) — ОБЯЗАТЕЛЬНАЯ карточка приёмки (см. Slice Gate check выше)
   - **Step-by-step mode:** after every task completion (step-by-step checkpoint above)
   - Task is unclear → ask for clarification
   - Implementation reveals a design issue → suggest updating artifacts
   - Error or blocker encountered → report and wait for guidance
   - User interrupts
   - **Verification/decision task completed** → conditional task checkpoint (see above)

7. **On completion or pause — Session Handoff Summary**

   Generate three-section summary with one of the following headers based on context:
   - `## Paused for Acceptance — S<N>` (handoff в конце среза, default)
   - `## Stopped — <причина>` (пользовательский стоп)
   - `## Implementation Complete` (все срезы приняты)

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
