---
name: openspec-continue-change
description: Continue working on an OpenSpec change by creating the next artifact. Use when the user wants to progress their change, create the next artifact, or continue their workflow.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.1.1"
---

Continue working on a change by creating the next artifact.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Output style:**
- Сводка в чате после создания артефакта — **T-CONFIRM** из `.cursor/docs/opsx-output-style.md` §5.5 (действие → изменённые файлы → следующий шаг).
- **Изменения в артефактах** (`proposal.md`, `design.md`, `tasks.md`, spec deltas) подчиняются §1 «Три слоя» и §3: пользовательские секции артефактов без `S<N>.T<M>/D<N>/R<N>`/номеров задач; внутренние ID — только в `## Slices`, `## Decisions`, `## Tasks`, `## Risks`. Перечисления — нумерованные списки. Перед записью — self-check-5 (§7).

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If multiple active changes: run `openspec list --json` sorted by most recently modified, present top 3-4 options showing name, schema, status, last modified time, mark most recent as "(Recommended)", and use **AskUserQuestion tool** to let user select

   Always announce: "Using change: <name>" and how to override (e.g., `/opsx:continue <other>`).

2. **Check current status**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand current state. The response includes:
   - `schemaName`: The workflow schema being used (e.g., "spec-driven")
   - `artifacts`: Array of artifacts with their status ("done", "ready", "blocked")
   - `isComplete`: Boolean indicating if all artifacts are complete

3. **Act based on status**:

   ---

   **If all artifacts are complete (`isComplete: true`)**:
   - Congratulate the user
   - Show final status including the schema used
   - Suggest: "All artifacts created! You can now implement this change or archive it."
   - STOP

   ---

   **If artifacts are ready to create** (status shows artifacts with `status: "ready"`):
   - Pick the FIRST artifact with `status: "ready"` from the status output
   - Get its instructions:
     ```bash
     openspec instructions <artifact-id> --change "<name>" --json
     ```
   - Parse the JSON. The key fields are:
     - `context`: Project background (constraints for you - do NOT include in output)
     - `rules`: Artifact-specific rules (constraints for you - do NOT include in output)
     - `template`: The structure to use for your output file
     - `instruction`: Schema-specific guidance
     - `outputPath`: Where to write the artifact
     - `dependencies`: Completed artifacts to read for context
   - **Create the artifact file**:
     - Read any completed dependency files for context
     - Use `template` as the structure - fill in its sections
     - Apply `context` and `rules` as constraints when writing - but do NOT copy them into the file
     - Write to the output path specified in instructions
   - Show what was created and what's now unlocked
   - STOP after creating ONE artifact

   ---

   **If no artifacts are ready (all blocked)**:
   - This shouldn't happen with a valid schema
   - Show status and suggest checking for issues

4. **After creating an artifact, show progress**
   ```bash
   openspec status --change "<name>"
   ```

**Output**

After each invocation, show:
- Which artifact was created
- Schema workflow being used
- Current progress (N/M complete)
- What artifacts are now unlocked
- Prompt: "Want to continue? Just ask me to continue or tell me what to do next."

**Artifact Creation Guidelines**

The artifact types and their purpose depend on the schema. Use the `instruction` field from the instructions output to understand what to create.

Common artifact patterns:

**spec-driven schema** (proposal → specs → design → tasks):
- **proposal.md**: Ask user about the change if not clear. Fill in Why, What Changes, Capabilities, Impact.
  - The Capabilities section is critical - each capability listed will need a spec file.
- **specs/<capability>/spec.md**: Create one spec per capability listed in the proposal's Capabilities section (use the capability name, not the change name).
- **design.md**: Document technical decisions, architecture, and implementation approach. **Включает обязательную секцию `## Slices`** (для ЗНИ ≥6 задач) с описанием вертикальных срезов — см. `.cursor/rules/vertical-slices.mdc`.
- **tasks.md**: Break down implementation into checkboxed tasks **по срезам**: H1-заголовки `# Срез S<N>: ...`, метаданные среза (`**Сценарий:**`, `**Приёмка:**`, `**Связь со spec:**`, `**Зависимости:**`), задачи `S<N>.<M>`, обязательный приёмочный тест `S<N>.T<M>` и маркер `<!-- slice-gate: ... -->`.

**Slice Generation Gate (МАНДАТОРНО, между design и tasks):**
Если создаётся `tasks.md` и в `design.md` нет секции `## Slices`, а у ЗНИ ожидается ≥6 задач — **СТОП**. Сначала вызвать `Task(subagent_type="onec-code-architect")` с шаблоном «Architect — slice decomposition» из `.cursor/skills/1c-agent-patterns/SKILL.md`, получить `## Slices`, добавить в design.md (StrReplace), показать пользователю, дождаться подтверждения.

> Перед вызовом Task — **Task Pre-call Checklist** из `.cursor/rules/tool-name-guard.mdc` (subagent_type из списка 1С-агентов; `model` не передавать). Только после этого переходить к генерации tasks через шаблон «Architect — slice-aware task decomposition». Подробнее — `.cursor/skills/openspec-ff-change/SKILL.md` (шаг 5e.1) и `.cursor/skills/openspec-new-change/SKILL.md` (Guardrails).

**Дополнение задач после старта реализации:**
Если пользователь просит «добавить задачу X» в уже стартовавшую ЗНИ:
1. Спросить (или вывести из контекста): к какому срезу относится X?
2. Вставить задачу с ID `S<N>.<M+1>` в нужный срез **перед** приёмочным `S<N>.T<M>`.
3. Если задача относится к **уже принятому** срезу (S<N>.T<M> = `[x]`) — это новый дефект; создать **fix-срез** `S<N>.fix-<K>` или новый `S<M+1>` с пометкой `(исправление S<N>)` — **не** переоткрывать принятый срез.

For other schemas, follow the `instruction` field from the CLI output.

**Guardrails**
- Create ONE artifact per invocation
- Always read dependency artifacts before creating a new one
- Never skip artifacts or create out of order
- If context is unclear, ask the user before creating
- Verify the artifact file exists after writing before marking progress
- Use the schema's artifact sequence, don't assume specific artifact names
- **IMPORTANT**: `context` and `rules` are constraints for YOU, not content for the file
  - Do NOT copy `<context>`, `<rules>`, `<project_context>` blocks into the artifact
  - These guide what you write, but should never appear in the output
