# Changelog — 1C Agent Ecosystem

## [2.0] - 2026-03-08

### Changed (onec-code-explorer)
- Added TASK CLASSIFICATION: Focused Investigation / Hypothesis Verification / Full Feature Exploration
- Added Phase 0: Process Caller Context (use trace-analyst findings, classify task before code reading)
- Added Extension Analysis (cf/cfe): annotation types, base contract, interplay mapping, risks
- Added Verified Facts / Hypotheses format in Output Guidance with explicit markers
- Added Hypothesis Verification Template (mini-template for hypothesis reports)
- Refined anti-pattern: "no design decisions" instead of blanket "no recommendations"; exploration facts (extension points, contracts) are allowed
- Renamed Recommendations → Extension Points / Modification Notes in output template
- Linked Report Levels to Task Classification (Compact / Hypothesis Template / Full)
- Marked Architecture Analysis and Phases 3-4 as optional (Full Exploration only)
- Replaced Example 2, added Example 3 with realistic cf/cfe scenarios

## [1.1] - 2026-02-27

### Changed
- All agents: BSL LSP marked as NOT_CONNECTED with MCP fallback
- All agents: RLM marked as NOT_CONNECTED
- sdd-workflow.mdc: reduced to navigation document
- onec-code-explorer: added depth control, report levels, anti-patterns
- onec-code-writer: added per-invocation scope limit, idempotency
- onec-code-architect: added OpenSpec integration, plan revision, realistic testing
- onec-code-reviewer: fixed SQL->1C examples, removed aspirational integrations
- onec-code-simplifier: fixed model metadata, added pipeline integration
- 1c-dispatch-gate.mdc, 1c-agent-delegation.mdc: added Light Mode (точечная правка)

## [1.0] - 2026-02-08
- Initial version of all agents
- Source: AndreevED/1c-ai-feature-dev-workflow + improvements
