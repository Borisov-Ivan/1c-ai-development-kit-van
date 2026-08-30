## Срез S1 — передача на приёмку: scenario-map-readability-meaning

**Change:** scenario-map-readability-meaning
**Schema:** spec-driven
**Прогресс:** 26/27 задач [x] (приёмка среза S1.accept: [ ])

### 1. Что реализовано

Шаблон панели рисует два средства: граф со связями (полосы по слою, легенда, прокрутка, перенос длинного ряда) и таблицу смысловых колонок. Шапка скрывается живым переключателем; клик выбирает узел, файл открывается кнопкой. Скилл и роль сборщика принимают `header.medium`, проверяют смысл по полям манифеста при скрытой шапке и считают порог по правилам выбранного средства. Добавлены эталон таблицы и эталон «полотно есть — смысла нет»; хороший эталон графа стартует с исхода и держит ловушку на событии сброса.

### Карта правок (перед тестом)

См. секцию `2026-08-30` в `reports/code-map.md`.

- **S1.1** · шаблон панели · полосы по слою — узлы одного слоя в одной полосе; подпись — имя слоя, не ранг. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):165-198
- **S1.4** · шаблон панели · скрыть шапку — переключатель прячет заголовок и вывод. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):422-433
- **S1.15** · шаблон панели · аннотация у якоря — не правая колонка. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):280-292
- **S1.23** · шаблон панели · бюджет разборчивости — натуральный размер, прокрутка, перенос ряда длиннее пяти. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):231-277
- **S1.24** · шаблон панели · таблица колонок — строка = узел, кнопка доказательства. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):448-456

## Explain scope (handoff)

- source: apply
- change: scenario-map-readability-meaning
- focus: slice-S1
- report: openspec/changes/scenario-map-readability-meaning/reports/code-map.md

### 2. Что проверить СЕЙЧАС

**Primary acceptance:** попросить карту сценария по теме с несколькими отчётами → открыть панель штатной кнопкой среды → скрыть шапку → назвать ответ на вопрос шапки и ловушку; имена сущностей читаются без сжатия всего полотна; стартово выбран носитель исхода.

Остальные сценарии — см. `tasks.md` (опционально).

### 3. Следующие задачи

| Задача | Действие | Тип | Исполнитель | Зависит от | Статус |
|--------|----------|-----|-------------|------------|--------|
| `S1.accept` | Принять срез «Читаемая карта со смыслом» | Ручной тест | пользователь | рабочие задачи среза | `[ ]` |

### 4. Как вернуться

`/opsx:apply scenario-map-readability-meaning` — новая сессия начнётся с запроса вердикта (принят / не принят / дефект в предыдущем срезе). Если нужно изменить постановку — `/opsx:extend scenario-map-readability-meaning`; затем снова `/opsx:apply scenario-map-readability-meaning`.

### 5. Blockers

Нет.

### 7. Short-cut

Если уже проверено и принято — напишите обычной фразой («принято», «срез S1 принят»), отмечу без повторной простыни в чате.
