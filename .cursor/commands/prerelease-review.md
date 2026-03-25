---
name: /prerelease-review
id: prerelease-review
category: Quality
description: Pre-release code review for 1C extensions with severity escalation and openspec change creation
---

Провести предрелизное ревью расширения 1С.

**Input**:

- `/prerelease-review` — без аргументов: определить расширение из контекста или предложить выбор (режим **full-extension**, как раньше).
- `/prerelease-review <расширение>` — полное предрелизное ревью всех `.bsl` в каталоге расширения (**full-extension**).
- `/prerelease-review <расширение> <change-name>` — ревью в рамках ЗНИ (**change-scoped**): Tier 1 и механические проверки только по файлам из выполненных задач `[x]` в `tasks.md` этого change (см. скилл); Tier 2 (explorer) — по всему расширению.

`<change-name>` — каталог change в `openspec/changes/<name>/` или `openspec/changes/archive/<name>/` (полное имя папки, например `2026-03-25-edo-ea-batch-signing-rs-elektronnye-podpisi`).

**FIRST AND ONLY action**: Read `.cursor/skills/prerelease-review/SKILL.md`.
Do NOT read any other files, traces, or modules in the same tool call.
After reading the skill, follow its instructions step by step before taking any other action.
