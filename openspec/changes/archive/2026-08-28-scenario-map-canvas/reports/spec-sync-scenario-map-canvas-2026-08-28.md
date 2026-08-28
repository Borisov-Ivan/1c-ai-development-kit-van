# Spec sync — scenario-map-canvas (2026-08-28)

**Change:** `scenario-map-canvas`  
**Mode:** archive (ADDED → новая главная capability)

## Capability

- `openspec/specs/scenario-map-canvas/spec.md` — **создана**
- Источник: `openspec/changes/scenario-map-canvas/specs/scenario-map-canvas/spec.md`
- Секция `## ADDED Requirements` перенесена как `## Requirements`; добавлен `## Purpose` из лида дельты

## Requirements (ADDED → main)

1. Silence unless asked or hinted
2. Direct request draws the scenario map
3. Technical fallback is not a map
4. Node contract forbids empty or code-primary nodes
5. Causal map has layers or branches
6. Offer by topology not by topic
7. No dedicated map command
8. Two map names stay distinct
9. Hint only on an existing decision line
10. Map outside walkthrough uses named source

## MODIFIED / REMOVED / RENAMED

Нет: главной спеки до синхронизации не было.

## Notes

- Критерий успеха публикации: штатная кнопка среды после чистой проверки панели у родителя; ссылка в чате не критерий.
- Картограф не пишет файл панели.
- У узла обязательно имя; у ребра — `evidence_ref`; порядок прохода — следование, не причинность.
