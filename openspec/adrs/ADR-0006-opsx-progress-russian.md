# ADR-0006: Язык команд /opsx:* — русский, профиль не сильнее бюджета чата

**Статус:** Accepted
**Дата:** 2026-08-20
**Область:** kit / chat surface
**Источник:** openspec/changes/archive/2026-08-20-kit-session-noapi-visibility-and-ru-progress/reports/architecture-2026-08-19-kit-session-noapi-visibility.md
**Load-bearing:** no
**Protects-invariants:**
  - "Progress и вводная речь /opsx:* только на русском"
  - "MAY профиля не меняет язык команды и не отменяет канон лимита"

## Контекст

Стиль `/opsx:*` уже русский, но Communication и MAY профиля Grok уводили progress в английские каркасы. Бюджет чата требовал короткую строку, не язык.

## Решение

Runtime-норма языка — always-apply бюджет чата (§6 и §1b «язык»). Профиль MAY длины/тона не покрывает смену языка. Английские каркасы — примеры провала, не новые пункты HALT.

## Альтернативы

| Вариант | Почему отклонён |
|---------|-----------------|
| Расширить HALT top-20 английскими глаголами | Постановка запрещает как основную защиту |
| Только гайд стиля без always-apply | Снова проигрыш Communication |

## Последствия

- Положительные: язык команды устойчив к профилю и Communication.
- Отрицательные: самопроверка перед отправкой обязательна на каждом ходе `/opsx:*`.

## Связи

- **Specs:** openspec/specs/chat-surface-clarity/spec.md, openspec/specs/chat-model-profiles/spec.md
- **Changes:** archive/2026-08-20-kit-session-noapi-visibility-and-ru-progress/
- **Связанные ADR:** ADR-0001
