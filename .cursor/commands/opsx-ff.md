---
name: /opsx:ff
id: opsx-ff
category: Workflow
description: Создание или дозавершение change со всеми артефактами для реализации
---

Fast-forward through artifact creation — **новый** change или **resume** существующего (дозавершение артефактов).

**Первое действие:** прочитать `.cursor/skills/openspec-ff-change/SKILL.md` и далее идти по его шагам. До прочтения скилла — никаких чтений артефактов, трасс, модулей.

**Бриф (Sync Card):** B0 при `## Для /opsx:ff` в чате/handoff (≤1 строка, текстовое «да»); B1 при свободном тексте (≤6 строк: От вас / Цель / На выходе / Подтвердить?) — см. `opsx-output-style.md` §5.1.

**Второе действие (только новый change):** Metadata Gate. Read `openspec/project.md` (ФИО по умолчанию). Один вопрос в чат: опциональный `comment_suffix` (если ФИО в project.md) или ФИО + комментарий. Без ответа `openspec new change` не запускается. Resume существующего change — metadata из proposal.md, gate пропускается.

Input: argument after the command is the change name (kebab-case) or a description of what they want to build.
Optional flag: `--skip-architect "<причина>"` to bypass mandatory Architect Gate.
