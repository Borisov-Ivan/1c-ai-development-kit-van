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

**Output style:**
- Пользовательские сообщения в чате (AskQuestion-блоки, сводка после генерации артефактов) — шаблон **T-BRIEF** (единый каркас §5.1: **От вас / Цель / План / На выходе / Ок?**, 8–12 строк) / **T-CONFIRM** по контексту, см. `.cursor/docs/opsx-output-style.md`. Стиль вывода — §2.5 «Человеческий слой». Файлы `temp/briefs/*.md` не создаются. KB-discovery (Read `openspec/knowledge/_index.yaml` и при необходимости KB `.md`) — **внутренний шаг перед брифом**, в чат не выводится.
- **Генерируемые артефакты** `proposal.md`, `design.md`, `tasks.md`, spec deltas — подчиняются §1 «Три слоя» и §3 «Запрет внутренних ID в пользовательских полях»: поля `Why`, `What Changes`, `Scope`, `Scenarios`, `Requirements` — UX-слой без утечки `S<N>.T<M>`, `D<N>`, `R<N>`, номеров задач `12.9`; внутренние ID допустимы только в `## Slices`, `## Decisions`, `## Tasks`, `## Risks`. Любое перечисление ≥2 пунктов — нумерованный список. Перед записью артефакта — self-check-5 (§7).

**Steps**

1. **Determine change name and brief**

   a. **If argument provided** — use it as change name (kebab-case). Proceed to step 2.

   b. **If no argument — auto-detect from context (приоритет источников: чат → handoff → temp/reports → legacy → запрос):**
      0. **Chat short-circuit (приоритет 1):** Прочитать **последние 30–50 сообщений текущего чата** и найти **самый свежий** блок `## Для /opsx:ff` (формат — см. `openspec-explore/SKILL.md`, секция «Финал bug-профиля»). Если найден и тема совпадает с запросом:
         - Entry-бриф **опускается** — «Создаю ЗНИ по утверждённому отчёту в чате» + AskQuestion `[Подтвердить / Изменить имя / Сначала explore]`.
         - Имя change: kebab-case-токен из «Что менять» / «Файлы» / темы; derive из заголовка темы при необходимости.
         - `exploreContext` = разобранные поля блока (Симптом, Корневая причина, Что менять, Файлы, Приёмка, Связь с архивом, Architect/verify). Это **primary source** для всех артефактов.
      1. **Handoff-файл (приоритет 2):** `Glob temp/explore-handoff-*.md` за последние **48 часов**. Если найден свежий, тема совпадает — Read; извлечь блок `## Для /opsx:ff` → `exploreContext`; AskQuestion как выше.
      2. **Полные отчёты `Task` (приоритет 3):** `Glob temp/reports/{trace-analysis,exploration,correlation,architecture}-*.md` за 48 ч. Если найден свежий по теме — Read; derive topic и brief из секций `## Для заказчика` / `## Свод`. AskQuestion с предложенным именем (источник = имя файла).
      3. **Legacy session (приоритет 4):** `Glob openspec/sessions/*/analysis.md` за 48 ч. Если найден и тема совпадает — Read; в `## Готовый материал для ЗНИ` поля → `exploreContext`; AskQuestion `[Подтвердить / Изменить имя / Сначала explore]`.
      4. **Legacy explore-summary (приоритет 5):** `Glob temp/explore-summary-*.md` за 48 ч. Если найден:
         - Имя из строки `Готово к созданию ЗНИ <name>` или derive из `**Тема:**`.
         - Brief из `**Ключевые решения:**` (2–3 предложения).
         - AskQuestion:
         ```
         Из контекста обсуждения:
         - **Имя ЗНИ:** `<kebab-name>`
         - **Бриф:** <2-3 sentences from key decisions>
         - **Источник:** explore-summary-YYYY-MM-DD.md

         1. Подтвердить
         2. Изменить имя
         3. Уточнить бриф
         ```
      5. **`openspec list --json`:** если ровно 1 активный change с незакрытыми артефактами — AskQuestion: «Найден активный change `<name>` (N/M артефактов). Продолжить? [Да / Новый change]».
      6. **Запрос пользователю (последний шаг):** AskQuestion (open-ended): «Не нашёл готового блока `## Для /opsx:ff` в чате или handoff. Что хотите реализовать? Опишите задачу.» Derive a kebab-case name и brief из ответа.

   **IMPORTANT**: Do NOT proceed without a confirmed change name.

1.5. **Сбор метаданных маркеров (Metadata)**
   После подтверждения имени и брифа, запросить данные для маркеров разработчика и генерации ТЗ (если они не очевидны из контекста):
   AskQuestion:
   ```
   Для оформления комментариев в коде (// +++ ... [ID#...]) укажите:
   1. Разработчик (ФИО, например "Борисов И.Г."):
   2. Идентификатор ЗНИ (например "ID#79714"):
   3. Название ЗНИ (для комментария, например "Сохранение участников Согласования при частичном повторе 2.1 - развитие"):
   
   Генерация ТЗ.md (документ для согласования с заказчиком):
   [Нужно при verify] / [Не нужно — не тратить контекст] / [Решить позже]
   ```
   *Примечание: Название ЗНИ можно предзаполнить на основе брифа/имени.*

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

8. **Вставка блока Metadata**
   При создании `proposal.md` (или сразу после его генерации) обязательно добавить блок метаданных после секции `## Why`:
   ```markdown
   ## Metadata (comment markers)

   developer: <ФИО>
   zni_id: <ID>
   zni_name: <Название>
   generate_tz: <auto | no | deferred>
   ```

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
- **Behavior Contract / Implementation Options**: при создании `design.md` для UX-значимых, интеграционных, UI/form, перехватов и переносов поведения обязательно включить:
  - `## Behavior Contract` — что пользователь/система наблюдает, какие инварианты должны выполняться, условия включения/выключения, без преждевременной фиксации имён процедур;
  - `## Implementation Options` — 2+ варианта реализации или явное обоснование, почему вариант один; выбранный вариант должен быть самым простым исполнимым способом, совместимым с ADR и существующими механизмами.
  Если пошаговый пользовательский ввод уже содержит «как сделать», перепроверь: это архитектурное ограничение или только возможный рецепт. Рецепт помещается в `Implementation Options`, не в `Behavior Contract`.
- **Design Gate**: при пошаговом создании design — проверить триггеры `architect-gate.mdc` перед переходом к следующему артефакту (аналогично Design Gate в ff). Если триггеры сработали и architecture-*.md отсутствует — ПАУЗА. Вывести сообщение об обязательности архитектурного ревью и запустить архитектора (с fallback на self-review в случае ошибки). Пропуск возможен только через создание файла `.gate-override.yaml` (см. `openspec-ff-change/SKILL.md`).
- **Slice Generation Gate (MANDATORY)**: после создания `design.md` и до генерации `tasks.md` (или любых артефактов, зависящих от tasks):
  1. Определить объём ЗНИ. Если ≥ 6 задач — декомпозиция на срезы **обязательна**; если ≤ 5 — опциональна (один срез-контейнер).
  2. Проверить, содержит ли `design.md` секцию `## Slices`.
  3. Если нет (и tier ≥ Standard) — делегировать **onec-code-architect** шаблоном «Architect — slice decomposition» (`1c-agent-patterns/architect.md`).
  4. Результат (таблица срезов + сценарии + граф зависимостей + покрытие Scenarios) вставить в `design.md`.
  5. Показать пользователю компактное резюме декомпозиции и AskQuestion: `[Принять] / [Скорректировать] / [Пересобрать]`.
  6. Генерация `tasks.md` (через «Architect — slice-aware task decomposition») запрещена, пока `## Slices` не принята.
  Формат и детали — `.cursor/rules/vertical-slices.mdc` (в т.ч. **ИНВАРИАНТ: Defect placement** для fix-задач после старта реализации).
