# Срез S1 — Живой мэппинг моделей (2026-08-16)

- **S1.1–S1.6, S1.11** · правила выбора моделей · таблица ролей, самосверка, двухшаговые цепочки, закрытая эскалация (modified) — Primary на живые слаги; список моделей читается из описания Task; Fable не роль по умолчанию. [`.cursor/rules/model-selection.mdc`](../../../../.cursor/rules/model-selection.mdc):16-83
- **S1.7** · правило архитектора · секция модели (modified) — слаг убран, ссылка на таблицу ролей. [`.cursor/rules/architect-gate.mdc`](../../../../.cursor/rules/architect-gate.mdc):95-99
- **S1.8** · чеклист вызова субагента · параметр model (modified) — два шага Primary, затем без model; убрано ложное утверждение про inherit. [`.cursor/rules/tool-name-guard.mdc`](../../../../.cursor/rules/tool-name-guard.mdc):22-88
- **S1.9** · поиск по rules, skills, commands, agents — мёртвых Primary-слагов в рантайме нет. Исключения: CHANGELOG.md, анти-примеры composer-2 и fast, цель политики Fable.
- **S1.10** · скилл проверки постановки и шаблоны архитектора (modified) — независимый разбор: Fable при наличии слага, иначе Opus 5; декомпозиция срезов на Opus. [`.cursor/skills/openspec-verify-change/SKILL.md`](../../../../.cursor/skills/openspec-verify-change/SKILL.md):199-242
