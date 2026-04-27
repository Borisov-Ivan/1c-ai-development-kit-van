---
name: /prerelease-review
id: prerelease-review
category: Quality
description: Предрелизное ревью расширения 1С с эскалацией серьёзности и привязкой к change
---

Провести предрелизное ревью расширения 1С.

**Input**:

- `/prerelease-review` — без аргументов: определить расширение из контекста или предложить выбор (режим **full-extension**, как раньше).
- `/prerelease-review <расширение>` — полное предрелизное ревью всех `.bsl` в каталоге расширения (**full-extension**).
- `/prerelease-review <расширение> <change-name>` — ревью в рамках ЗНИ (**change-scoped**): scope строится из `reports/architecture-*.md` → `tasks.md` → `design.md` (git fallback; `debug.md`/`slice-acceptance` только предупреждения). Tier 1 и механические проверки идут только по `target_files` текущего расширения; BSL из других cfe/cf попадают в `reference_files` как read-only context без findings. Перед запуском агентов показывается Scope Preview; при неоднозначных путях задаётся уточняющий вопрос. Tier 2 (explorer) — по всему расширению.

`<change-name>` — каталог change в `openspec/changes/<name>/` или `openspec/changes/archive/<name>/` (полное имя папки, например `2026-03-25-edo-ea-batch-signing-rs-elektronnye-podpisi`).

**Первое действие:** прочитать `.cursor/skills/prerelease-review/SKILL.md` и далее идти по его шагам. До прочтения скилла — никаких чтений артефактов, трасс, модулей.
