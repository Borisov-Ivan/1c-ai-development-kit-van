---
description: Первичный bootstrap или re-sync таксономии базы знаний (Knowledge Base) для существующего проекта
---

# Skill: openspec-knowledge-init

**Команда:** `/opsx:knowledge-init`

## Назначение
Первичный bootstrap таксономии (`openspec/knowledge/_taxonomy.yaml`) для существующего проекта без полного `/init-project`, либо **идемпотентный re-sync** после добавления/удаления расширения в `src/*/cfe/*`.

## Алгоритм

1. **Чтение контекста:**
   - Прочитать `openspec/project.md` (если есть).
   - Прочитать `openspec/specs/architecture.md` (если есть).
   - Получить список расширений (Glob/ls `src/*/cfe/*`).

2. **Построение предлагаемой таксономии (draft):**
   - По одному `domain` на каждое расширение из `src/*/cfe/*` с корректным `source`.
   - `subdomains` — из подсистем / ключевых общих модулей (эвристика на основе архитектуры).
   - Обязательно добавить блок `cross` из шаблона `openspec/knowledge/_taxonomy.template.yaml`.

3. **Сравнение (Diff):**
   - Если `openspec/knowledge/_taxonomy.yaml` уже существует, построить diff между текущим файлом и draft.
   - Если файла нет, подготовить summary новой таксономии.

4. **Подтверждение (Confirm):**
   - Показать пользователю diff или summary.
   - Запросить подтверждение на запись.

5. **Запись (Write):**
   - После подтверждения пользователя сохранить результат в `openspec/knowledge/_taxonomy.yaml`.
   - Файл `_index.yaml` и сами файлы фактов (KB-*.md) этот скилл **не трогает**.
