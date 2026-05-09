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
      - Layer ordering inside slice is guidance only (метаданные → UI: Конфигуратор или BSL модуля формы → код → приёмка); enforce via task-level dependency graph from tasks.md.
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

   **Пошаговый режим** (внутренний код режима — `step-by-step`, в чат не цитируется) — более жёсткий режим, активируется когда выполнено **хотя бы одно** из условий (триггеры):
   - `explicit-request` — пользователь прямо попросил: «по одной», «пошагово», «по шагам», «одну задачу».
   - `debug-session` — `debug.md` существует AND был изменён сегодня (активная отладка).
   - `fix-slice` — имя среза начинается с `Fix ` / `Фикс `, либо срез создан из `/opsx:debug` (секция «Fix-задачи» в debug.md).
   - `slice-size-threshold` — в принимаемом срезе ≥5 задач (включая `S<N>.T<M>`).

   В пошаговом режиме — пауза также после КАЖДОЙ завершённой задачи (не только на slice-gate).

   **Batch mode** активируется ТОЛЬКО в legacy mode (без срезов) и по явному запросу пользователя — sequential execution с паузами только на ошибках/условных задачах.

   **Announce mode (обязательно, с явной причиной в пользовательском языке):**
   - "Режим: пауза на каждом slice-gate" — по умолчанию в slice mode без триггеров пошагового режима.
   - "Режим: пошаговый (пауза после каждой задачи, так как <причина>)" — выбрать причину: «вы просили пошагово», «активная отладка», «срез содержит фиксы», «в срезе много шагов». Внутренние ID триггеров (`slice-size-threshold` и т.д.) в текст для пользователя **не выводить**.
   - "Режим: пакетный (пауза только на ошибках)".

   **5.5b Слой чата при apply (анти-шум)** — относится ко **всем** промежуточным сообщениям в чате (старт сессии, между задачами, перед делегированием writer). Финальный **T-HANDOFF** (шаг 7) не отменяется.

   | В чат пользователю | В артефактах / контексте модели |
   |---|---|
   | Блокеры, предупреждения, вопросы с выбором | Полные пути, grep, вывод CLI |
   | Короткий UX-итог: что сделано / что будет дальше (1–3 предложения) | Повторный дословный pre-apply, дубли одной строки PASS |
   | Прогресс: «задача M/N», срез в формате §10 `opsx-output-style` (**Срез S\<N\>: «название»**) | Перечисление сырого `S1.1–S1.T5` в одной строке без названия среза |
   | Режим **человеческим языком**: «пауза после каждой задачи — в срезе много шагов» / «вы просили пошагово» / «активная отладка по debug» | Обязательное цитирование внутренних id триггеров (`slice-size-threshold`, `step-by-step`, `awaiting-acceptance`); при необходимости id один раз в `debug.md` или в конце сообщения мелким блоком «Техническое» |
   | «Маркеры разработчика в proposal заполнены» | Полный текст строк `// +++` / `// ---` в чате |
   | Одна строка со ссылкой на отчёт verify при старте (если нужна): `reports/verification-*.md` | Дважды одно и то же PASS + длинный путь |
   | Пошаговая пауза: что изменилось, что проверить руками, варианты ответа | Списки инструментов ради отчёта («ReadLints», «grep OK») — допустимо заменить на «автопроверки пройдены», если детали не важны для приёмки |
   | Роли исполнителей по-русски: «агент», «агент + ревью», «пользователь», «оркестратор» | Имена агентов (`onec-code-writer`, `onec-code-reviewer`, `onec-code-explorer`, `onec-code-architect`, `openspec-quality-controller`) — только во внутреннем контексте делегирования; в чат не цитируются |
   | Обозначение проверки на человеческом языке: «архитектурное ревью закрыто», «проверка прошла резервным агентом» | Имена гейтов (`Architect Gate`, `Slice Gate`, `Implementation Impact Gate`) и техкоды режимов (`Step-by-step`, `checkpoint`, `Tier`, `Standard/Lite/Full`) — только в `debug.md`, отчётах `reports/` и в скрытом контексте модели |

   **Не считать обязательным содержимым ответа пользователю:** нарратив «читаю скилл / по протоколу команды»; строки вида «Explored N files» / «Ran OpenSpec…» как **текст итогового сообщения** (это следы инструментов — остаются в UI, но не обязаны дублироваться в сводке для человека).

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
   | Модуль формы (BSL) | путь `Forms/.../Ext/Form/Module.bsl`, «программно создать элемент», «Элементы.Добавить», «видимость элементов» без правки `Form.xml` | **onec-code-writer** + **onec-code-reviewer** после |
   | Форма / Form.xml / Конфигуратор | «Form.xml», «реквизиты формы», «добавить форму», «колонки в Конфигураторе», создание/изменение XML формы | **СТОП.** Инструкция ручного конфигурирования (1c-xml-write-guard.mdc). WAIT — не продолжать до выгрузки |
   | Верификация метаданных | «проверить соответствие», «проверить наличие» | Оркестратор (Glob/Grep/Read — только проверка, не реализация) |
   | Приёмочный тест (`S<N>.T<M>`) или ручной тест | «ручной тест», «убедиться», `S<N>.T<M>` | **Режимы по срезам / пошаговый** (внутренние коды `step-by-slice` / `step-by-step`): trigger Slice Gate (см. шаг 6). **Legacy batch:** пропустить с предупреждением; включить в Session Summary секцию «Отложенные ручные тесты» |
   | Создание метаданных | «создать регистр», «создать справочник», «создать форму» | **СТОП** — блокер пользователю (`1c-no-metadata-creation.mdc`) |

   **HALT:** Оркестратор НЕ реализует задачи типов BSL-код и модули формы самостоятельно. Оркестратор готовит промпт и делегирует. Прямое использование Write/StrReplace для .bsl и **любая правка Form.xml** (включая скрипты/JSON-конвейеры) — запрещены. Для `Form.xml`/Конфигуратора: СТОП — инструкция ручного конфигурирования и WAIT до выгрузки/приёмки пользователя. Для программного создания элементов в `Form/Module.bsl`: обычный BSL pipeline (`onec-code-writer` → `ReadLints` → `onec-code-reviewer`). Ref: `1c-agent-delegation.mdc`, `1c-utility-agents.mdc`, `1c-xml-write-guard.mdc`.

   **Code-Truth Journal (mandatory after writer/reviewer success):**
   - После каждой BSL/form-module задачи извлечь из ответа `onec-code-writer` блок `created_or_modified_symbols`.
   - Spot-check: Grep/Read каждый `evidence` или `name` в указанном файле. Если символ не найден — НЕ отмечать задачу `[x]`; pause с рекомендацией `/opsx:extend <change-name> --code-sync`.
   - В `debug.md` записывать только факты из кода, не план:
     ```markdown
     ### Code-Truth — <task-id> — YYYY-MM-DD
     - task: <S<N>.<M> / legacy id>
     - symbols:
       - <name> @ <file>:<lines>, annotation=<annotation>, action=<created|modified|removed>
     - verification: grep/read OK | mismatch <details>
     - source: writer.created_or_modified_symbols
     ```
   - Запрещено писать в `debug.md` имена процедур/хелперов, которых нет в `created_or_modified_symbols` или spot-check.

   **Investigation Loop при apply.** Если reviewer в отчёте включил секцию `## Investigation Request`:
   1. Вызвать explorer (contract resolution deep) по таблице из Investigation Request. Шаблон: «Explorer — contract resolution (deep)» из `1c-agent-patterns/explorer.md`.
   2. Сохранить вывод в `reports/resolved-contract-<slug>-YYYY-MM-DD.md` (артифакт ЗНИ).
   3. Повторно вызвать reviewer с Resolved Contracts в промпте.
   4. При последующем устранении замечаний — передать Resolved Contracts в промпт writer.
   Протокол: см. `1c-agent-delegation.mdc`, секция CONTRACT RESOLUTION; шаблоны: `1c-agent-patterns/explorer.md` (Explorer — contract resolution), `1c-agent-patterns/writer.md` (Writer — review fix), `1c-agent-patterns/reviewer.md` (Reviewer — ревью кода).

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
   - **Пошаговая пауза (если активен пошаговый режим):** После отметки задачи выполненной, ОБЯЗАТЕЛЬНАЯ ПАУЗА. Заголовки и формулировки — в пользовательском языке (англицизмы `Step-by-step`, `checkpoint` в чат не цитируются; см. §3.1 `opsx-output-style.md`).

     **Шаблон для задач кода/форм** (выполненных агентом):

     ```
     ## Ваш шаг (пошаговая пауза)

     **Задача `S<N>.<M>` («<краткое описание из tasks.md в «ёлочках»>») реализована.**

     ### Что изменено
     - Файл: `<path>`, строки X-Y
     - <одно предложение по сути правки>

     ### Что проверить у себя — задача `S<N>.<M>` («<описание>»)
     1. <шаг 1 в императиве>
     2. <шаг 2>
     ...

     **Варианты:** [Подтвердить / Проблема / Пропустить]
     ```

     - **Подтвердить** → продолжить.
     - **Проблема** → пользователь описывает проблему, создать задачу follow-up в том же срезе (до `S<N>.T<M>`), НЕ продолжать до решения или «Пропустить».
     - **Пропустить** → продолжить, добавить пометку «(не проверено пользователем)», включить в Session Summary как непроверенное.

     **Шаблон для задач приёмки** (`S<N>.T<M>`):

     ```
     ## Ваш шаг (приёмочный тест) — `S<N>.T<M>` («<краткое описание теста>»)

     ### Сценарий
     1. <шаг 1>
     ...

     ### Зависимости
     - `S<N>.<M>` [x] — <описание>

     **Варианты:** [Тест пройден → перейти к slice-gate / Тест не пройден / Отложить]
     ```

     Это эквивалент Slice Gate; шаги описаны выше.

     **Правило «первое упоминание ID — с описанием».** Каждое первое упоминание `S<N>.<M>` или `S<N>.T<M>` в заголовке секции / карточки / handoff-сообщения сопровождается коротким описанием задачи в «ёлочках». Голый `S<N>.<M>` без описания (например «Что имеет смысл проверить у себя (к `S1.2`)» или «`S1.2` закрыта с моей стороны») в заголовках чата запрещён. Повторное упоминание в той же секции — уже без описания. Срез — по правилу §10 `opsx-output-style.md` (`Срез S<N>: «<название>»`).
   - **If this was a verification/decision task** (identified in Conditional Task Detection) → trigger ОБЯЗАТЕЛЬНАЯ ПАУЗА above before proceeding
   - Continue to next task

   **Pause if:**
   - **Slice Gate reached** (все non-test задачи среза `[x]`, остался только `S<N>.T<M>` или первый task следующего среза) — ОБЯЗАТЕЛЬНАЯ карточка приёмки (см. Slice Gate check выше)
   - **Пошаговый режим:** после завершения каждой задачи (пошаговая пауза выше)
   - Task is unclear → ask for clarification
   - Implementation reveals a design/scope issue → stop implementation and suggest `/opsx:extend <change-name>` (or `/opsx:extend <change-name> --from-review <report-path>` if the issue came from review), then `/opsx:verify <change-name>`
   - Error or blocker encountered → report and wait for guidance
   - User interrupts
   - **Verification/decision task completed** → пауза условной задачи (см. выше «Conditional Task Detection»)

7. **On completion or pause — T-HANDOFF (единый шаблон)**

   Формат — **T-HANDOFF** из `.cursor/docs/opsx-output-style.md` §5.2. Заголовок выбирается по варианту:
   - `acceptance` → `## Срез S<N> — передача на приёмку: <change-name>` (handoff в конце среза, default)
   - `pause` → `## Сессия приостановлена: <change-name>` (issue / пользовательский стоп)
   - `final` → `## Реализация завершена: <change-name>` (все срезы приняты)

   **Имена секций одинаковы во всех трёх вариантах** (см. раздел «Output — T-HANDOFF» ниже):

   - `### 1. Что реализовано` — за каждую задачу этого сеанса: `[x] N.M — описание`, файл `path` со строками, «что изменено» одним предложением, авто-проверка (spot-check) OK/расхождение.
   - `### 2. Что проверить СЕЙЧАС` — для каждой закрытой задачи с критериями приёмки (маркеры `убедиться`, `проверить`, `критерий приёмки`, `Критерий приёмки`): переписать критерии в императиве нумерованным списком (1. Открыть… 2. Выполнить… 3. Убедиться…). Для задач типа «Ручной тест» — полный сценарий с ожидаемыми результатами. Если ничего не требуется от пользователя — одна строка «Ручная проверка не требуется для задач этого сеанса».
   - `### 3. Следующие задачи` — таблица `Задача | Действие | Тип | Исполнитель | Зависит от | Статус`; 3–5 следующих. Для каждой:
     - **Задача** — ID `S<N>.<M>` / `S<N>.T<M>` в backticks.
     - **Действие** — короткое описание задачи из `tasks.md` (одна фраза в «ёлочках» или без — глагол + что делается). Без имён процедур и кодов категорий.
     - **Тип** — русское обозначение из набора: `Код модуля` (BSL общий модуль / объектный модуль), `Код формы` (BSL `Forms/.../Ext/Form/Module.bsl`, программное создание элементов), `Ручной тест`, `Ручная регрессия`, `Конфигуратор` (создание/правка метаданных через UI 1С), `Проверка` (Grep/Read оркестратора).
     - **Исполнитель** — русские роли: `агент`, `агент + ревью`, `пользователь`, `оркестратор`. Имена `onec-code-writer` / `onec-code-reviewer` / `onec-code-explorer` / `onec-code-architect` в чат не выводятся (см. §3.1 `opsx-output-style.md`).
     - **Зависит от** — ID задач в backticks; если зависимость `[ ]` — пометить «невыполнима до `<id>`».
     - **Статус** — `[x]` / `[ ]`.
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
| Задача | Действие | Тип | Исполнитель | Зависит от | Статус |
|--------|----------|-----|-------------|------------|--------|
| `S1.3` | заполнить значения по умолчанию на новом цикле | Код модуля | агент + ревью | `S1.2` | [ ] |
| `S1.4` | проверить пересчёт состава при смене настройки | Код формы | агент + ревью | `S1.3` | [ ] |
| `S1.5` | прогнать сценарий повторного согласования вручную | Ручная регрессия | пользователь | `S1.1`–`S1.4` | [ ] |
| `S1.T1`–`S1.T5` | приёмочные тесты среза | Ручной тест | пользователь | см. выше | [ ] |

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

**Self-check перед выводом** (§7 стайл-гайда):
1. В «Что проверить СЕЙЧАС» нет внутренних ID (`R<N>/SC<N>/D<N>`) в тексте пункта — только в скобках в конце.
2. Имена команд / модулей / UI — по типографическим правилам §2.
3. Перечисления — нумерованный список.
4. «Что проверить» — императивы, без формулировок гипотез.
5. Каждая секция ≤7 пунктов; длиннее — выносить в отчёт `reports/`.
6. **Первое упоминание `S<N>.<M>` / `S<N>.T<M>`** в заголовке секции / карточки / handoff-сообщения — с коротким описанием задачи в «ёлочках» (например «Что проверить у себя — задача `S1.2` («перенос флага из шаблона в БП»)»). Голый ID без описания в заголовке (например «к `S1.2`», «`S1.2` закрыта с моей стороны») — провал self-check. Срез — по §10 `opsx-output-style.md`.
7. **Колонка «Действие»** в таблице «Следующие задачи» — обязательна; «Тип» и «Исполнитель» — только из русских наборов значений (см. описание шага 7); имена `onec-code-*` в чат не выводятся.
8. **Англицизмы** (`Step-by-step`, `checkpoint`, `Tier`, `Standard/Lite/Full` как метки) и имена движка (`Architect Gate`, `Slice Gate`, `Implementation Impact Gate`) — в пользовательский вывод не попадают; внутренние ID триггеров (`slice-size-threshold`, `awaiting-acceptance`) — только в `debug.md` / в скрытом контексте модели.

**Guardrails**
- **Output style:** все пользовательские сообщения (Acceptance Handoff, pause, final, Implementation summary) выводятся по единому шаблону **T-HANDOFF** из `.cursor/docs/opsx-output-style.md` §5.2; имена секций одинаковы во всех вариантах; перед отправкой — self-check-5 (§7).
- Keep going through tasks until done or blocked
- Always read context files before starting (from the apply instructions output)
- **Spot-check after each task:** Grep (or Read) to confirm the change; for 5+ files, check at least 3. Do not mark task complete if verification fails.
- If task is ambiguous, pause and ask before implementing
- If implementation reveals issues, pause and suggest artifact updates
- Keep code changes minimal and scoped to each task
- Update task checkbox immediately after completing each task
- **Code-Truth Journal:** for every writer-completed BSL/form task, append factual symbols from `created_or_modified_symbols` to `debug.md`; if code and artifacts diverge, pause and route to `/opsx:extend <change-name> --code-sync`.
- Pause on errors, blockers, or unclear requirements - don't guess
- Use contextFiles from CLI output, don't assume specific file names
- **Task Dispatch:** classify each task before implementation; delegate to the correct executor per dispatch table. Orchestrator MUST NOT implement BSL or form-module tasks directly — only prepare context and delegate.
- **Form XML / Configurator tasks:** STOP — produce manual configuration instructions (`1c-xml-write-guard.mdc`); do not edit `Form.xml` or continue until the user has performed configuration and re-exported.
- **Form module BSL tasks:** if the task changes `Forms/.../Ext/Form/Module.bsl` only (for example `Элементы.Добавить`, visibility, event handlers), run the standard BSL writer/reviewer pipeline; this is not a `Form.xml` task.
- Reference: `1c-agent-delegation.mdc` (BSL gate), `1c-utility-agents.mdc` (forms, queries, tests).
- **vertical-slices.mdc:** вердикт Slice Gate **[3]** и любое добавление `# Срез` — только по **ИНВАРИАНТ: Defect placement** (не создавать fix-срез при `S<K>.T<M>` = `[ ]` без cross-slice).

**Fluid Workflow Integration**

This skill supports the "actions on a change" model:

- **Can be invoked anytime**: Before all artifacts are done (if tasks exist), after partial implementation, interleaved with other actions
- **Allows artifact updates**: If implementation reveals design issues, suggest updating artifacts - not phase-locked, work fluidly
