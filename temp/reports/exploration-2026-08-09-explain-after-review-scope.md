# Exploration: explain после ревью/реализации — охват обработанного кода в брифе

**Дата:** 2026-08-09  
**user-goal:** После `/review`, `/release-review` и после реализации (apply/writer) предлагать `/opsx:explain`; explain в этом режиме берёт в охват обработанный код и показывает охват в entry-брифе для подтверждения.  
**Вне scope:** «критическое ревью vs договорённости / as-designed queue» (параллельное исследование).

---

## Свод

Сейчас `/opsx:explain` зрелый (B-explain → карта → карточки → журнал), но **входит в поток почти только из explore**. Финалы `/review`, `/release-review` и `/opsx:apply` **не предлагают** explain и **не передают** структурированный список обработанных модулей/процедур. Артефакты с охватом уже есть (`review-*.md`, `code-map.md`, handoff-acceptance, Code-Truth в `debug.md`), но explain **не умеет их автоподхватывать** как рамку «Охват». Главный продуктовый gap — handoff-контракт review/apply → explain + ослабление/уточнение HALT «модули не в бриф» для режима post-review/apply.

---

## Для заказчика

После ревью или внедрения кода логично сразу пройтись по **тому, что трогали**, глазами — с подтверждением «да, разбираем вот это». Сейчас такой переход нужно вручную: вызвать `/opsx:explain` и заново описать рамку. Цель ЗНИ — чтобы kit сам предложил разбор и в первом брифе показал охват (какие модули/изменения), а вы подтвердили или сузили.

---

## Как сейчас (факты с путями)

### 1) Propose / handoff к explain из review / apply

| Источник | Предлагает `/opsx:explain`? | Что предлагает в «Дальше» / next step |
|----------|----------------------------|--------------------------------------|
| `/opsx:explore` | **Да** — при цепочке точек в отчёте | `.cursor/skills/openspec-explore/SKILL.md` §2 синтез: «Дальше» может быть `/opsx:explain`; предпочтительно при call chain / hardcode-карте; «одной строкой, без второго брифа» |
| `/review` | **Нет** (grep по skill/commands — 0) | Карточка 4 слота, слот **Куда дальше**: устранение / extend / archive (`.cursor/skills/review/SKILL.md` §4.4 п.4; self-check §7) |
| `/release-review` | **Нет** (тот же skill, `release_mode=true`) | То же + при ARCH/MUST_FIX scope → `/opsx:extend … --from-review` |
| `/opsx:apply` | **Нет** (grep по apply skill — 0) | T-HANDOFF: acceptance / pause / final → verify / apply / archive / extend (`.cursor/skills/openspec-apply-change/SKILL.md` шаг 7; `.cursor/docs/opsx-output-style.md` §5.2) |
| Команды `review.md`, `release-review.md`, `opsx-apply.md` | Только делегирование в skill; explain не упоминается | — |
| `opsx-explain.md` | Вход: трасса, отчёт `temp/reports/…`, change, путь модуля, «как работает X» после **explore** | Примеры: `@temp/reports/trace-analysis-…`, кнопка по замеру — **не** review/apply |

**Вывод:** единственный канонический propose explain — explore. Review/apply богаты артефактами охвата, но next-step меню explain не включает.

### 2) Как формируется B-explain и слот Охват / Варианты

**SSOT брифа:** `.cursor/skills/openspec-explain/templates/entry-brief.md`  
**Индекс:** `.cursor/docs/templates/brief-card.md` § B-explain  
**Протокол:** `.cursor/skills/openspec-explain/SKILL.md` Entry Protocol §1  
**Бюджет:** `chat-output-budget.mdc` — B-explain ≤6 слотов

| Слот | Обяз. | Смысл сейчас |
|------|-------|--------------|
| **Сценарий** | да | Действия пользователя / операции замера |
| **Вопрос** | да | Якорь «что понять» |
| **Варианты** *или* **Охват** | да | XOR: 2–3 рамки **или** один абзац уже ясного охвата |
| **Контекст** | опц. | Пути трассы / отчёта / change |
| **Подтвердить?** | да | номер / «да» / уточнение |

**HALT в брифе (критично для темы):**

- Запрещены слоты Цель / Источник / Решено когда.
- **«Список модулей (`pav…`, M01…) — в карту точек / карточки, не в бриф»** (`entry-brief.md` HALT; SKILL self-check брифа п.3).
- Варианты и Охват одновременно — запрещены.
- До подтверждения: нет `Task`, нет массового Read `.bsl`; допустим Read ≤3 уже указанных отчётов для брифа.

**Карта точек** (после «да»): `templates/inventory-card.md` — имена эффектов ≤12 строк, без кода; модули/идентификаторы — на карточках точек.

**Эталоны:** сценарий из замера (`voice-good-brief.md`, эталоны A/B в `entry-brief.md`) — **не** сценарий «только что отрецензировали / внедрили diff».

### 3) Артефакты охвата, которые уже пишутся (но explain не подхватывает)

| Источник | Артефакт | Что содержит для охвата |
|----------|----------|-------------------------|
| Review | `…/reports/review-<scope-slug>-YYYY-MM-DD.md` (+ reasoning) | Scope UX в чате («Что отрецензировано»); полный отчёт с findings по файлам; список `target_files` резолвится в сессии (шаг 1), **отдельной секции handoff→explain нет** |
| Release-review | тот же + Tier 2 / Category 12 | Scope шире (всё расширение или change-scoped); explain-propose нет |
| Apply | `reports/code-map.md` | Накопительная карта: задача → модуль → процедура → path:lines |
| Apply | `reports/handoff-acceptance-S<N>-YYYY-MM-DD.md` | «Что реализовано» + полная «Карта правок» среза |
| Apply | `debug.md` Code-Truth Journal | `created_or_modified_symbols` после writer |
| Apply (чат) | блок «Карта правок (перед тестом)» | ≤5 пунктов проза + citation |

### 4) Входы explain сегодня

Команда явно допускает `@temp/reports/…`, но skill Entry Protocol ориентирован на **трассу / explore / «как работает X»**. Нет ветки «source = review report / code-map / post-apply handoff» с автозаполнением **Охват** из списка обработанных файлов/процедур.

---

## Gaps

1. **Нет propose explain** в финале `/review`, `/release-review`, T-HANDOFF apply (acceptance/final после реализации).
2. **Нет автоподхвата** списка файлов/модулей/процедур из review scope или apply code-map в B-explain.
3. **Конфликт HALT:** «модули не в бриф» vs user-goal «охват обработанного кода в entry-брифе». Нужно явно разрешить *компактный UX-охват* (человеческие имена модулей/процедур или «N файлов из ревью») в слоте **Охват**, оставив сырой dump `pav…`/Mxx и полный inventory в карте/журнале.
4. **Нет профиля сценария** «после ревью / после внедрения»: текущие эталоны — замер/клик; для post-review **Сценарий** = «прошли ревью / внедрили срез», **Вопрос** = «как устроены затронутые места».
5. **Explore shortcut** «explain без второго брифа» **не подходит** для post-review: здесь бриф с охватом — как раз цель подтверждения.
6. **Release-review full-extension:** охват может быть огромным — без вариантов «только Tier1 / только файлы с findings / весь scope» explain раздуется.
7. **Документация заказчика** (`review-guide.md`, `quick-start.md`, README) не связывает ревью/apply → explain.
8. **Нет machine-readable блока** в конце review-отчёта / handoff (типа `## Explain scope`) — оркестратор вынужден парсить prose findings.

---

## Предлагаемый handoff-контракт (review/apply → explain brief)

### A. Когда предлагать

| Триггер | Условие propose | Формулировка «Дальше» (одна строка) |
|---------|-----------------|-------------------------------------|
| Финал `/review` (после карточки 4 слотов / шага 7) | Scope ≤ ~12 `.bsl` **или** есть ≥2 логических точки (несколько процедур/файлов с findings или после writer-fix) | `/opsx:explain` по охвату ревью (или `@<review-report>`) |
| Финал `/release-review` | Предлагать с **Варианты** рамки (не весь cfe по умолчанию): Tier1 / файлы с замечаниями / весь scope | то же |
| Apply `acceptance` (срез с BSL) | После карты правок; опционально рядом с «принято» | `/opsx:explain` по карте правок среза |
| Apply `final` | Если за сессию/change менялся BSL | explain по `code-map.md` change |
| Apply pause / только ARCH | **Не** propose explain как default (сначала extend) | — |

Приоритет next step: блокеры (MUST_FIX ask / extend) **выше** explain; explain — когда отчёт «достаточен» или пользователь отказался от fix, либо после успешного fix-цикла.

### B. Что передают review / apply (артефакты)

Добавить в конец **main review report** и в **handoff-acceptance** / хвост **code-map** секцию (или YAML frontmatter-блок):

```markdown
## Explain scope (handoff)

- source: review | apply
- change: <name|none>
- focus: diff-focused | full | slice-S<N>
- files:
  - path: src/.../Module.bsl
    procedures: [Имя1, Имя2]   # опц.; из Review Boundaries / code-map
- report: <path to review-*.md | code-map.md | handoff-acceptance-*>
```

**Минимум для MVP:** список `files[]` + путь к отчёту-источнику. Процедуры — желательно (из Review Boundaries / code-map), не блокер.

**Запрещено:** отдельный `temp/explain-handoff-*.md` (уже запрещён skill explain) — handoff живёт **внутри** review/handoff/code-map.

### C. Как explain собирает B-explain (режим post-review/apply)

При входе `/opsx:explain @…/review-*.md` | `@…/code-map.md` | `@…/handoff-acceptance-*` | фраза «по ревью» / «по срезу» в той же сессии:

1. Read источника (≤3 файла) → извлечь `## Explain scope` или эвристику: files из отчёта / code-map.
2. Бриф **B-explain** с **Охват** (не Варианты), кроме release full-extension → тогда **Варианты**.
3. Слоты:

| Слот | Заполнение |
|------|------------|
| **Сценарий** | «После ревью `<scope>`» / «После реализации среза S\<N\> ЗНИ `<name>`» (1–2 предложения эффекта, не протокол) |
| **Вопрос** | Default: «как устроены затронутые места и на что смотреть при приёмке/сопровождении» (можно уточнить) |
| **Охват** | UX-абзац: N модулей / ключевые процедуры **человеческим языком**; при ≥4 файлах — «все файлы из ревью/карты (список в Контекст)» + 1–3 якоря в прозе |
| **Контекст** | пути: review-report / code-map / change; **здесь** полный список path (маркированный), без свалки в Охват |
| **Подтвердить?** | «да» / уточнить (убрать файл, только процедуры с findings) |

4. После «да» — карта точек **только** в утверждённом охвате (inventory из explorer или из code-map/Review Boundaries без расширения на «весь механизм»).

### D. Правка HALT брифа (точечная)

В `entry-brief.md` / SKILL:

- HALT «список модулей не в бриф» уточнить: запрещён **сырой** inventory / коды Mxx / префиксы `pav…` как замена сценарию.
- **Разрешено** в **Охват**/**Контекст** для source=review|apply: компактные пути `.bsl` и имена процедур из handoff-секции (бюджет: Охват ≤ ~5 строк смысла; полный список — Контекст).

### E. Не создавать

- Отдельный handoff-файл explain.
- Автостарт прохода без подтверждения брифа.
- Авто-explain на каждый trivial light-review (1 файл, 0 findings) — только мягкий hint или пропуск.

---

## Файлы kit к изменению

| Файл | Изменение |
|------|-----------|
| `.cursor/skills/review/SKILL.md` | §4.4 / §7: условие propose `/opsx:explain`; запись `## Explain scope` в main report; self-check |
| `.cursor/commands/review.md`, `release-review.md` | Одна строка в description/памятке: после ревью возможен explain по охвату (опц.) |
| `.cursor/docs/review-guide.md` | Когда после ревью звать explain |
| `.cursor/skills/openspec-apply-change/SKILL.md` | acceptance/final: propose explain; писать/дополнять Explain scope в code-map или handoff-acceptance |
| `.cursor/docs/opsx-output-style.md` §5.2 | Next step / short-cut: опц. `/opsx:explain` после BSL-среза |
| `.cursor/skills/openspec-explain/SKILL.md` | Entry: ветка source=review\|apply; автозаполнение Охват; лимит scope |
| `.cursor/skills/openspec-explain/templates/entry-brief.md` | Эталон C — post-review/apply; уточнение HALT модулей |
| `.cursor/skills/openspec-explain/fixtures/voice-good-brief.md` | (опц.) второй эталон post-apply |
| `.cursor/docs/templates/brief-card.md` § B-explain | Ссылка на эталон post-review |
| `.cursor/commands/opsx-explain.md` | Пример входа `@…/review-*.md`, `@…/code-map.md` |
| `.cursor/docs/quick-start.md` / FAQ (если есть строка про explain) | Связка review/apply → explain |
| `.cursor/rules/chat-output-budget.mdc` (+ full при необходимости) | Без новых лимитов; при необходимости — примечание что Охват post-review может содержать краткий список path в Контекст |

**Не трогать (вне темы):** as-designed queue / critical-vs-agreed review disposition.

---

## Критерии приёмки

1. После `/review` (и `/release-review` при подходящем scope) в слоте «Куда дальше» / финале **может** появиться `/opsx:explain` (по правилам приоритета над fix/extend).
2. После apply acceptance/final с BSL — T-HANDOFF или short-cut **может** предложить `/opsx:explain` по карте правок.
3. В `review-*.md` и/или `code-map.md` / `handoff-acceptance-*` есть блок **`## Explain scope`** со списком files (и желательно procedures).
4. Вызов `/opsx:explain @<review|code-map|handoff>` (или эквивалент в той же сессии) строит **B-explain** со слотом **Охват** (или **Варианты** для огромного release scope), отражающим обработанный код; пользователь подтверждает до карты.
5. До «да» нет массового обхода `.bsl` / Task inventory вне утверждённой рамки.
6. HALT голоса и бюджет B-explain ≤6 слотов соблюдены; полный dump модулей не подменяет **Сценарий**/**Вопрос**.
7. Эталон брифа post-review/apply есть в `entry-brief.md` (или fixtures).
8. Explore-propose explain **не ломается**; тема as-designed не затронута.

---

## Имя ЗНИ (kebab)

**`explain-after-review-apply-scope`**

Альтернативы: `explain-scope-from-review-apply`, `opsx-explain-post-implementation-scope`.

---

## Риски / открытые вопросы

1. **Порог propose:** всегда vs только при N≥2 файлах / после fix / по явному «разбери»? Рекомендация: не предлагать на trivial light-review без findings.
2. **Release full-extension:** обязательны Варианты (Tier1 / findings-only / all) — иначе карта неподъёмна.
3. **Сосуществование next steps:** fix ask и explain в одном финале — explain только как вторичный hint после отказа от fix, или отдельной строкой «также можно»?
4. **Эвристика без `## Explain scope`:** поддерживать fallback (парсинг findings paths) для старых отчётов или только новый формат?
5. **Семантика Охват vs карта:** охват = файлы/процедуры (рамка); карта = эффекты внутри рамки — не смешивать в одном слоте.
6. **Связь с Code-Truth:** symbols из debug.md — обогащение карты или только files? Для MVP достаточно files+procedures из Boundaries/code-map.
7. **Параллельная ЗНИ** про disposition ревью — не пересекать контракты; Explain scope не должен кодировать accepted/rejected findings.

---

## Источники (прочитано / grep)

- `.cursor/commands/opsx-explain.md`, `review.md`, `release-review.md`, `opsx-apply.md`
- `.cursor/skills/openspec-explain/SKILL.md` + `templates/entry-brief.md`, `inventory-card.md`
- `.cursor/docs/templates/brief-card.md` § B-explain
- `.cursor/skills/review/SKILL.md` (§1 scope, §4.4, §7)
- `.cursor/skills/openspec-apply-change/SKILL.md` (T-HANDOFF, code-map)
- `.cursor/skills/openspec-explore/SKILL.md` (propose explain)
- `.cursor/docs/opsx-output-style.md` §5.1 / §5.2, `review-guide.md`
- Grep `.cursor` на `opsx:explain` / explain после review/apply
