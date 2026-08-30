# Exploration: флаги команд, слои API/моделей, точка `--noapi`/`--api`

**Дата:** 2026-08-17  
**Репозиторий:** kit `1c-ai-development-kit-van` (не конфигурация 1С)  
**Режим:** только чтение + этот отчёт  
**user-goal:** как устроить слои «доступность моделей / без API / с API», куда писать признак проекта и что документировать.

**Existing Knowledge:** Discovery выполнен, совпадений нет.  
**Archive hypothesis (`kit-evolution-models-economy-profiles`):** подтверждена — выбор модели в `model-selection.mdc`, сессионной проверки *доступности/лимитов* в том change не было; есть лишь «самосверка enum перед первым `model=`».

---

## Для заказчика

Сейчас **нет общего парсера флагов**: каждый command.md объявляет свои ключи, а соответствующий SKILL.md читает их из текста сообщения пользователя (LLM-разбор). Дорогие модели субагентов задаёт **одна таблица** — `.cursor/rules/model-selection.mdc`; скиллы на неё ссылаются, не дублируют слаги. Узнать лимит API Cursor **до** вызова нельзя — только наличие слага в описании `Task` и сбой самого `Task`. Для `--noapi`/`--api` лучше один контракт в правилах моделей + опциональный дефолт в `openspec/project.md`, а не копия в 40 command-файлах.

---

## Свод

| Вопрос | Ответ |
|--------|--------|
| Общий парсер флагов? | **Нет.** Конвенция: `.cursor/commands/*.md` → Read `SKILL.md` → шаг «Parse флаги» / разбор в Entry Protocol. |
| Кто жжёт API-модели? | Оркестратор через `Task(model=…)` по таблице: architect (Opus/Fable), reviewer (Gemini), simplifier (Composer Fast). Writer/explorer/trace/QC — **без** `model=` (модель чата). |
| Сессионный кэш доступности? | **Нет.** Есть handoff `temp/session-notes.md`, persistence протокола команды, и «первая сверка enum» в `model-selection.mdc` — не probe лимитов. |
| Probe лимита до вызова? | **Нет API/MCP.** Сигналы: enum в описании `Task`; ошибка вызова (лимиты, Invalid model). |
| Куда вставлять `--noapi`/`--api` | SSOT поведения → `model-selection.mdc` (+ тонкий cue в `tool-name-guard` / session-discipline). Дефолт проекта → `openspec/project.md`. В command.md — одна строка-ссылка только у команд, которые зовут дорогие `Task`. |

---

## Флаги сегодня (таблица: команда, флаг, смысл, кто парсит)

**Механизм:** нет кода-парсера и нет общего `flags.md`. Пользовательский текст команды → оркестратор (после Read скилла) интерпретирует `--ключ` по инструкции скилла/команды.

| Команда | Флаг | Смысл | Кто парсит | Политика? |
|---------|------|--------|------------|-----------|
| `/opsx:apply` | `--slice S<N>` | Только один срез | SKILL apply §1b (+ список в command) | Режим выполнения |
| `/opsx:apply` | `--since-slice S<N>` | Начать с среза N | SKILL apply §1b | Режим |
| `/opsx:apply` | `--step-by-step` | Пауза после каждой задачи | SKILL apply §1b | Режим |
| `/opsx:apply` | `--batch` | Все срезы без slice-gate | SKILL apply §1b | **Да — обход пауз приёмки** |
| `/opsx:new` | `--skip-architect "<причина>"` | Обход Architect Gate + `.gate-override.yaml` | SKILL new (Design Gate) | **Да — обход gate** |
| `/opsx:extend` | `--from-review\|--from-report\|--from-debug\|--from-verify\|--from-architecture\|--from-explore <path>` | Источник расширения постановки | SKILL extend Entry | Источник (не gate) |
| `/opsx:extend` | `--code-sync` | Артефакты догоняют код | SKILL extend | Режим протокола (B2) |
| `/opsx:verify` | *(нет user-ключей)* | Режим выбирает скилл по артефактам/тексту | — | — |
| `/opsx:explore`, `/opsx:explain` | *(нет)* | Свободный ввод | — | — |
| `/opsx:archive` | `--force-legacy` | Архив при непринятых `S<N>.accept` | SKILL archive §3.5 | **Да — обход slice-gate приёмки** |
| `/opsx:bulk-archive`, `/opsx:sync` | *(нет `--*`)* | Имена change | SKILL | — |
| `/opsx:status` | `--short`, `--reports` | Урезанный вывод / таблица отчётов | SKILL status | Вывод |
| `/opsx:overview` | `--tz <path>`, `--audience фа\|заказчик` | Тон обзора | command + SKILL overview | Вывод |
| `/opsx:knowledge-add` | `--no-bundle`, `--ttl <days>` | Не копировать source / TTL | SKILL knowledge-add | Режим записи |
| `/opsx:knowledge-audit` | `--domain`, `--overdue`, `--status`, `--ids`, `--action`, `--no-reuse-test`, `--reindex`, `--metrics`, `--taxonomy-sync`, `--from-archive`, `--structure-check` (+ `--force-delete` с action) | Фильтры/режимы аудита KB | SKILL knowledge-audit | Часть — деструктивные с `--action` |
| `/review` | `--full` | Полное ревью, off light-triage | SKILL review | **Да — обход light-review** |
| `/release-review` | *(нет; `release_mode=true` зашит)* | Предрелиз | command → SKILL review | Режим команды |
| `/session-save\|restore\|retro`, `/init-project`, `/opsx:knowledge-init` | *(нет пользовательских `--`)* | — | — | — |

**Не путать** с CLI OpenSpec (`openspec list --json`, `openspec status --change … --json`) — это инструменты скилла, не флаги slash-команды.

**Internal (не user-палитра):** verify → `extend --from-verify` в режиме repair-from-verify без чата.

### Политика / override (кратко)

- **`--skip-architect`** — единственный легальный escape Architect Gate на `/opsx:new` (аудит в `.gate-override.yaml`). Layer 4 verify **не** обходится этим флагом.
- **`--full`** — отключает light-review triage в `/review`.
- **`--batch`** — отключает остановки slice-gate в apply.
- **`--force-legacy`** — архив без закрытия приёмочных задач срезов.

---

## Кто жжёт конкретные модели

### SSOT

`.cursor/rules/model-selection.mdc` — таблица Primary, двухшаговая цепочка Primary → без `model=`, закрытая эскалация Fable, самосверка enum «перед первым в сессии вызовом с `model=`».

Дублирующие указатели (без своей таблицы слагов): `tool-name-guard.mdc`, `1c-agent-patterns/SKILL.md`, `architect-gate.mdc`, отдельные шаблоны architect/reviewer.

### С `model=` (дороже / конкретный API-slug)

| Роль | Primary | Команды/скиллы, которые обычно запускают |
|------|---------|------------------------------------------|
| `onec-code-architect` | `claude-opus-5-thinking-high`; Fable при `design-challenge` / тяжёлом `deep-analysis` | `/opsx:new`, `/opsx:verify` (L2.5/L4/L5), `/opsx:explore` (gate), `/opsx:extend` (аудиты), `/review` (архит. ветка) |
| `onec-code-reviewer` | `gemini-3.1-pro` | `/opsx:apply` (после writer), `/review`, `/release-review` |
| `onec-code-simplifier` | `composer-2.5-fast` | `/review` (REFACTOR/поверхность), apply при surface-якоре |

Скиллы **не** хардкодят слаги в большинстве мест: пишут «по `model-selection.mdc`» или «без `model=`». Исключение по смыслу — verify: явно «Task без `model=`» для QC и «закрытая эскалация Fable» для challenge/loop.

### Без `model=` (модель чата)

| Роль | Где |
|------|-----|
| `onec-code-writer` | apply, review-fix |
| `onec-code-explorer` | explore, review Tier 2, extend `--code-sync` |
| `onec-trace-analyst` | explore (трасса) |
| `openspec-quality-controller` | verify Layer 2 |

### Слои для дизайна economy (рекомендуемая карта)

1. **Доступность слага** — enum в описании инструмента `Task` (уже есть самосверка).  
2. **Без API-override** (`--noapi` / project default) — все `Task` без `model=` (чат); Fable/Opus/Gemini не запрашивать.  
3. **С API** (default kit сегодня) — таблица Primary + fallback без `model=` при сбое.  
4. **Явный `--api`** — форсировать политику Primary даже если project.md сказал noapi (сессионный override).

---

## Точка однократной проверки за сессию

| Механизм | Что даёт | Probe лимитов? |
|----------|----------|----------------|
| `model-selection.mdc` «перед первым в сессии вызовом с `model=`» | Сверка слага с enum `Task` | **Нет** — только «slug есть/нет» |
| `command-session-persistence.mdc` | Протокол команды на каждом ходе | Нет |
| `temp/session-notes.md` (`/session-save`) | Handoff между чатами | Нет; шаблон Current/Next/Decisions/Links |
| Отдельный probe credits/availability | — | **Отсутствует** |

**Ближайшая точка «старт команды» для однократной логики:**

1. Сразу после Entry Protocol скилла (после обязательного Read `SKILL.md` по `command-skill-gate`) — **до** первого `Task`, **или**  
2. Внутри чеклиста `tool-name-guard` / абзаца самосверки `model-selection` при **первом** вызове с `model=` в сессии.

Запись результата (если понадобится кэш режима): поле в runtime-памяти оркестратора **или** строка в `temp/session-notes.md` / маленький `temp/session-model-mode.md` (сейчас такого файла нет). Не путать с `openspec/project.md` (долгоживущий дефолт проекта).

---

## Можно ли узнать лимит до вызова

**Нет.** В kit и в доступных MCP на момент отчёта нет инструмента «usage / credits / model quota».

Что реально есть:

| Сигнал | Когда | Что означает |
|--------|-------|--------------|
| Слаг в описании `Task` | До вызова (чтение схемы инструмента) | Модель **в enum сборки**, не «есть кредиты» |
| Ошибка `Task` | После вызова | Недоступность, таймаут, лимиты/credits, `Invalid model selection` |
| Fallback без `model=` | После сбоя Primary | Политика уже в `model-selection.mdc` |

**Следствие для дизайна «probe на старте»:** бесплатный probe лимита невозможен. «Прогрев» через пустой `Task` жжёт квоту. Имеет смысл: (a) декларативный режим `--noapi`/`project.md`, (b) lazy: первый сбой Primary → пометить сессию «API недоступен» и дальше не слать `model=`, (c) сверка enum без вызова.

---

## Варианты вставки `--noapi`/`--api`

### A. Один SSOT-контракт (рекомендуется)

**Файлы:**  
- Поведение: `.cursor/rules/model-selection.mdc` (новая секция «Режим API / no-API»).  
- Cue перед Task: одна строка в `tool-name-guard.mdc`.  
- Дефолт проекта: секция в `openspec/project.md` (через `/init-project` / `capture-to-project.mdc`), напр. `subagent_api: default|noapi`.  
- Документация для человека: короткий абзац в `AGENTS.md` или faq; **не** 40 копий.

**Приоритет:** явный флаг в сообщении → дефолт `project.md` → поведение kit (сегодня = API Primary).

**Плюс:** одна правка меняет все команды, которые уже обязаны читать `model-selection` перед `Task`.  
**Но:** оркестратор должен помнить режим на follow-up (persistence); флаги не видны в палитре command.md, пока не добавить одну строку-ссылку у «дорогих» команд.

### B. Правка каждого `command.md` (+ зеркало в каждом SKILL)

**Плюс:** флаги видны в палитре Cursor у каждой команды.  
**Но:** 20+ файлов, дрейф формулировок, команды без `Task` (status, sync, session-*) получат бессмысленный шум; verify уже принципиально «без ключей в палитре».

### C. Только `project.md`, без slash-флагов

**Плюс:** ноль копипасты в commands.  
**Но:** нельзя быстро форсировать «сегодня без API» без правки файла; хуже UX для разовой экономии.

### Практичная комбинация

A + тонкие упоминания **только** у команд с дорогими `Task`: `opsx-new`, `opsx-verify`, `opsx-apply`, `opsx-explore`, `opsx-extend`, `review`, `release-review`. Остальным — достаточно SSOT.

---

## Риски

1. **`--noapi` vs Architect Gate / Layer 4** — без Opus/Fable независимый challenge деградирует до чата; нужен явный риск в чате / `.gate-override` / согласие (как при исчерпании цепочки сейчас).  
2. **`--skip-architect` ≠ `--noapi`** — разные оси (пропуск gate vs модель вызова).  
3. **Ложный «probe»** — принять наличие слага в enum за «лимит ОК».  
4. **Копипаста флагов** — разъезд семантики между apply/new/review.  
5. **Кэш «API мёртв» на всю сессию** — лимит мог восстановиться; нужен `--api` или сброс.  
6. **Writer уже на чате** — `--noapi` экономит в основном reviewer/architect/simplifier, не весь apply.  
7. **release-review** жёстко тянет Gemini-reviewer — noapi сильнее бьёт по предрелизу.

---

## Доказательства (path:line)

```27:37:.cursor/skills/openspec-apply-change/SKILL.md
1b. **Parse флаги команды** (см. `.cursor/commands/opsx-apply.md`):
   | `--slice S<N>` | выполнить **только** срез S<N> ...
   | `--batch` | все оставшиеся срезы без остановок на slice-gate ...
```

```15:19:.cursor/commands/opsx-apply.md
**Флаги:**
- `--slice S<N>` — выполнить **только** срез S<N> ...
- `--batch` — выполнить **все** оставшиеся срезы без остановок на slice-gate ...
```

```16:17:.cursor/commands/opsx-new.md
Optional flag: `--skip-architect "<причина>"` to bypass mandatory Architect Gate.
```

```12:13:.cursor/commands/review.md
**Флаги:**
- `--full` — полное ревью файлов (отключить light-review triage).
```

```8:10:.cursor/commands/opsx-verify.md
Глубину прогона выбирает оркестратор внутри skill (без ключей в палитре).
```

```20:34:.cursor/rules/model-selection.mdc
| `onec-code-architect` | `claude-opus-5-thinking-high` |
| `onec-code-writer` | *(без `model`)* |
| `onec-code-reviewer` | `gemini-3.1-pro` |
...
Перед **первым в сессии** вызовом с `model=` оркестратор сверяет слаг Primary с этим списком.
```

```96:98:.cursor/rules/model-selection.mdc
Неуспешный ответ `Task`: недоступность модели, таймаут, лимиты/credits, `Invalid model selection`...
```

```63:65:.cursor/rules/tool-name-guard.mdc
... Перед первым в сессии вызовом с `model=` — самосверка слага с описанием инструмента `Task`.
При сбое или `Invalid model selection` — **второй шаг**: вызов **без** параметра `model` ...
```

```404:409:.cursor/skills/openspec-verify-change/SKILL.md
| 2 | `openspec-quality-controller` | — (без `model=`) | ...
| 4 | `onec-code-architect` | `design-challenge` | ...
| 5 | `onec-code-architect` | `task-readiness` | ...
```

```19:21:.cursor/skills/session-save/SKILL.md
## Current
## Next
## Decisions
## Links
```

```280:280:.cursor/skills/openspec-verify-change/SKILL.md
Layer 4 нельзя «обойти» прогоном `--skip-architect`, переданным в new.
```

**MCP:** поиск инструментов `model|usage|limit|billing|credit` — совпадений нет (2026-08-17).

**Архивная гипотеза:** change `kit-evolution-models-economy-profiles` ввёл самосверку enum и двухшаговый fallback; сессионного probe доступности/лимитов не добавлял (см. tasks S1.4, spec `subagent-model-mapping`).

---

## Итог для следующей постановки

1. Слои: enum-доступность → режим noapi/api (декларатив) → Primary+fallback при сбое.  
2. Признак проекта: `openspec/project.md`; сессионный override: `--noapi`/`--api`.  
3. Документировать: одна секция в `model-selection.mdc` + cue в `tool-name-guard` + опционально 6–7 command.md.  
4. Не строить «probe лимита на старте» как обязательный `Task`.
