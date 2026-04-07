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

**Auto-yes policy:** Invoking archive means the user accepts the recommended path: proceed despite incomplete artifacts/tasks, **sync delta specs to main** when a delta exists, and **extract all ADR-worthy decisions** from architecture reports. Do **not** use **AskUserQuestion** for these steps—collect issues into the **Warnings** block in the final summary (step 7). Only step 1 may prompt when the target change is ambiguous.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If multiple active changes: run `openspec list --json`, show only active changes (not archived), include schema, and use **AskUserQuestion tool** to let user select

   Always announce: "Using change: <name>" and how to override (e.g., `/opsx:archive <other>`).

2. **Check artifact completion status**

   Run `openspec status --change "<name>" --json` to check artifact completion.

   Parse the JSON to understand:
   - `schemaName`: The workflow being used
   - `artifacts`: List of artifacts with their status (`done` or other)

   Maintain a **warnings accumulator** for step 7.

   **If any artifacts are not `done`:**
   - Append to warnings: list each incomplete artifact by name and status (e.g. `Artifact "debug" was not marked done`)
   - **Do not** use AskUserQuestion; continue automatically

3. **Check task completion status**

   Read the tasks file (typically `tasks.md`) to check for incomplete tasks.

   Count tasks marked with `- [ ]` (incomplete) vs `- [x]` (complete).

   **If incomplete tasks found:**
   - Parse task IDs from lines (e.g. `- [ ] 3.1 ...` → include `3.1` in the warning list when present)
   - Append to warnings: count and, when identifiable, IDs (e.g. `4 incomplete tasks in tasks.md (3.1, 3.2, 4.1, 5.3)`)
   - **Do not** use AskUserQuestion; continue automatically

   **If no tasks file exists:** Proceed without task-related warning.

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
   - Show a **brief informational** summary of candidate decisions (report file + one-line title each)—**no AskUserQuestion**
   - **Automatically extract all** ADR-worthy decisions (equivalent to former option «Да, извлечь все»):
     1. Determine next ADR number: Glob `openspec/adrs/ADR-*.md`, take max NNNN + 1 (or 0001 if empty)
     2. For each selected decision, create ADR file using format from `.cursor/rules/adr-format.mdc`:
        - Status: **Accepted** (decision was implemented in the change being archived)
        - Source: planned archive path to the report file (see above)
        - Area: derive from change context (proposal.md topic)
     3. Update `openspec/adrs/README.md` — add row to the index table
   - If no ADR-worthy candidates exist after review, note in summary: `ADR: No ADR-worthy decisions extracted` (no files created)

   **If no architecture reports found:** Skip this step; summary: `ADR: No architecture reports`.

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
   - **`### Warnings`** — only if the warnings accumulator from steps 2–3 is non-empty; list each bullet. If empty, **omit** the Warnings section entirely.

**Output On Success**

Use this template; adapt lines to facts (omit `### Warnings` when there are none). Do not claim «All tasks complete» when warnings list incomplete tasks—use neutral closing or reference Warnings.

```
## Archive Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** ✓ Synced to main specs (N requirements updated) | Already up to date | No delta specs
**ADR:** ✓ Extracted N ADRs (ADR-NNNN, ...) | No architecture reports | No ADR-worthy decisions extracted

### Warnings
- <only when applicable: incomplete artifacts, incomplete tasks with IDs, etc.>
```

**Guardrails**
- Always prompt for change selection if not provided (step 1 only)
- Use artifact graph (`openspec status --json`) for completion checking
- **Don't block archive on warnings** — inform in the final summary (`### Warnings`) and proceed automatically
- **Recommended actions are automatic:** delta spec sync when merge is needed; ADR extraction for all ADR-worthy decisions from `reports/architecture-*.md`
- Preserve `.openspec.yaml` when moving to archive (it moves with the directory)
- Show clear summary of what happened
- Use `openspec-sync-specs` approach (agent-driven) whenever sync runs
- If delta specs exist, always run the sync assessment and show the combined summary **before** executing sync (informational only, no confirmation prompt)
