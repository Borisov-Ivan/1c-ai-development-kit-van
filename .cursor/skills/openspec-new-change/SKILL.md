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
- Сводка в чате («что создано», следующий шаг) — шаблон **T-CONFIRM** §5.5 + **Chat Surface Contract** §2.6: handoff на языке эффекта, **без** перечня файлов; **один** next step — `/opsx:verify <name>` (не «verify или apply», без auto-chain).
- **Подтверждение постановки перед scaffold:** бриф по §5.1 (Sync Card). **B0** при свежем `## Для /opsx:ff` в чате/handoff — одна строка + текстовое «да» / имя (без `AskQuestion` на entry). **B1** при свободном тексте — слоты **От вас / Цель / На выходе / Подтвердить?**, ≤6 строк; слот **План** в чат **запрещён**. KB-discovery — internal, в чат не выводится. `temp/briefs/*.md` не создаются.
- **Генерируемые артефакты** `proposal.md`, `design.md`, `tasks.md`, spec deltas — подчиняются §1 «Три слоя» и §3 «Запрет внутренних ID в пользовательских полях»: секции для заказчика/приёмки (`Why`, `What Changes`, `Scope`, `Scenarios`, `Requirements`) — UX-слой; внутренние ID (`S<N>.<M>`, `S<N>.accept`, `D<N>`, `R<N>`, `I<N>`, номера задач `12.9`) — только в `## Slices`, `## Decisions`, `## Tasks`, `## Risks`. Перечисления — нумерованные списки. Перед записью — self-check-5 (§7).

**Steps**

1. **Determine change name**

   a. **If argument provided** — use it as change name (kebab-case). Proceed to step 2.

   b. **If no argument — auto-detect from context (приоритет источников: чат → handoff → legacy → запрос):**
      0. **Chat short-circuit (приоритет 1):** Прочитать **последние 30–50 сообщений текущего чата сверху-вниз** и найти **самый свежий** блок `## Для /opsx:ff` (формат — см. `openspec-explore/SKILL.md`, секция «Финал bug-профиля»). Если найден и тема совпадает с запросом пользователя:
         - **B0** — одна строка: «Создаю ЗНИ по блоку в чате — имя `<slug>`. Подтвердите «да» или укажите имя.» (**текстом**, не `AskQuestion` на entry). END TURN.
         - Имя change: первый kebab-case-токен из «Что менять» / «Файлы», иначе derive из заголовка темы.
         - `exploreContext` = разобранные поля блока (Симптом, Корневая причина, Что менять, Файлы, Приёмка, Связь с архивом, Architect/verify). Это **primary source** для `proposal`, `design`, `tasks`; не пересобирать вручную.
      1. **Handoff-файл (приоритет 2):** `Glob temp/explore-handoff-*.md` за последние **48 часов**. Если найден свежий файл, тема совпадает:
         - Read; извлечь блок `## Для /opsx:ff` (тот же формат) → `exploreContext`.
         - **B0:** «Создаю ЗНИ из handoff — имя `<name>`. Подтвердите «да» или укажите имя.» (текстом).
      2. **Legacy session (приоритет 3, только если шаги 0–1 пусты):** `Glob openspec/sessions/*/analysis.md` за последние 48 ч. Если найден и тема совпадает:
         - Read; в `## Готовый материал для ЗНИ` (legacy формат) — те же поля → `exploreContext`.
         - **B0:** «Создаю ЗНИ из legacy-сессии — имя `<name>`. Подтвердите «да» или укажите имя.» (текстом).
      3. **Legacy explore-summary (приоритет 4):** `Glob temp/explore-summary-*.md` за последние 48 ч (старый формат). Если найден:
         - Имя из строки `Готово к созданию ЗНИ <name>` или derive из `**Тема:**`.
         - Извлечь `Architect Gate`, `Ключевые решения`, `Knowledge findings`, `Рекомендации по срезам` в `exploreContext`.
         - **B0:** «Создаю ЗНИ из Explore Summary — имя `<name>`. Подтвердите «да» или укажите имя.» (текстом).
      4. **`openspec list --json`:** если ровно 1 активный change с незакрытыми артефактами — одна строка в чат: «Найден активный change `<name>`. Продолжить с ним или новый?» (текстом).
      5. **Запрос пользователю (последний шаг):** «Не нашёл готового блока `## Для /opsx:ff` в чате или handoff. Опишите change или повторите ключевые поля (Симптом, Корневая причина, Файлы) — оформлю по шаблону.»

      Derive kebab-case name из описания пользователя в шаге 5.

   **IMPORTANT**: Do NOT proceed without a confirmed change name.

1.25. **Explore / Session Context Gate**

   После подтверждения имени change определить `exploreContext` (тот же приоритет источников, что в шаге 1b):
   - Если на шаге 1b.0 уже найден блок `## Для /opsx:ff` в чате — использовать его (primary).
   - Если на шаге 1b.1 уже прочитан `temp/explore-handoff-*.md` — использовать его.
   - Если на шаге 1b.2 уже прочитан `openspec/sessions/*/analysis.md` (legacy) — использовать его.
   - Если на шаге 1b.3 уже прочитан `temp/explore-summary-*.md` (legacy) — использовать его.
   - Если имя передано аргументом и `exploreContext` ещё не задан — сначала просмотреть последние сообщения чата на блок `## Для /opsx:ff`, затем `Glob temp/explore-handoff-*.md` (≤48ч), затем `openspec/sessions/*/analysis.md` (≤48ч, legacy), затем `temp/explore-summary-*.md` (legacy).
   - Извлечь как минимум: Симптом / Why, Корневая причина (с маркером `[verified]` / `[hypothesis: план]`), Что менять (scope), Файлы (модули/расширение), Приёмка (acceptance), Связь с архивом (extends `<change>` / новый / unrelated), Architect / verify (yes/no). Для legacy-источников — `Architect Gate`, `Ключевые решения`, `Knowledge findings`, `Рекомендации по срезам`.
   - Если найден блок `## Для /opsx:ff` (в чате или handoff) — это **primary source** для `proposal`, `design`, `specs`, `tasks`; не пересобирать вручную.
   - Если источник старше 48 часов или не относится к change — считать, что `exploreContext` отсутствует.
   - Если `exploreContext` отсутствует, это не блокирует простой ff. Design Gate ниже выполнит hard-gate только при структурных триггерах.

1.5. **Metadata Gate (MANDATORY для нового change)**

   Read `openspec/project.md` → секция **«Разработчик по умолчанию»** → `defaultDeveloper` (ФИО с пробелами, trim), `cfMarkerPrefix`. Канон domain_label и запреты — § «Канон маркеров (domain_label)» в project.md.

   **Предзаполнение domain_label:** если в чате/handoff есть блок `## Для /opsx:ff` с полем **«Тема маркера»** — использовать как черновик; иначе после брифа предложить фразу из Why / What Changes (не kebab-name change, не process-метки).

   **Resume (каталог `openspec/changes/<name>/` уже существует):**
   - Если `proposal.md` есть и `developer` заполнен (не `<ФИО>` / `<developer>`) — **не спрашивать** Metadata Gate; использовать metadata из proposal.
   - Если в proposal плейсхолдеры — один вопрос как ниже (только domain_label / comment_suffix, если ФИО есть в project.md).

   **Новый change — один текстовый вопрос в чат** (без `AskQuestion`):

   - **Если `defaultDeveloper` задан в project.md:**
     ```
     ФИО для маркеров: <из project.md>.
     Доменное пояснение для маркера (1 фраза по-русски: что меняем и зачем).
     Пустой ответ допустим только для mechanical change (marker_style: minimal) — иначе укажите domain_label.
     ```
   - **Если ФИО в project.md нет:**
     ```
     Укажите ФИО (формат «<Фамилия И.О.>» с пробелами) и доменное пояснение для маркера (1 фраза).
     Примеры GOOD: «<Фамилия И.О.> при 429 не снимать операцию с опроса».
     Примеры BAD: «<Фамилия И.Г.> устранение findings release-review».
     ```

   **Soft-reject:** если ответ (domain_label часть) матчит запреты из project.md § Канон domain_label — одна строка «это process-метка, укажите доменное пояснение» и **повтор вопроса** (не писать в proposal).

   Парсинг ответа:
   - Если ФИО только из project.md — вся строка ответа → `comment_suffix` (domain_label), если не пусто.
   - Иначе первая часть → `developer` (нормализовать пробелы в инициалах); остаток → `comment_suffix`.
   - Пустой suffix при новом change → только если пользователь явно указал mechanical / `minimal`; иначе повтор вопроса.

   Допустимо: `пропустить` / `позже` → `developer: <ФИО>`, `marker_style: canonical`, follow-up F1; `отмена` / `стоп` → завершить ff.

   **После первого указания ФИО** (когда в project.md не было значения) — предложить записать в «Разработчик по умолчанию» по `.cursor/rules/capture-to-project.mdc`.

   **STOP:** дождаться ответа (кроме resume с валидным proposal metadata).

   **Guardrail:** `openspec new change` до завершения Metadata Gate для **нового** change запрещён.

   Запись в `proposal.md` (шаг 5) — **канонический формат** (не list с `zni_id` / `zni_name` / `generate_tz`):
   ```markdown
   ## Metadata (comment markers)

   developer: <ФИО>
   comment_suffix: <domain_label; пусто только при marker_style: minimal>
   marker_style: canonical
   ```

   **Парсинг Metadata (resume / read):** поддерживать оба формата в proposal:
   - yaml-like: `developer:`, `comment_suffix:`, `marker_style:`
   - list: `- **developer:**`, `- **comment_suffix:**`, `- **marker_style:**`
   Follow-up при плейсхолдере: `- [ ] F1 Заполнить developer в proposal.md (и при необходимости project.md) до первого кода`

2. **Create or resume the change directory**

   Проверить: существует ли `openspec/changes/<name>/`.

   **Если каталог существует (resume):**
   - **НЕ** вызывать `openspec new change`.
   - Одна строка в чат: «Дозавершаю ЗНИ `<name>` (resume)».
   - Перейти к шагу 3.

   **Если каталога нет (новый change):**
   ```bash
   openspec new change "<name>"
   ```
   Создаёт scaffold в `openspec/changes/<name>/`.

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
   Strictly follow the Subagent result protocol from `.cursor/rules/chat-output-budget.mdc` §5:
   - For `interrupted-by-user`: PAUSE and ask the user how to proceed.
   - For `failed`: Retry once. If retry fails, inform the user "Агент недоступен, делаю упрощённый вариант сам / откладываю" and wait for decision or create minimal scaffold.
   - **NEVER silently skip** an artifact and **NEVER invent error causes** (like "timeout") without evidence. Every `applyRequires` artifact MUST be written to disk before the ff session ends.

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
      - If the change name/brief was derived from a `## Для /opsx:ff` block (chat or `temp/explore-handoff-*.md`) or legacy `openspec/sessions/*/analysis.md`, use it as `exploreContext` for `proposal`, `design`, `specs`, and `tasks` (verified sections only; hypotheses — с пометкой `[hypothesis: план]`).
      - If `exploreContext` exists, use it as source context for `proposal`, `design`, `specs`, and `tasks`: для нового формата (`## Для /opsx:ff`) — Симптом → `## Why`, Корневая причина / Что менять → `## What Changes` / scope, Файлы → `## Scope`, Приёмка → `## Acceptance Criteria` / scenarios, Связь с архивом → `## Decisions` (extends/precedent), Architect/verify → Design Gate. Для legacy — `Ключевые решения` → scope/design rationale, `Knowledge findings` → context/assumptions, `Рекомендации по срезам` → `## Slices`, `Architect Gate` → Design Gate. Treat `exploreContext` as verified investigation context only to the extent its reports are referenced; do not invent code facts from prose.
      - **Special case: `tasks` artifact (slice-aware task decomposition)**:
        Before delegating tasks, the **Slice Generation Gate** must have been passed (see step 5e.1 below) and design.md MUST contain a `## Slices` section.

        Delegate to **onec-code-architect** with the "Architect — slice-aware task decomposition" template (`1c-agent-patterns/architect.md`).
        Pass: paths to proposal.md, design.md (with approved `## Slices` section, включая `### Матрица приёмки` если есть), specs/, and the `template` from instructions.

        **Primary acceptance context (правило среза 6):** в промпт архитектору явно передать:
        - Primary acceptance per slice из design.md `## Slices`.
        - Требование: в каждом срезе **ровно одна** `S<N>.accept`:
          ```
          - [ ] S<N>.accept Принять срез S<N> «<имя>» — <бизнес-результат>:
            - **Primary (обязательно):** <шаги из **Primary acceptance:**>
            - Scenario «<имя>» (опционально): <…>
          ```
          `[x]` = Primary пройден. Остальные Scenario — optional или `S<N>.<M>`.
        - Metadata: `**Primary acceptance:**` обязателен при `# Срез S<N>`.
        - **User Task Contract** (`.cursor/rules/vertical-slices.mdc` § User Task Contract): от пользователя — только ручное конфигурирование и `S<N>.accept`; unknown API/runtime → `design.md` § Assumptions + кодовые задачи агента; **запрещены** `S<N>.<M>` с user IB/runtime spike.
        - Ссылки: `.cursor/rules/vertical-slices.mdc` (правило среза 6 + «ФОРМАТ S<N>.accept» + User Task Contract), `.cursor/rules/task-readability.mdc` (Исключение 1), `.cursor/skills/1c-agent-patterns/architect.md` (шаблон slice-aware task decomposition).

        The architect produces tasks.md with:
        - H1 headers `# Срез S<N>: <имя>` (one per slice from design)
        - metadata blocks under each slice header (Сценарий, **Primary acceptance**, Приёмка, Связь со spec, Зависимости; опц. **Режим apply:** mechanical)
        - task IDs with slice prefix `S<N>.<M>`
        - **exactly one** acceptance task `S<N>.accept` per slice, with a bullet-checklist of scenarios in its body (one bullet per Scenario from `**Связь со spec:**`)
        - slice-gate markers `<!-- slice-gate: <criterion> -->`

        No classification P0–P4, no `# Фаза N`, no `<!-- phase-gate -->`, no multiple `S<N>.T<M>` per slice (legacy format — only for migrated changes). See `.cursor/rules/vertical-slices.mdc` (в т.ч. **ИНВАРИАНТ: Defect placement** — не плодить `# Срез S<N+1>` для дефекта непринятого среза без cross-slice / frozen-slice).

        Architect reads files independently and returns tasks.md content.
        Save the result to `outputPath`.
        If architect Task fails — apply error handling above (retry once, then create yourself).

        **Post-tasks self-check (Primary + Acceptance Coverage):**
        После сохранения `tasks.md` — mechanical self-check:
        1. Grep `# Срез S\d+` — для каждого среза grep `**Primary acceptance:**` → CRITICAL если нет.
        2. Grep `^- \[[ x]\] S\d+\.accept\b` — count = count срезов; иначе CRITICAL.
        3. В каждом `S<N>.accept` — sub-bullet `**Primary (обязательно):**` → CRITICAL если нет.
        4. >1 mandatory sub-bullet без «опционально» → WARNING (`acceptance-simplicity-overload`).
        5. Scenario из spec не покрыт Primary/optional/`S<N>.<M>` → WARNING.
        6. Legacy `S<N>.T<M>` → SUGGESTION.
        7. **User Task Contract (grep):** строки `^- \[[ x]\] S\d+\.\d+` — DENY/ALLOW из `vertical-slices.mdc` § User Task Contract; CRITICAL `user-task-contract-violation` → не предлагать apply; в финале ff — «нужен `/opsx:verify <name>`» или inline-fix tasks (удалить spike, Assumptions в design) до завершения ff.
        8. CRITICAL/WARNING → «Рекомендую `/opsx:verify <name>`».
      - **All other artifacts**: Create the artifact file using `template` as the structure
      - Apply `context` and `rules` as constraints - but do NOT copy them into the file
      - **Metadata block**: When creating `proposal.md`, ALWAYS add `## Metadata (comment markers)` (`developer`, `comment_suffix`, `marker_style`) immediately after `## Why`.
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
         - Delegate to **onec-code-architect** with the "Architect — slice decomposition" template (`1c-agent-patterns/architect.md`).
         - Pass: paths to proposal.md, design.md (without Slices), specs/; **User Task Contract** — Risks с «runtime-verify» → Assumptions + «проверка в Primary accept», не user-задача.
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
         - Delegate to **openspec-quality-controller** (quick check — criteria 1, 3, 5, 5b, 8–11 from QC), see `openspec-quality-controller.md`. **Do NOT** grep keyword lists for criterion 8 — QC semantic judgment only.
         - If critical issues — show the user and AskQuestion whether to regenerate.
         - Otherwise — proceed.
      6. **Foundation Slice Guard** (before AskQuestion «Принять» on proposed slices):
         1. Grep `specs/**/spec.md` for `scenario-implementation-leak` per `.cursor/rules/openspec-specs-gate.mdc` (implementation-leak markers in `- **THEN**` only — structural check).
         2. If QC (or architect output) indicates `slice-foundation-with-gate` / `slice-not-vertical` on a proposed decomposition — **do not offer «Принять»**; only «Скорректировать» / «Пересобрать» with explanation (merge foundation into primary slice).
         3. If `scenario-implementation-leak` found on a Requirement that would become its own slice — remediation: move to `design.md` Behavior Contract before accepting slices (or user override explicitly).
         4. User-spike inside slice (Risks «пользователь верифицирует на ИБ») — **не принимать**; merge в Assumptions + Primary accept (User Task Contract).
      7. **Primary acceptance pre-check (правило среза 6):**
         - For each slice in `## Slices`: Primary acceptance column filled; one blocking journey.
         - In § Risks design не должно остаться «пользователь верифицирует на ИБ» — только Assumptions + accept.
         - Hint for task decomposition: mandatory Primary sub-bullet in `S<N>.accept`.
      7. **Guardrail:** do NOT invoke the tasks architect template until `design.md` contains the `## Slices` section (or Lite tier was explicitly chosen).

      **Error handling:** if architect Task fails (error / timeout after retry), create a minimal single-slice draft yourself (1 container slice covering all tasks) and log a warning to the user. Для перестройки legacy tasks — `/opsx:extend <name>` с architect slice decomposition или ручная правка по `vertical-slices.mdc`.

6. **Show final status**
   ```bash
   openspec status --change "<name>"
   ```

**Output**

After completing all artifacts, summarize in chat (T-CONFIRM, Chat Surface Contract §2.6):
- Change name (one line, language of effect — «ЗНИ создано»)
- **Risk Surfacing (ОБЯЗАТЕЛЬНО):** 1–3 границы на UX-языке («Что меняется / что НЕ меняется»)
- Architect Gate status: one line if actionable for user; details in `reports/`
- **One next step only:** `/opsx:verify <name>` — без auto-chain, без «или apply»
- **Do NOT** list created artifact paths in chat (non-events / file list handoff — fail)

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
- **Blast Radius (for design artifact)**: если сработал `.cursor/rules/precedent-regression-gate.mdc` или во входном контексте есть блок `## Cross-Archive Context` / явное указание оркестратора на конфликт с архивным change — **обязательна** секция `## Blast Radius` в `design.md`. Таблица (или список строк) со столбцами: **Контракт** | **Архивный источник** (путь к архивному `spec.md` / `proposal.md` или `ADR-NNNN`) | **Бизнес-эффект** (что увидит конечный пользователь 1С — не только имена процедур и реквизитов) | **Альтернативы** | **Обоснование**. Без этой секции Architect Gate по precedent не считается закрытым (см. `architect-gate.mdc`).
- **Implementation Options (for design artifact)**: для UI, интеграций, перехватов и переносов поведения добавить секцию `## Implementation Options`. Минимум: `Option A / Option B`, выбранный вариант, почему он проще/надёжнее, какие варианты отклонены. Конкретная реализация в `tasks.md` должна ссылаться на выбранный вариант, но задача формулируется через результат, а не через рецепт.

**Guardrails**
- **Metadata Gate MUST NOT be silently skipped** (новый change): не вызывать `openspec new change` без ответа на Metadata Gate. Перед финальной сводкой проверить `proposal.md` на `<ФИО>`, `<developer>`, «Уточнить до». Если плейсхолдеры и пользователь не выбирал «пропустить» — WARNING в сводке.
- **Explore context MUST NOT be used only for naming**: Если в последних сообщениях чата найден свежий блок `## Для /opsx:ff` или относится свежий `temp/explore-handoff-*.md` (или legacy `temp/explore-summary-*.md`), прочитать как source context и перенести все поля (Симптом, Корневая причина с маркером, Что менять, Файлы, Приёмка, Связь с архивом, Architect/verify) в `proposal`, `design`, `specs`, `tasks` и Design Gate. Для legacy — те же поля + `Architect Gate`, key decisions, knowledge findings, slice recommendations.
- Create ALL artifacts needed for implementation (as defined by schema's `apply.requires`)
- Always read dependency artifacts before creating a new one
- If context is critically unclear, ask the user - but prefer making reasonable decisions to keep momentum
- If a change with that name already exists, **resume** (шаг 2) — не предлагать отдельную команду continue
- Verify each artifact file exists after writing before proceeding to next
- **Completion checkpoint (MANDATORY on every turn):** Before processing a user follow-up message during ff, run `openspec status --change "<name>" --json`. If any `applyRequires` artifact has status != `"done"`: (1) Notify the user: «Артефакт `<id>` не создан. Продолжить создание?» (2) Complete the missing artifact BEFORE handling the follow-up request. Rationale: user follow-ups in ff are still part of the ff session (`session-discipline.mdc`, Persistence). Missing artifacts must not be silently dropped.
