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
  - reports/quality-control-2026-08-16-2.md
  - reports/architecture-new-2026-08-16.md
confidence: high
open_questions_count: 0
superseded_by: null
verdict: ГОТОВО
---

# Task readiness — kit-evolution-models-economy-profiles (повтор)

## KB references

Discovery выполнен, совпадений нет. Таксономии нет. Конфликтов с KB нет.

## Вердикт

**ГОТОВО** — по текущим артефактам оркестратор может провести ЗНИ без возврата на уточнение: правки markdown/rules/agents по `design.md` + spec + тексту задачи; ручные проверки — в сессии Cursor на границах срезов. Кода 1С и Конфигуратора в scope нет.

Прошлые пробелы G1–G4 закрыты as-is (см. ниже). Носитель независимого разбора постановки не переоткрывался: пока слага Fable нет в enum `Task`, вызов идёт на Opus 5, не на GPT-5.6 и не без `model=`.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач (markdown/rules/agents) | **OK** | Каждая `S<N>.<M>` — глагол + путь + зачем + якорь решения. Новые файлы профилей — `Создать` (в репо их нет). Правки существующих — `Заменить`/`Вынести`/`Перевести`/`Удалить` с именами файлов. Фикстура ревьювера — один путь `temp/fixtures/reviewer-diet-baseline.bsl`; источник фрагмента есть в `std-06-code-modules.md`. Закрытая таблица эскалации Fable пишется как политика + fallback Opus 5; живой вызов Fable не в обязательной приёмке. |
| 2 | Реализуемость форм и метаданных | **OK** | `form_mode: n/a`. Маркеров ручной конфигурации нет. Кода 1С в scope нет. Скрытых требований к Конфигуратору нет. |
| 3 | Разрешённость решений | **OK** | Open Question про команду смены профиля закрыта: команду не делать, строка в `/opsx:status` (задача среза профилей). «Сам или вопрос пользователю» после двух неудач субагента — рантайм-политика, не вилка реализации. Носитель независимого разбора — closed decision, не «или». Два источника фикстуры не меняют путь файла и не требуют выбора заказчика. |
| 4 | Полнота покрытия | **OK** | 35 сценариев пяти delta spec покрыты Primary, опциональной приёмкой или задачей внутри среза (сверка по spec, не только по отчёту согласованности). Срез диеты ревьювера своей дельты не создаёт — расширяет `always-apply-context-budget` «Бюджет промптов агентов». Диета `onec-code-architect.md` в spec не обещана (Non-Goals). |
| 5 | Согласованность | **OK** | `design.md` § Context больше не утверждает Fable членом enum. Задача выноса авто-исправления оставляет в delegation дословный минимум apply-reviewer (D6(в), spec «Якорь apply-reviewer», Blast Radius ADR-0003). Primary профилей не требует живого слага из первого среза. «Создать» совпадает с репо: профилей нет; `reviewer-checks.md`, `1c-writer-pipeline.mdc`, `knowledge-format.mdc`, `glossary.md`, `CHANGELOG.md` в агентах, alias-стабы и `openspec-sessions.mdc` — на месте для правок/удаления. |
| 6 | Связность и порядок | **OK** | По одному `S<N>.accept` и одному `<!-- slice-gate -->` на срез (6/6), legacy `S<N>.T<M>` нет. Граф: первый срез независим; диета контекста независима от мэппинга; диета ревьювера / профили / делегирование после диеты контекста; гигиена последняя (`S2, S4, S5`). Общие файлы (`AGENTS.md`, delegation, `review/SKILL.md`) идут в этом порядке. Обязательная приёмка профилей достижима задачами своего среза. |
| 7 | Архитектурная эстетика (правила kit) | **OK** | Лишних механизмов нет (нет файла-состояния профиля, нет новой команды смены профиля). Упаковка + тонкие профили соответствуют Why. Переизобретения БСП/1С нет. |
| 8 | User Task Contract | **OK** | Mechanical grep по телам `S<N>.<M>`: нет DENY-маркеров (тестовая ИБ, стенд, консоль, отладчик, эмуляция API, условные цепочки после verify). Прогоны в сессии Cursor стоят в `S<N>.accept`. Замеры байт, таблица обязательств, инвентарь чек-листов, поиск ссылок, базовый прогон ревьювера на фикстуре kit — работа apply-агента, не runtime-spike пользователя. |

**Precedent Coherence:** **OK**.

- Архивных delta тех же capability нет (`openspec/changes/archive/**/specs/<capability>/` пуст).
- ADR-0001: контракт чата остаётся в always-apply `chat-output-budget.mdc`; профили MUST NOT не ослабляют лимиты и HALT-список. Не revoke.
- ADR-0003: семантика не меняется; `## Blast Radius` в `design.md` заполнен (носитель полной процедуры → `review/SKILL.md`, always-apply якорь минимума apply-reviewer сохраняется). Modified Capabilities пусты — согласовано.
- KB invariant: Discovery пуст.

## Повторная проверка G1–G4 (закрыты)

| Было | Сейчас | Статус |
|---|---|---|
| G1. Поиск мёртвых слагов vs таблица Fable vs enum сборки | Задача поиска рантайм-`model=`: MAY для `claude-fable-5-thinking-high` в таблице эскалации + fallback «нет в enum → Opus 5 + одна строка». Запись таблицы: политика пишется всегда, живой вызов Fable не в обязательной приёмке. Spec «Рантайм свободен…» и «Независимый разбор…» зеркалят то же. `design.md` § Context не хардкодит Fable как член enum. | закрыто |
| G2. Вынос carve-out оставлял cue вместо обязательства | Задача выноса авто-исправления: в delegation лимит итераций **и** дословный минимум D6(в). Spec-сценарий «Якорь apply-reviewer». Указатель в apply-skill обновляется на «якорь минимума — delegation; полная процедура — review/SKILL.md шаг 4.5». Blast Radius ADR-0003. | закрыто |
| G3. Эталон BSL не назван | Путь `temp/fixtures/reviewer-diet-baseline.bsl` в задаче создания и в обязательной приёмке того же среза. Источник: `std-06-code-modules.md` (фрагменты BSL есть). Не `src/`, не объект конфигурации. | закрыто |
| G4. Приёмка профилей требовала слаг первого среза; диета архитектора висела | Primary профилей: сессия Grok 4 extra high + три конфликтных запроса. `**Зависимости:** S2` — без первого среза. Диета `onec-code-architect.md` — Non-Goals design и шапка среза диеты ревьювера. В ядре промпта ревьювера явно оставлены DESIGN AUTHORITY / QualityFlag / `prompt_contract_version`. | закрыто |

Закрытая развилка носителя независимого разбора не поднималась.

## Simplicity Check

- **Viable alternatives:** режим не выбирает новый технический путь; as-is vs точечные правки артефактов до apply. As-is достаточно.
- **Selected simplest viable design:** не применяется (оценка исполнимости, не выбор подхода).
- **Why not simpler:** —
- **Complexity budget:** правки только markdown/rules/agents; 0 хуков 1С; 0 новых объектов метаданных.

## Неблокирующие замечания (не пробелы)

Исполнитель закрывает их по design/spec без вопроса заказчику:

- В задаче согласования описаний цепочки в скиллах скобки сокращены («независимый разбор — Fable»). Полное правило — в design D1a, spec и задаче таблицы эскалации: нет слага → Opus 5 + строка. Обязательная приёмка первого среза проверяет полный текст.
- Два источника фикстуры: у `proportional-surface.md` нет фрагмента BSL; рабочий источник — `std-06-code-modules.md`. Путь файла один.
- «Вынести в `reviewer-checks.md` и соседние»: файл уже есть. Инвентарь до/после ловит потери.
- «Топ-10 on-demand по размеру/частоте»: состав на apply; spec допускает.
- Роутер профилей: `alwaysApply` в задаче не назван. Из пирамиды D4 (стаб в `AGENTS.md` → роутер → профили on-demand) и порога ≤ 34 КБ следует on-demand; контрольный замер после дописывания delegation это ловит.

## Что исполнимо as-is

- Таблица ролей Opus 5 / Gemini / Composer / inherit, двухшаговые цепочки, самосверка enum, удаление ложного «inherit нет в enum», замена дубля слага в architect-gate, tool-name-guard, таблица эскалации Fable с fallback Opus 5.
- Живой вызов обычного архитектора на `claude-opus-5-thinking-high` (слаг есть в enum этой сборки). Живой вызов Fable не требуется.
- Перенос минимума трёх session-правил, слияние BSL-guard и стабов чата, разжалование XML-guard и трёх command/context гейтов, вынос KB CONTEXT и таблицы writer pipeline с якорями D6(в), D12 (glossary + пометка init-project), замер байт, таблица обязательств, четыре smoke в чистом окне.
- Роутер + четыре профиля, MAY/MUST NOT, precedence, carve-out stub→full в профиле GPT, строка в status. Primary профилей — чат Grok + три конституционных конфликта.
- Запрет built-in explore для 1С, intent-брифы, coverage-first, эскалация после двух неудач, контрольный замер бюджета.
- Шапки «Когда загружать», shortcut triage, safety floor / promotion triggers, перенос CHANGELOG, удаление alias-стабов и `openspec-sessions.mdc`.

## Источники

- `proposal.md`, `design.md`, `tasks.md`, `debug.md` (closed_decisions: `independent_challenge_carrier`)
- `specs/subagent-model-mapping/spec.md`, `always-apply-context-budget/spec.md`, `chat-model-profiles/spec.md`, `delegation-safeguards/spec.md`, `rules-hygiene/spec.md`
- `reports/architecture-task-readiness-2026-08-16.md` (G1–G4), `reports/quality-control-2026-08-16-2.md`
- `openspec/adrs/ADR-0001-chat-facing-vs-agent-facing.md`, `openspec/adrs/ADR-0003-review-quality-disposition.md`
- Verified: enum `Task.model` этой сборки без `claude-fable-5-thinking-high`; `std-06-code-modules.md` содержит фрагменты BSL; `proportional-surface.md` — нет; профилей `model-*.mdc` в репо нет; `openspec/project.md` отсутствует (D12)
