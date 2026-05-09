# Quality Controller — шаблоны промптов

Шаблоны для делегирования `Task(subagent_type="openspec-quality-controller")`. Domain-agnostic readonly-агент. Активная модель — фронтматтер `.cursor/agents/openspec-quality-controller.md`.

Критерии оценки (Slice Coherence: Scenario Coverage, Slice Independence, Slice Completeness, Slice Dependency Graph, Slice Gate Integrity, Rework Risk) — `.cursor/rules/vertical-slices.mdc`.

Общие правила, обработка ошибок — `SKILL.md` (навигатор).

---

## Quality Controller — slice coherence review (verify шаг 7.6)

Used by `/opsx:verify` step 7.6 — MANDATORY in every pre-apply verification. Domain-agnostic assessment of task ordering, dependencies, and execution risk. Complements the architect's realizability review (step 7.7).

**Agent file:** `.cursor/agents/openspec-quality-controller.md` (model: Opus, readonly). Role, evaluation criteria and output format defined in agent system prompt.

```
Task(
  description="Quality Control [change-name]",
  prompt="## Artifacts

         - tasks: <path to tasks.md>
         - design: <path to design.md>
         - proposal: <path to proposal.md>
         - specs: <path to specs/>
         - Manual config checklist (verify step 7.5):
           <checklist table or 'none found'>
         - Mechanical check issues (verify steps 7A-7E):
           <list or 'none'>
         - Repository state: <list of existing objects/files
           mentioned in tasks, with empty/non-empty status>

         Save result to:
         openspec/changes/<change-name>/reports/quality-control-YYYY-MM-DD.md.",
  subagent_type="openspec-quality-controller"
)
```

**Slice-transition context (optional):** When verify runs in slice-transition mode (between accepted and next slice), add to the prompt:

```
         ## Slice-transition context (only if mode = slice-transition)
         - Mode: slice-transition
         - Accepted slice: S<N>
         - Completed slice tasks: <list of [x] S<N>.* tasks>
         - Upcoming slices and their tasks: <list of [ ] S<N+1>.*, S<N+2>.*...>
         - Slice Gate Decisions (debug.md): <content or 'none'>
         - Implementation notes (debug.md): <content or 'none'>
```
