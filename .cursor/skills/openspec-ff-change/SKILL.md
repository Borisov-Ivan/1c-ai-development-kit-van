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

3. **Get the artifact build order**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to get:
   - `applyRequires`: array of artifact IDs needed before implementation (e.g., `["tasks"]`)
   - `artifacts`: list of all artifacts with their status and dependencies

4. **Create artifacts in sequence until apply-ready**

   Use the **TodoWrite tool** to track progress through the artifacts.

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
      - **Special case: `tasks` artifact (task decomposition)**:
        Instead of writing tasks directly, delegate to **onec-code-architect** with the
        "Architect — task decomposition" template (`1c-agent-patterns/SKILL.md`).
        Pass: paths to proposal.md, design.md, specs/, and the `template` from instructions.
        Architect reads files independently and returns tasks.md content.
        Save the result to `outputPath`.
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

   e. **Design Gate (after design artifact)**:
      After creating the `design` artifact, check architect-gate triggers mechanically:

      1. **Check objective markers** (Glob/Grep, not subjective assessment):
         - Glob `reports/architecture-*.md` in change dir and `temp/reports/` — architect report exists?
         - Glob `reports/trace-analysis-*.md`, `reports/exploration-*.md` — analytical agents were used?
         - Glob `temp/explore-summary-*.md` or `reports/explore-summary-*.md` — explore summary exists?
         - Grep design.md for: «базовая процедура», «платформа», «повторная запись», «перехват», «после вызова базы», «&Вместо», «&После»
      2. **Check semantic and structural triggers** from `architect-gate.mdc`
      3. **Decision matrix:**
         - **Triggers fired AND `architecture-*.md` found** → continue (architect already reviewed)
         - **Triggers fired AND NO `architecture-*.md`** → **PAUSE.** AskQuestion to USER (not agent decision):
           ```
           "Design создан. Сработали маркеры Architect Gate:
           - [list of triggered markers]
           Архитектурный анализ не найден.
           1. Запустить архитектора сейчас [Рекомендуется]
           2. Вернуться в explore для архитектурного анализа
           3. Продолжить без архитектора (на ваш риск)"
           ```
           - Option 1 → call **onec-code-architect** to review design.md, save report, incorporate feedback
           - Option 2 → STOP ff, suggest `/opsx:explore`
           - Option 3 → continue, document user's decision in design.md
         - **No triggers fired** → continue without pause

   f. **Design Review Gate (после всех артефактов)**:
      Когда все `applyRequires` артефакты готовы (перед шагом 5), проверить триггеры Design Review из `architect-gate.mdc` (секция DESIGN REVIEW ТРИГГЕРЫ):

      1. Glob `reports/trace-analysis-*.md`, `reports/exploration-*.md` — суммарно ≥ 2 файла?
      2. Grep design.md / proposal.md на маркеры bug fix (`исправь`, `ошибка`, `баг`, `fix`, `crash`, `не работает`, `падает`)
      3. Grep design.md / proposal.md на `&ИзменениеИКонтроль`
      4. Grep tasks.md на паттерны ветвления: `При отрицательн`, `Если в п.`, `Альтернатив`, `workaround`, `Иначе →`, `Иначе —`
      5. Grep design.md на `вероятно`, `возможно`, `скорее всего`, `гипотеза` — и при этом отсутствует секция `## Hypotheses`

      **Decision:**
      - **Triggers fired AND `reports/design-review-*.md` NOT found** →
        AskQuestion:
        ```
        "Артефакты созданы. Обнаружены маркеры сложности постановки:
        - [перечисление сработавших триггеров]
        Рекомендую ревью постановки (полнота, verified/hypothesis,
        критерии приёмки, покрытие spec, риски).
        1. Запустить ревью [Рекомендуется]
        2. Пропустить, перейти к apply"
        ```
        - Option 1 → call **onec-code-architect** с фокусом на качество артефактов
          (prompt: все артефакты текстом + фокусные вопросы из `architect-gate.mdc`).
          Сохранить отчёт в `reports/design-review-YYYY-MM-DD.md`.
          Внести рекомендованные правки уровня medium+ в артефакты.
        - Option 2 → продолжить
      - **Triggers NOT fired** → продолжить без паузы
      - **`reports/design-review-*.md` found** → продолжить (уже проведено)

5. **Show final status**
   ```bash
   openspec status --change "<name>"
   ```

**Output**

After completing all artifacts, summarize:
- Change name and location
- List of artifacts created with brief descriptions
- What's ready: "All artifacts created! Ready for implementation."
- Prompt: "Run `/opsx:apply` or ask me to implement to start working on the tasks."

**Artifact Creation Guidelines**

- Follow the `instruction` field from `openspec instructions` for each artifact type
- The schema defines what each artifact should contain - follow it
- Read dependency artifacts for context before creating new ones
- Use `template` as the structure for your output file - fill in its sections
- **IMPORTANT**: `context` and `rules` are constraints for YOU, not content for the file
  - Do NOT copy `<context>`, `<rules>`, `<project_context>` blocks into the artifact
  - These guide what you write, but should never appear in the output
- **Design Rationale (for design artifact)**: если решение предполагает интеграцию с существующим кодом, добавить секцию «## Design Rationale» (почему эта точка реализации, контракты, паттерны проекта). **Важно:** самописный Rationale НЕ закрывает Architect Gate — критерии валидности и триггеры в `architect-gate.mdc`.

**Guardrails**
- Create ALL artifacts needed for implementation (as defined by schema's `apply.requires`)
- Always read dependency artifacts before creating a new one
- If context is critically unclear, ask the user - but prefer making reasonable decisions to keep momentum
- If a change with that name already exists, suggest continuing that change instead
- Verify each artifact file exists after writing before proceeding to next
