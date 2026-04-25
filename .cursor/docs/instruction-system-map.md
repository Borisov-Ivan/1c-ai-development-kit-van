# Instruction System Map

This document defines the source-of-truth map for Cursor instructions in this repository.
It is a maintenance index for humans and agents; runtime behavior remains in rules, skills,
and agent prompts.

## Layers

| Layer | Purpose | Runtime weight |
|---|---|---|
| `AGENTS.md` | Navigation index and command decision tree | Low |
| `.cursor/rules/*.mdc` | Invariants, gates, and safety constraints | Medium to high |
| `.cursor/skills/**/SKILL.md` | Command workflows and procedural protocols | Loaded on demand |
| `.cursor/agents/*.md` | Subagent roles, input contracts, and output contracts | Loaded per subagent |
| `.cursor/docs/**` | References, standards, long examples, history | Loaded by explicit reference |

## Canonical Sources

| Domain | Canonical source | Notes |
|---|---|---|
| 1C dispatch and delegation | `.cursor/rules/1c-agent-delegation.mdc` | Main HALT/delegation dispatcher. |
| Subagent invocation rules | `.cursor/rules/tool-name-guard.mdc` | Defines allowed subagent types and model override policy. |
| Project cf/cfe paths | `.cursor/rules/project-paths.mdc` | `openspec/project.md` remains the data source. |
| BSL write prohibition | `.cursor/rules/bsl-write-guard.mdc` | Short invariant; detailed flow lives in `1c-agent-delegation.mdc`. |
| Metadata XML write prohibition | `.cursor/rules/1c-xml-write-guard.mdc` | Form XML requires manual configuration instructions. |
| Root-cause gate for fixes | `.cursor/rules/verified-cause-gate.mdc` | Applies before behavior-changing fixes. |
| OpenSpec workflow | `.cursor/rules/sdd-workflow.mdc` and command skills | Rules navigate; skills execute. |
| Task decomposition | `.cursor/rules/vertical-slices.mdc` | Replaces phase gates for new work. |
| Legacy phase gates | `.cursor/rules/phase-gates.mdc` | Legacy reference only; not an always-on source. |
| BSL coding standards | `.cursor/docs/1c-coding-standards.md` and `.cursor/docs/standard/**` | Rule file is only a thin loader/redirect. |
| BSL antipatterns | `.cursor/rules/bsl-antipatterns.mdc` and `.cursor/docs/antipatterns/bsl-antipatterns.md` | Reviewer-only. Do not load for writer prompts. |
| OpenSpec output style | `.cursor/docs/opsx-output-style.md` | Skills should reference this instead of duplicating templates. |

## Deprecated Runtime Entries

These entries must not be treated as active capabilities:

| Entry | Status | Replacement |
|---|---|---|
| `phase-gates.mdc` as always-on rule | Deprecated | `vertical-slices.mdc`; `/opsx:migrate-slices` for old tasks. |
| Full `1c-coding-standards.mdc` body | Deprecated | `.cursor/docs/1c-coding-standards.md` and domain docs. |
| `onec-form-generator` | Removed | `1c-forms` skills with XML write guard restrictions. |
| `onec-test-generator` | Removed | Manual/OpenSpec test tasks until test workflow is restored. |
| `onec-metadata-helper` | Removed | `onec-code-explorer` and project metadata rules. |
| `onec-query-optimizer` | Removed | `1c-query-optimization` skill plus architect/reviewer. |

## Maintenance Rules

1. Do not place changelog history in runtime prompts. Use git history or docs.
2. Do not duplicate full gate text across rules, skills, and agents. Reference the canonical source.
3. Deprecated behavior may remain as docs, but must not be `alwaysApply: true`.
4. New command skills should contain workflow steps only; long examples belong in docs.
5. Agent prompts should keep role, input contract, boundaries, and output format. Training examples should be minimal.
