---
report_type: architecture
generated_at: 2026-08-19
agent: onec-code-architect
mode: design
tier: medium
scope:
  change: null
  slices: [S1, S2]
  files:
    - .cursor/rules/model-selection.mdc
    - .cursor/rules/tool-name-guard.mdc
    - .cursor/rules/session-discipline.mdc
    - .cursor/docs/faq-kit.md
    - .cursor/rules/chat-output-budget.mdc
    - .cursor/rules/chat-output-budget-full.mdc
    - .cursor/docs/opsx-output-style.md
    - .cursor/rules/model-adaptation.mdc
    - .cursor/rules/model-grok4.mdc
    - .cursor/skills/openspec-verify-change/SKILL.md
    - openspec/specs/session-api-mode/spec.md
    - openspec/specs/chat-surface-clarity/spec.md
    - openspec/specs/chat-model-profiles/spec.md
  modules: []
  capabilities:
    - session-api-mode
    - chat-surface-clarity
    - chat-model-profiles
verdict: extends
precedent: extends
confidence: high
open_questions_count: 2
superseded_by: null
---

# Architecture: видимость «без API» и русский progress `/opsx:*`

**Исход:** достаточно дописать существующие правила (канон лимита + русский progress); новый механизм режима, файл-состояние и печать `-noapi` оркестратором не нужны. Два среза S1/S2 независимы; относительно ADR-0004 и архива `kit-session-api-mode` — **extends**, не revoke.

## KB references

Discovery совпадений нет; `openspec/knowledge/_taxonomy.yaml` в kit отсутствует — блок Existing Knowledge пуст.

- (нет KB-ID) — not relevant — таксономия и индекс KB в kit не заведены; на решение не влияли.

## Task

После лимита платных моделей человек по одной короткой русской строке понимает: дальше субагенты на модели чата. Progress команд `/opsx:*` не уходит английским из‑за Communication Cursor или профиля модели чата. Таблица Primary, двухшаговая цепочка и классификация липких сбоев не меняются.

## Complexity

Medium (правила kit, 3 capability ADDED, 0 модулей 1С).

## Chosen Approach

**Approach:** Minimal changes — расширить уже существующий канон и spec, без третьего режима.

**Rationale:**

- Поведение вызовов на инциденте PavDO уже совпало с ADR-0004 (retry без `model=`). Сломались **видимость** и **язык**, не переключение режима.
- Канон «дорогие модели недоступны — дальше на модели чата» уже есть в `model-selection.mdc` (~строка 61) и в spec «Память после лимита». Дыры: обязанность сказать **в том же ходе**; запрет цитировать платформу; запрет говорить «включился noapi»; запрет печатать `-noapi` как сигнал памяти.
- Язык `/opsx:*` уже русский в `opsx-output-style.md` §2, но без приоритета над Communication / MAY профиля. §6 budget не требует русского. Это дыра приоритета, не отсутствие SSOT.
- Новый механизм (файл-состояние, третий режим, токен в чат от оркестратора) отменён ADR-0004 Non-Goals и ограничениями этой постановки.

## Simplicity Check

- **Viable alternatives:**
  1. **Дописать правила** (видимость в `model-selection` + язык в budget/style/профиле) — 0 нового механизма.
  2. **Оркестратор печатает `-noapi` в чат** после лимита — ломает ADR-0004 (токен — слово пользователя).
  3. **Файл-состояние / `openspec/project.md`** — уже отклонено архивом и ADR-0004.
  4. **Третий режим «видимость»** — Parallel Workflow поверх того же признака.
  5. **HALT top-20 английскими глаголами** как основная защита — постановка запрещает.
  6. **Только FAQ** без обязанности канона в том же ходе — английский абзац платформы остаётся первым.
  7. **Новая capability** `session-api-visibility` — дубль `session-api-mode`.
- **Selected simplest viable design:** вариант 1.
- **Why not simpler:** вариант 6 не закрывает инцидент. Убрать S2 нельзя: английский progress был **до** лимита. Свести оба среза в одну capability хуже: язык progress не про режим API.
- **Complexity budget:** Files touched: 10 runtime + 3 spec ADDED. Hooks: 0. New procedures: 0. Feature flags: 0. New modes / state files: 0.

## Existing Mechanisms

Предпочтение: расширить канон и spec `session-api-mode`, не плодить параллельный «режим видимости».

| Механизм | Как использовать |
|----------|------------------|
| Два входа в один режим «без API» | Не добавлять третий вход. Видимость = канон, не токен. |
| Канон одной строки без имени модели | Дописать **когда** сказать и **что запрещено**; текст канона не менять. |
| Пропуск шага 1 только на новых вызовах | Не отменять фоновый `Task`. Канон в том же ходе, без абзаца «ещё летит». |
| Cue: токены → память → таблица | Усилить: память после лимита = тот же «без API», даже без `-noapi`. |
| Русский по умолчанию | Добавить приоритет над Communication / профилем. |
| Progress marker §6 | MUST русский; примеры-запреты **не** в HALT §7. |
| MAY прямой речи Grok | MUST NOT: не меняет язык `/opsx:*` и не отменяет канон. |
| Строка «эскалация недоступна в сборке» | **Другой сигнал**, не смешивать с каноном лимита. |
| FAQ «как включить ключом» | ADDED: токен vs память; почему в чате нет `-noapi` после лимита. |
| `command-session-persistence.mdc` | **Не трогать.** Cue уже в `session-discipline.mdc`. |

## Slices

| Срез | Имя | Outcome | Основные файлы | Primary | Capability |
|------|-----|---------|----------------|---------|------------|
| S1 | Сигнал лимита | После липкого сбоя — одна русская строка канона; дальше модель чата; нет `-noapi` и «включился noapi» | `model-selection.mdc`, `tool-name-guard.mdc`, `session-discipline.mdc`, `faq-kit.md` | R1 (+ R2, R3, FAQ) | `session-api-mode` ADDED |
| S2 | Русский progress | Progress `/opsx:*` только по-русски; профиль не отменяет язык | budget stub+full §6/§1b, `opsx-output-style.md` §2, `model-adaptation.mdc`, `model-grok4.mdc`, verify SKILL | R4 (+ язык R5) | `chat-surface-clarity` + `chat-model-profiles` ADDED |

**Зависимости:** нет. S1 самодостаточен. S2 самодостаточен.

**Стык §1b:** два именованных пункта, вливаемые в любом порядке: (S1) канон после липкого сбоя; (S2) progress на русском.

### S1 — видимость

Подсекция «Видимость для пользователя» в `model-selection.mdc`: один режим; оркестратор не пишет `-noapi` и не говорит «включился noapi»; канон в том же ходе (в т.ч. при фоне); текст платформы не протокол; in-flight не отменять; перед следующим `Task` с `model=` — не передавать платную модель.

FAQ в **S1**, не третий срез: токен vs память; почему после лимита нет `-noapi`.

### S2 — язык

§6: только русский; каркасы `I'll` / `Starting` / `Switched to` — примеры провала, не top-20 HALT. §2 style: приоритет над Communication. Профиль: узкий MUST NOT. Verify SKILL: отсылка, не дубль. R5: язык уже существующей строки эскалации, не второй канон лимита.

## Blast Radius

Обязательна в будущем `design.md`. Вердикт: **extends**. Supersedes нет. Не делать REMOVED ни одного Scenario архива `session-api-mode`.

| Контракт | Архивный источник | Эффект для пользователя kit | Альтернативы | Обоснование |
|----------|-------------------|-----------------------------|--------------|-------------|
| Режим в оркестраторе; нет `project.md` | ADR-0004; archive D1 | Новый чат снова «с API» | Признак в репо | Non-Goal сохранён |
| Токен — слово пользователя | ADR-0004 | После лимита ключ в чате не появляется; сигнал — канон | Печать `-noapi` | Extends |
| In-flight → шаг 2 | ADR-0004 | Фон может доиграть ошибкой; канон уже сказан | Отмена Task | Не revoke |
| Sticky только лимит/недоступность/enum | ADR-0004 D3 | Таймаут не липнет | Липнуть на любой Switched | Множества сбоев не смешивать |
| `-noapi` ≠ skip-architect | ADR-0004 | Разбор постановки остаётся | Путать с skip | Не отменяем |
| Таблица ролей и цепочка | ADR-0004; economy-profiles | После канона вызовы без платной модели | Переписать таблицу | Вне scope |
| Одна строка без имени модели | ADR-0001; archive S1.3 | Канон, не слаг и не `Switched to` | Английский парафраз | Extends наблюдаемость |
| FAQ ключ вкл/выкл | archive S2 | Токен vs память | Удалить старый FAQ | ADDED, не REMOVED |
| Русский chat-facing | ADR-0001 | Progress не на английском | HALT глаголов | Extends язык |
| MAY профиля | chat-model-profiles | Прямая речь Grok на русском | Запретить MAY целиком | Узкий MUST NOT |
| Палитра команд | archive S2 | Не трогаем | Копипаста ключей | Вне scope |

## Рекомендации для «Постановка ЗНИ»

**Why:** после лимита человек не видит режим «без API», и progress `/opsx:*` уходит по-английски, хотя вызовы уже на модели чата.

**Что менять:** S1 видимость + FAQ; S2 язык; spec только ADDED; в `design.md` — Blast Radius и вердикт extends.

**Не менять:** таблица Primary; цепочка; sticky vs timeout; файл-состояние; печать `-noapi`; третий режим; HALT top-20 глаголами; отмена независимого разбора; палитра команд.

**Приёмка без ИБ:** Grep канона и запретов; stub=full §6; FAQ токен vs память; diff без `project.md`; ручной чеклист оркестратора (T8). Primary S1 = R1, Primary S2 = R4.

**Неблокирующие:** Q1 FAQ в S1 (включить). Q2 не плодить вторую фразу эскалации.

## Ответы на явные вопросы

1. Дописать правила достаточно; новый механизм режима не нужен.
2. S1 и S2 оставить; жёсткой зависимости нет.
3. ADDED в `session-api-mode` (S1) и в существующие `chat-surface-clarity` / `chat-model-profiles` (S2). Новой capability нет.
4. Канон лимита и «эскалация недоступна в сборке» — два сигнала, не смешивать.
5. `## Blast Radius` в будущем `design.md` — да.
6. FAQ — в S1, не отдельный срез.

## Test Scenarios (кратко)

T1 канон+запреты Grep; T2 чеклист model без токена; T3 FAQ; T4 нет третьего режима; T5 русский §6; T6 MUST NOT профиля; T7 два сигнала; T8 ручной чеклист после лимита; T9 токен без канона лимита (R2).
