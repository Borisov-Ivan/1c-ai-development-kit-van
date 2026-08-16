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
  - reports/architecture-task-readiness-2026-08-16.md
  - reports/architecture-task-readiness-2026-08-16-2.md
  - reports/quality-control-2026-08-16-3.md
  - reports/architecture-new-2026-08-16.md
confidence: high
open_questions_count: 0
superseded_by: null
verdict: ГОТОВО
---

# Task readiness — kit-evolution-models-economy-profiles (после repair)

## KB references

Discovery выполнен, совпадений нет. Таксономии нет. Конфликтов с KB нет.

## Вердикт

**ГОТОВО** — по текущим артефактам оркестратор может провести ЗНИ as-is без возврата на уточнение: правки markdown/rules/agents по `design.md` + spec + тексту задачи; ручные проверки — в сессии Cursor на границах срезов. Кода 1С и Конфигуратора в scope нет.

Repair (якорь поверхности, Gate check persistence, эталон `std-06-code-modules.md`, условная запись Fable в задаче согласования цепочек) закрыт в живых proposal / design / tasks / spec. Носитель независимого разбора постановки не переоткрывался: пока слага Fable нет в enum `Task`, вызов идёт на Opus 5, не на GPT-5.6 и не без `model=`.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач (markdown/rules/agents) | **OK** | Каждая рабочая задача — глагол + путь + зачем + якорь решения. Новые файлы профилей — `Создать` (в репо их нет). Правки существующих — `Заменить` / `Вынести` / `Перевести` / `Удалить` с именами файлов. Эталон ревьювера — один существующий файл поставки `.cursor/docs/standard/std-06-code-modules.md` (фрагменты BSL есть; 0 `*.bsl` в репо; новый `.bsl` и `temp/` явно запрещены). Закрытая таблица эскалации Fable пишется как политика + fallback Opus 5; живой вызов Fable не в обязательной приёмке. |
| 2 | Реализуемость форм и метаданных | **OK** | `form_mode: n/a`. Маркеров ручной конфигурации нет. Кода 1С в scope нет. Скрытых требований к Конфигуратору нет. |
| 3 | Разрешённость решений | **OK** | Open Question про команду смены профиля закрыта: команду не делать, строка в `/opsx:status`. «Сам или вопрос пользователю» после двух неудач субагента — рантайм-политика, не вилка реализации. Условная формулировка Fable в задаче согласования цепочек — запись закрытого правила (есть слаг в enum → Fable, иначе Opus 5), не выбор заказчика. Носитель независимого разбора — closed decision, не «или». |
| 4 | Полнота покрытия | **OK** | 36 сценариев пяти delta spec покрыты Primary, опциональной приёмкой или задачей внутри среза (сверка по spec). Новый сценарий «Якорь поверхности после выноса процедуры» — design § Scenarios, связь со spec среза диеты контекста, пункт (3) задачи выноса авто-исправления. Срез диеты ревьювера своей дельты не создаёт — расширяет `always-apply-context-budget` «Бюджет промптов агентов». Диета `onec-code-architect.md` в spec не обещана (Non-Goals). |
| 5 | Согласованность | **OK** | `design.md` § Context не утверждает Fable членом enum. Задача выноса авто-исправления оставляет в delegation дословный минимум apply-reviewer **и** MUST поверхности (D6(в), spec, Blast Radius ADR-0003); вынос не сносит carve-out слияния write-guard и «post-reviewer только через writer». Primary профилей не требует живого слага из первого среза. Эталон ревьювера один и тот же в proposal Impact, таблице срезов design, задаче базовой линии и обязательной приёмке. «Создать» совпадает с репо: профилей нет; `reviewer-checks.md`, `1c-writer-pipeline.mdc`, `knowledge-format.mdc`, `glossary.md`, `CHANGELOG.md` в агентах, alias-стабы и `openspec-sessions.mdc` — на месте для правок/удаления. `openspec/project.md` отсутствует (D12). Историческая строка `temp/fixtures/…` в первом блоке `debug.md` — журнал прошлой дельты, не живой путь. |
| 6 | Связность и порядок | **OK** | По одному `S<N>.accept` и одному `<!-- slice-gate -->` на срез (6/6), legacy `S<N>.T<M>` нет. Граф: первый срез независим; диета контекста независима от мэппинга; диета ревьювера / профили / делегирование после диеты контекста; гигиена последняя (`S2, S4, S5`). Общие файлы (`AGENTS.md`, delegation, `review/SKILL.md`) идут в этом порядке. Обязательная приёмка профилей достижима задачами своего среза. |
| 7 | Архитектурная эстетика (правила kit) | **OK** | Лишних механизмов нет (нет файла-состояния профиля, нет новой команды смены профиля). Упаковка + тонкие профили соответствуют Why. Переизобретения БСП/1С нет. |
| 8 | User Task Contract | **OK** | Mechanical grep по телам `S<N>.<M>`: нет DENY-маркеров (тестовая ИБ, стенд, консоль, отладчик, эмуляция API, условные цепочки после verify). Прогоны в сессии Cursor стоят в `S<N>.accept`. Замеры байт, таблица обязательств, инвентарь чек-листов, поиск ссылок, базовый прогон ревьювера на файле поставки — работа apply-агента, не runtime-spike пользователя. Orchestrator pre-check: UTC none. |

**Precedent Coherence:** **OK**.

- Архивных delta тех же capability нет (`openspec/changes/archive/**/specs/<capability>/` пуст).
- ADR-0001: контракт чата остаётся в always-apply `chat-output-budget.mdc`; профили MUST NOT не ослабляют лимиты и HALT-список. Не revoke.
- ADR-0003: семантика не меняется; `## Blast Radius` в `design.md` заполнен (носитель полной процедуры → `review/SKILL.md`; always-apply якорь минимума apply-reviewer **и** MUST поверхности сохраняются). Modified Capabilities пусты — согласовано.
- KB invariant: Discovery пуст.

## Repair (проверено по артефактам, не по прошлым отчётам готовности)

| Что чинили | Где сейчас | Статус |
|---|---|---|
| Якорь поверхности в always-apply после выноса процедуры | D6 адресаты пункт (3); задача выноса авто-исправления пункт (3); spec Scenario «Якорь поверхности после выноса процедуры»; design § Scenarios среза диеты; Blast Radius | закрыто |
| Gate check (активная команда / ограничения скилла / СТОП) в переносимом минимуме | D6 переносимый минимум; задача переноса session-правил | закрыто |
| Эталон диеты ревьювера | `.cursor/docs/standard/std-06-code-modules.md` в proposal Impact, таблице срезов, задаче базовой линии и обязательной приёмке; файл есть, фрагменты BSL есть; `temp/` и новый `.bsl` запрещены | закрыто |
| Согласование описаний цепочки ∩ D1a ∩ D3 | Задача поиска по скиллам: независимый разбор — Fable при наличии слага в enum, иначе Opus 5 + одна строка; то же в обязательной приёмке и маркере границы первого среза | закрыто |

Закрытая развилка носителя независимого разбора (`independent_challenge_carrier`) не поднималась.

## Simplicity Check

- **Viable alternatives:** режим не выбирает новый технический путь; as-is vs точечные правки артефактов до apply. As-is достаточно.
- **Selected simplest viable design:** не применяется (оценка исполнимости, не выбор подхода).
- **Why not simpler:** —
- **Complexity budget:** правки только markdown/rules/agents; 0 хуков 1С; 0 новых объектов метаданных.

## Неблокирующие замечания (не пробелы)

Исполнитель закрывает их по design/spec без вопроса заказчику:

- Восемь сценариев покрыты рабочей задачей, но не именованным буллетом приёмки (поиск мёртвых слагов, согласование цепочек, два якоря после выноса, порог целостности поставки, два неудачных прохода, coverage-first бриф, контрольный замер после делегирования). Покрытие spec выполняется задачей.
- Задача выноса авто-исправления не цитирует заголовок сценария якоря поверхности в скобках — содержание THEN совпадает.
- Вводная фраза обязательной приёмки профилей («чат остаётся на Grok») пересекается с опциональной приёмкой первого среза; отличительная нагрузка профилей — три конфликтных запроса.
- Роутер профилей: `alwaysApply` в задаче не назван. Из пирамиды D4 (стаб в `AGENTS.md` → роутер → профили on-demand) и порога ≤ 34 КБ следует on-demand; контрольный замер после дописывания delegation это ловит.
- «Топ-10 on-demand по размеру/частоте»: состав на apply; spec допускает.
- Первый блок `debug.md` ещё упоминает `temp/fixtures/reviewer-diet-baseline.bsl` — журнал прошлой дельты; живые proposal/design/tasks этого пути не несут.

## Что исполнимо as-is

- Таблица ролей Opus 5 / Gemini / Composer / inherit, двухшаговые цепочки, самосверка enum, удаление ложного «inherit нет в enum», замена дубля слага в architect-gate, tool-name-guard, таблица эскалации Fable с fallback Opus 5.
- Живой вызов обычного архитектора на `claude-opus-5-thinking-high` (слаг есть в enum этой сборки). Живой вызов Fable не требуется.
- Перенос минимума трёх session-правил **включая Gate check**, слияние BSL-guard и стабов чата, разжалование XML-guard и трёх command/context гейтов, вынос KB CONTEXT и таблицы writer pipeline с якорями D6(в) (apply-reviewer + поверхность), D12 (glossary + пометка init-project), замер байт, таблица обязательств, четыре smoke в чистом окне.
- Роутер + четыре профиля, MAY/MUST NOT, precedence, carve-out stub→full в профиле GPT, строка в status. Primary профилей — чат Grok + три конституционных конфликта.
- Запрет built-in explore для 1С, intent-брифы, coverage-first, эскалация после двух неудач, контрольный замер бюджета.
- Шапки «Когда загружать», shortcut triage, safety floor / promotion triggers, перенос CHANGELOG, удаление alias-стабов и `openspec-sessions.mdc`.
- Базовая линия и приёмка диеты ревьювера на фрагментах BSL из `std-06-code-modules.md` без создания `.bsl`.

## Источники

- `proposal.md`, `design.md`, `tasks.md`, `debug.md` (closed_decisions: `independent_challenge_carrier`)
- `specs/subagent-model-mapping/spec.md`, `always-apply-context-budget/spec.md`, `chat-model-profiles/spec.md`, `delegation-safeguards/spec.md`, `rules-hygiene/spec.md`
- `reports/quality-control-2026-08-16-3.md` (контекст покрытия; выводы перепроверены по артефактам)
- `openspec/adrs/ADR-0001-chat-facing-vs-agent-facing.md`, `openspec/adrs/ADR-0003-review-quality-disposition.md`
- Verified: enum `Task.model` этой сборки без `claude-fable-5-thinking-high`; `std-06-code-modules.md` содержит фрагменты BSL; профилей `model-*.mdc` в репо нет; `openspec/project.md` отсутствует (D12); `openspec/glossary.md` есть; alias-стабы и `openspec-sessions.mdc` на месте для удаления; 0 файлов `*.bsl`
