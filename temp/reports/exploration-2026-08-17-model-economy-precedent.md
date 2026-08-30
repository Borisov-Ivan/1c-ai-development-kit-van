# Exploration: прецедент model-economy и слои доступности

**Дата:** 2026-08-17  
**Репозиторий:** `c:\GitHub\1c-ai-development-kit-van`  
**Change-прецедент:** `openspec/changes/kit-evolution-models-economy-profiles` (complete, 73/73)  
**Режим:** только чтение + этот отчёт  
**Existing Knowledge:** Discovery выполнен, совпадений нет  

---

## Для заказчика

В ЗНИ `kit-evolution-models-economy-profiles` уже зафиксированы: таблица ролей → Primary, `model: inherit` у агентов, самосверка enum, двухшаговая цепочка Primary → без `model=`, запрет Fable как запасной модели. **Сессионного кэша «Primary недоступен» и флагов `--noapi` / `--api` там нет** — после исчерпания лимита каждый следующий `Task` снова бьётся в Primary и только потом падает на модель чата. Это и есть корень жалобы «вся работа идёт по fallback неэффективно и некрасиво». Самый простой слой поверх: **session-cache после первого сбоя API** (не probe на старте). Признак проекта — строка в overlay `openspec/project.md`; сессионный override — флаги команды. Новый ADR не обязателен: достаточно дельты к `model-selection` + capability `subagent-model-mapping`.

---

## Свод

| Вопрос | Ответ коротко |
|---|---|
| Что уже зафиксировано | Мэппинг, inherit, enum self-check, цепочка 2 шага, Fable только закрытая эскалация, профили чата (тон/MAY, не выбор модели API) |
| Чего нет | Session-cache доступности Primary; `--noapi` / `--api`; probe квоты; файл-состояние модели |
| Почему fallback «некрасивый» | Нет памяти о сбое: каждый Primary-вызов снова падает → двойной шум |
| Рекомендуемый слой | Session-cache после первого сбоя (quota/unavailable/Invalid model) → до конца чата звать роли сразу без `model=` |
| Куда писать признак | Проект: `openspec/project.md` (overlay). Сессия: флаг команды / явная фраза пользователя |
| Документировать | Дельта `subagent-model-mapping` + правка `model-selection.mdc` / `tool-name-guard.mdc`; ADR — только если режим «доступность» станет конституцией kit |
| Связь с архивом | **directly-related** |

---

## Инварианты, которые нельзя ломать

Зафиксированы в `design.md` (D1–D3, D1a), `specs/subagent-model-mapping/spec.md`, runtime SSOT `.cursor/rules/model-selection.mdc` и `.cursor/rules/tool-name-guard.mdc`.

| Инвариант | Суть | Почему нельзя ломать |
|---|---|---|
| Таблица ролей → Primary | architect→Opus5, reviewer→gemini, simplifier→composer-2.5-fast; writer/explorer/trace/QC → без `model=` | SSOT выбора модели для работы; дубли в других файлах запрещены |
| `model: inherit` во frontmatter агентов | Конкретная модель задаётся параметром `Task.model`, не YAML | Единый контракт Cursor subagents; tool-name-guard |
| Двухшаговая цепочка | Primary (если задан) → вызов **без** `model=`; трёхступенчатые удалены | D2; при сбое шага 1 обязан выполниться шаг 2 того же `subagent_type` |
| Целостность цепочки | Нельзя считать делегирование исчерпанным и подменять отчёт оркестратором, пока не сделан финальный шаг без `model=` | После полного исчерпания — СТОП пользователю |
| Запрет Fable как fallback | Сбой Opus **не** эскалирует на Fable; Fable — только закрытый список режимов + наличие слага в enum | Иначе авария модели = счёт за самую дорогую |
| Самосверка enum | Перед **первым в сессии** вызовом с `model=` сверить слаг с описанием `Task`; нет слага → без `model=` + предупреждение; **запрет** молчаливой «похожей» модели | D3; устойчивость к дрейфу Cursor |
| Запреты в параметре `Task` | Не передавать `model="inherit"` / `"default"` / `"auto"` как retry; inherit = **отсутствие** параметра | Иначе ломается смысл второго шага |
| Профили ≠ выбор API-модели | `model-adaptation` / `model-*` — MAY длины/нарратива/делегирования; MUST NOT ослаблять гейты | Другая ось; не путать с доступностью Primary |
| Нет файла-состояния профиля | Селектор — self-knowledge; overlay в `project.md` опционален | D4 / Existing Mechanisms: сознательно отклонено `.dev.env`-состояние |

**Не ломать при добавлении слоёв доступности:** двухшаговую семантику (шаг 2 остаётся «без `model=`»), запрет Fable-as-fallback, no family guessing, inherit-через-отсутствие-параметра, таблицу ролей как SSOT.

---

## Что происходит при исчерпании лимита (факт)

### Факт по правилам (не гипотеза)

1. **Определение сбоя** (`model-selection.mdc` § «Что считать сбоем»): недоступность модели, таймаут, **лимиты/credits**, `Invalid model selection`, иные ошибки API. Содержательный отказ агента — **не** повод менять модель.

2. **На один вызов роли с Primary:** шаг 1 (`model=<Primary>`) → при сбое шаг 2 (тот же `subagent_type` **без** `model=` = модель чата).

3. **Кэша «Primary исчерпан на сессию» нет.** Единственное «первый в сессии» — самосверка **enum** (есть ли слаг в описании `Task`), не квота/credits.

4. **Следствие:** следующий независимый `Task` той же роли снова начинается с Primary. Если лимит API всё ещё исчерпан — снова failed Primary → снова fallback. При серии делегирований (architect → explorer → reviewer…) пользователь видит пачку failed-вызовов и работу «как будто всё уже на чате», но с лишним шумом и задержкой.

5. **После полного исчерпания обоих шагов одного вызова:** СТОП, сообщение пользователю; не подмена отчёта. Это **не** переключает режим на весь остаток сессии.

6. Подтверждение из verify того же change: независимый разбор упирался в лимит API и шёл на модели чата (`reports/verification-2026-08-16.md`, `verification-2026-08-16-2.md`) — поведение соответствует правилам, без session-sticky режима.

### Объясняет ли это жалобу?

**Да.** Жалоба «вся работа идёт по fallback неэффективно и некрасиво» = ожидаемое поведение текущей политики при длительном недоступном Primary: **каждый** Primary-вызов снова платит failed-шаг, хотя исход уже известен. Цепочка корректна по инварианту «не пропускать шаг 2», но **не экономна** при повторяющемся сбое квоты.

---

## Слои поверх цепочки (рекомендация)

### Три логических слоя (предложение)

| Слой | Где живёт | Что делает | Как обнаруживается |
|---|---|---|---|
| **A. Проектный** | `openspec/project.md` (overlay; создаётся `/init-project`) | Политика по умолчанию: `models: api` \| `noapi` (имена условные) | Читается оркестратором при делегировании |
| **B. Сессионный** | Память оркестратора в чате (+ опционально флаги команды) | После первого API-сбоя Primary: «Primary degraded» до конца сессии / до `--api` | Только факт сбоя `Task` (отдельного API «есть квота» нет) |
| **C. Вызовный** | Существующая цепочка | Primary → без `model=` (не ломать) | Как сейчас |

Профили чата (`model-adaptation`) — **четвёртая ось** (тон), не слой доступности. Не смешивать.

### Рекомендация: session-cache после первого сбоя (не probe на старте)

**Почему проще и честнее probe:**

- Отдельного API «есть ли квота на Opus/Gemini» в Cursor для оркестратора **нет** — единственный сигнал = сбой `Task`.
- Probe на старте команды = либо лишний платный/падающий вызов «в никуда», либо ложноположительный (Primary жив для architect, но reviewer уже в лимите).
- Session-cache: **первый** реальный вызов с Primary идёт штатно; при сбое класса «лимиты / недоступность / Invalid model» оркестратор запоминает `primary_degraded=true` и **последующие** роли с Primary вызывает сразу без `model=` (это семантически всё ещё «шаг 2 цепочки», просто шаг 1 пропускается как уже исчерпанный для сессии). Одна строка пользователю: «дорогие модели вызова недоступны — дальше на модели чата» (без слагов/имён агентов — ADR-0001).

**Честное «но»:**

1. **Ложный sticky:** краткий сбой сети/таймаут пометит сессию как degraded — до `--api` или нового чата Primary не пробуется. Смягчение: sticky только для явных сигналов лимита/credits/unavailable; для таймаута — опционально «один повтор Primary» или не sticky.
2. **Разные Primary разные квоты:** Opus исчерпан, Gemini ещё жив. Грубая политика «все Primary → chat» проще, но грубее. Тоньше (дороже в правилах): кэш **по слагу** Primary.
3. **Нет персистентности между чатами:** это плюс (нет файла-состояния, согласуется с D4 «файл-состояния нет»), минус — каждый новый чат снова «нащупывает» лимит одним failed-вызовом.
4. **Не отменяет целостность цепочки:** при первом сбое в сессии шаг 2 того же вызова **обязан** выполниться; cache влияет только на **следующие** вызовы.
5. **Writer/explorer уже без Primary** — на них cache не влияет; боль — architect/reviewer/simplifier.

**Probe на старте — отклонить как default:** нет квота-API; probe = искусственный сбой или бесполезный успех; усложняет вход команды и конфликтует с «первый tool call = Read SKILL» в командных сессиях.

---

## Стыковка `--noapi` / `--api`

Интерпретация поверх существующей цепочки (не ломая её):

| Режим | Поведение относительно Primary → chat | Целостность цепочки |
|---|---|---|
| **default (api)** | Штатно: шаг 1 Primary, при сбое шаг 2; + session-cache после сбоя | Полная |
| **`--noapi`** (форс без API-моделей вызова) | Сразу шаг 2: все роли **без** `model=` (модель чата). Primary не вызывается | Цепочка не ломается: это явный выбор «только финальный шаг»; Fable-эскалация тоже off (или только по явной просьбе — зафиксировать в spec) |
| **`--api`** | Игнорировать проектный `noapi` и session-cache; снова пробовать таблицу Primary | Обычная двухшаговая цепочка |

Precedence (согласовать с D5 профилей):

**явный флаг команды / указание пользователя → project overlay → session-cache → таблица Primary.**

- `--noapi` побеждает project `api` и отключает попытки Primary.
- `--api` побеждает project `noapi` и сбрасывает/игнорирует session degraded.
- Профили чата **не** участвуют в этом precedence (MUST NOT выбора модели API).

Куда писать признак проекта:

- **SSOT проектного режима:** строка в `openspec/project.md` (уже принятый канал overlay для профиля модели, D4). Пример смысла: `subagent_models: noapi` / `api` (точный ключ — в новой ЗНИ).
- **Не** в always-apply правилах kit по умолчанию (consumer-проекты разные).
- **Сессионный** признак — не файл: флаг команды или sticky после сбоя в контексте чата.
- Документировать в `model-selection.mdc` (поведение) + краткая отсылка в `/opsx:status` (как уже намечено для профиля в Open Questions D4).

---

## ADR vs дельта spec

| Вариант | Когда | Вердикт |
|---|---|---|
| Дельта к capability `subagent-model-mapping` + правка `model-selection.mdc` / `tool-name-guard.mdc` | Session-cache, `--noapi`/`--api`, project overlay | **Достаточно** — это расширение той же оси «как звать Task.model» |
| Дельта `chat-model-profiles` | Нет | Не то: профили = тон/MAY, не доступность API |
| Новый ADR | Если фиксируем конституцию: «режим доступности моделей — обязательный слой kit с жёстким precedence навсегда» и это пересекается с несколькими capability | **Не обязателен сейчас**; ADR-0001 уже закрывает chat-facing (не светить слаги/имена агентов при сообщении о degraded) |
| Правка ADR-0001 | Только если меняется граница chat/agent | Не требуется для cache/флагов |

**Рекомендация:** новая маленькая ЗНИ (или extend, если ещё не archive в main specs — в kit change лежит в `openspec/changes/…`, main `openspec/specs/subagent-model-mapping` не найден) с ADDED requirements: session sticky after API failure; project overlay; command flags; явный Non-Goal «нет probe квоты».

---

## Связь с архивом

**Метка: directly-related**

**Почему:** новая идея опирается на ту же capability и те же инварианты (таблица Primary, двухшаговая цепочка, запрет Fable-fallback, enum self-check). Архивная ЗНИ — прецедент «что нельзя сломать» и одновременно доказательство пробела: в Goals/Non-Goals и Existing Mechanisms **нет** сессионной проверки доступности и флагов `--noapi`/`--api` (гипотеза из входа подтверждена). Это не adjacent (не «рядом по тону профилей»), не unrelated: любой слой доступности обязан стыковаться с `subagent-model-mapping` / `model-selection.mdc`.

**Чего в архиве точно нет (подтверждение гипотезы):**

- session-cache / sticky после лимита;
- `--noapi` / `--api`;
- probe квоты;
- файл-состояние выбора модели (отклонено в D4).

**Что в архиве есть и переиспользовать:** overlay `project.md` как канал проектного override; «первый в сессии» паттерн (сейчас только для enum) — расширить смыслом degraded; сообщение одной строкой без слагов (D1a / ADR-0001).

---

## Доказательства (path:line)

### Цепочка и сбой без session-cache

- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\model-selection.mdc:30` — цепочка «два шага: Primary → без `model=`»; ошибка (в т.ч. лимиты) → второй шаг  
- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\model-selection.mdc:34` — самосверка enum **перед первым в сессии** вызовом с `model=` (только enum, не квота)  
- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\model-selection.mdc:96-98` — что считать сбоем: лимиты/credits; не содержательный отказ  
- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\model-selection.mdc:100-104` — целостность цепочки; после полного исчерпания СТОП (нет sticky-режима на сессию)  
- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\tool-name-guard.mdc:63-74` — при сбое второй шаг без `model=`; Fable не запасной  

### Инварианты мэппинга / Fable / inherit

- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\model-selection.mdc:11-14` — inherit во frontmatter; таблица = SSOT; рекомендуемый чат Grok 4  
- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\model-selection.mdc:20-28` — таблица ролей  
- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\model-selection.mdc:51` — сбой Opus не → Fable  
- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\model-selection.mdc:78` — Fable не запасная при сбое Opus  
- `c:\GitHub\1c-ai-development-kit-van\openspec\changes\kit-evolution-models-economy-profiles\design.md:44` — D2: цепочки до двух шагов  
- `c:\GitHub\1c-ai-development-kit-van\openspec\changes\kit-evolution-models-economy-profiles\design.md:36-40` — D1a: Fable не fallback после Opus  
- `c:\GitHub\1c-ai-development-kit-van\openspec\changes\kit-evolution-models-economy-profiles\specs\subagent-model-mapping\spec.md:27-32` — Requirement двухшаговой цепочки; Scenario «Сбой Primary»  
- `c:\GitHub\1c-ai-development-kit-van\openspec\changes\kit-evolution-models-economy-profiles\specs\subagent-model-mapping\spec.md:49-51` — Scenario «Сбой Opus не включает Fable»  

### Нет файла-состояния; overlay project.md

- `c:\GitHub\1c-ai-development-kit-van\openspec\changes\kit-evolution-models-economy-profiles\design.md:50` — файл-состояния нет; override — `openspec/project.md`  
- `c:\GitHub\1c-ai-development-kit-van\openspec\changes\kit-evolution-models-economy-profiles\design.md:88` — «Новых механизмов хранения/состояния не создаётся»; отклонено файл-состояние профиля  

### Профили ≠ доступность API

- `c:\GitHub\1c-ai-development-kit-van\openspec\changes\kit-evolution-models-economy-profiles\specs\chat-model-profiles\spec.md:20-21` — MAY/MUST NOT; не выбор Task.model  
- `c:\GitHub\1c-ai-development-kit-van\.cursor\rules\model-adaptation.mdc:44,56-58` — MUST NOT гейтов; длина внутри лимитов чата  

### ADR-0001 (пересечение)

- `c:\GitHub\1c-ai-development-kit-van\openspec\adrs\ADR-0001-chat-facing-vs-agent-facing.md:9,12,23` — в чат не копировать slug/имена субагентов (релевантно сообщению о degraded)  

### Архитектурный отчёт (цели / Non-Goals)

- `c:\GitHub\1c-ai-development-kit-van\openspec\changes\kit-evolution-models-economy-profiles\reports\architecture-new-2026-08-16.md:39-47` — выбран упаковка + профили; modelTier отклонён; новых механизмов хранения 0  
- Non-Goals design: `design.md:18-24` — нет UI-инфры, нет `.dev.env`, нет смены состава агентов; **доступность/квота/session-cache не в Goals**  

### Verify: лимит API на практике

- `openspec/changes/kit-evolution-models-economy-profiles/reports/verification-2026-08-16.md:117` — разбор на модели чата из‑за лимита API  
- `openspec/changes/kit-evolution-models-economy-profiles/reports/verification-2026-08-16-2.md:70` — то же  

### Main specs

- `openspec/specs/subagent-model-mapping/` — **не найден** в kit root (capability живёт в change `specs/`); при новой ЗНИ ориентир — delta в change + sync по процессу kit.

---

## Итог для постановки следующей ЗНИ (черновик)

1. Не пересматривать таблицу ролей, inherit, Fable-policy, двухшаговую семантику.  
2. Добавить: session sticky после API-сбоя Primary; project overlay `api|noapi`; флаги `--noapi` / `--api` с precedence.  
3. Явно Non-Goal: probe квоты без сигнала Task; файл-состояние между чатами.  
4. Документ: delta `subagent-model-mapping` + `model-selection.mdc` + checklist в `tool-name-guard.mdc`; ADR не обязателен.  
5. Прецедент: `kit-evolution-models-economy-profiles` — **directly-related**.
