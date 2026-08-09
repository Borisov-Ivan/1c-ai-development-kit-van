# ADR-0002: Handoff охвата в `/opsx:explain` после review/apply

**Статус:** Accepted
**Дата:** 2026-08-09
**Область:** kit / explain · review · apply
**Источник:** openspec/changes/archive/2026-08-09-explain-after-review-apply-scope/reports/architecture-new-2026-08-09.md
**Load-bearing:** no

## Контекст

После `/review`, `/release-review` и `/opsx:apply` охват обработанного кода уже известен, но `/opsx:explain` не предлагался, а бриф Охвата заполнялся вручную. Отдельный файл handoff плодил ещё один артефакт; сырой список модулей в брифе конфликтовал с HALT entry-brief.

## Решение

1. Секция `## Explain scope` живёт **внутри** review-отчёта и `code-map.md` (SSOT для apply); в handoff-acceptance — копия или ссылка. Отдельный `temp/explain-handoff-*.md` не создавать.
2. Propose `/opsx:explain` в финалах review/apply — ниже MUST_FIX / extend; trivial light-review без findings не обязан предлагать.
3. Prefill B-explain: UX-абзац в **Охват** (или **Варианты** для huge release); полный список path — только в **Контекст**; карта точек только после «да».

## Альтернативы

| Вариант | Плюсы | Минусы | Почему отклонён |
|---------|-------|--------|-----------------|
| Отдельный `temp/explain-handoff-*.md` | Чистый контракт | Ещё один файл; легко устаревает | Non-goal; дублирует отчёт/code-map |
| Автостарт explain без брифа | Меньше кликов | Нет подтверждения рамки | Ломает протокол B-explain |
| Эвристика старых отчётов без секции | Совместимость | Хрупкий prefill | Out of MVP (later) |

## Последствия

- Положительные: один handoff-формат; explain стартует с известным охватом; explore-shortcut не ломается.
- Отрицательные: старые отчёты без секции не автозаполняют Охват до повторного review.
- Нейтральные: disposition as-designed / queue-fix — вне scope (отдельная ЗНИ).

## Связи

- **Specs:** openspec/specs/explain-post-implementation-scope/spec.md
- **Changes:** archive/2026-08-09-explain-after-review-apply-scope/
- **Supersedes:** —
- **Связанные ADR:** ADR-0001
