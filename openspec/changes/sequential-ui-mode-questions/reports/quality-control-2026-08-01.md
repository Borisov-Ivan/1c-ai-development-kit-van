# Quality Control — sequential-ui-mode-questions

**Date:** 2026-08-01  
**Mode:** slice  
**Context:** verify Layer 2 — Slice Coherence (criteria 1–6, 8, 8b, 9–11); specs: 3 + 9 Scenarios (Layout bsl-only / Legacy bsl-only layout included)  
**Artifacts:** `tasks.md`, `design.md`, `proposal.md`, `specs/sequential-gate-questions/spec.md`, `specs/split-form-layout-modes/spec.md`  
**Manual config checklist (verify 7.5):** маркеров ручной конфигурации в tasks.md не найдено  
**Mechanical check issues (7A–7E):** none (checkboxes OK, slice-gate present, Forms & layouts mode n/a / artifact_mode не требуется)  
**User Task Contract pre-check evidence (2.1a):** none  
**Repository state:** метапроект kit — правки только `.cursor/**`; `openspec/project.md` отсутствует; прикладных Form.xml/Template.xml/BSL в scope нет

## Verdict

`OK`

## Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1 Один вопрос за ход | One selection question per orchestrator turn (3 scenarios) | S1.1–S1.3 | S1.accept (Primary + 1 optional; 3/3 via Primary/optional/tasks) | нет | yes `<!-- slice-gate -->` |
| S2 Раздельные режимы Form/Template | Separate form and layout delivery modes (9 scenarios) | S2.1–S2.5 | S2.accept (Primary + 6 optional; 9/9 via Primary/optional/tasks) | S1 | yes `<!-- slice-gate -->` |

Follow-up F1–F2 вне срезов — не входят в gate.  
**Режим apply:** mechanical на обоих срезах (migration/docs kit).

## Scenario Coverage

| Scenario | Covered by | Status |
|---|---|---|
| Metadata question without Mode Gate in same message | S1 Primary; S1.1, S1.2 | OK |
| Second gate only after answer | S1 Primary; S1.1 | OK |
| Dual selection questions blocked | S1.accept optional (literal); S1.3 | OK |
| Form-only change asks only about form | S2.2; S2.accept optional (paraphrase «Form-only / Layout-only») | OK |
| Layout-only change asks only about layout | S2.2; S2.accept optional (paraphrase «Form-only / Layout-only») | OK |
| Mixed modes for form and layout | S2 Primary; S2.1–S2.3 | OK |
| Layout bsl-only rejected | S2.accept optional (literal); S2.1, S2.3, S2.4 | OK |
| Legacy single artifact_mode still readable | S2 Primary; S2.1, S2.3, S2.4 | OK |
| Legacy bsl-only does not force layout bsl-only | S2.accept optional (literal) + Primary; S2.1–S2.4 | OK |
| Pair fields override legacy artifact_mode | S2.accept optional (literal); S2.1, S2.3, S2.4 | OK |
| Kit evolution without UI modes | S2.2; S2.accept optional (paraphrase «Kit evolution») | OK |
| Empty mode blocks apply for in-scope artifact | S2.accept optional (literal); S2.1, S2.3, S2.4 | OK |

Всего `#### Scenario:` в specs: **12** (3 + 9). Пропусков нет. Agent-path «верифицировать по коду» не требуется: покрытие через Primary / optional accept / задачи задач skills/rules.

## Dependency Graph

```mermaid
flowchart LR
  S1[S1 Один вопрос за ход] --> S2[S2 Раздельные режимы Form/Template]
```

- Cycles: none  
- Forward acceptance dependency: none (S2 ← S1 только назад; Primary S1 не требует слоя S2)  
- Undeclared dependencies: none (`**Зависимости:** S1` совпадает с design `## Slices`)

## Checklist evaluation

| # | Criterion | Result |
|---|---|---|
| 1 | Scenario Coverage | Pass — все 12 `#### Scenario:` покрыты Primary / optional accept / `S<N>.<M>` |
| 2 | Slice Independence | Pass — S1 принимаем без S2; S2 объявляет зависимость от S1 |
| 3 | Slice Completeness | Pass — kit-meta: слои = skills/rules/templates; нужные файлы в задачах S1/S2 |
| 4 | Slice Dependency Graph | Pass |
| 5 | Slice Gate Integrity | Pass — ровно один `S<N>.accept` + `<!-- slice-gate -->` на срез |
| 5b | Acceptance Checklist Coverage | Pass — `**Primary acceptance:**` + mandatory Primary sub-bullet в обоих срезах; новые Scenario (Layout bsl-only, Legacy bsl-only≠layout) в optional/Primary |
| 6 | Rework Risk | Low — outcomes различны (последовательность вопросов vs split modes); зависимость явная |
| 8 | Slice Verticality | Pass — оба Primary: наблюдаемый протокол `/opsx:new` / proposal+apply (black-box для автора ЗНИ), не programmatic-only |
| 8b | Self-Achievable Acceptance | Pass — Primary S1 достижим S1.1–S1.3; Primary S2 достижим S2.1–S2.5 без слоя более позднего среза; дубля Primary нет |
| 9 | Foundation slice with gate | Pass — S1 Primary не programmatic-only; не foundation+consumer double-gate |
| 10 | Acceptance Simplicity | Pass — по одному mandatory Primary sub-bullet на срез |
| 11 | User Task Contract | Pass — в `S<N>.<M>` нет runtime-spike / ИБ / консоль / отладчик; DENY-подстрок нет. «Учебный прогон» только в `S<N>.accept` / metadata приёмки |

## Task readability

| Task | Assessment |
|---|---|
| S1.1, S1.2 | Verb + file + change + (Decision) — OK |
| S1.3 | Verb + target (self-check new) + HALT rule — OK |
| S2.1 | Verb + file + split modes + layout без bsl-only + pair/legacy + empty/`n/a` + (Decision) — OK |
| S2.2 | Verb + file + sequence/resume/extend/legacy Decision 7 — OK |
| S2.3–S2.4 | Verb + file + pair-over-legacy + layout bsl-only STOP + empty/`n/a` — OK |
| S2.5 | Verb + file list + term sync — OK |
| S1.accept / S2.accept | Business result in title; Primary mandatory present — OK |
| Optional Scenario names | Часть имён сокращена («Form-only / Layout-only», «Kit evolution») — покрытие сохранено через tasks; см. SUGGESTION |

Алертов `task-opaque-title` / `task-too-short` / `accept-checklist-empty` / `primary-acceptance-missing` нет.

## Alerts

### SUGGESTION — `accept-scenario-name-paraphrase` (S2.accept)

- **Affected:** S2.accept optional bullets «Form-only / Layout-only», «Kit evolution»  
- **Severity:** SUGGESTION  
- **Evidence:** `#### Scenario:` в `specs/split-form-layout-modes/spec.md` названы буквально `Form-only change asks only about form`, `Layout-only change asks only about layout`, `Kit evolution without UI modes`; в accept — сокращения. Coverage через S2.2 + optional есть → не `accept-bullets-missing-scenario`.  
- **Recommendation:** выровнять имена в optional bullets (и при желании разнести Form-only / Layout-only на два sub-bullet) буквально со spec — для читаемости handoff.

Иных CRITICAL / WARNING нет.

## Recommendations

### Automatic fix (optional)

- Выровнять имена Scenario в optional bullets S2.accept под литералы `#### Scenario:` из `specs/split-form-layout-modes/spec.md` (см. SUGGESTION выше).

### Decision required

- Нет.

## Notes

- Два среза при Standard-размере оправданы независимыми outcomes (design `## Slices`): S1 — инвариант одного вопроса за ход; S2 — раздельные `form_mode`/`layout_mode` + legacy/empty/bsl-only layout.  
- Out of scope (не оценивалось): исполнимость учебного прогона «прямо сейчас», наличие тестовых данных/ИБ.
