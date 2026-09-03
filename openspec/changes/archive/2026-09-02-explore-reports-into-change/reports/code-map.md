# Срез S1 — Фактура в каталоге ЗНИ (2026-09-02)

- **S1.1** · правило сохранения отчётов · секция «Переезд в каталог ЗНИ» (created) — алгоритм отбора, allowlist, переезд не копия, тихий пропуск, перепись `report:`. [`.cursor/rules/preserve-subagent-reports.mdc`](.cursor/rules/preserve-subagent-reports.mdc):64-100
- **S1.2** · скилл создания ЗНИ · шаг 2.1 «Перенос отчётов исследования» (created) — переезд сразу после появления каталога, до записи постановки; финал без списка путей. [`.cursor/skills/openspec-new-change/SKILL.md`](.cursor/skills/openspec-new-change/SKILL.md):161-170
- **S1.3** · контракт постановки · примечание к полю Architect / verify (modified) — после переезда `report:` указывает на `reports/<файл>` внутри ЗНИ. [`.cursor/skills/openspec-new-change/templates/handoff-contract.md`](.cursor/skills/openspec-new-change/templates/handoff-contract.md):20-20
- **S1.4** · скилл дополнения ЗНИ · `--from-report` из `temp` (modified) — сначала переезд, дальше ссылки на каталог ЗНИ. [`.cursor/skills/openspec-extend-change/SKILL.md`](.cursor/skills/openspec-extend-change/SKILL.md):43-43
- **S1.5** · скилл исследования · Continuity (modified) — glob 7 дней по allowlist, включая `openspec/changes/*/reports/`, без служебных отчётов проверки. [`.cursor/skills/openspec-explore/SKILL.md`](.cursor/skills/openspec-explore/SKILL.md):35-42
- **S1.6** · стиль чата · таблица «Файлы» и короткое подтверждение создания ЗНИ (modified) — после new отчёты в каталоге задачи; фраза без перечня путей. [`.cursor/docs/opsx-output-style.md`](.cursor/docs/opsx-output-style.md):345-345
- **S1.7** · шаблон журнала разбора · правило href при переезде (modified) — `../../src/` → `../../../../src/`, label citation не менять. [`.cursor/skills/openspec-explain/templates/explain-report.md`](.cursor/skills/openspec-explain/templates/explain-report.md):38-38
- **S1.8** · тест-кейс explore→new · точки 7–8 (modified) — файл из превью в `reports/` ЗНИ, в `temp` нет; финал new без списка путей. [`.cursor/skills/openspec-explore/test-cases/question-to-new-handoff.md`](.cursor/skills/openspec-explore/test-cases/question-to-new-handoff.md):23-24
- **S1.9** · сверка по тексту (modified) — контракт переезда совпадает с дельтой без живого прогона команд.

# Срез S2 — Вводные в отчёте (2026-09-02)

- **S2.1** · правило сохранения · секция «Шапка вводных» + prepend-if-missing (created) — пятипольная шапка, запрет цитаты чата, страховка при сохранении. [`.cursor/rules/preserve-subagent-reports.mdc`](.cursor/rules/preserve-subagent-reports.mdc):104-128
- **S2.2** · агент обследования · шапка сразу после H1 (modified) — ссылка на SSOT, «Для заказчика» в конце отдельно. [`.cursor/agents/onec-code-explorer.md`](.cursor/agents/onec-code-explorer.md):415-419
- **S2.3** · агент трассы · шапка после H1 (modified) — «Что наблюдаешь» остаётся симптомом. [`.cursor/agents/onec-trace-analyst.md`](.cursor/agents/onec-trace-analyst.md):320-328
- **S2.4** · агент архитектуры · шапка после YAML и H1 только для отчёта исследования (modified). [`.cursor/agents/onec-code-architect.md`](.cursor/agents/onec-code-architect.md):585-589
- **S2.5** · промпт исследования · слоты вводных (modified) — формулировка из постановки, не из находок. [`.cursor/skills/openspec-explore/SKILL.md`](.cursor/skills/openspec-explore/SKILL.md):176-176
- **S2.6** · профиль дефекта · граница шапки и Symptom Lock (modified). [`.cursor/skills/openspec-explore/profiles/bug.md`](.cursor/skills/openspec-explore/profiles/bug.md):59-59
- **S2.7** · журнал разбора · «Мета» без второй шапки (modified). [`.cursor/skills/openspec-explain/templates/explain-report.md`](.cursor/skills/openspec-explain/templates/explain-report.md):125-125
- **S2.8** · чат-постановка · список отчётов в блок не входит (modified). [`.cursor/skills/openspec-explore/templates/handoff-block.md`](.cursor/skills/openspec-explore/templates/handoff-block.md):38-38
- **S2.9** · тест-кейс · точка 9 про шапку в exploration-файле (modified). [`.cursor/skills/openspec-explore/test-cases/question-to-new-handoff.md`](.cursor/skills/openspec-explore/test-cases/question-to-new-handoff.md):25-25
- **S2.10** · сверка по тексту (modified) — шапка совпадает с дельтой без живого прогона команд.

