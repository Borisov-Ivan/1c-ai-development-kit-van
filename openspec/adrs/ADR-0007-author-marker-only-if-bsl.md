# ADR-0007: Вопрос маркера автора только если будет BSL

**Статус:** Accepted
**Дата:** 2026-08-20
**Область:** kit / metadata gate
**Источник:** openspec/changes/archive/2026-08-20-kit-session-noapi-visibility-and-ru-progress/reports/architecture-task-readiness-2026-08-19-3.md
**Load-bearing:** no
**Protects-invariants:**
  - "Пропуск вопроса маркера только при доказанном kit-only"
  - "n/a закрывает гейт и не попадает в маркер кода"

## Контекст

`/opsx:new` всегда спрашивал маркер автора. Для эволюции kit без BSL вопрос лишний. Молчаливый пропуск при деловой постановке без литерала `.bsl` опасен: BSL может появиться позже.

## Решение

Спрашивать, если в постановке есть `.bsl` / `src/` / расширение, или kit-only не доказан. Kit-only: `developer: n/a`, гейт закрыт. На apply при непустом `marker_scope` — defaultDeveloper или один вопрос ФИО; в маркер `n/a` не писать.

## Альтернативы

| Вариант | Почему отклонён |
|---------|-----------------|
| Всегда спрашивать | Шум на kit-only ЗНИ |
| Молча `n/a` если нет литерала `.bsl` | Деловая постановка без пути всё равно может дать BSL |

## Последствия

- Положительные: kit-only ЗНИ без лишнего вопроса.
- Отрицательные: эвристика kit-only должна смотреть постановку, не Impact.

## Связи

- **Specs:** openspec/specs/sequential-gate-questions/spec.md
- **Changes:** archive/2026-08-20-kit-session-noapi-visibility-and-ru-progress/
