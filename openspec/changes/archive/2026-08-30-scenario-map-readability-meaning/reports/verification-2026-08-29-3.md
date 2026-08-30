---
verify_mode: pre-apply
change: scenario-map-readability-meaning
date: 2026-08-29
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
  closed_decisions:
    - id: infographic_meaning_carriers
      summary: "Карта — инфографика: смысл с полотна (граф плюс до двух аннотаций с якорем и доказательством); зона ловушки — подсветка якоря; новое relation «ожидалось, но отсутствует» не в этой ЗНИ."
      closed_at: "2026-08-29"
      source: verify-user-answer
    - id: short_map_layout_owner
      summary: "Раскладку считает панель; полосы — дорожки по полю слоя узла, не по рангу; ручные координаты родителя не вводятся. Обратное ребро не пунктиром (пунктир — тип связи). Виды — переключатель раскладки; режимы — подсветка."
      closed_at: "2026-08-29"
      source: verify-user-answer
  open_decision_id: null
  decision_round: 2
  decision_round_max: 2
  verify_depth: incremental
  assumptions_accepted: []
  open_known_questions:
    - "Кто судит спорную формулировку вывода в шапке (родитель vs приёмка) — не блокирует старт; по умолчанию родитель, пользователь — последняя инстанция на приёмке среза"
  artifacts_mtime:
    proposal.md: "2026-08-29T18:29:18"
    design.md: "2026-08-29T18:29:58"
    tasks.md: "2026-08-29T18:30:33"
    specs/scenario-map-canvas/spec.md: "2026-08-29T18:29:58"
  last_challenge_at: "2026-08-29T18:29:58"
---

## Резюме для разработчика

scenario-map-readability-meaning — можно запускать apply. Шаблон панели сам считает раскладку и рисует полосы по слоям узлов.

Уже зафиксировано: смысл читается с полотна (граф и выносы с доказательством); раскладку считает панель, полосы — дорожки по слою.

План правит шаблон `.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`, скилл карты и роль сборщика. Клик по узлу больше не открывает модуль: файл открывается кнопкой в панели деталей.

На живой карте штампа ЭП проверьте, что полосы слоёв не накрывают друг друга.

**Следующий шаг:** `/opsx:apply scenario-map-readability-meaning`

Полный отчёт: openspec/changes/scenario-map-readability-meaning/reports/verification-2026-08-29-3.md

После закрытия развилки раскладки независимый разбор постановки подтвердил выбранный путь: направление связей, легенда, честные полосы и клик-как-выбор бьют в конкретные места текущего шаблона. Прикладная конфигурация 1С не меняется.

## Что меняется в постановке

**Расширение / конфигурация:** kit (не `src/` конфигурации 1С).

**Точки изменения:**

- `.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md` — полосы по полю `layer`, маркер направления и легенда, выбор узла без открытия файла, кнопка доказательства, рендер аннотаций у якоря, подсветка режимов.
- `.cursor/skills/scenario-map-canvas/SKILL.md` — проверка смысла до записи, проверка читаемости после записи, контракт клика, поля `header.focus_node`, `modes`, `annotations`.
- `.cursor/agents/onec-scenario-map-designer.md` и `.cursor/skills/1c-agent-patterns/scenario-map-designer.md` — несколько отчётов, расхождения как кандидаты, возврат аннотаций и стартового узла.
- `fixtures/map-bad-no-insight.md` — новый плохой эталон; хороший эталон — аннотация ловушки с якорем на узел события сброса.

**Что НЕ меняется:** словарь `kind` / `relation`, порог четырёх публикуемых сущностей, запрет выдуманных рёбер, регистрация файла родителем, успех штатной кнопкой среды. ADR-0008 не заменяется: в защищаемых инвариантах нет «клик = открыть файл» и нет «смысл только из стрелок».

**Связанные ADR / KB / архив:** ADR-0008; архив `2026-08-28-scenario-map-canvas` (отмена THEN «выбор узла сразу открывает доказательство» и смена подписи полос — в `design.md` § Blast Radius). Таксономия KB в kit не заведена.

### К сведению

- Имена `header.focus_node`, `modes` и `annotations` в текущем скилле ещё нет — это новые поля манифеста, не ошибка адреса.
- При наложении полос разных слоёв на эталоне штампа ЭП в готовности задач рекомендовано не рисовать заливку и оставить имя слоя рядом с узлами; форма режима (`id`, подсветка, короткий ответ) и якорь аннотации на связь парой «откуда-куда» в задачах ещё не расписаны по полям — исполнитель допишет по сниппетам в отчёте готовности.
- Плохой эталон должен показать оба провала (вывод только в шапке и аннотация без доказательства), не один из двух.
- В скилле и обязательных пунктах шаблона остались слова «полосы уровней» — финальная сверка среза должна их вычистить вместе с остатками «клик открывает доказательство».
- Соседняя ЗНИ `overview-map-offer` в своей дельте всё ещё держит старый исход клика; при архивации позже закрытая дельта может откатить THEN в основном spec. Сверка среза это ловит, если дописать проверку активных дельт.
- Приёмка живой панели — на границе среза `S1.accept`, в проекте Документооборота; автотестов панелей в kit нет.
- Кто судит спорную формулировку вывода в шапке — по умолчанию родитель, пользователь — последняя инстанция на приёмке; старт не блокирует.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте; ровно один `S1.accept`; `<!-- slice-gate -->` есть; `form_mode: n/a`; `<!-- phase-gate -->` нет; User Task Contract DENY-grep: none; маркеров ручной конфигурации нет.
- **Layer 2 (Internal Coherence):** PASS; QC: `reports/quality-control-2026-08-29-4.md` (verdict OK, alerts: none). 13/13 Scenario покрыты (11 в `S1.accept`, 2 задачами `S1.8` / `S1.14`). Code-Truth pre-apply: WARNING `header.focus_node` / `modes` / `annotations` отсутствуют в текущем SKILL (новые поля). Precedent: INFO `precedent-documented` — ADDED→MODIFIED сценария клика и подписи полос закрыты секцией Blast Radius; ADR-0008 не Supersedes. KB Discovery пропущен (taxonomy отсутствует).
- **Layer 2.5 (Loop Detection):** PASS. `## Slice Gate Decisions` нет; `AcceptLoop(S1)=0`; `PatchRounds(S1)=2` (две секции `## Extend —`); порог 3 не достигнут.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт Requirements; каждый Requirement имеет Scenario; все 13 Scenario в `## Slices`. `scenario-implementation-leak`: none. `process-only-marker-suffix`: none (`comment_suffix` пуст, `marker_style: minimal`).
- **Layer 4 (Independent Challenge):** APPROVE; отчёт: `reports/design-challenge-2026-08-29-3.md`. Incremental: delta закрывает прежние атаки (полосы, пунктир, виды/режимы) по коду шаблона; reopen closed decisions без verified new fact не требуется. Наблюдения (пунктир не вынесен в spec; смешанный ряд без подписи) не блокируют.
- **Layer 5 (Implementation Readiness):** WARNING; отчёт: `reports/architecture-task-readiness-2026-08-29-3.md` (ГОТОВО С ЗАМЕЧАНИЯМИ). Блокирующего вопроса нет. G1–G8 — формулировки/форма данных внутри существующих задач (не CRITICAL); G6 — риск соседней дельты, не дефект этой постановки. User Task Contract OK.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

нет открытых. Closed: `infographic_meaning_carriers`, `short_map_layout_owner`.

## Источники

- `openspec/changes/scenario-map-readability-meaning/reports/quality-control-2026-08-29-4.md`
- `openspec/changes/scenario-map-readability-meaning/reports/design-challenge-2026-08-29-3.md`
- `openspec/changes/scenario-map-readability-meaning/reports/architecture-task-readiness-2026-08-29-3.md`
- алерты: `precedent-documented` (INFO), `phantom-symbol` `header.focus_node` / `modes` / `annotations` (WARNING pre-apply)
