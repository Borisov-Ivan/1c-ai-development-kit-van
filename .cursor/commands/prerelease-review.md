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
- `/prerelease-review <расширение> <change-name>` — ревью в рамках ЗНИ (**change-scoped**): Tier 1 и механические проверки только по файлам из выполненных задач `[x]` в `tasks.md` этого change (см. скилл); Tier 2 (explorer) — по всему расширению.

`<change-name>` — каталог change в `openspec/changes/<name>/` или `openspec/changes/archive/<name>/` (полное имя папки, например `2026-03-25-edo-ea-batch-signing-rs-elektronnye-podpisi`).

**Первое действие:** прочитать `.cursor/skills/prerelease-review/SKILL.md` и далее идти по его шагам. До прочтения скилла — никаких чтений артефактов, трасс, модулей.
