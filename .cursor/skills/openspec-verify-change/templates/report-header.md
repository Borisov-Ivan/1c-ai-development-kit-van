# YAML frontmatter отчёта verify

Копируется в начало `reports/verification-YYYY-MM-DD.md` из `templates/report-header.md` (плейсхолдеры заменить):

```yaml
---
verify_mode: <slice-pre | slice-post | slice-post-final | slice-scoped | slice-transition | legacy-pre | legacy-mixed | legacy-post>
change: <имя-change>
date: YYYY-MM-DD
verdict: "<технический вердикт для YAML — не повторять в абзаце «Суть»>"
tier: <Lite | Standard | Full>
snapshot:
  accepted_tasks:
    - S1.1
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "YYYY-MM-DDTHH:mm:ss"
    design.md: "YYYY-MM-DDTHH:mm:ss"
    tasks.md: "YYYY-MM-DDTHH:mm:ss"
    specs/<capability-folder>/spec.md: "YYYY-MM-DDTHH:mm:ss"
---
```

Человеческие формулировки «Этап / объём проверки / готовность» **не** дублируются отдельной шапкой в `## Executive Summary`: только абзацы **«Суть»** и опционально **«Что в работе»** по `templates/executive-summary.md`. Режим и вердикт для автоматизации — в YAML (`verify_mode`, `verdict`, `tier`, **`snapshot`**).
