# Срез S1 — Explain scope после review/apply (2026-08-09)

Kit meta-change (без продуктового BSL). Карта правок skills/commands/docs.

- **S1.1** · review skill · сохранение отчёта (modified) — обязательная секция `## Explain scope` в main report + self-check. [`.cursor/skills/review/SKILL.md`](.cursor/skills/review/SKILL.md)
- **S1.2** · apply skill · code-map / handoff (modified) — SSOT охвата в `code-map.md`, копия/ссылка в handoff-acceptance, запрет отдельного explain-handoff. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md)
- **S1.3** · review skill · финал / «Куда дальше» (modified) — propose `/opsx:explain` ниже MUST_FIX/extend; skip trivial light-review. [`.cursor/skills/review/SKILL.md`](.cursor/skills/review/SKILL.md)
- **S1.4** · output style + apply · T-HANDOFF (modified) — опциональный explain после BSL acceptance/final. [`.cursor/docs/opsx-output-style.md`](.cursor/docs/opsx-output-style.md), [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md)
- **S1.5** · commands + guide (modified) — когда звать explain после ревью. [`.cursor/commands/review.md`](.cursor/commands/review.md), [`.cursor/commands/release-review.md`](.cursor/commands/release-review.md), [`.cursor/docs/review-guide.md`](.cursor/docs/review-guide.md)
- **S1.6** · explain skill · Entry Protocol 1a (modified) — prefill B-explain из `## Explain scope`, Read ≤3. [`.cursor/skills/openspec-explain/SKILL.md`](.cursor/skills/openspec-explain/SKILL.md)
- **S1.7** · entry-brief + fixture (modified) — эталон C, HALT path только в Контекст. [`.cursor/skills/openspec-explain/templates/entry-brief.md`](.cursor/skills/openspec-explain/templates/entry-brief.md), [`.cursor/skills/openspec-explain/fixtures/voice-good-brief.md`](.cursor/skills/openspec-explain/fixtures/voice-good-brief.md)
- **S1.8** · brief-card + команда explain (modified) — ссылка на эталон C, примеры `@review-*.md` / `@code-map.md`. [`.cursor/docs/templates/brief-card.md`](.cursor/docs/templates/brief-card.md), [`.cursor/commands/opsx-explain.md`](.cursor/commands/opsx-explain.md)
- **S1.9** · верификация kit (check) — explore-propose explain на месте; disposition as-designed не затронут.

## Explain scope (handoff)

- source: apply
- change: explain-after-review-apply-scope
- focus: slice-S1
- files:
  - path: .cursor/skills/review/SKILL.md
  - path: .cursor/skills/openspec-apply-change/SKILL.md
  - path: .cursor/skills/openspec-explain/SKILL.md
  - path: .cursor/skills/openspec-explain/templates/entry-brief.md
  - path: .cursor/docs/opsx-output-style.md
  - path: .cursor/docs/review-guide.md
  - path: .cursor/docs/templates/brief-card.md
  - path: .cursor/commands/review.md
  - path: .cursor/commands/release-review.md
  - path: .cursor/commands/opsx-explain.md
- report: openspec/changes/explain-after-review-apply-scope/reports/code-map.md
