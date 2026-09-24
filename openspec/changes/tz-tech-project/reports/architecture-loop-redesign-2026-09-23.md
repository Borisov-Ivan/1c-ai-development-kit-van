---
report_type: deep-analysis
generated_at: 2026-09-23
agent: onec-code-architect
mode: deep-analysis
scope:
  change: tz-tech-project
  slices: [S1]
  files:
    - openspec/changes/tz-tech-project/debug.md
    - openspec/changes/tz-tech-project/proposal.md
    - openspec/changes/tz-tech-project/design.md
    - openspec/changes/tz-tech-project/tasks.md
    - openspec/changes/tz-tech-project/specs/tz-tech-project/spec.md
  modules: []
  capabilities: [tz-tech-project]
related_reports:
  - reports/verification-2026-09-23.md
  - reports/verification-2026-09-23-2.md
  - reports/verification-2026-09-23-3.md
  - reports/verification-2026-09-23-4.md
  - reports/design-challenge-2026-09-23.md
  - reports/design-challenge-2026-09-23-2.md
  - reports/design-challenge-2026-09-23-3.md
  - reports/architecture-extend-coherence-2026-09-23.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Deep Analysis — петля приёмки S1 (tz-tech-project)

## Вводные аудита

| Поле | Значение |
|------|----------|
| Срез | S1 (единственный) |
| S1.accept | `[ ]` — приёмка не подписана |
| Slice Gate Decisions | нет |
| AcceptLoop(S1) | 0 |
| PatchRounds(S1) | 5 (порог 3) |
| Приёмка на ИБ | не начиналась |
| Характер раундов | уточнения постановки до apply (`--from-verify` + брифы заказчика) |
| Closed decisions | EC-1 / EC-2 / EC-3 (verified user answer 2026-09-23) — **не переоткрывать** |

Источники истины этого аудита: `debug.md` (Extend + Verify decision ledger + External Contract Ledger), `proposal.md`, `design.md`, `tasks.md`, `specs/tz-tech-project/spec.md`. Файлы `reports/architecture-*.md` и challenge/verify упомянуты **только как след раундов**, не как доказательство текущего контракта.

## Task

Ответить: корень петли один или это N независимых уточнений? Выбрать **consolidation** (собрать срез заново) или **minimum** (оставить текущий текст, больше не патчить до приёмки).

## Complexity

Medium — один срез, без кода 1С; ось риска — когерентность постановки после 5 патчей, не архитектура модулей.

## Вердикт

**Корень один (неполная поверхность приёмки), проявившийся как 5 инкрементов по двум осям. Рекомендация: minimum — не пересобирать S1; стоп патчей до первой приёмки на файле задания.**

## Анализ корня

### Что фиксируют пять Extend

| # | Источник (debug.md) | Тема патча | Ось |
|---|---------------------|------------|-----|
| 1 | repair-from-verify attempt 1 | имена `<имя>-*.md`, форма пункта листа, дыра по имени в cf, часы из прозы, шаблон не второй источник | каркас выхода + зачатки часов |
| 2 | repair-from-verify attempt 2 | ≥2 варианта у вопроса; часы = нижняя × коэффициент; надбавка за названный фактор; сохранение ответов; шаблон не runtime | лист + формула часов (черновик) |
| 3 | бриф заказчика, вариант 1 | **два последовательных вывода**; надбавка **после** умножения; техпроект «по просьбе» (тогда); пустой лист = «вопросов нет» | **триггер/поток** + уточнение формулы |
| 4 | бриф заказчика, вариант 2 | дробь часов **вверх** до целого | формула часов |
| 5 | ответ verify, вариант A | техпроект по **подтверждению в листе**, не по просьбе; часы формула зафиксирована | **триггер** + закрепление формулы |

### Один корень vs N независимых

**Не N независимых дефектов продукта.** Пять записей — не пять разных «багов среза», а последовательное доопределение одной пользовательской цели из `proposal.md` ## Why («сначала вопросы/согласование часов, после согласования — каркас техпроекта») без готового Behavior Contract на двух осях:

1. **Ось trigger (EC-1):** когда появляется `<имя>-техпроект.md`  
   - след: «оба файла сразу» (отказ two-phase в Extend 2) → «два шага, техпроект по просьбе» (Extend 3) → «по подтверждению в листе» (Extend 5 / EC-1).  
   - Это **одна ось**, три формулировки подряд, не три независимые фичи.

2. **Ось visible-result / часы (EC-2, EC-3):** как считать часы из прозы  
   - след: «собрать из прозы» (Extend 1) → нижняя × коэффициент + фактор (Extend 2) → надбавка **после** коэффициента и не умножается (Extend 3 / EC-2) → округление вверх (Extend 4 / EC-3).  
   - Это **одна формула**, доопределяемая по слоям, не четыре независимых правила из разных доменов.

Сопутствующие правки Extend 1–2 (имена файлов, форма пункта, дыры, сохранение ответов, шаблон не SSOT) — **каркас той же поверхности приёмки**, без которого сценарии S1 непроверяемы. Они не образуют отдельный «корень №2», а заполняют пробелы, которые verify вскрывал до закрытия EC.

**Итог классификации:** один корень = **недоспецифицированный контракт приёмки S1 на осях trigger + hours** до первого apply. Пять патчей — N **инкрементов обнаружения** этого корня, кластеризуемых в 2 оси (не в 5 независимых уточнений и не в один атомарный баг).

### Closed decisions — статус в живых артефактах

Проверено по текущим `proposal.md` / `design.md` (D1, D3, Behavior Contract, «Решения verify») / `tasks.md` (S1.2, S1.6, S1.9, S1.accept) / `spec.md` (Requirement + scenarios «Согласование часов», «Техпроект…», «Часы собраны из прозы»):

| ID | Контракт | Живые артефакты | Переоткрытие |
|----|----------|-----------------|--------------|
| EC-1 / second-step-confirmation | техпроект после подтверждения в листе; согласование на 1-м запуске сразу | согласованы | запрещено без нового verified fact |
| EC-2 / hours-surcharge-after-coefficient | `(нижняя × коэфф.) + надбавка`; надбавка на коэфф. не умножается | согласованы | запрещено |
| EC-3 / hours-round-up | дробь вверх до целого; целое не трогать | согласованы | запрещено |

Журнальная строка Extend (3) в `debug.md` всё ещё описывает тогдашнее «только по этой просьбе» — это **историческая запись раунда**, не текущий контракт; Extend (5) явно supersede’ит триггер. Противоречия между живыми proposal/design/tasks/spec по EC-1/2/3 **не найдено**.

### Почему порог PatchRounds=5 сработал, а AcceptLoop=0

Петля шла **до apply и до ИБ**: verify/challenge → repair постановки → снова verify. Приёмка среза (`S1.accept`) ни разу не запускалась, поэтому это не «зацикленная приёмка после реализации», а **переразметка Behavior Contract**. Порог 3 на PatchRounds справедливо поднял redesign-аудит; он не означает автоматически, что живой текст сейчас противоречив.

## Simplicity Check

- **Viable alternatives:**
  1. **Consolidation** — переписать S1 «с чистого листа»: один Behavior Contract с EC-1/2/3, пересобрать tasks/spec/proposal вокруг того же смысла, обнулить шум journal/старых формулировок в голове оркестратора.
  2. **Minimum** — оставить текущие proposal/design/tasks/spec как есть; запретить новые `--from-verify` патчи S1 до Primary acceptance на реальном файле задания; journal Extend оставить историей.
  3. **Гибрид «лёгкая гигиена»** — minimum + точечная правка только явных leftover-фраз вне EC (если найдутся). Сейчас leftover в живых артефактах нет → гибрид **не нужен**.

- **Selected simplest viable design:** **Minimum (вариант 2).**

- **Why not simpler / why not consolidation:**
  - Ещё проще «ничего не решать» нельзя: порог 5>3 требует явного стоп-условия, иначе verify снова потянет Extend.
  - Consolidation **не упрощает наблюдаемое поведение** (семантика уже = EC-1/2/3) и **увеличивает** риск регресса формулировок при переписке пяти файлов без новой информации от заказчика или кода.
  - Пересборка была бы оправдана при живых противоречиях proposal↔design↔spec↔tasks; проверка файлов такого противоречия не показывает.

- **Complexity budget (если выбрать minimum):**
  - Files touched: **0** (сейчас)
  - Hooks/intercepts: 0 (вне кода 1С)
  - New procedures/functions: 0
  - Conditional branches / feature flags: 0
  - Дополнительных Extend до приёмки: **0** (жёсткий стоп)

- **Complexity budget (если выбрать consolidation):**
  - Files touched: 4–5 (proposal, design, tasks, spec, возможно debug hygiene)
  - Semantic delta vs EC: **≈0**
  - Риск: повторное открытие уже закрытых осей через перефраз

## Chosen Approach

**Approach:** Minimum freeze постановки S1.

**Rationale:**
- Корень = одна недоспецифицированная поверхность приёмки; она **уже закрыта** тремя customer-direct EC в ledger.
- Живые артефакты согласованы с EC-1/2/3.
- Приёмка на ИБ не начиналась — следующий сигнал должен прийти от прогона команды, не от очередного challenge без кода.
- Consolidation даёт косметическую ясность ценой повторного риска рассинхрона; при текущей когерентности это over-engineering процесса, не продукта.

## Found Patterns (процесса постановки)

### Pattern P1: Repair до apply вместо Slice Gate

- **Where:** `debug.md` ## Extend — (1)…(5); S1.accept = `[ ]`
- **Usage:** пять правок tasks/spec/design без подписанной приёмки и без Slice Gate Decisions
- **Evidence:** секции Extend в `debug.md`; чеклист в `tasks.md` / `design.md`
- **Confidence:** high
- **Applicability:** после freeze — только apply → приёмка; новый Extend только при конфликте с EC или новым verified user answer

### Pattern P2: Ось триггера уточнялась трижды одной темой

- **Where:** Extend (2) disposition `two-phase-output rejected` → Extend (3) `two-sequential-outputs accepted` + «по просьбе» → Extend (5) confirmation / EC-1
- **Evidence:** `debug.md` строки disposition Extend 2, 3, 5; текущий `design.md` D1
- **Confidence:** high
- **Applicability:** не переоткрывать форму «просьба vs подтверждение» без нового факта

### Pattern P3: Формула часов наращивалась слоями

- **Where:** Extend 1→2→3→4 (+ закрепление в 5); EC-2, EC-3
- **Evidence:** `debug.md`; `design.md` D3; `spec.md` Scenario «Часы собраны из прозы»
- **Confidence:** high
- **Applicability:** формула считалась incomplete contract, не отдельными багами

## Assumptions

- **A1:** Оркестраторные факты (Slice Gate нет, AcceptLoop=0, PatchRounds=5, приёмка ИБ не начиналась) верны.  
  - **Confidence:** high (согласуются с `tasks.md` S1.accept `[ ]` и пятью секциями Extend).  
  - **Verification:** при расхождении — пересчёт по `debug.md` / чеклисту.

- **A2:** Закрытые решения 2026-09-23 остаются авторитетом заказчика.  
  - **Confidence:** high (`authority: customer-direct`, `confirmation: confirmed` в ledger).  
  - **Verification:** только новый verified user answer / код после apply.

## Open Questions

Нет. Блокеров для выбора minimum нет.

## Gaps (не требуют consolidation)

1. **Журнал Extend (3)** в `debug.md` исторически содержит «по просьбе» — читатель может спутать с текущим контрактом. Это шум журнала, не дефект design/spec. При minimum **не править**, пока оркестратор опирается на ledger + § «Решения verify».
2. Старые `reports/verification-*-4.md` / challenge отражают состояние «до EC» — след раундов; не использовать как SSOT.

## Recommendation (для оркестратора)

1. **Принять minimum:** не запускать consolidation S1; не писать новый `--from-verify` Extend по косметике.
2. **Стоп-условие патчей:** до Primary `S1.accept` на прогоне `/opsx:techproject` по одному файлу задания — только verify/apply без правки постановки, кроме нового `confirmed_by: user` / verified code fact, конфликтующего с EC.
3. **Не переоткрывать** EC-1, EC-2, EC-3.
4. **Consolidation отложить** до случая, когда живые proposal/design/tasks/spec снова разойдутся или заказчик даст новый контракт на той же оси.
5. Следующий полезный ход процесса: **apply / реализация** (или pre-apply verify без repair, если ещё не GO), затем приёмка S1 — не шестой патч текста.

## Knowledge conflicts

Секции `## Existing Knowledge` во входе не было — N/A.

## Источники

- `openspec/changes/tz-tech-project/debug.md` — Verify decision ledger, External Contract Ledger, Extend (1)–(5)
- `openspec/changes/tz-tech-project/proposal.md` — Why, What Changes, Acceptance Criteria
- `openspec/changes/tz-tech-project/design.md` — D1–D5, Behavior Contract, Решения verify, Slices
- `openspec/changes/tz-tech-project/tasks.md` — S1.1–S1.9, S1.accept
- `openspec/changes/tz-tech-project/specs/tz-tech-project/spec.md` — ADDED Requirements + scenarios
- След раундов (не SSOT): `reports/verification-2026-09-23*.md`, `reports/design-challenge-2026-09-23*.md`, `reports/architecture-extend-coherence-2026-09-23.md`
