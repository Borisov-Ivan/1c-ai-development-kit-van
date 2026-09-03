# Срез S1 — Пропуск холостого вопроса поставки (2026-09-01)

- **S1.1** · правило поставки формы · классификатор «только модуль / разметка / неясно» (created) — при доказанном «только модуль» записывать поставку программно без выбора из трёх, форму из списка не выкидывать. [`.cursor/rules/forms-mxl-mode-gate.mdc`](.cursor/rules/forms-mxl-mode-gate.mdc):37-55
- **S1.2** · правило поставки формы · поясняющая строка (created) — «записываю поставку программно» не считается вопросом выбора; отсутствие строки не дефект. [`.cursor/rules/forms-mxl-mode-gate.mdc`](.cursor/rules/forms-mxl-mode-gate.mdc):59-65
- **S1.3** · цикл создания ЗНИ · шаг 5.d.1 (modified) — классификатор до канона вопроса; смесь форм в одном ходе; kit `n/a` без вопроса; макет в new не спрашивать. [`.cursor/skills/openspec-new-change/SKILL.md`](.cursor/skills/openspec-new-change/SKILL.md):266-286
- **S1.4** · справка kit · раздел «Режим формы» (modified) — пропуск вопроса при «только модуль»; пустой ответ только на заданный вопрос. [`.cursor/docs/faq-kit.md`](.cursor/docs/faq-kit.md):22-32
- **S1.5** · быстрый старт · таблица сценариев и §5 (modified) — вопрос режима формы задаётся не всегда. [`.cursor/docs/quick-start.md`](.cursor/docs/quick-start.md):48-48, 78-80
- **S1.6–S1.8** · регресс readers · сверка по тексту (verified) — политика макета и lone `artifact_mode` не менялись. Apply/verify skills без правок этой ЗНИ.
