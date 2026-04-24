---
name: /opsx:ff
id: opsx-ff
category: Workflow
description: Быстрое создание change со всеми артефактами для реализации
---

Fast-forward through artifact creation - generate everything needed to start implementation.

**Первое действие:** прочитать `.cursor/skills/openspec-ff-change/SKILL.md` и далее идти по его шагам. До прочтения скилла — никаких чтений артефактов, трасс, модулей.

**Второе действие:** Metadata Gate. Запросите developer, zni_id и zni_name. Без ответа пользователя команда `openspec new change` не запускается.

Input: argument after the command is the change name (kebab-case) or a description of what the user wants to build.
