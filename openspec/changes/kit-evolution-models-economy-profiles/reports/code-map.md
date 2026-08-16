# Срез S1 — Живой мэппинг моделей (2026-08-16)

- **S1.1–S1.6, S1.11** · правила выбора моделей · таблица ролей, самосверка, двухшаговые цепочки, закрытая эскалация (modified) — Primary на живые слаги; список моделей читается из описания Task; Fable не роль по умолчанию. [`.cursor/rules/model-selection.mdc`](../../../../.cursor/rules/model-selection.mdc):16-83
- **S1.7** · правило архитектора · секция модели (modified) — слаг убран, ссылка на таблицу ролей. [`.cursor/rules/architect-gate.mdc`](../../../../.cursor/rules/architect-gate.mdc):95-99
- **S1.8** · чеклист вызова субагента · параметр model (modified) — два шага Primary, затем без model; убрано ложное утверждение про inherit. [`.cursor/rules/tool-name-guard.mdc`](../../../../.cursor/rules/tool-name-guard.mdc):22-88
- **S1.9** · поиск по rules, skills, commands, agents — мёртвых Primary-слагов в рантайме нет. Исключения: CHANGELOG.md, анти-примеры composer-2 и fast, цель политики Fable.
- **S1.10** · скилл проверки постановки и шаблоны архитектора (modified) — независимый разбор: Fable при наличии слага, иначе Opus 5; декомпозиция срезов на Opus. [`.cursor/skills/openspec-verify-change/SKILL.md`](../../../../.cursor/skills/openspec-verify-change/SKILL.md):199-242

# Срез S2 — Диета always-apply (2026-08-16)

- **S2.1** · дисциплина сессии · переносимый минимум трёх гейтов (modified) — первый вызов только чтение скилла, persistence, стратегия контекста. [`.cursor/rules/session-discipline.mdc`](../../../../.cursor/rules/session-discipline.mdc):11-51
- **S2.2 / S2.7** · диспетчер 1С · запрет прямой правки BSL и три исключения (modified) — Mechanical, шапка метода, контекст apply/review; файл `bsl-write-guard.mdc` удалён. [`.cursor/rules/1c-agent-delegation.mdc`](../../../../.cursor/rules/1c-agent-delegation.mdc):22-36
- **S2.3 / S2.6** · бюджет чата · навигатор, тишина, принципы диалога (modified) — стабы удалены. [`.cursor/rules/chat-output-budget.mdc`](../../../../.cursor/rules/chat-output-budget.mdc):10-20
- **S2.4** · XML-guard · разжалование в on-demand (modified) — compact-запрет остаётся в delegation. [`.cursor/rules/1c-xml-write-guard.mdc`](../../../../.cursor/rules/1c-xml-write-guard.mdc):1-5
- **S2.9–S2.12** · диспетчер 1С · якоря KB, авто-исправления ревью, поток writer (modified) — эталон порядка в writer-pipeline. [`.cursor/rules/1c-agent-delegation.mdc`](../../../../.cursor/rules/1c-agent-delegation.mdc):92-129 · [`.cursor/rules/1c-writer-pipeline.mdc`](../../../../.cursor/rules/1c-writer-pipeline.mdc):8-12
- **S2.13** · диспетчер гейтов · cue разжалованных правил (modified). [`.cursor/rules/gate-dispatcher.mdc`](../../../../.cursor/rules/gate-dispatcher.mdc):26-29
- **S2.14–S2.16** · индекс поставки · карта SSOT, glossary, пометка project.md (modified). [`AGENTS.md`](../../../../AGENTS.md):18-56
- **S2.17** · целостность поставки · порог ≤ 34 КБ (modified). [`.cursor/docs/delivery-integrity.md`](../../../../.cursor/docs/delivery-integrity.md):13
- **S2.18–S2.19** · отчёты замера и обязательства. [`reports/obligation-diff-S2-2026-08-16.md`](obligation-diff-S2-2026-08-16.md) · [`reports/always-apply-budget-S2-2026-08-16.md`](always-apply-budget-S2-2026-08-16.md)

# Срез S3 — Диета промпта reviewer (2026-08-16)

Документы kit, без `.bsl` в репозитории. Explain scope не требуется.

- **S3.1** · базовый прогон ревьювера (saved). [`reports/reviewer-diet-baseline-2026-08-16.md`](reviewer-diet-baseline-2026-08-16.md)
- **S3.accept-prep** · пост-диет прогон и сверка классов. [`reports/reviewer-diet-after-2026-08-16.md`](reviewer-diet-after-2026-08-16.md) · [`reports/reviewer-diet-compare-2026-08-16.md`](reviewer-diet-compare-2026-08-16.md)
- **S3.2 / S3.7** · инвентарь до/после диеты (modified). [`reports/reviewer-diet-inventory-2026-08-16.md`](reviewer-diet-inventory-2026-08-16.md)
- **S3.3–S3.5** · ядро промпта + on-demand чек-листы + строка `Checklists read:` (modified). [`.cursor/agents/onec-code-reviewer.md`](../../../../.cursor/agents/onec-code-reviewer.md):65-79 · [`.cursor/docs/standard/reviewer-checks.md`](../../../../.cursor/docs/standard/reviewer-checks.md):1-3
- **S3.6** · граничный случай отчёта (modified). [`.cursor/skills/review/SKILL.md`](../../../../.cursor/skills/review/SKILL.md):705

# Срез S4 — Профили моделей (2026-08-16)

Документы kit, без `.bsl`. Explain scope не требуется.

- **S4.1–S4.4** · роутер профилей (created). [`.cursor/rules/model-adaptation.mdc`](../../../../.cursor/rules/model-adaptation.mdc):8-60
- **S4.5–S4.10** · профили Grok / Fable / GPT / Opus, MAY и MUST NOT (created). [`.cursor/rules/model-grok4.mdc`](../../../../.cursor/rules/model-grok4.mdc):8-12
- **S4.11** · строка в индексе поставки (modified). [`AGENTS.md`](../../../../AGENTS.md):5
- **S4.12** · снимок статуса (modified). [`.cursor/skills/openspec-status/SKILL.md`](../../../../.cursor/skills/openspec-status/SKILL.md)

# Срез S5 — Усиление делегирования (2026-08-16)

Документы kit, без `.bsl`. Explain scope не требуется.

- **S5.1 / S5.6 / S5.7** · запрет встроенного explore для 1С, две неудачи, профиль (modified). [`.cursor/rules/1c-agent-delegation.mdc`](../../../../.cursor/rules/1c-agent-delegation.mdc):22-22 · [`.cursor/rules/1c-agent-delegation.mdc`](../../../../.cursor/rules/1c-agent-delegation.mdc):119
- **S5.2** · маршрутизация стратегии контекста (modified). [`.cursor/skills/context-strategy/SKILL.md`](../../../../.cursor/skills/context-strategy/SKILL.md):47-53
- **S5.3–S5.5** · intent-бриф и coverage-first (modified). [`.cursor/skills/1c-agent-patterns/SKILL.md`](../../../../.cursor/skills/1c-agent-patterns/SKILL.md):12-25 · [`.cursor/skills/1c-agent-patterns/writer.md`](../../../../.cursor/skills/1c-agent-patterns/writer.md):7-28 · [`.cursor/skills/1c-agent-patterns/reviewer.md`](../../../../.cursor/skills/1c-agent-patterns/reviewer.md):7
- **S5.8** · контрольный замер always-apply 34662 байт. [`reports/always-apply-budget-S5-2026-08-16.md`](always-apply-budget-S5-2026-08-16.md)

# Срез S6 — Гигиена свода (2026-08-16)

Документы kit, без `.bsl`. Explain scope не требуется.

- **S6.1** · шапка «Когда загружать» в топ-10 on-demand и профилях (modified). [`.cursor/rules/1c-halt-triggers.mdc`](../../../../.cursor/rules/1c-halt-triggers.mdc):10 · [`.cursor/rules/model-adaptation.mdc`](../../../../.cursor/rules/model-adaptation.mdc):8
- **S6.2** · индекс = cue (modified). [`.cursor/rules/gate-dispatcher.mdc`](../../../../.cursor/rules/gate-dispatcher.mdc):11 · [`AGENTS.md`](../../../../AGENTS.md):4
- **S6.3** · shortcut triage (modified). [`.cursor/rules/task-triage.mdc`](../../../../.cursor/rules/task-triage.mdc):9-11
- **S6.4–S6.5** · safety floor и promotion triggers (modified). [`.cursor/rules/1c-halt-triggers.mdc`](../../../../.cursor/rules/1c-halt-triggers.mdc):12-28
- **S6.6** · журнал агентов перенесён. [`.cursor/docs/agents-CHANGELOG.md`](../../../../.cursor/docs/agents-CHANGELOG.md)
- **S6.7–S6.9** · alias-стабы и `openspec-sessions.mdc` удалены; отчёт ссылок. [`reports/remnant-links-S6-2026-08-16.md`](remnant-links-S6-2026-08-16.md)
- **S6.10** · итоговый список команд и карта SSOT. [`AGENTS.md`](../../../../AGENTS.md):14-35

