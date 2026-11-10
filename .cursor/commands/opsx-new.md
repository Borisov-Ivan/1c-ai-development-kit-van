---
name: /opsx:new
id: opsx-new
category: Workflow
description: Создание или дозавершение change (ЗНИ) со всеми артефактами для реализации
---

Создание change (ЗНИ) — **новый** change или **resume** существующего (дозавершение артефактов).

Ключ `-noapi` / `-api` пишется в любом сообщении чата и не является флагом этой команды.

**Первое действие:** прочитать `.cursor/skills/openspec-new-change/SKILL.md` и далее идти по его шагам. До прочтения скилла — никаких чтений артефактов, трасс, модулей.

**Бриф (Sync Card):** B0 при `## Постановка ЗНИ` в чате/handoff (информирующая строка, без согласования имени); B1 при свободном тексте — карточка **Изменение** + Подтвердить? — см. `.cursor/docs/templates/brief-card.md`.

Вопрос про маркер задаёт скилл создания своим шагом.

Input: argument after the command is the change name (kebab-case) or a description of what they want to build.
Optional flag: `--skip-architect "<причина>"` to bypass mandatory Architect Gate.
