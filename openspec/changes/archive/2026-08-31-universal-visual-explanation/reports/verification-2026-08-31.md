---
verify_mode: pre-apply
change: universal-visual-explanation
date: 2026-08-31
verdict: GO
layer_status:
  layer_1_hygiene: AUTOFIXED
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
    - id: verify_review_direct_request_panel
      summary: "На /opsx:verify и /review автопанель и системный canvas запрещены; прямая просьба открывает панель, в чате одна строка эффекта."
      closed_at: "2026-08-30"
      source: verify-user-answer
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: incremental
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-08-30T10:39:46Z"
    design.md: "2026-08-30T21:14:44Z"
    tasks.md: "2026-08-30T21:14:48Z"
    specs/visual-explanation/spec.md: "2026-08-30T21:14:44Z"
    specs/scenario-map-canvas/spec.md: "2026-08-30T09:32:50Z"
    specs/always-apply-context-budget/spec.md: "2026-08-30T09:32:51Z"
    specs/delegation-safeguards/spec.md: "2026-08-30T09:32:51Z"
  last_challenge_at: "2026-08-30T21:14:44Z"
---

## Резюме для разработчика

universal-visual-explanation — можно запускать apply. Новый скилл визуального объяснения заменяет карту сценария: панель рядом с чатом по просьбе «покажи, как устроено», старый сборщик и граф снимаются.

**Следующий шаг:** `/opsx:apply universal-visual-explanation`

По просьбе открывается панель с вопросом, выводом и структурой ответа; на проверке постановки и ревью сами не открываем. Прикладной код 1С не меняется.

Подправил в постановке: в список снятия старой карты добавлены словари kit; при тесном полотне нельзя оставлять иерархию.

## Что меняется в постановке

**Расширение / конфигурация:** прикладной `src/` не затрагивается. Меняется kit: `.cursor/skills/`, `.cursor/rules/`, `.cursor/agents/`, `openspec/adrs/`, `openspec/glossary.md`, `openspec/knowledge/_taxonomy.yaml`.

**Точки изменения:**

- `.cursor/skills/visual-explanation/SKILL.md` — новый протокол просьбы и автопанели.
- `.cursor/skills/visual-explanation/fixtures/panel-shell.md` — тонкий рендер `Stack` / `Table` / `Text`.
- `.cursor/rules/gate-dispatcher.mdc` — указатель «покажи схему» на новый скилл.
- `.cursor/skills/scenario-map-canvas/**`, `.cursor/agents/onec-scenario-map-designer.md` — удаление.
- `openspec/adrs/ADR-0010-visual-explanation-panel.md` — несущая замена ADR-0008 и ADR-0009.
- `openspec/glossary.md` и `openspec/knowledge/_taxonomy.yaml` — словари kit без статьи старой карты.

**Что НЕ меняется:** регистрация файла панели родителем и успех кнопкой среды; запрет голого списка без вывода; файл панели не в git; «без схемы» до выхода сессии; «покажи схему компоновки» — ответ про 1С; соседняя ЗНИ `scenario-map-explain-and-overlap` не реализуется.

**Связанные ADR / KB / архив:** ADR-0008, ADR-0009 → ADR-0010; архивы `2026-08-28-scenario-map-canvas`, `2026-08-30-scenario-map-readability-meaning`, `2026-08-30-overview-map-offer`, `2026-08-30-scenario-map-show-scheme-phrase`. Фактов KB нет.

### Подправил в постановке

- Убрал лишний пустой абзац в рисках design.
- В список миграции и сверки добавил `openspec/glossary.md` и переименование поддомена таксономии.
- В пороге читаемости явно запретил иерархию при тесном полотне.

### К сведению

- Отмена capability `scenario-map-canvas` и несущих ADR-0008/0009 закрыта таблицей последствий для человека.
- Соседнюю открытую ЗНИ про наложение подписей план не сливает — только пометка в её журнале.
- На `/opsx:verify` и `/review` панель открывается только по прямой просьбе; в чате одна строка эффекта.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** AUTOFIXED. Нормализован лишний пустой абзац в `design.md` § Risks.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-31-2.md` — OK, 24/24 Scenario, 8b/11 чистые, S1.12 inside-slice. Code-Truth: нет 1С-символов в backticks, `openspec/project.md` отсутствует (kit). Precedent 2.4: ADDED→REMOVED/MODIFIED по `scenario-map-canvas`, `always-apply-context-budget`, `delegation-safeguards` + supersede Load-Bearing 0008/0009 закрыты `## Blast Radius` → INFO `precedent-documented`. Архивов 9 (≤10).
- **Layer 2.5 (Loop Detection):** PASS. `S1.accept` = `[ ]`; Slice Gate Decisions нет; PatchRounds = 2 (`## Extend —` 2026-08-30 и 2026-08-31) < `acceptance_loop_max` 3.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт ADDED `visual-explanation`; у каждого ADDED/MODIFIED Requirement есть Scenario; implementation-leak в THEN нет; `comment_suffix` пустой при `marker_style: minimal`.
- **Layer 4 (Independent Challenge):** APPROVE. Сырой отчёт `reports/design-challenge-2026-08-31.md` был CHALLENGE с gaps G1–G3 класса `implementation_invariant`. Post-challenge classifier → Repair Loop. Gaps закрыты: glossary в S1.7/S1.11/Migration; S1.12 таксономия; порог «не поток и не иерархия» в design/spec/S1.1/S1.11. Ось `verify_review_direct_request_panel` не переоткрывалась. Повторный Fable не вызывался (один вызов на гейт). `last_challenge_at` = mtime design после repair.
- **Layer 5 (Implementation Readiness):** PASS. Отчёт до repair: `reports/architecture-task-readiness-2026-08-31.md` — ГОТОВО С ЗАМЕЧАНИЯМИ (gaps = G1/G2). После repair сниппеты внесены; Layer 5.1: маркеров ручной конфигурации нет. User Task Contract: none.

### Авто-исправлено (Layer 1)

| # | Что | Было | Стало |
|---|-----|------|-------|
| 1 | whitespace-normalized | `design.md` § Risks: два пустых абзаца после заголовка | Один перевод строки перед списком |

### Развёрнутые карточки развилок

не применялось (Repair Loop, без decision)

### User Task Contract pre-check (2.1a)

none

## Источники

- `openspec/changes/universal-visual-explanation/reports/quality-control-2026-08-31.md`
- `openspec/changes/universal-visual-explanation/reports/quality-control-2026-08-31-2.md`
- `openspec/changes/universal-visual-explanation/reports/design-challenge-2026-08-31.md`
- `openspec/changes/universal-visual-explanation/reports/architecture-task-readiness-2026-08-31.md`
- алерты: `precedent-documented` (INFO); Layer 4 CHALLENGE G1–G3 → repair → APPROVE
