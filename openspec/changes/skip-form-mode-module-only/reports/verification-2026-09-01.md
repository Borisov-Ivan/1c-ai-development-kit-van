---
verify_mode: pre-apply
change: skip-form-mode-module-only
date: 2026-09-01
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: CHALLENGE
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
    design.md: "2026-09-01T02:41:42Z"
    tasks.md: "2026-09-01T02:46:32Z"
    specs/split-form-layout-modes/spec.md: "2026-09-01T02:36:29Z"
  last_challenge_at: "2026-09-01T02:41:42Z"
classifier:
  layer_4: implementation_invariant
  action: repair-from-verify
---

## Резюме для разработчика

skip-form-mode-module-only — постановка дописывается: независимая проверка оставила выбранный путь, но потребовала сузить признаки «только модуль» и согласовать смесь форм.

**Следующий шаг:** внутренний допись постановки, затем повторная проверка (чат после цикла).

План по-прежнему: если в ЗНИ правят только модуль формы, не спрашивать «вручную / автоматически / программно» и сразу писать поставку программно. Независимая проверка подтвердила, что это закрывает холостой выбор и не ломает три русских варианта вопроса, когда вопрос всё же задаётся.

## Что доработать в постановке

### Рекомендации

- **Признаки «только модуль»:** не считать достаточными сами «обработчики» и «видимость элементов» — без «в модуле» это может быть правка свойств в Конфигураторе; тогда нужен вопрос, а не молчаливая запись программно.
- **Смесь форм:** в одном ходе запись программно для «только модуль» плюс ровно один вопрос из трёх по другой форме (поясняющая строка не второй выбор).
- **Поясняющая строка:** рекомендуется, не обязательна; критерий skip — запись в карточке.

Эти пункты классифицированы как инварианты реализации (не смена оси). Repair Loop применяет их без вопроса человеку.

## Что меняется в постановке

**Расширение / конфигурация:** прикладной `src/` не затрагивается. Точки — правила kit.

**Точки изменения:**

- `.cursor/rules/forms-mxl-mode-gate.mdc` — классификатор перед каноном вопроса поставки формы.
- `.cursor/skills/openspec-new-change/SKILL.md` шаг 5.d.1 — прогон классификатора до вопроса.
- `.cursor/docs/faq-kit.md`, `.cursor/docs/quick-start.md` — справка: вопрос задаётся не всегда.

**Что НЕ меняется:** запрет молчаливого «автоматически»; макет в new не спрашивается; дыра режима (пусто/`n/a` при задаче на форму) остаётся блокером; default пустого ответа на **заданный** вопрос — вручную.

**Связанные ADR / KB / архив:** ADR-0001 (три русских варианта, когда вопрос задаётся); архив `2026-08-18-sequential-ui-mode-questions` — осознанное сужение MUST-вопроса (таблица последствий в design).

### К сведению

- Таксономия базы знаний в kit отсутствует — на вердикт не влияет.
- Маркеры автора в BSL для этой ЗНИ не применяются (`developer: n/a`).

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы, один `<!-- slice-gate -->`, fences закрыты. `form_mode: n/a` корректно (kit).
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-09-01.md` Verdict OK, 12/12 Scenario. User Task Contract 2.1a: none. Precedent: MODIFIED vs archive ADDED, Blast Radius заполнен → `precedent-documented` INFO. Code-truth: kit markdown, `project.md` отсутствует; целевые файлы `.cursor/**` существуют (pre-apply phantom N/A).
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` на момент первого прогона отсутствовал; AcceptLoop=0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт ADDED Requirement; оба Requirement имеют Scenario; все Scenario в ## Slices; срез не пустой; implementation-leak в THEN нет; `comment_suffix` пуст + `marker_style: minimal`.
- **Layer 4 (Independent Challenge):** CHALLENGE. Отчёт: `reports/design-challenge-2026-09-01.md`. Post-challenge classifier: все три Gaps = `implementation_invariant` (ось A не меняется; Architectural alternatives: нет равноправной развилки). Repair Loop, не 3a-decision.
- **Layer 5 (Implementation Readiness):** PASS. Отчёт: `reports/architecture-task-readiness-2026-09-01.md`. Вердикт ГОТОВО. Layer 5.1: маркеров ручной конфигурации этой ЗНИ нет.

### Авто-исправлено (Layer 1)

mechanical-замечаний не обнаружено

### Развёрнутые карточки развилок

Нет (classifier → repair).

## Источники

- `reports/quality-control-2026-09-01.md`
- `reports/design-challenge-2026-09-01.md`
- `reports/architecture-task-readiness-2026-09-01.md`
- алерты: `precedent-documented` (INFO)
