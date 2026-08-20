# Карта правок: kit-session-noapi-visibility-and-ru-progress

# Срез S1 — Сигнал лимита (2026-08-20)

- **S1.1** · правило выбора моделей · видимость режима (modified) — один режим «без API»; оркестратор не печатает `-noapi` и не говорит «включился noapi»; канон в том же ходе, в том числе пока другой вызов в фоне. [`.cursor/rules/model-selection.mdc`](../../../../.cursor/rules/model-selection.mdc):22-32
- **S1.2** · правило выбора моделей · in-flight (modified) — уже ушедший вызов не отменяется; после фона канон не повторяется; абзац «ещё летит» не нужен. [`.cursor/rules/model-selection.mdc`](../../../../.cursor/rules/model-selection.mdc):32
- **S1.3** · правило выбора моделей · токен без канона лимита (modified) — явный `-noapi` включает режим; канон лимита не обязателен, если памяти ещё не было. [`.cursor/rules/model-selection.mdc`](../../../../.cursor/rules/model-selection.mdc):30
- **S1.4** · правило выбора моделей · строка про Opus 5 (modified) — при отсутствии слага сильной модели в чат «Модель архитектора: Opus 5»; канон лимита без имени модели. [`.cursor/rules/model-selection.mdc`](../../../../.cursor/rules/model-selection.mdc):132-140
- **S1.4** · промпт архитектора · строка про Opus 5 (modified) — та же фраза вместо «дорогая эскалация недоступна». [`.cursor/skills/1c-agent-patterns/architect.md`](../../../../.cursor/skills/1c-agent-patterns/architect.md):188
- **S1.4** · протокол `/opsx:verify` · строка про Opus 5 (modified) — та же замена на шаге независимого разбора постановки. [`.cursor/skills/openspec-verify-change/SKILL.md`](../../../../.cursor/skills/openspec-verify-change/SKILL.md):242
- **S1.14** · бюджет чата (stub) · разбор сбоя субагента (modified) — дословный канон и триггер: первая строка хода, не ждать финала команды. [`.cursor/rules/chat-output-budget.mdc`](../../../../.cursor/rules/chat-output-budget.mdc):52-54
- **S1.14** · бюджет чата (полное тело) · разбор сбоя субагента (modified) — дословный канон и триггер в §5. [`.cursor/rules/chat-output-budget-full.mdc`](../../../../.cursor/rules/chat-output-budget-full.mdc):154-156
- **S1.16** · бюджет чата, правило коммуникации verify, протокол `/opsx:verify` · исключение «одно сообщение» (modified) — канон лимита и «Модель архитектора: Opus 5» не ждут карточки вердикта; «Дописываю постановку…» — progress repair. [`.cursor/rules/chat-output-budget.mdc`](../../../../.cursor/rules/chat-output-budget.mdc):54; [`.cursor/rules/verify-user-communication.mdc`](../../../../.cursor/rules/verify-user-communication.mdc):17
- **S1.17** · бюджет чата §1b · пункт «канон» (modified) — после липкого сбоя канон первой строкой; счёт пунктов полного тела = 9. [`.cursor/rules/chat-output-budget.mdc`](../../../../.cursor/rules/chat-output-budget.mdc):66-68; [`.cursor/rules/chat-output-budget-full.mdc`](../../../../.cursor/rules/chat-output-budget-full.mdc):78-90
- **S1.5** · чеклист вызова субагента · память после лимита (modified) — после липкого сбоя режим «без API», даже без токена пользователя. [`.cursor/rules/tool-name-guard.mdc`](../../../../.cursor/rules/tool-name-guard.mdc):24
- **S1.6** · дисциплина сессии · cue сигнала (modified) — память = «без API», сигнал = канон, не токен. [`.cursor/rules/session-discipline.mdc`](../../../../.cursor/rules/session-discipline.mdc):27
- **S1.7** · FAQ kit · токен vs память (modified) — ключ пишет человек; после лимита оркестратор не печатает `-noapi`. [`.cursor/docs/faq-kit.md`](../../../../.cursor/docs/faq-kit.md):18-20

# Срез S2 — Русский progress (2026-08-20)

BSL в срезе нет. Explain scope: n/a.

- **S2.1** · бюджет чата (stub) · progress (modified) — в `/opsx:*` progress только русский; язык команды важнее Communication. [`.cursor/rules/chat-output-budget.mdc`](../../../../.cursor/rules/chat-output-budget.mdc):56-58
- **S2.2** · бюджет чата (stub) · §1b пункт «язык» (modified) — progress и вводная речь на русском; не смешивать с пунктом «канон». [`.cursor/rules/chat-output-budget.mdc`](../../../../.cursor/rules/chat-output-budget.mdc):66-68
- **S2.3** · бюджет чата (полное тело) · §1b и §6 (modified) — те же нормы; в заголовке §1b 10 пунктов. [`.cursor/rules/chat-output-budget-full.mdc`](../../../../.cursor/rules/chat-output-budget-full.mdc):78-91,173-177
- **S2.4** · стиль `/opsx:*` · §2 (modified) — runtime-норма языка — бюджет чата, не этот гайд. [`.cursor/docs/opsx-output-style.md`](../../../../.cursor/docs/opsx-output-style.md):40
- **S2.5** · профиль Grok 4 · MUST NOT (modified) — MAY прямой речи не меняет язык `/opsx:*` и не отменяет канон лимита. [`.cursor/rules/model-grok4.mdc`](../../../../.cursor/rules/model-grok4.mdc):32
- **S2.6** · адаптация модели · Precedence (modified) — профиль не разрешает английский progress и не отменяет канон лимита. [`.cursor/rules/model-adaptation.mdc`](../../../../.cursor/rules/model-adaptation.mdc):46
- **S2.7** · протокол `/opsx:verify` · progress (modified) — английский progress не изобретать; допустимы русские каноны. [`.cursor/skills/openspec-verify-change/SKILL.md`](../../../../.cursor/skills/openspec-verify-change/SKILL.md):369

# Срез S3 — Маркер только при BSL (2026-08-20)

BSL в срезе нет. Explain scope: n/a.

- **S3.1** · протокол `/opsx:new` · Metadata Gate (modified) — вопрос маркера только при BSL/`src/`; пропуск только при доказанном kit-only (`developer: n/a`). [`.cursor/skills/openspec-new-change/SKILL.md`](../../../../.cursor/skills/openspec-new-change/SKILL.md):67-71
- **S3.2** · карточка брифа · Metadata Gate (modified) — то же условие пропуска. [`.cursor/docs/templates/brief-card.md`](../../../../.cursor/docs/templates/brief-card.md):45
- **S3.6** · протокол `/opsx:apply` · Metadata Prep (modified) — `n/a` не имя для маркера; при непустом `marker_scope` — defaultDeveloper или вопрос ФИО. [`.cursor/skills/openspec-apply-change/SKILL.md`](../../../../.cursor/skills/openspec-apply-change/SKILL.md):51,126-127
