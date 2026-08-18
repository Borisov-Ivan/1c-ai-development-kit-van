# Architecture self-review — sequential-ui-mode-questions

**Дата:** 2026-07-31  
**Режим:** Design Gate fallback (agent unavailable — API limit)  
**Пометка:** self-review fallback, agent unavailable

## Контекст

Эволюция kit: UX одного вопроса за ход; split `form_mode`/`layout_mode`; Mode Gate на design. Источник: explore `temp/reports/exploration-2026-07-31-sequential-ui-mode-questions.md`, proposal/design/specs в change.

## Вердикт

**design OK с оговорками** — правки не блокируют tasks; ниже SUGGESTION.

## Проверка Decisions

| Решение | Оценка |
|---------|--------|
| `form_mode` / `layout_mode` | OK, согласовано с подтверждённым брифом |
| END TURN между гейтами | OK; нужен явный HALT в SKILL self-check |
| Mode Gate на design | OK; снимает батч с Metadata |
| Legacy `artifact_mode` → оба канала | OK, обязательно в apply/verify |
| `[form:…]` вне scope | OK |

## Behavior Contract / resume

- Контракт наблюдаемый и тестируемый сценариями specs.
- Resume: не переспрашивать валидные `form_mode`/`layout_mode` — зафиксировано.
- Дыра (SUGGESTION): явно описать, что при `form_mode` заполнен, а `layout_mode` пуст при наличии Template в tasks — STOP/extend, не молчаливый default (в design Risks уже есть fallback; усилить в tasks S2).

## Срезы

- S1 / S2 вертикальны: S1 = наблюдаемый порядок вопросов; S2 = разные режимы + apply.
- Primary S1 достижим задачами правки SKILL/brief-card.
- Primary S2 достижим Mode Gate + apply/verify consumers.
- Нет foundation-only среза.

## Риски батчинга

Mitigation (END TURN + self-check) достаточны при дисциплине оркестратора; остаточный риск — модель игнорирует SKILL → приёмка S1 ловит регрессию.

## Рекомендуемые правки design (необязательные до tasks)

1. В Decisions п.2 уточнить: для ЗНИ без UI писать `form_mode: n/a` и `layout_mode: n/a` (не оставлять секцию только с legacy `artifact_mode: n/a` после миграции текста gate).
2. В Risks добавить: пустой один из режимов при UI-задаче на соответствующий артефакт → блокер verify/apply.

## Knowledge conflicts

Нет.
