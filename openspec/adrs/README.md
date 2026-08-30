# Architecture Decision Records

| ADR | Название | Статус | Дата | Область |
|-----|----------|--------|------|---------|
| [ADR-0001](ADR-0001-chat-facing-vs-agent-facing.md) | Граница chat-facing vs agent-facing и язык Mode Gate | Load-Bearing | 2026-08-01 | kit / chat surface |
| [ADR-0002](ADR-0002-explain-scope-handoff-from-review-apply.md) | Handoff охвата в `/opsx:explain` после review/apply | Accepted | 2026-08-09 | kit / explain · review · apply |
| [ADR-0003](ADR-0003-review-quality-disposition.md) | Ортогональный QualityFlag / Disposition в code-review | Accepted | 2026-08-10 | kit / code-review |
| [ADR-0004](ADR-0004-session-api-mode.md) | Сессионный режим с API / без API по ключу в чате | Load-Bearing | 2026-08-18 | kit / выбор моделей субагентов |
| [ADR-0005](ADR-0005-noapi-visibility-canon-same-turn.md) | Видимость режима без API — канон в том же ходе | Accepted | 2026-08-20 | kit / chat surface · выбор моделей |
| [ADR-0006](ADR-0006-opsx-progress-russian.md) | Язык команд /opsx:* — русский, профиль не сильнее бюджета | Accepted | 2026-08-20 | kit / chat surface |
| [ADR-0007](ADR-0007-author-marker-only-if-bsl.md) | Вопрос маркера автора только если будет BSL | Accepted | 2026-08-20 | kit / metadata gate |
| [ADR-0008](ADR-0008-scenario-map-native-parent-registration.md) | Карта сценария — нативная регистрация панели родителем | Superseded by ADR-0010 | 2026-08-28 | kit / scenario map canvas |
| [ADR-0009](ADR-0009-scenario-map-main-view-answers-header.md) | Главный вид карты сценария отвечает на вопрос шапки | Superseded by ADR-0010 | 2026-08-30 | kit / scenario map canvas |
| [ADR-0010](ADR-0010-visual-explanation-panel.md) | Визуальное объяснение текущего ответа на панели рядом с чатом | Load-Bearing | 2026-08-31 | kit / visual explanation |
