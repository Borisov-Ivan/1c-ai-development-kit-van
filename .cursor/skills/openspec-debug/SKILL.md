---
name: openspec-debug
description: Investigate a bug (trace/remark/screenshots) in context of an OpenSpec change; produce RCA and capture fix tasks in change artifacts.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: project
  version: "2.1"
---

Investigate a test-found bug and produce a root-cause analysis and a fix plan that is **captured inside the same OpenSpec change**.

This skill is designed for the `/opsx:debug` command (alias: `/debug`).

## Input (free-form)

The user may provide any combination of:
- Trace file path (e.g. `C:/GitHub/PavDO/temp/Замеры/...txt`)
- Textual remark / expected vs actual behavior
- Screenshots (attached images)
- Optional OpenSpec change id (e.g. `fix-exclude-participants-v2`)
- Optional task number/id (e.g. `4.3`)

## Output (what you must produce)

1. **Scope**: which change and which task(s) this relates to
2. **Evidence summary**: what the trace/remark/screenshots show
3. **Root cause**: why it happens (with file/function references)
4. **Fix plan**: code steps + artifact steps (tasks.md, design.md)
5. **Apply (default scenario)**: capture tasks in `tasks.md` for `/opsx:apply` and update artifacts (add/refine tasks, add note in `design.md` if the bug reveals a design gap). Then hand off to `/opsx:apply <change>` for implementation.

## Guardrails

- **Always separate verified facts from hypotheses in RCA.** Never present a hypothesis as a verified fact.
- **Default scenario:** after producing the fix plan, **capture tasks** in tasks.md and update design.md. Code implementation is done via `/opsx:apply`. Only skip artifact edits if the user explicitly asks for "plan only".
- **Never invent metadata names**. Any reference to metadata or types must be validated against XML dumps in `src/` (see "Metadata validation" below).
- If information is insufficient: ask 1–2 targeted questions, then continue.

## Steps

## Entry Protocol (MANDATORY)

При входе в debug **первый шаг** — определить change, загрузить контекст, сформировать и **показать бриф**. До подтверждения брифа запрещены: вызов Task (trace-analyst, explorer, architect), чтение файла трассы. Единственные допустимые действия до брифа: Read этого скилла (command-skill-gate), определение change, загрузка артефактов change и project.md. После показа брифа — **END TURN**; продолжение — только после явного подтверждения пользователя в следующем сообщении.

### 0. Определить change и загрузить контекст

- Если change id указан в запросе — использовать его.
- Иначе: выполнить `openspec list --json`, при неоднозначности — **AskQuestion** для выбора change.
- Объявить: `Using change: <name>`, способ переопределения: `/debug <other-change>`.
- Выполнить `openspec instructions apply --change "<name>" --json`.
- Прочитать существующие `contextFiles` (proposal.md, design.md, tasks.md, specs/** при наличии).
- Прочитать `openspec/project.md` — извлечь пути к cf и cfe из секции «Структура репозитория» (для передачи субагентам по правилу project-paths.mdc).
- Если пользователь указал номер задачи: найти её в tasks.md и считать основной областью; если не найдена — показать соседние и уточнить.

### 0b. Классификация входа и бриф

- **Классифицировать вход:** трасса (путь к .pff / *_TRACE_*.txt) / текстовое замечание (ожидание vs реальность) / скриншот(ы).
- **Сформировать бриф** из:
  - Контекст (суть доработки из proposal)
  - Сценарий (ожидаемое поведение затронутой задачи из tasks.md; при указанном номере задачи — её описание)
  - Затронутые модули/процедуры (из design.md)
  - Симптом (текст ошибки / замечание пользователя; при трассе — описание из пользовательского ввода, **не** из чтения файла трассы)
  - Артефакты (пути к трассам, скриншотам, файлам)
  - План исследования: 1 → onec-trace-analyst (при трассе) или пропуск; 2 → по результатам: onec-code-explorer (VQ или полная цепочка); 3 → при архитектурной проблеме: onec-code-architect; 4 → RCA → задачи в tasks.md → hand off на /opsx:apply
- **Показать бриф** пользователю по шаблону ниже.
- **END TURN.** Не вызывать Task, не читать трассу. Дождаться явного подтверждения («ОК», «Да», «Подтверждаю») в **следующем** сообщении.

**Шаблон брифа (формат — T-BRIEF по `.cursor/docs/opsx-output-style.md`):**

```
---
**Бриф для отладки (change: <name>)**

- **Контекст:** [UX-слой, 1 предложение из proposal — зачем существует change; без D<N>/S<N>.T<M>/R<N>]
- **Сценарий:** [UX-слой, 1–2 предложения: что должно происходить в отлаживаемой задаче; без внутренних ID]
- **Симптом:** [UX-слой, только факты; 1 предложение или нумерованный список; без «должно быть»]
- **Технический контекст:** [Код-слой, список `path/Module.bsl` / `ИмяПроцедуры` / метаданных в backticks; без UX-надписей]
- **Артефакты:** [пути к трассам, скриншотам — по одному на строку]

**План** (разрешены внутренние ID):
1. → `onec-trace-analyst` (если есть трасса) — путь к трассе + бриф
2. → `onec-code-explorer` — верификация VQ / полная цепочка
3. → `onec-code-architect` — если сработал architect-gate
4. → RCA (Verified / Hypotheses) → задачи в `tasks.md` → hand off на `/opsx:apply <change>`

Бриф верный? Подтвердите — начну с шага 3 (загрузка входов) и делегирования.
---
```

**Self-check перед выводом** (см. `.cursor/docs/opsx-output-style.md` §7): (1) слои разделены — в «Симптом/Сценарий/Контекст» нет `D<N>/S<N>.T<M>/R<N>/I<N>/SC<N>` и номеров задач вида `12.9`; (2) имена объектов — UX-надписи в «ёлочках», идентификаторы кода в backticks, не подряд 3+ разнотипных термина без русского слова-разделителя; (3) любое перечисление ≥2 пунктов — нумерованный список; (4) «Симптом» без формулировок «должно быть / ожидается»; (5) каждое поле ≤3 строк или ≤7 пунктов списка.

Если данных недостаточно для брифа — задать 1–2 уточняющих вопроса (AskQuestion). **После подтверждения** перейти к шагу 3 (Load debug inputs) и далее.

---

## Per-turn Delegation Gate (MANDATORY на follow-up)

На **каждом follow-up ходе** (после завершения Entry Protocol) перед выполнением действия:

1. **Классифицировать запрос:** подразумевает ли он обследование кода, трассировку вызовов, анализ модулей?
2. **Маркеры обследования:** «обследуй», «проверь в коде», «найди где», «проследи вызов», «уточни в коде», «посмотри модуль», «как вызывается», «откуда берётся», а также контекст задач из tasks.md типа «уточнить в коде базы».
3. **При срабатывании → СТОП:**
   - НЕ запускать Grep, Glob, Read по .bsl/.xml модулям для анализа логики.
   - Сформировать бриф (агент + что искать + артефакты контекста).
   - Делегировать через Task (onec-code-explorer / onec-trace-analyst / onec-code-architect).
4. **Допустимо до делегирования:** Read артефактов OpenSpec (proposal, design, tasks, specs) для обогащения брифа — до 3 файлов. Grep/Glob/Read по .bsl для обследования логики — запрещено; допустимы точечные обращения (пути к файлам, проверка наличия процедуры) в объёме до 3 обращений.

Контекст оркестратора — дорогой ресурс; обследование кода выполняют субагенты в изолированном контексте.

---

### 3) Load debug inputs

- **Если указан путь к файлу трассы:** зафиксировать путь. **Не читать** файл трассы — он будет передан onec-trace-analyst по пути. Записать только текстовое описание ошибки пользователя как доказательство (симптом). См. `.cursor/rules/1c-error-analysis.mdc` (ЗАПРЕТ подменять trace-analyst ручным чтением).
- If screenshots are attached: read image attachments and extract what the UI shows (titles, messages, states).
- If only a textual remark is provided: treat it as evidence and ask for missing reproduction details only if necessary.

### 3.5) Trace analysis (when trace or multi-line stack is available)

**3.5.0. Контекст для trace-analyst.** Бриф уже подготовлен в Entry Protocol (шаг 0b). Здесь — финализация: убедиться, что в промпт trace-analyst входят суть доработки (proposal), ожидаемое поведение затронутой задачи (tasks.md), затронутые модули (design.md), что искать в трассе (вывести из ожидаемого поведения), фактический симптом (из шага 3 — текст ошибки/замечание пользователя). Передавать trace-analyst **путь к файлу трассы** (не содержимое) и подготовленный бриф (см. `.cursor/rules/1c-error-analysis.mdc`, шаг 1 ДЕЙСТВИЕ — «Подготовить бриф»).

If step 3 loaded a trace (PFF/TRACE file) or an error stack with 3+ call lines:

1. **Run onec-trace-analyst** (Task tool, subagent_type="onec-trace-analyst"):
   - Pass the trace file path **and the enriched context brief** (from step 3.5.0).
   - Do not pass only "Parse trace" — use the structured brief so the agent can focus analysis (expected behavior, relevant modules, what to look for in the trace).
   - Obtain: structured summary, key findings relevant to the error, Verified facts / Hypotheses.

2. If the trace-analyst report contains "Insufficient data" or "Request TRACE_FULL", ask the user for the full trace and do not continue the chain until it is provided. Otherwise proceed.

3. **Verification queries** — check if the trace-analyst report contains a `## Verification queries for explorer` section with VQ-items:
   - **If VQ-items exist**: run **onec-code-explorer** with the targeted verification prompt (template «Explorer — верификация гипотез trace-analyst» from `1c-agent-patterns/SKILL.md`). Pass: path to the trace-analyst report, the VQ list, and modules_hint from the report. Explorer returns a confirms/refutes/inconclusive answer for each VQ with code citations.
   - **If no VQ-items**: skip to step 4.

4. **Merge VQ answers into RCA** (only if step 3 ran explorer):
   - For each VQ where explorer answered **confirms** — move the corresponding hypothesis to Verified facts (with explorer's code citation).
   - For each VQ where explorer answered **refutes** — record as "Refuted hypothesis" (valuable context for architect).
   - For each VQ where explorer answered **inconclusive** — keep as Hypothesis with updated verification plan.
   - Result: updated Verified facts / Hypotheses / Refuted hypotheses for the final RCA.

5. **Full code exploration** (conditional) — run **onec-code-explorer** for the full call chain only if:
   - Step 3 did NOT already call explorer (no VQ-items existed), OR
   - After step 4 merge, significant unresolved hypotheses remain, OR
   - The trace involves 3+ modules and a full call chain reconstruction is needed.
   - Task: restore the full call chain in code (trace shows "what", code shows "why").
   - Pass: list of modules and line numbers from the trace-analyst summary + VQ verification results (if available), focus on extension files (e.g. `src/**/cfe/**`).
   - If step 3 already called explorer and all hypotheses are resolved — skip this step.

6. If trace-analyst or explorer identified an **architectural issue** (e.g. write conflicts, transaction problems, data flow issues):
   - **Run onec-code-architect**:
     - Task: propose fix options (transaction boundaries, write order, or skip write in handler).
     - Pass: RCA from trace-analyst/explorer, paths to relevant files.

7. Merge results into step 6 (Root cause): Verified facts and Hypotheses come from trace-analyst output, enriched by VQ verification (step 4) and supplemented by explorer (step 5).

**3.5.8. Сохранение отчётов субагентов.** После шагов 3.5.1–3.5.7 сохранить полные отчёты аналитических агентов по правилу `preserve-subagent-reports.mdc`: отчёт onec-trace-analyst — в `openspec/changes/<id>/reports/trace-analysis-YYYY-MM-DD.md` (или `temp/reports/` при отсутствии change); отчёт onec-code-explorer — в `reports/exploration-YYYY-MM-DD.md` или `reports/resolved-contract-*-YYYY-MM-DD.md` при investigation loop; отчёт onec-code-architect — в `reports/architecture-YYYY-MM-DD.md`. В design.md / debug.md ссылаться на полный отчёт (путь к файлу), не дублировать выжимку.

7.5. **Anti-pattern detection (optional).**
   After RCA is established, evaluate whether the root cause represents a **generalizable anti-pattern** that could recur in other code.
   Three criteria (ALL must be met):
   - **Повторяемость**: паттерн может встретиться в другом коде (не уникален для данного модуля/сценария).
   - **Пробел в ревью**: текущий ревьювер НЕ обнаружит этот паттерн (нет AP-NNN в `.cursor/rules/bsl-antipatterns.mdc`).
   - **Обобщаемость**: можно сформулировать абстрактный принцип (без привязки к конкретному change/модулю).

   If all three criteria are met:
   - Inform user: «Ситуация [описание] тянет на антипаттерн — зарегистрируем? [Да / Нет]»
   - User may also directly ask: «зарегистрируй антипаттерн».
   - On confirmation:
     1. Grep `.cursor/docs/antipatterns/bsl-antipatterns.md` for existing similar AP.
     2. Determine next AP-NNN ID.
     3. Formulate generalized principle (abstract, not tied to current incident).
     4. Add full card to `.cursor/docs/antipatterns/bsl-antipatterns.md`.
     5. Add index entry to `.cursor/rules/bsl-antipatterns.mdc`.
   - On rejection: note in debug.md (section «Anti-pattern considered but not registered»).

### 4) Investigate in codebase (read-only)

If step 3.5 was already run (trace analyzed by subagents), use their output as the basis; do not duplicate manual search.

**Context Strategy:** если исследование требует анализа 3+ файлов или файлов данных (XML, HTML, CSV) — применить стратегию из `.cursor/skills/context-strategy/SKILL.md` (инвентаризация → decision matrix → субагенты → синтез).

Use the trace/remark to identify likely modules and entry points:
- Search for procedure/function names from the trace
- Search for key phrases from exception messages
- Narrow down to the modules changed by this change (prefer extension `src/**/cfe/**` first)

Read the relevant files and map an execution path:
- "What calls what"
- Inputs/outputs that lead to the failure
- Conditions that differ from the expected behavior in design/tasks

### 5) Metadata validation (mandatory)

Before concluding anything that mentions metadata names or types, validate against XML in `src/`.

**Applies to any of these forms:**
- `Перечисления.X.Y`
- `РегистрСведений.X` / `РегистрНакопления.X` / `РегистрБухгалтерии.X` / …
- `Справочники.X`, `Документы.X`, `БизнесПроцессы.X`, `Задачи.X`, …
- `Тип("СправочникСсылка.X")`, `Тип("ПеречислениеСсылка.X")`, etc.
- `Метаданные.<Type>.<Name>` usage

**How to validate (unified paths):**
- Search under `src/` recursively for the relevant XML:
  - Enum: `src/**/Enums/<X>.xml` and its `EnumValue` names
  - Register: `src/**/InformationRegisters/<X>.xml` and its dimensions/resources/attributes
  - Catalog/Document/BP/Task/etc.: `src/**/<Kind>/<X>.xml`
  - If unsure of kind: look in `src/**/Configuration.xml` for `<Enum>`, `<InformationRegister>`, `<Catalog>`, etc.

**If not found:**
1. Search alternatives (similar names in the same folder and in `Configuration.xml`)
2. Show the user available candidates (a short list)
3. **STOP**: do not use an unverified name in conclusions or plan

### 6) Root cause and conclusions

Write a **structured RCA** with two mandatory sections. Never present a hypothesis as a verified fact.

**## Verified facts**

- What is **definitely established** from the evidence (trace, log, code).
- Each fact must have a **concrete reference**: trace line number, log entry, file:line in code.
- Example: "In trace line 15540, M15:47, `pavIU_ИсполнительИсключен` is called; trace shows branch 'excluded' at M15:50."

**## Hypotheses**

- What is **assumed** but not directly proven (e.g. "algorithm returns exclude because of missing executor context").
- For each hypothesis, add a **verification plan**: what to log, which scenario to run, what to check in the trace — or mark "hypothesis-based fix" with a follow-up verification task.

Keep the RCA compact; the split ensures apply/debug can later enforce the verified cause gate (see `verified-cause-gate.mdc`).

### 5.5) Architect Gate (после RCA, до фикса)

Перед переходом к плану фикса проверить триггеры из `.cursor/rules/architect-gate.mdc` (объективные маркеры, семантические, структурные). В контексте debug автоматически срабатывают: **bug fix** (объективный маркер); наличие отчётов trace-analyst или explorer в сессии (объективный маркер «вызывался trace-analyst/explorer»). Дополнительно проверить остальные триггеры (перехват базовой процедуры, новый объект в design, несколько точек реализации, фикс меняет UX-сценарий и т.д.).

- **При срабатывании любого триггера:** вызвать **onec-code-architect** с брифом (RCA, корневая причина, предложенный подход, Fix Quality чеклист). Использовать шаблон «Architect — fix quality review» из `1c-agent-patterns/SKILL.md`. Результат сохранить в `reports/architecture-debug-YYYY-MM-DD.md` по `preserve-subagent-reports.mdc`. Учесть рекомендации в плане фикса (шаг 7). **К шагу 7 переходить ТОЛЬКО после получения отчёта архитектора.**
- **Исключение:** пользователь явно пишет «пропустить архитектора» → в debug.md секция «Architect Gate» с записью «Пользователь отклонил. Причина: …» → затем шаг 7. Оркестратор **НЕ** принимает решение «пропустить» самостоятельно (не допускается обоснование «фикс точечный»).
- **Триггеры не сработали** — перейти к шагу 7 без вызова архитектора.

Исключения по architect-gate.mdc (Gate не срабатывает): Light Mode без семантических триггеров и без изменения UX-сценария, рефакторинг без изменения поведения, опечатки. В debug типичный сценарий — bug fix, поэтому проверка обязательна.

### 7) Plan and capture tasks (default: artifacts + hand off)

**7a. Plan** — предложить план в двух слоях:

**Code steps** (конкретные, мелкие): какие файлы менять, что менять, что логировать / граничные случаи.

**Artifact steps:**
- Добавить или уточнить задачи в `openspec/changes/<change>/tasks.md` **с привязкой к срезу**:
  - **Если ЗНИ в slice mode** (есть `# Срез S<N>`): определить, к какому срезу относится фикс.
    - Дефект в **непринятом** срезе S<N> (есть задачи `[ ]` или S<N>.T<M> = `[ ]`) → добавить задачу как `S<N>.<M+1>` **перед** приёмочным `S<N>.T<M>`.
    - Дефект в **уже принятом** срезе S<K> (S<K>.T<M> = `[x]`) → **не** переоткрывать его. Создать **fix-срез**: новый раздел `# Срез S<N+1>: Исправление дефекта S<K> — <короткое описание>` с метаданными (`**Сценарий:** воспроизведение дефекта, проверка фикса`, `**Зависимости:** S<K>`, `**Связь со spec:**` — те же сценарии, что в S<K>) и собственным `S<N+1>.T<M>`. Альтернатива — в рамках уже идущего следующего среза добавить «fix» задачи с пометкой `(исправление S<K>)` если они не нарушают сценарий этого среза.
    - Дефект, не относящийся ни к одному существующему срезу — создать новый срез аналогично.
  - **Если ЗНИ в legacy mode** (нет `# Срез`): вставлять в соответствующую секцию или «7. Рефакторинг и качество» как «7.x Исправить: …»; при наличии устаревших `<!-- phase-gate` маркеров — рекомендовать `/opsx:verify --migrate-to-slices` отдельным сообщением (но **не** автоматически).
- При выявленном пробеле в design — краткая заметка в `design.md` (для slice-mode — обязательно обновить `## Slices`, если меняется состав срезов).
- **Hypothesis gate:** если корневая причина в **## Hypotheses**: первая задача плана — верификация (логирование, воспроизведение, проверка трассы) **или** явная пометка «hypothesis-based fix» + задача follow-up верификации после фикса. Если корневая причина в **## Verified facts** — переходить к задачам фикса.

**Slice Gate Decisions log:** если фикс — следствие неуспешной приёмки среза в `/opsx:apply` (пользователь выбрал `[3] Дефект в предыдущем срезе` или `[2] Не принят`), эта debug-сессия должна оставить запись в `debug.md` секции `## Slice Gate Decisions`: дата, ID среза, решение, RCA, ссылки на отчёты trace-analyst/explorer/architect, новые задачи фикса.

**Default:** после плана выполнить 7b (артефакты) и hand off. Не спрашивать подтверждение перед правкой артефактов, если пользователь не просил «plan only». **Если пользователь явно:** "plan only" — не править артефакты.

---

**7b. Update artifacts.** Обновить `tasks.md` и при необходимости `design.md`. Формирование задач в tasks.md:
- Каждая задача — одна конкретная правка (файл, процедура, что менять, почему — ссылка на RCA).
- В тексте задачи указать корневую причину (Verified / Hypothesis), чтобы apply при вызове writer мог передать Root Cause Context.
- Slice-aware вставка: применяются правила из 7a (slice mode → правильный срез / fix-срез; legacy → плоский список). Для slice mode каждая новая задача получает ID `S<N>.<M>` в рамках своего среза.
- Задачи на верификацию гипотезы или follow-up — по Hypothesis gate в 7a.

### 8) Hand off

После обновления артефактов:
- Предложить: `/opsx:apply <change>` для реализации задач. При наличии hypothesis-based задач — предупредить о необходимости верификации (или задачи follow-up в tasks.md).

---

## Интеграция

- **Output style:** `.cursor/docs/opsx-output-style.md` — бриф отладки выводится по шаблону **T-BRIEF**; перед отправкой — self-check-5 (§7).
- **command-skill-gate.mdc:** первый и единственный инструмент в первом батче при вызове команды — Read этого скилла.
- **command-session-persistence.mdc:** протокол debug действует на **каждом** ходе сессии (Entry Protocol, Per-turn Gate, шаги 3–8). Выход из протокола — только по явному завершению пользователем или смене команды.
- **1c-agent-delegation.mdc (APPLY GATE):** debug не реализует код — реализация через `/opsx:apply`. Writer и reviewer вызываются только в контексте apply.
- **preserve-subagent-reports.mdc:** полные отчёты trace-analyst, explorer, architect сохранять в `openspec/changes/<id>/reports/` (или `temp/reports/`); в design/debug ссылаться на файл отчёта.
- **architect-gate.mdc:** единый источник триггеров для шага 5.5 (Architect Gate после RCA).
- **project-paths.mdc:** пути к cf и cfe брать из `openspec/project.md`; передавать субагентам (explorer, trace-analyst, architect) в промпте.
- **context-strategy-gate.mdc:** при исследовании 3+ файлов или файлов данных — загружать `.cursor/skills/context-strategy/SKILL.md` и следовать Entry Protocol до чтения файлов.
- **1c-error-analysis.mdc:** не читать трассу вручную; делегировать onec-trace-analyst с путём и брифом. TRACE_FULL по запросу агента — запросить у пользователя.
- **verified-cause-gate.mdc:** перед фиксом — разделение Verified facts / Hypotheses, цепочка «Почему», корневая причина; hypothesis-based fix только с задачей верификации или follow-up.

---

**Last updated**: 2026-03-16 | **Version**: 2.1 | **Changes**: Debug не реализует код — убраны 7b–7g (writer, LINT, API, EXTENSION, reviewer, Investigation Loop). Остаётся RCA + задачи в tasks.md + hand off на /opsx:apply. APPLY GATE в Integration.
