---
name: /init-project
id: init-project
category: Workflow
description: "Диагностика проекта, бутстрап OpenSpec, интервью → openspec/project.md и architecture"
---

Проверь готовность проекта (выгрузка, OpenSpec, агенты), подскажи недостающее, затем собери информацию через интервью → `openspec/project.md` → `openspec/specs/architecture.md`. В **kit** файлов `openspec/project.md`, `openspec/specs/architecture.md` и `openspec/config.yaml` нет — они появляются после `/init-project` в целевом проекте 1С.

**Первое действие:** прочитать [`.cursor/docs/init-project-protocol.md`](../docs/init-project-protocol.md) и выполнить протокол целиком (Phase 0…). До чтения протокола — не создавать каталоги и не писать `project.md`.

**Input:** `/init-project` (без обязательных аргументов).

**SSOT протокола:** `.cursor/docs/init-project-protocol.md` (не дублировать фазы в этом файле команды).
