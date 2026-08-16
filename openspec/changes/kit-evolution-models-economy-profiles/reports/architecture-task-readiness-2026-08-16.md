---
report_type: task-readiness
generated_at: 2026-08-16
agent: onec-code-architect
mode: task-readiness
scope:
  change: kit-evolution-models-economy-profiles
  slices: [S1, S2, S3, S4, S5, S6]
  files: []
  modules: []
  capabilities:
    - subagent-model-mapping
    - always-apply-context-budget
    - chat-model-profiles
    - delegation-safeguards
    - rules-hygiene
related_reports:
  - reports/quality-control-2026-08-16.md
  - reports/architecture-new-2026-08-16.md
confidence: high
open_questions_count: 0
superseded_by: null
verdict: НЕ ГОТОВО
---

# Task readiness — kit-evolution-models-economy-profiles

## KB references

Discovery выполнен, совпадений нет. Таксономии нет. Конфликтов с KB нет.

## Вердикт

**НЕ ГОТОВО** — оркестратор не может провести ЗНИ as-is без возврата: три столкновения в тексте задач (поиск «мёртвых» слагов vs таблица эскалации Fable при отсутствии слага в enum этой сборки; вынос carve-out ревью vs правило «обязательство остаётся в always-apply»; обязательная приёмка профилей требует живой слаг архитектора из первого среза) и одна дыра «где файл» (диета ревьювера: в kit нет `.bsl`, путь эталона не назван).

Подход не пересматривался. Ниже — только исполнимость написанного.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач (markdown/rules/agents) | **GAP** | Большинство пунктов «глагол + путь + зачем» исполнимы. Блокеры: (а) поиск рантайм-слагов запрещает слаги вне enum, а таблица эскалации Fable предписывает записать `claude-fable-5-thinking-high`, которого в enum этой сборки нет; (б) прогон ревьювера «на эталонном фрагменте BSL из документации kit» — в репозитории 0 файлов `.bsl`, путь не назван; (в) вынос § АВТО-ИСПРАВЛЕНИЕ оставляет в delegation только cue, хотя design требует дословное обязательство в always-apply якоре для диалоговых триггеров. |
| 2 | Формы и метаданные | **OK** | `form_mode: n/a`. Маркеров ручной конфигурации нет. Кода 1С в scope нет. |
| 3 | Разрешённость решений | **OK** | Open Question про `/opsx:rulesmodel`: черновое «в срезе профилей команду не делать» закрыто задачей строки в `/opsx:status`. «Сам или вопрос пользователю» после двух неудач субагента — рантайм-политика, не вилка реализации. Равноправный ремонт зависимости профилей→мэппинг — не «или» внутри задачи, а дыра порядка (критерий 6). |
| 4 | Полнота покрытия | **OK** | 34 сценария пяти delta spec покрыты Primary, опциональной приёмкой или задачей внутри среза (перепроверено по spec, не только по отчёту согласованности). Срез диеты ревьювера своей delta не создаёт — расширяет `always-apply-context-budget` «Бюджет промптов агентов». Диета `onec-code-architect.md` в spec не обещана. |
| 5 | Согласованность | **GAP** | `design.md` § Context перечисляет Fable в enum; verified runtime этой сборки — нет. Задача выноса авто-исправления ревью (cue + лимит итераций) противоречит D6(в) и spec «Разжалование без потери обязательств» п. (в). D7 «вторым приоритетом sidecar архитектора» не попал ни в задачи, ни в «вне scope». |
| 6 | Связность и порядок | **GAP** | По одному `S<N>.accept` и одному `<!-- slice-gate -->` на срез (6/6), legacy `S<N>.T<M>` нет. Объявленный граф: первый срез независим; диета контекста независима от мэппинга; диета ревьювера / профили / делегирование после диеты контекста; гигиена последняя. Дыра: обязательная приёмка профилей требует живой Primary архитектора Opus 5, который пишет только первый срез, а в зависимостях профилей указан только срез диеты контекста. Создание файлов профилей предшествует шапкам «Когда загружать» (гигиена зависит от профилей) — порядок здесь верный. |
| 7 | Архитектурная эстетика (правила kit) | **OK** | Задачи не добавляют лишних механизмов сверх design (нет файла-состояния профиля, нет новой команды смены профиля). Упаковка + тонкие профили — не over-engineering относительно Why. Переизобретения БСП/1С нет (код 1С вне scope). |
| 8 | User Task Contract | **OK** | В `S<N>.<M>` нет spike «тестовая ИБ / стенд / консоль / отладчик / эмулировать вызов». Прогоны в сессии Cursor стоят в `S<N>.accept` (допустимо). Замеры байт, таблица обязательств, инвентарь чек-листов, поиск ссылок — работа apply-агента. |

**Precedent Coherence:** **OK** (отмены load-bearing контрактов нет, `## Blast Radius` не требуется).

- ADR-0001 (chat-facing): упаковка оставляет контракт чата в always-apply `chat-output-budget.mdc`; профили MUST NOT ослабляют лимиты и HALT-список; предупреждение о смене модели — «без жаргона». Не revoke.
- ADR-0003 (review disposition): перенос полной процедуры carve-out в `review/SKILL.md` — extends (финальный as-designed/queue-fix уже там). Копия обязательства уже есть в `openspec-apply-change/SKILL.md`. Риск — не отмена ADR, а неполный якорь в always-apply (критерий 5). Ядро промпта ревьювера с `DESIGN AUTHORITY` / `QualityFlag` / `prompt_contract_version` задачи явно не фиксируют — см. пробел G4 (предотвращение случайного выноса SSOT).

## Simplicity Check

- **Viable alternatives:** режим не выбирает новый технический путь; as-is vs точечные правки артефактов до apply.
- **Selected simplest viable design:** не применяется (оценка исполнимости, не выбор подхода).
- **Why not simpler:** —
- **Complexity budget:** правки только markdown/rules; 0 хуков 1С; 0 новых объектов метаданных.

## Пробелы

### G1. Поиск мёртвых слагов vs таблица Fable vs enum этой сборки

- **Задача/артефакт:** `tasks.md` пункты замены поиска рантайм-`model=` и записи закрытой таблицы эскалации Fable; `specs/subagent-model-mapping/spec.md` сценарии «Рантайм свободен от мёртвых слагов» и «Независимый разбор постановки идёт на Fable»; `design.md` § Context (enum с Fable).
- **Что отсутствует:** согласованное правило для слага, которого нет в enum `Task.model` этой сборки (`inherit`, `claude-opus-5-thinking-high`, `composer-2.5-fast`, `cursor-grok-4.5-high`, `cursor-grok-4.6-xhigh`, `gemini-3.1-pro`, `gpt-5.6-sol-medium` — **нет** `claude-fable-5-thinking-high`). Обязательная приёмка первого среза — текст правил + живой вызов Opus 5 (исполнимо). Живой вызов Fable в этой сборке недостижим; D3 как раз предписывает не подставлять отсутствующий слаг.
- **Рекомендация:** политика Fable пишется; живой вызов Fable не входит в обязательную приёмку; поиск мёртвых слагов исключает таблицу эскалации с явной оговоркой D3.

**Сниппет — `tasks.md`, пункт поиска рантайм-слагов** (добавить к исключениям):

```
исключения: исторические записи CHANGELOG.md; анти-примеры tool-name-guard.mdc;
закрытая таблица эскалации Fable — слаг claude-fable-5-thinking-high MAY быть
записан как цель политики вместе с fallback D3 (нет в enum сборки → вызов
без model= + одна строка предупреждения) и не считается мёртвым Primary
```

**Сниппет — `tasks.md`, пункт таблицы эскалации Fable** (в конец пункта):

```
Если слаг Fable отсутствует в описании инструмента Task текущей сборки,
таблица всё равно фиксирует режимы и триггеры; фактический вызов идёт по D3
(без model= + предупреждение). Живой вызов Fable не входит в обязательную
приёмку первого среза.
```

**Сниппет — `specs/subagent-model-mapping/spec.md`**, сценарий «Рантайм свободен от мёртвых слагов», в THEN:

```
THEN слагов вне актуального enum нет, кроме: CHANGELOG.md; анти-примеров
tool-name-guard.mdc; цели закрытой эскалации Fable, явно связанной с fallback
«нет в enum → без model=» (D3)
```

**Сниппет — тот же spec**, сценарий «Независимый разбор постановки идёт на Fable», в THEN:

```
THEN в правилах указан Fable и одна строка в чат; если слаг отсутствует в
enum сборки, вызов выполняется по D3 (без model=), без подстановки «похожей»
модели. Наблюдаемая приёмка среза — текст правил, не успешный Task с этим слагом
```

**Сниппет — `design.md` § Context**, заменить перечень enum на:

```
Актуальный enum Task.model исполнитель читает из описания инструмента Task
своей сборки (D3), не из этой строки. На момент постановки в части сборок
присутствовал claude-fable-5-thinking-high; если слага нет — эскалация
описывается политикой + D3, без хардкода «пример enum».
```

### G2. Эталон BSL для диеты ревьювера не существует и не назван

- **Задача/артефакт:** прогон ревьювера до диеты и обязательная приёмка «тот же фрагмент»; QC SUGGESTION подтверждён чтением репо.
- **Что отсутствует:** путь файла. Glob `**/*.bsl` по kit = 0 файлов. `temp/fixtures/` нет. `.cursor/docs/standard/reviewer-checks.md` уже существует (справочник, не модуль). Без имени файла базовая линия и приёмка разъедутся; создать `.bsl` в `src/` нельзя (нет метаданных, writer по BSL не вызывается).
- **Рекомендация:** фикстура вне `src/`, один путь в задаче и в приёмке.

**Сниппет — заменить формулировку прогона до диеты:**

```
- [ ] S3.1 Создать при отсутствии и прогнать onec-code-reviewer на
  `temp/fixtures/reviewer-diet-baseline.bsl` (короткий синтетический модуль:
  скопировать фрагмент BSL из `.cursor/docs/standard/std-06-code-modules.md`
  или образец из `.cursor/docs/proportional-surface.md`; это фикстура kit,
  не объект конфигурации, не src/). Сохранить полный отчёт в `reports/`
  как базовую линию (D7)
```

В обязательной приёмке того же среза заменить «эталонном фрагменте» на `` `temp/fixtures/reviewer-diet-baseline.bsl` ``.

### G3. Приёмка профилей требует слаг, который пишет только первый срез

- **Задача/артефакт:** метаданные среза профилей `**Зависимости:** S2`; Primary «архитектор идёт с Primary Opus 5»; QC `undeclared-dependency` подтверждён.
- **Что отсутствует:** либо зависимость от первого среза, либо сужение Primary. Два ремонта равноправны по QC; для независимости первого среза и меньшего перекрытия приёмки выбран **сужение Primary** (живой мэппинг остаётся в первом срезе).
- **Рекомендация:** убрать клаузулу Opus 5 из Primary профилей; оставить чат Grok + три конституционных конфликта.

**Сниппет — `tasks.md`, срез профилей, Primary в шапке и в accept:**

```
**Primary acceptance:** в сессии Grok 4 extra high запустить команду workflow
→ чат остаётся на Grok; три конфликтных запроса («отвечай подробнее лимита»,
«не перепроверяй себя», «не читай стаб и полное тело») получают ответ в пользу
базового свода.
```

(Удалить «делегирование архитектору → архитектор вызывается с Primary Opus 5» / «архитектор идёт с Primary Opus 5».)

`**Зависимости:** S2.` — без изменения.

В `design.md` § Slices, строка профилей, колонка Primary acceptance — та же формулировка без Opus 5.

### G4. Вынос авто-исправления ревью оставляет cue вместо обязательства (D6(в) + ADR-0003)

- **Задача/артефакт:** вынос § АВТО-ИСПРАВЛЕНИЕ в `review/SKILL.md`; передача SSOT writer pipeline в apply-skill (указатель carve-out там: `SSOT: 1c-agent-delegation.mdc § АВТО-ИСПРАВЛЕНИЕ`).
- **Что отсутствует:** дословный минимум apply-reviewer в always-apply якоре (триггер — ход apply, не glob). Cue не заменяет обязательство (D6(в), spec always-apply п. (в)). После выноса секции указатель в apply-skill станет битым, если его не сменить.
- **Рекомендация:** полная процедура — в `review/SKILL.md`; в delegation — лимит итераций **и** дословный минимум carve-out; обновить указатель в apply-skill.

**Сниппет — конец пункта выноса авто-исправления:**

```
оставив в delegation: (1) лимит итераций writer↔reviewer = 2;
(2) дословный минимум D6(в): авто-fix только functional MUST_FIX без
QualityFlag=weak, tag design-prescribed и agreement-override; weak /
design-prescribed / agreement-override — не авто-fix, не авто-waive,
не AskQuestion в apply, одна строка-след «на /review потребуется
подтверждение качества». Полная процедура — в review/SKILL.md
```

**Сниппет — пункт передачи SSOT writer pipeline**, добавить:

```
в `.cursor/skills/openspec-apply-change/SKILL.md` заменить указатель
«SSOT: 1c-agent-delegation.mdc § АВТО-ИСПРАВЛЕНИЕ» на
«якорь минимума — 1c-agent-delegation.mdc; полная процедура — review/SKILL.md шаг 4.5»
```

**Сниппет — сжатие промпта ревьювера** (ядро, чтобы не вынести SSOT ADR-0003):

```
В ядре промпта оставить: ROLE, INPUT CONTRACT, DESIGN AUTHORITY & QUALITY
DISPOSITION (runtime-SSOT QualityFlag / Disposition / whitelist Evidence),
REPORT FORMAT с полями QualityFlag/Disposition, prompt_contract_version.
Чек-листы доменов — в on-demand; DESIGN AUTHORITY не выносить.
```

**Сниппет — вне scope D7 sidecar архитектора** (в шапку среза диеты ревьювера или в Non-Goals design):

```
Диета `.cursor/agents/onec-code-architect.md` (sidecar per-mode) — вне этой ЗНИ.
```

### SUBOPTIMAL (не блокируют apply после G1–G4)

- Таблица `design.md` § Slices не перечисляет имена `#### Scenario:` из spec (binding есть в «Связь со spec» каждого среза). Не исполнимость.
- «Вынести в `reviewer-checks.md` и соседние»: файл уже есть и большой. Исполнитель мержит в него и при необходимости колется по типам задач — допустимо без уточнения, если инвентарь до/после (следующий пункт того же среза) ловит потери.
- «Топ-10 on-demand по размеру/частоте»: состав определяется на apply замером; spec это допускает.

## Что исполнимо as-is (не пробелы)

- Таблица ролей Opus 5 / Gemini / Composer / inherit, двухшаговые цепочки, самосверка enum, удаление ложного «inherit нет в enum», замена дубля слага в architect-gate, tool-name-guard.
- Живой вызов обычного архитектора на `claude-opus-5-thinking-high` (слаг есть в enum этой сборки).
- Перенос минимума трёх session-правил, слияние BSL-guard и стабов чата, разжалование XML-guard и трёх command/context гейтов, вынос KB CONTEXT и таблицы writer pipeline, D12 (glossary + пометка init-project), замер байт, таблица обязательств, четыре smoke в чистом окне.
- Роутер + четыре профиля, MAY/MUST NOT, precedence, carve-out stub→full в профиле GPT, строка в status.
- Запрет built-in explore для 1С, intent-брифы, coverage-first, эскалация после двух неудач, контрольный замер бюджета.
- Шапки «Когда загружать», shortcut triage, safety floor / promotion triggers, перенос CHANGELOG, удаление alias-стабов и `openspec-sessions.mdc`.

## Источники

- `proposal.md`, `design.md`, `tasks.md`
- `specs/subagent-model-mapping/spec.md`, `always-apply-context-budget/spec.md`, `chat-model-profiles/spec.md`, `delegation-safeguards/spec.md`, `rules-hygiene/spec.md`
- `reports/quality-control-2026-08-16.md` (учтён, расхождения с файлами проверены)
- `openspec/adrs/ADR-0001-chat-facing-vs-agent-facing.md`, `openspec/adrs/ADR-0003-review-quality-disposition.md`
- `openspec/specs/review-quality-disposition/spec.md`
- `.cursor/skills/openspec-apply-change/SKILL.md` (указатель SSOT авто-исправления)
- `.cursor/rules/1c-agent-delegation.mdc` § АВТО-ИСПРАВЛЕНИЕ
- Verified runtime: enum `Task.model` этой сборки (без `claude-fable-5-thinking-high`); Glob `**/*.bsl` = 0
