---
verify_mode: pre-apply
change: scenario-map-readability-meaning
date: 2026-08-30
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: FAIL
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks:
    - S1.3
    - S1.5
    - S1.6
    - S1.7
    - S1.8
    - S1.12
    - S1.16
    - S1.17
    - S1.18
    - S1.21
    - S1.22
  closed_decisions:
    - id: infographic_meaning_carriers
      summary: "Карта — инфографика: смысл с полотна (граф плюс до двух аннотаций с якорем и доказательством); зона ловушки — подсветка якоря; новое relation «ожидалось, но отсутствует» не в этой ЗНИ."
      closed_at: "2026-08-29"
      source: verify-user-answer
    - id: short_map_layout_owner
      summary: "Раскладку считает панель; полосы — дорожки по полю слоя узла, не по рангу; ручные координаты родителя не вводятся. Обратное ребро не пунктиром (пунктир — тип связи). Виды — переключатель раскладки графа."
      closed_at: "2026-08-29"
      source: verify-user-answer
    - id: main_view_answers_header
      summary: "Главный вид отвечает на вопрос шапки при скрытой шапке; средства этой ЗНИ — граф и таблица со смысловыми колонками; бюджет разборчивости; стартовый узел — исход или виновник. Расширение перечня средств и поле режимов — не в этой ЗНИ."
      closed_at: "2026-08-30"
      source: extend-loop-redesign
  open_decision_id: null
  decision_round: 3
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-08-30T00:37:19"
    design.md: "2026-08-30T00:37:21"
    tasks.md: "2026-08-30T00:39:19"
    specs/scenario-map-canvas/spec.md: "2026-08-30T00:38:16"
  last_challenge_at: "2026-08-30T00:37:21"
---

## Резюме для разработчика

scenario-map-readability-meaning — до старта нужен ваш выбор по логике таблицы и контракта манифеста.

**Следующий шаг:** внутренний ремонт постановки (без вопроса в чат), затем повторная проверка.

После петли приёмки постановка переведена с обязательного графа на «главный вид отвечает на вопрос шапки». Независимый разбор подтверждает ось, но до apply не хватает имени поля средства, контракта колонок таблицы, зеркала запрета выдуманных рёбер для строк, правила смешанного содержания и задачи на порог публикации по средству.

## Что доработать в постановке

### Рекомендации

- **Имя и контракт таблицы:** зафиксировать `header.medium`, колонки, строка = узел, выбор строки как выбор узла.
- **Порог по средству:** задача на шаги «Связи» и «Порог» скилла.
- **Предикат смысла на манифесте:** носители — поля манифеста, не раскладка панели.
- **Строка таблицы не выдумывает правило** без видимого в источнике основания.
- **Смешанное содержание:** умолчание граф; смена средства в круге ремонта смысла.
- **Бюджет:** натуральный размер, горизонтальная прокрутка, перенос ряда длиннее пяти.

## Что меняется в постановке

**Расширение / конфигурация:** kit (скилл карты, шаблон панели, роль сборщика, ADR-0009). Продуктовый код 1С не меняется.

**Точки изменения:** шаблон панели, скилл, роль сборщика, эталоны, дельта требований.

**Что НЕ меняется:** регистрация родителем, успех кнопкой среды, словарь `relation`, порог четырёх, запрет выдуманных рёбер для графа, модель сборщика.

**Связанные ADR / архив:** ADR-0008 (пять инвариантов), ADR-0009, архив `2026-08-28-scenario-map-canvas`.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте; ровно один `S1.accept`; `<!-- slice-gate -->` есть; `form_mode: n/a`; `<!-- phase-gate -->` нет; UTC DENY-grep none.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-30.md`. 17/17 Scenario; 8b Pass; критерий 10 — один осмотр. Precedent: `precedent-documented` (Blast Radius в design и ADR-0009). Code-truth: kit-only, `openspec/project.md` отсутствует, символов BSL нет.
- **Layer 2.5 (Loop Detection):** PASS. AcceptLoop(S1)=5, PatchRounds≥3; закрыто `architecture-loop-redesign-2026-08-30.md` позже последней `awaiting-acceptance`.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт; у каждого Requirement есть Scenario; implementation-leak не найден.
- **Layer 4 (Independent Challenge):** CHALLENGE → classifier: implementation_invariant (G1–G3); G4 гигиена ADR-0008. Отчёт: `reports/design-challenge-2026-08-30.md`. Closed axis не переоткрывается.
- **Layer 5 (Implementation Readiness):** FAIL. Отчёт: `reports/architecture-task-readiness-2026-08-30.md`. GAP: имя поля, контракт таблицы, задача порога, остаток режимов, порядок сверки, поведение бюджета.

### Авто-исправлено (Layer 1)

mechanical-замечаний не обнаружено

### Классификация Repair Loop

Все блокеры — repair (implementation_invariant). Decision blockers нет.

## Источники

- `reports/quality-control-2026-08-30.md`
- `reports/design-challenge-2026-08-30.md`
- `reports/architecture-task-readiness-2026-08-30.md`
- `reports/architecture-loop-redesign-2026-08-30.md`
- алерты: implementation_invariant G1–G3; L5 GAP 1–6; `precedent-documented`
