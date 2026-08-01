# Quality Control — Slice Coherence (re-verify after Repair Loop 1)

**Change:** `chat-surface-clarity`  
**Date:** 2026-08-01  
**Mode:** slice (`# Срез S1`…`S3`)  
**Artifacts:** `tasks.md` (перечитан после repair), `design.md` (перечитан), `proposal.md`, `specs/chat-surface-clarity/spec.md`  
**Context:** re-verify; новый Scenario «Apply pause label is product language» должен быть покрыт S2  
**Prior QC:** `reports/quality-control-2026-08-01.md` (WARNING)

### Verdict

`OK`

### Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1 Канон Mode Gate и зеркала | Mode Gate / эталоны / faq / без преамбулы | S1.1–S1.5 (5) | S1.accept (Primary + 1 optional; 4/4) | — | yes (`<!-- slice-gate -->`) |
| S2 Copy-paste команд P0 | AskQuestion / pause / review / status-handoff | S2.1–S2.5 (5) | S2.accept (Primary + 2 optional; 4/4) | S1 | yes |
| S3 SSOT-конфликты и приёмка | Entry brief KB / Agent names + final grep | S3.1–S3.4 (4) | S3.accept (Primary + 1 optional; 2/2) | S2 | yes |

### Scenario Coverage

| Scenario | Covered by | Status |
|---|---|---|
| Mode Gate question is product language | S1 Primary; S1.1 | OK |
| Good examples do not teach jargon | S1 Primary; S1.2 | OK |
| FAQ matches form-only Mode Gate | S1 Primary; S1.3 | OK |
| Mode question has no process preamble | S1.5; S1.accept optional | OK |
| Slice acceptance prompt without gate names | S2 Primary; S2.2 | OK |
| Apply pause label is product language | S2 Primary («Пошаговая пауза»); S2.2; S2.accept optional | OK |
| Review fix prompt without agent slugs | S2 Primary (`onec-code-`); S2.4 | OK |
| Status and handoff separate chat from file | S2 Primary; S2.1–S2.3, S2.5; S2.accept optional | OK |
| Entry brief excludes KB list | S3 Primary; S3.1 | OK |
| Agent names banned uniformly | S3 Primary; S3.1; S3.accept optional | OK |

Все 10 `#### Scenario:` из `specs/chat-surface-clarity/spec.md` покрыты Primary, optional accept или задачей `S<N>.<M>`. Новый Scenario «Apply pause label is product language» привязан к S2 (metadata `**Связь со spec:**`, задача S2.2, Primary + optional в `S2.accept`) и согласован с `design.md` § Матрица приёмки.

### Dependency Graph

```mermaid
flowchart LR
  S1[S1 Mode Gate canon] --> S2[S2 Command copy-paste]
  S2 --> S3[S3 SSOT + final grep]
```

- Циклов нет.
- Зависимости только назад; объявлены в metadata (`S2→S1`, `S3→S2`); целевые срезы существуют.
- Forward acceptance dependency / дубль Primary между срезами — не обнаружены.
- Каждый срез имеет самостоятельный Primary (канон Mode Gate → шаблоны команд включая pause label → SSOT+grep), согласован с `design.md` § Slices.

### Checklist evaluation

| # | Criterion | Result |
|---|---|---|
| 1 | Scenario Coverage | OK (10/10, включая Apply pause → S2) |
| 2 | Slice Independence | OK |
| 3 | Slice Completeness | OK (kit meta-change; слои 1С не требуются; файлы среза достаточны для Primary) |
| 4 | Slice Dependency Graph | OK |
| 5 | Slice Gate Integrity | OK (ровно один `S<N>.accept` + `<!-- slice-gate -->` на срез; критерии gate — одно предложение) |
| 5b | Acceptance Checklist Coverage | OK (`**Primary acceptance:**` + mandatory Primary sub-bullet во всех срезах; gaps по Scenario нет) |
| 6 | Rework Risk | OK после repair — см. notes |
| 8 | Slice Verticality | OK (Primary — наблюдаемое отсутствие жаргона в chat-facing текстах kit; не programmatic-only API-ревью) |
| 8b | Self-Achievable Acceptance | OK (Primary каждого среза достижим задачами того же среза) |
| 9 | Foundation slice with gate | OK (S1/S2 не foundation-only: у каждого свой user-facing outcome) |
| 10 | Acceptance Simplicity | OK (один mandatory Primary на срез; прочие Scenario — optional или `S<N>.<M>`) |
| 11 | User Task Contract | OK (DENY-паттернов в `S<N>.<M>` нет; pre-check evidence: none; «вручную» в S1.1 — язык канона Mode Gate, не runtime-spike ИБ) |
| — | Task Readability | OK после repair — см. notes |

Pre-checks from prompt (manual config / mechanical / User Task Contract): согласованы с оценкой; CRITICAL по ним нет. Repository state kit meta-change — учтён (приёмка через чтение/grep chat-facing, не ИБ).

### Repair Loop 1 — закрытие алертов prior QC

| Prior alert | Severity | Status after repair | Evidence |
|---|---|---|---|
| `rework-risk` (S3.4 vs файлы S1/S2) | WARNING | Closed | S3.4: «точечный closure без переоткрытия оси решений и без повторного slice-gate S1/S2»; `design.md` Behavior Contract: финальный grep — кумулятивная приёмка change |
| `task-opaque-title` (S3.2) | WARNING | Closed | S3.2 перечисляет пути `openspec-extend-change` / `openspec-explore` / `openspec-verify-change` + формат decision-block A/B / brief-card B2 |
| `slice-gate-criterion-thin` | SUGGESTION | Closed | Markers S1/S2/S3 содержат одно предложение критерия из Primary |

### Alerts

Нет CRITICAL / WARNING / SUGGESTION по каноническим критериям QC.

### Notes (non-blocking)

- Маркеры `<!-- slice-gate -->` стоят сразу после metadata (до списка задач), а не после `S<N>.accept`. Presence/integrity критерия 5 соблюдены; позиция — стилистическое отклонение от примера в `vertical-slices.mdc`, не алерт.
- Transient исполнимость grep/приёмки на текущем диффе — out of scope QC.

### Remediation (auto-repair)

Не требуется.

**Decision-required:** нет (`slice-accept-not-self-achievable` / merge срезов не требуется).

### Recommendations

**Automatic fix:** нет.

**Decision required:** нет. Три среза с независимыми outcomes оправданы; Scenario «Apply pause label is product language» корректно размещён в S2.
