# Exploration: признак «проект без API» в `openspec/project.md`

Дата: 2026-08-17  
Репозиторий: `c:\GitHub\1c-ai-development-kit-van`  
Режим: только чтение исходников + запись этого отчёта  
Existing Knowledge: Discovery выполнен, совпадений нет (подтверждено: готового поля/секции noapi в каноне `project.md` нет).

---

## Для заказчика

Сейчас в kit **нет** готового места «проект без API». Канон `openspec/project.md` задаётся `/init-project` (Phase 4) и покрывает продукт, пути, соглашения OpenSpec и overlay комментариев BSL — **не** политику вызова моделей Cursor.

Логично завести **новую подсекцию** в `## Соглашения` (не YAML, не overlay маркеров BSL). Запись по просьбе «отметь проект как noapi» уже закрывается протоколом **capture-to-project** (зеркало → подтверждение → Write). Отдельный обязательный шаг интервью в `/init-project` полезен как опция при первом запуске, но не обязателен для минимального решения.

В самом репозитории kit файла `openspec/project.md` **нет по дизайну**; у потребителя без файла — как «init не пройден»: дефолт = с API, пути не подставляются, overlay маркеров пуст.

---

## Свод

| Вопрос | Ответ в одну строку |
|--------|---------------------|
| Канон секций | Phase 4 `init-project-protocol.md`; секции «политика агентов / модели» **нет** |
| Куда класть noapi | Новая `###` под `## Соглашения`; ключ в стиле `defaultDeveloper` |
| Почему не overlay BSL | Overlay = маркеры/ФИО/`framework_contract_version`; Phase 4.5 sync только их |
| Запись по просьбе | `capture-to-project`: Read/каркас → зеркало → confirm → Write — **достаточно** |
| Нужен ли шаг init | Желателен короткий вопрос в интервью; не блокер для capture |
| Docs (минимум) | protocol Phase 4 + capture + 1 FAQ; quick-start одна строка про `/init-project` |
| Имя | Заголовок: «Политика моделей Task»; ключ: `taskModelMode: chat-only` |
| Нет `project.md` | Kit: норма (D12). Потребитель: не инициализирован → дефолт «с API» |

Слои (как устроить мысленно, без домена 1С):

1. **Базовый свод kit** — `model-selection.mdc` (Primary → fallback без `model=`), `model-adaptation.mdc` (профили чата).
2. **С API (дефолт)** — нет признака в `project.md` → оркестратор передаёт Primary-слаги как сейчас.
3. **Без API (признак)** — в `project.md` явно `taskModelMode: chat-only` → все `Task` без `model=` (модель чата), без попыток Primary/API-роутинга.

Уже есть задел: `model-adaptation.mdc` говорит «опциональный override — строка в overlay `openspec/project.md`», но **форма секции в Phase 4 не определена**. Признак noapi / `taskModelMode` как раз закрывает этот пробел (рядом с будущими override профиля, не смешивая с BSL-overlay).

---

## Канон секций project.md

**SSOT каркаса:** `.cursor/docs/init-project-protocol.md` → Phase 4 (команда `/init-project` только отсылает к протоколу).

### Список секций (канон)

1. `# OpenSpec: <название проекта>`
2. Поле шапки (не YAML frontmatter): `framework_contract_version: 2026-06`
3. Одно предложение-описание
4. `## Продукт`
5. `## Назначение` (Проблема / Цель / Аудитория)
6. `## Область`
   - `### Ключевые возможности`
   - `### Принципы`
   - `### Техническая область`
7. `## Внешние зависимости`
8. `## Структура репозитория` (таблица путей + принцип)
9. `## Соглашения`
   - `### Идентификаторы изменений`
   - `### Спецификации`
   - `### Задачи`
   - `### Код`
   - `#### Разработчик по умолчанию` — ключи `defaultDeveloper`, `cfMarkerPrefix`
10. `## Форматы и соглашения по комментариям BSL`
    - intro + ссылка на `marker-canon.md`
    - `### Whitelist предрелиза`
    - `### Обязательный контроль (соблюдение формата)`
    - `### Расширения allow-list AP-054` (опционально)

### Framework-управляемые (Phase 4.5 / overlay-шаблон)

Только:

- `framework_contract_version`
- `#### Разработчик по умолчанию` (шаблон ссылок)
- `## Форматы и соглашения по комментариям BSL` (структура таблиц, не VALUE-строки)

Источник: `.cursor/templates/project-overlay.template.md`.

### Есть ли секция «политика агентов / модели / ограничения»?

**Нет.** Ни в Phase 4, ни в overlay-шаблоне, ни в `capture-to-project.mdc` как именованный тип договорённости.

Смежные, но другие смыслы:

- `## Внешние зависимости` — продуктовые/инфра API 1С (сервисы, облака), Блок 5 интервью; **не** Cursor Task API.
- `model-adaptation.mdc` — упоминает project overlay override **без** канонической секции.
- `model-selection.mdc` — SSOT выбора `Task.model`; читает enum сборки, **не** `project.md`.

---

## Куда класть признак (рекомендация + отвергнутые места)

### Рекомендация

**Новая подсекция** под `## Соглашения`:

```markdown
### Политика моделей Task

- **taskModelMode:** `chat-only` — вызовы субагентов только моделью чата (без параметра `model=` / без Primary API-роутинга).
```

Семантика по умолчанию (как просил заказчик):

| Состояние | Смысл |
|-----------|--------|
| Секции/ключа **нет** | **С API** — действует таблица Primary из `model-selection.mdc` |
| `taskModelMode: chat-only` | **Без API** — все `Task` без `model=` |
| (опционально позже) `taskModelMode: api` | Явное «с API»; избыточно, если дефолт = отсутствие ключа |

Почему сюда:

- `## Соглашения` уже держит **проектные правила работы агентов/артефактов** (ID change, specs, код, ФИО маркеров) — политика вызова моделей того же класса.
- Стиль ключей совпадает с `defaultDeveloper` / `cfMarkerPrefix` (camelCase + жирная метка).
- Не попадает под Framework Contract Sync → consumer VALUE не затрётся merge overlay.
- Рядом можно позже положить строку override профиля чата (то, что уже намекает `model-adaptation.mdc`), не смешивая с BSL.

### Отвергнутые места

| Место | Почему нет |
|-------|------------|
| **YAML frontmatter** | У `project.md` нет YAML `---`; единственное поле шапки — `framework_contract_version:` как строка после H1. Новый FM сломает стиль и парсинг ожиданий агентов. |
| **`project-overlay.template.md` / framework-managed** | Overlay = маркеры BSL + ФИО + версия контракта. noapi — VALUE среды Cursor, не грамматика комментариев; Phase 4.5 не должен sync’ить политику API. |
| **Таблица Whitelist / Обязательный контроль** | Про распознавание `//` комментариев; семантика API моделей сюда чужеродна. |
| **`## Внешние зависимости`** | Про интеграции продукта (HTTP, облака 1С), Блок 5; путаница «API продукта» vs «API Cursor». |
| **`## Структура репозитория`** | Только пути cf/cfe (`project-paths.mdc`). |
| **Отдельный файл** (`.dev.env`, rule always-apply) | Design профилей моделей уже отверг файл-состояние; SSOT договорённостей проекта — `project.md` + capture. |
| **Только устная договорённость / chat-lexicon** | Не переживает сессию; lexicon — словарь запретов жаргона, не хранилище флагов. |

### Почему не в overlay-шаблоне комментариев BSL

Шаблон явно перечисляет, что **не** входит в overlay: Продукт, Назначение, Структура, принципы и т.д. Управляемые блоки — только версия контракта, разработчик по умолчанию, таблицы комментариев. Признак noapi не про маркеры и не должен участвовать в Framework Contract Sync.

---

## Протокол записи по просьбе

### Как сейчас (capture-to-project)

Триггер: пользователь просит зафиксировать договорённость в проект / `project.md` / соглашения (без обязательной slash-команды).

Протокол:

1. **Read или каркас** — есть файл → прочитать стиль/секции; нет → Phase 0 скелет OpenSpec + полный шаблон Phase 4 + только явно согласованное + `framework_contract_version`.
2. **Зеркало** — показать целевую секцию/фрагмент (или полный черновик при создании с нуля).
3. **Confirm + Write** — писать только после явного «ок» / правки+«да».

Ограничения: без домыслов; не дублировать MECHANISM marker-canon; BSL-договорённости → overlay-таблицы.

### Достаточно ли для «отметь проект как noapi»?

**Да, протокола capture достаточно**, если агент знает каноническое имя секции/ключа (после доработки docs/protocol):

1. Read `openspec/project.md` (или каркас Phase 4, если файла нет).
2. Зеркало: фрагмент `### Политика моделей Task` с `taskModelMode: chat-only`.
3. После «ок» — Write.

Отдельный **обязательный** шаг `/init-project` не нужен для минимального UX «отметь сейчас».

### Нужен ли шаг в `/init-project`?

| Вариант | Рекомендация |
|---------|--------------|
| Минимальный | Только capture + строка в Phase 4 каркасе (пустая/заглушка или отсутствие секции = с API) |
| Удобный | Опциональный вопрос в Phase 3 (новый короткий блок или хвост Блока 6/«среда»): «Субагенты через API-модели Cursor или только модель чата?» — предзаполнение «с API»; при «без API» сразу писать секцию |
| Не делать | Отдельная slash-команда / всегда-apply rule только ради флага |

`/init-project` уже создаёт пустой `project.md` в Phase 0 и заполняет каркас в Phase 4; признак — VALUE, его можно не спрашивать, пока пользователь не скажет.

Связь с runtime (для будущего apply-change, не часть этой разведки): читатели признака — `model-selection.mdc` / оркестратор перед `Task`; иначе флаг будет «мёртвым текстом» в `project.md`.

---

## Документы, которые трогать

### Минимальный набор (без расползания)

| Документ | Зачем | Объём |
|----------|--------|-------|
| `.cursor/docs/init-project-protocol.md` | Каркас Phase 4 + (опц.) вопрос интервью | MUST: 5–15 строк секции в шаблоне |
| `.cursor/rules/capture-to-project.mdc` | Явно: просьба noapi / «без API» → секция + ключ, зеркало→Write | MUST: короткий абзац/пример |
| `.cursor/docs/faq-kit.md` | Сейчас **нет** ни слова про `project.md` / init — один Q&A «как отметить проект без API» | SHOULD: 5–8 строк |
| `.cursor/docs/quick-start.md` | Сейчас таблица команд **без** `/init-project` | SHOULD: 1 строка в таблице «Первичная настройка → `/init-project`» |

### Не трогать в первой итерации (или только одна ссылка)

| Документ | Почему отложить |
|----------|-----------------|
| `AGENTS.md` | Уже есть строка про `project.md` + capture; достаточно при желании дописать «политика моделей Task» в тот же bullet — не отдельный раздел |
| `chat-lexicon.md` | Не про хранение флагов; `noapi`/`chat-only` не HALT-жаргон чата |
| `project-overlay.template.md` | Не framework-managed |
| `README.md` | Уже есть строка `/init-project` в таблице; дублировать FAQ не нужно |
| `bsl-comment-formats-project.md` / `marker-layers-guide.md` | Другой домен (маркеры) |
| `model-selection.mdc` / `model-adaptation.mdc` | Нужны для **поведения** агента после введения признака (следующий change), не для «куда писать» |

### Замечание по текущим пробелам docs

- `quick-start.md` и `faq-kit.md` **молчат** про `/init-project` и `project.md` (grep по этим путям — пусто).
- `README.md` упоминает `/init-project` одной строкой таблицы.
- `AGENTS.md:53` — SSOT: overlay/пути + capture.

---

## Поведение если project.md нет

### Репозиторий kit (этот репо)

- Файл **отсутствует намеренно** (D12 в change `kit-evolution-models-economy-profiles`): стартовый `project.md` в kit не заводят, чтобы не перезаписать consumer при поставке.
- Поведение задокументировано: блок путей в промптах агентов **опускается**; overlay маркеров пуст → строгая гигиена `marker-canon`; override профиля в adaptation — опционален «если файл есть».

Это **не** «проект без API»; это **шаблон kit без consumer-контекста**.

### Потребительский проект без `openspec/project.md`

Интерпретация: **не прошёл `/init-project`** (или не завершил Phase 4), а не «noapi».

Ожидаемое поведение агента сегодня:

| Подсистема | Без `project.md` |
|------------|------------------|
| Пути cf/cfe | Не из чего читать → не выдумывать `src/cf`; по `project-paths` / delegation — опускать блок или остановиться до init |
| Whitelist маркеров | Пустой overlay → строгая гигиена |
| Профиль чата | Базовый свод / self-knowledge; overlay override нет |
| Выбор `Task.model` | Таблица Primary как есть (= **с API**, пока нет признака) |
| Просьба «отметь noapi» | `capture-to-project` **может создать** скелет OpenSpec + Phase 4 каркас + секцию политики — после зеркала и confirm |

Рекомендация для канона после введения признака:

- Нет файла / нет ключа → **с API** (не трактовать отсутствие init как noapi).
- Явный `taskModelMode: chat-only` → без API.
- Если пользователь просит noapi при отсутствии файла — capture создаёт файл (не молчаливый дефолт в воздухе).

---

## Доказательства (path:line)

### Команда и SSOT протокола

- `.cursor/commands/init-project.md:10` — первое действие: Read `init-project-protocol.md`; до протокола не писать `project.md`.
- `.cursor/commands/init-project.md:14` — SSOT фаз в протоколе, не в команде.
- `.cursor/docs/init-project-protocol.md:65` — Phase 0: создание пустого `openspec/project.md`.
- `.cursor/docs/init-project-protocol.md:123-145` — Phase 2 триаж; framework-секции перечислены (версии, разработчик, BSL) — **без** политики моделей.
- `.cursor/docs/init-project-protocol.md:222-224` — Блок 5 «Внешние зависимости»: внешние сервисы (API, облака) — продуктовый смысл.
- `.cursor/docs/init-project-protocol.md:283-373` — Phase 4 полный каркас секций (канон списка выше).
- `.cursor/docs/init-project-protocol.md:343-346` — образец ключей `defaultDeveloper`, `cfMarkerPrefix`.
- `.cursor/docs/init-project-protocol.md:383-388` — Phase 4.5 управляемые секции (узкий список).

### Overlay-шаблон

- `.cursor/templates/project-overlay.template.md:9-15` — шапка `framework_contract_version`.
- `.cursor/templates/project-overlay.template.md:19-27` — «Разработчик по умолчанию».
- `.cursor/templates/project-overlay.template.md:32-62` — только таблицы комментариев BSL.
- `.cursor/templates/project-overlay.template.md:66-72` — что **не** входит в overlay (продукт, пути, принципы…).

### Capture

- `.cursor/rules/capture-to-project.mdc:10-12` — триггер фиксации в project.md / соглашения.
- `.cursor/rules/capture-to-project.mdc:16-29` — Read/каркас → зеркало → Confirm + Write.
- `.cursor/rules/capture-to-project.mdc:18-20` — при отсутствии файла: Phase 0 + шаблон Phase 4.
- `.cursor/rules/capture-to-project.mdc:39-41` — связь с init-project Phase 0/4/4.5/Блок 7.

### Docs потребителя (пробелы)

- `.cursor/docs/quick-start.md:20-28` — таблица команд **без** `/init-project`.
- `.cursor/docs/faq-kit.md` — разделы explore/new, формы, поставка, session; **нет** project.md/init/noapi.
- `README.md:72` — строка «Первичная настройка проекта | `/init-project`».
- `AGENTS.md:53` — project.md создаётся `/init-project`; kit отсутствует; + capture + project-paths.

### Модели / overlay без формы секции

- `.cursor/rules/model-adaptation.mdc:16` — «Опциональный override — строка в overlay `openspec/project.md`».
- `.cursor/rules/model-adaptation.mdc:38-41` — precedence: пользователь → project overlay → профиль → базовый свод.
- `.cursor/rules/model-selection.mdc:20-30` — таблица Primary; цепочка Primary → без `model=` при сбое API.
- `.cursor/rules/model-selection.mdc:98` — ошибки API как триггер fallback.
- `openspec/changes/kit-evolution-models-economy-profiles/specs/chat-model-profiles/spec.md:35-40` — overlay побеждает профиль; форма секции не специфицирована.
- `openspec/changes/kit-evolution-models-economy-profiles/design.md:84` — D12: `project.md` в kit не заводить.

### Пути и отсутствие файла в kit

- `.cursor/rules/project-paths.mdc:11` — SSOT путей = секция «Структура репозитория».
- `.cursor/rules/1c-agent-delegation.mdc:92` — в kit файл отсутствует → блок путей опускается.
- Проверка на диске 2026-08-17: `openspec/project.md` в kit-репо — **ABSENT**.

### Стиль ключей / слои маркеров (для аналогии имени)

- `.cursor/docs/marker-layers-guide.md:36-37` — `defaultDeveloper`, `cfMarkerPrefix` в project.md.
- `.cursor/docs/bsl-comment-formats-project.md:4-5` — project.md = VALUES; marker-canon = MECHANISM.

---

## Рекомендуемое каноническое имя (итог для п.5)

| Роль | Значение |
|------|----------|
| Заголовок секции (человекочитаемый) | `### Политика моделей Task` |
| Машинный ключ | `taskModelMode` |
| Значение «без API» (user «noapi») | `chat-only` |
| Дефолт без ключа | режим **с API** (Primary по `model-selection.mdc`) |
| Синонимы в чате для capture | «noapi», «без API», «только модель чата», «не вызывать API-модели» → писать `taskModelMode: chat-only` |

Не использовать как имя секции голый `noapi` (жаргон без контекста) и не класть в `framework_contract_version`.

---

## Следующий шаг (вне этой разведки)

1. Зафиксировать секцию в Phase 4 + пример в capture.  
2. Отдельным change научить `model-selection` / оркестратор читать `taskModelMode` перед `Task`.  
3. FAQ + одна строка quick-start.
