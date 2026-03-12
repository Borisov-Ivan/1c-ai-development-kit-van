---
name: openspec-verify-change
description: Universal quality gate for OpenSpec changes. Pre-apply — artifact quality, task specificity, gates. Post-apply — implementation completeness, correctness, coherence.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "3.0"
  generatedBy: "1.1.1"
---

Universal quality gate for OpenSpec changes. Works in two modes determined automatically:
- **Pre-apply**: artifact format, task quality, manual config checklist, **mandatory architect readiness review**, Architect Gate, Design Review, TZ Review, project constraints
- **Post-apply**: implementation completeness, correctness, coherence

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If multiple active changes: run `openspec list --json`, show changes that have tasks artifact, include schema, mark incomplete as "(In Progress)", and use **AskUserQuestion tool** to let user select

   Always announce: "Using change: <name>" and how to override (e.g., `/opsx:verify <other>`).

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
   | >0 | >0 | >0 | **mixed** |
   | >0 | >0 | 0 | **post-apply** |

   Announce mode to user:
   ```
   Режим: pre-apply (артефакты не реализованы)
   Режим: mixed (N/M задач выполнено — pre-проверки для оставшихся, post-проверки для выполненных)
   Режим: post-apply (все задачи выполнены)
   ```

5. **Initialize report structure**

   Create a report structure with sections:
   - **Artifact Format** (pre-apply, mixed)
   - **Task Quality** (pre-apply, mixed)
   - **Manual Configuration Sufficiency** (pre-apply, mixed) — structured checklist with proof
   - **Task Readiness (Architect)** (pre-apply, mixed) — mandatory architect holistic assessment
   - **Gates** (pre-apply, mixed): Architect Gate, Design Review, TZ Review, Project Constraints
   - **Completeness** (post-apply, mixed)
   - **Correctness** (post-apply, mixed)
   - **Coherence** (post-apply, mixed)

   Each section can have CRITICAL, WARNING, or SUGGESTION issues.

---

## Pre-apply checks (modes: pre-apply, mixed)

6. **Artifact Format Check**

   **6A. Task checkboxes:**
   - Every task line must have `- [ ]` or `- [x]` prefix
   - Scan for lines matching pattern `^- \d+\.\d+\s` (bare task without checkbox)
   - If bare tasks found:
     - Add CRITICAL: "Задачи без чекбоксов: N строк. apply/estimate/archive не смогут отслеживать прогресс"
     - Set `autofix_checkboxes = true` for step 12

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

7.6. **Task Readiness Architect Review (MANDATORY)**

   **This step executes ALWAYS in pre-apply and mixed modes.** It is not remediation — it is part of the verification pipeline. The architect (Opus model) provides the expert holistic assessment that mechanical checks cannot.

   **What to pass to the architect:**
   - Full text of: tasks.md, design.md, proposal.md
   - Paths to specs/ files (architect reads them)
   - Checklist table from step 7.5 (if manual config markers were found), or "маркеров ручной конфигурации не найдено"
   - List of issues from steps 7A-7E (if any), or "механических замечаний нет"

   **Architect prompt** (use template from `1c-agent-patterns/SKILL.md`, section "Architect — task readiness review"):

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

8. **Architect Gate Check**

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

   **Result:**
   - No triggers fired → `OK`
   - Triggers fired AND `architecture-*.md` exists → `OK (отчёт: <filename>)`
   - Triggers fired AND NO `architecture-*.md` → CRITICAL: "Сработали маркеры Architect Gate: [list]. Архитектурный анализ не найден. Рекомендация: запустить `/opsx:verify` с опцией устранения или onec-code-architect вручную"

9. **Design Review Gate Check**

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

10. **TZ Review Check**

    - Glob `ТЗ.md` in change dir
    - If not found → `N/A` (skip)
    - If found:
      - Glob `reports/tz-review-*.md` in change dir
      - If no review report → SUGGESTION: "ТЗ создано, но ревью не проводилось"
      - If review report exists:
        - Grep report for severity markers: `критично`, `обязательно`, `CRITICAL`, `HIGH`
        - If high-severity remarks found → WARNING: "ТЗ содержит неустранённые замечания уровня [severity]"
        - If no high-severity → `OK`

11. **Project Constraints Check**

    Read `openspec/project.md` and extract allowed directories (e.g., `cfe/` only, not `cf/`).
    For each task in tasks.md that mentions a file path:
    - Check if path is within allowed directories
    - If path is outside → CRITICAL: "Задача N.M ссылается на `<path>`, что за пределами разрешённых директорий (project.md). Переписать задачу на расширение (cfe/)?"

---

## Post-apply checks (modes: post-apply, mixed)

In **mixed** mode, post-apply checks apply **only to tasks marked `[x]`**.

12. **Verify Completeness**

    **Task Completion**:
    - Parse checkboxes: `- [ ]` (incomplete) vs `- [x]` (complete)
    - Count complete vs total tasks
    - If incomplete tasks exist (post-apply mode only):
      - Add CRITICAL issue for each incomplete task
      - Recommendation: "Complete task: <description>" or "Mark as done if already implemented"

    **Spec Coverage**:
    - If delta specs exist in `openspec/changes/<name>/specs/`:
      - Extract all requirements (marked with "### Requirement:")
      - For each requirement:
        - Search codebase for keywords related to the requirement
        - Assess if implementation likely exists
      - If requirements appear unimplemented:
        - Add CRITICAL issue: "Requirement not found: <requirement name>"
        - Recommendation: "Implement requirement X: <description>"

13. **Verify Correctness**

    **Requirement Implementation Mapping**:
    - For each requirement from delta specs:
      - Search codebase for implementation evidence
      - If found, note file paths and line ranges
      - Assess if implementation matches requirement intent
      - If divergence detected:
        - Add WARNING: "Implementation may diverge from spec: <details>"
        - Recommendation: "Review <file>:<lines> against requirement X"

    **Scenario Coverage**:
    - For each scenario in delta specs (marked with "#### Scenario:"):
      - Check if conditions are handled in code
      - Check if tests exist covering the scenario
      - If scenario appears uncovered:
        - Add WARNING: "Scenario not covered: <scenario name>"
        - Recommendation: "Add test or implementation for scenario: <description>"

14. **Verify Coherence**

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

## Report and remediation

15. **Generate Verification Report**

    **Summary Scorecard:**
    ```
    ## Verification Report: <change-name>
    ### Режим: pre-apply | mixed | post-apply

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

    ### Итог
    N CRITICAL, M WARNING, K SUGGESTION.
    ```

    **Final Assessment:**
    - CRITICAL issues present → "N критичных замечаний. Требуется устранение до apply/archive."
    - Only warnings → "Критичных замечаний нет. M предупреждений. Готов к apply/archive (с учётом замечаний)."
    - All clear → "Все проверки пройдены. Готов к apply/archive."

16. **Offer remediation**

    If any CRITICAL or WARNING issues found, offer:
    ```
    Устранить замечания?
    1. Да, автоматически (все, что возможно)
    2. Да, по одному (с подтверждением каждого)
    3. Нет, продолжить
    ```

    **Auto-remediation actions by issue type:**

    | Issue | Action |
    |---|---|
    | Missing checkboxes | Direct StrReplace: `- N.M` → `- [ ] N.M` for each bare task line |
    | Task quality (missing details, ambiguity) | Delegate to **onec-code-architect** with prompt: "Доработать tasks.md: устранить замечания [list]". Pass current tasks.md, design.md, proposal.md, specs/. Architect returns updated tasks.md |
    | Architect Gate not closed | Offer to run onec-code-architect for architecture review. Save report to `reports/architecture-verify-YYYY-MM-DD.md` |
    | Design Review not done | Offer to run onec-code-architect with design review focus. Save report to `reports/design-review-YYYY-MM-DD.md` |
    | Repo Consistency (WARNING from 7E) | Suggest rewriting task: «создать» → «доработать» / «наполнить содержимым» if object already exists |
    | TZ review remarks | Suggest `/opsx:doc-tz <name>` to regenerate TZ |
    | Project constraints violation | Suggest rewriting tasks to target allowed directories |
    | Incomplete tasks (post-apply) | List remaining tasks, suggest `/opsx:apply <name>` |
    | Spec/design divergence (post-apply) | Suggest updating artifact or implementation |

    After remediation, re-run affected checks and update report.

17. **Save verification report**

    Save the report to `reports/verification-<mode>-YYYY-MM-DD.md` in the change directory,
    where `<mode>` is `pre`, `mixed`, or `post`.

---

**Verification Heuristics**

- **Task Quality**: mechanical checks (Grep for markers, presence of sections) first; semantic assessment only for ambiguity
- **Completeness**: focus on objective checklist items (checkboxes, requirements list)
- **Correctness**: use keyword search, file path analysis, reasonable inference — don't require perfect certainty
- **Coherence**: look for glaring inconsistencies, don't nitpick style
- **False Positives**: when uncertain, prefer SUGGESTION over WARNING, WARNING over CRITICAL
- **Actionability**: every issue must have a specific recommendation with file/line references where applicable

**Graceful Degradation**

- If only tasks.md exists: run format + quality checks; skip spec/design/gates checks
- If tasks + design exist: add gate checks
- If tasks + design + specs: full pre-apply + post-apply checks
- If TZ absent: skip TZ review, don't flag
- Always note which checks were skipped and why

**Output Format**

Use clear markdown with:
- Tables for summary scorecards
- Grouped lists for issues (CRITICAL/WARNING/SUGGESTION)
- Code references in format: `file.bsl:123`
- Specific, actionable recommendations
- No vague suggestions like "consider reviewing"
