---
report_type: plan-review
generated_at: 2026-08-30
agent: onec-code-architect
mode: plan-review
review_mode: peer
scope:
  change: kit-review-hygiene
  slices: [S1, S2, S3, S4, S5]
  files:
    - .cursor/skills/openspec-apply-change/SKILL.md
    - .cursor/skills/openspec-overview/SKILL.md
    - .cursor/skills/openspec-status/SKILL.md
    - .cursor/docs/glossary.md
    - .cursor/docs/delivery-integrity.md
    - .cursor/rules/session-discipline.mdc
    - .cursor/rules/gate-dispatcher.mdc
    - .cursor/skills/openspec-new-change/SKILL.md
    - .cursor/skills/context-strategy/SKILL.md
    - .cursor/agents/onec-scenario-map-designer.md
  modules: []
  capabilities:
    - kit-project-neutrality
    - chat-surface-clarity
    - scenario-map-canvas
    - always-apply-context-budget
    - delegation-safeguards
related_reports: []
confidence: high
open_questions_count: 0
superseded_by: null
---

# Plan Review (peer) — kit-review-hygiene

## KB references

Каталога `openspec/knowledge/` нет; discovery пуст. Ссылок на KB-факты нет.

## Адрес ревью

Проверка `design.md` относительно `proposal.md`, архивных контрактов last-slice и overview-map-offer, ADR-0009 / ADR-0001 и текущего текста kit. Кода 1С нет. Правки прикладной конфигурации не предлагаются. Архив `openspec/changes/archive/**` не предлагается править. Allow-list AP-031 (`pav_` / `lvv_` / `пр_`) не предлагается сужать.

## Verdict for orchestrator

Chosen **вариант A** — самый простой исполнимый путь: сегменты `cf`/`cfe` в путях **этой** ЗНИ, один нейтральный словарь примеров, точечные правки протокола. Развилку last-slice (три слова vs архив без предрелиза) design **не** переписывает — меняется детектор и ярлык `cf-ea` → `cf`. Переписывать срезы не нужно.

Перед apply в `design.md` закрыть три уточнения секций (ниже). Это не смена Chosen и не развилка по коду 1С.

---

## Design Rationale

Why поставки: в чужой проект уезжают имена чужой выгрузки (фильтр охвата + учебные литералы); порог схемы после описания считает «оба отсева», хотя главное средство уже может быть таблицей; скилл читается на каждом ходе; битая ссылка и несуществующий режим инструмента.

Chosen A адресует **именно** эти боли:

| Why | Design |
|---|---|
| Фильтр зашит путями одной выгрузки | Классификатор по сегментам `/cf/` `/cfe/` в путях задач; ярлык `cf` |
| Учебные эталоны несут те же имена | Один словарь `src/Конфигурация/cf/` · `cfe/ДемоРасширение/` · `sample-change` · `ext_` |
| Порог описания = «оба отсева» | Порог ≥4 по правилам выбранного средства (ADR-0009) |
| Согласие и «соседняя ЗНИ» | Тот же один отчёт; фраза про соседа уходит, «все пути» не включаются |
| Повторный Read скилла | Read только на входе сессии; протокол на каждом ходе без Read |
| Битая ссылка / `explore/fast` / полный Read скилла картографом | Точечный ремонт ссылок и fallback |

Вариант B (overlay `project.md` как allow-list фильтра) **не** закрывает эталоны и при наивном чтении «если в карточке есть cfe — scope = cfe» дал бы ложный `mixed` на kit-only ЗНИ в проекте с расширениями. Вариант C (комментарий «замените») не мешает утечке при копировании `.cursor/`.

Это `extends` к архиву last-slice (тот же смысл развилки) и overview-map-offer (один отчёт, панель только по согласию). Не `revokes`. ADR не создаём: повтор ADR-0009 на входе описания; нейтральность — гигиена поставки.

## Existing Mechanisms

Проверено по текущим файлам (не по памяти design):

1. **Классификатор apply** (`.cursor/skills/openspec-apply-change/SKILL.md` ~121–132, ~423–424): Grep `tasks.md` и при необходимости `design.md` на `src/.../*.bsl`; литералы `src/ЭДО и ЭА/cf/`, `src/ЭДО ПАО/cfe/`, `src/ДО3 Демо/cfe/`; ключ `cf-ea`; last-slice: `cfe`/`mixed` → три слова; пусто/`cf-ea` → архив без `ревью`. **Расширяем алгоритм и ярлык, не формулировку трёх слов.**
2. **Статус** (`.cursor/skills/openspec-status/SKILL.md` ~40–43): scope-ключ ещё `cf-ea`, preview-транспорт уже `cf`. Свести ключ к глоссарию.
3. **Глоссарий** (`.cursor/docs/glossary.md` `marker_scope`): уже `cf | cfe | mixed | не определён`. Apply/status отстают — цель S1.
4. **Пути проекта** (`.cursor/rules/project-paths.mdc`): SSOT корней — таблица `openspec/project.md`; строки с `/cf/` и `/cfe/`. В репо kit файла нет. Правило **запрещает** считать умолчание `src/cf/` — сегментный детектор это соблюдает (не хардкод корня, а сегмент в фактическом пути).
5. **Карта** (`.cursor/skills/scenario-map-canvas/SKILL.md` шаги 2–4, § «Молчание и пороги»): узел без доказательства отсеять всегда; узел без инцидентной связи — только граф; таблица связь не требует; порог ≥4 после отсева **выбранного средства**. Overview (~150–160) ещё пишет «после обоих отсевов» и «связанных сущностей» + фразу про соседнюю ЗНИ. S2 выравнивает описание с скиллом карты, не с архивным текстом «оба отсева».
6. **Сессия:** always-apply `session-discipline.mdc` D5 сейчас требует FIRST AND ONLY Read скилла **на каждом ходе**; Persistence уже требует протокол без «свободного режима». Страховка обрезки в always-apply есть, имён карточек verify нет; они живут в on-demand `command-skill-gate.mdc` (agent-only: `executive-summary` / `info-section` / `layer-1-hygiene-table`). S3: Read только вход; имена карточек — в always-apply (ADR-0001: в чат не копировать).
7. **Cue карты:** `gate-dispatcher.mdc` строка «покажи схему» → путь скилла карты. Не копировать тело протокола.
8. **Битая ссылка:** `openspec-new-change/SKILL.md` ~350: `see openspec-quality-controller.md` — файла с таким относительным именем нет. Рабочие цели: `.cursor/skills/1c-agent-patterns/quality-controller.md` (шаблоны) и `.cursor/agents/openspec-quality-controller.md` (роль).
9. **`explore/fast`:** `.cursor/skills/context-strategy/SKILL.md` ~71–72. В enum `Task.subagent_type` режима `fast` нет — `explore`.
10. **Картограф:** `.cursor/agents/onec-scenario-map-designer.md` сейчас `Read` всего `scenario-map-canvas/SKILL.md` до ответа. Goal 4 постановки: не читать скилл карты целиком.
11. **Last-slice main spec** (`openspec/specs/chat-surface-clarity/spec.md`, Requirement last-slice): условие — «код расширения», не ярлык выгрузки. Design сохраняет WHEN/THEN.
12. **AP-031:** allow-list `pav_`/`lvv_`/`пр_` в `.cursor/docs/antipatterns/bsl-antipatterns.md` ~1702 — механизм LIST. Вне scope, verified.

## Simplicity Check

- **Viable alternatives:**
  1. **A (Chosen)** — сегменты пути в Grep задач/design; нейтральный словарь; точечный протокол. Файлы: markdown `.cursor/**`. Хуков 1С: 0.
  2. **B** — allow-list корней в `project.md`; kit без overlay молчит. Не чинит эталоны; риск ложного `cfe`/`mixed` на kit-only, если карточку читать как «в репозитории есть расширение».
  3. **C** — литералы + комментарий «замените». Утечка при копировании `.cursor/` остаётся.
- **Selected simplest viable:** A. Без нового overlay, без смены развилки, без правки AP-031.
- **Why not simpler:** ещё проще = оставить литералы (C) — не закрывает Why. Слить S4+S5 в один срез смешает «ссылка открывается» и «Grep утечки = 0» — разные пользовательские исходы. Слить S5 в S1 сделало бы foundation из замены имён в файлах, которых S1 не касается.
- **Complexity budget:**
  - Files touched: десятки markdown в `.cursor/**` (S5 — широкая замена литералов; протокол — узкий)
  - Hooks/intercepts: 0
  - New procedures/functions: 0
  - Conditional branches / feature flags: 0 (кроме уже существующей развилки last-slice)

Only one viable option для **детектора в kit без `project.md`**: сегменты `cf`/`cfe` (тот же предикат, что `project-paths.mdc`). Overlay (B) и комментарий (C) Why не закрывают.

---

## Полнота

Покрыты все пять пунктов What Changes. Non-Goals соблюдены (соседние ЗНИ не принимать; потолок карты / оболочка панели / AP-031 / archive/** / `.bsl` — вне).

Пробелы (не блокеры Chosen, правки текста design):

1. **BC1 vs текущий Grep-набор.** Сейчас apply/status: `tasks.md` + `design.md`. BC1 пишет «задач и постановки». Архивный last-slice: «код расширения в путях **задач**». Постановка (`proposal.md`) не должна становиться третьим источником без нужды; `design.md` нельзя молча выкинуть — иначе ЗНИ, где пути BSL ещё только в design, потеряет шаблоны маркеров.
2. **BC1 vs «карточка проекта».** Proposal/EM говорят «из карточки, если есть». BC1 карточки не использует. Нужна явная граница: `project.md` **не** задаёт `marker_scope` фактом наличия каталога cfe в репозитории; scope — только пути **этой** ЗНИ. Иначе kit-only в чужом проекте с расширениями получит три слова ревью.
3. **S4 — целевой href.** «Ссылка открывается» без пути: указать `.cursor/skills/1c-agent-patterns/quality-controller.md` (это тот файл, на который new-change опирается как на шаблон делегирования).
4. **Чеклист поставки в S1.** `delivery-integrity.md` сейчас **не** содержит литералов ЭДО. Пункт S1 в чеклисте = «фильтр охвата без путей заказчика», не «Grep утечки = 0» (это Primary S5). Иначе S1 украдёт приёмку S5.

## Корректность (verified facts)

| Утверждение design | Факт | Статус |
|---|---|---|
| Три пути-литерала в apply | SKILL.md 122–123 | confirmed |
| Last-slice ветка `cf-ea` | SKILL.md 423–424 | confirmed |
| Глоссарий уже `cf` | glossary.md:37 | confirmed |
| Overview: оба отсева + соседняя ЗНИ | overview SKILL.md 142–160 | confirmed |
| Карта: отсев по средству | scenario-map-canvas SKILL.md 53–57, 158, 164, 175 | confirmed |
| `/cfe/` не содержит `/cf/` как сегмент | `/cfe/` = `/cf` + `e/`; предикат `/cf/` требует слэш после `f` | confirmed |
| D5 Read на каждом ходе | session-discipline.mdc 11–19 | confirmed |
| Карточки verify agent-only | command-skill-gate.mdc 29 | confirmed |
| `explore/fast` в плане анализа | context-strategy SKILL.md 71–72 | confirmed |
| Битая ссылка QC | new-change SKILL.md 350; glob `openspec-quality-controller.md` только в `agents/` | confirmed |
| ADR-0009 table vs graph | ADR-0009 Решение п.2; canvas `medium: table` без рёбер | confirmed |
| ADR-0001 карточки не в чат | ADR-0001 Protects-invariants | confirmed |
| Blast Radius last-slice = extends | archive design Decision 3 + main spec «код расширения» | confirmed |
| Assumption kit без project.md | `openspec/project.md` в kit нет | confirmed |

**Неточность BC3:** формулировка «таблица — без доказательства» читается как «доказательство не фильтруем». Canvas: доказательство отсекается **всегда**; у таблицы нет только отсева «без инцидентной связи». EM3 в design сказано верно («таблица: без доказательства, связь не нужна» в смысле двух отсевов графа vs одного). BC3 выровнять с EM3 и canvas.

**Слэши Windows.** Assumption 1: смешанный слэш не меняет класс. BC1 операционно проверяет `/cf/` `/cfe/`. На win32 путь в tasks может быть `src\cfe\`. Без нормализации `\` → `/` kit-only vs cfe разъедется. Зафиксировать шаг нормализации в BC1 (не открытый вопрос пользователю).

**Условия намёка 1–2.** S2 меняет только счётчик ≥4 (отсев средства). Вывод «не из этапов» и топологический признак остаются из overview-map-offer / canvas. Primary S2 («четыре доказанные строки без рёбер → намёк, если средство таблица») предполагает, что вывод и признак в отчёте уже есть. Это не отмена архивного контракта предложения.

## Реалистичность

Все срезы **mechanical** (markdown `.cursor/**`) — согласовано с `developer: n/a` и apply-gate kit-only.

Приёмка без прогона чата на чужой ИБ (Assumption 3) реалистична: сверка текста + Grep. Last-slice смысл проверяется сверкой веток в apply SKILL (три слова vs архив), не живым apply на стенде.

Риск 2 (бюджет always-apply ≤ 34 КБ, `delivery-integrity.md` п.7): копировать в D5 **3–6 строк** имён карточек, не тело `command-skill-gate.mdc`. Уже в Risks — оставить.

Риск 3 (голос эталонов): менять только литералы. Список утечки в BC5 достаточен как отрицательный Grep; положительный словарь в BC5 задан.

Откат: git литералов; развилку last-slice целиком не откатывать — верно.

## Соответствие Why

Полное: детектор, словарь, порог средства, вход сессии, ссылки/fallback. Симптом «в другом проекте развилка молча без предрелиза» закрывается **не** переписыванием трёх слов, а тем, что `cfe` больше не требует путей ЭДО — в чужом `src/…/cfe/` сегмент сработает. Это тот же контракт last-slice, другой предикат.

## Чёткость приёмки

| Срез | Primary наблюдаем? | Замечание |
|---|---|---|
| S1 | Да: нет литералов фильтра; kit-only → архив без `ревью`; cfe в tasks → три слова (optional) | Optional «три слова» не должен стать blocking Primary — иначе kit-only ЗНИ этой поставки не примет S1 |
| S2 | Да: таблица 4 доказанных строк без рёбер при средстве table | В accept явно: условия 1–2 (вывод + признак) не снимаются |
| S3 | Да: текст «Read только первый ход»; cue диспетчера короткий | «Замер бюджета always-apply» — agent-задача, не user-spike; не делать blocking |
| S4 | Да: ссылка открывается; нет `explore/fast` | Указать целевой путь ссылки |
| S5 | Да: Grep списка утечки в `.cursor/**` = 0 | Это UX поставки (копия `.cursor/` чистая), не foundation |

## Ложные границы срезов

**S5 не foundation.** Primary «Grep утечки = 0 по `.cursor/**`» — наблюдаемый исход копирования kit в чужой проект. Правило 4a (self-achievable) выполняется, если задачи S5 включают **дочистку оставшихся литералов** (не только файлы «кроме S1–S4») и финальный Grep.

Ложная независимость в текущем тексте: «S5 → нет» и «зависимостей приёмки нет». Whole-tree Grep **не** проходит, пока в apply/overview ещё «ЭДО…» / `nastroyka-knopok-processov`. Это **порядок apply**, не отсутствие ценности S5.

Рекомендация (не объединять срезы):

- Приёмка S1–S4 **не** ждёт S5 (S1 Primary — развилка/фильтр, не Grep имён).
- Практический порядок S1→S2→S3→S4→S5 оставить.
- В графе: литералы в файлах S1–S4 править **в том же файле**, что протокол (уже есть); S5 — остаток + доказательство Grep=0.
- Убрать фразу «зависимостей приёмки нет» без оговорки: S5 с Primary по всему дереву идёт последним; задачи S5 самодостаточны за счёт дочистки.

Чеклист поставки **не** выделять срезом — верно; не класть в S1 blocking «Grep утечки = 0».

## Анти-паттерны (peer)

| Паттерн | Вердикт |
|---|---|
| Shadow Storage | NOT_APPLICABLE |
| Parallel Workflow | OK — не вводится вторая развилка last-slice |
| Convention Break | OK — словарь к глоссарию и `project-paths.mdc` |
| API Bypass | NOT_APPLICABLE |
| Reinvented Abstraction | OK — сегменты те же, что извлечение путей из карточки |
| Orphan Extension | NOT_APPLICABLE |
| Defensive Cake | NOT_APPLICABLE |
| Hardcoded Identity Filter (AP-055) | OK — Chosen **снимает** allow-list чужих путей; новый список имён форм не вводится |
| Foundation slice | OK после оговорки по S5 (см. выше) |

## Blast Radius / precedent

Таблица Blast Radius в design достаточна. Класс: `extends`, не `revokes`.

- Last-slice: `cfe`/`mixed` → три слова; пусто/`cf` → архив без предрелиза. Слова `архив`/`стоп` как в архивной ЗНИ. Ярлык `cf` = бывший `cf-ea`.
- Overview-map-offer: один отчёт, панель по согласию, без автосборки. Фраза «после соседней ЗНИ» уходит **без** включения «все пути» в этот вход.
- ADR-0009: порог описания по средству, не отмена графа как средства.
- ADR-0001: имена служебных карточек в always-apply правиле, не в чат.

Не предлагать: принимать/архивировать соседние ЗНИ; вынос `pav_` из AP-031; правки `openspec/changes/archive/**`.

## Identity Filter / Data Contract

Хуков `&После` / списков имён форм нет. Data Contract Gate к BSL не применяется. Секция `## Hardcode Justification` не нужна: Chosen — сегмент пути, не allow-list имён.

---

## Рекомендации к design.md (конкретные правки секций)

Переписывать Chosen / срезы / last-slice **не** требуется. Точечно:

### 1. `## Behavior Contract` п.1

Заменить набор источников и предикат на:

- Grep: `tasks.md` и `design.md` (как сейчас в apply/status), пути `src/**/*.bsl`.
- Перед сегментами нормализовать `\` → `/`.
- Есть `/cfe/` и нет `/cf/` как сегмента каталога выгрузки → `cfe`; только `/cf/` → `cf`; оба → `mixed`; нет путей → не определён (для развилки = как `cf`).
- `openspec/project.md`: **не** источник `marker_scope`. Карточка задаёт, как в этом репо пишутся корни (`/cf/` `/cfe/`), но наличие строки cfe в таблице не делает kit-only ЗНИ `mixed`.

### 2. `## Behavior Contract` п.3

Выровнять с EM3 и canvas: отсев без доказательства — **всегда**; отсев без инцидентной связи — **только граф**; таблица связь не требует. Условия намёка «вывод» и «топологический признак» — без изменения архива overview-map-offer. Согласие — тот же один отчёт; «все пути» в этот вход не подмешивать.

### 3. `## Slices` / граф зависимостей / матрица приёмки

- Явно: S5 не foundation; Primary Grep=0 — исход поставки.
- Порядок apply S1→…→S5 сохранить; литералы в файлах S1–S4 — в том же коммите/задаче, что протокол.
- Оговорка вместо «зависимостей приёмки нет»: S1–S4 принимаются без S5; S5 Primary по дереву — после них или за счёт дочистки в задачах S5.
- S1 чеклист поставки: пункт про фильтр/сегменты, не про список утечки.
- S4: целевой href контролёра — `.cursor/skills/1c-agent-patterns/quality-controller.md`.
- S1 optional «три слова при cfe в tasks» не делать blocking Primary.

### 4. Не менять

- `## Implementation Options` Chosen A.
- `## Decisions` 1–3 (детектор не развилка; словарь; AP-031).
- `## Blast Radius`.
- Формулировку трёх слов и веток `архив`/`стоп`.

## Open Questions

Нет. Состав словаря и закрытые оси (last-slice, AP-031, archive/**) не переоткрывать.
