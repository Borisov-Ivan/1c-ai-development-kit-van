# Системное ревью: защита от регрессии контрактов между ЗНИ

Чеклист совместимости и рисков после внедрения `precedent-regression-gate`, verify **9b**, Blast Radius, archive **5.5.b**, HALT 4, extend drift.

## Backward-compatibility

- ADR без `Load-bearing` / KB без `invariant` — трактовать как **Load-bearing: no** / **invariant: false** (см. `adr-format.mdc`, `knowledge-format.mdc`).
- Активные changes без `## Blast Radius`: шаг 9b срабатывает только при **MODIFIED/REMOVED** в дельте spec **и** пересечении с архивным **ADDED** той же capability. Чистые ADDED-only changes новых capabilities не затрагиваются.

## Производительность verify

- Glob только по `<capability>` из текущей дельты; запрет полного обхода всех архивов без фильтра.
- Бюджет **10** архивных changes; при превышении — INFO с рекомендацией `--full-precedent-audit` (не блокирующий).
- KB invariant-проверка: только якоря, пересекающиеся с `scope.files` текущего change.

## Разграничение гейтов

| Механизм | Зона ответственности |
|----------|----------------------|
| **scope-coherence-audit** (extend) | Бриф extend, счётчик debug, расползание scope |
| **precedent-regression** (9b / gate) | Дельта spec ↔ архив ADDED, отмена собственных контрактов ЗНИ |
| **code-truth-gate** | Фантомные символы, соответствие коду |
| **Substituted Authority** (`existing-mechanism-priority`) | Подмена типового кода базы |
| **openspec-specs-gate** | Наличие/структура specs vs содержательная регрессия (дополняет 9b) |

## Риски ложных срабатываний

- Реструктуризация без смены WHEN/THEN → INFO `precedent-restructure`, не CRITICAL (алгоритм 9b).
- Расширение контракта без отмены → режим `precedent-coherence-audit`, классификация `extends`, понижение severity до INFO где применимо.
- Технические правки лексикона без изменения WHEN/THEN — не триггерить CRITICAL.

## Промпт-инфляция архитектора

- **Cross-Archive Context:** не более **3** архивных changes.
- KB с `invariant: true`: не более **5** фактов в промпт.
- Цель: рост контекста не более **~30%** к предыдущему KB Discovery (ориентир для оркестратора).

## Тесты регрессии фреймворка (перед merge правок)

1. `/opsx:verify` на **трёх** архивных changes без активной дельты — OK, без новых CRITICAL от 9b.
2. Восстановить инцидентный change `2026-05-07-do2-pavlik-role-autoplace-task-access` в тестовый каталог — ожидать CRITICAL `precedent-regression` со ссылкой на `2026-04-10-do2-roli-avtopodstanovka` (или эквивалентный архивный источник).
3. `/opsx:extend` с расширением scope **без** отмены инварианта — `Drift-check: pass` сохраняется при корректном брифе.
4. `/opsx:ff` «зелёная» новая capability — ложного переполнения Cross-Archive Context нет.

См. также: `temp/reports/precedent-rollout-pilot.md`.
