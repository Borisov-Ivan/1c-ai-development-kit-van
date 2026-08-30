---
name: /session-restore
id: session-restore
category: Workflow
description: Прочитать session-notes и предложить команду (без авто-apply)
---

Восстановить контекст из `temp/session-notes.md` и предложить следующую команду.

**Первое действие:** прочитать `.cursor/skills/session-restore/SKILL.md` и следовать шагам. До прочтения — никаких других чтений.

**Запрещено:** авто-запуск `/opsx:apply`, writer, правок кода. Только навигация.
