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
  - reports/architecture-task-readiness-2026-08-18.md
  - reports/quality-control-2026-08-18.md
confidence: high
open_questions_count: 0
superseded_by: null
verdict: ГОТОВО
---

# Task readiness — kit-session-api-mode (повтор после repair инвариантов)

## KB references

Discovery выполнен, совпадений нет. Таксономии нет. Конфликтов с KB нет.

## Вердикт

**ГОТОВО** — после repair инвариантов (`tasks.md` S1.12–S1.13, согласованные D2/D3/D5/D7 в `design.md` и spec) оркестратор может провести ЗНИ as-is без возврата на уточнение. Правки markdown-правил kit. Writer BSL и Конфигуратор вне scope. Ось «режим сессии vs признак в project.md» не пересматривалась. Приёмка пользователем сейчас не оценивалась.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | **OK** | Каждая `S<N>.<M>` — глагол + путь + наблюдаемый результат + якорь D1–D7 / ADR-0001 / Scenario. Целевые файлы существуют и непусты (`model-selection.mdc`, `tool-name-guard.mdc`, `session-discipline.mdc`, `faq-kit.md`, семь команд палитры, `opsx-status.md`). S1.1–S1.5 пишут секцию режима и два множества сбоев; S1.6 — пункт чеклиста про `model`; S1.7 — cue 2–4 строк на каждом ходе. S1.8–S1.13 и S2.9 — сверка по тексту существующих файлов, не выбор формулировки заказчиком. S1.12/S1.13 явно «верифицировать по тексту» `model-selection.mdc`. |
| 2 | Реализуемость форм и метаданных | **OK** | `form_mode: n/a`. Метаданных 1С нет. Маркеров ручной конфигурации нет. Приёмка — чтение правил / FAQ / палитры и контрольный ход в чате apply, без ИБ. |
| 3 | Разрешённость решений | **OK** | D1–D7 выбраны. Open Questions: нет блокирующих. «Или» в задачах — варианты токенов и список команд палитры, не развилка реализации. Порядок при обоих токенах и при слаг+токен зафиксирован (последний токен; этот вызов со слагом, дальше без API). |
| 4 | Полнота покрытия | **OK** | Четыре Requirement spec закрыты. 13/13 Scenario: S1.12 закрывает «Токен на дешёвой команде»; S1.13 закрывает «Разовый слаг и токен в одном сообщении»; остальные — запись S1.1–S1.7 / static S1.8–S1.11 / optional accept / S2.1–S2.9. Палитра explore/extend в tasks совпадает с WHEN spec. |
| 5 | Согласованность | **OK** | tasks ↔ design: файлы срезов, D1–D7, S2 после S1, Primary совпадают с `## Slices`. Repair: токен=слово (S1.1/S1.9), молчание после лимита (S1.3), дешёвая команда не глотает сигнал (S1.1 + S1.12 + S2.9), cue на каждый ход (S1.7), палитра explore/extend (S2.5–S2.6), разовый слаг+токен (S1.4 + S1.13). Таблицу ролей не трогать (S1.1 + S1.11) согласовано с Blast Radius. `openspec/project.md` вне правок (D1). Механических замечаний и executability issues нет. |
| 6 | Связность кода и порядок задач | **OK** | Порядок: S1.1–S1.7 (запись) → S1.8–S1.13 (static, цели уже написаны предыдущими шагами) → `S1.accept` → S2.1–S2.8 → S2.9 → `S2.accept`. Ровно один accept на срез; по одному `<!-- slice-gate -->`; текст маркера = Primary; legacy `S<N>.T<M>` нет. S2 зависит от S1. Общий `model-selection.mdc` не делится между срезами. |
| 7 | Архитектурная эстетика (Design Smells) | **OK** | Один признак сессии, SSOT в одном правиле, cue в двух соседях, FAQ + одна строка у дорогих команд. Нет признака в `project.md`, probe, файла-состояния, копипасты ключа во все команды. S1.12/S1.13 — гранулярность сверки, не второй контур. |
| 8 | User Task Contract | **OK** | В телах `S1.1–S1.13` и `S2.1–S2.9` нет user runtime-spike: нет ИБ, консоли, отладчика, эмуляции API, условных цепочек «после стенда». S1.8–S1.13 и S2.9 — агентская сверка текста. Контрольный ход `-noapi` только в `S1.accept`. Опциональное «если в чате apply случился живой лимит» — наблюдение при совпадении, не требование исчерпать квоту. |

**Precedent Coherence:** **OK**. `design.md` § Precedent и `## Blast Radius` заполнены: ось `kit-evolution-models-economy-profiles` расширяется слоем пропуска шага 1, не отменяется. Capability `session-api-mode` — новая. ADR-0001: одна строка без слага (S1.3). KB invariant: Discovery пуст.

## Simplicity Check

- **Viable alternatives:** as-is vs точечные правки артефактов до apply. Архитектурный путь не выбирался.
- **Selected simplest viable design:** as-is достаточно для реализации.
- **Why not simpler:** —
- **Complexity budget:** ~12 markdown-файлов kit; 0 метаданных 1С; 0 хуков; 0 репозиторных feature flags.

## Неблокирующие замечания (не пробелы)

Исполнитель закрывает их по design/spec без вопроса заказчику:

- S1.12 дублирует формулировку S1.1 про токен на дешёвой команде — это static-якорь Scenario, не вторая постановка.
- S1.13 дублирует S1.4 про слаг+токен — то же.
- S2.3–S2.8 не повторяют явную фразу S2.2 «не в список Флаги»; для `opsx-apply.md` и `review.md` строку ставить вне блока `**Флаги:**`.
- `/session-save` в D5 назван аналогом; spec Scenario фиксирует `/opsx:status` (S2.9 + S1.12).

## Пробелы

Нет (GAP / SUBOPTIMAL не выставлены). Сниппеты для вставки не требуются.

## Что исполнимо as-is

- Секция режима в `model-selection.mdc`: токены как целые слова, регистр, последний токен побеждает, новый чат = «с API», токен на дешёвой команде переключает режим.
- Пропуск шага 1 только на новых вызовах; шаг 2 уже ушедшего вызова обязателен.
- Липкая память только для лимита/credits, недоступности, ошибки выбора модели; после липкого сбоя одна строка без слага, дальше без повтора строки.
- Запрет Primary и самой дорогой эскалации в «без API», кроме разового явного слага; слаг+токен: этот вызов со слагом, дальше без API.
- Cue в `tool-name-guard.mdc` и `session-discipline.mdc` (на каждом ходе) без копирования таблицы токенов.
- FAQ и одна строка в палитре семи дорогих команд (включая explore/extend); `opsx-status.md` ключ флагом не объявляет.

## Источники

- `openspec/changes/kit-session-api-mode/proposal.md`
- `openspec/changes/kit-session-api-mode/design.md` (D1–D7, Behavior Contract, Slices, Blast Radius)
- `openspec/changes/kit-session-api-mode/tasks.md` (включая S1.12–S1.13)
- `openspec/changes/kit-session-api-mode/specs/session-api-mode/spec.md`
- Целевые файлы проверены Glob: все 12 путей существуют
- `reports/architecture-task-readiness-2026-08-18.md` — предыдущий прогон до S1.12–S1.13; выводы перепроверены по живым артефактам
