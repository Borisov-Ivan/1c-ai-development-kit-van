---
verify_mode: pre-apply
change: skip-form-mode-module-only
date: 2026-09-01
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
  repair_attempt: 1
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-09-01T02:34:54Z"
    design.md: "2026-09-01T03:08:37Z"
    tasks.md: "2026-09-01T03:09:09Z"
    specs/split-form-layout-modes/spec.md: "2026-09-01T03:08:57Z"
  last_challenge_at: "2026-09-01T03:08:37Z"
---

## Резюме для разработчика

skip-form-mode-module-only — можно запускать apply. Если в ЗНИ правят только модуль формы, выбора из трёх не будет — в карточке сразу поставка программно.

**Следующий шаг:** `/opsx:apply skip-form-mode-module-only`

План правит правило вопроса поставки формы и цикл создания ЗНИ: «обработчики» и «видимость» без «в модуле» по-прежнему дают вопрос (это может быть Конфигуратор). При двух формах в одном ходе можно записать программно для модуля и задать один вопрос про разметку.

Подправил в постановке: сузил признаки «только модуль» и зафиксировал смесь форм в одном ходе.

## Что меняется в постановке

**Расширение / конфигурация:** прикладной `src/` не затрагивается.

**Точки изменения:**

- `.cursor/rules/forms-mxl-mode-gate.mdc` — классификатор «только модуль / разметка / неясно» перед каноном вопроса; рекомендуемая поясняющая строка.
- `.cursor/skills/openspec-new-change/SKILL.md` шаг 5.d.1 — прогон классификатора до вопроса; смесь форм в одном ходе.
- `.cursor/docs/faq-kit.md`, `.cursor/docs/quick-start.md` — справка: вопрос задаётся не всегда.

**Что НЕ меняется:** запрет молчаливого «автоматически»; макет в new не спрашивается; дыра режима (пусто/`n/a` при задаче на форму) — блокер; default пустого ответа на **заданный** вопрос — вручную; три русских варианта вопроса, когда вопрос задаётся (ADR-0001).

**Связанные ADR / KB / архив:** ADR-0001; архив `2026-08-18-sequential-ui-mode-questions` (осознанное сужение MUST-вопроса, таблица последствий в design).

### Подправил в постановке

- Сузил достаточные признаки «только модуль»: без «в модуле» обработчики и видимость не дают skip.
- Зафиксировал смесь форм: запись программно + один вопрос из трёх в одном ходе.
- Поясняющая строка рекомендуется, не обязательна; критерий skip — карточка ЗНИ.

### К сведению

- Таксономия базы знаний в kit отсутствует — на запуск apply не влияет.
- Маркеры автора в BSL для этой ЗНИ не применяются.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы, один `<!-- slice-gate -->`, fences закрыты. `form_mode: n/a` корректно (kit).
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-09-01-2.md` Verdict OK, 12/12 Scenario, CRITICAL/WARNING нет. User Task Contract 2.1a: none. Precedent: MODIFIED vs archive ADDED, Blast Radius заполнен → `precedent-documented` INFO. Code-truth: kit markdown, `project.md` отсутствует; целевые `.cursor/**` существуют.
- **Layer 2.5 (Loop Detection):** PASS. Нет `awaiting-acceptance`; AcceptLoop=0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт ADDED Requirement; Scenario у обоих Requirement; все Scenario в ## Slices; срез не пустой; implementation-leak нет; `comment_suffix` пуст + `marker_style: minimal`.
- **Layer 4 (Independent Challenge):** APPROVE. Отчёт: `reports/design-challenge-2026-09-01-2.md`. Предыдущий CHALLENGE (`design-challenge-2026-09-01.md`) классифицирован как `implementation_invariant` → Repair Loop attempt 1; gaps закрыты; новых verified gaps нет.
- **Layer 5 (Implementation Readiness):** PASS. Отчёт: `reports/architecture-task-readiness-2026-09-01-2.md`. Вердикт ГОТОВО. Layer 5.1: маркеров ручной конфигурации этой ЗНИ нет.

### Авто-исправлено (Layer 1)

mechanical-замечаний не обнаружено

### Repair Loop

- attempt: 1
- class: implementation_invariant
- files: design.md, specs/split-form-layout-modes/spec.md, tasks.md, debug.md

## Источники

- `reports/quality-control-2026-09-01-2.md`
- `reports/design-challenge-2026-09-01.md` (первый прогон, CHALLENGE → repair)
- `reports/design-challenge-2026-09-01-2.md` (повтор, APPROVE)
- `reports/architecture-task-readiness-2026-09-01-2.md`
- алерты: `precedent-documented` (INFO)
