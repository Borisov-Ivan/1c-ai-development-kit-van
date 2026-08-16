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

