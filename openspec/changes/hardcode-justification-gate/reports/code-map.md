# Срез S1 — Реестр и запах (2026-08-08)

- **S1.1** · `.cursor/rules/bsl-antipatterns.mdc` · Writer bulletin + каталог (modified) — индекс AP-055 Hardcoded Identity Filter с детекторами и remediation.
- **S1.1b** · `.cursor/docs/antipatterns/bsl-antipatterns.md` · карточка AP-055 (created) — полная карточка: детекторы, out-of-class, remediation, примеры.
- **S1.2** · bulletin + карточка AP-055 (modified) — явная граница: коды отказа / ключи протокола / закрытые enum не identity-filter.
- **S1.3** · `.cursor/rules/existing-mechanism-priority.mdc` · § Scope-as-literals (created) — запах рядом с Substituted Authority + отсылка к Hardcode Justification.
- **S1.4** · `.cursor/rules/existing-mechanism-priority.mdc` · шаблон Hardcode Justification (created) — SSOT для копирования в design прикладных ЗНИ.

# Срез S2 — Architect HALT (2026-08-08)

- **S2.1** · `.cursor/agents/onec-code-architect.md` · Identity Filter Gate (created) — HALT до Chosen allow-list; три вопроса Hardcode Justification.
- **S2.2** · `.cursor/rules/architect-gate.mdc` · семантический триггер Identity Filter Gate (created) — оркестратор подгружает HALT при allow-list в хуке.
- **S2.3** · architect + architect-gate (modified) — запрет обхода «временный список на первый релиз».

# Срез S3 — Writer + Reviewer (2026-08-08)

- **S3.1** · `.cursor/agents/onec-code-writer.md` · G21 (created) — HALT на identity-literals без Hardcode Justification.
- **S3.2** · writer agent + `1c-agent-patterns/writer.md` (modified) — G21 в Gate Results / чеклисте.
- **S3.3–S3.5** · `onec-code-reviewer.md` + `reviewer-checks.md` · Phase 2.6 Identity / Hardcode Audit (created) — completeness N=N; contradiction → MUST_FIX AP-055.
- **S3.6** · `.cursor/skills/review/SKILL.md` (modified) — зеркало Phase 2.6 в light-review / Risk Surfacing.
