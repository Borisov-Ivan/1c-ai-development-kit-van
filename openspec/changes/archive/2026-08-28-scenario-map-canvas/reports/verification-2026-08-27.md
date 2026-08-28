---
verify_mode: pre-apply
change: scenario-map-canvas
date: 2026-08-27
verdict: GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: APPROVE
  layer_5_implementation_readiness: WARNING
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - Намёк в исследовании — отложен, не блокер apply
    - Kill-критерии — Follow-up вне среза
  artifacts_mtime:
    proposal.md: "2026-08-27T04:42:58Z"
    design.md: "2026-08-27T05:06:41Z"
    tasks.md: "2026-08-27T05:06:41Z"
    specs/scenario-map-canvas/spec.md: "2026-08-27T04:42:58Z"
  last_challenge_at: "2026-08-27T05:06:41Z"
---

## Резюме для разработчика

scenario-map-canvas — можно запускать apply. Панель рядом с чатом показывается только по просьбе: узлы «что происходит» с доказательством, без навигатора по модулю.

**Следующий шаг:** `/opsx:apply scenario-map-canvas`

План добавляет скилл карты сценария, строку в диспетчере (и запрет рисовать панель «потому что так сказала среда», и вход по просьбе) и вариант в уже существующей строке «Следующий шаг» на выходе длинного разбора с замерами. Если панель открыть нельзя, те же узлы уходят в журнал разбора и на выходе не затираются.

Границы: без просьбы панель молчит; намёк только на выходе разбора, не в исследовании; отдельной команды нет.

## Что меняется в постановке

**Расширение / конфигурация:** kit (файлы `.cursor/` и `openspec/`), продуктовый BSL не меняется.

**Точки изменения:**

- `.cursor/skills/scenario-map-canvas/SKILL.md` — новый контракт панели: узел = эффект шага + доказательство; порядок действий по просьбе.
- `.cursor/rules/gate-dispatcher.mdc` — always-apply строка: в сессиях `/opsx:*` карту рисовать только по просьбе или намёку; просьба → прочитать скилл.
- `.cursor/skills/openspec-explain/SKILL.md` и `templates/exit-card.md` — просьба в середине прохода без смены команды; намёк в существующей строке «Следующий шаг»; запись журнала сохраняет секцию «Карта сценария».
- `.cursor/skills/openspec-explain/templates/explain-report.md` — необязательная секция «Карта сценария» в каркасе журнала.
- `.cursor/docs/chat-lexicon.md` (Слой 2), `openspec/glossary.md`, `AGENTS.md` — два имени: карта точек vs карта сценария.

**Что НЕ меняется:** карта точек в чате; слот «Дальше» в исследовании; `opsx-output-style.md`, `brief-card.md`, шаблон карты точек; прикладная конфигурация 1С.

**Связанные ADR / KB / архив:** ADR-0001 (намёк — в чат, без внутренних имён); ADR-0002 (карту не подмешивать в бриф Охвата); архив `explain-after-review-apply-scope` (без новой команды и без автостарта). Таксономия KB в kit отсутствует.

### К сведению

- Намёк в исследовании отложен: не занимает слот «Дальше» у предложения разбора.
- Kill-критерии карты — Follow-up вне среза, не блокер старта.
- Наблюдения реализации (не блокеры): строка диспетчера несёт и запрет, и указатель на скилл; эталон узлов — секция в скилле, не отдельный fixture-файл; в журнале рядом окажутся заголовки «Карта» (имена точек) и «Карта сценария» (узлы панели).

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте, `<!-- slice-gate -->` закрыт, fences сбалансированы. Info: Follow-up без префикса среза (вне среза, ожидаемо). `form_mode: n/a`.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-27-3.md` — OK. 15/15 scenarios покрыты (Primary / optional / S1.<M>). User Task Contract: none. Один срез, один accept, self-achievable Primary.
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` без Slice Gate Decisions; AcceptLoop = 0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт requirements; у каждого Requirement есть Scenario; scenarios в матрице design. implementation-leak в THEN нет. `comment_suffix` пустой, `marker_style: minimal` — kit meta-change, BSL-маркеры n/a.
- **Layer 4 (Independent Challenge):** APPROVE. Отчёт: `reports/design-challenge-2026-08-27-3.md`. Первый прогон CHALLENGE (три implementation_invariant); после repair residual R1 (стык журнала); после второй правки — APPROVE. Ось не менялась.
- **Layer 5 (Implementation Readiness):** WARNING. Отчёт: `reports/architecture-task-readiness-2026-08-27-3.md` — ГОТОВО С ЗАМЕЧАНИЯМИ, блокирующих GAP нет. Ручных маркеров конфигурации не найдено.

### Авто-исправлено (Layer 1)

mechanical-замечаний не обнаружено

### Repair Loop (internal)

Две итерации repair-from-verify (не user-extend):

1. Молчание в always-apply диспетчере; согласование порогов 5 точек / 4 узлов; источник вне разбора; порядок действий по просьбе; отказ от «чат-файла разбора».
2. Секция «Карта сценария» в каркасе журнала; Write на выходе секцию сохраняет (S1.10a).

### Code-Truth Gate

- status: OK
- checked artifacts: design.md, tasks.md, debug.md, specs/**
- `openspec/project.md` отсутствует (kit). 1С-символов процедур/модулей нет. phantom-symbols: none (pre-apply).

### Precedent Regression (Layer 2.4)

- Дельта spec: только ADDED, MODIFIED/REMOVED нет.
- Invariant KB: taxonomy отсутствует, фактов нет.
- Load-Bearing ADR-0001 упомянут как связанный, без Supersedes, без Blast Radius (отмены нет).
- Алерты: нет CRITICAL.

### Развёрнутые карточки развилок

нет (verdict GO)

## Источники

- `openspec/changes/scenario-map-canvas/reports/quality-control-2026-08-27.md`
- `openspec/changes/scenario-map-canvas/reports/quality-control-2026-08-27-2.md`
- `openspec/changes/scenario-map-canvas/reports/quality-control-2026-08-27-3.md`
- `openspec/changes/scenario-map-canvas/reports/design-challenge-2026-08-27.md`
- `openspec/changes/scenario-map-canvas/reports/design-challenge-2026-08-27-2.md`
- `openspec/changes/scenario-map-canvas/reports/design-challenge-2026-08-27-3.md`
- `openspec/changes/scenario-map-canvas/reports/architecture-task-readiness-2026-08-27.md`
- `openspec/changes/scenario-map-canvas/reports/architecture-task-readiness-2026-08-27-2.md`
- `openspec/changes/scenario-map-canvas/reports/architecture-task-readiness-2026-08-27-3.md`
- алерты: none blocking
