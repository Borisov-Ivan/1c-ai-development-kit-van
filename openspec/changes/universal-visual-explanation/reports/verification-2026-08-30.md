---
verify_mode: pre-apply
change: universal-visual-explanation
date: 2026-08-30
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
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: verify_review_direct_request_panel
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "панель по прямой просьбе на /opsx:verify и /review"
  artifacts_mtime:
    proposal.md: "2026-08-30T09:30:22Z"
    design.md: "2026-08-30T09:45:56Z"
    tasks.md: "2026-08-30T10:06:59Z"
    specs/visual-explanation/spec.md: "2026-08-30T09:40:51Z"
    specs/scenario-map-canvas/spec.md: "2026-08-30T09:32:50Z"
    specs/always-apply-context-budget/spec.md: "2026-08-30T09:32:51Z"
    specs/delegation-safeguards/spec.md: "2026-08-30T09:32:51Z"
  last_challenge_at: "2026-08-30T09:45:56Z"
---

## Резюме для разработчика

universal-visual-explanation — до старта нужен ваш выбор по логике панели на проверке постановки и ревью.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify universal-visual-explanation`.

План снимает «карту сценария» и ставит визуальное объяснение: скилл `.cursor/skills/visual-explanation/SKILL.md`, тонкий шаблон `fixtures/panel-shell.md` на примитивах среды, указатели сессий, удаление старого скилла и агента-сборщика, ADR-0010 вместо ADR-0008 и ADR-0009. Прикладной код 1С не меняется. Срез один: по просьбе «покажи, как это устроено» рядом с чатом открывается панель; старого конвейера в рабочих файлах kit нет.

Независимый разбор постановки: цель «схема появляется, когда без картинки хуже» расходится с полным запретом панели на `/opsx:verify` и `/review` даже по просьбе. Остальные замечания разбора — дописка инвариантов (без DAG в первой поставке, лестница упрощения, список миграции) и не блокируют выбор.

## Решения до apply

### 1. Панель по просьбе на проверке постановки и ревью

**В чём проблема.** План запрещает kit-панель на `/opsx:verify` и `/review` и по просьбе, и сам; цель ЗНИ этого запрета не просит.

**На что влияет.** Во время проверки постановки и ревью кода «покажи, как устроено» либо откроет панель кнопкой среды, либо останется текстом — даже если ответ ветвистый.

**Если выбрать A / B.** A — по просьбе панель есть, сами не открываем; в чате по-прежнему одна строка. B — панели нет даже по просьбе, пока идёт эта команда; запрет нужно явно записать в цель ЗНИ.

**Что в коде сейчас.** `design.md` Behavior Contract п. 2 и spec «Проверка постановки без панели»: kit-панель не строить ни по просьбе, ни авто. В Blast Radius запрет сохранён «из‑за канона одного сообщения»; Why про это молчит. Задачи S1.1 и S1.11 повторяют полный запрет.

**Что предлагает план.** Замена карты на объяснение того же вопроса; автопанель только на развилке / сравнении / иерархии; на verify/review — полное молчание.

**Почему это развилка.** Независимый разбор: молчание на просьбе в самых «структурных» сессиях повторяет старую причину «карты нет, когда нужна». Два наблюдаемых поведения; ось носителя (родитель пишет файл, без сборщика) не меняется.

**Варианты решения.**

- **A. По просьбе открывать** — spec/design: на `/opsx:verify` и `/review` MUST NOT автопанель и MUST NOT системный canvas; прямая просьба открывает панель; чат — одна строка эффекта. S1.1, S1.11, Scenario «Проверка постановки без панели» переписать под этот контракт.
- **B. Не открывать даже по просьбе** — полный запрет остаётся; в `proposal.md` ## Why / Impact одна фраза, что проверка постановки и ревью сознательно без kit-панели.

**Что изменится после выбора.** Фиксация в proposal/design/spec/tasks; затем дописка инвариантов первой поставки (без `computeDAGLayout`, лестница до кнопки среды, указатели `AGENTS.md`).

**Источники** *(техническое):* `reports/design-challenge-2026-08-30-2.md` gap 2; alert `implementation_invariant` смешан с Why↔plan → decision.

## Что меняется в постановке

**Расширение / конфигурация:** прикладной `src/` не затрагивается. Меняется kit: `.cursor/skills/`, `.cursor/rules/`, `.cursor/agents/`, `openspec/adrs/`.

**Точки изменения:**

- `.cursor/skills/visual-explanation/SKILL.md` — новый протокол просьбы и автопанели (ещё не создан).
- `.cursor/skills/visual-explanation/fixtures/panel-shell.md` — тонкий рендер `Stack` / `Table` / `Text`.
- `.cursor/rules/gate-dispatcher.mdc` — указатель «покажи схему» на новый скилл.
- `.cursor/skills/scenario-map-canvas/**`, `.cursor/agents/onec-scenario-map-designer.md` — удаление.
- `openspec/adrs/ADR-0010-visual-explanation-panel.md` — несущая замена ADR-0008 и ADR-0009.

**Что НЕ меняется:** регистрация файла панели родителем и успех кнопкой среды; запрет голого списка без вывода; файл панели не в git; «без схемы» до выхода сессии; «покажи схему компоновки» — ответ про 1С; соседняя ЗНИ `scenario-map-explain-and-overlap` не реализуется.

**Связанные ADR / KB / архив:** ADR-0008, ADR-0009 → ADR-0010; архивы `2026-08-28-scenario-map-canvas`, `2026-08-30-scenario-map-readability-meaning`, `2026-08-30-overview-map-offer`, `2026-08-30-scenario-map-show-scheme-phrase`. KB в kit нет.

### К сведению

- Отмена capability `scenario-map-canvas` и несущих ADR-0008/0009 в design закрыта таблицей последствий для человека, не молча.
- Соседнюю открытую ЗНИ про наложение подписей план не сливает и не доводит — только пометка в её журнале.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте; `<!-- slice-gate -->` закрыт; `form_mode: n/a`; префиксы `S1.` есть; fences сбалансированы.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-30-2.md` — OK, 22/22 Scenario, 8b/11 чистые. Code-Truth: нет 1С-символов в backticks, `openspec/project.md` отсутствует (kit) — не phantom. Precedent 2.4: ADDED→REMOVED/MODIFIED по `scenario-map-canvas`, `always-apply-context-budget` (Map cue), `delegation-safeguards` (Map designer) + supersede Load-Bearing 0008/0009 закрыты `## Blast Radius` → INFO `precedent-documented`.
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` до прогона отсутствовал; `S1.accept` не принимался; AcceptLoop = 0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт ADDED `visual-explanation`; у каждого ADDED/MODIFIED Requirement есть Scenario; implementation-leak в THEN нет; `comment_suffix` пустой при `marker_style: minimal` — допустимо.
- **Layer 4 (Independent Challenge):** CHALLENGE. Отчёт: `reports/design-challenge-2026-08-30-2.md`. Post-challenge classifier: gap 2 (verify/review просьба vs полный запрет) → decision (Why↔plan); gaps 1, 3–7 → `implementation_invariant` (отложены до ответа на decision, mixed-report rule).
- **Layer 5 (Implementation Readiness):** PASS. Отчёт: `reports/architecture-task-readiness-2026-08-30.md` — ГОТОВО, gaps_count: 0. Layer 5.1: маркеров ручной конфигурации нет.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

См. `## Решения до apply` § 1. Agent-key: `verify_review_direct_request_panel`.

Отложенный repair (после user-extend `--from-verify` по ответу):

1. MUST NOT `computeDAGLayout` / абсолютная раскладка в v1; S1.2 без «при необходимости».
2. Один порог появления: авто = закрытый перечень spec; предложение ≠ вопрос «точно схему?».
3. Операциональная лестница до кнопки среды (порог элементов/связей → таблица или карточка, не DAG).
4. Design Behavior 7 = spec: оба чтения «панель / объект 1С» → одна строка выбора.
5. Migration Plan: `AGENTS.md`, `.cursor/docs/agents-CHANGELOG.md`.
6. Behavior 3: шапка — часть объяснения; не экзамен скрытой шапки ADR-0009.

### User Task Contract pre-check (2.1a)

none

## Источники

- `openspec/changes/universal-visual-explanation/reports/quality-control-2026-08-30-2.md`
- `openspec/changes/universal-visual-explanation/reports/design-challenge-2026-08-30-2.md`
- `openspec/changes/universal-visual-explanation/reports/architecture-task-readiness-2026-08-30.md`
- алерты: `precedent-documented` (INFO); Layer 4 CHALLENGE gap 2 → decision; deferred `implementation_invariant` gaps 1, 3–7
