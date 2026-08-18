# Срез S1 — Режим сессии (2026-08-18)

- **S1.1** · правило выбора моделей · секция «Токены в сообщении» (created) — разбор `-noapi` / `-api` как целых слов, `--api-key` не токен, дешёвые команды тоже переключают режим. [`.cursor/rules/model-selection.mdc`](.cursor/rules/model-selection.mdc):22-30
- **S1.2** · правило выбора моделей · секция «Пропуск шага 1 цепочки» (created) — на новых вызовах сразу модель чата; уже ушедший вызов обязан сделать шаг 2. [`.cursor/rules/model-selection.mdc`](.cursor/rules/model-selection.mdc):43-47
- **S1.3** · правило выбора моделей · секция «Два множества сбоев» (created) — липнет только лимит / недоступность / ошибка выбора модели; таймаут не липнет; одна строка без повтора. [`.cursor/rules/model-selection.mdc`](.cursor/rules/model-selection.mdc):49-61
- **S1.4** · правило выбора моделей · секция «Порядок перед вызовом» (created) — слаг → токены → память → таблица ролей; разовый слаг с `-noapi` на этот вызов. [`.cursor/rules/model-selection.mdc`](.cursor/rules/model-selection.mdc):32-41
- **S1.5** · правило выбора моделей · секция «Не путать с `--skip-architect`» (created) — разбор постановки остаётся, `.gate-override.yaml` не создаётся. [`.cursor/rules/model-selection.mdc`](.cursor/rules/model-selection.mdc):63-65
- **S1.6** · чеклист вызова · пункт про `model` (modified) — в режиме без API не передавать платную модель, кроме разового override. [`.cursor/rules/tool-name-guard.mdc`](.cursor/rules/tool-name-guard.mdc):24
- **S1.7** · дисциплина сессии · cue режима (created) — на каждом ходе: токены, память, таблица ролей; follow-up не сбрасывает. [`.cursor/rules/session-discipline.mdc`](.cursor/rules/session-discipline.mdc):27

# Срез S2 — Подсказка в палитре (2026-08-18)

- **S2.1** · FAQ kit · секция «Режим без API» (created) — как включить и выключить ключом и чем это не пропуск архитектора. [`.cursor/docs/faq-kit.md`](.cursor/docs/faq-kit.md):12-16
- **S2.2** · палитра `/opsx:new` · строка про ключ (created) — не в Optional flag. [`.cursor/commands/opsx-new.md`](.cursor/commands/opsx-new.md):10
- **S2.3** · палитра `/opsx:verify` · строка про ключ (created). [`.cursor/commands/opsx-verify.md`](.cursor/commands/opsx-verify.md):10
- **S2.4** · палитра `/opsx:apply` · строка про ключ (created) — не в списке «Флаги». [`.cursor/commands/opsx-apply.md`](.cursor/commands/opsx-apply.md):10
- **S2.5** · палитра `/opsx:extend` · строка про ключ (created). [`.cursor/commands/opsx-extend.md`](.cursor/commands/opsx-extend.md):10
- **S2.6** · палитра `/opsx:explore` · строка про ключ (created). [`.cursor/commands/opsx-explore.md`](.cursor/commands/opsx-explore.md):10
- **S2.7** · палитра `/review` · строка про ключ (created) — не в списке «Флаги». [`.cursor/commands/review.md`](.cursor/commands/review.md):10
- **S2.8** · палитра `/release-review` · строка про ключ (created). [`.cursor/commands/release-review.md`](.cursor/commands/release-review.md):10
- **S2.9** · палитра `/opsx:status` · сверка (без правки) — `-noapi` не флаг и не параметр ввода. [`.cursor/commands/opsx-status.md`](.cursor/commands/opsx-status.md):17-22

