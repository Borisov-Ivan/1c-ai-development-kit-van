---
name: /opsx:new
id: opsx-new
category: Workflow
description: Создание или дозавершение change (ЗНИ) со всеми артефактами для реализации
---

Создание change (ЗНИ) — **новый** change или **resume** существующего (дозавершение артефактов).

**Первое действие:** прочитать `.cursor/skills/openspec-new-change/SKILL.md` и далее идти по его шагам. До прочтения скилла — никаких чтений артефактов, трасс, модулей.

**Бриф (Sync Card):** B0 при `## Постановка ЗНИ` в чате/handoff (информирующая строка, без согласования имени); B1 при свободном тексте (≤6 строк: связный абзац «что понял / что изменится» + Подтвердить?) — см. `opsx-output-style.md` §5.1.

**Второе действие (только новый change):** Metadata Gate. Read `openspec/project.md` (`defaultDeveloper`, канон `domain_label`). Агент сам собирает готовый маркер из «Темы маркера» / Why и предлагает принять через `AskQuestion`; свободный вопрос — только если собрать не из чего. Без metadata `openspec new change` не запускается. Resume — metadata из proposal.md, gate пропускается.

Input: argument after the command is the change name (kebab-case) or a description of what they want to build.
Optional flag: `--skip-architect "<причина>"` to bypass mandatory Architect Gate.
