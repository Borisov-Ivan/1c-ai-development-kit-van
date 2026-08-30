---
verify_mode: pre-apply
change: scenario-map-readability-meaning
date: 2026-08-30
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
    proposal.md: "2026-08-30T00:05:09"
    design.md: "2026-08-30T00:05:31"
    tasks.md: "2026-08-30T00:18:04"
    specs/scenario-map-canvas/spec.md: "2026-08-30T00:03:46"
  last_challenge_at: "2026-08-30T00:05:31"
---

## Резюме для разработчика

scenario-map-readability-meaning — можно запускать apply. Главный вид отвечает на вопрос шапки: граф или таблица колонок.

Подправил в постановке: в задачах явно назвал все места порога и запретов содержимого.

Приёмка — живая панель после пересборки: скрыть шапку и назвать ответ. Эталон таблицы появится в ходе apply. Первую строку скилла и статью словаря кита поправьте вместе с контрактом таблицы: карта сценария — ещё и таблица колонок.

**Следующий шаг:** `/opsx:apply scenario-map-readability-meaning`

Полный отчёт: openspec/changes/scenario-map-readability-meaning/reports/verification-2026-08-30-2.md

План правит kit: шаблон панели `canvas-shell.md`, скилл `scenario-map-canvas`, роль сборщика, эталоны, дельту требований и ADR-0009. Продуктовый код 1С не меняется.

### Подправил в постановке

- В задачах второго средства, порога и сверки назвал все места скилла, где формула порога и запрет полотна без связей ещё графовые.

### К сведению

- Первая строка скилла, «Назначение», различение имён в Guardrails и статья «Карта сценария» в словаре кита всё ещё говорят «панель со связями»; поправить вместе с контрактом таблицы.
- В Decision 13 ссылка на смену средства при провале бюджета указывает на пункт 10 Behavior Contract; правило бюджета — в пункте 11 (одна цифра).
- Соседние скиллы предложения карты (`openspec-explain`, `openspec-overview`) держат графовую формулу порога; вне охвата этой ЗНИ: на предложении таблицы не срабатывают.
- После эталона таблицы фразу «в скилле образца без рёбер нет» переписать на «хорошего образца списка без рёбер нет».
- При переписывании запретов содержимого удержать «таблица шагов без вывода — не карта».

## Что меняется в постановке

**Расширение / конфигурация:** kit (скилл карты, шаблон панели, роль сборщика, эталоны, ADR-0009). Продуктовый код 1С не меняется.

**Точки изменения:** шаблон панели (полосы по слою, легенда, скрыть шапку, бюджет, таблица, аннотация у якоря); скилл (предикат смысла, `header.medium`, порог по средству); роль сборщика; эталоны графа, таблицы и «полотно без смысла».

**Что НЕ меняется:** регистрация файла родителем, успех штатной кнопкой среды, словарь `relation`, порог четырёх публикуемых сущностей, запрет выдуманных рёбер, модель сборщика, пять инвариантов ADR-0008.

**Связанные ADR / архив:** ADR-0008 (пять инвариантов), ADR-0009 (главный вид отвечает на вопрос шапки), архив `2026-08-28-scenario-map-canvas`.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте; ровно один `S1.accept`; `<!-- slice-gate -->` есть; `form_mode: n/a`; `<!-- phase-gate -->` нет; UTC DENY-grep none.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-30-3.md` (verdict OK, alerts: none). 18/18 Scenario; 8b Pass; критерий 10 — один осмотр. Precedent: `precedent-documented` (Blast Radius в design и ADR-0009). Code-truth: kit-only, `openspec/project.md` отсутствует, символов BSL нет.
- **Layer 2.5 (Loop Detection):** PASS. Петля закрыта `reports/architecture-loop-redesign-2026-08-30.md` позже последней `awaiting-acceptance`. Повторный deep-analysis не запускался.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт; у каждого Requirement есть Scenario; implementation-leak не найден.
- **Layer 4 (Independent Challenge):** APPROVE. Отчёт: `reports/design-challenge-2026-08-30-2.md`. G1–G3 закрыты; ось не менялась. `design.md` после APPROVE не менялся (repair attempt 2 — только `tasks.md`).
- **Layer 5 (Implementation Readiness):** WARNING. Отчёт: `reports/architecture-task-readiness-2026-08-30-3.md`. Пробелы порога и графоцентричных норм скилла закрыты расширением S1.24 / S1.26 / S1.20. Остаток: словарь кита и вводные строки скилла («панель со связями») — недостающие ссылки, не нереализуемая задача; apply правит вместе с контрактом таблицы.

### Repair Loop

- attempt 1: контракт `header.medium`, таблица D12, порог S1.26, предикат манифеста, смешанное содержание, бюджет.
- attempt 2: расширены перечни мест в S1.20, S1.24, S1.26.
- Decision blockers: нет.
- residual L5: WARNING (glossary / intro lines).

### Авто-исправлено (Layer 1)

mechanical-замечаний не обнаружено

## Источники

- `reports/quality-control-2026-08-30-3.md`
- `reports/design-challenge-2026-08-30-2.md`
- `reports/architecture-task-readiness-2026-08-30-3.md`
- `reports/architecture-loop-redesign-2026-08-30.md`
- алерты: L5 WARNING glossary/intro; `precedent-documented`
