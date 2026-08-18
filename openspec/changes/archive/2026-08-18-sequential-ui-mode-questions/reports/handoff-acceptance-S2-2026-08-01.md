## Срез S2 — передача на приёмку: sequential-ui-mode-questions

**Change:** sequential-ui-mode-questions  
**Schema:** spec-driven  
**Прогресс:** 5/5 рабочих задач [x]; `S2.accept` — `[ ]` (ручная приёмка)

### 1. Что реализовано

Mode Gate касается только управляемых форм: режим задаётся на design по одной форме (с именем), разные формы могут иметь разные `form_mode` в map `forms:`. Макет в `/opsx:new` больше не спрашивается; на apply по умолчанию вручную, программный путь — только с записанным разрешением. Обновлены SSOT-правило, протоколы new/apply/verify и потребители (forms, mxl, xml-guard, handoff explore, kit-workflow).

### Карта правок (перед тестом)

1. Переписан Mode Gate под per-form и политику макета — [`.cursor/rules/forms-mxl-mode-gate.mdc`](.cursor/rules/forms-mxl-mode-gate.mdc)
2. В `/opsx:new` вопрос режима перенесён на design (цикл одна форма → пауза) — [`.cursor/skills/openspec-new-change/SKILL.md`](.cursor/skills/openspec-new-change/SKILL.md)
3. Apply/verify читают `form_mode` / `forms:` и не требуют Mode макета в new
4. В постановке explore поле «Режим формы» (без склейки с макетом) — [`.cursor/skills/openspec-explore/templates/handoff-block.md`](.cursor/skills/openspec-explore/templates/handoff-block.md)

Полная карта: `openspec/changes/sequential-ui-mode-questions/reports/code-map.md`

### 2. Что проверить СЕЙЧАС

**Primary acceptance:**
1. В учебном proposal с двумя формами заданы разные `form_mode` (map `forms:`)
2. По тексту `/opsx:new` вопросы режима на design идут по одной форме с паузой между ними
3. Макет в new не спрашивается; apply к макету по умолчанию вручную

Опционально — см. bullets в `S2.accept` в `tasks.md` (multi-form, legacy, kit n/a, empty mode, layout permission).

### 3. Следующие задачи

| Задача | Действие | Тип | Исполнитель | Зависит от | Статус |
|--------|----------|-----|-------------|------------|--------|
| `S2.accept` | принять срез «Режимы форм» по Primary | Ручной тест | пользователь | `S2.1`–`S2.5` | [ ] |
| `F1` | заполнить developer, если появятся маркеры кода | Проверка | пользователь | — | [ ] |
| `F2` | рассмотреть маркер `[form:…]` | Проверка | пользователь | — | [ ] |

### 4. Как вернуться

`/opsx:apply sequential-ui-mode-questions` — новая сессия начнётся с запроса вердикта по срезу S2.

### 5. Blockers

Нет.

### 7. Short-cut

Если уже проверено и принято — напишите обычной фразой («принято», «срез S2 принят»), отмечу без полного handoff.
