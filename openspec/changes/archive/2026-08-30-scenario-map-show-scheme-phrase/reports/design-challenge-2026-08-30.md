---
report_type: design-challenge
generated_at: 2026-08-30
agent: onec-code-architect
mode: design-challenge
scope:
  change: scenario-map-show-scheme-phrase
  design_mtime: "2026-08-30T10:58:58.2338226+09:00"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — scenario-map-show-scheme-phrase

## Адверсариальная установка

Независимый разбор: прочитаны только `proposal.md`, `design.md`, `specs/scenario-map-canvas/spec.md`, `tasks.md`; для фактов kit — текущие тексты `.cursor/skills/scenario-map-canvas/SKILL.md`, `gate-dispatcher.mdc`, указатели explain/explore, main `openspec/specs/scenario-map-canvas/spec.md` (требование «Direct request draws the scenario map»). Отчёты `reports/architecture-*.md` как источник истины **не** использовались. Closed decisions пусты — reopen не требуется.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** короткая «покажи схему» не поднимает путь карты (cue/скилл завязаны на длинную фразу) → вместо панели рисунок в чате или разбор объекта 1С; вопрос «панель или объект» нужен только когда оба чтения ещё живы.
- **Design адресует:**
  - Why «скилл не поднимается» → две поверхности подгрузки (cue диспетчера + `description`) + якорь в Entry Protocol (Decisions 1–2, Goals 1–2).
  - Why «тот же путь, что длинная фраза» → ADDED-требование узнавания ссылается на существующее «Direct request draws…» без MODIFIED (Decision 4, Behavior Contract 7).
  - Why «не путать с объектом 1С» → явный объект во фразе = ответ без панели; вопрос только при неоднозначности; особый случай «предмет прохода сам объект-схема» (Behavior Contract 3–5, Goals 3–4).
  - Why «рисунок в чате не заменяет панель» → Behavior Contract 1 повторяет запрет замены; сам путь GenerateImage в design не перехватывается явно (опора на то, что после узнавания идёт штатный порядок скилла карты).
- **Покрытие:** **частичное**. Ядро Why (узнавание короткой фразы + коллизия с объектом 1С + ADDED вместо MODIFIED) закрыто. Слабое место: наблюдаемое условие Scenario 3 в дельте spec шире Behavior Contract п. 5 и AC1 — при ручной приёмке «смешанный ход» может конфликтовать с «голая просьба → панель сразу». Симптом «рисунок в чате» закрыт косвенно (маршрут в скилл), без отдельного запрета конкурирующего инструмента рисования.

### Q2 — Optimality

- **Выбранный путь:** SSOT узнавания в Entry Protocol; cue + `description` для подгрузки; указатели explain/explore; словарь/лексикон; вопрос только при неоднозначности; дельта ADDED (Вариант A).
- **Альтернативы из Implementation Options (кратко):** B whitelist — ломает «близкие»; C спрашивать при любом 1С-уточнении — ломает однозначный объект; D только словарь — дыра подгрузки; E MODIFIED «Direct request…» — риск затирания соседних дельт. Отклонение A→E согласовано с Why п. 5 и Impact.
- **Альтернативы, не упомянутые в `## Implementation Options`:**
  1. **Негативный cue против рисунка в чате** — в always-apply / chat-budget явно: при голой «покажи схему» в `/opsx:*` не вызывать GenerateImage / не рисовать схему markdown’ом; панель — отдельным путём. **Плюс:** бьёт прямо в симптом Why («вместо панели появляется рисунок»). **Минус:** не поднимает скилл карты сам по себе; без Entry Protocol/cue остаётся дыра «скилл не читается»; дублирует запрет «рисунок не заменяет», уже в скилле. **Почему не лучше A:** лечит симптом, не вход; без A панель всё равно не соберётся.
  2. **Машинный SSOT синонимов (fixtures/YAML + сверка задачами)** — закрытый или полузакрытый файл фраз как единственный список; Entry Protocol ссылается на файл. **Плюс:** меньше рассинхрона cue/`description`/указателей; сверка S1.5 становится diff по одному артефакту. **Минус:** противоречит Non-Goal «не whitelist»; «близкие формулировки» либо закрываются, либо файл снова размыт. **Почему не лучше A:** для kit-only с открытыми «близкими» проза Entry Protocol + якорь-пример дешевле и совпадает с Decision 1; YAML не снимает предикат неоднозначности.
  3. **Жёсткий default по типу сессии без указателей** — в explain/explore с источником голая «схема» всегда карта; вопрос только если в карточке/отчёте subject явно schema-object; правки только Entry Protocol + cue/`description`, без S1.3–S1.4. **Плюс:** меньше файлов. **Минус:** explain/explore снова расходятся с картой при эволюции формулировок; словарь «три смысла схемы» из Why/Impact не закрывается. **Почему не лучше A:** design Risks п. 2 как раз про рассинхрон — указатели оправданы.
- **Вердикт по Q2:** **оптимален** среди жизнеспособных путей для kit-only. Альтернативы 1–3 либо уже́, либо дороже без лучшего покрытия Why. Существенных сомнений по выбору A нет; сомнения — в точности контракта неоднозначности (см. Gaps), не в оси решения.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** **с оговорками**
- **Причины:**
  - **Да:** ADDED vs MODIFIED — правильный ответ на соседние дельты; Blast Radius честно формулирует `extends`, не revoke; SSOT в одном Entry Protocol без второго тела правил.
  - **Да:** предикат «явный объект 1С → без вопроса» vs «предмет прохода = схема 1С → вопрос» прямо бьёт в AC2/AC4 Why.
  - **Оговорка:** Scenario 3 («оба чтения ещё живы») без операционализации пересекается с Scenario 1 / Behavior Contract 5 — свежий ревьюер не поймёт, когда «смешанный ход» обязан спросить, а когда сразу панель; до apply это надо сузить в spec/design.

## Verdict

**CHALLENGE** — выбранный путь A решает Why и оптимальнее перечисленных альтернатив, но дельта-spec Scenario 3 и критерий «предмет прохода = объект-схема 1С» недостаточно жёсткие для однозначной приёмки AC1 vs AC3.

## Gaps for design.md

1. **implementation_invariant — Scenario 3 vs Behavior Contract 5:** в `specs/scenario-map-canvas/spec.md` Scenario «Неоднозначная просьба…» WHEN сейчас: нет имени объекта, нет слов «карта сценария», «оба чтения ещё живы». Behavior Contract п. 5 и Scenario 1 требуют: при источнике и предмете **не** объект-схема — панель **сразу**. Нужно либо (a) в Scenario 3 явно сузить WHEN до случая «предмет прохода/отчёта сам объект-схема» (тогда Scenario 3 ≈ Scenario 4) и убрать размытое «смешанный ход» без критерия, либо (b) в design.md дать **закрытый** перечень наблюдаемых признаков «оба чтения живы», совместимый с BC5 (что **не** включает «компоновка звучала раньше в теме»).
2. **implementation_invariant — операционализация «предмет прохода сам объект-схема 1С»:** в Behavior Contract / Decisions зафиксировать критерий для explain (текущая точка / объект разбора) и explore (текущий отчёт / заголовок темы), чтобы ручной прогон AC4 не гадал. Сейчас формулировка есть, измеримости нет.
3. **implementation_invariant (minor) — exit-card explain:** шаблоны `openspec-explain/templates/exit-card.md` по-прежнему предлагают только длинную «покажи карту сценария». Scope ЗНИ указатели в SKILL explain/explore + glossary/lexicon перечисляет; либо явно Non-Goal «exit-card не трогаем», либо одна фраза в Non-Goals/tasks, чтобы короткая просьба не расходилась с подсказкой «Следующий шаг».

Архитектурная развилка по коду/поведению **не** требуется: ось A держится; gaps — уточнение контракта, не смена подхода.

## Architectural alternatives

Нет равноправной развилки по наблюдаемому поведению панели. Разница негативного cue (альтернатива 1) — только побочный путь «рисунок в чате», не замена A.

## Источники

- proposal.md — `## Why`, `## What Changes` п. 1–5, Acceptance 1–4, Scope ADDED не MODIFIED
- design.md — Goals/Non-Goals, Existing Mechanisms, Behavior Contract 1–7, Implementation Options A–E, Decisions 1–7, Blast Radius, Risks 1–3, Slices S1
- specs/scenario-map-canvas/spec.md (delta) — Requirement «Show-scheme phrase is a direct request»; Scenarios 1–4
- openspec/specs/scenario-map-canvas/spec.md — Requirement «Direct request draws the scenario map» (не переписывается этой ЗНИ)
- Код/kit (verified) — `.cursor/skills/scenario-map-canvas/SKILL.md` Entry Protocol «Узнавание просьбы»; `.cursor/rules/gate-dispatcher.mdc` cue с «покажи схему»; explain/explore указатели; `exit-card.md` всё ещё только длинная фраза
