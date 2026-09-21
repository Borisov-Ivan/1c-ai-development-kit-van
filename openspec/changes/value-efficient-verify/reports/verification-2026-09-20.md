---
verify_mode: pre-apply
change: value-efficient-verify
date: 2026-09-20
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: WARNING
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: WARNING
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: WARNING
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: unregistered_external_evidence
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - когда свежее указание заказчика без записи в журнале останавливает проверку
  artifacts_mtime:
    proposal.md: "2026-09-20T09:51:50Z"
    design.md: "2026-09-20T09:56:11Z"
    tasks.md: "2026-09-20T10:02:17Z"
    specs/value-efficient-verify/spec.md: "2026-09-20T09:56:32Z"
  last_challenge_at: "2026-09-20T09:56:11Z"
post_challenge_classifier:
  decision: unregistered_external_evidence
  repair_deferred_until_user_answer:
    - implementation_invariant: fingerprint vs B7 (design D4)
    - implementation_invariant: who may set confirmation for customer-direct
    - implementation_invariant: map cascade onto existing verdict formula
    - implementation_invariant: External Contract Ledger vs Verify decision ledger priority
    - design-slice-spec-title-drift
    - task-readiness G1 rules_versions / hash recipe
    - task-readiness G2 reopen vs closed_decisions
    - task-readiness G4 invalidation_map vs verify_depth
  dropped:
    - G6 test fixture (transient; QC 8b self-achievable OK)
    - G8 runtime-defect boundary (already design Non-Goals)
    - D5 hash-vs-section-table fork (axis holds; neither alternative fully superior)
    - reopen-closed-decision: none (closed_decisions empty)
---

## Резюме для разработчика

value-efficient-verify — до старта нужен ваш выбор по логике внешнего журнала ожиданий.

**Что решить: когда свежее указание заказчика начинает останавливать проверку**

План останавливает работу только по уже занесённым записям. Пустой журнал считается старым режимом. Указание, которое никто не занёс, проверка пропустит — хотя боль как раз в расхождении с заказчиком при внутренне связном плане.

- **A. Только занесённые записи** — меньше ложных остановок, но свежая фраза в отчёте или возврате не остановит работу, пока её явно не занесут.
- **B. Сначала спросить про найденное** — если в уже читаемых файлах есть свежее указание без записи, проверка спрашивает: занести как тему или отклонить. Забытое указание не пройдёт молча, но появятся вопросы на шум в файлах.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify value-efficient-verify`.

План меняет навык проверки ЗНИ и связанные правила: журнал ожиданий в существующем файле истории ЗНИ, ранняя остановка повторной темы, затем точечный пересчёт контролей. Кода конфигурации 1С нет.

## Решения до apply

### Когда свежее указание заказчика начинает останавливать проверку

**Цель ЗНИ:** прямые указания заказчика и явно принятые оси референса должны быть обязательным входом проверки, чтобы внутренне связный план не проходил при расхождении с более свежим внешним ожиданием.

**Что в коде сейчас.** Навык `.cursor/skills/openspec-verify-change/SKILL.md` читает постановку и журнал решений проверки. Свежая фраза заказчика в отчёте или возврате не является самостоятельным источником новизны, пока её не занесли структурированной записью.

**Что предлагает план.** Секция `## External Contract Ledger` в `debug.md`. Проверка блокирует только по записям с источником и уровнем авторитетности. Нет секции — старый режим, не ошибка. Регистрация возвратов планируется в навыке применения на границе среза.

**Почему это развилка.** Независимая проверка плана: Requirement «Внешний контракт участвует в проверке» выполняется при пустом журнале. Самый частый отказ — «заказчик сказал новое, запись не создали» — проходит так же, как сегодня. Это сохраняет исходную боль из `## Why`.

**Варианты решения.**

- **A. Только занесённые записи** — сохранить Behavior Contract п. 1 и план миграции: внешним контрактом считаются только структурированные записи; отсутствие секции не ошибка. **Компромисс:** меньше ложных остановок, но незанесённое указание не блокирует.
- **B. Сначала спросить про найденное** — если в уже читаемых проверкой файлах есть свежее внешнее событие позже последней записи журнала, оркестратор требует классификацию «занести как тему / отклонить с причиной» до продолжения. **Компромисс:** забытое указание не проходит молча, но появятся вопросы на шум в файлах.

**Влияет на:** остановится ли `/opsx:verify` (и дальше `/opsx:apply`), когда указание заказчика ещё не занесено в журнал.

**Что изменится после выбора.** Выбор зафиксируется в постановке (design / spec / tasks) и в человекочитаемой секции «Решения verify». Repair-уточнения формулы отпечатка, кто закрывает запись и стык с существующим журналом решений — после ответа.

## Что меняется в постановке

**Расширение / конфигурация:** kit (`.cursor/skills`, `.cursor/rules`, `.cursor/agents`) — не выгрузка `src/` 1С.

**Точки изменения:**

- `.cursor/skills/openspec-verify-change/SKILL.md` — чтение журнала ожиданий, ранняя остановка, каскад и дельта повторной проверки.
- `.cursor/rules/openspec-specs-gate.mdc`, `.cursor/rules/vertical-slices.mdc`, `.cursor/rules/architect-gate.mdc` — оси референса, повтор темы vs петля приёмки, триггеры профильного разбора.
- `.cursor/skills/openspec-apply-change/SKILL.md`, `.cursor/skills/review/SKILL.md` — регистрация и передача затронутых записей.
- `.cursor/agents/onec-code-reviewer.md`, `.cursor/agents/openspec-quality-controller.md`, `.cursor/agents/onec-code-architect.md` — узкий контекст по затронутым записям и дельте.

**Что НЕ меняется:** объекты метаданных 1С; инвариант ADR-0010 (панель объяснения на проверке сама не открывается); порог трёх раундов приёмки среза как запас для ЗНИ без классифицированной темы.

**Связанные ADR / KB / архив:** ADR-0010 (Load-Bearing) — без отмены. Архивных ЗНИ с capability `value-efficient-verify` нет. KB taxonomy в kit отсутствует.

### К сведению

- В `design.md` у первого среза «Связь со spec» ещё старые заголовки требований и сценария; в `tasks.md` и spec имена уже совпадают. Покрытие сценариев 6/6.
- Приёмочный прогон на универсальной тестовой ЗНИ — граница среза, не рабочая задача. Отсутствие самой тестовой ЗНИ в задачах не блокирует старт реализации.
- Честная граница «проверка постановки не обещает найти любой дефект времени выполнения» уже в Non-Goals; отдельный сценарий spec не обязателен.
- Замечания к формулировкам задач (источник версии правила, стык с журналом закрытых решений, приоритет карты инвалидации и глубины проверки) — после выбора по журналу ожиданий.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы, `<!-- slice-gate -->`, `form_mode: n/a`, без `<!-- phase-gate -->`.
- **Layer 2 (Internal Coherence):** WARNING. QC `reports/quality-control-2026-09-20.md` verdict OK. Алерт `design-slice-spec-title-drift` (SUGGESTION в QC; механический `scenario-orphan-design` по точному заголовку «Открытый сигнал высокого авторитета» в design Slices). User Task Contract pre-check: none. Code-Truth: символов процедур 1С нет (kit markdown). Precedent 2.4: дельта spec только ADDED; archive по capability пуст; Supersedes Load-Bearing нет.
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` на момент прогона отсутствовал; `S1.accept`/`S2.accept` = `[ ]`; AcceptLoop/PatchRounds = 0.
- **Layer 3 (Problem-Solution Trace):** WARNING. Why покрыт четырьмя Requirement. Каждый Requirement имеет Scenario. `scenario-implementation-leak`: нет маркеров. `process-only-marker-suffix`: comment_suffix пуст. `scenario-orphan-slice` — то же расхождение имени в design S1.
- **Layer 4 (Independent Challenge):** CHALLENGE. Отчёт: `reports/design-challenge-2026-09-20.md`. Classifier: одна decision-развилка `unregistered_external_evidence` (Why ↔ structured-only ledger). Остальное — repair после ответа либо drop (см. YAML `post_challenge_classifier`). last_challenge_at обновлён (= design_mtime).
- **Layer 5 (Implementation Readiness):** WARNING. Отчёт: `reports/architecture-task-readiness-2026-09-20.md` — ГОТОВО С ЗАМЕЧАНИЯМИ. 5.1 manual-config: маркеров нет. User Task Contract: OK. GAP не CRITICAL (as-is реализуемо вставками в tasks/design).

### Авто-исправлено (Layer 1)

mechanical-замечаний не обнаружено

### Развёрнутые карточки развилок

См. «Решения до apply». Код: `unregistered_external_evidence`. Смешанный отчёт: decision имеет приоритет; repair не запускался.

## Источники

- `openspec/changes/value-efficient-verify/reports/quality-control-2026-09-20.md`
- `openspec/changes/value-efficient-verify/reports/design-challenge-2026-09-20.md`
- `openspec/changes/value-efficient-verify/reports/architecture-task-readiness-2026-09-20.md`
- алерты: `design-slice-spec-title-drift`, `scenario-orphan-design`, `scenario-orphan-slice`
