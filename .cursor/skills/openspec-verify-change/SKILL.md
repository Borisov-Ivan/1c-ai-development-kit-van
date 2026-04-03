---
name: openspec-verify-change
description: Universal quality gate for OpenSpec changes. Pre-apply — artifact quality, task specificity, phase coherence (QC before Architect), conditional TZ generation, gates, scope gate. Post-apply — implementation completeness, correctness, coherence.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "6.0"
  generatedBy: "1.1.1"
---

Universal quality gate for OpenSpec changes. Works in two modes determined automatically:
- **Pre-apply**: artifact format, task quality, manual config checklist, **phase coherence (Quality Controller)** — **строго до** architect readiness review (шаг 7.7), **mandatory architect readiness review**, **TZ generation** (при пороге задач или явном запросе, шаг 7.8), Architect Gate, Design Review, TZ Review, project constraints
- **Post-apply**: implementation completeness, correctness, coherence

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If multiple active changes: run `openspec list --json`, show changes that have tasks artifact, include schema, mark incomplete as "(In Progress)", and use **AskUserQuestion tool** to let user select

   Always announce: "Using change: <name>" and how to override (e.g., `/opsx:verify <other>`).

1b. **Scope Gate — новое требование vs verify**

   Если в сообщении пользователя **помимо** выбора change и команды `/opsx:verify` есть:
   - новое функциональное требование (формулировки вроде «нужно предусмотреть», «добавить», «учесть сценарий», «не забудь», «доработай постановку»);
   - явный запрос расширить scope change (новые задачи, требования, сценарии в свободной форме).

   **СТОП** до разрешения. Использовать **AskUserQuestion** (или эквивалент):

   - Текст: «В запросе обнаружено новое требование: „<краткая формулировка>“. Verify — quality gate для **существующих** артефактов. Выберите вариант:»
   - **Вариант 1:** Сначала дополнить артефакты (оркестратор вносит правки → подтверждение пользователя), затем verify полного scope.
   - **Вариант 2:** Verify текущего scope как есть; новое требование — отдельно после (`/opsx:explore`, `/opsx:ff`, ручное дополнение).
   - **Вариант 3:** Verify текущего scope as-is; новое требование зафиксировать как TODO в отчёте verify (Executive Summary), без правки артефактов в этой сессии.

   **Поведение по выбору:**
   - **1:** Внести правки в proposal/design/spec/tasks по согласованию; получить явное подтверждение пользователя («ок», «да» и т.п.); продолжить verify с шага 2. В итоговом отчёте — секция `## Изменения артефактов в ходе verify` (перечень файлов и сути правок). Маркер: «Артефакты модифицированы перед верификацией. QC и Architect оценивали **изменённую** версию.»
   - **2:** Продолжить verify без правок; в конце отчёта — «Не включено в scope: <требование>. Рекомендация: `/opsx:explore` или `/opsx:ff`.»
   - **3:** Продолжить verify без правок; в Executive Summary — «TODO (не верифицировано в этом прогоне): <требование>.»

   Если **только** `/opsx:verify` / `/opsx:verify <change>` без дополнительного текста требований — шаг 1b **пропустить**.

2. **Check status to understand the schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand:
   - `schemaName`: The workflow being used (e.g., "spec-driven")
   - Which artifacts exist for this change

3. **Get the change directory and load artifacts**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   This returns the change directory and context files. Read all available artifacts from `contextFiles`.
   Also read `openspec/project.md` for project-level constraints.

4. **Determine verification mode**

   Parse tasks.md:
   - Count lines matching `- [ ]` (incomplete checkboxes)
   - Count lines matching `- [x]` (complete checkboxes)
   - Count lines matching `- N.M` without checkbox (bare task lines)

   **Mode decision:**

   | Checkboxes found | `[x]` count | `[ ]` count | Mode |
   |---|---|---|---|
   | 0 (bare lines only) | — | — | **pre-apply** |
   | >0 | 0 | >0 | **pre-apply** |
   | >0 | >0 | >0 | **mixed** or **phase-transition** (see below) |
   | >0 | >0 | 0 | **post-apply** |

   **Phase-transition mode detection:**

   Phase-transition activates in ANY of these cases:
   1. User or apply explicitly requested phase-transition review (e.g. "verify in phase-transition mode", "phase gate review")
   2. The prompt indicates this run was triggered from apply at a phase gate
   3. **Auto-detect:** tasks.md contains `<!-- phase-gate -->` markers AND there exist `[x]` tasks before a gate AND `[ ]` tasks after that gate (= a phase boundary has been crossed)

   For case 3 (auto-detect): automatically set mode = phase-transition. Announce: "Обнаружены phase gates. Фаза N завершена (K задач [x] до gate, M задач [ ] после). Режим: phase-transition (mixed + проверка актуальности оставшихся задач)."

   When phase-transition:
   - Mode = **phase-transition**
   - Inherit mixed-mode checks and ADD phase-specific checks (step 7.6b)
   - Otherwise mixed (both [x] and [ ] present) = **mixed**

   Announce mode to user:
   ```
   Режим: pre-apply (артефакты не реализованы)
   Режим: mixed (N/M задач выполнено — pre-проверки для оставшихся, post-проверки для выполненных)
   Режим: phase-transition (ревью на границе фазы — актуальность оставшихся задач)
   Режим: post-apply (все задачи выполнены)
   ```

5. **Initialize report structure**

   Create a report structure with sections:
   - **Artifact Format** (pre-apply, mixed)
   - **Task Quality** (pre-apply, mixed)
   - **Manual Configuration Sufficiency** (pre-apply, mixed) — structured checklist with proof
   - **Phase Coherence (Quality Controller)** (pre-apply, mixed) — phase classification, dependency graph, false start detection, rework risk
   - **Task Readiness (Architect)** (pre-apply, mixed) — mandatory architect holistic assessment of realizability
   - **TZ (Functional Requirements)** (pre-apply, mixed) — generated TZ document, gap analysis
   - **Gates** (pre-apply, mixed): Architect Gate, Design Review, TZ Review, Project Constraints
   - **Completeness** (post-apply, mixed)
   - **Correctness** (post-apply, mixed)
   - **Coherence** (post-apply, mixed)
   - **Развёрнутые объяснения замечаний** (если есть любые CRITICAL/WARNING/SUGGESTION) — обязательная секция в **файле** отчёта и в сообщении пользователю; см. шаг 16

   Each section can have CRITICAL, WARNING, or SUGGESTION issues.

---

## Pre-apply checks (modes: pre-apply, mixed)

6. **Artifact Format Check**

   **6A. Task checkboxes:**
   - Every task line must have `- [ ]` or `- [x]` prefix
   - Scan for lines matching pattern `^- \d+\.\d+\s` (bare task without checkbox)
   - If bare tasks found:
     - Add CRITICAL: "Задачи без чекбоксов: N строк. apply/estimate/archive не смогут отслеживать прогресс"
     - Set `autofix_checkboxes = true` for step 17

   **6B. Task numbering:**
   - Tasks should follow `N.M` numbering within `## N. Group` sections
   - If numbering absent or inconsistent: WARNING

   **6C. Group headers:**
   - Sections should be `## N. Название`
   - If tasks exist without group headers: SUGGESTION

7. **Task Quality Check**

   For each task line (matching `- [ ] N.M` or bare `- N.M`):

   **7A. Classify task type:**
   - **Code task**: mentions `.bsl`, `процедур`, `функци`, `реализовать`, `добавить`, `изменить`, `перехват`, `аннотаци` — requires file path and acceptance criteria
   - **Metadata task**: mentions `создать в расширении`, `регистр`, `обработк`, `справочник`, `форм` without `.bsl` path — requires action description and expected result
   - **Test task**: mentions `тест`, `проверить`, `убедиться`, `регрессия` — requires action steps and expected result
   - **Investigation task**: mentions `обследова`, `найти`, `проверить путь`, `зафиксировать` — requires what to find and acceptance criteria

   **7B. Check required elements by task type:**

   | Element | Code task | Metadata task | Test task | Investigation task |
   |---|---|---|---|---|
   | File path (`src/...` or backticked path) | CRITICAL if absent | SUGGESTION | N/A | SUGGESTION |
   | Acceptance criteria (`Критерии приёмки` / `Что проверить` / bullet list under task) | CRITICAL if absent | WARNING if absent | WARNING if absent | WARNING if absent |
   | Specific action (`Что делать` / `Что менять` or clear verb phrase) | WARNING if vague | WARNING if vague | WARNING if vague | WARNING if vague |
   | Dependencies (`Зависимости` when task refs other groups) | WARNING if absent | WARNING if absent | N/A | WARNING if absent |

   **7C. Ambiguity markers (Grep on tasks.md):**
   Search for patterns indicating vagueness:
   - `или аналог` — CRITICAL: which one exactly?
   - `при необходимости` — WARNING: what condition triggers necessity?
   - `и т.д.`, `и т.п.`, `и др.` — WARNING: incomplete enumeration
   - `при наличии` — WARNING: presence of what?
   - `по возможности` — WARNING: is this optional?
   - `примерно`, `ориентировочно` — WARNING: imprecise
   - `какой-либо`, `подобн` — WARNING: which one?
   - `(или ...)` — WARNING: alternatives not resolved
   - `переиспользовать логику X или Y` — CRITICAL: decision not made
   - `X/Y` (слэш между существительными рядом с глаголами действия: `вернуть`, `использовать`, `установить`, `записать`) — WARNING: альтернатива не разрешена
   - `Неопределено`, `Null`, `""`, `пустая строка`, `пустое значение` без указания контракта возврата — CRITICAL: какой контракт возврата?
   - `X или Y` при двух глаголах действия (`добавить X или получать Y`, `создать X или использовать Y`) — CRITICAL: решение не принято

   For each found marker: report the task number, the marker, and a recommendation to clarify.

   **7D. Atomicity check:**
   If a single task line (before sub-items) contains 3+ distinct verbs of action (`создать`, `реализовать`, `добавить`, `обернуть`, `проверить`, etc.): WARNING "task may not be atomic — consider splitting".

   **7E. Repo Consistency:**
   For tasks containing «создать» + object type (`регистр`, `обработк`, `справочник`, `документ`, `форм`):
   - Extract the object name from the task description
   - Glob the repository for a directory or file matching that name (e.g., `**/InformationRegisters/<Name>`, `**/DataProcessors/<Name>`, `**/Catalogs/<Name>`)
   - If object **already exists**: WARNING — "Задача N.M говорит «создать X», но X уже существует в репозитории (`path`). Уточнить: «доработать» / «наполнить содержимым»?"
   - If object **does not exist**: OK (consistent with «создать»)

   **7F. Executability & Ordering Check:**

   Mechanical pre-check for all tasks (enriches data for QC step 7.6).

   **7F.1 Functional dependency extraction (all tasks):**
   For each task line, extract implied preconditions:
   - P4 tasks: Grep for `заполнить`, `запустить`, `отправить`, `открыть`, `убедиться` + object name → map to P2/P3 tasks implementing that object
   - P2/P3 tasks: Grep for references to procedures/functions from other modules (pattern `МодульИмя.МетодИмя`) → map to tasks that create/modify those procedures
   - P1 tasks: Grep for data attribute references → map to P0 tasks that create the object
   - Any task: Grep for `Зависимости:` or `Зависимость:` → explicit deps

   For each found dependency (после Actionability Gate при финализации отчёта):
   - Dep task `[ ]` AND current task `[ ]`:
     - Если зависимость **явно указана** в тексте задачи (`Зависимости:` / `Зависимость:` с ID M.K) → **INFO**: "задача N.M зависит от M.K ([ ]); порядок обеспечен объявленными зависимостями / apply"
     - Если зависимость **выявлена только эвристикой**, но **не** отражена в `Зависимости:` → **WARNING**: "задача N.M предположительно зависит от M.K — добавить явные **Зависимости:** в tasks.md"
   - Dep task `[ ]` AND current task needs it for execution — то же правило: явная ссылка в tasks → INFO; нет явной ссылки → WARNING
   - Dep task `[x]` but line > current task line → SUGGESTION: "задача N.M расположена до зависимости M.K в файле"

   **7F.2 Execution order text validation:**
   Grep tasks.md for `Порядок выполнения|Порядок реализации|Последовательность`. If found:
   - Extract task IDs (pattern `\d+\.\d+`)
   - Check each ID exists in tasks.md and its status
   - Flag contradictions with file order

   **7F.3 Phase gate named task check:**
   For each `<!-- phase-gate: ... -->`:
   - Extract task IDs from marker text
   - Check status of each → flag `[ ]` tasks

   Pass all 7F results to Quality Controller (step 7.6) and Architect (step 7.7): "Executability issues (verify 7F): <list or 'замечаний нет'>".

   **Reference format** (for recommendations):
   ```
   - [ ] N.M Краткое описание
     - **Файл:** `path/to/file.bsl`
     - **Что делать:** конкретное действие
     - **Критерии приёмки:**
       * Проверка 1
       * Проверка 2
     - **Зависимости:** N.M, N.M
   ```

7.5. **Manual Configuration Sufficiency Check (structured checklist)**

   **7.5A. Find markers.** Grep tasks.md (case-insensitive) for manual configuration markers:
   `создать в расширении`, `добавить форму`, `создать обработку`, `создать регистр`, `добавить реквизит`, `создать справочник`, `создать документ`, `форму записи`, `форму списка`

   If no markers found → record "маркеров ручной конфигурации не найдено", skip to 7.6.

   **7.5B. Classify each marker** by object type: **Metadata**, **Form**, or **Attributes**.

   **7.5C. For each marker — build and fill a checklist table.** For every row, put a **literal quote** from design.md or `ОТСУТСТВУЕТ`. A business-scenario description (e.g. "выбор ящика → авторизация → запись") is NOT a form description — mark as `ОТСУТСТВУЕТ` for Form rows.

   Checklist by object type:

   **Metadata** (РС, справочник, документ, обработка):

   | Элемент | Требование | Цитата из design / статус |
   |---|---|---|
   | Имя объекта | Точное имя объекта метаданных | *цитата* или `ОТСУТСТВУЕТ` |
   | Реквизиты / измерения / ресурсы | Имя, тип, длина — для каждого | *цитата* или `ОТСУТСТВУЕТ` |
   | Подсистема | В какую подсистему включить | *цитата* или `ОТСУТСТВУЕТ` |

   **Form** (форма обработки, форма документа, форма РС):

   | Элемент | Требование | Цитата из design / статус |
   |---|---|---|
   | Группы | Перечень групп (шаги / страницы / закладки) с назначением | *цитата* или `ОТСУТСТВУЕТ` |
   | Поля | Перечень полей: имя, тип/привязка данных, видимость/доступность | *цитата* или `ОТСУТСТВУЕТ` |
   | Таблицы | Имя таблицы, перечень колонок | *цитата* или `ОТСУТСТВУЕТ` |
   | Команды / кнопки | Перечень с описанием действий | *цитата* или `ОТСУТСТВУЕТ` |
   | UX-сценарий | Пошаговое: что пользователь видит и делает на каждом шаге | *цитата* или `ОТСУТСТВУЕТ` |

   **Attributes** (реквизиты объекта):

   | Элемент | Требование | Цитата из design / статус |
   |---|---|---|
   | Имя | Точное имя реквизита | *цитата* или `ОТСУТСТВУЕТ` |
   | Тип | Тип данных, длина | *цитата* или `ОТСУТСТВУЕТ` |
   | Назначение | Зачем нужен | *цитата* или `ОТСУТСТВУЕТ` |

   **7.5D. Assessment (strict rule):**
   - Any cell = `ОТСУТСТВУЕТ` → **CRITICAL**: "Задача N.M требует ручной конфигурации (`маркер`), но в design.md нет: [перечень ОТСУТСТВУЕТ-элементов]. Рекомендация: дополнить design секцией с полным описанием."
   - All cells filled with quotes → OK

   **IMPORTANT:** The filled checklist table is the **proof** of this check. It MUST be included verbatim in the verification report (section "Полнота ручной конфигурации"). Writing "OK — design describes scenario" without the table is a verification failure.

7.6. **Quality Controller — Phase Coherence Review (MANDATORY)**

   **This step executes ALWAYS in pre-apply and mixed modes.** Domain-agnostic assessment of task ordering, dependencies, and execution risk. Complements the architect's realizability review (step 7.7).

   **Prepare repository state** (before calling the controller):
   For each task in tasks.md that mentions a file path or object name:
   - Glob the repository for the object/file
   - Record: exists / does not exist / exists but empty (e.g., Form.xml with only `<form>` root)
   - Record: if code file (`.bsl`) is non-empty while prerequisite tasks are still `- [ ]`

   **What to pass to the Quality Controller:**
   - Full text of: tasks.md, design.md, proposal.md
   - Paths to specs/ files
   - Checklist table from step 7.5 (if manual config markers were found), or "маркеров ручной конфигурации не найдено"
   - List of issues from steps 7A-7E (if any), or "механических замечаний нет"
   - Executability issues from step 7F (if any), or "замечаний выполнимости нет"
   - Repository state (object/file existence and emptiness list)

   **Quality Controller prompt** (use template from `1c-agent-patterns/SKILL.md`, section "Quality Controller — phase coherence review"):

   Call via `Task(subagent_type="openspec-quality-controller")`. Agent file: `.cursor/agents/openspec-quality-controller.md` (model: Opus, readonly). The controller evaluates 4 criteria:
   1. **Phase Classification** — classify every task as P0 (Infrastructure) / P1 (Specification-UI) / P2 (Implementation) / P3 (Integration) / P4 (Verification)
   2. **Dependency Graph** — explicit refs between tasks, artifact deps (task uses object from another task), phase deps (implicit P2→P0)
   3. **False Start Detection** — code exists but prerequisite task pending = CRITICAL; object exists but "create" task pending = WARNING
   4. **Rework Risk** — P2 task depends on incomplete P1 spec = HIGH risk; depends on hypothesis = MEDIUM risk

   **After receiving the controller's report:**
   1. Save full report to `reports/quality-control-YYYY-MM-DD.md`.
   2. Include verdict and phase classification table in the verification report (section "Фазовая когерентность (Quality Controller)").
   3. Map each alert to verification issues (затем **Actionability Gate**):
      - `false-start`, `phase-violation`, `cycle` → CRITICAL (Gate: обычно actionable — дефект постановки или кода)
      - `rework-risk` HIGH / MEDIUM:
        - Если в `tasks.md` зависимости между затронутыми задачами **явно заданы** и **не противоречат** графу QC → переклассифицировать в **INFO** (риск снимается соблюдением порядка apply; пользователю нечего менять в артефактах ради порядка)
        - Если зависимость **отсутствует** или **противоречит** графу → **WARNING** (нужна правка tasks/design)
      - `missing-dependency` → WARNING (actionable: дополнить tasks)
      - `missing-phase-gate` → SUGGESTION
      - `phase-gate-blocked`, `task-validity-drift` → WARNING (phase-transition), затем Gate
      - `ordering-mismatch`, `iteration-drift`, `phase-gate-named-task-blocked`, `phase-gate-stale-ref`, `execution-order-contradiction`:
        - Если граф зависимостей в tasks **согласован** с топологическим порядком — **INFO**; иначе **WARNING**
      - `ordering-cosmetic` → SUGGESTION

7.6b. **Phase Transition Review (phase-transition mode ONLY)**

   **This step executes ONLY in phase-transition mode.** Assesses whether remaining tasks are still valid after completing the current phase.

   **Context to collect:**
   - Completed tasks (current phase): list from tasks.md marked `[x]` that belong to the phase just finished (tasks before the last crossed phase-gate)
   - Upcoming tasks (next phases): list from tasks.md marked `[ ]` that follow the next `<!-- phase-gate -->`
   - debug.md (if exists): implementation issues discovered during the phase
   - Recent architecture/exploration reports in change `reports/`

   **Quality Controller call (enhanced):**
   Pass the same inputs as step 7.6, plus:
   - "Mode: phase-transition"
   - "Completed phase tasks: [list]"
   - "Upcoming phase tasks: [list]"
   - "Implementation notes (debug.md): <content or 'none'>"
   QC evaluates criterion #5 (Phase Gate Review) in addition to standard criteria. Use template from `1c-agent-patterns/SKILL.md` (QC prompt with optional phase-transition context block).

   **Порядок:** enhanced QC (абзац выше) MUST завершиться **до** вызова Architect phase-transition (аналогично запрету параллели 7.6/7.7).

   **Architect call (phase-transition focus):**
   Use template from `1c-agent-patterns/SKILL.md`, section "Architect — phase transition review (verify шаг 7.6b)".
   Pass: tasks.md, design.md, proposal.md, path to debug.md, paths to recent reports.
   Focus: are upcoming tasks still valid given implementation results? Any design drift? Need restructuring?
   Save architect result to `reports/phase-transition-YYYY-MM-DD.md`.

7.7. **Task Readiness Architect Review (MANDATORY)**

   **Порядок выполнения:** шаг **7.6** (Quality Controller) MUST завершиться **до** запуска шага **7.7** (Architect). Архитектор получает результат QC (фазовая таблица и alerts из 7.6) как входной параметр. **Параллельный** запуск QC (7.6) и Architect (7.7) **запрещён** (оптимизация по latency не оправдывает нарушение зависимости).

   **This step executes ALWAYS in pre-apply and mixed modes.** It is not remediation — it is part of the verification pipeline. The architect provides the expert holistic assessment that mechanical checks cannot.

   **What to pass to the architect:**
   - Full text of: tasks.md, design.md, proposal.md
   - Paths to specs/ files (architect reads them)
   - Checklist table from step 7.5 (if manual config markers were found), or "маркеров ручной конфигурации не найдено"
   - List of issues from steps 7A-7E (if any), or "механических замечаний нет"
   - Executability issues from step 7F (if any), or "замечаний выполнимости нет"
   - Quality Controller result: phase classification table and alerts from step 7.6 (or "Quality Controller замечаний нет")

   **Architect prompt** (use template from `1c-agent-patterns/SKILL.md`, section "Architect — task readiness review (verify шаг 7.7)"):

   ```
   ## Задача

   Оцени готовность ЗНИ `<name>` к реализации. Не детали кода — целостная оценка:
   можно ли по этим артефактам реализовать ЗНИ силами агентов (writer, form-generator)
   и пользователя (ручная конфигурация) без возвратов на уточнение?

   ## Артефакты

   - proposal: <путь>
   - design: <путь>
   - tasks: <путь>
   - specs: <путь>
   - Чеклист ручной конфигурации (verify, шаг 7.5): <чеклист-таблица или «маркеров не найдено»>
   - Замечания механических проверок (verify, шаги 7A-7E): <список или «замечаний нет»>
   - Фазовая когерентность (verify, шаг 7.6 Quality Controller): <фазовая таблица и alerts или «замечаний нет»>

   ## Критерии оценки

   Для каждого критерия — вердикт (OK / GAP) и краткое обоснование:

   1. **Реализуемость кодовых задач.** Может ли writer (1С-разработчик по промпту)
      реализовать каждую задачу из tasks.md, имея только design.md + spec + текст задачи?
      Есть ли задачи, где непонятно ЧТО делать или ГДЕ делать?

   2. **Реализуемость форм и метаданных.** Может ли form-generator построить каждую форму
      по описанию в design? Может ли пользователь создать каждый объект метаданных
      без дополнительных вопросов? Для форм: описаны ли элементы (группы, поля,
      таблицы, команды), UX-сценарий?

   3. **Разрешённость решений.** Все ли «или»/«/» разрешены? Есть ли неопределённые
      контракты возврата? Есть ли задачи с двумя путями реализации без выбора?

   4. **Полнота покрытия.** Покрывают ли задачи все requirements из spec?
      Есть ли пробелы — требование описано, но задачи на него нет?

   5. **Согласованность.** Нет ли противоречий между tasks и design? Между tasks и spec?
      Совпадают ли «создать/доработать» в tasks с реальным состоянием репозитория?

   6. **Качество фиксов (Fix Quality).** Для каждой задачи в tasks.md, помеченной как исправление
      (RCA, корневая причина, «исправление»): (a) Фикс направлен на корневую причину, а не на симптом?
      (b) Есть ли более «здоровые» альтернативы (меньше условий, одна точка изменения, без обходных флагов)?
      (c) Нет ли признаков заплатки (обход, дублирование, assumption-driven)? (d) Учтён ли UX-сценарий
      (что видит/делает пользователь после фикса)?

   ## Формат ответа

   ### Вердикт

   ГОТОВО / ГОТОВО С ЗАМЕЧАНИЯМИ / НЕ ГОТОВО

   ### Оценка по критериям

   | # | Критерий | Вердикт | Обоснование |
   |---|----------|---------|-------------|
   | 1 | Реализуемость кодовых задач | OK/GAP | ... |
   | 2 | Реализуемость форм и метаданных | OK/GAP | ... |
   | 3 | Разрешённость решений | OK/GAP | ... |
   | 4 | Полнота покрытия | OK/GAP | ... |
   | 5 | Согласованность | OK/GAP | ... |
   | 6 | Качество фиксов (Fix Quality) | OK/GAP | ... |

   ### Пробелы (только при GAP)

   Для каждого GAP:
   - Задача / артефакт
   - Что отсутствует / неоднозначно
   - Рекомендация (что дополнить, где)

   НЕ НУЖНО: ревью архитектуры, оценка рисков, альтернативные подходы.
   Только: можно ли реализовать as-is.
   ```

   **After receiving the architect's report:**
   1. Save full report to `reports/task-readiness-review-YYYY-MM-DD.md`.
   2. Include verdict and criteria table in the verification report (section "Готовность к реализации (архитектор)").
   3. Map each GAP to verification issues:
      - "Не реализуемо без уточнения" → CRITICAL
      - "Можно реализовать, но субоптимально / неоднозначно" → WARNING

7.8. **TZ Generation (conditional in pre-apply / mixed)**

   Generates a human-readable technical specification (ТЗ) document from change artifacts. The TZ serves as a functional requirements artifact oriented at stakeholder review. Gaps in TZ generation reveal gaps in source artifacts.

   **Порог обязательности (только для режимов pre-apply и mixed):**
   - Подсчитать в `tasks.md` строки с `- [ ]` и `- [x]` (каждая строка задачи с чекбоксом = одна задача).
   - **4 и более** задач → ТЗ **генерируется обязательно** (выполнить **Logic** ниже).
   - **1–3** задачи → ТЗ **не генерировать**, если пользователь **явно** не запросил ТЗ в том же сообщении (фразы вроде «с ТЗ», «сгенерируй ТЗ», «нужно ТЗ», «включи ТЗ») и не указывал отдельно `/opsx:doc-tz`. В отчёте verify: «ТЗ: не генерировалось (3 или менее задач по чекбоксам). При необходимости: `/opsx:doc-tz <name>`.» Перейти к шагу 9 без записи `ТЗ.md`.
   - **0** задач с чекбоксами (например, только bare-строки) → трактовать как «меньше порога»; ТЗ не генерировать, если нет явного запроса.
   - **Явный запрос ТЗ** в сообщении пользователя → генерировать **независимо** от количества задач.

   **Перезапись `ТЗ.md`:** если файл уже существует — **перезаписывать** только при фактической генерации в этом прогоне (порог выполнен или явный запрос). Если генерация **пропущена** по порогу — **сохранить** существующий `ТЗ.md` без изменений; в отчёте: «ТЗ: существующий файл сохранён (ниже порога обязательности / генерация не требовалась).»

   **Режимы post-apply и phase-transition:** при чистом post-apply (все задачи `[x]`) шаг 7.8 обычно не применяется; если verify запускается в **mixed**, использовать тот же подсчёт задач по всему `tasks.md`.

   **Logic:** (выполнять только если генерация ТЗ обязательна или запрошена по правилам выше)
   1. Read the TZ prompt from `.cursor/skills/openspec-docs/prompts/change-tz.md`
   2. Read all change artifacts: proposal.md, design.md, specs/\*/spec.md, latest `reports/architecture-*.md` (if any), latest `reports/exploration-*.md` (if any). Optionally `openspec/project.md` for product context.
   3. Apply the prompt to generate the TZ document. The TZ is generated by the orchestrator (not a subagent) — this is cheaper than full `/opsx:doc-tz` with architect review.
   4. **Verify completeness**: for each TZ section defined in the prompt template:
      - If the section is filled with substantive content from artifacts → OK
      - If a section cannot be filled (data absent in artifacts) → WARNING with indication of which artifact is incomplete
      - If "Проблема" section is empty (no Why in proposal) → WARNING: "proposal.md не содержит обоснования (секция Why)"
      - If "Критерии приёмки" section is empty (no scenarios in spec) → WARNING: "spec не содержит сценариев для критериев приёмки"
   5. Run the prompt's built-in "Верификация артефактов" checks (contradictions, defaults analysis, completeness)
   5b. **Lexicon check**: read Grep patterns from `.cursor/docs/tz-lexicon-dictionary.md` (section "Grep-паттерны"). Run Grep on the generated TZ text.
      - Matches found → WARNING: "ТЗ содержит нарушения лексики: [found words]. Рекомендация: заменить на русские эквиваленты из словаря (`.cursor/docs/tz-lexicon-dictionary.md`) или перегенерировать ТЗ (`/opsx:doc-tz <name>`)."
      - No matches → OK
   6. Save TZ to `openspec/changes/<name>/ТЗ.md`
   7. Add TZ generation remarks (if any) to the verification report

   **Report section:** `### ТЗ (функциональные требования)` — status (generated / generated with warnings / skipped threshold / skipped — user N/A), file path, list of gaps if any.

   Если шаг 7.8 пропущен по порогу — в отчёте указать статус **skipped (threshold)** и не выполнять пункты 4–5b Logic для ТЗ.

9. **Architect Gate Check**

   Check triggers from `architect-gate.mdc`:

   **Objective markers:**
   - Glob `reports/trace-analysis-*.md` in change dir — trace-analyst was used?
   - Glob `reports/exploration-*.md` in change dir — explorer was used?
   - Grep design.md for bug fix markers: `исправь`, `ошибка`, `баг`, `fix`, `crash`, `не работает`, `падает`
   - Grep design.md for: `базовая процедура`, `платформа`, `повторная запись`, `перехват`, `после вызова базы`, `компенсация`
   - Grep design.md for new metadata: `новый регистр`, `создать регистр`, `новый документ`, `создать документ`, `новый справочник`, `создать справочник`, `новый БП`, `создать БП`

   **Semantic triggers:**
   - Grep design.md for: `&Вместо`, `&После`, `&Перед`
   - Check if design mentions alternative approaches without resolution
   - Grep design.md for missing `## Existing Mechanisms` when integration is described
   - Grep design.md for missing `## Design Rationale` when integration is described

   **Structural triggers:**
   - Count distinct files in tasks.md — >1 file affected?
   - Estimate total lines of change — >10 lines?

   **Gate closure check:**
   - Glob `reports/architecture-*.md` in change dir and `temp/reports/`

   **Debug fix check (дополнительно):**
   - Grep tasks.md на маркеры: `(исправление)`, `RCA:`, `корневая причина`, `reports/trace-analysis`, `reports/exploration`
   - Если маркеры найдены И нет ни одного `reports/architecture-*.md` в change dir (в т.ч. `architecture-debug-*.md`):
     → CRITICAL: "В tasks.md есть задачи-исправления из debug без архитектурного ревью. Рекомендация: запустить onec-code-architect или /opsx:debug с прохождением Architect Gate (шаг 5.5)."

   **Result:**
   - No triggers fired AND (no debug fix markers OR architecture-*.md exists) → `OK`
   - Triggers fired AND `architecture-*.md` exists → `OK (отчёт: <filename>)`
   - Triggers fired AND NO `architecture-*.md` → CRITICAL: "Сработали маркеры Architect Gate: [list]. Архитектурный анализ не найден. Рекомендация: запустить `/opsx:verify` с опцией устранения или onec-code-architect вручную"
   - Debug fix markers in tasks AND NO `architecture-*.md` → CRITICAL (см. Debug fix check выше)

10. **Design Review Gate Check**

   Check triggers from `architect-gate.mdc` (DESIGN REVIEW section):
   1. Glob `reports/trace-analysis-*.md` + `reports/exploration-*.md` — total >= 2?
   2. Grep design.md / proposal.md for bug fix markers
   3. Grep design.md / proposal.md for `&ИзменениеИКонтроль`
   4. Grep tasks.md for conditional branching: `При отрицательн`, `Если в п.`, `Альтернатив`, `workaround`, `Иначе →`, `Иначе —`
   5. Grep design.md for `вероятно`, `возможно`, `скорее всего`, `гипотеза` without `## Hypotheses` section
   6. Grep tasks.md for manual config markers (`создать в расширении`, `добавить форму`, `создать обработку`, `создать регистр`, `добавить реквизит`, `создать справочник`) + check design.md for exhaustive instructions (names, types, form elements). If tasks require manual config but design lacks full description → trigger fires

   **Gate closure check:**
   - Glob `reports/design-review-*.md` in change dir

   **Result:**
   - No triggers fired → `OK`
   - Triggers fired AND `design-review-*.md` exists → `OK (отчёт: <filename>)`
   - Triggers fired AND no review → WARNING: "Сработали маркеры Design Review: [list]. Ревью постановки не проводилось. Рекомендация: запустить ревью"

11. **TZ Review Check**

    - Если шаг 7.8 был **пропущен по порогу** — статус `N/A` (ТЗ не генерировалось); не добавлять SUGGESTION «ТЗ создано, но ревью не проводилось».
    - Glob `ТЗ.md` in change dir
    - If not found → `N/A` (skip)
    - If found:
      - **Lexicon check**: read Grep patterns from `.cursor/docs/tz-lexicon-dictionary.md`. Grep `ТЗ.md` for matches.
        - Matches found → WARNING: "В ТЗ обнаружены нарушения лексики: [words]. Рекомендация: `/opsx:doc-tz <name>` или ручная правка."
        - No matches → OK (lexicon)
      - Glob `reports/tz-review-*.md` in change dir
      - If no review report → SUGGESTION: "ТЗ создано, но ревью не проводилось"
      - If review report exists:
        - Grep report for severity markers: `критично`, `обязательно`, `CRITICAL`, `HIGH`
        - If high-severity remarks found → WARNING: "ТЗ содержит неустранённые замечания уровня [severity]"
        - If no high-severity → `OK`

12. **Project Constraints Check**

    Read `openspec/project.md` and extract allowed directories (e.g., `cfe/` only, not `cf/`).
    For each task in tasks.md that mentions a file path:
    - Check if path is within allowed directories
    - If path is outside → CRITICAL: "Задача N.M ссылается на `<path>`, что за пределами разрешённых директорий (project.md). Переписать задачу на расширение (cfe/)?"

---

## Post-apply checks (modes: post-apply, mixed)

In **mixed** mode, post-apply checks apply **only to tasks marked `[x]`**.

13. **Verify Completeness**

    **Task Completion**:
    - Parse checkboxes: `- [ ]` (incomplete) vs `- [x]` (complete)
    - Count complete vs total tasks
    - If incomplete tasks exist:
      - **post-apply mode (все задачи должны быть закрыты):** Add CRITICAL issue for each incomplete task; Recommendation: "Complete task: <description>" or "Mark as done if already implemented"
      - **mixed mode:** незавершённые `[ ]` задачи — **не** CRITICAL/WARNING. Добавить **INFO**: «N задач с `[ ]` ожидают реализации через `/opsx:apply`» (Actionability Gate: следствие режима, не дефект верификации)

    **Spec Coverage**:
    - If delta specs exist in `openspec/changes/<name>/specs/`:
      - Extract all requirements (marked with "### Requirement:")
      - **mixed mode:** проверять покрытие **только** для требований, которые **целиком** относятся к уже выполненным `[x]` задачам (по смысловому сопоставлению tasks ↔ spec). Требования, относящиеся к невыполненным задачам — **INFO**: «M requirements ожидают реализации (связанные задачи `[ ]`)»
      - **post-apply mode:** для каждого requirement — поиск в коде; если не реализовано → CRITICAL: "Requirement not found: <requirement name>"
      - Для **mixed**, если requirement относится к `[x]`-задачам, но реализация не найдена → **WARNING** (расхождение: задача отмечена выполненной, код/spec не сходятся)

14. **Verify Correctness**

    **Requirement Implementation Mapping**:
    - **mixed mode:** выполнять **только** для требований/частей spec, отнесённых к задачам с `[x]`. Для остальных — не выдавать WARNING «не реализовано»; при необходимости одна **INFO**-строка в духе «сценарии невыполненных задач не проверялись в коде»
    - For each requirement from delta specs (в **post-apply** — все; в **mixed** — только связанные с `[x]`):
      - Search codebase for implementation evidence
      - If found, note file paths and line ranges
      - Assess if implementation matches requirement intent
      - If divergence detected:
        - Add WARNING: "Implementation may diverge from spec: <details>"
        - Recommendation: "Review <file>:<lines> against requirement X"

    **Scenario Coverage**:
    - **mixed mode:** для сценариев, относящихся к **невыполненным** задачам — **INFO** или пропуск, не WARNING
    - For each scenario in delta specs (marked with "#### Scenario:") — в **post-apply** полный проход; в **mixed** только сценарии для `[x]`-контекста:
      - Check if conditions are handled in code
      - Check if tests exist covering the scenario
      - If scenario appears uncovered **и** задачи для него уже `[x]`:
        - Add WARNING: "Scenario not covered: <scenario name>"
        - Recommendation: "Add test or implementation for scenario: <description>"

15. **Verify Coherence**

    **Design Adherence**:
    - If design.md exists in contextFiles:
      - Extract key decisions (look for sections like "Decision:", "Approach:", "Architecture:")
      - Verify implementation follows those decisions
      - If contradiction detected:
        - Add WARNING: "Design decision not followed: <decision>"
        - Recommendation: "Update implementation or revise design.md to match reality"
    - If no design.md: Skip design adherence check, note "No design.md to verify against"

    **Code Pattern Consistency**:
    - Review new code for consistency with project patterns
    - Check file naming, directory structure, coding style
    - If significant deviations found:
      - Add SUGGESTION: "Code pattern deviation: <details>"
      - Recommendation: "Consider following project pattern: <example>"

---

## Actionability Gate (перед записью замечаний в отчёт)

Применяется **ко всем** замечаниям перед финальным присвоением severity в отчёте verify (после сбора результатов шагов 6–15, 7.6, 7.7 и т.д.).

**Цель:** пользователь, запускающий verify, видит **WARNING/CRITICAL** только там, где нужно **решение или правка артефакта до apply**; всё остальное — контекст, а не «угроза».

**Уровень INFO** (контекст):

- Не входит в счётчики вердикта (N CRITICAL / M WARNING / K SUGGESTION).
- **Не** триггерит предложение remediation (шаг 17).
- В сообщении пользователю — **компактно** (bullet-строки в секции «К сведению»), **без** карточек решений.
- Формат в отчёте: `- [INFO] <краткий текст>`.

**Тест для каждого кандидата в CRITICAL / WARNING / SUGGESTION:**

| Шаг | Вопрос | Если да → |
|-----|--------|------------|
| 1 | Пользователь может устранить **правкой артефакта** (proposal/design/spec/tasks) **до** старта apply? | Присвоить severity по правилам соответствующего шага verify. |
| 2 | Замечание **полностью снимается** автоматикой (`/opsx:apply`, phase gates, явные **Зависимости:** в tasks)? | **INFO** (или не включать в отчёт, если дублирует очевидное). |
| 3 | Замечание — **неизбежное следствие режима** (pre-apply / mixed: код ещё не реализован по невыполненным `[ ]`)? | **INFO** (например: «K задач ожидают реализации»), не WARNING. |

**Склеивание:** если после Gate не осталось CRITICAL и WARNING, но есть SUGGESTION — статус «Готов. Предложения к сведению». Если нет ни CRITICAL, ни WARNING, ни SUGGESTION — «Все проверки пройдены. Готов к apply/archive». При наличии INFO добавить в Executive Summary строку: `**Контекст (INFO):** K пометок — см. секцию в отчёте` (только если K > 0).

## Issue Classification (mechanical / judgment)

После Actionability Gate каждое замечание с severity CRITICAL / WARNING / SUGGESTION дополнительно классифицируется для маршрутизации в Phase A (авто-исправление) или Phase B (карточки решений). Классификация определяет **кто** принимает решение: машина или пользователь.

**Критерий mechanical:** исправление детерминировано (однозначная замена), не меняет scope / логику / порядок задач, обратимо через git.

**Критерий judgment:** правка меняет scope, порядок, подход, архитектуру или контракт — решение пользователя приведёт к **разному коду** при apply.

| Тип замечания | Класс | Обоснование |
|---|---|---|
| Missing checkboxes (6A) | mechanical | Формат, не меняет содержание |
| TZ lexicon violation (7.8 / 11) | mechanical | Замена слов по реестру, детерминировано |
| Repo Consistency wording (7E) | mechanical | `создать X` → `доработать X` при доказанном существовании объекта |
| Task quality — ambiguity, missing details (7B / 7C) | judgment | Architect может переформулировать scope |
| Architect Gate not closed (9) | judgment | Архитектурный отчёт может изменить подход |
| Design Review not done (10) | judgment | Ревью может выявить пробелы в design |
| Phase violation / false start (QC 7.6) | judgment | Переупорядочивание меняет что делается первым |
| Executability issues (7F) | judgment | Зависимости влияют на порядок реализации |
| Rework risk (QC 7.6) | judgment | Вопрос: сначала спецификация или сразу код |
| Missing phase gates (QC) | judgment | Структура фаз меняет точки остановки |
| Project constraints violation (12) | judgment | Меняет целевые каталоги |
| TZ generation gaps (7.8) | footnote | ТЗ — документ для заказчика, не для apply |
| TZ review remarks (11) | footnote | Не влияет на реализацию |
| Incomplete tasks (post-apply, 13) | footnote | Рекомендация `/opsx:apply` |
| Spec/design divergence (post-apply, 15) | footnote | Информационное расхождение |

**Класс footnote:** замечания с severity SUGGESTION, не влияющие на ход реализации. Показываются пользователю в секции «К сведению» (одна строка каждое) — не как карточка решения и не как авто-исправление.

---

## Report and remediation

16. **Generate Verification Report**

    **Executive Summary (обязательная первая секция отчёта):**

    ```
    ## Executive Summary

    **Вердикт:** N CRITICAL, M WARNING, K SUGGESTION
    **Контекст (INFO):** <число> пометок — см. секцию «Контекст (INFO)» ниже *(только если INFO > 0; иначе строку опустить)*
    **Решений от пользователя:** <число> — <перечень решений или «не требуется»>
    **Статус:** <одна фраза>
    ```

    Правила заполнения:
    - Счётчики **Вердикта** учитывают только CRITICAL / WARNING / SUGGESTION. **INFO не входят** в N, M, K.
    - CRITICAL > 0 → Статус: «Блокировано до устранения: [перечень CRITICAL]»
    - Только WARNING (INFO допускаются) → Статус: «Готов при принятии рисков: [перечень WARNING]»
    - Только SUGGESTION (INFO допускаются) → Статус: «Готов. Предложения к сведению»
    - Нет CRITICAL, нет WARNING, нет SUGGESTION (возможны только INFO) → Статус: «Все проверки пройдены. Готов к apply/archive»
    - «Решений от пользователя» — перечислить конкретные решения, которые не может принять машина (выбор подхода, отложить/реализовать задачу, принять риск). Если таких нет — «не требуется». INFO **не** считаются запросом решения.

    **Summary Scorecard (после Executive Summary):**
    ```
    ## Verification Report: <change-name>
    ### Режим: pre-apply | mixed | post-apply | phase-transition

    ### Формат артефактов
    | Проверка | Статус |
    |---|---|
    | Чекбоксы `- [ ]` | OK / CRITICAL (N строк без чекбоксов) |
    | Нумерация N.M | OK / WARNING |
    | Заголовки групп | OK / SUGGESTION |

    ### Качество задач
    - [CRITICAL] N.M — нет пути к файлу, нет критериев приёмки
    - [WARNING] N.M — размытость: «или аналог ...»
    - [WARNING] N.M — «создать X», но X уже существует (repo consistency)
    - [SUGGESTION] N.M — рекомендуется разбить на 2 задачи
    ...

    ### Выполнимость и порядок задач (verify 7F, QC 5d)
    - [INFO] порядок N.M → M.K обеспечен явными **Зависимостями:** в tasks (не требует действий пользователя до apply)
    - [WARNING] N.M — нет явной зависимости от M.K при выявленной потребности — дополнить tasks.md
    - [SUGGESTION] N.M — расположен до зависимости M.K в файле (при этом граф может быть OK)
    - [WARNING] Phase Gate: задача N.M [ ], K.L [ ] (именованы в маркере gate)
    - [SUGGESTION] «Порядок выполнения» не покрывает задачи: [list]
    (или: замечаний выполнимости нет)

    ### Контекст (INFO)

    Список всех INFO-строк (после Actionability Gate). Без развёрнутых абзацев. Пример:
    - [INFO] K задач с `[ ]` ожидают реализации (mixed)
    - [INFO] Цепочка 4.1→4.2 объявлена в tasks; apply соблюдает порядок

    ### Полнота ручной конфигурации (чеклист шага 7.5)

    **Задача N.M** — маркер: `создать обработку` — тип: Metadata

    | Элемент | Требование | Цитата из design / статус |
    |---|---|---|
    | Имя объекта | Точное имя | «КД_НастройкаМЧД» |
    | Реквизиты | Имя, тип, длина | ... или `ОТСУТСТВУЕТ` |
    | Подсистема | Куда включить | ... или `ОТСУТСТВУЕТ` |

    **Задача N.M** — маркер: `добавить форму` — тип: Form

    | Элемент | Требование | Цитата из design / статус |
    |---|---|---|
    | Группы | Перечень групп | ... или `ОТСУТСТВУЕТ` |
    | Поля | Имя, тип, привязка | ... или `ОТСУТСТВУЕТ` |
    | Таблицы | Имя, колонки | ... или `ОТСУТСТВУЕТ` |
    | Команды/кнопки | Перечень, действия | ... или `ОТСУТСТВУЕТ` |
    | UX-сценарий | Шаги пользователя | ... или `ОТСУТСТВУЕТ` |

    (повторить для каждого маркера; при отсутствии маркеров — «маркеров не найдено»)

    ### Фазовая когерентность (Quality Controller)

    **Вердикт:** OK / WARNING / CRITICAL
    **Полный отчёт:** reports/quality-control-YYYY-MM-DD.md

    | Задача | Фаза | Зависит от | Статус |
    |--------|------|-----------|--------|
    | 1.1    | P0   | -         | OK     |
    | 2.1    | P1   | 1.1       | OK     |
    | 3.1    | P2   | 1.1       | OK     |
    ...

    Alerts:
    - [CRITICAL] false-start: задача N.M (P2) — код существует, но предшественник K.L (P0) не завершён
    - [WARNING] rework-risk: задача N.M (P2) зависит от незавершённой спецификации P1
    ...

    ### Phase Transition Review (phase-transition only)

    **Текущая фаза:** N (завершена)
    **Следующая фаза:** N+1

    | Проверка | Статус |
    |---|---|
    | Актуальность задач следующей фазы | OK / WARNING |
    | Design drift | OK / WARNING |
    | Необходимость перепроектирования | Нет / Да (рекомендация) |

    Детали: см. reports/phase-transition-YYYY-MM-DD.md и quality-control (критерий #5).

    ### Готовность к реализации (архитектор)

    **Вердикт:** ГОТОВО / ГОТОВО С ЗАМЕЧАНИЯМИ / НЕ ГОТОВО
    **Полный отчёт:** reports/task-readiness-review-YYYY-MM-DD.md

    | # | Критерий | Вердикт |
    |---|----------|---------|
    | 1 | Реализуемость кодовых задач | OK / GAP |
    | 2 | Реализуемость форм и метаданных | OK / GAP |
    | 3 | Разрешённость решений | OK / GAP |
    | 4 | Полнота покрытия | OK / GAP |
    | 5 | Согласованность | OK / GAP |

    Пробелы:
    - [CRITICAL/WARNING] ...

    ### ТЗ (функциональные требования)

    **Статус:** сгенерировано / сгенерировано с замечаниями / пропущено (порог задач) / пропущено (явный запрос не был)
    **Файл:** ТЗ.md (или «не создавался»)

    | Проверка | Статус |
    |---|---|
    | Лексика ТЗ | OK / WARNING (N нарушений) |

    Замечания (при наличии):
    - [WARNING] proposal.md не содержит обоснования (секция Why)
    - [WARNING] spec не содержит сценариев для критериев приёмки
    ...

    ### Gates
    | Gate | Статус | Детали |
    |---|---|---|
    | Architect Gate | OK / CRITICAL | триггеры: [...] |
    | Design Review | OK / WARNING | триггеры: [...] |
    | ТЗ Review | OK / N/A / WARNING | |
    | Project Constraints | OK / CRITICAL | |

    ### Полнота реализации (post-apply)
    | Проверка | Статус |
    |---|---|
    | Задачи | X/Y выполнено |
    | Требования spec | M/N покрыто |

    ### Корректность (post-apply)
    - [WARNING] ...

    ### Согласованность (post-apply)
    - [WARNING] ...
    - [SUGGESTION] ...

    ### Авто-исправлено (Phase A)

    | # | Что | Было | Стало |
    |---|-----|------|-------|
    | 1 | Чекбоксы | N строк без `[ ]` | Исправлено |
    | 2 | ... | ... | ... |
    (или: «mechanical-замечаний не обнаружено»)

    ### Итог
    N CRITICAL, M WARNING, K SUGGESTION (INFO в счётчик не входят; при необходимости отдельно: «INFO: R»).

    ### Развёрнутые объяснения замечаний

    **Обязательно** в **файле** отчёта, если есть **хотя бы одно** замечание (CRITICAL / WARNING / SUGGESTION). Если таких нет — секция: «Замечаний нет (INFO см. выше / в секции Контекст).»

    **INFO** в эту секцию **не** включаются развёрнуто — только перечень в «Контекст (INFO)».

    Формат (нумерация сквозная по всем severity, сначала CRITICAL, затем WARNING, затем SUGGESTION): заголовки уровня 4 `#### CRITICAL N — …`, `#### WARNING N — …`, `#### SUGGESTION N — …`; под каждым — абзац (для CRITICAL/WARNING 3–5 предложений; для SUGGESTION 1–2 предложения).

    **Связь с сообщением пользователю:** файл отчёта содержит развёрнутые абзацы (полная запись); сообщение пользователю использует формат **карточек решений** для judgment-замечаний (см. шаг 17). Это разные форматы — файл как долгосрочная память, карточки как инструмент принятия решений.

    См. `.cursor/rules/verify-user-communication.mdc` — правила 2, 3, 7, 8.
    ```

    **Сообщение пользователю** формируется на шаге 17 после Phase A (авто-исправление механических замечаний). Формат карточек решений — см. шаг 17.

    Коммуникация с пользователем: `.cursor/rules/verify-user-communication.mdc`

16a. **Phase A — Mechanical auto-fix (silent)**

    Выполняется **сразу после** генерации отчёта, **до** показа результатов пользователю. Без вопросов и подтверждений.

    **Правило:** применяются **только** замечания с классом `mechanical` (см. Issue Classification).

    **Действия:**

    | Замечание | Действие |
    |---|---|
    | Missing checkboxes (6A) | StrReplace: `- N.M` → `- [ ] N.M` для каждой строки без чекбокса |
    | TZ lexicon violation (7.8 / 11) | StrReplace запрещённых слов в `ТЗ.md` по `.cursor/docs/tz-lexicon-dictionary.md` |
    | Repo Consistency wording (7E) | StrReplace: `создать X` → `доработать X` / `наполнить содержимым` в tasks.md |

    **Ре-верификация Phase A:**
    После всех mechanical-исправлений перезапустить **только** затронутые проверки (шаги 6–7E) на изменённых файлах. QC и Architect **не** перезапускаются на Phase A (механические правки не меняют scope).

    Результат Phase A записать в отчёт: секция `### Авто-исправлено (Phase A)` с таблицей Before/After.

17. **Phase B — Show results + Judgment decision cards**

    **INFO** не участвуют в remediation и не показываются как карточки.
    **Footnote**-замечания (см. Issue Classification) показываются в секции «К сведению» — одна строка каждое.

    **Формат сообщения пользователю (обязательный):**

    **Блок 1 — Авто-исправлено (Phase A):**
    Если Phase A (шаг 16a) выполнила хотя бы одно исправление:
    ```
    ## Авто-исправлено

    | # | Что | Было | Стало |
    |---|-----|------|-------|
    | 1 | Чекбоксы | 3 строки без `[ ]` | Исправлено |
    | 2 | Лексикон ТЗ | «парсинг» | «разбор» |
    ```
    Если Phase A не нашла mechanical-замечаний — блок опустить.

    **Блок 2 — Требует вашего решения (judgment-замечания):**
    Если есть замечания с классом `judgment` — показать **карточку решения** для каждого:
    ```
    ## Требует вашего решения (N)

    ### 1. <Заголовок> (<SEVERITY>)

    **Проблема:** <в чём конкретно дефект — 1 предложение>
    **Влияние на реализацию:** <что изменится при apply если не исправить — 1 предложение>
    **Варианты:**
      a) <конкретное действие> — <что получим>
      b) <альтернативное действие> — <что получим>
      c) Принять как есть — <чем рискуем>
    ```

    Три обязательных поля карточки:
    - **Проблема** — конкретный дефект (1 предложение, без общих слов)
    - **Влияние на реализацию** — как это повлияет на код / поведение при apply (1 предложение)
    - **Варианты** — 2–3 действия с последствиями; всегда есть «Принять как есть» с описанием риска

    **Действия по вариантам (judgment):**

    | Замечание | Варианты для карточки |
    |---|---|
    | Task quality (7B / 7C) | a) Запустить архитектора для доработки tasks.md b) Принять как есть — writer додумает |
    | Architect Gate not closed (9) | a) Запустить архитектурный анализ (→ `reports/architecture-verify-YYYY-MM-DD.md`) b) Принять как есть — реализация без архитектурного ревью |
    | Design Review not done (10) | a) Запустить ревью постановки (→ `reports/design-review-YYYY-MM-DD.md`) b) Принять как есть — возможны пробелы в design |
    | Phase violation / false start (QC 7.6) | a) Переупорядочить задачи по фазам b) Отметить реализованные как `[x]` c) Принять как есть |
    | Executability issues (7F) | a) Добавить `Зависимости:` в tasks b) Переупорядочить секции c) Принять — apply разберётся |
    | Rework risk (QC 7.6) | a) Завершить спецификацию P1 в design.md b) Принять — начать кодирование с риском переделки |
    | Missing phase gates (QC) | a) Запустить архитектора для реструктуризации (шаблон «Architect — phase gate restructuring» из `1c-agent-patterns/SKILL.md`) b) Принять — работать без phase gates |
    | Phase transition issues (7.6b) | a) Реструктурировать через архитектора b) Обновить design.md c) Принять как есть |
    | Project constraints violation (12) | a) Переписать задачи на разрешённые каталоги b) Обосновать исключение |

    Если judgment-замечаний нет — блок опустить.

    **Блок 3 — К сведению (footnote + INFO):**
    ```
    ## К сведению
    - ТЗ без ревью архитектора — при необходимости `/opsx:doc-tz <name>`
    - 6 задач ожидают реализации (mixed mode)
    ```
    Footnote-замечания и INFO — по одной строке. Если ни footnote, ни INFO нет — блок опустить.

    **Блок 4 — Вердикт:**
    ```
    ## Вердикт: <ГОТОВ / ГОТОВ С ОГОВОРКОЙ / БЛОКИРОВАНО>
    Решений от вас: N. Напишите номера выбранных вариантов (например: «1a, 2c»).
    Следующий шаг: `/opsx:apply <name>` или `/opsx:archive <name>`.
    ```

    Если judgment-замечаний нет → «Решений от вас не требуется».

    **Голые счётчики** («0 CRITICAL, 2 WARNING, 1 SUGGESTION») без карточек / таблиц — **запрещены**.

    **Примеры:**

    Хорошо (нет judgment-замечаний):
    ```
    ## Авто-исправлено

    | # | Что | Было | Стало |
    |---|-----|------|-------|
    | 1 | Чекбоксы | 2 строки без `[ ]` | Исправлено |

    ## К сведению
    - ТЗ сгенерировано без ревью — при необходимости `/opsx:doc-tz`

    ## Вердикт: ГОТОВ
    Решений от вас не требуется. Следующий шаг: `/opsx:apply <name>`.
    ```

    Хорошо (есть judgment):
    ```
    ## Авто-исправлено

    | # | Что | Было | Стало |
    |---|-----|------|-------|
    | 1 | Лексикон ТЗ | «парсинг» | «разбор» |

    ## Требует вашего решения (1)

    ### 1. Неоднозначность в задаче 3.1 (WARNING)

    **Проблема:** Задача 3.1 описывает «загрузку данных», но не указан формат
    файла и поведение при дублях — два допустимых пути реализации.
    **Влияние на реализацию:** Writer выберет формат произвольно; при приёмке
    возможно несовпадение с ожиданием.
    **Варианты:**
      a) Запустить архитектора для уточнения tasks.md — задача станет однозначной
      b) Принять как есть — writer примет решение, ревьювер проверит

    ## К сведению
    - 4 задачи ожидают реализации (mixed mode)

    ## Вердикт: ГОТОВ С ОГОВОРКОЙ
    Решений от вас: 1. Напишите номер варианта (например: «1a»).
    ```

    **17a. Mandatory re-verification after judgment remediation**

    После выполнения действий по выбранным вариантам judgment-карточек, если затронуто **содержимое** артефакта (`tasks.md`, `design.md`, `spec`, `proposal`):

    1. Перезапустить **только затронутые** механические проверки (шаги 6–7F) на изменённых артефактах.
    2. Если remediation затронула `tasks.md` и в этом прогоне уже выполнялся QC (шаг 7.6):
       - **Перезапустить QC** с обновлённым `tasks.md` (те же входы + пометка «re-run after remediation»).
       - Новые алерты QC → добавить в отчёт verify.
    3. Перезапуск Architect (шаг 7.7) **не обязателен**, если remediation **не** добавляла новые задачи и **не** меняла явные зависимости между задачами в `tasks.md`. Если добавлялись задачи или менялись зависимости — **перезапустить** шаг 7.7 с обновлёнными артефактами и свежим результатом QC (п.2).
    4. Обновить файл отчёта: секция `### Re-verification after remediation` — что перепроверено, новые алерты или «новых алертов нет».

    Без перезапуска затронутых проверок по п.1–2 (и п.3 при необходимости) remediation **не считается завершённой**.

    Phase A mechanical fixes **не** триггерят 17a (их ре-верификация выполнена в шаге 16a).

    **17b. Final verdict after judgment remediation**

    После выполнения judgment-действий и ре-верификации (17a) — финальное сообщение:

    ```
    ## Результат устранения

    | # | Замечание | Было | Стало | Что сделано |
    |---|-----------|------|-------|-------------|
    | 1 | <описание> | WARNING | OK | <действие> |

    ## Вердикт: ГОТОВ
    Решений от вас не требуется. Следующий шаг: `/opsx:apply <name>`.
    ```

    Если пользователь выбрал «Принять как есть» по некоторым карточкам:
    ```
    ## Принятые риски

    | # | Замечание | Риск |
    |---|-----------|------|
    | 1 | <описание> | <одно предложение — чем рискуем> |
    ```

    Коммуникация с пользователем: `.cursor/rules/verify-user-communication.mdc`

18. **Save verification report**

    Save the report to `reports/verification-<mode>-YYYY-MM-DD.md` in the change directory,
    where `<mode>` is `pre`, `mixed`, `post`, or `phase-N` (N = completed phase number when in phase-transition mode).

---

**Verification Heuristics**

- **Task Quality**: mechanical checks (Grep for markers, presence of sections) first; semantic assessment only for ambiguity
- **Completeness**: focus on objective checklist items (checkboxes, requirements list)
- **Correctness**: use keyword search, file path analysis, reasonable inference — don't require perfect certainty
- **Coherence**: look for glaring inconsistencies, don't nitpick style
- **False Positives**: when uncertain, prefer SUGGESTION over WARNING, WARNING over CRITICAL
- **Actionability**: every **CRITICAL / WARNING / SUGGESTION** must answer: «что пользователь меняет в артефактах или решает до apply?» Иначе → **INFO** (см. Actionability Gate). INFO допускаются без «рекомендации устранить» в стиле remediation
- **Two-phase remediation**: mechanical issues (deterministic, format-only) → silent auto-fix Phase A (шаг 16a); judgment issues (affect scope/order/approach) → decision cards Phase B (шаг 17). См. Issue Classification
- **INFO**: контекст режима и автоматики; не дублировать как WARNING только потому что задачи ещё `[ ]` или зависимости корректно объявлены

**Graceful Degradation**

- If only tasks.md exists: run format + quality checks; skip spec/design/gates checks
- If tasks + design exist: add gate checks
- If tasks + design + specs: full pre-apply + post-apply checks
- TZ is generated by verify (step 7.8) when task-count threshold or explicit user request is met; otherwise skipped; TZ Review gate (step 11) checks for prior ТЗ review reports when `ТЗ.md` exists
- Always note which checks were skipped and why

**Output Format**

Use clear markdown with:
- Tables for summary scorecards
- Grouped lists for issues (CRITICAL/WARNING/SUGGESTION); отдельный блок bullets для **INFO**
- Code references in format: `file.bsl:123`
- Specific, actionable recommendations
- No vague suggestions like "consider reviewing"

Коммуникация с пользователем: `.cursor/rules/verify-user-communication.mdc` — обязательные требования к Executive Summary, двухфазному remediation (Phase A mechanical auto-fix + Phase B judgment decision cards), карточкам решений, и явному указанию решений от пользователя.
