---
verify_mode: pre-apply
change: scenario-map-canvas
date: 2026-08-28
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
  accepted_tasks:
    - S1.1
    - S1.1a
    - S1.2
    - S1.3
    - S1.4
    - S1.5
    - S1.6
    - S1.7
    - S1.8
    - S1.9
    - S1.10
    - S1.10a
    - S1.11
    - S1.12
    - S1.13
  closed_decisions:
    - id: direct_request_linear_publish
      summary: "Прямая просьба сильнее предложения: при ≥4 публикуемых сущностях панель всегда; линейная цепочка с подписанными связями допустима; предлагать схему по-прежнему только при топологии."
      closed_at: "2026-08-28"
      source: verify-user-answer
    - id: edges_evidenced_or_investigate
      summary: "Подписи на связях только из уже видимых фактов (отчёт, журнал, порядок прохода); выдумывать рёбра запрещено; если связей не хватает — панель не публиковать, можно продолжить разбор или исследование."
      closed_at: "2026-08-28"
      source: verify-user-answer
  open_decision_id: null
  decision_round: 2
  decision_round_max: 2
  verify_depth: incremental
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-08-28T03:09:56Z"
    design.md: "2026-08-28T04:40:12Z"
    tasks.md: "2026-08-28T04:40:38Z"
    specs/scenario-map-canvas/spec.md: "2026-08-28T04:38:39Z"
  last_challenge_at: "2026-08-28T04:40:12Z"
---

## Резюме для разработчика

scenario-map-canvas — можно запускать apply.

План правит скилл `.cursor/skills/scenario-map-canvas/SKILL.md`, строку в диспетчере гейтов, шаблоны разбора и исследования и роль исполнителя макета. Продуктовый BSL не меняется. Первый срез уже в коде кита; его приёмка ещё не подписана.

**Следующий шаг:** `/opsx:apply scenario-map-canvas`

## Что меняется в постановке

**Расширение / конфигурация:** kit (`.cursor/`, `openspec/`), продуктовый BSL не меняется.

**Точки изменения:**

- `.cursor/skills/scenario-map-canvas/SKILL.md` — контракт шапка / узлы / связи / виды; создание файла панели с нуля; проверка, когда схему предлагать; намёк не собирает панель; сборку файла отдаёт исполнитель макета.
- `.cursor/rules/gate-dispatcher.mdc` — просьба и принятое предложение рисуют; намёк только предлагает.
- `.cursor/skills/openspec-explain/` и `.cursor/skills/openspec-explore/SKILL.md` — вариант схемы в существующих строках решения; отложенная постройка «сразу карту» со ссылкой в том же сообщении, что карточка порога.
- `.cursor/agents/onec-scenario-map-designer.md` и таблица ролей — исполнитель макета, без отдельного слага модели.

**Что НЕ меняется:** отдельной команды карты нет; молчание без просьбы и без принятого предложения; файл панели не в git; `opsx-output-style.md` и `brief-card.md` не трогаются; прикладная конфигурация 1С не меняется.

**Связанные ADR / KB / архив:** ADR-0001, ADR-0002, ADR-0006 соблюдены, не отменяются. Таксономия KB в kit отсутствует.

### К сведению

- Заголовок первого среза всё ещё упоминает намёк на выходе; печать варианта — работа третьего среза. На apply не влияет.
- Сценарий «Семь линейных шагов не обязаны давать карту» указан в связях и второго, и третьего среза (косметика).
- Маркеров ручной конфигурации нет; `form_mode: n/a`.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте, `<!-- slice-gate -->` закрыт на S1/S2/S3, fences сбалансированы. Info: Follow-up без префикса среза; `form_mode: n/a`.
- **Layer 2 (Internal Coherence):** PASS. QC `reports/quality-control-2026-08-28-6.md` Verdict OK; 37/37 Scenario покрыты. SUGGESTION only (dual Связь listing; stale S1 heading). User Task Contract: none. Precedent: spec только ADDED, архива capability нет; Blast Radius относительно S1 заполнен. Code-truth pre-apply: kit markdown, phantom будущих файлов (fixtures, агент картографа) — WARNING рецепта, не блокер.
- **Layer 2.5 (Loop Detection):** PASS. S1.accept `[ ]`, AcceptLoop=1 (awaiting-acceptance); PatchRounds по `## Extend —` < порога 3. S2/S3 без awaiting-acceptance. Repair без новой секции `## Extend —`.
- **Layer 3 (Problem-Solution Trace):** PASS. Why (три провала) покрыты Direct request / Offer / Technical fallback / Node contract. Каждый Requirement имеет Scenario. Scenario ↔ Slices и accept/tasks согласованы. scenario-implementation-leak: none. comment_suffix пуст (kit, маркеры BSL не применяются).
- **Layer 4 (Independent Challenge):** APPROVE. Отчёт: `reports/design-challenge-2026-08-28-6.md`. Residual — формулировки задач, не развилки. last_challenge_at обновлён до mtime design.md.
- **Layer 5 (Implementation Readiness):** PASS. Отчёт: `reports/architecture-task-readiness-2026-08-28-6.md` вердикт ГОТОВО. Маркеров ручной конфигурации не найдено. GAP предыдущего прогона (S2.4a) закрыт repair.

### Авто-исправлено (Layer 1)

не применялось

### Repair Loop

internal repair-from-verify, attempt 1: закрыты ход публикации отложенного согласия, разведение сценариев предложения разбора, исход к выходу без порога, наследование раскладки согласия, S2.4a. Без user-facing extend. После repair — повтор L2/L4/L5.

### Развёрнутые карточки развилок

нет

## Источники

- `openspec/changes/scenario-map-canvas/reports/quality-control-2026-08-28-6.md`
- `openspec/changes/scenario-map-canvas/reports/design-challenge-2026-08-28-6.md`
- `openspec/changes/scenario-map-canvas/reports/architecture-task-readiness-2026-08-28-6.md`
- alerts: none blocking; SUGGESTION dual-svyaz-listing, stale-S1-heading
