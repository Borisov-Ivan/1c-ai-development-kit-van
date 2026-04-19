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
      1. Glob `temp/explore-summary-*.md`. If found, read the most recent one (by date in filename).
         Extract change name from line matching `Готово к созданию ЗНИ <name>`
         or derive kebab-case from `**Тема:**`.
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
      - **Special case: `tasks` artifact (slice-aware task decomposition)**:
        Before delegating tasks, the **Slice Generation Gate** must have been passed (see step 5e.1 below) and design.md MUST contain a `## Slices` section.

        Delegate to **onec-code-architect** with the "Architect — slice-aware task decomposition" template (`1c-agent-patterns/SKILL.md`).
        Pass: paths to proposal.md, design.md (with approved `## Slices` section), specs/, and the `template` from instructions.

        The architect produces tasks.md with:
        - H1 headers `# Срез S<N>: <имя>` (one per slice from design)
        - metadata blocks under each slice header (Сценарий, Приёмка, Связь со spec, Зависимости)
        - task IDs with slice prefix `S<N>.<M>`
        - acceptance tasks `S<N>.T<M>` inside each slice
        - slice-gate markers `<!-- slice-gate: <critérion> -->`

        No classification P0–P4, no `# Фаза N`, no `<!-- phase-gate -->`. See `.cursor/rules/vertical-slices.mdc`.

        Architect reads files independently and returns tasks.md content.
        Save the result to `outputPath`.
        If architect Task fails — apply error handling above (retry once, then create yourself).
      - **All other artifacts**: Create the artifact file using `template` as the structure
      - Apply `context` and `rules` as constraints - but do NOT copy them into the file
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
      2. Check if `architecture-*.md` already exists in `reports/` (from prior explore session)
      3. **If triggers fired AND no architecture report**:
         - **MANDATORY PAUSE** — AskQuestion:
           ```
           Design создан. Сработали триггеры Architect Gate: [list].
           Рекомендуется архитектурное ревью перед продолжением.
           1. Запустить архитектора
           2. Пропустить (задокументировать отказ)
           ```
         - Option 1 → delegate to `onec-code-architect` with design review brief. Save report to `reports/architecture-ff-YYYY-MM-DD.md`. If architect suggests design changes — apply them to design.md, show diff to user.
         - Option 2 → document skip: add note to design.md footer: `<!-- Architect Gate: triggers [...] fired, skipped by user at ff -->`
      4. **If triggers fired AND architecture report exists** → OK, continue
      5. **If no triggers fired** → continue without pause

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
      6. **Guardrail:** do NOT invoke the tasks architect template until `design.md` contains the `## Slices` section (or Lite tier was explicitly chosen).

      **Error handling:** if architect Task fails (error / timeout after retry), create a minimal single-slice draft yourself (1 container slice covering all tasks) and log a warning to the user. The user may run `/opsx:verify --migrate-to-slices` later to decompose.

6. **Show final status**
   ```bash
   openspec status --change "<name>"
   ```

**Output**

After completing all artifacts, summarize:
- Change name and location
- List of artifacts created with brief descriptions
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

**Guardrails**
- Create ALL artifacts needed for implementation (as defined by schema's `apply.requires`)
- Always read dependency artifacts before creating a new one
- If context is critically unclear, ask the user - but prefer making reasonable decisions to keep momentum
- If a change with that name already exists, suggest continuing that change instead
- Verify each artifact file exists after writing before proceeding to next
- **Completion checkpoint (MANDATORY on every turn):** Before processing a user follow-up message during ff, run `openspec status --change "<name>" --json`. If any `applyRequires` artifact has status != `"done"`: (1) Notify the user: «Артефакт `<id>` не создан. Продолжить создание?» (2) Complete the missing artifact BEFORE handling the follow-up request. Rationale: user follow-ups in ff are still part of the ff session (`command-session-persistence`). Missing artifacts must not be silently dropped.
