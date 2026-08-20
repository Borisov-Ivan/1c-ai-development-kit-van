## Срез S3 — передача на приёмку: kit-session-noapi-visibility-and-ru-progress

**Change:** kit-session-noapi-visibility-and-ru-progress
**Прогресс:** 7/7 рабочих задач среза S3 [x]; `S3.accept` — `[ ]`.

### 1. Что реализовано

На `/opsx:new` вопрос маркера пропускается только если доказано, что ЗНИ — только правила и документы kit. Деловой текст без `.bsl` — спросить. Если позже появится BSL, `/opsx:apply` не пишет `n/a` в маркер кода.

### Карта правок (перед тестом)

- **S3.1** · `/opsx:new` · пропуск только kit-only. [`.cursor/skills/openspec-new-change/SKILL.md`](../../../../.cursor/skills/openspec-new-change/SKILL.md):67-71
- **S3.2** · карточка брифа · то же условие. [`.cursor/docs/templates/brief-card.md`](../../../../.cursor/docs/templates/brief-card.md):45
- **S3.6** · `/opsx:apply` · `n/a` не в маркер. [`.cursor/skills/openspec-apply-change/SKILL.md`](../../../../.cursor/skills/openspec-apply-change/SKILL.md):126-127

Полная карта: `reports/code-map.md`

### 2. Что проверить СЕЙЧАС

**Primary:** в протоколе `/opsx:new` вопрос маркера пропускается только при доказанном kit-only; ЗНИ без `.bsl` из правил kit не спрашивает маркер.

1. Откройте шаг Metadata Gate в скилле `/opsx:new`.
2. Сверьте карточку брифа, секцию Metadata Gate.

### 4. Как вернуться

`/opsx:apply kit-session-noapi-visibility-and-ru-progress`

### 7. Short-cut

«принято» / «срез S3 принят».
