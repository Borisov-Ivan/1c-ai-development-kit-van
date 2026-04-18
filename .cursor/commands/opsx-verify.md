---
name: /opsx:verify
id: opsx-verify
category: Workflow
description: Universal quality gate — slice-pre / slice-post / slice-scoped / migrate-to-slices / legacy
---

Universal quality gate for OpenSpec changes. Режим определяется автоматически по структуре `tasks.md`:

- **slice-pre** — ЗНИ в slice mode, ни один срез ещё не принят (артефакты, качество задач, когерентность срезов через Quality Controller, Architect readiness, ТЗ при пороге, gates).
- **slice-post** — часть срезов принята; для принятых выполняются post-checks (completeness, correctness, coherence), для непринятых — pre-checks.
- **slice-post (final)** — все срезы приняты, готов к archive.
- **slice-transition** — после `S<N>.T<M>` = `[x]` оценка актуальности upcoming срезов (вызывается apply на slice-gate или вручную).
- **slice-scoped** — verify одного среза (`--slice S<N>`).
- **migrate-to-slices** — реструктуризация плоского/фазового tasks.md в вертикальные срезы (architect через шаблон «Architect — slice restructuring»).
- **legacy** — tasks.md без `# Срез`: pre-apply / mixed / post-apply (старая модель совместимости).

Phase A: silent auto-fix mechanical issues. Phase B: judgment decision cards.

**FIRST AND ONLY action**: Read `.cursor/skills/openspec-verify-change/SKILL.md`.
Do NOT read any other files, traces, or modules in the same tool call.
After reading the skill, follow its instructions step by step before taking any other action.

**Input:**
- `<change-name>` (optional, e.g. `/opsx:verify add-auth`).

**Флаги:**
- `--slice S<N>` — verify только одного среза (артефакты + связанные Requirements/Scenarios + файлы реализованных задач S<N>). Tier ≥ Standard.
- `--since-slice S<N>` — verify-pre для среза S<N> и всех последующих (полезно после правок design.md `## Slices`).
- `--migrate-to-slices` — режим миграции legacy/фазового tasks.md в срезы. Architect перестраивает, пользователь подтверждает diff, скилл применяет StrReplace.
- `--full` / `--standard` — повысить tier (по умолчанию определяется автоматически: Lite ≤5 задач/1 срез, Standard 6–15 задач/2+ срезов, Full ≥16 задач/3+ срезов или slice-transition).
