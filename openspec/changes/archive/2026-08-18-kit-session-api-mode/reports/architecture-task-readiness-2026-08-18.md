---
report_type: task-readiness
generated_at: 2026-08-18
agent: onec-code-architect
mode: task-readiness
scope:
  change: kit-session-api-mode
  slices: [S1, S2]
  files:
    - .cursor/rules/model-selection.mdc
    - .cursor/rules/tool-name-guard.mdc
    - .cursor/rules/session-discipline.mdc
    - .cursor/docs/faq-kit.md
    - .cursor/commands/opsx-new.md
    - .cursor/commands/opsx-verify.md
    - .cursor/commands/opsx-apply.md
    - .cursor/commands/opsx-extend.md
    - .cursor/commands/opsx-explore.md
    - .cursor/commands/review.md
    - .cursor/commands/release-review.md
    - .cursor/commands/opsx-status.md
  modules: []
  capabilities:
    - session-api-mode
related_reports:
  - reports/architecture-new-2026-08-17.md
  - reports/quality-control-2026-08-18.md
confidence: high
open_questions_count: 0
superseded_by: null
verdict: ГОТОВО
---

# Task readiness — kit-session-api-mode

## KB references

Discovery выполнен, совпадений нет. Таксономии нет. Конфликтов с KB нет.

## Вердикт

**ГОТОВО** — по текущим `proposal.md` / `design.md` / `tasks.md` / `specs/session-api-mode/spec.md` оркестратор может провести ЗНИ as-is без возврата на уточнение: правки markdown-правил kit (`.cursor/rules`, `.cursor/docs`, `.cursor/commands`). Кода 1С, writer BSL и Конфигуратора в scope нет. Ось «режим сессии vs признак в project.md» не пересматривалась.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | **OK** | Каждая `S<N>.<M>` — глагол + путь файла + наблюдаемый результат + якорь D1–D7 / ADR-0001. Целевые файлы существуют и непусты. S1.1–S1.5 пишут секцию режима и два множества сбоев в `model-selection.mdc` (рядом с уже существующими «Что считать сбоем» и «Целостность цепочки Task», не смешивая списки). S1.6 — пункт 2 чеклиста `tool-name-guard.mdc` («`model` в вызове?»). S1.7 — cue 2–4 строк в `session-discipline.mdc` (Persistence / follow-up). S1.8–S1.11 и S2.9 — сверка по тексту, не выбор формулировки заказчиком. S2.1–S2.8 — одна строка / один ответ FAQ; S2.2 явно запрещает список «Флаги» / Optional flag. Место вставки в markdown исполнитель выбирает по соседним секциям файла — это не пробел постановки. |
| 2 | Реализуемость форм и метаданных | **OK** | `form_mode: n/a`. Метаданных 1С, Form.xml, Template.xml, ролей нет. Маркеров ручной конфигурации нет. Скрытого шага в Конфигураторе нет. Приёмка — чтение правил / FAQ / палитры и контрольный ход в чате apply, без ИБ. |
| 3 | Разрешённость решений | **OK** | D1–D7 выбраны (режим в оркестраторе; токены; липкая память только для лимита/недоступности/ошибки выбора модели; SSOT в `model-selection.mdc`; дешёвые команды молчат; пропуск шага 1 не отменяет шаг 2 текущего вызова; эскалация/Primary в «без API» не зовутся). Open Questions в design: нет блокирующих. «Или» в задачах — варианты токенов (`-noapi` / `--noapi`) и список команд палитры, не развилка реализации. Порядок при обоих токенах зафиксирован (последний слева направо). |
| 4 | Полнота покрытия | **OK** | Четыре Requirement spec закрыты задачами. 13/13 Scenario: S1 — «Ключ без API» (Primary), «Ключ с API» / «Новый чат» / «Память после лимита» / «Таймаут» / «Не путать» / «Эскалация» (optional accept + слои S1.1–S1.7), «Оба токена» / «Ложное слово» / «Целостность первого сбоя» (S1.8–S1.10); S2 — «FAQ» (Primary), «Подсказка в палитре» (S2.2–S2.8 + optional accept), «Команда без дорогих вызовов молчит» (S2.9). Палитра дорогих команд в tasks шире примера WHEN spec (`explore`/`extend` добавлены по design) — покрытие не дырявое. |
| 5 | Согласованность | **OK** | tasks ↔ design: файлы срезов, D1–D7, зависимость S2 после S1, Primary обоих срезов совпадают с таблицей `## Slices`. Таблицу ролей не трогать (S1.1 + S1.11) согласовано с Blast Radius. tasks ↔ spec: поле «Связь со spec» поимённо совпадает с `#### Scenario:`. D5 «session-save и аналоги» не требует отдельной задачи: spec WHEN — `/opsx:status -noapi`; S2.9 проверяет этот представитель. `openspec/project.md` сознательно вне правок (D1). |
| 6 | Связность кода и порядок задач | **OK** | Порядок: S1.1–S1.7 (запись) → S1.8–S1.11 (static) → `S1.accept` → S2.1–S2.8 → S2.9 → `S2.accept`. Ровно один `S1.accept` и один `S2.accept`; по одному `<!-- slice-gate -->` на срез; текст маркера = Primary; legacy `S<N>.T<M>` нет. S2 объявляет зависимость от S1. Общий файл `model-selection.mdc` не делится между срезами. |
| 7 | Архитектурная эстетика (Design Smells) | **OK** | Лишнего механизма нет: один признак сессии, SSOT смысла в одном правиле, cue в двух соседях, FAQ + одна строка только у дорогих команд. Нет признака в `project.md`, нет probe, нет файла-состояния, нет копипасты ключа во все команды. Дробление S1.1–S1.5 — гранулярность задач на один файл, не второй контур выбора модели. |
| 8 | User Task Contract | **OK** | В телах `S1.1–S1.11` и `S2.1–S2.9` нет user runtime-spike: нет ИБ, консоли, отладчика, эмуляции API без UX-proxy, условных цепочек «после стенда / после verify S». S1.8–S1.11 и S2.9 — агентская сверка текста. Контрольный ход `-noapi` стоит только в `S1.accept` (граница среза, не spike). Опциональное «если в чате apply случился живой лимит» — наблюдение при совпадении, не требование исчерпать квоту. Pre-check 2.1a: none. |

**Precedent Coherence:** **OK**. `design.md` § Precedent и `## Blast Radius` заполнены: ось `kit-evolution-models-economy-profiles` (двухшаговая цепочка и таблица ролей) расширяется слоем пропуска шага 1, не отменяется. Capability `session-api-mode` — новая; `subagent-model-mapping` в `openspec/specs/` ещё нет. ADR-0001: одна строка без слага после липкого сбоя (S1.3). KB invariant: Discovery пуст.

## Simplicity Check

- **Viable alternatives:** as-is vs точечные правки артефактов до apply. Архитектурный путь не выбирался.
- **Selected simplest viable design:** as-is достаточно для реализации.
- **Why not simpler:** —
- **Complexity budget:** ~12 markdown-файлов kit; 0 метаданных 1С; 0 хуков; 0 репозиторных feature flags.

## Неблокирующие замечания (не пробелы)

Исполнитель закрывает их по design/spec без вопроса заказчику:

- S2.3–S2.8 не повторяют явную фразу S2.2 «не в список Флаги / Optional flag»; смысл тот же (D5 + spec MUST NOT объявлять ключ флагом). Для `opsx-apply.md` и `review.md` строку ставить вне блока `**Флаги:**`.
- Три сценария S1 («Оба токена», «Ложное слово», «Целостность первого сбоя») и «Команда без дорогих вызовов молчит» покрыты static-задачами, не optional-буллетом accept — допустимо.
- Заголовок новой секции в `model-selection.mdc` в задаче не назван: содержание D1–D7 и запрет смешивать два множества сбоев однозначны.
- `/session-save` в D5 назван аналогом дешёвых команд; отдельной сверки нет — spec Scenario фиксирует `/opsx:status`.

## Пробелы

Нет (GAP / SUBOPTIMAL не выставлены). Сниппеты для вставки не требуются.

## Что исполнимо as-is

- Секция режима сессии в `model-selection.mdc`: токены `-noapi`/`-api` (и с двумя дефисами), границы слова, регистр, последний токен побеждает, новый чат = «с API».
- Пропуск шага 1 только на новых вызовах; шаг 2 уже ушедшего вызова обязателен; явный `-noapi` = сразу без `model=`, не отказ от делегирования.
- Липкая память только для лимита/credits, недоступности модели, ошибки выбора модели; таймаут/нераспознанная сеть — шаг 2 этого вызова без липкого режима; одна строка без слага (ADR-0001).
- Запрет Primary и самой дорогой эскалации в «без API», кроме разового явного слага; порядок слаг → токены → память → таблица ролей.
- Отличие от `--skip-architect` / `.gate-override.yaml`.
- Cue в `tool-name-guard.mdc` и `session-discipline.mdc` без копирования таблицы токенов и классификации сбоев.
- FAQ: включить / выключить / не путать с пропуском архитектора.
- Одна строка в палитре семи дорогих команд; `opsx-status.md` ключ флагом не объявляет.

## Источники

- `openspec/changes/kit-session-api-mode/proposal.md`
- `openspec/changes/kit-session-api-mode/design.md` (D1–D7, Behavior Contract, Slices, Blast Radius)
- `openspec/changes/kit-session-api-mode/tasks.md`
- `openspec/changes/kit-session-api-mode/specs/session-api-mode/spec.md`
- Целевые файлы: `model-selection.mdc` (в т.ч. «Что считать сбоем», «Целостность цепочки Task», таблица ролей), `tool-name-guard.mdc` (чеклист пункт 2), `session-discipline.mdc`, `faq-kit.md`, команды палитры и `opsx-status.md`
- `reports/quality-control-2026-08-18.md` — только как контекст покрытия срезов (13/13); выводы готовности перепроверены по живым артефактам
