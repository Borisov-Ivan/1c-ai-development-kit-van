---
name: openspec-ff-change
description: Fast-forward through OpenSpec artifact creation. Use when the user wants to quickly create all artifacts needed for implementation without stepping through each one individually.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.1.1"
---

Fast-forward through artifact creation - generate everything needed to start implementation in one go.

**Input**: The user's request may include a change name (kebab-case), a description of what they want to build, or nothing (auto-detect from context).

**Output style:**
- Сводка в чате («что создано», ссылки на артефакты, следующий шаг) — шаблон **T-CONFIRM** из `.cursor/docs/opsx-output-style.md` §5.5.
- **Генерируемые артефакты** `proposal.md`, `design.md`, `tasks.md`, spec deltas — подчиняются §1 «Три слоя» и §3 «Запрет внутренних ID в пользовательских полях»: секции для заказчика/приёмки (`Why`, `What Changes`, `Scope`, `Scenarios`, `Requirements`) — UX-слой; внутренние ID (`S<N>.T<M>`, `D<N>`, `R<N>`, `I<N>`, номера задач `12.9`) — только в `## Slices`, `## Decisions`, `## Tasks`, `## Risks`. Перечисления — нумерованные списки. Перед записью — self-check-5 (§7).

**Steps**

1. **Determine change name**

   a. **If argument provided** — use it as change name (kebab-case). Proceed to step 2.

   b. **If no argument — auto-detect from context:**
      0. Glob `temp/intake-brief-*.md` (exclude `temp/intake-brief-example-*.md`). If found, read the most recent one (by date in filename).
         Extract change name from `### Рекомендованный следующий шаг` if it contains `/opsx:ff <name>` or derive kebab-case from `**Тема:**` / `### Нормализованная цель`.
         Extract brief from `### Нормализованная цель`, `### Scope`, and `### План исследования`.
         AskQuestion: «Из Intake Brief: `<name>`. Использовать?
         [Да / Другое имя / Сначала explore]».
         If the user chooses `Сначала explore`, stop and recommend `/opsx:explore @temp/intake-brief-...md`.
      1. Glob `temp/explore-summary-*.md`. If found, read the most recent one (by date in filename).
         Extract change name from line matching `Готово к созданию ЗНИ <name>`
         or derive kebab-case from `**Тема:**`.
         Extract `Architect Gate`, `Ключевые решения`, `Knowledge findings`, and `Рекомендации по срезам` into `exploreContext`. This context is authoritative input for `proposal`, `design`, `specs`, `tasks`, and Design Gate; do not use Explore Summary only for change-name detection.
         AskQuestion: «Из Explore Summary: `<name>`. Использовать?
         [Да / Другое имя]».
      2. If no Explore Summary — run `openspec list --json`.
         If exactly 1 active change with incomplete artifacts — AskQuestion:
         «Найден активный change `<name>` (N/M задач). Продолжить?
         [Да / Новый change]».
      3. If nothing found — AskQuestion (open-ended):
         «What change do you want to work on? Describe what you want to build or fix.»
         Derive kebab-case name from description.

   **IMPORTANT**: Do NOT proceed without a confirmed change name.

1.25. **Explore Summary Context Gate**

   После подтверждения имени change определить `exploreContext`:
   - Если на шаге 1b.1 уже прочитан `temp/explore-summary-*.md` — использовать его.
   - Если имя передано аргументом и `exploreContext` ещё не задан — Glob `temp/explore-summary-*.md`, взять самый свежий файл за последние 48 часов, если он относится к этой теме (совпадает имя change или `**Тема:**` явно соответствует запросу), и прочитать его как source context.
   - Извлечь из Summary как минимум: `Architect Gate` (`not-required` / `required-pending` / `passed: <path>` / `declined: <reason>`), `Ключевые решения`, `Knowledge findings`, `Рекомендации по срезам`.
   - Если Summary старше 48 часов или не относится к change — считать, что `exploreContext` отсутствует.
   - Если `exploreContext` отсутствует, это не блокирует простой ff. Design Gate ниже выполнит hard-gate только при структурных триггерах.

1.5. **Metadata Gate (MANDATORY)**

   После подтверждения имени ЗНИ запросить данные для маркеров разработчика и генерации ТЗ.
   **Это обязательный шаг перед scaffold.**
   
   1. Выведите текстовый запрос в чат (без `AskQuestion` и без других инструментов):
      ```
      Для оформления комментариев в коде (// +++ ... [ID#...]) укажите:
      1. Разработчик (ФИО, например «Борисов И.Г.»):
      2. Идентификатор ЗНИ (например «ID#79714»):
      3. Название ЗНИ для комментария (короткое):
      
      Генерация ТЗ.md (документ для согласования с заказчиком):
      4. Нужно ли генерировать ТЗ.md: Да / Нет / Решить позже
      ```
   2. Не вызывайте `AskQuestion`: это свободный многострочный ввод, пользователь отвечает обычным текстом в чат.
   3. Допустимые ответы:
      - заполненные пункты 1–4 — использовать как Metadata Gate;
      - `пропустить`, `плейсхолдеры`, `позже` — продолжить с плейсхолдерами;
      - `отмена`, `cancel`, `стоп` — завершить ff без создания change.
   
   **STOP: дождаться ответа.**
   
   **Guardrail:** Выполнение шага 2 (`openspec new change`) до завершения Metadata Gate СТРОГО ЗАПРЕЩЕНО.
   
   - **Если пользователь прислал заполненные пункты:** Запомните введённые данные. На шаге 5 при генерации `proposal.md` заполните блок `## Metadata (comment markers)` реальными значениями (не используйте «Уточнить до»). Также добавьте поле `generate_tz: auto | no | deferred` в зависимости от ответа про ТЗ (`auto` = да/нужно при verify, `no` = нет/не нужно, `deferred` = решить позже).
   - **Если пользователь попросил пропустить:** На шаге 5 при генерации `proposal.md` запишите нормализованные плейсхолдеры:
     - `developer: <developer>`
     - `zni_id: <zni_id>`
     - `zni_name: <заполняется из темы>`
     - `generate_tz: auto` (по умолчанию)
     А также при генерации `tasks.md` добавьте в блок `## Follow-up` (или создайте его в конце файла) задачу:
     `- [ ] F1 Заполнить Metadata (developer / zni_id) в proposal.md до первого кода`

2. **Create the change directory**
   ```bash
   openspec new change "<name>"
   ```
   This creates a scaffolded change at `openspec/changes/<name>/`.

3. **Read project context**
   Read `openspec/project.md` for project-level constraints (editing rules, allowed directories, conventions).
   All subsequent artifacts (proposal, design, tasks, specs) MUST respect these constraints.
   In particular: if project.md restricts edits to specific directories (e.g., only cfe/, not cf/) —
   design and tasks MUST NOT propose changes outside allowed directories.

4. **Get the artifact build order**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to get:
   - `applyRequires`: array of artifact IDs needed before implementation (e.g., `["tasks"]`)
   - `artifacts`: list of all artifacts with their status and dependencies

5. **Create artifacts in sequence until apply-ready**

   Use the **TodoWrite tool** to track progress through the artifacts.

   **Error handling (MANDATORY for all Task delegations in ff):**
   If a Task call returns an error (Error, Aborted, timeout):
   1. **Retry once** with the same prompt.
   2. If retry also fails — create the artifact yourself using the `template`
      and dependency artifacts (proposal, design, specs). Log a warning to the user:
      "Делегирование агенту не удалось; артефакт создан оркестратором."
   3. **NEVER silently skip** an artifact. Every `applyRequires` artifact
      MUST be written to disk before the ff session ends.

   Loop through artifacts in dependency order (artifacts with no pending dependencies first):

   a. **For each artifact that is `ready` (dependencies satisfied)**:
      - Get instructions:
        ```bash
        openspec instructions <artifact-id> --change "<name>" --json
        ```
      - The instructions JSON includes:
        - `context`: Project background (constraints for you - do NOT include in output)
        - `rules`: Artifact-specific rules (constraints for you - do NOT include in output)
        - `template`: The structure to use for your output file
        - `instruction`: Schema-specific guidance for this artifact type
        - `outputPath`: Where to write the artifact
        - `dependencies`: Completed artifacts to read for context
      - Read any completed dependency files for context
      - If the change name/brief was derived from `temp/intake-brief-*.md`, read that Intake Brief as source context for `proposal`, `design`, `specs`, and `tasks`. Use it as customer-intent context, not as a verified code investigation.
      - If `exploreContext` exists, use it as source context for `proposal`, `design`, `specs`, and `tasks`: carry `Ключевые решения` into scope/design rationale, `Knowledge findings` into context/assumptions, `Рекомендации по срезам` into `## Slices`, and `Architect Gate` into Design Gate. Treat `exploreContext` as verified investigation context only to the extent its reports are referenced; do not invent code facts from prose.
      - **Special case: `tasks` artifact (slice-aware task decomposition)**:
        Before delegating tasks, the **Slice Generation Gate** must have been passed (see step 5e.1 below) and design.md MUST contain a `## Slices` section.

        Delegate to **onec-code-architect** with the "Architect — slice-aware task decomposition" template (`1c-agent-patterns/SKILL.md`).
        Pass: paths to proposal.md, design.md (with approved `## Slices` section, включая `### Матрица приёмки` если есть), specs/, and the `template` from instructions.

        **Acceptance Scope Tightness context (правило среза 6):** в промпт архитектору явно передать:
        - Извлечённый список Scenarios per slice из design.md `## Slices` (столбец «Scenarios из spec» и/или матрица приёмки).
        - Требование: каждый `S<N>.T<M>` SHALL иметь хвостовую ссылку `(Scenario: «<имя>»)` на Scenario из `**Связь со spec:**` **этого же** среза; количество `T<M>` ≤ 2 × количество Scenarios; инварианты/NFR/перф-проверки — НЕ в приёмку среза, а в `design.md#Assumptions` / обычную задачу / `## Follow-up`.
        - Ссылки: `.cursor/rules/vertical-slices.mdc` (правило среза 6), `.cursor/rules/task-readability.mdc` (Исключение 1 для `T<M>`), `.cursor/skills/1c-agent-patterns/SKILL.md` (шаблон slice-aware task decomposition, правило 10.1).

        The architect produces tasks.md with:
        - H1 headers `# Срез S<N>: <имя>` (one per slice from design)
        - metadata blocks under each slice header (Сценарий, Приёмка, Связь со spec, Зависимости)
        - task IDs with slice prefix `S<N>.<M>`
        - acceptance tasks `S<N>.T<M>` inside each slice, каждая с `(Scenario: «…»)` в хвосте
        - slice-gate markers `<!-- slice-gate: <critérion> -->`

        No classification P0–P4, no `# Фаза N`, no `<!-- phase-gate -->`. See `.cursor/rules/vertical-slices.mdc` (в т.ч. **ИНВАРИАНТ: Defect placement** — не плодить `# Срез S<N+1>` для дефекта непринятого среза без cross-slice / frozen-slice).

        Architect reads files independently and returns tasks.md content.
        Save the result to `outputPath`.
        If architect Task fails — apply error handling above (retry once, then create yourself).

        **Post-tasks self-check (Acceptance Scope Tightness):**
        После сохранения `tasks.md` — mechanical self-check:
        1. Grep `tasks.md` на `^- \[[ x]\] S\d+\.T\d+` — собрать все acceptance tasks.
        2. Для каждого `T<M>` проверить наличие хвостовой скобки `(Scenario: «…»)` или `(Scenarios: «…», …)`.
        3. Сверить имя(имена) Scenario с `**Связь со spec:**` соответствующего среза.
        4. Зафиксировать mismatches:
           - `T<M>` без ссылки → **WARNING** в сводке ff.
           - `T<M>` со Scenario не из `**Связь со spec:**` → **WARNING**.
           - `|T<M>| > 2 × |Scenarios|` в срезе → **SUGGESTION**.
        5. Если есть WARNING — в финальной сводке ff: «Обнаружены замечания Acceptance Scope Tightness. Рекомендую `/opsx:verify <name>` для полной проверки критерием 5b QC и получения карточек решений.»
        6. Если mismatches нет — лог «Acceptance ↔ Scenario mapping OK».
      - **All other artifacts**: Create the artifact file using `template` as the structure
      - Apply `context` and `rules` as constraints - but do NOT copy them into the file
      - **Metadata block**: When creating `proposal.md`, ALWAYS add the `## Metadata (comment markers)` block (with developer, zni_id, zni_name, generate_tz) immediately after `## Why`.
      - Show brief progress: "✓ Created <artifact-id>"

   b. **Continue until all `applyRequires` artifacts are complete**
      - After creating each artifact, re-run `openspec status --change "<name>" --json`
      - Check if every artifact ID in `applyRequires` has `status: "done"` in the artifacts array
      - Stop when all `applyRequires` artifacts are done

   c. **If an artifact requires user input** (unclear context):
      - Use **AskUserQuestion tool** to clarify
      - Then continue with creation

   d. **ADR Discovery (before/during design artifact)**:
      Before creating the `design` artifact, search for existing ADR decisions relevant to this change:
      1. Glob `openspec/adrs/ADR-*.md` — if any ADR files exist
      2. Grep ADR files for keywords related to the change area (from proposal topic, module names, subsystem names)
      3. If relevant ADRs found — include references in the design artifact's Context or Design Rationale section:
         `Связанные ADR: ADR-NNNN (краткое описание) — [ссылка]`
      4. If relevant ADRs found and the proposed approach contradicts an existing ADR — note this explicitly in design.md Risks section

   e. **Design Gate (MANDATORY — after design, before specs/tasks)**:

      After the `design` artifact is created and written, **before** proceeding to `specs` or `tasks`:

      1. Check triggers from `architect-gate.mdc` on the just-created design.md:
         - **Objective markers**: Grep design.md for bug fix markers, base procedure interception, new metadata objects
         - **Semantic triggers**: Grep for `&Вместо`, `&После`, `&Перед`; missing `## Existing Mechanisms` or `## Design Rationale` when integration is described
         - **Structural triggers**: >1 file affected, >10 lines of change, contract/API changes
      2. Check if `architecture-*.md` already exists in `reports/` (from prior explore session or current change).
      3. Check `exploreContext.Architect Gate` if present:
         - `passed: <path>` → treat as existing architecture report only if the path exists and scope intersects the current change; otherwise treat Architect Gate as fired.
         - `required-pending` → Architect Gate is considered fired regardless of design.md wording.
         - `declined: <reason>` → Architect Gate is considered fired unless the current ff invocation also includes `--skip-architect <причина>`.
         - `not-required` → continue with normal trigger evaluation from design.md.
      4. **Hard-gate when no recent Explore Summary exists:** if `exploreContext` is absent, structural triggers fired (`>1 file affected`, `>10 lines of change`, or contract/API change), no architecture report exists, and `--skip-architect <причина>` was not provided — stop ff after showing:
         ```
         Design создан. Сработали структурные триггеры Architect Gate, но свежий Explore Summary не найден.
         Для сложной постановки сначала выполните `/opsx:explore` или сознательно повторите `/opsx:ff <name> --skip-architect <причина>`.
         ff остановлен до создания specs/tasks.
         ```
      5. **If triggers fired AND no architecture report**:
         - **MANDATORY PAUSE** — Если пользователь не передал флаг `--skip-architect <причина>`, вывести информационное сообщение (без AskQuestion с выбором пропуска):
           ```
           Design создан. Сработали триггеры Architect Gate: [list].
           Архитектурный анализ обязателен и запускается сейчас.
           Если нужно сознательно отложить — завершите ff и запустите его повторно с флагом `--skip-architect <причина>`.
           ```
         - Delegate to `onec-code-architect` with design review brief. Save report to `reports/architecture-ff-YYYY-MM-DD.md`. If architect suggests design changes — apply them to design.md, show diff to user.
         - **Error handling for architect:** Если агент упал (после 1 retry), оркестратор проводит self-review по шаблону архитектора (структура отчёта + пометка «self-review fallback, agent unavailable») и обязательно пишет файл `reports/architecture-ff-selfreview-YYYY-MM-DD.md`.
         - **If `--skip-architect <причина>` was provided:** Создать файл `.gate-override.yaml` в корне change с содержимым:
           ```yaml
           gate: architect
           reason: "<причина>"
           timestamp: <текущая дата ISO>
           ```
           Продолжить без вызова архитектора.
      6. **If triggers fired AND architecture report exists** → OK, continue
      7. **If no triggers fired** → continue without pause

   e.1. **Slice Generation Gate (MANDATORY — after Design Gate, before `specs`/`tasks`):**

      After the `design` artifact is created (and Design Gate passed), **before** proceeding to any artifact whose creation depends on design (notably `tasks`, but also before further specs refinement):

      1. Read the just-created `design.md` and all `specs/**/spec.md`.
      2. Count likely tasks volume from design scope (rough estimate — files, procedures, UI elements).
         - If estimated ≤ 5 tasks (Lite tier) — slice decomposition is OPTIONAL; may proceed with a single container slice `S1`.
         - If estimated ≥ 6 tasks — slice decomposition is **MANDATORY**.
      3. Grep `design.md` for existing `## Slices` section.
      4. **If `## Slices` section is absent (or empty) AND tier ≥ Standard:**
         - Delegate to **onec-code-architect** with the "Architect — slice decomposition" template (`1c-agent-patterns/SKILL.md`).
         - Pass: paths to proposal.md, design.md (without Slices), specs/.
         - The architect returns the `## Slices` block (table of slices + scenarios + files + acceptance + dependency graph + coverage matrix).
         - Insert the returned block into `design.md` (append after existing sections, before "Risks" if present).
         - Show the user a compact summary:
           ```
           Предложенная декомпозиция на срезы:
           - S1: <имя> — <сценарий одной строкой>
           - S2: <имя> — <сценарий>
           - ...
           Всего срезов: N. Сценариев покрыто: K/M.
           ```
         - AskQuestion: `[Принять] / [Скорректировать (указать замечание)] / [Пересобрать срезы]`.
           - `Принять` → перейти к `tasks`.
           - `Скорректировать` → принять пользовательский комментарий, повторно делегировать architect с этим комментарием, обновить `design.md`.
           - `Пересобрать срезы` → повторить делегирование со сменой модели или указанием «другое группирование».
      5. **If `## Slices` section is present:**
         - Validate with Quality Controller (quick check — criteria 1, 3, 5 from QC), see `openspec-quality-controller.md`.
         - If critical issues — show the user and AskQuestion whether to regenerate.
         - Otherwise — proceed.
      6. **Acceptance Scope Tightness pre-check (правило среза 6):**
         - Read the `## Slices` block from `design.md`. For each slice row, extract the Scenarios column (ссылки на `#### Scenario:` из spec).
         - Validate per slice:
           * Scenarios count SHALL be ≥1 and ≤3. Если >3 — предупредить архитектора и предложить раздробить срез. Если 0 — это не срез, а prereq-слой (см. правило декомпозиции 7).
           * Если в таблице есть отдельная `### Матрица приёмки (Acceptance ↔ Scenario)` — проверить, что каждый `T<M>` привязан к Scenario из того же среза; отсутствие матрицы при Standard/Full tier — рекомендация архитектору дополнить.
         - Эти проверки — «hint» для следующего шага `slice-aware task decomposition`: архитектор должен соблюдать Acceptance Scope Tightness при генерации `tasks.md`.
      7. **Guardrail:** do NOT invoke the tasks architect template until `design.md` contains the `## Slices` section (or Lite tier was explicitly chosen).

      **Error handling:** if architect Task fails (error / timeout after retry), create a minimal single-slice draft yourself (1 container slice covering all tasks) and log a warning to the user. The user may run `/opsx:verify --migrate-to-slices` later to decompose.

6. **Show final status**
   ```bash
   openspec status --change "<name>"
   ```

**Output**

After completing all artifacts, summarize:
- Change name and location
- List of artifacts created with brief descriptions
- Architect Gate status: `not-required` / `passed: <path>` / `declined: <reason>` / `skipped via .gate-override.yaml` / `self-review fallback`
- What's ready: "All artifacts created! Ready for implementation."
- Prompt: "Рекомендуется: `/opsx:verify <name>` для проверки качества артефактов (фазовая когерентность, ТЗ, реализуемость, gates). Или сразу `/opsx:apply <name>` для начала реализации."

**Artifact Creation Guidelines**

- Follow the `instruction` field from `openspec instructions` for each artifact type
- The schema defines what each artifact should contain - follow it
- Read dependency artifacts for context before creating new ones
- Use `template` as the structure for your output file - fill in its sections
- **IMPORTANT**: `context` and `rules` are constraints for YOU, not content for the file
  - Do NOT copy `<context>`, `<rules>`, `<project_context>` blocks into the artifact
  - These guide what you write, but should never appear in the output
- **Design Rationale (for design artifact)**: если решение предполагает интеграцию с существующим кодом, добавить секцию «## Design Rationale» — обоснование выбора: почему эта точка реализации, какие контракты, какие паттерны проекта. **Важно:** самописный Rationale НЕ закрывает Architect Gate — критерии валидности и триггеры в `architect-gate.mdc`.
- **Existing Mechanisms (for design artifact)**: если создаётся новый объект, workflow или хранилище при интеграции с базой — обязательна секция `## Existing Mechanisms`: какие штатные механизмы обследованы, почему не подошли, какой уровень Preference Hierarchy выбран. Шаблон секции — в `existing-mechanism-priority.mdc`.
- **Behavior Contract (for design artifact)**: для каждой UX-значимой или интеграционной доработки добавить секцию `## Behavior Contract`. В ней фиксировать наблюдаемое поведение, инварианты, условия включения/выключения, acceptance-критерии на уровне результата. Не фиксировать конкретные имена процедур, если они ещё не verified по коду или не являются архитектурным контрактом.
- **Implementation Options (for design artifact)**: для UI, интеграций, перехватов и переносов поведения добавить секцию `## Implementation Options`. Минимум: `Option A / Option B`, выбранный вариант, почему он проще/надёжнее, какие варианты отклонены. Конкретная реализация в `tasks.md` должна ссылаться на выбранный вариант, но задача формулируется через результат, а не через рецепт.

**Guardrails**
- **Metadata Gate MUST NOT be silently skipped**: Do not run `openspec new change` without getting an answer to the developer/zni_id prompt. Before showing the final summary, verify `proposal.md` for placeholders like "Уточнить до", `<developer>`, `<zni_id>`. If found and the user did NOT choose "Пропустить", add a WARNING to the summary.
- **Explore Summary MUST NOT be used only for naming**: If a recent relevant `temp/explore-summary-*.md` exists, read it as source context and carry `Architect Gate`, key decisions, knowledge findings, and slice recommendations into artifact creation and Design Gate.
- Create ALL artifacts needed for implementation (as defined by schema's `apply.requires`)
- Always read dependency artifacts before creating a new one
- If context is critically unclear, ask the user - but prefer making reasonable decisions to keep momentum
- If a change with that name already exists, suggest continuing that change instead
- Verify each artifact file exists after writing before proceeding to next
- **Completion checkpoint (MANDATORY on every turn):** Before processing a user follow-up message during ff, run `openspec status --change "<name>" --json`. If any `applyRequires` artifact has status != `"done"`: (1) Notify the user: «Артефакт `<id>` не создан. Продолжить создание?» (2) Complete the missing artifact BEFORE handling the follow-up request. Rationale: user follow-ups in ff are still part of the ff session (`command-session-persistence`). Missing artifacts must not be silently dropped.
