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

2. **Check status to understand the schema and verify Metadata**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand:
   - `schemaName`: The workflow being used (e.g., "spec-driven")
   - Which artifact contains the tasks (typically "tasks" for spec-driven, check status for others)

   **Metadata Prep (MANDATORY):** Before writing any code, check `proposal.md` for comment marker placeholders:
   - Read or Grep `openspec/changes/<name>/proposal.md` for `<developer>`, `<zni_id>`, «Уточнить до `/opsx:apply`» or «Уточнить».
   - If any placeholders are found, STOP and use **AskQuestion** to request the missing developer/zni_id.
   - Replace the placeholders in `proposal.md` with the user's answers.
   - If `tasks.md` has an `F1` Follow-up task for this, mark it as completed.

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

   **Pre-flight: verify check & Metadata**

   Glob в change dir (любой из):
   - `reports/verification-slice-pre-*.md`
   - `reports/verification-legacy-pre-*.md`
   - `reports/verification-legacy-mixed-*.md`

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

   **Metadata (comment markers) check:**
   Прочитать `proposal.md`. Найти секцию `## Metadata (comment markers)`.
   - Если секция есть — извлечь `developer`, `zni_id`, `zni_name`. Сформировать строки:
     `open_marker` = `// +++ {developer} {date} {zni_name} [{zni_id}]` (где date — текущая дата `dd.MM.yyyy`)
     `close_marker` = `// --- {developer} [{zni_id}]`
   - Если секции нет — **AskQuestion**:
     ```
     В proposal.md отсутствует блок Metadata для маркеров комментариев.
     Укажите:
     1. Разработчик (ФИО):
     2. Идентификатор ЗНИ (например ID#12345):
     3. Название ЗНИ:
     ```
     Дописать блок `## Metadata (comment markers)` в `proposal.md` после `## Why`. Сформировать `open_marker` и `close_marker`.
   Эти строки будут передаваться в промпт `onec-code-writer`.

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
      [3] Дефект в предыдущем срезе S<K> — укажу S<K> и суть дефекта

   4. По ответу:
      - [1] → mark [x], append debug.md "решение: принят", сгенерировать reports/slice-acceptance-S<N>-YYYY-MM-DD.md, перейти к задачам S<N+1>.
      - [2] → запросить описание проблемы; append debug.md "решение: не принят" + секция ## Debug — S<N>; создать fix-задачи перед S<N>.T<M>; начать их выполнение.
      - [3] → запросить **S<K>** и описание дефекта; **Grep** в `tasks.md` строку приёмки `S<K>.T<M>`:
        - Если `S<K>.T<M>` = **`[ ]`** (срез S<K> **не** принят) → **inside-slice rework** по `.cursor/rules/vertical-slices.mdc` (**ИНВАРИАНТ: Defect placement**): добавить fix-задачи **внутрь** `S<K>` **перед** `S<K>.T<M>`; **не** создавать `# Срез S<N+1>` без cross-slice; append в `debug.md` `Решение: inside-slice rework` + RCA-кратко; начать выполнение fix-задач.
        - Если `S<K>.T<M>` = **`[x]`** (срез S<K> принят, frozen) → создать **fix-срез** `# Срез S<N+1>: …` с отдельным `S<N+1>.T<M>` по `vertical-slices.mdc`; **снять** `[x]` с `S<K>.T<M>` только если инвариант/постановка явно требует повторной приёмки S<K> (зафиксировать в `debug.md`); иначе — только приёмка нового среза.

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

   **Step-by-step mode** — более жёсткий режим, активируется когда выполнено **хотя бы одно** из условий (триггеры):
   - `explicit-request` — пользователь прямо попросил: «по одной», «step-by-step», «пошагово», «по шагам», «одну задачу».
   - `debug-session` — `debug.md` существует AND был изменён сегодня (активная отладка).
   - `fix-slice` — имя среза начинается с `Fix ` / `Фикс `, либо срез создан из `/opsx:debug` (секция «Fix-задачи» в debug.md).
   - `slice-size-threshold` — в принимаемом срезе ≥5 задач (включая `S<N>.T<M>`).

   В режиме step-by-step — пауза также после КАЖДОЙ завершённой задачи (не только на slice-gate).

   **Batch mode** активируется ТОЛЬКО в legacy mode (без срезов) и по явному запросу пользователя — sequential execution с паузами только на ошибках/условных задачах.

   **Announce mode (обязательно, с явной причиной):**
   - "Режим: step-by-slice (пауза на каждом slice-gate)" — по умолчанию в slice mode без триггеров step-by-step.
   - "Режим: step-by-step (триггер: `<id-триггера>`; пауза после каждой задачи и на slice-gate)" — выбрать один из: `explicit-request`, `debug-session`, `fix-slice`, `slice-size-threshold`. При нескольких одновременно — указать все через запятую.
   - "Режим: batch/legacy (пауза только на ошибках)".

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

     Действие — сгенерировать T-HANDOFF вариант `acceptance` (формат — `.cursor/docs/opsx-output-style.md` §5.2; НЕ вызывать AskQuestion):

     ```
     ## Срез S<N> — передача на приёмку: <change-name>

     **Прогресс:** N/N non-test задач [x]; `S<N>.T<M>` — `[ ]` (ручная приёмка).

     ### 1. Что реализовано
     1. [x] S<N>.<M> — <одно предложение>
        - Файл: `<path>`, строки X-Y
        - Авто-проверка: OK | линтер чист | reviewer PASS | <замечания одной строкой>

     ### 2. Что проверить СЕЙЧАС
     Сценарий `S<N>.T<M>` в императиве (переписать критерии приёмки по пунктам; внутренние ID регрессий — в скобках в конце пункта):
     1. Открыть <что>
     2. Выполнить <действие>
     3. Убедиться <ожидаемый результат> (регрессия R<N>, если применима)

     ### 3. Как вернуться
     `/opsx:apply <change-name>` — новая сессия начнётся с запроса вердикта (принят / не принят / дефект в предыдущем срезе). Если при проверке выяснится, что нужно изменить scope/design/tasks, используйте `/opsx:extend <change-name>`; команда покажет бриф и вернёт в `/opsx:verify`. Пока вы проверяете — оркестратор ничего не делает.

     ### 4. Short-cut
     Если уже проверено и принято — напишите `принято S<N>` / `accept S<N>`, отмечу без полного handoff.
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
     2. T-HANDOFF вариант `acceptance` по шаблону шага 7 (заголовок — `## Срез S<N> — передача на приёмку: <change-name>`). Секция «Что проверить СЕЙЧАС» заполняется сценарием из `S<N>.T<M>` (та же информация, что в Acceptance Handoff Card выше).
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
     3. T-HANDOFF вариант `pause` (по шаблону шага 7).
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
   - Implementation reveals a design/scope issue → stop implementation and suggest `/opsx:extend <change-name>` (or `/opsx:extend <change-name> --from-review <report-path>` if the issue came from review), then `/opsx:verify <change-name>`
   - Error or blocker encountered → report and wait for guidance
   - User interrupts
   - **Verification/decision task completed** → conditional task checkpoint (see above)

7. **On completion or pause — T-HANDOFF (единый шаблон)**

   Формат — **T-HANDOFF** из `.cursor/docs/opsx-output-style.md` §5.2. Заголовок выбирается по варианту:
   - `acceptance` → `## Срез S<N> — передача на приёмку: <change-name>` (handoff в конце среза, default)
   - `pause` → `## Сессия приостановлена: <change-name>` (issue / пользовательский стоп)
   - `final` → `## Реализация завершена: <change-name>` (все срезы приняты)

   **Имена секций одинаковы во всех трёх вариантах** (см. раздел «Output — T-HANDOFF» ниже):

   - `### 1. Что реализовано` — за каждую задачу этого сеанса: `[x] N.M — описание`, файл `path` со строками, «что изменено» одним предложением, авто-проверка (spot-check) OK/расхождение.
   - `### 2. Что проверить СЕЙЧАС` — для каждой закрытой задачи с критериями приёмки (маркеры `убедиться`, `проверить`, `критерий приёмки`, `Критерий приёмки`): переписать критерии в императиве нумерованным списком (1. Открыть… 2. Выполнить… 3. Убедиться…). Для задач типа «Ручной тест» — полный сценарий с ожидаемыми результатами. Если ничего не требуется от пользователя — одна строка «Ручная проверка не требуется для задач этого сеанса».
   - `### 3. Следующие задачи` — таблица `Задача | Тип | Исполнитель | Зависит от | Статус`; 3–5 следующих. Для каждой: Type (BSL / Form / Manual test / Metadata / …), Executor (agent / user), статус зависимостей (`[x]`/`[ ]`); если зависимость `[ ]` — пометить «невыполнима до N.M».
   - `### 4. Как вернуться` — `/opsx:apply <change-name>`, одна строка. Если выявлен scope/design mismatch, добавить вторую строку: `Обновить scope: /opsx:extend <change-name>` (после extend — `/opsx:verify <change-name>`).
   - `### 5. Blockers` — нумерованный список задач, которые не могут продолжаться, и почему.
   - `### 6. Issue` — **только в варианте `pause`**: описание проблемы 1 абзац + нумерованные **Options** из 2–3 вариантов решения.
   - `### 7. Short-cut` — **только в варианте `acceptance`**: строка про `принято S<N>` / `accept S<N>`.

   Если все срезы приняты (`final`) — добавить строку «All tasks complete. Ready to archive: `/opsx:archive <change-name>`». Если `pause` из-за design/scope mismatch — предложить `Follow-up: /opsx:extend <change-name>` рядом с вариантами решения. Если `pause` — ждать ответа пользователя. Если `acceptance` — end turn.

   **Self-check** (см. §7 стайл-гайда) перед выводом: слои разделены, нумерованные списки, одинаковые имена секций, длина в пределах лимитов.

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

**Output — T-HANDOFF (единый шаблон, см. `.cursor/docs/opsx-output-style.md` §5.2)**

Три варианта заголовка при одинаковых именах секций — выбирается по состоянию:

| Вариант | Заголовок | Когда |
|---------|-----------|-------|
| `acceptance` | `## Срез S<N> — передача на приёмку: <change-name>` | Slice Gate: все non-test задачи `[x]`, `S<N>.T<M>` ждёт ручной приёмки |
| `pause` | `## Сессия приостановлена: <change-name>` | Issue / неясное требование / пользователь «стоп» |
| `final` | `## Реализация завершена: <change-name>` | Все задачи `[x]`, включая все `S<N>.T<M>` |

**Общая структура вывода (секции 1–5; секции 6–7 — только в указанных вариантах):**

```
## <Заголовок варианта>

**Change:** <change-name>
**Schema:** <schema-name>
**Прогресс:** N/M задач [x] (срез S<N>.T<M>: <статус>)

### 1. Что реализовано
1. [x] <id задачи> — <одно предложение>
   - Файл: `<path>`, строки X-Y
   - Что изменено: <одно предложение>
   - Авто-проверка: OK | расхождение <описание>

### 2. Что проверить СЕЙЧАС
1. <шаг 1 в императиве> → <ожидаемый результат> (регрессия R<N>, если применима)
2. <шаг 2> → <ожидаемый результат>
(или: «Ручная проверка не требуется для задач этого сеанса».)

### 3. Следующие задачи
| Задача | Тип | Исполнитель | Зависит от | Статус |
|--------|-----|-------------|------------|--------|
| ...    | ... | ...         | ...        | [x]/[ ] |

### 4. Как вернуться
`/opsx:apply <change-name>` — продолжит с первого непринятого среза.

### 5. Blockers (если есть)
1. <блокер> — <чем закрывается>

<!-- только для варианта `pause` -->
### 6. Issue
<1 абзац: описание проблемы>

**Options:**
1. <вариант 1>
2. <вариант 2>
3. Другой подход (описать)

<!-- только для варианта `acceptance` -->
### 7. Short-cut
Если уже проверено и принято — напишите `принято S<N>` / `accept S<N>`, отмечу без полного handoff.

<!-- только для варианта `final` -->
> All tasks complete. Ready to archive: `/opsx:archive <change-name>`.
```

**Имена секций** (`### 1. Что реализовано`, `### 2. Что проверить СЕЙЧАС`, `### 3. Следующие задачи`, `### 4. Как вернуться`, `### 5. Blockers`) — **одинаковы во всех трёх вариантах**; это же именование используется в `debug.md` `## Slice Gate Decisions` → «Связанный отчёт».

**Self-check перед выводом** (§7 стайл-гайда): (1) в «Что проверить СЕЙЧАС» нет внутренних ID (`R<N>/SC<N>/D<N>`) в тексте пункта — только в скобках в конце; (2) имена команд / модулей / UI — по типографическим правилам §2; (3) перечисления — нумерованный список; (4) «Что проверить» — императивы, без формулировок гипотез; (5) каждая секция ≤7 пунктов; длиннее — выносить в отчёт `reports/`.

**Guardrails**
- **Output style:** все пользовательские сообщения (Acceptance Handoff, pause, final, Implementation summary) выводятся по единому шаблону **T-HANDOFF** из `.cursor/docs/opsx-output-style.md` §5.2; имена секций одинаковы во всех вариантах; перед отправкой — self-check-5 (§7).
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
- **vertical-slices.mdc:** вердикт Slice Gate **[3]** и любое добавление `# Срез` — только по **ИНВАРИАНТ: Defect placement** (не создавать fix-срез при `S<K>.T<M>` = `[ ]` без cross-slice).

**Fluid Workflow Integration**

This skill supports the "actions on a change" model:

- **Can be invoked anytime**: Before all artifacts are done (if tasks exist), after partial implementation, interleaved with other actions
- **Allows artifact updates**: If implementation reveals design issues, suggest updating artifacts - not phase-locked, work fluidly
