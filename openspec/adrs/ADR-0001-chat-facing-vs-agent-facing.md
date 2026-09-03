# ADR-0001: Граница chat-facing vs agent-facing и язык Mode Gate

**Статус:** Load-Bearing
**Дата:** 2026-08-01
**Область:** kit / chat surface
**Источник:** openspec/changes/archive/2026-08-01-chat-surface-clarity/reports/architecture-new-2026-08-01.md
**Load-bearing:** yes
**Protects-invariants:**
  - "В чат копируются только продуктовые формулировки; skill/compile/Gate/Schema/slug агентов — agent-facing"
  - "Вопрос режима формы — три русских варианта (Конфигуратор / Form.xml в репозитории / модуль формы) без жаргона поставки kit"
  - "Полный handoff со Schema и таблицами — только в reports; в чате thin"
  - "Entry-бриф не содержит списка KB и slug субагентов"

## Контекст

Каноны и AskQuestion-шаблоны kit сами нарушали Тест понятности: разработчик 1С не мог выбрать вариант из одного сообщения без словаря внутренних имён. Точечная правка одного Mode Gate не закрывала утечки в new/apply/status/review.

## Решение

1. Править только chat-facing тексты (copy-paste в чат, эталоны «хорошо», thin handoff/status). Agent-facing таблицы `form_mode`/skill, тела pipeline и промпты Task остаются.
2. Канон Mode Gate в чате — три русских варианта; условие skill — только после выбора, agent-only.
3. Thin chat vs файл: Schema и markdown-таблицы срезов — только в `reports/handoff-*.md`.
4. KB в entry-брифе запрещён; имена субагентов в чате запрещены единообразно (opsx / lexicon / brief-card).

## Альтернативы

| Вариант | Плюсы | Минусы | Почему отклонён |
|---------|-------|--------|-----------------|
| Только Mode Gate | Малый diff | Не закрывает apply/status/review | Не достигает цели |
| Новый параллельный гайд стиля | «Чистый» документ | Четвёртый SSOT | Плодит расхождения |

## Последствия

- Положительные: единый язык чата для потребителя kit; grep-приёмка chat-facing зон.
- Отрицательные: большой diff по skills — править только chat-facing абзацы.
- Нейтральные: логика vertical-slices / verify Layer не меняется.

## Связи

- **Specs:** openspec/specs/chat-surface-clarity/spec.md; openspec/specs/explore-report-intake/spec.md; openspec/specs/explore-report-promote/spec.md; openspec/specs/split-form-layout-modes/spec.md
- **Changes:** archive/2026-08-01-chat-surface-clarity/; archive/2026-09-02-explore-reports-into-change/; archive/2026-09-02-skip-form-mode-module-only/
- **Supersedes:** —
- **Связанные ADR:** —
