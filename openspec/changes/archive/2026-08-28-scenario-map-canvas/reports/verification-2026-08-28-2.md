---
verify_mode: pre-apply
change: scenario-map-canvas
date: 2026-08-28
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
  repair_attempt: 2
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
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - edge_origin_from_walk_vs_invent
    - deferred_offer_publish_turn
    - offer_scenario_inventory_vs_exit
  artifacts_mtime:
    proposal.md: "2026-08-28T03:09:56Z"
    design.md: "2026-08-28T03:59:49Z"
    tasks.md: "2026-08-28T04:01:40Z"
    specs/scenario-map-canvas/spec.md: "2026-08-28T03:59:24Z"
  last_challenge_at: "2026-08-28T03:59:49Z"
---

## Резюме для разработчика

scenario-map-canvas — apply пока нельзя: не удалось автоматически дописать постановку за 2 итерации.

В постановке уже ясно: по просьбе схема строится даже на цепочке шагов, намёк только предлагает и не рисует сам, а в исследовании карта берётся из текущего отчёта. Не зафиксировано, откуда на схеме берутся подписи на связях — из порядка уже разобранных шагов или их нельзя ставить, пока связь не видна в отчёте. Из-за этого первая просьба снова может дать пустую панель или выдуманные стрелки. Также не сказано, в каком сообщении чата появляется ссылка на панель, если человек согласился на «сразу карту» ещё до первой карточки, а четыре сущности накопились позже.

**Следующий шаг:** опишите в чате, как поступить, или `/opsx:extend scenario-map-canvas`.

План правит скилл `.cursor/skills/scenario-map-canvas/SKILL.md`, строку в `gate-dispatcher.mdc`, шаблоны разбора и исследования, таблицу ролей и файл агента картографа. Продуктовый BSL не меняется. Первый срез уже в коде кита; приёмка этого среза ещё не подписана.

## Что доработать в постановке

### Рекомендации

- **Откуда стрелки на панели:** в постановке контракта карты или роли картографа явно: для линейной просьбы источником подписанных связей может быть порядок уже разобранных карточек или записей журнала; для ветвления — только отношение, уже видное в переданном отчёте или журнале; додумывать рёбра из модуля вне переданных диапазонов нельзя так же, как публиковать узел без доказательства.
- **Когда появляется панель после «сразу карту»:** одна строка в том же ходе, где карточка прохода впервые дала четыре связанные сущности с доказательством; не ждать выхода разбора; не занимать слот шага отдельным вопросом про карту.
- **Предложение на списке точек vs на выходе:** в сценарии «Разбор предлагает схему без замеров» развести два момента: на подтверждении списка — вариант по предсказанной топологии без порога «уже четыре»; на выходе — порог после обоих отсевов.

## Что меняется в постановке

**Расширение / конфигурация:** kit (`.cursor/`, `openspec/`), продуктовый BSL не меняется.

**Точки изменения:**

- `.cursor/skills/scenario-map-canvas/SKILL.md` — контракт шапка / узлы / связи / виды; создание файла панели с нуля; проверка, когда схему предлагать; намёк не собирает панель.
- `.cursor/rules/gate-dispatcher.mdc` — просьба и принятое предложение рисуют; намёк только предлагает.
- `.cursor/skills/openspec-explain/` и `.cursor/skills/openspec-explore/SKILL.md` — вариант схемы в существующих строках решения; отложенная постройка «сразу карту».
- `.cursor/agents/onec-scenario-map-designer.md` и `.cursor/rules/model-selection.mdc` — роль макета; в таблице ролей без параметра модели.
- `.cursor/docs/chat-lexicon.md`, `openspec/glossary.md` — три имени: карта точек, карта сценария, текстовый резерв.

**Что НЕ меняется:** отдельной команды карты нет; без просьбы и без принятого предложения панель сама не появляется; `opsx-output-style.md` и `brief-card.md`; прикладная конфигурация 1С; карта на `/review` и на этой команде проверки — вне этой ЗНИ.

**Связанные ADR / KB / архив:** ADR-0001, ADR-0002, ADR-0006; архивного `specs/scenario-map-canvas` нет. Таксономия KB в kit отсутствует.

### К сведению

- Приёмка первого среза ещё не подписана; рабочие задачи этого среза уже отмечены сделанными.
- Follow-up про критерии отключения карты — вне срезов.
- Заголовок первого среза всё ещё упоминает намёк на выходе; намёк теперь у третьего среза — косметика.
- Сценарий «Семь линейных шагов не обязаны давать карту» дважды в связи второго и третьего среза — косметика.
- `form_mode: n/a`; маркеров ручной конфигурации 1С нет.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте, `<!-- slice-gate -->` закрыт на S1/S2/S3, fences сбалансированы. Info: Follow-up без префикса среза; `form_mode: n/a`.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-28-4.md` — Verdict OK; CRITICAL/WARNING нет; 33/33 Scenario покрыты. SUGGESTION: dual Связь «Семь линейных шагов…»; устаревший заголовок S1.
- **Layer 2.5 (Loop Detection):** PASS. S1.accept `[ ]`; AcceptLoop(S1)=1; PatchRounds(S1)=2 < 3. S2/S3 без awaiting-acceptance. Repair записан в `## Verify repair —`, без третьего `## Extend —` на незапущенные срезы.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт requirements. У каждого Requirement есть Scenario. implementation-leak в THEN нет. `comment_suffix` пустой.
- **Layer 4 (Independent Challenge):** CHALLENGE. Отчёт: `reports/design-challenge-2026-08-28-4.md`. Ось просьбы не переоткрыта (`reopen-blocked: direct_request_linear_publish`). Classifier: Gaps 1–3 — `implementation_invariant`. Repair Loop attempt 2 исчерпан — residual не ушёл в decision A/B.
- **Layer 5 (Implementation Readiness):** PASS. Отчёт: `reports/architecture-task-readiness-2026-08-28-4.md` — ГОТОВО. Ручных маркеров конфигурации не найдено. User Task Contract: OK.

### Авто-исправлено (Layer 1)

mechanical-замечаний не обнаружено

### Code-Truth Gate

- status: OK (pre-apply WARNING-класс не эскалирован)
- checked artifacts: design.md, tasks.md, debug.md, specs/**
- `openspec/project.md` отсутствует (kit). 1С-символов процедур/модулей нет.
- planned files (ещё не в репо, ожидаемо): `.cursor/agents/onec-scenario-map-designer.md`, `fixtures/map-good-causal.md`, `fixtures/map-bad-accordion.md`, `1c-agent-patterns/scenario-map-designer.md`.
- phantom-symbols: none для существующего кита.

### Precedent Regression (Layer 2.4)

- Дельта spec: только ADDED, MODIFIED/REMOVED нет. Архивного `specs/scenario-map-canvas/spec.md` нет.
- Invariant KB: taxonomy отсутствует, фактов нет.
- Load-Bearing ADR-0001 упомянут как связанный, без Supersedes.
- Blast Radius в design закрывает отмену контрактов S1 этой же ЗНИ (не архив).
- Алерты CRITICAL: нет.

### Repair Loop

Два internal repair-from-verify в этом прогоне: (1) источник согласия / порог / отложенная постройка / финал с постановкой; (2) намёк не рисует, просьба в исследовании берёт отчёт, MAY на списке точек, сценарии публикации. После attempt 2 Layer 4 остался CHALLENGE (происхождение рёбер, ход публикации, разведение сценария предложения). Terminal: не авто-чинить дальше.

## Источники

- `openspec/changes/scenario-map-canvas/reports/quality-control-2026-08-28-4.md`
- `openspec/changes/scenario-map-canvas/reports/design-challenge-2026-08-28-4.md`
- `openspec/changes/scenario-map-canvas/reports/architecture-task-readiness-2026-08-28-4.md`
- алерты: `implementation_invariant` residual after repair cap (edge origin, deferred publish turn, offer scenario split)
