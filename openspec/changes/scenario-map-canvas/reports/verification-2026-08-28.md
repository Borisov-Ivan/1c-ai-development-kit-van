---
verify_mode: pre-apply
change: scenario-map-canvas
date: 2026-08-28
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: FAIL
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: WARNING
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: WARNING
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
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
  closed_decisions: []
  open_decision_id: direct_request_linear_publish
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - direct_request_linear_publish
    - inventory_card_offer_before_walk
    - accepted_offer_missing_scenario
    - cartographer_primary_slug
    - merge_cartographer_into_causal_slice
  artifacts_mtime:
    proposal.md: "2026-08-28T01:27:08Z"
    design.md: "2026-08-28T01:28:24Z"
    tasks.md: "2026-08-28T01:29:54Z"
    specs/scenario-map-canvas/spec.md: "2026-08-28T01:27:08Z"
  last_challenge_at: "2026-08-28T01:28:24Z"
---

## Резюме для разработчика

scenario-map-canvas — до старта нужен ваш выбор по логике прямой просьбы «покажи карту».

**Что решить: строить ли схему, если шаги идут цепочкой без ветвлений и разных уровней**

Постановка требует и «по просьбе нарисовать», и «на панели видны разные уровни или ветки». Если разработчик просит карту по четырём шагам подряд, одно правило говорит «рисуй», другое — «такой столбик публиковать нельзя». Пока это не закрыто, первая просьба может дать либо запрещённый список со стрелками, либо тупик: строить обязан, показать нельзя.

- **A. Та же планка, что у предложения** — схема только если есть ветка или разные уровни; иначе в чате одна строка, чего не хватает. Просьба не обещает картинку на любой цепочке.
- **B. Просьба сильнее предложения** — при достаточных сущностях панель всегда; линейная цепочка рисуется как цепочка с подписями на связях. Пользователь всегда получает схему, но она иногда будет «столбиком».

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify scenario-map-canvas`.

Полный отчёт: openspec/changes/scenario-map-canvas/reports/verification-2026-08-28.md

План правит скилл `.cursor/skills/scenario-map-canvas/SKILL.md`, строку в `gate-dispatcher.mdc`, шаблоны разбора и исследования, таблицу ролей и новый файл агента картографа. Продуктовый BSL не меняется. Первый срез уже в коде кита (узлы с доказательством по просьбе); приёмка этого среза ещё не подписана.

## Решения до apply

### Рекомендации

- **Прямая просьба и линейная цепочка:** зафиксировать исход A или B (карточка ниже). Без этого приёмка «первая просьба даёт схему» неоднозначна.
- **Регистрация картографа отдельной приёмкой:** сверка файла агента и указателей — не пользовательский исход. После выбора по просьбе внутренний ремонт перенесёт эти задачи в срез «карта показывает причинность» и снимет отдельную подпись.
- **Просьба при числе сущностей ниже порога:** в чеклисте второго среза нет наблюдаемого отказа одной строкой; дописать вместе с порогом по сущностям, не по шагам рассказа.
- **«Сразу карту» до первой карточки разбора:** в строке подтверждения списка имён ещё нет доказательств; смысл согласия не выбран. Чинится после A/B (убрать вариант или описать режим прохода).

### Развилки

#### 1. Когда прямая просьба встречает линейную цепочку

**Цель ЗНИ:** панель показывает причинность и уровни, а не столбик шагов; первая просьба не уходит в плоский текст.

**Что в коде сейчас.** Скилл карты (состояние после первого среза) отдаёт узлы «эффект + доказательство». Дельта spec обязывает по прямой просьбе построить панель, если доказанных сущностей не меньше четырёх, и одновременно требует на панели не меньше двух уровней либо ветку со схождением; список без связей публиковать нельзя; текстовый резерв — только при техническом отказе среды.

**Что предлагает план.** Снять предикат «панель уже открыта», рисовать схему со связями, предлагать её из исследования и разбора по форме связей.

**Почему это развилка.** Независимый разбор: для четырёх сущностей подряд исход не определён — строить обязан, публиковать как столбик нельзя, резерв запрещён, одна строка причины описана только для «сущностей меньше четырёх».

**Варианты решения.**

- **A. Та же планка, что у предложения** — просьба проходит те же условия, что намёк: хватает публикуемых узлов **и** есть ветка или разные уровни; иначе панели нет и в чате одна строка. **Компромисс:** часть просьб получит отказ вместо картинки.
- **B. Просьба сильнее предложения** — при достаточном числе сущностей панель всегда; требование «уровни или ветка» относится к раскладке (линейная цепочка — подписанные связи). **Компромисс:** пользователь всегда видит схему, но она может быть столбиком.

**Влияет на:** что разработчик увидит, сказав «покажи карту сценария» на простом последовательном разборе.

**Что изменится после выбора.** В spec и design появится один исход для просьбы без ветвлений; задачи второго среза и скилл карты будут сверкаться с ним.

**Источники** *(техническое):* design-challenge-2026-08-28.md Gaps 1, Architectural alternatives «Критерий публикации»; spec Direct request vs Causal map vs Node contract.

## Что меняется в постановке

**Расширение / конфигурация:** kit (`.cursor/`, `openspec/`), продуктовый BSL не меняется.

**Точки изменения:**

- `.cursor/skills/scenario-map-canvas/SKILL.md` — контракт шапка / узлы / связи / виды; создание файла панели с нуля; проверка, когда схему предлагать.
- `.cursor/rules/gate-dispatcher.mdc` — три входа: просьба, принятое предложение, намёк на существующей строке.
- `.cursor/skills/openspec-explain/` и `.cursor/skills/openspec-explore/SKILL.md` — вариант схемы в уже существующих строках решения.
- `.cursor/agents/onec-scenario-map-designer.md` и `.cursor/rules/model-selection.mdc` — роль, которая рисует макет; политика модели как у остальных ролей.
- `.cursor/docs/chat-lexicon.md`, `openspec/glossary.md` — три имени: карта точек, карта сценария, текстовый резерв.

**Что НЕ меняется:** отдельной команды карты нет; без просьбы и без принятого предложения панель сама не появляется; `opsx-output-style.md` и `brief-card.md`; прикладная конфигурация 1С; карта на `/review` и на этой команде проверки — вне этой ЗНИ.

**Связанные ADR / KB / архив:** ADR-0001 (формулировки в чат — продуктовые); ADR-0002 (карту не подмешивать в бриф Охвата разбора); ADR-0006 (короткие статусы по-русски); архив `explain-after-review-apply-scope`. Таксономия KB в kit отсутствует. Blast Radius в design относительно уже сделанного первого среза этой ЗНИ.

### К сведению

- Приёмка первого среза ещё не подписана; рабочие задачи этого среза уже отмечены сделанными.
- Follow-up про критерии отключения карты — вне срезов, не мешает старту после закрытия развилки.
- `form_mode: n/a`; маркеров ручной конфигурации 1С нет.
- Имя секции журнала «Схема (текстовый резерв)» уже есть в задачах второго среза; открытый вопрос design №1 можно снять после правок.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте, `<!-- slice-gate -->` закрыт на S1/S2/S2b/S3, fences сбалансированы. Info: Follow-up без префикса среза; `form_mode: n/a`.
- **Layer 2 (Internal Coherence):** FAIL. QC: `reports/quality-control-2026-08-28.md` — CRITICAL `slice-not-vertical` + `slice-foundation-with-gate` (S2b grep-Primary + gate, потребитель S3). WARNING: `accept-bullets-missing-scenario` («Просьба при числе сущностей ниже порога»); `rework-risk-unaccepted-predecessor` (S2 переписывает SKILL.md при `S1.accept` = `[ ]`). User Task Contract: none. 8b self-achievable: Pass (S1 vs S2 Then различаются).
- **Layer 2.5 (Loop Detection):** PASS. S1.accept `[ ]`; AcceptLoop(S1)=1 (awaiting-acceptance); PatchRounds(S1)=2 (`## Extend —` 2026-08-27 и 2026-08-28). max=2 < acceptance_loop_max=3. S2/S2b/S3 без awaiting-acceptance.
- **Layer 3 (Problem-Solution Trace):** WARNING. Why (три провала) покрыт requirements. У каждого Requirement есть Scenario. implementation-leak в THEN нет. `comment_suffix` пустой. Нет Scenario «принятое предложение → панель» (вход D5.2); финал исследования с блоком постановки ЗНИ вытесняет «Дальше» — в design не оговорено. scenario-orphan-accept: порог ниже четырёх сущностей.
- **Layer 4 (Independent Challenge):** CHALLENGE. Отчёт: `reports/design-challenge-2026-08-28.md`. Ось (молчание, нет команды, создание с нуля, предложение по форме связей, роль с общей политикой модели) не отменяется. Classifier: одна развилка в чат (`direct_request_linear_publish`); прочие gaps — implementation_invariant / вторая развилка «сразу карту» отложена (mixed: decision first). `last_challenge_at` обновлён (CHALLENGE в чат).
- **Layer 5 (Implementation Readiness):** WARNING. Отчёт: `reports/architecture-task-readiness-2026-08-28.md` — ГОТОВО С ЗАМЕЧАНИЯМИ. GAP: порог в скилле остаётся «по узлам»; эталон-список в скилле; переименование секции журнала не во всех файлах; Primary-слаг картографа не выбран; словарь kind/relation/view.type; MUST NOT предложения без адресной задачи. Ручных маркеров конфигурации не найдено. User Task Contract: OK.

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

Не запускался: смешанный отчёт, приоритет decision. После ответа пользователя — user-extend `--from-verify` (ремонт S2b + gaps Layer 5 + остаток Layer 4).

### Развёрнутые карточки развилок

`open_decision_id: direct_request_linear_publish` — см. «Решения до apply» §1.

Отложены (не в чат): merge S2b→S2 (repair после ответа); inventory-card «сразу карту» (вторая развилка Layer 4); Primary-слаг картографа.

## Источники

- `openspec/changes/scenario-map-canvas/reports/quality-control-2026-08-28.md`
- `openspec/changes/scenario-map-canvas/reports/design-challenge-2026-08-28.md`
- `openspec/changes/scenario-map-canvas/reports/architecture-task-readiness-2026-08-28.md`
- алерты: `slice-not-vertical`, `slice-foundation-with-gate`, `accept-bullets-missing-scenario`, `rework-risk-unaccepted-predecessor`
