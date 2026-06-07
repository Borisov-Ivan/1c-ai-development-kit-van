---
name: /opsx:ff
id: opsx-ff
category: Workflow
description: Создание или дозавершение change со всеми артефактами для реализации
---

Fast-forward through artifact creation — **новый** change или **resume** существующего (дозавершение артефактов).

**Первое действие:** прочитать `.cursor/skills/openspec-ff-change/SKILL.md` и далее идти по его шагам. До прочтения скилла — никаких чтений артефактов, трасс, модулей.

**Второе действие (только новый change):** Metadata Gate. Read `openspec/project.md` (ФИО по умолчанию). Один вопрос в чат: опциональный `comment_suffix` (если ФИО в project.md) или ФИО + комментарий. Без ответа `openspec new change` не запускается. Resume существующего change — metadata из proposal.md, gate пропускается.

Input: argument after the command is the change name (kebab-case) or a description of what they want to build.
Optional flag: `--skip-architect "<причина>"` to bypass mandatory Architect Gate.
