# Срез S1 — Маршрут починки с прежним результатом (2026-10-16)

- **S1.1** · правило размещения · (modified) — починка с прежним результатом встаёт в открытую приёмку, число срезов само по себе новый срез не открывает. [`.cursor/rules/vertical-slices.mdc`](.cursor/rules/vertical-slices.mdc):355-420
- **S1.2** · ветка недостижимой приёмки · (modified) — при том же результате и том же моменте приёмки карточка «в какой срез» не показывается. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):519-523
- **S1.3** · ограничение ремонта и раскладка дополнения · (modified) — при том же результате вопрос перед раскладкой не задаётся, уже открытая приёмка из текста ошибки снимается. [`.cursor/skills/openspec-extend-change/SKILL.md`](.cursor/skills/openspec-extend-change/SKILL.md):214-215
- **S1.4** · таблица глубины · (modified) — после первой полной проверки прежняя формула идёт на реализацию, смена формулы остаётся полной проверкой. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):84-88
- **S1.5** · исход дополнения · (modified) — «проверка не требуется» называет ту же таблицу: замена значения и строка починки. [`.cursor/skills/openspec-extend-change/SKILL.md`](.cursor/skills/openspec-extend-change/SKILL.md):457-470
