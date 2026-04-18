---
name: openspec-new-change
description: Start a new OpenSpec change using the experimental artifact workflow. Use when the user wants to create a new feature, fix, or modification with a structured step-by-step approach.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.1.1"
---

Start a new change using the experimental artifact-driven approach.

**Input**: The user's request may include a change name (kebab-case), a description of what they want to build, or nothing (auto-detect from context).

**Steps**

1. **Determine change name and brief**

   a. **If argument provided** — use it as change name (kebab-case). Proceed to step 2.

   b. **If no argument — auto-detect from context:**
      1. Glob `temp/explore-summary-*.md`. If found, read the most recent one (by date in filename).
         Extract change name from line matching `Готово к созданию ЗНИ <name>`
         or derive kebab-case from `**Тема:**`.
         Extract brief from `**Ключевые решения:**` section (2-3 sentences).
         AskQuestion:
         ```
         Из контекста обсуждения:
         - **Имя ЗНИ:** `<kebab-name>`
         - **Бриф:** <2-3 sentences from key decisions>
         - **Источник:** explore-summary-YYYY-MM-DD.md

         1. Подтвердить
         2. Изменить имя
         3. Уточнить бриф
         ```
      2. If no Explore Summary — Glob `temp/reports/{trace-analysis,exploration,correlation}-*.md`.
         If found, read the most recent report, derive topic and brief from its content.
         AskQuestion with proposed name and brief (same format as above, source = report filename).
      3. If no reports — run `openspec list --json`.
         If exactly 1 active change with incomplete artifacts — AskQuestion:
         «Найден активный change `<name>` (N/M артефактов). Продолжить?
         [Да / Новый change]».
      4. If nothing found — AskQuestion (open-ended, no preset options):
         «Что хотите реализовать? Опишите задачу.»
         From the answer, derive a kebab-case name and brief.

   **IMPORTANT**: Do NOT proceed without a confirmed change name.

2. **Determine the workflow schema**

   Use the default schema (omit `--schema`) unless the user explicitly requests a different workflow.

   **Use a different schema only if the user mentions:**
   - A specific schema name → use `--schema <name>`
   - "show workflows" or "what workflows" → run `openspec schemas --json` and let them choose

   **Otherwise**: Omit `--schema` to use the default.

3. **Create the change directory**
   ```bash
   openspec new change "<name>"
   ```
   Add `--schema <name>` only if the user requested a specific workflow.
   This creates a scaffolded change at `openspec/changes/<name>/` with the selected schema.

4. **Read project context**
   Read `openspec/project.md` for project-level constraints (editing rules, allowed directories, conventions).
   All subsequent artifacts (proposal, design, tasks, specs) MUST respect these constraints.
   In particular: if project.md restricts edits to specific directories (e.g., only cfe/, not cf/) —
   design and tasks MUST NOT propose changes outside allowed directories.

5. **Show the artifact status**
   ```bash
   openspec status --change "<name>"
   ```
   This shows which artifacts need to be created and which are ready (dependencies satisfied).

6. **Get instructions for the first artifact**
   The first artifact depends on the schema (e.g., `proposal` for spec-driven).
   Check the status output to find the first artifact with status "ready".
   ```bash
   openspec instructions <first-artifact-id> --change "<name>"
   ```
   This outputs the template and context for creating the first artifact.

7. **STOP and wait for user direction**

**Output**

After completing the steps, summarize:
- Change name and location
- Schema/workflow being used and its artifact sequence
- Current status (0/N artifacts complete)
- The template for the first artifact
- Prompt: "Ready to create the first artifact? Just describe what this change is about and I'll draft it, or ask me to continue."

**Guardrails**
- Do NOT create any artifacts yet - just show the instructions
- Do NOT advance beyond showing the first artifact template
- If the name is invalid (not kebab-case), ask for a valid name
- If a change with that name already exists, suggest continuing that change instead
- Pass --schema if using a non-default workflow
- **ADR Discovery**: при создании design — Glob `openspec/adrs/ADR-*.md`, Grep по области задачи. Если релевантные ADR найдены — включить ссылки в Context/Design Rationale секцию design.md. Если подход противоречит ADR — отметить в Risks. Формат: `.cursor/rules/adr-format.mdc`
- **Design Gate**: при пошаговом создании design — проверить триггеры `architect-gate.mdc` перед переходом к следующему артефакту (аналогично Design Gate в ff). Если триггеры сработали и architecture-*.md отсутствует — ПАУЗА, AskQuestion пользователю
- **Slice Generation Gate (MANDATORY)**: после создания `design.md` и до генерации `tasks.md` (или любых артефактов, зависящих от tasks):
  1. Определить объём ЗНИ. Если ≥ 6 задач — декомпозиция на срезы **обязательна**; если ≤ 5 — опциональна (один срез-контейнер).
  2. Проверить, содержит ли `design.md` секцию `## Slices`.
  3. Если нет (и tier ≥ Standard) — делегировать **onec-code-architect** шаблоном «Architect — slice decomposition» (`1c-agent-patterns/SKILL.md`).
  4. Результат (таблица срезов + сценарии + граф зависимостей + покрытие Scenarios) вставить в `design.md`.
  5. Показать пользователю компактное резюме декомпозиции и AskQuestion: `[Принять] / [Скорректировать] / [Пересобрать]`.
  6. Генерация `tasks.md` (через «Architect — slice-aware task decomposition») запрещена, пока `## Slices` не принята.
  Формат и детали — `.cursor/rules/vertical-slices.mdc`.
