## Why

Оркестратор копирует в чат каноны и AskQuestion-шаблоны, которые сами нарушают Тест понятности: жаргон kit (`skill`, имена гейтов, Schema, имена агентов) и процессные преамбулы. Разработчик 1С не может выбрать вариант из одного сообщения. Правка одного Mode Gate не закрывает утечки в new/apply/verify/status/review.

## What Changes

- Переписать chat-facing каноны и «хорошие» эталоны (Mode Gate, decision-block, lexicon, faq/quick-start, handoff) без жаргона поставки kit.
- Вычистить copy-paste / AskQuestion в new, apply, status, review и шаблонах verify.
- Свести конфликты SSOT в opsx-output-style (имена агентов, KB в брифе) с brief-card и lexicon.
- Привязать «спроси пользователя» к decision-block или brief-card B2; зафиксировать grep-приёмку chat-facing зон.
- **Не** менять agent-facing тела слоёв verify, XML/BSL guards и промпты субагентов (кроме явных user-facing вставок).

## Capabilities

### New Capabilities

- `chat-surface-clarity`: требования к текстам оркестратора в чат — Тест понятности, запрет жаргона kit в copy-paste канонах, разделение thin-chat vs файл отчёта.

### Modified Capabilities

- (нет — в `openspec/specs/` ещё нет capability-спеков kit chat surface)

## Impact

- Файлы: `.cursor/rules/forms-mxl-mode-gate.mdc`, `.cursor/docs/templates/decision-block.md`, `.cursor/docs/chat-lexicon.md`, `.cursor/docs/faq-kit.md`, `.cursor/docs/quick-start.md`, `.cursor/docs/opsx-output-style.md`, `.cursor/docs/casebooks/form-module-notes.md`, skills explore/new/apply/verify/status/review (chat-facing фрагменты), опц. `ux-acceptance-isolated-chat.md`.
- Потребители kit: после поставки `.cursor` поведение чата `/opsx:*` становится читаемым без знания внутренних имён движка.
- Метапроект: ветка `fix/chat-surface-clarity`; папку change в main потребителей не мержить.

## Scope

- In scope: chat-facing тексты (каноны «для чата», AskQuestion prompt-блоки, брифы, thin handoff, faq/quick-start).
- Out of scope: Layer/GO в technical audit, XML write guard тела, промпты Task, код 1С / Form.xml.

## Metadata (comment markers)

developer:
comment_suffix:
marker_style: minimal

## Forms mode

form_mode: n/a
