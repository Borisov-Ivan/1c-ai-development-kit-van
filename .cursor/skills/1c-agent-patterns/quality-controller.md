# Quality Controller — шаблоны промптов

Шаблоны для делегирования `Task(subagent_type="openspec-quality-controller")`. Domain-agnostic readonly-агент. Активная модель — фронтматтер `.cursor/agents/openspec-quality-controller.md`.

         Критерии оценки (Slice Coherence: Scenario Coverage, Slice Independence, Slice Completeness, Slice Dependency Graph, Slice Gate Integrity, Acceptance Checklist 5b, Rework Risk, criteria 8–10) — `.cursor/rules/vertical-slices.mdc`.

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

         ## Out of scope

         Не оценивай: качество формулировки приёмочных шагов, выполним ли
         тест сейчас на ИБ, нужны ли тестовые данные. Это apply/archive.

         Save result to:
         openspec/changes/<change-name>/reports/quality-control-YYYY-MM-DD.md.

         ## Final message to chat (HARD CONSTRAINT)

         Your final assistant message in this turn is a single line:
         \"Отчёт сохранён: openspec/changes/<change-name>/reports/quality-control-YYYY-MM-DD.md\".

         Do NOT include verdict, severity, slice coherence summary, layer
         name, recommendations, or any other analysis в финальном сообщении.
         Full analysis goes ONLY to the saved markdown file.

         Reason: the user does NOT read your final message. The orchestrator
         reads the file and synthesizes a single message for the user.
         Anything you put в финальный assistant message becomes user-visible
         chat noise.

         Cursor will auto-generate a user_visible_high_level_summary card from
         your reasoning. To keep that card readable by the orchestrator (not by
         the user as raw text), AVOID in your reasoning steps:
         - artifact IDs without unfolding: S1.0, S1.T5, Option A, F1
         - engine layer names: Layer N, design-challenge, task-readiness, QC,
           PASS/FAIL/CHALLENGE/APPROVE/REJECT, slice coherence, snapshot
         - internal section names: Three-Question Challenge, Simplicity Check
         Use plain language: «первый ручной шаг», «приёмочный тест единственного
         шаблона», «выбранный вариант реализации».",
  subagent_type="openspec-quality-controller",
  run_in_background=false
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
