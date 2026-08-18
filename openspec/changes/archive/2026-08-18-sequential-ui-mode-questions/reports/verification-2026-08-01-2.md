---
verify_mode: pre-apply
change: sequential-ui-mode-questions
date: 2026-08-01
verdict: GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: APPROVE
  layer_5_implementation_readiness: PASS
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions:
    - id: acceptance_loop_s2_path
      summary: "Не замораживать dual-channel постановку S2 — сузить ЗНИ до форм (Mode Gate только form_mode per-form); макеты вне Mode Gate"
      closed_at: "2026-08-01"
      source: verify-user-answer
    - id: forms_only_no_layout_mode_gate
      summary: "Макеты вне Mode Gate new; default manual; programmatic только с явного разрешения на apply; поле layout_mode как выбор не вводим"
      closed_at: "2026-08-01"
      source: verify-user-answer
    - id: per_form_mode_on_design
      summary: "Вопрос режима формы на design по каждой форме в scope (не один режим на всю ЗНИ); END TURN между вопросами"
      closed_at: "2026-08-01"
      source: verify-user-answer
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-07-31T23:08:56Z"
    design.md: "2026-07-31T23:17:46Z"
    tasks.md: "2026-07-31T23:18:04Z"
    specs/sequential-gate-questions/spec.md: "2026-07-31T23:09:20Z"
    specs/split-form-layout-modes/spec.md: "2026-07-31T23:17:39Z"
  last_challenge_at: "2026-07-31T23:17:46Z"
---

## Резюме для разработчика

sequential-ui-mode-questions — можно запускать apply.

План после сужения: один вопрос выбора за ход в `/opsx:new` и режим поставки **по каждой форме** (`form_mode` / map `forms:` на design). Макеты вне Mode Gate — вручную по умолчанию, программный путь только с записанного разрешения на apply. Правки — протоколы kit в `.cursor/**`, не прикладной BSL.

Подправил в постановке: дописал канон записи режимов форм, алгоритм списка форм на design, правило legacy при нескольких формах и норму разрешения на non-manual макет.

**Следующий шаг:** `/opsx:apply sequential-ui-mode-questions`

## Что меняется в постановке

**Расширение / конфигурация:** метапроект kit — `.cursor/**` (не `src/` прикладной конфигурации).

**Точки изменения:**

- `.cursor/skills/openspec-new-change/SKILL.md` — END TURN / HALT одного вопроса; Mode Gate форм на design (цикл per-form).
- `.cursor/docs/templates/brief-card.md` — Metadata без соседних вопросов.
- `.cursor/rules/forms-mxl-mode-gate.mdc` — Mode только формы; `## Forms mode`; политика макета Decision 9.
- `.cursor/skills/openspec-apply-change/SKILL.md`, `openspec-verify-change/SKILL.md` — readers per-form + legacy fallback + permission for Template.
- Skills `1c-forms` / `1c-mxl`, handoff explore, `kit-template-workflow.md`, `1c-xml-write-guard.mdc` — термины и политика.

**Что НЕ меняется:** прикладной BSL, Form.xml, Template.xml consumer-проектов; обязательный `[form:…]` (Follow-up F2).

**Связанные ADR / KB / архив:** нет (capabilities ADDED; архивных MODIFIED/REMOVED нет).

### Подправил в постановке

После независимого аудита дописаны инварианты реализации (без смены оси forms-only): канон YAML `forms:`, enumeration scope, legacy×N, форма разрешения apply, выравнивание S1 Primary с design-stage Mode.

### К сведению

- Имя capability `split-form-layout-modes` историческое; содержание — forms-only / per-form.
- Layer 2.5: PatchRounds S2 ≥ порога, но петля уже разобрана (`architecture-loop-redesign-2026-08-01.md` + решение пользователя → forms-only).
- Metadata: `marker_style: minimal`, пустой `comment_suffix` — допустимо для kit.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS — checkboxes, slice-gate, Forms mode (`form_mode: n/a`) OK; autofix не применялся.
- **Layer 2 (Internal Coherence):** PASS — QC `OK` (`quality-control-2026-08-01-3.md`, 11/11 scenarios; 8b/11 Pass); User Task Contract none; Code-Truth N/A (kit docs); Precedent 2.4 — только ADDED, архивов/KB/ADR нет.
- **Layer 2.5 (Loop Detection):** PASS — S2 PatchRounds≥3, но закрытие: redesign + user path A (forms-only); новый redesign не запускался.
- **Layer 3 (Problem-Solution Trace):** PASS — Why↔Req↔Scenario↔Slices↔Tasks; scenario-implementation-leak не найден; process-only-marker-suffix N/A.
- **Layer 4 (Independent Challenge):** APPROVE — `design-challenge-2026-08-01-3.md` (после repair attempt 1 по gaps из `design-challenge-2026-08-01-2.md`).
- **Layer 5 (Implementation Readiness):** PASS — `architecture-task-readiness-2026-08-01-3.md` вердикт ГОТОВО; manual-config markers none; User Task Contract OK.

### Авто-исправлено (Layer 1)

не применялось

### Repair Loop

- attempt 1: repair-from-verify по `implementation_invariant` gaps challenge-2 → extend 2026-08-01 (repair-from-verify); re-verify → GO.
- attempt 2: не потребовался.

## Источники

- `reports/quality-control-2026-08-01-3.md`
- `reports/design-challenge-2026-08-01-2.md` (pre-repair CHALLENGE)
- `reports/design-challenge-2026-08-01-3.md` (post-repair APPROVE)
- `reports/architecture-task-readiness-2026-08-01-3.md`
- `reports/architecture-loop-redesign-2026-08-01.md`
- `reports/architecture-extend-coherence-2026-08-01-2.md`
