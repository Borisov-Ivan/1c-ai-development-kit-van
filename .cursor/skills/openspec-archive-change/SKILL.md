---
name: openspec-archive-change
description: Archive a completed change in the experimental workflow. Use when the user wants to finalize and archive a change after implementation is complete.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.1"
  generatedBy: "1.1.1"
---

Archive a completed change in the experimental workflow.

**Output style:** итоговое сообщение пользователю (что архивировано, куда, Warnings) — шаблон **T-CONFIRM** из `.cursor/docs/opsx-output-style.md` §5.5: действие → изменённые файлы (новый путь в `archive/`, затронутые specs) → следующий шаг. Блок Warnings — нумерованный список коротких пунктов (см. §4 стайл-гайда). Перед выводом — self-check-5 (§7).

**Auto-yes policy:** Invoking archive means the user accepts the recommended path: proceed despite incomplete artifacts/tasks, **sync delta specs to main** when a delta exists, and **extract all ADR-worthy decisions** from architecture reports. Do **not** use **AskQuestion** for ADR/sync, gaps артефактов шага 2–3 или незакрытых обычных задач без slice-gate — переносить в **Warnings** (шаг 7). **Исключения (AskQuestion разрешён):** шаг 1 — выбор change при неоднозначности; шаг 3.5 — непринятые приёмочные тесты в slice mode; шаг 5.5 — сохранение KB-фактов.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If multiple active changes: run `openspec list --json`, show only active changes (not archived), include schema, and use **AskQuestion** to let user select

   Always announce: "Using change: <name>" and how to override (e.g., `/opsx:archive <other>`).

2. **Check artifact completion status**

   Run `openspec status --change "<name>" --json` to check artifact completion.

   Parse the JSON to understand:
   - `schemaName`: The workflow being used
   - `artifacts`: List of artifacts with their status (`done` or other)

   Maintain a **warnings accumulator** for step 7.

   **If any artifacts are not `done`:**
   - Append to warnings: list each incomplete artifact by name and status (e.g. `Artifact "debug" was not marked done`)
   - **Do not** use AskQuestion; continue automatically

2a. **Verify freshness check (soft-gate, не блокирующий)**

   Grep в `openspec/changes/<name>/reports/` по маскам:
   - `verification-slice-post-final-*.md` (slice mode)
   - `verification-legacy-post-*.md` (legacy mode)

   **Если свежий финальный отчёт verify не найден** — добавить в warnings строку:
   `Final verify report not found. Рекомендуется запустить /opsx:verify <name> до архива, чтобы зафиксировать статус completeness/correctness/coherence.`

   Не блокирует архив — только предупреждает. Если отчёт найден — в summary шага 7 вывести строку `Verify: <имя последнего отчёта> (<дата>)`.

2b. **Knowledge verify в scope ЗНИ (soft-gate, не блокирующий)**

   Определить изменённые файлы: `git diff --name-only <merge-base>...HEAD` (точка ответвления change-ветки от main).

   Найти KB-факты, чьи anchor-paths пересекают этот diff:
   Read `openspec/knowledge/_index.yaml`, фильтр по `anchor-paths` ∈ `diff.files`.

   Verify каждый (алгоритм §3 из knowledge-format.mdc). Для каждого drift:
   - Добавить в warnings accumulator: `KB-NNNN: <drift type> — <title>`
   - Не блокировать archive
   В summary шага 7 вывести: `Knowledge: verified N, drift K (см. /opsx:knowledge-audit)`

3. **Check task completion status**

   Read the tasks file (typically `tasks.md`) to check for incomplete tasks.

   Count tasks marked with `- [ ]` (incomplete) vs `- [x]` (complete).

   **If incomplete tasks found:**
   - Parse task IDs from lines (e.g. `- [ ] 3.1 ...` или `- [ ] S2.4 ...` → include `3.1` / `S2.4` in the warning list when present)
   - Append to warnings: count and, when identifiable, IDs (e.g. `4 incomplete tasks in tasks.md (S1.3, S2.1, S2.4, S3.7)`)
   - **Do not** use AskQuestion; continue automatically

   **If no tasks file exists:** Proceed without task-related warning.

   3.2. **Check developer comment markers balance (HARD BLOCKER)**

   Read `proposal.md` and check for the `## Metadata (comment markers)` block.
   - If the block exists, extract `zni_id`.
   - Build a diff of all `*.bsl` files in the change relative to the baseline (merge-base with main/master).
   - In the diff, count the number of added lines matching the open marker pattern containing `[{zni_id}]` (e.g., `// +++ ... [{zni_id}]`).
   - Count the number of added lines matching the close marker pattern containing `[{zni_id}]` (e.g., `// --- ... [{zni_id}]`).
   - **If the counts do not match:**
     - This is a **hard blocker** (override auto-yes).
     - Do not execute steps 4–7. Show the user:
       ```
       ## Архив заблокирован: дисбаланс маркеров комментариев
       
       Обнаружено несовпадение парных маркеров разработчика для ЗНИ {zni_id}:
       - Открывающих маркеров (// +++): {count_open}
       - Закрывающих маркеров (// ---): {count_close}
       
       Архив возможен только при строгом равенстве.
       Пожалуйста, проверьте код и добавьте недостающие маркеры.
       ```
     - Stop execution (return).
   - **If counts match (or no markers found):** proceed to the next step.

   3.5. **Check slice acceptance status (slice mode only — HARD BLOCKER)**

   Detect slice mode: grep `tasks.md` for `^# Срез S\d+`.

   **Legacy mode (нет `# Срез`):** пропустить шаг 3.5.

   **Bypass `--force-legacy`:** Если в команде пользователя есть флаг **`--force-legacy`**, не показывать карточку и AskQuestion. Сразу добавить в warnings: `Archived with --force-legacy: контракт срезов нарушен; непринятые приёмочные тесты остаются с [ ]` (перечислить каждый `S<N>.T<M>` со статусом `[ ]`, если есть). Продолжить со шага 4.

   **Если slice mode и нет `--force-legacy`:**

   1. Парсинг `tasks.md` по блокам между заголовками `# Срез S<N>`.
      - **Приёмочный тест** — строка чеклиста с ID **`S<N>.T<M>`** (после первой точки идёт буква **`T`**).
      - **Рабочая задача среза** — строка с **`S<N>.<число>`**, где после точки только цифры (например `S1.3`), без `T`.
      - Для каждого среза определить: есть ли **`S<N>.T<M>`** с **`[ ]`**. Если есть — пометить срез «есть непринятые T» и проверить: **все** рабочие задачи этого среза **`[x]`**? Если да — срез **готов к приёмке из archive**; если нет — срез **не готов** (перечислить незакрытые рабочие ID).

   2. **Если все `S<N>.T<M>` = `[x]`** — продолжить со шага 3.6. В финальном summary: `Slices: K/K приняты`.

   3. **Если есть `[ ]` на любом `S<N>.T<M>`:** показать **краткую карточку** (не полный T-HANDOFF из `/opsx:apply`; итоговый вывод archive остаётся **T-CONFIRM**, §5.5):

      ```
      ## Slice gate при архивации — непринятые приёмочные тесты

      | Срез | Тест | Готовность среза | Строка (фрагмент) |
      |------|------|------------------|-------------------|
      | …    | …    | да / нет (+ незакрытые задачи при «нет») | … |
      ```

      Пояснение одной строкой: без **`[x]`** на **`S<N>.T<M>`** контракт среза формально не закрыт; подтверждение ниже фиксирует действие.

   4. **Условие опции A:** опция **A** в AskQuestion допустима **только если** каждый срез, в котором есть **`[ ]`** на **`S<N>.T<M>`**, уже **«готов»** (все рабочие задачи среза **`[x]`**). Если условие не выполнено — перед AskQuestion вывести строку «**Вариант A недоступен:** есть срезы с незакрытыми задачами реализации; завершите через `/opsx:apply <name>`.» и выдать **AskQuestion только с опциями B, C, D**.

   5. **AskQuestion** (исключение из auto-yes). Подписи опций должны явно содержать дисклеймер: подтверждение успешного прогона на ИБ — ответственность пользователя.

      - **A.** *(если выполнено условие п.4)* Принято на ИБ — **отметить все перечисленные `S<N>.T<M>`** с **`[ ]`** как **`[x]`** в `tasks.md`, **продолжить архив** (шаги 4–7 после повторной проверки п.8).
      - **B.** Тесты не пройдены / нужна доработка → **STOP**; рекомендовать `/opsx:apply <name>` или `/opsx:verify <name>`.
      - **C.** Отложить архив → **STOP**.
      - **D.** Принудительное продолжение **без** отметки в `tasks.md` (семантика **`--force-legacy`**) → шаги 4–7; в warnings: `Archived with --force-legacy: …` (перечислить непринятые `S<N>.T<M>`).

   6. Обработка ответов: **B** или **C** → завершить archive (**return**). **D** → warnings как в п.5, продолжить шаг 4.

   7. **Ответ A — обязательные артефакты (MUST):**
      - Для каждой строки **`- [ ] S<N>.T<M>`** среди блокирующих заменить на **`- [x]`** (без изменения текста сценария).
      - **Append** в `debug.md` секцию **`## Slice Gate Decisions`** — по **каждому** затронутому срезу отдельный подблок или один сводный с перечнем тестов; формат:
        ```markdown
        ### Slice S<N> — <краткое имя из заголовка среза> (YYYY-MM-DD)
        Срез: S<N> — <имя>
        Решение: принят (archive)
        Обоснование: подтверждение пользователя при `/opsx:archive`; приёмочные тесты отмечены в tasks.md.
        Изменения tasks: отмечены [x]: <S<N>.T<M>, …>
        Связанный отчёт: reports/slice-acceptance-S<N>-YYYY-MM-DD.md
        ```
      - Для **каждого** затронутого среза создать **`reports/slice-acceptance-S<N>-YYYY-MM-DD.md`** (каноническое имя см. `.cursor/rules/vertical-slices.mdc`): краткий отчёт (факт принятия при архивации, дата, перечень `T<M>`, напоминание что прогон ИБ подтверждён пользователем).

   8. После выполнения п.7 **повторить** парсинг п.1–2: все **`S<N>.T<M>`** должны быть **`[x]`**. Если после правок остался **`[ ]`** — **STOP**, сообщить о несоответствии `tasks.md` (ошибка парсера/формата). Иначе — перейти к шагу **3.6**.

   Итог в summary после успешного прохода без force-legacy: `Slices: K/K приняты` (или с пометкой, что приёмка зафиксирована через **вариант A** при архивации).

   3.6. **Code-Truth Gate (HARD BLOCKER for completed scope)**

   Выполнить `.cursor/rules/code-truth-gate.mdc` для `design.md`, `tasks.md`, `debug.md`, `specs/**`:
   - извлечь технические символы (`pav_*`, имена процедур/функций в backticks, аннотации расширения, стабильные имена элементов формы);
   - проверить их `Grep`/`rg` по путям из `openspec/project.md` и явно затронутым файлам;
   - игнорировать строки-флаги, ADR/KB/Scenario/Requirement, команды `/opsx:*`.

   Если найден `phantom-symbol`, относящийся к `[x]` задаче, принятому срезу или завершённому legacy-scope:
   - это **hard blocker** (override auto-yes);
   - не выполнять шаги 4–7;
   - показать пользователю:
     ```markdown
     ## Архив заблокирован: артефакты ссылаются на несуществующий код

     Найдены технические имена в `design.md` / `tasks.md` / `debug.md` / `specs/**`, которых нет в выгрузке.

     | Symbol | Artifact | Scope |
     |--------|----------|-------|
     | <symbol> | <path> | <task/slice> |

     Варианты:
     1. `/opsx:extend <name> --code-sync` — если код верен, а артефакты устарели.
     2. `/opsx:apply <name>` — если артефакты верны, а код не реализован.
     ```
   - завершить archive (return).

   Если `phantom-symbol` относится только к незавершённым follow-up задачам — добавить warning и продолжить.

4. **Assess delta spec sync state**

   Check for delta specs at `openspec/changes/<name>/specs/`. If none exist, proceed without sync.

   **If delta specs exist:**
   - Compare each delta spec with its corresponding main spec at `openspec/specs/<capability>/spec.md`
   - Determine what changes would be applied (adds, modifications, removals, renames)
   - Show a **brief informational** combined summary to the user (what would be merged), then proceed—**no prompt**

   **Default action (automatic):**
   - If the delta is **already fully reflected** in main specs: note in the final summary (e.g. `Specs: Already up to date with main specs`) and **do not** re-run sync unless you detect drift
   - If **changes are needed**: **always** execute sync using `/opsx:sync` logic (read and follow `.cursor/skills/openspec-sync-specs/SKILL.md` for the active change)

   Proceed to the next step after sync completes or after confirming no merge was needed.

5. **ADR extraction (architecture decision records)**

   Before reading reports, resolve the **planned archive path** for Source fields: `openspec/changes/archive/YYYY-MM-DD-<change-name>/` (same date and name as in step 6). Use `.../reports/<architecture-file>.md` in each ADR **Source** even though the move happens in step 6.

   Check if `reports/architecture-*.md` exists in the change directory.

   **If architecture reports found:**
   - For each `architecture-*.md`, read the report and identify key **decisions** (not analysis/validation).
   - A decision is ADR-worthy if: it affects future changes, involves trade-offs between alternatives, or establishes a contract/pattern/principle. See criteria in `.cursor/rules/adr-format.mdc`.
   - Show a **brief informational** summary of candidate decisions (report file + one-line title each)—**no AskQuestion**
   - **Automatically extract all** ADR-worthy decisions (equivalent to former option «Да, извлечь все»):
     1. Determine next ADR number: Glob `openspec/adrs/ADR-*.md`, take max NNNN + 1 (or 0001 if empty)
     2. For each selected decision, create ADR file using format from `.cursor/rules/adr-format.mdc`:
        - Status: **Accepted** (decision was implemented in the change being archived)
        - Source: planned archive path to the report file (see above)
        - Area: derive from change context (proposal.md topic)
     3. Update `openspec/adrs/README.md` — add row to the index table
   - If no ADR-worthy candidates exist after review, note in summary: `ADR: No ADR-worthy decisions extracted` (no files created)

   **If no architecture reports found:** Skip this step; summary: `ADR: No architecture reports`.

5.5. **Facts extraction (single-decision)**

   Использовать единый extraction-протокол из `.cursor/skills/openspec-knowledge-add/SKILL.md` (разделы `Extraction Contract`, `Candidate Validation`, `Preview / AskQuestion`, `Save Protocol`) с archive-specific overrides ниже. Это единственный источник истины для отбора KB-кандидатов, проверки anchors, dedup, TTL и отказных состояний.

   **Inputs:** `reports/exploration-*.md`, `reports/trace-analysis-*.md`, `reports/resolved-contract-*.md` в каталоге архивируемой ЗНИ. Качество фактов — ответственность самих reports: archive агрегирует verified-факты и применяет фильтры `knowledge-worthy` + `Reuse Value Test`, но не проводит новое обследование кода.

   **Archive-specific overrides:**
   - Planned stable source для `source.report`: `openspec/changes/archive/YYYY-MM-DD-<change-name>/reports/<report>.md` (тот же путь, куда report попадёт после шага 6).
   - Source bundle **не создаётся**: архивный report сам является стабильным source.
   - Если reports не найдены → state = `Skipped — no analytical reports`.
   - Если taxonomy отсутствует → state = `Blocked — taxonomy missing`, warning: `Knowledge: blocked — _taxonomy.yaml отсутствует. Запустите /opsx:knowledge-init или /init-project для генерации.`
   - Если кандидатов нет после фильтров → state = `No candidates after filters`; archive продолжается.
   - Если кандидаты отброшены Reuse Value Test → state = `Deferred N — reuse value not justified`; добавить в warnings краткий список source + проваленные RVT-критерии.
   - Если кандидаты есть → показать per-candidate карточки из `openspec-knowledge-add` и один AskQuestion: «Сохранить N извлечённых KB-фактов? [yes | no]».
   - `yes` → сгенерировать `KB-NNNN-slug.md` + атомарно обновить `_index.yaml` → state = `Saved N (KB-NNNN, ...)`.
   - `no` → ничего не писать → state = `Declined by user`.

   **Mapping состояний (резюме):**

   | Условие | Knowledge state |
   |---|---|
   | Saved (yes на AskQuestion) | `Saved N (KB-NNNN, ...)` |
   | Declined (no на AskQuestion) | `Declined by user` |
   | Reports есть, кандидатов нет после фильтров | `No candidates after filters` |
   | Кандидаты есть, но все/часть отложены Reuse Value Test | `Deferred N — reuse value not justified` (+ Warnings) |
   | Reports не найдены вовсе | `Skipped — no analytical reports` |
   | Reports есть, taxonomy отсутствует | `Blocked — taxonomy missing` |

6. **Perform the archive**

   Create the archive directory if it doesn't exist:
   ```bash
   mkdir -p openspec/changes/archive
   ```

   Generate target name using current date: `YYYY-MM-DD-<change-name>`

   **Check if target already exists:**
   - If yes: Fail with error, suggest renaming existing archive or using different date
   - If no: Move the change directory to archive

   ```bash
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```

7. **Display summary**

   Show archive completion summary including:
   - Change name
   - Schema that was used
   - Archive location
   - Whether specs were synced / up to date / no delta
   - Whether ADRs were extracted (count and numbers) or skipped with reason
   - Knowledge state — одно из шести: `Saved N`, `Deferred N`, `Declined by user`, `No candidates after filters`, `Skipped — no analytical reports`, `Blocked — taxonomy missing` (см. шаг 5.5)
   - **`### Warnings`** — only if the warnings accumulator from steps 2–3 is non-empty; list each bullet. If empty, **omit** the Warnings section entirely.

**Output On Success**

Use this template; adapt lines to facts (omit `### Warnings` when there are none). Do not claim «All tasks complete» when warnings list incomplete tasks—use neutral closing or reference Warnings.

```
## Archive Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Slices:** K/K приняты | N/A (legacy mode) | Принято при архивации (вариант A → `принят (archive)` в debug) | Force-legacy (контракт срезов нарушен)
**Specs:** ✓ Synced to main specs (N requirements updated) | Already up to date | No delta specs
**ADR:** ✓ Extracted N ADRs (ADR-NNNN, ...) | No architecture reports | No ADR-worthy decisions extracted
**Knowledge:** ✓ Saved N (KB-NNNN, ...) | Deferred N — reuse value not justified | Declined by user | No candidates after filters | Skipped — no analytical reports | Blocked — taxonomy missing

### Warnings
- <only when applicable: incomplete artifacts, incomplete tasks with IDs, etc.>
```

**Guardrails**
- Always prompt for change selection if not provided (step 1 only)
- Use artifact graph (`openspec status --json`) for completion checking
- **Don't block archive on warnings** — inform in the final summary (`### Warnings`) and proceed automatically
- **EXCEPTION (slice mode, step 3.5):** при любом `S<N>.T<M>` = `[ ]` — **pause** до **AskQuestion**: варианты **A** (отметить `[x]` и продолжить при готовых срезах), **B/C** (стоп), **D** / **`--force-legacy`** (продолжить без отметки, warnings). Флаг **`--force-legacy`** в команде обходит карточку.
- **Recommended actions are automatic:** delta spec sync when merge is needed; ADR extraction for all ADR-worthy decisions from `reports/architecture-*.md`
- Preserve `.openspec.yaml` when moving to archive (it moves with the directory)
- Show clear summary of what happened
- Use `openspec-sync-specs` approach (agent-driven) whenever sync runs
- If delta specs exist, always run the sync assessment and show the combined summary **before** executing sync (informational only, no confirmation prompt)
