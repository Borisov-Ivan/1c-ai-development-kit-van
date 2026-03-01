---
name: openspec-debug
description: Investigate a bug (trace/remark/screenshots) in context of an OpenSpec change and plan fixes captured in change artifacts.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: project
  version: "1.0"
---

Investigate a test-found bug and produce a root-cause analysis and a fix plan that is **captured inside the same OpenSpec change**.

This skill is designed for the `/debug` command.

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
5. **Apply (default scenario)**: implement the code fix and update artifacts (add/refine tasks in `tasks.md`, add note in `design.md` if the bug reveals a design gap). Then suggest re-test and `/opsx:apply` for remaining work.

## Guardrails

- **Always separate verified facts from hypotheses in RCA.** Never present a hypothesis as a verified fact.
- **Default scenario:** after producing the fix plan, **implement the code change** and **update artifacts** (tasks + design) in the same change. Only skip implementation or artifact edits if the user explicitly asks for "plan only", "tasks only", or "do not edit artifacts".
- **Never invent metadata names**. Any reference to metadata or types must be validated against XML dumps in `src/` (see "Metadata validation" below).
- If information is insufficient: ask 1–2 targeted questions, then continue.

## Steps

### 1) Determine the change

If the change id is provided: use it.

Otherwise:
- If you can infer a likely change from the conversation context, propose it.
- If ambiguous, run:

```bash
openspec list --json
```

Then use the **AskQuestion** tool to let the user select a change.

Always announce:
- `Using change: <name>`
- How to override: `/debug <other-change>`

### 2) Load change context

Run:

```bash
openspec instructions apply --change "<name>" --json
```

Read `contextFiles` that exist (typically `proposal.md`, `design.md`, `tasks.md`, and `specs/**` if present).

If the user provided a task number/id:
- Locate it in `tasks.md` and treat it as primary scope
- If not found, show nearby tasks and ask the user to confirm the intended one

### 3) Load debug inputs

- If a trace file path is provided: read it as text.
- If screenshots are attached: read image attachments and extract what the UI shows (titles, messages, states).
- If only a textual remark is provided: treat it as evidence and ask for missing reproduction details only if necessary.

### 3.5) Trace analysis (when trace or multi-line stack is available)

**3.5.0. Подготовить контекст для trace-analyst** (перед вызовом агента). На основе шага 2 (уже загружены proposal, design, tasks) синтезировать структурированный бриф:
- Суть доработки (из proposal)
- Ожидаемое поведение затронутой задачи (из tasks.md — конкретная задача, если указан номер)
- Затронутые модули/процедуры (из design.md — секция с архитектурой/модулями)
- Что искать в трассе (вывести из ожидаемого поведения: например, если задача «создать задачи при проведении» — искать вызов создания задач, запись в регистр задач, обработчик проведения)
- Фактический симптом (из шага 3 — текст ошибки / замечание пользователя)

Если шаг 3.5.0 выполнен — передавать trace-analyst путь к трассе **и подготовленный бриф** (см. формат в `.cursor/rules/1c-error-analysis.mdc`, раздел ПОДГОТОВКА КОНТЕКСТА).

If step 3 loaded a trace (PFF/TRACE file) or an error stack with 3+ call lines:

1. **Run onec-trace-analyst** (Task tool, subagent_type="onec-trace-analyst"):
   - Pass the trace file path **and the enriched context brief** (from step 3.5.0).
   - Do not pass only "Parse trace" — use the structured brief so the agent can focus analysis (expected behavior, relevant modules, what to look for in the trace).
   - Obtain: structured summary, key findings relevant to the error, Verified facts / Hypotheses.

2. If the trace-analyst report contains "Insufficient data" or "Request TRACE_FULL", ask the user for the full trace and do not continue the chain until it is provided. Otherwise proceed.

3. **From trace-analyst output, run onec-code-explorer**:
   - Task: restore the full call chain in code (trace shows "what", code shows "why").
   - Pass: list of modules and line numbers from the summary, focus on extension files (e.g. `src/**/cfe/**`).

4. If trace-analyst or explorer identified an **architectural issue** (e.g. write conflicts, transaction problems, data flow issues):
   - **Run onec-code-architect**:
     - Task: propose fix options (transaction boundaries, write order, or skip write in handler).
     - Pass: RCA from trace-analyst/explorer, paths to relevant files.

5. Merge results into step 6 (Root cause): Verified facts and Hypotheses come from trace-analyst output, supplemented by explorer.

### 4) Investigate in codebase (read-only)

If step 3.5 was already run (trace analyzed by subagents), use their output as the basis; do not duplicate manual search.

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

Keep the RCA compact; the split ensures apply/debug can later enforce the hypothesis gate (see `hypothesis-verification-gate.mdc`).

### 7) Plan and apply fixes (default: code + artifacts)

Propose a fix plan in two layers:

**Code steps** (concrete, small): which files to modify, what to change, what to log / edge cases.

**Artifact steps** (to keep "big picture"):
- Add or refine tasks in `openspec/changes/<change>/tasks.md` (under the relevant section or "7. Рефакторинг и качество" as "7.x Исправить: …")
- If the bug reveals a missing/incorrect design decision: add a short note in `design.md`
- **Hypothesis gate:** If the root cause is under **## Hypotheses** (not Verified facts):
  - **First** task in the plan must be **verification** (e.g. add logging, reproduce scenario, check trace) so the hypothesis becomes a verified fact, **or**
  - Explicitly mark a "hypothesis-based fix" and add a **follow-up verification** task after the fix.
  - If the root cause is under **## Verified facts**, you may proceed directly to the fix task(s).

**Default:** implement the code fix and update `tasks.md` and `design.md` as above. Do **not** ask for confirmation before editing unless the user has previously asked for "plan only" or "do not edit".

**If user explicitly prefers:** "plan only" → do not implement or edit artifacts; "tasks only" → implement code + update tasks only; "do not edit artifacts" → implement code only.

### 8) Hand off

After applying the fix and artifacts:
- Suggest re-running the relevant test task(s), then `/opsx:verify` + `/review` if needed
- Suggest `/opsx:apply <change>` for any remaining tasks before `/opsx:archive`
