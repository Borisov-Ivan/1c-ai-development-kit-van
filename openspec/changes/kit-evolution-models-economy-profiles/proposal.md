# Proposal: kit-evolution-models-economy-profiles

## Why

Таблица выбора моделей субагентов ссылается на слаги, которых нет в актуальном enum инструмента Task (`claude-opus-4-8-thinking-high` и др.) — каждый вызов архитектора начинается с ошибки выбора модели и молча деградирует на запасную модель; новые модели (Opus 5, Fable 5, GPT-5.6) не задействованы. Постоянный always-apply контекст (~54 КБ на каждый запрос) содержит ~20 КБ дублей, а поведение оркестратора никак не адаптируется под модель чата. Референс-репозиторий `ai_rules_1c` (обновление 2026-08-16) даёт проверенные принципы: тонкие профили моделей с запретом ослаблять гейты, самосверка enum, экономия свода.

Источники (verified): `temp/reports/exploration-2026-08-16-kit-critical-review.md`, `temp/reports/exploration-2026-08-16-ai-rules-1c-model-adaptation.md`.

## Metadata (comment markers)

developer: n/a
comment_suffix:
marker_style: minimal

Маркеры не применяются: kit-метапроект, изменения только в `.cursor/**` и `AGENTS.md`, кода 1С в scope нет (решение пользователя, 2026-08-16).

## Forms mode

form_mode: n/a

## What Changes

- Мэппинг моделей субагентов актуализируется под живой enum Task: обычный архитектор → `claude-opus-5-thinking-high`, simplifier → `composer-2.5-fast`, reviewer остаётся `gemini-3.1-pro`; writer/explorer наследуют модель чата. Fable (`claude-fable-5-thinking-high`) — не роль по умолчанию, а закрытая эскалация: независимый разбор постановки и тяжёлый deep-analysis; не запасная модель при сбое Opus. Рекомендуемый чат оркестратора — Grok 4 (`cursor-grok-4.6-xhigh`). Цепочки сокращаются до «Primary → без `model=`»; дубль слага в `architect-gate.mdc` заменяется ссылкой на SSOT.
- Добавляется правило самосверки enum: актуальный список слагов оркестратор читает из описания инструмента Task своей сборки; при расхождении с таблицей — не подставлять «похожую» модель молча (запрет коэрции из референса).
- Always-apply набор сокращается на ~37–40% (цель ≤ 34 КБ): полный `1c-xml-write-guard.mdc` → on-demand; три файла, консолидированные в `session-discipline.mdc`, разжалуются из always-apply; стабы `conversational-discipline` и `orchestrator-as-navigator` сливаются в `chat-output-budget.mdc`; `1c-agent-delegation.mdc` сжимается (KB CONTEXT, carve-out, дубль pipeline → on-demand); диета промпта `onec-code-reviewer.md` (67 КБ).
- Вводится слой профилей: роутер `model-adaptation.mdc` + `model-grok4.mdc` (оркестратор) и `model-fable5.mdc` / `model-gpt56.mdc` / `model-opus5.mdc` (чат, если пользователь так выбрал, и MAY в брифе субагента с соответствующим Primary). Три волны из отчёта по `ai_rules_1c` §13 входят в эту ЗНИ срезами S4 / S5 / S6. Профиль настраивает длину ответов, нарратив, охоту к делегированию — и никогда не ослабляет write-guard, LINT GATE, reviewer, HALT-триггеры.
- Точечные усиления делегирования: запрет built-in Explore (`subagent_type: "explore"`) для обследования 1С-кода; intent-брифы субагентам (цель + ограничения + критерий готовности); эскалация «2 неудачи субагента на ясной постановке → оркестратор делает сам»; coverage-first в брифах reviewer; аудит шаблонов промптов на reasoning-extraction-фразы.
- Гигиена свода: шапки «Когда загружать» в on-demand правилах (SSOT триггера — frontmatter, индекс — routing cue); decision shortcut в начало `task-triage.mdc`; секция safety floor + promotion triggers в `1c-halt-triggers.mdc`; удаление рудиментов (CHANGELOG из `.cursor/agents/`, alias-стабы `opsx-ff`/`opsx-continue`, `openspec-sessions.mdc`).

Вне scope: UI-тестовая инфраструктура (agent-browser / Playwright / Windows-MCP), вендорный скилл `1c-metadata-manage`, `.dev.env`-инфраструктура референса, отрезание legacy-слоёв `vertical-slices.mdc` / `artifact_mode` (отдельная мажорная ревизия).

## Capabilities

### New Capabilities

- `subagent-model-mapping`: актуальный мэппинг ролей, рекомендуемый чат Grok 4, Fable только как закрытая эскалация архитектора, самосверка enum, цепочки Primary → inherit, запрет молчаливой коэрции.
- `always-apply-context-budget`: состав и предельный размер always-apply набора (≤ 34 КБ вместе с AGENTS.md), правила разжалования дублей в on-demand.
- `chat-model-profiles`: профили поведения (роутер + grok4/fable5/gpt56/opus5), граница MAY/MUST NOT, precedence, неослабляемый пол гейтов.
- `delegation-safeguards`: запрет built-in Explore для 1С-кода, intent-брифы, эскалация после двух неудач субагента, coverage-first брифы reviewer.
- `rules-hygiene`: шапки «Когда загружать», decision shortcut в triage, safety floor + promotion triggers, удаление рудиментов.

### Modified Capabilities

<!-- пусто: существующие specs (review-quality-disposition, chat-surface-clarity, explain-post-implementation-scope) не затрагиваются -->

## Impact

- `.cursor/rules/`: `model-selection.mdc`, `architect-gate.mdc`, `1c-agent-delegation.mdc`, `chat-output-budget.mdc`, `session-discipline.mdc`, `1c-xml-write-guard.mdc`, `bsl-write-guard.mdc`, `conversational-discipline.mdc`, `orchestrator-as-navigator.mdc`, `command-skill-gate.mdc`, `command-session-persistence.mdc`, `context-strategy-gate.mdc`, `task-triage.mdc`, `1c-halt-triggers.mdc`; новые `model-adaptation.mdc`, `model-grok4.mdc`, `model-fable5.mdc`, `model-gpt56.mdc`, `model-opus5.mdc`.
- `.cursor/agents/`: `onec-code-reviewer.md` (диета), перенос `CHANGELOG.md`.
- `.cursor/commands/`: удаление `opsx-ff.md`, `opsx-continue.md`. Команда смены профиля отклонена в design (D4/Open Questions) — при потребности отдельным change.
- `AGENTS.md`: обновление карты SSOT и списка команд.
- Риск: consumer-проекты, скопировавшие kit, получат изменённый состав always-apply — правила поведения не ослабляются, меняется только упаковка (кроме новых профилей — аддитивно).
