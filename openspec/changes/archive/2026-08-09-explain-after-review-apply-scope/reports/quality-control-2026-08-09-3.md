# Quality Control — explain-after-review-apply-scope

Date: 2026-08-09  
Report: `quality-control-2026-08-09-3.md` (re-verify after repair-from-verify; does not overwrite `-2` / base)  
Mode: slice (detected `# Срез S1`)  
Scope: slice coherence, scenario coverage, independence, gates, rework risk, verticality, self-achievable acceptance, foundation+gate, acceptance simplicity, User Task Contract, task readability  
Out of scope: IB executability now, test data, baseline snapshots

Context (prompt): repair updated design D1/D2a/D4/D5 + tasks S1.2–S1.4 + spec Apply artifacts SSOT `code-map`; checkboxes and slice-gate intact; kit meta-change under `.cursor/`.

Manual config checklist (verify 7.5): none (kit meta-change; no Configurator markers)  
Mechanical hygiene (verify 7A–7E): consistent with prompt (checkboxes, one slice-gate, fences OK; `form_mode: n/a`)  
User Task Contract pre-check (verify 2.1a): none provided; QC mechanical+semantic check below — no DENY hits in S1.1–S1.9; S1.9 ALLOW-agent

## Verdict

`OK`

## Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1 Explain scope после review/apply | After review/apply kit offers `/opsx:explain` and B-explain shows processed-code scope before map | S1.1–S1.9 (9) | S1.accept (Primary + 3 optional; all 10 spec scenarios covered via Primary / optional / S1.\<M\> → 10/10) | нет | `<!-- slice-gate -->` present |

Notes: Standard size (9 impl + accept); single-slice default matches design `## Slices` and thresholds (6–15 → 1 slice unless independent outcomes). `**Режим apply:** mechanical`. Product BSL/Form/XML not required.

Repair alignment (post D1/D2a/D4/D5): S1.2 pins apply SSOT to `code-map.md` + handoff copy/link; S1.3/S1.4 encode propose priority vs MUST_FIX/extend (D2a); Primary + S1.6–S1.7 encode compact Охват / paths-in-Контекст (D4) and MVP prefill-only-with-section (D5). No new slice split introduced.

## Scenario Coverage

| Scenario | Covered by | Status |
|---|---|---|
| Review report has Explain scope | S1.1; Связь со spec | OK |
| Apply artifacts have Explain scope | S1.2 (SSOT code-map + handoff copy/link); Связь со spec | OK |
| Review offers explain | S1.3; optional accept (paraphrased «Review/Apply offer explain») | OK |
| Apply offers explain | S1.4; optional accept (same paraphrased bullet) | OK |
| Trivial review skips default propose | S1.3; optional «Trivial skip» (name paraphrase) | OK |
| Prefill Охват from review | Primary; S1.6–S1.7 | OK |
| Huge release uses Варианты | Primary («или Варианты»); S1.6 | OK |
| No mass Read before confirm | Primary (карта до «да»); S1.6 (Read ≤3) | OK |
| Compact paths allowed | S1.7 (HALT / entry-brief); design D4 | OK |
| Explore still suggests explain | S1.9; optional accept (literal name) | OK |

## Dependency Graph

```mermaid
flowchart LR
  S1[S1 Explain scope после review/apply]
```

- Cycles: none  
- Forward acceptance dependencies: none (single slice)  
- Undeclared dependencies: none (`**Зависимости:** нет`)  
- Parallel change `independent-review-disposition`: out of scope per proposal (no cross-slice dependency declared or required)

## Checklist Results

| # | Criterion | Result |
|---|---|---|
| 1 | Scenario Coverage | Pass — all 10 `#### Scenario:` covered by Primary, optional accept, and/or agent `S1.<M>` (static «по коду kit» for explore/HALT paths) |
| 2 | Slice Independence | Pass — sole slice; acceptance does not require a later slice |
| 3 | Slice Completeness | Pass — kit skills/commands/docs layers sufficient for Primary (no product metadata/BSL/Form layer missing); apply SSOT layer present in S1.2 |
| 4 | Slice Dependency Graph | Pass |
| 5 | Slice Gate Integrity | Pass — exactly one `S1.accept` + one `<!-- slice-gate -->` |
| 5b | Acceptance Checklist Coverage | Pass — `**Primary acceptance:**` present; mandatory `**Primary (обязательно):**` present; no foreign-slice Scenario; no uncovered Scenario (coverage via `S1.<M>` counts) |
| 6 | Rework Risk | Pass — no duplicate Primary across slices; no undeclared reliance on unaccepted predecessor; repair did not introduce foundation/consumer split |
| 8 | Slice Verticality | Pass — mandatory Primary is observable kit protocol (invoke `/opsx:explain` on artifact with `## Explain scope` → B-explain Охват/Варианты + Контекст → confirm before map), not programmatic-only API/diff accept |
| 8b | Self-Achievable Acceptance | Pass — Primary reachable via S1.1–S1.9 alone (handoff section + prefill + propose paths) |
| 9 | Foundation slice with gate | N/A — single slice |
| 10 | Acceptance Simplicity | Pass — one mandatory black-box journey; three optional bullets |
| 11 | User Task Contract | Pass — no DENY runtime-spike phrasing in S1.1–S1.9; S1.9 ALLOW-agent («Верифицировать по коду kit»); accept metadata «без обязательной ИБ продукта» is boundary accept, not mid-slice user spike; no «после verify/стенда» chains |

## Task Readability

| Task | Pattern check | Notes |
|---|---|---|
| S1.1 | Pass | Verb + file (`review/SKILL.md`) + outcome (Explain scope + self-check) |
| S1.2 | Pass | Verb + apply skill + SSOT code-map / handoff rule + (D1) |
| S1.3 | Pass | Verb + review/release-review slot + D2+D2a constraints |
| S1.4 | Pass | Verb + opsx-output-style / T-HANDOFF + priority vs verify/extend |
| S1.5 | Pass | Verb + command/guide files + when-to-call outcome |
| S1.6 | Pass | Verb + explain skill + prefill / map-frame outcome |
| S1.7 | Pass | Verb + entry-brief + HALT/fixture outcome |
| S1.8 | Pass | Verb + brief-card / opsx-explain examples |
| S1.9 | Pass | Agent static verify («по коду kit») + grep targets; not opaque D-only title |
| S1.accept | Pass (accept exception) | Business result in title; Primary mandatory bullet present |

No `task-opaque-title` / `task-too-short` / `accept-checklist-empty` emitted.

## Alerts

None at CRITICAL or WARNING.

### SUGGESTION — optional accept Scenario names vs literal spec titles

- **affected:** S1.accept optional bullets  
- **alert type:** `accept-scenario-name-alignment` (informational; not a 5b coverage miss)  
- **severity:** SUGGESTION  
- **evidence:** Spec titles are `Review offers explain`, `Apply offers explain`, `Trivial review skips default propose`. Accept uses `Scenario «Review/Apply offer explain»` and `Scenario «Trivial skip»`. Coverage remains OK via S1.3 / S1.4 / S1.3. Literal match only for «Explore still suggests explain».  
- **recommendation:** Rename optional bullets to literal Scenario titles (split Review/Apply into two lines) or drop paraphrased optionals and rely on S1.3–S1.4 + Primary.

### Remediation (auto-repair)

- alert: `accept-scenario-name-alignment` (SUGGESTION only; optional polish)  
- target: `tasks.md` slice S1 / `S1.accept`  
- action: Replace optional bullets with literal names, e.g. `Scenario «Review offers explain» (опционально): …`, `Scenario «Apply offers explain» (опционально): …`, `Scenario «Trivial review skips default propose» (опционально): …` — or remove the three paraphrased optionals (coverage already via S1.3–S1.4 / S1.9).

## Recommendations

### Automatic / low-risk polish

- Align optional accept Scenario «ёлочки» with literal `#### Scenario:` titles (see remediation above). Non-blocking for apply.

### Decision required

- None. Single-slice plan remains coherent after D1/D2a/D4/D5 repair; no merge/split needed.

## Summary for verify Layer 2

Slice Coherence: **OK**. Repair-from-verify tightened apply SSOT and propose/HALT/prefill decisions without breaking gate integrity, scenario coverage, verticality, self-achievable Primary, or User Task Contract. Only residual SUGGESTION is cosmetic Scenario-name alignment in optional accept bullets.
