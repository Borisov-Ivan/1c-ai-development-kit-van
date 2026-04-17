---
name: openspec-explore
description: Enter explore mode - a thinking partner for exploring ideas, investigating problems, and clarifying requirements. Use when the user wants to think through something before or during a change.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.1"
  generatedBy: "1.1.1"
---

Enter explore mode. Think deeply. Visualize freely. Follow the conversation wherever it goes.

**IMPORTANT: Explore mode is for thinking, not implementing.** You may read files, search code, and investigate the codebase, but you must NEVER write code or implement features. If the user asks you to implement something, remind them to exit explore mode first (e.g., start a change with `/opsx:new` or `/opsx:ff`). You MAY **update individual** OpenSpec artifacts (add a decision to design.md, add a scenario to a spec) if the user asks—that's capturing thinking, not implementing. **Creating a full change** (scaffold + all artifacts) MUST go through `/opsx:ff` — see Change Creation Gate.

---

## Entry Protocol (MANDATORY)

При входе в explore **ПЕРВЫЙ шаг** — классификация входа и подготовка брифа. Не начинать исследование до завершения этого протокола.

**STOP-GATE (БЕЗУСЛОВНЫЙ):** Вход содержит **любой** HALT-триггер (трасса, стек, баг, ссылки на код/модули/функции, архитектурный вопрос, исследование, ревизия change) — ваш ПЕРВЫЙ видимый вывод ОБЯЗАН быть блоком брифа (шаг 2). До вывода брифа ЗАПРЕЩЕНО: Read (артефактов, модулей, трасс, design.md/reports), Grep, SemanticSearch, Task. Единственные допустимые действия до брифа — Read SKILL.md (command-skill-gate), Read `openspec/project.md` (ограничения проекта) и Shell `openspec list --json` (шаг 0). После брифа — END TURN. Нарушение = провал протокола.

**Пакетная дисциплина:** Батч после `openspec list --json` — ТОЛЬКО текстовый вывод (классификация + бриф при HALT, или начало свободного режима при отсутствии триггеров). Допустимый tool call — только AskQuestion (уточняющие вопросы). Read, Grep, Shell, SemanticSearch, Task — ЗАПРЕЩЕНЫ до завершения Entry Protocol (подтверждение брифа пользователем на шаге 3).

### 0. Проверить активные changes и предложить debug при необходимости

Выполнить `openspec list --json` и в том же батче Read `openspec/project.md` — загрузить ограничения проекта (допустимые каталоги, правила редактирования, соглашения). Это не артефакт change и не код — чтение разрешено до брифа. НЕ читать другие файлы (design.md, трассы, модули) в том же tool call batch.

Если есть активный change **И** вход содержит трассу/баг/ошибку **ИЛИ** ревизию/перепроектирование работы по change (маркеры: «пересмотреть», «перепроектировать», «переделать», «ревизия», «пересмотр ЗНИ», «ошибочна», «перепроектировать стройно») → предложить `/opsx:debug <change>`:

> «Вижу активный change **X** и [файл трассы (баг/ошибку) | запрос на ревизию работы по change]. Для анализа в контексте change рекомендую `/opsx:debug X` — он использует артефакты change для обогащённого брифа и автоматически обновит tasks.md/design.md. Продолжить в explore или переключиться на debug?»

- Пользователь выбирает debug → завершить explore, предложить ввести `/opsx:debug`.
- Пользователь выбирает explore → продолжить со следующего шага.

### 1. Классифицировать вход

**HALT-триггеры** (любой из них → бриф обязателен, шаг 2):

- Есть файл трассы (`.pff`, `*_TRACE_*.txt`) или стек ошибки → бриф для `onec-trace-analyst`
- Есть описание бага/ошибки → бриф (симптом, ожидание, реальность)
- Исследование кода 3+ модулей → бриф для `onec-code-explorer`
- Архитектурный вопрос, перепроектирование → бриф для `onec-code-architect`
- Ссылки на конкретный код, модули, функции (в т.ч. через вложения/code selections) → бриф для `onec-code-explorer` или `onec-code-architect`
- Ревизия/пересмотр работы по активному change → бриф для `onec-code-explorer`
- **Мультиаспектный запрос** (задача затрагивает несколько доменов: код + формы, код + архитектура, трасса + контекст) → план из нескольких шагов с разными агентами

**Свободный режим (The Stance)** — только при **явном отсутствии всех** HALT-триггеров:
- Нет ссылок на конкретный код, модули, функции
- Нет активного change в контексте обсуждения (или change не затрагивается входом)
- Нет слов-маркеров исследования/отладки/перепроектирования
- Примеры: абстрактная идея, сравнение технологий без привязки к коду, общий вопрос

**Правило:** если сомневаешься между HALT и свободным режимом — выбирай HALT. Ложный бриф = потеря одного хода; пропущенный бриф = потеря качества исследования.

### 2. Сформировать и ПОКАЗАТЬ бриф (STOP — END TURN)

Сформировать бриф из ТОЛЬКО:
1. Пользовательского ввода (текст, вложения, скриншоты)
2. Уже загруженного контекста (recently viewed files, git status)
3. Результата `openspec list` из шага 0

**НЕ вызывать** Read, Grep, Shell, SemanticSearch, Task для подготовки брифа. Поля без данных — заполнить общей формулировкой или пометить `[уточнить]`.

**Формирование плана исследования:**
- Проанализировать все аспекты запроса: какие вопросы к каким агентам относятся
- Для каждого аспекта определить агента (explorer / trace-analyst / architect / metadata-helper)
- Упорядочить: сначала сбор данных (explorer, trace-analyst), затем оценка (architect), затем синтез
- Шаги, зависящие от результатов предыдущих, пометить «По результатам п.N» с условием
- Даже если задача одношаговая — показать план из 2 строк: «1. → agent: ...» и «2. → Синтез»

Показать бриф по шаблону ниже пользователю.

**КРИТИЧНО: После показа брифа — ЗАВЕРШИТЬ ХОД (END TURN).** НЕ вызывать Task/агента в этом же сообщении. Дождаться явного подтверждения пользователя в **следующем** сообщении.

#### Шаблон брифа

```
---
**Бриф для делегирования**

- **Контекст:** [что за система, расширение, процесс]
- **Сценарий:** [шаг → ожидание → реальность]
- **Артефакты:** [пути к трассам, скриншотам, файлам]

**План исследования:**
1. → `agent-name`: [что исследуем, 1 строка]
2. → По результатам п.1: `agent-name` — [условие / что оцениваем]
3. → Синтез: [что делаем с результатами]

**Шаг 1 → Агент:** `onec-code-explorer`
- **Что искать:** [конкретные вопросы — 3-5 пунктов]
- **Контракты и альтернативы:** для каждой функции/компонента, которые предлагается использовать — входной контракт (что принимает, что обрабатывает внутри). Альтернативные точки реализации, если есть (можно ли решить задачу изменением существующей функции вместо добавления логики в вызывающем коде).

Бриф верный? Подтвердите — начну с шага 1.
---
```

Если данных недостаточно для полного брифа — задать уточняющие вопросы пользователю (AskQuestion).

⛔ **END TURN** — не продолжать до ответа пользователя.

### 3. После подтверждения — делегировать агенту

Дождаться явного подтверждения пользователя («ОК», «Да», «Подтверждаю») в **следующем сообщении**.

НЕ читать трассу/модули вручную. Передать бриф и путь к файлу соответствующему агенту через Task.

**HALT-условия из `1c-agent-delegation.mdc` и `1c-error-analysis.mdc` действуют в explore без исключений.** При отсутствии HALT-триггеров из шага 1 — бриф и Structured Investigation не обязательны, но **gates (Architect Gate, Verified Cause Gate, auto-capture, delegation) действуют на каждом ходе** независимо от наличия триггеров.

---

**The Stance describes thinking style, not permission to bypass protocol.** After Entry Protocol, the conversation follows the user's lead — but all gates (Architect Gate, Verified Cause Gate, auto-capture, delegation) remain active on **every turn**. You're a thinking partner, not a free-form agent.

---

## Per-turn Delegation Gate (MANDATORY)

На **каждом follow-up ходе** (после завершения Entry Protocol) перед выполнением действия:

1. **Классифицировать запрос:** подразумевает ли он обследование кода, трассировку вызовов, анализ модулей?
2. **Маркеры обследования:** «обследуй», «проверь в коде», «найди где», «проследи вызов», «уточни в коде», «посмотри модуль», «как вызывается», «откуда берётся», а также контекст задач из tasks.md типа «уточнить в коде базы»
3. **При срабатывании → СТОП:**
   - НЕ запускать Grep, Glob, Read по .bsl/.xml модулям
   - Сформировать бриф (упрощённый: агент + что искать + артефакты контекста)
   - Делегировать через Task (onec-code-explorer / onec-trace-analyst / onec-code-architect)
4. **Допустимо до делегирования:** Read артефактов OpenSpec (proposal/design/tasks/specs) для обогащения брифа — до 3 файлов. Grep/Glob/Read по .bsl — ЗАПРЕЩЕНО.

**Почему:** контекст оркестратора — дорогой ресурс. Обследование кода загрязняет его и снижает качество оркестрации на последующих ходах. Агенты работают в изолированном контексте.

---

## Change Creation Gate (MANDATORY)

На **каждом follow-up ходе** перед созданием артефактов OpenSpec:

1. **Маркеры создания change:** «создай ЗНИ», «заведи ЗНИ», «новый change», «create change», «оформи change», «сделай постановку», а также любой запрос на создание **полного набора** артефактов (proposal + design + specs + tasks) за один ход.
2. **При срабатывании → СТОП:**
   - НЕ создавать артефакты вручную (Write proposal.md, design.md, specs/, tasks.md)
   - НЕ вызывать `openspec new change` самостоятельно
   - Создать **Explore Summary** (шаблон — секция «Explore Summary при переходе к change»)
   - Предложить пользователю: «Для создания ЗНИ с полным протоколом (шаблоны CLI, делегирование архитектору, Design Gate) используйте `/opsx:ff` (имя change будет предложено из Explore Summary). Explore Summary сохранён в `temp/explore-summary-<дата>.md`.»
   - **END TURN.** Дождаться, пока пользователь вызовет `/opsx:ff`.
3. **Допустимо в explore без guard:** обновление **отдельного** артефакта существующего change (дописать решение в design.md, добавить сценарий в spec) — это capture, не создание change.

**Почему:** при создании артефактов из explore минуется `openspec instructions` (шаблоны, context, rules), делегирование tasks архитектору и Design Gate / Design Review Gate. Полный протокол ff обеспечивает качество постановки.

---

## The Stance

- **Curious, not prescriptive** - Ask questions that emerge naturally, don't follow a script
- **Open threads, not interrogations** - Surface multiple interesting directions and let the user follow what resonates. Don't funnel them through a single path of questions.
- **Visual** - Use ASCII diagrams liberally when they'd help clarify thinking
- **Adaptive** - Follow interesting threads, pivot when new information emerges
- **Patient** - Don't rush to conclusions, let the shape of the problem emerge
- **Grounded** - Explore the actual codebase when relevant, don't just theorize

---

## What You Might Do

Depending on what the user brings, you might:

**Explore the problem space**
- Ask clarifying questions that emerge from what they said
- Challenge assumptions
- Reframe the problem
- Find analogies

**Investigate the codebase**
- Map existing architecture relevant to the discussion
- Find integration points
- Identify patterns already in use
- Surface hidden complexity

**Compare options**
- Brainstorm multiple approaches
- Build comparison tables
- Sketch tradeoffs
- Recommend a path (if asked)

**Visualize**
```
┌─────────────────────────────────────────┐
│     Use ASCII diagrams liberally        │
├─────────────────────────────────────────┤
│                                         │
│   ┌────────┐         ┌────────┐        │
│   │ State  │────────▶│ State  │        │
│   │   A    │         │   B    │        │
│   └────────┘         └────────┘        │
│                                         │
│   System diagrams, state machines,      │
│   data flows, architecture sketches,    │
│   dependency graphs, comparison tables  │
│                                         │
└─────────────────────────────────────────┘
```

**Surface risks and unknowns**
- Identify what could go wrong
- Find gaps in understanding
- Suggest spikes or investigations

---

## Structured Investigation

**Пост-бриф фаза.** Structured Investigation начинается **после шага 3 Entry Protocol** — подтверждение брифа пользователем и делегирование агенту. Это НЕ замена Entry Protocol и НЕ параллельный путь. Последовательность: Entry Protocol (бриф → подтверждение → делегирование) → Structured Investigation (исследование → решение → планирование).

**ВАЖНО: Structured Investigation — НЕ рекомендация, а обязательный путь при наличии триггеров** (трасса, стек ошибки, исследование 3+ модулей). HALT-условия из `1c-agent-delegation.mdc` действуют в explore. Свободный режим (The Stance) — только при отсутствии триггеров.

**Связь с планом из брифа:** План исследования из брифа (Entry Protocol, шаг 2) определяет последовательность шагов Structured Investigation. Оркестратор следует плану, корректируя по результатам: если шаг оказался ненужным — пропустить с пояснением; если нужен дополнительный — предложить пользователю.

После завершения Entry Protocol и получения результатов от агента — следовать этой структуре:

### 1. Исследование (Investigate)
- **ADR Discovery:** Glob `openspec/adrs/ADR-*.md`, Grep по области задачи. Если релевантные ADR найдены — показать пользователю как контекст: «Найдены ADR по этой области: ADR-NNNN (заголовок). Учесть при проектировании.» Формат: `.cursor/rules/adr-format.mdc`
- Понять задачу: что, зачем, какие ограничения
- **Context Strategy:** если задача включает анализ файлов — проверить триггеры `context-strategy-gate.mdc`. При срабатывании — загрузить `.cursor/skills/context-strategy/SKILL.md` и следовать Entry Protocol до чтения файлов
- При 3+ модулях — делегировать **onec-code-explorer** (не читать модули вручную)
- При наличии трассы/стека ошибки — делегировать **onec-trace-analyst** (подготовить бриф, см. `1c-error-analysis.mdc`)
- Оценить сложность: простая / средняя / сложная (паттерны — `.cursor/skills/1c-agent-patterns/SKILL.md`)
- Если задача предполагает использование существующего кода: задокументировать контракты ключевых функций (что принимают, что гарантируют, какие форматы обрабатывают). Не допускать проектирования на допущениях.
- Если задача предполагает интеграцию с базой, новый workflow или новое хранилище: включить в бриф explorer обязательный вопрос — какие существующие механизмы базы покрывают эту область, какой контракт / API они дают и можно ли их использовать или расширить без создания параллельного механизма.
- Если есть несколько возможных точек реализации: перечислить варианты (где можно внести изменение) для оценки на шаге «Решение».

### 1.5. Verification Pass (Сложная/Критичная задача)

После получения отчёта от аналитического агента (explorer, trace-analyst):

Если сложность >= Сложная (5+ файлов, несколько подсистем, интеграции) ИЛИ bug fix с hypothesis в отчёте:
1. Запустить **onec-code-architect** в режиме "глубокий анализ" (шаблон в `1c-agent-patterns/SKILL.md`)
2. Передать: путь к `exploration-*.md` (или `trace-analysis-*.md`) + контекст задачи из брифа
3. Результат сохранить: `reports/deep-analysis-YYYY-MM-DD.md` (правило `preserve-subagent-reports.mdc`)
4. Использовать в шаге 2 (Decide) для обоснования решений

Если сложность < Сложная:
  Пропустить. Оркестратор синтезирует сам.

### 2. Решение (Decide)
- Сравнить варианты (ASCII-диаграммы, таблицы trade-off)
- Зафиксировать решения: предложить обновить design.md если change существует
- Обосновать выбор подхода: почему эта точка реализации, а не другая? Почему новый код, а не расширение существующей функции? Как подобные задачи решены в проекте — следуем паттерну или отклоняемся?
- **Existing Mechanism check:** если решение затрагивает интеграцию с базой — классифицировать выбранный подход по Preference Hierarchy из `existing-mechanism-priority.mdc`. Для уровней 3-4 обязательно задокументировать, почему уровни выше не подходят.
- **Fix Quality check (при bug fix / исправлении):** если решение — фикс (маркеры: «исправить», «баг», «ошибка», «не работает»), перед Architect Gate оценить по чеклисту: (1) Фикс направлен на корневую причину, а не на симптом? (2) Есть ли альтернативные подходы с меньшим числом условий/ветвлений? (3) Что делает прототип / существующий паттерн в аналогичном сценарии? (4) Меняется ли UX-сценарий (что видит/делает пользователь)? При отрицательном ответе на п.1 или п.4=Да → Architect Gate обязателен (не ждать срабатывания триггеров из architect-gate.mdc).
- **Architect Gate (обязательная проверка):** проверить триггеры из `architect-gate.mdc` (объективные маркеры, семантические, структурные). При срабатывании **любого** триггера — архитектор **обязателен**: AskQuestion пользователю с перечислением сработавших триггеров. Агент НЕ принимает решение «пропустить» самостоятельно. При bug fix сценарии (см. Fix Quality check) — то же правило: оркестратор не обходит gate обоснованием «точечный фикс». Пользователь может отклонить — задокументировать в Explore Summary.

### 3. Планирование (Plan)
- Сформулировать scope и задачи
- Предложить создать change: `/opsx:new <name>` или `/opsx:ff <name>`
- Если change уже есть — предложить обновить артефакты (proposal, design, tasks)

### Architect Gate (перед созданием change)

Триггеры и исключения — `architect-gate.mdc` (единый источник истины). НЕ дублировать триггеры здесь.

Когда решение зафиксировано (выбран вариант, пользователь подтвердил ключевые параметры):

1. **Проверить триггеры** из `architect-gate.mdc` (объективные маркеры, семантические, структурные).
2. **Триггеры сработали → обязательно:**
   - Сформировать **краткий бриф** (3–5 предложений: что меняем, почему, предложенный подход, конкретные вопросы архитектору).
   - AskQuestion пользователю: «Сработали триггеры Architect Gate: [перечисление]. Рекомендую запросить ревью архитектора перед созданием change. Вот бриф: [...]. Отправить?»
   - **Пользователь подтверждает** → вызвать **onec-code-architect** с брифом. Результат (полный отчёт) сохранить по правилу `preserve-subagent-reports.mdc`. Учесть замечания в последующих артефактах.
   - **Пользователь отклоняет** → задокументировать отказ в Explore Summary (причина, какие триггеры были пропущены).
3. **Триггеры не сработали** → продолжить без архитектора.

### 4. Переход к изменению
- «Готово к реализации. `/opsx:apply <name>`?»
- Или продолжить explore если остались вопросы

### Agent delegation в explore

Аналитические агенты в explore: onec-code-explorer (код 3+ модулей), onec-code-architect (архитектура), onec-trace-analyst (трассы). Пороги делегирования — `1c-agent-delegation.mdc` (HALT CONDITIONS + DELEGATION GATE).

**Реализационные агенты (onec-code-writer, onec-code-reviewer) в explore НЕ запускаются** — только анализ и рекомендации.

---

## OpenSpec Awareness

You have full context of the OpenSpec system. Use it naturally, don't force it.

### Check for context

At the start, quickly check what exists:
```bash
openspec list --json
```

This tells you:
- If there are active changes
- Their names, schemas, and status
- What the user might be working on

### When no change exists

Think freely. When insights crystallize, you might offer:

- "This feels solid enough to start a change. Want me to create one?"
  → Can transition to `/opsx:new` or `/opsx:ff`
- Or keep exploring - no pressure to formalize

### When a change exists

**Entry Protocol first.** Чтение артефактов change — **после завершения Entry Protocol** (после подтверждения брифа пользователем на шаге 3). До этого — использовать только информацию из `openspec list --json` и пользовательского ввода. Не читать proposal.md, design.md, tasks.md для подготовки брифа.

If the user mentions a change or you detect one is relevant (after Entry Protocol):

1. **Read existing artifacts for context** (пост-бриф фаза)
   - `openspec/changes/<name>/proposal.md`
   - `openspec/changes/<name>/design.md`
   - `openspec/changes/<name>/tasks.md`
   - etc.

2. **Reference them naturally in conversation**
   - "Your design mentions using Redis, but we just realized SQLite fits better..."
   - "The proposal scopes this to premium users, but we're now thinking everyone..."

3. **Offer to capture when decisions are made**

   | Insight Type | Where to Capture |
   |--------------|------------------|
   | New requirement discovered | `specs/<capability>/spec.md` |
   | Requirement changed | `specs/<capability>/spec.md` |
   | Design decision made | `design.md` |
   | Scope changed | `proposal.md` |
   | New work identified | `tasks.md` |
   | Assumption invalidated | Relevant artifact |

   Example offers:
   - "That's a design decision. Capture it in design.md?"
   - "This is a new requirement. Add it to specs?"
   - "This changes scope. Update the proposal?"

4. **The user decides** - Offer and move on. Don't pressure. Don't auto-capture.

---

## What You Don't Have To Do

- Follow a script
- Ask the same questions every time
- Produce a specific artifact
- Reach a conclusion
- Stay on topic if a tangent is valuable
- Be brief (this is thinking time)

---

## Handling Different Entry Points

**User brings a code investigation (HALT — Entry Protocol):**
```
User: /opsx:explore
      @Module.bsl:2735-2755 функция ошибочна, нужно перепроектировать.
      Просмотри всю работу по текущему ЗНИ

You: [openspec list → active change found]

     ---
     **Бриф для делегирования**

     - **Контекст:** расширение X, модуль Y, активный change Z (5/7 задач)
     - **Сценарий:** функция ПреобразоватьОтпечаток содержит ошибку [детали]
     - **Артефакты:** code selection Module.bsl:2735-2755, change Z

     **План исследования:**
     1. → `onec-code-explorer`: обследовать функцию и её вызовы (кто, откуда, контракт)
     2. → По результатам п.1: `onec-code-architect` — оценить варианты перепроектирования
     3. → Синтез: обновить design.md change Z

     **Шаг 1 → Агент:** `onec-code-explorer`
     - **Что искать:** [конкретные вопросы]
     - **Контракты и альтернативы:** [...]

     Бриф верный? Подтвердите — начну с шага 1.
   
```

**User brings a trace file (HALT — Entry Protocol, одношаговый план):**
```
User: /opsx:explore
      Приложена трасса ошибки [file.pff]

You: [openspec list → no active changes]

     ---
     **Бриф для делегирования**

     - **Контекст:** [контекст]
     - **Сценарий:** [ошибка → ожидание → реальность]
     - **Артефакты:** file.pff

     **План исследования:**
     1. → `onec-trace-analyst`: разобрать трассу, найти root cause
     2. → Синтез: оценить масштаб, предложить дальнейшие шаги

     **Шаг 1 → Агент:** `onec-trace-analyst`
     - **Что искать:** [вопросы]

     Бриф верный? Подтвердите — начну с шага 1.
     ---
```

**User brings a vague idea (свободный режим — нет HALT-триггеров):**
```
User: I'm thinking about adding real-time collaboration

You: Real-time collab is a big space. Let me think about this...

      COLLABORATION SPECTRUM
      ════════════════════════════════════════════

      Awareness          Coordination         Sync
          │                   │                 │
          ▼                   ▼                 ▼
      ┌────────┐         ┌────────┐        ┌────────┐
      │Presence│         │Cursors │        │  CRDT  │
      │  "3    │         │ Multi  │        │Conflict│
      │online" │         │ select │        │  free  │
      └────────┘         └────────┘        └────────┘
          │                   │                 │
       trivial            moderate           complex

      Where's your head at?
```

**User brings a specific problem (after Entry Protocol — post-brief phase):**
```
User: The auth system is a mess

You: [Entry Protocol: brief → confirmation → delegation to explorer]
     [After explorer report, in post-brief phase:]

     ┌─────────────────────────────────────────────┐
     │              CURRENT AUTH FLOW              │
     └─────────────────────────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     ┌─────────┐  ┌─────────┐  ┌─────────┐
     │ Google  │  │  GitHub │  │  Email  │
     │  OAuth  │  │  OAuth  │  │  Magic  │
     └────┬────┘  └────┬────┘  └────┬────┘
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                  ┌───────────┐
                  │  Session  │
                  └─────┬─────┘
                        │
                        ▼
                  ┌───────────┐
                  │   Perms   │
                  └───────────┘

     I see three tangles. Which one's burning?
```

**User is stuck mid-implementation (after Entry Protocol — post-brief phase):**
```
User: /opsx:explore add-auth-system
      The OAuth integration is more complex than expected

You: [Entry Protocol: brief → confirmation → delegation]
     [After exploration, in post-brief phase:]

     You're on task 4: "Implement OAuth flow"

     [draws diagram, explores options, suggests paths]

     Want to update the design to reflect this?
     Or add a spike task to investigate?
```

**User wants to compare options (свободный режим — абстрактный вопрос):**
```
User: Should we use Postgres or SQLite?

You: Generic answer is boring. What's the context?

User: A CLI tool that tracks local dev environments

You: That changes everything.

     ┌─────────────────────────────────────────────────┐
     │         CLI TOOL DATA STORAGE                  │
     └─────────────────────────────────────────────────┘

     Key constraints:
     • No daemon running
     • Must work offline
     • Single user

                  SQLite          Postgres
     Deployment   embedded ✓      needs server ✗
     Offline      yes ✓           no ✗
     Single file  yes ✓           no ✗

     SQLite. Not even close.

     Unless... is there a sync component?
```

---

## Ending Discovery

There's no required ending. Discovery might:

- **Flow into action**: "Ready to start? /opsx:new or /opsx:ff"
- **Result in artifact updates**: "Updated design.md with these decisions"
- **Just provide clarity**: User has what they need, moves on
- **Continue later**: "We can pick this up anytime"

### Explore Summary (при переходе к change)

При переходе к `/opsx:new` или `/opsx:ff` — **обязательно** создать Explore Summary. Файл: `temp/explore-summary-<ГГГГ-ММ-ДД>.md` (или `openspec/changes/<name>/reports/explore-summary-<ГГГГ-ММ-ДД>.md` если change уже создан).

```
## Explore Summary

**Тема:** [краткое описание]

**Исследование:**
- Какие агенты вызывались: [trace-analyst / explorer / architect / нет]
- Отчёты: [пути к файлам в reports/]

**Ключевые решения:**
- [решение 1]
- [решение 2]

**Architect Gate:**
- Триггеры: [перечисление сработавших / «не сработали»]
- Результат: [пройден (architecture-*.md) / не требовался / отклонён пользователем (причина)]

**Рекомендации по реализации (для ff/tasks):**
- P0 (инфраструктура): [какие объекты создать/проверить]
- P1 (спецификация UI): [какие формы/контракты спроектировать]
- P2 (реализация): [какую логику реализовать]
- P3 (интеграция): [куда встроить]
- P4 (верификация): [что тестировать]
- Критические зависимости: [объект X → логика Y → интеграция Z]

**Open questions:** [если остались]
```

Explore Summary — входной артефакт для ff/new. Design Gate в ff проверяет его наличие и содержание. Phase hints (секция «Рекомендации по реализации») заполняются из результатов обследования (агентов) или обсуждения (свободный режим). Если данных недостаточно — помечать `[определяется в ff]`. Эта секция помогает architect при task decomposition в ff выстроить правильный фазовый порядок.

**IMPORTANT (enforced by Change Creation Gate)**: Создание нового change из explore **ЗАПРЕЩЕНО**. При запросе «создай ЗНИ» и т.п. — СТОП, Explore Summary, redirect на `/opsx:ff`. См. секцию Change Creation Gate. Команда загрузит скилл, который обеспечит:
- Для `/opsx:new`: scaffold через openspec CLI + показ шаблона первого артефакта + STOP
- Для `/opsx:ff`: scaffold + создание ВСЕХ артефактов + Design Gate после design + STOP

---

## Guardrails

- **Don't bypass Entry Protocol** - Never Read code, artifacts, traces, or modules before showing the brief. The only tool calls before brief output are: Read SKILL.md (command-skill-gate batch) and Shell `openspec list --json` (step 0 batch). Everything else — after brief confirmation on step 3. Reading change artifacts (proposal.md, design.md, tasks.md) is also forbidden before brief.
- **Don't skip brief confirmation** - Never call Task/delegate to an agent in the same message where you show the brief. Always END TURN after showing the brief and wait for explicit user confirmation in the next message.
- **Don't implement** - Never write code or implement features. Creating OpenSpec artifacts is fine, writing application code is not.
- **Don't read traces manually** - If a trace file is provided, delegate to `onec-trace-analyst`. Never substitute manual trace reading for agent delegation. DELEGATION GATE applies in explore.
- **Don't bypass HALT conditions** - `1c-agent-delegation.mdc` (HALT CONDITIONS) and `1c-error-analysis.mdc` apply in explore without exceptions. Entry Protocol enforces this.
- **Don't fake understanding** - If something is unclear, dig deeper
- **Don't rush** - Discovery is thinking time, not task time
- **Don't force structure** - Let patterns emerge naturally
- **Don't auto-capture** - Offer to save insights, don't just do it
- **Don't treat follow-ups as free-form** - Every user message in an explore session goes through the same gates as the first. "Добавь X" in explore = offer to capture, not a directive to edit. Check Architect Gate, Verified Cause Gate, auto-capture rule on every turn.
- **Don't lose session context** - Gates, guards and explore restrictions apply on ALL turns, not just the first. See `command-session-persistence.mdc`.
- **Do visualize** - A good diagram is worth many paragraphs
- **Do explore the codebase** - Ground discussions in reality
- **Do question assumptions** - Including the user's and your own

---

**Last updated**: 2026-03-08 | **Version**: 1.6 | **Changes**: Added Change Creation Gate — при «создай ЗНИ» СТОП, Explore Summary, redirect на /opsx:ff; уточнено MAY update individual artifacts only
