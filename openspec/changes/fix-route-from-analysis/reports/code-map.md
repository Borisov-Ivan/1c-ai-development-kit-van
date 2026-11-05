# Срез S1 — Маршрут починки с прежним результатом (2026-10-16)

- **S1.1** · правило размещения · (modified) — починка с прежним результатом встаёт в открытую приёмку, число срезов само по себе новый срез не открывает. [`.cursor/rules/vertical-slices.mdc`](.cursor/rules/vertical-slices.mdc):355-420
- **S1.2** · ветка недостижимой приёмки · (modified) — при том же результате и том же моменте приёмки карточка «в какой срез» не показывается. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):519-523
- **S1.3** · ограничение ремонта и раскладка дополнения · (modified) — при том же результате вопрос перед раскладкой не задаётся, уже открытая приёмка из текста ошибки снимается. [`.cursor/skills/openspec-extend-change/SKILL.md`](.cursor/skills/openspec-extend-change/SKILL.md):214-215
- **S1.4** · таблица глубины · (modified) — после первой полной проверки прежняя формула идёт на реализацию, смена формулы остаётся полной проверкой. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):84-88
- **S1.5** · исход дополнения · (modified) — «проверка не требуется» называет ту же таблицу: замена значения и строка починки. [`.cursor/skills/openspec-extend-change/SKILL.md`](.cursor/skills/openspec-extend-change/SKILL.md):457-470

# Срез S1 — Маршрут починки с прежним результатом (2026-11-05)

- **S1.6** · карточка проверки · (modified) — ветвь, которая не выполняет уже записанную приёмку, в пару не ставится; одна живая ветвь продолжается в том же запуске. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):526-526
- **S1.7** · шаг после ответа · (modified) — после настоящего ответа шаг читается из таблицы глубины, а не зовёт всю проверку заново. [`.cursor/skills/openspec-verify-change/templates/chat-summary.md`](.cursor/skills/openspec-verify-change/templates/chat-summary.md):99-99
- **S1.8** · карточка дополнения · (modified) — когда заявка и правило уже названы, пара «дописать или не делать» не показывается, подтверждение без номера принимает «да». [`.cursor/skills/openspec-extend-change/SKILL.md`](.cursor/skills/openspec-extend-change/SKILL.md):86-86
- **S1.9** · вход проверки · (modified) — фраза, уже сказанная в той же команде, передаётся в дополнение и не откладывается в заметки. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):74-74
- **S1.10** · слова вопроса · (modified) — перед показом вопрос пишется словами уже записанного результата, путь к заметке остаётся в отчёте. [`.cursor/docs/templates/decision-block.md`](.cursor/docs/templates/decision-block.md):48-48
