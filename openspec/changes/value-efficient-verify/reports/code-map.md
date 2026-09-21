# Карта правок — value-efficient-verify

# Срез S1 — Внешний контракт и ранняя остановка повторной темы (2026-09-21)

- **S1.1** · навык проверки · Load artifacts (modified) — проверка читает реестр внешнего контракта по schema, authority, axis и идентификатору темы. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):112-125
- **S1.2** · навык проверки · External validity (created) — незакрытая тема высокого авторитета останавливает продолжение до дорогих проверок. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):175-199
- **S1.3** · правило specs · Scenario Observability (modified) — принятые оси референса требуют наблюдаемый контракт или подтверждённое отличие. [`.cursor/rules/openspec-specs-gate.mdc`](.cursor/rules/openspec-specs-gate.mdc):73-73
- **S1.4** · правило срезов · Loop Detection (modified) — повтор темы отделён от кругов приёмки среза. [`.cursor/rules/vertical-slices.mdc`](.cursor/rules/vertical-slices.mdc):319-322
- **S1.5** · навык реализации · Slice Gate Decisions (modified) — возврат и подтверждение обновляют существующую запись контракта. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):449-449
- **S1.6** · навык ревью · Architectural Context (modified) — в ревью уходят только затронутые записи контракта. [`.cursor/skills/review/SKILL.md`](.cursor/skills/review/SKILL.md):370-370
- **S1.7** · роль ревью кода · Contract Map (modified) — код сверяется с переданными осями; цитата постановки не закрывает качество. [`.cursor/agents/onec-code-reviewer.md`](.cursor/agents/onec-code-reviewer.md):128-128
- **S1.8** · навык создания ЗНИ · шаг 5 (modified) — реестр создаётся только при явном условии заказчика, до согласования постановки. [`.cursor/skills/openspec-new-change/SKILL.md`](.cursor/skills/openspec-new-change/SKILL.md):288-294
- **S1.9** · навык расширения ЗНИ · user-extend (modified) — новое явное требование регистрируется как первичное событие. [`.cursor/skills/openspec-extend-change/SKILL.md`](.cursor/skills/openspec-extend-change/SKILL.md):332-332
- **S1.10** · навык проверки · Repair Loop и Update snapshot (modified) — отличие от условия высокого авторитета закрывает только ответ заказчика. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):424-450
- **S1.11** · навык проверки · Universal policy self-check (created) — предметные данные и ложная обязательность реестра отклоняются. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):452-463

# Срез S2 — Дельта-проверка и профильная эскалация (2026-09-21)

- **S2.1** · шаблон снимка · snapshot (modified) — в отчёте хранятся хэши входов, дайджест внешнего контракта, кэш и карта инвалидации. [`.cursor/skills/openspec-verify-change/templates/report-header.md`](.cursor/skills/openspec-verify-change/templates/report-header.md):41-52
- **S2.2** · навык проверки · Novelty Check (modified) — повтор считает детерминированную дельту по хэшам, а не по одной метке времени. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):140-148
- **S2.3** · навык проверки · каскад слоёв (modified) — дешёвый блокер завершает прогон до дорогих ролей. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):23-25
- **S2.4** · шаблон итога · Technical audit (modified) — в файле отчёта видны пересчитанные, переиспользованные и эскалированные контроли. [`.cursor/skills/openspec-verify-change/templates/executive-summary.md`](.cursor/skills/openspec-verify-change/templates/executive-summary.md):129-137
- **S2.5** · правило архитектора · Verify triggers (modified) — профильный вызов только при смене хэша оси или профильном триггере. [`.cursor/rules/architect-gate.mdc`](.cursor/rules/architect-gate.mdc):116-117
- **S2.6** · роль контроля срезов · Input and Process (modified) — оценка только изменившихся срезов и связанных сценариев. [`.cursor/agents/openspec-quality-controller.md`](.cursor/agents/openspec-quality-controller.md):39-49
- **S2.7** · промпт контроля срезов · Delta (modified) — в вызов уходят дельта, cache evidence и затронутый scope. [`.cursor/skills/1c-agent-patterns/quality-controller.md`](.cursor/skills/1c-agent-patterns/quality-controller.md):35-45
- **S2.8** · роль архитектора · verify modes (modified) — challenge и readiness читают только профильную дельту. [`.cursor/agents/onec-code-architect.md`](.cursor/agents/onec-code-architect.md):152-156
- **S2.9** · промпты архитектора · verify prompts (modified) — шаблоны принимают причину триггера и узкий контекст. [`.cursor/skills/1c-agent-patterns/architect.md`](.cursor/skills/1c-agent-patterns/architect.md):209-216
- **S2.10** · навык реализации · internal verify (modified) — на границе среза переиспользуется последний снимок. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):374-374
