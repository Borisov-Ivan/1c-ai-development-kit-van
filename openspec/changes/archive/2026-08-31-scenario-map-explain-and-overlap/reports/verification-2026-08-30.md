---
verify_mode: pre-apply
change: scenario-map-explain-and-overlap
date: 2026-08-30
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
    proposal.md: "2026-08-30T13:59:21+09:00"
    design.md: "2026-08-30T13:57:49+09:00"
    tasks.md: "2026-08-30T13:59:04+09:00"
    specs/scenario-map-canvas/spec.md: "2026-08-30T13:58:18+09:00"
  last_challenge_at: "2026-08-30T13:57:49+09:00"
---

## Резюме для разработчика

scenario-map-explain-and-overlap — можно запускать apply. Шаблон панели разведёт подписи и карточки; с полотна читается, что происходит и почему такой исход.

План правит шаблон панели (рамки текста, перенос длинного ранга в виде «Связи», зазор только наружу) и чек-листы скилла. Приёмка: скрыть шапку и своими словами объяснить ход; карта с длинным рангом — в том же взгляде.

В постановке уточнил: ход собирается с подписей, аннотаций и текста на коробках; сжимать зазор под ширину панели нельзя.

**Следующий шаг:** `/opsx:apply scenario-map-explain-and-overlap`

Ширина текста считается по символам — окончательно смотреть живую панель. Если подписи некуда поставить, схема уходит в таблицу колонок — так задумано.

## Что меняется в постановке

**Расширение / конфигурация:** прикладная конфигурация 1С не меняется. Kit: шаблон панели и скилл карты сценария.

**Точки изменения:**

- шаблон панели — вписать имена и карточки в рамки; развести подписи предикатом пересечения прямоугольников (уже есть в шаблоне); перенос ранга в виде «Связи» вниз по колонке; габариты включают текст; зазор не сжимать
- скилл карты — планка читаемости (подпись на коробке запрещена; снятая подпись = провал бюджета) и смысла до записи (ход механизма, не каталог влияний); запрет графа конвейера kit как ответа заказчику
- эталоны «хорошо / плохо» — плохой каталог влияний, хороший ход с полотна
- дельта требований `scenario-map-canvas` — текст не перекрыт; ход с полотна при скрытой шапке; перенос по направлению

**Что НЕ меняется:** регистрация панели родителем; картограф не пишет файл; ровно два средства вида; координаты считает панель; бюджет «не масштабировать полотно целиком»; модель сборщика как движок.

**Связанные ADR / архив:** ADR-0008, ADR-0009 (Load-Bearing); архив `2026-08-30-scenario-map-readability-meaning` (extends).

### К сведению

- Оценка ширины кириллицы по числу символов неточная — живой осмотр остаётся приёмкой.
- Сверка двенадцати унаследованных сценариев — по тексту скилла и шаблона, без живого осмотра в этой задаче.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы, `<!-- slice-gate -->`, `form_mode: n/a`, без `<!-- phase-gate -->`.
- **Layer 2 (Internal Coherence):** PASS; QC: `reports/quality-control-2026-08-30-2.md`. 18 Scenario покрыты. User Task Contract: none. Code-truth: `boxesOverlap` найден в шаблоне; pre-apply phantom не ставился. Precedent: MODIFIED «Causal map has layers or branches» vs archive ADDED — extends, Blast Radius заполнен → `precedent-documented` (INFO).
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` без Slice Gate Decisions; AcceptLoop/PatchRounds = 0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт ADDED kit-pipeline + MODIFIED Causal map. У каждого Requirement есть Scenario. Implementation-leak в THEN: нет. `comment_suffix` пуст — `process-only-marker-suffix` не ставится.
- **Layer 4 (Independent Challenge):** первый прогон CHALLENGE с 8× `implementation_invariant` → Repair Loop attempt 1 (design/spec/tasks/proposal). Повтор: APPROVE (`reports/design-challenge-2026-08-30-2.md`). Ось Chosen B не менялась.
- **Layer 5 (Implementation Readiness):** PASS; отчёт: `reports/architecture-task-readiness-2026-08-30-2.md`. Вердикт ГОТОВО, GAP нет. Manual-config маркеров нет.

### Авто-исправлено (Layer 1)

mechanical-замечаний не обнаружено

### Repair Loop

- attempt: 1
- class: implementation_invariant (из classifier Layer 4)
- артефакты: proposal.md, design.md, specs/scenario-map-canvas/spec.md, tasks.md, debug.md
- disposition: 8 gaps accepted; decision_round не менялся

### Развёрнутые карточки развилок

нет

## Источники

- `openspec/changes/scenario-map-explain-and-overlap/reports/quality-control-2026-08-30-2.md`
- `openspec/changes/scenario-map-explain-and-overlap/reports/design-challenge-2026-08-30.md` (CHALLENGE, repair input)
- `openspec/changes/scenario-map-explain-and-overlap/reports/design-challenge-2026-08-30-2.md` (APPROVE)
- `openspec/changes/scenario-map-explain-and-overlap/reports/architecture-task-readiness-2026-08-30-2.md`
- алерты: none blocking; INFO `precedent-documented`
