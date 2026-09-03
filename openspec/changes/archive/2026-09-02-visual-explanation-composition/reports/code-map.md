# Срез S1 — Читаемое объяснение на панели (2026-08-31)

- **S1.1** · навык визуального объяснения · критерий авто и рассказ (modified) — после разбора механизма слоями панель открывается или намекается; на полотне вопрос, вывод, скелет и одна сцена. [`.cursor/skills/visual-explanation/SKILL.md`](.cursor/skills/visual-explanation/SKILL.md):3-77
- **S1.1** · пошаговый разбор · скобка в предложении панели (modified) — снята ссылка на закрытый перечень авто; локальный намёк «ветки, условия или уровни» прежний. [`.cursor/skills/openspec-explain/SKILL.md`](.cursor/skills/openspec-explain/SKILL.md):137-139
- **S1.2** · шаблон панели · скелет со сценами (modified) — пример учит скелет с фокусом и шагами истории, не сетку; ветка таблицы для сравнения свойств на месте. [`.cursor/skills/visual-explanation/fixtures/panel-shell.md`](.cursor/skills/visual-explanation/fixtures/panel-shell.md):1-361
- **S1.3** · исследование · слот «Дальше» (modified) — намёк на панель, когда без картинки путаются части, слои или случаи. [`.cursor/skills/openspec-explore/SKILL.md`](.cursor/skills/openspec-explore/SKILL.md):217-217
- **S1.4** · опорное решение панели · два инварианта (modified) — авто по путанице слоёв; много частей остаются скелетом, таблица только для сравнения свойств. [`openspec/adrs/ADR-0010-visual-explanation-panel.md`](openspec/adrs/ADR-0010-visual-explanation-panel.md):8-30

# Срез S2 — Полотно как спутник сопоставления (2026-09-01)

- **S2.1** · навык визуального объяснения · работа над текстом, затем язык картинки (modified) — сначала одна работа над уже сказанным; скелет только для слоёв; сопоставление не становится конвейером на голую просьбу показать схему; файл только если полотно даёт восприятие, которого нет в тексте. [`.cursor/skills/visual-explanation/SKILL.md`](.cursor/skills/visual-explanation/SKILL.md):26-88
- **S2.2** · шаблон панели · библиотека рецептов (modified) — классификация рядом без обязательных кнопок; колонка = именованный класс, не пункт; копия без поля формы не падает в скелет; пустые связи не рисуют стрелки следования. [`.cursor/skills/visual-explanation/fixtures/panel-shell.md`](.cursor/skills/visual-explanation/fixtures/panel-shell.md):15-404
- **S2.3** · опорное решение панели · инвариант формы (modified) — перечень форм как подсказка рецепта, не закрытый мир; нет умолчания скелета. [`openspec/adrs/ADR-0010-visual-explanation-panel.md`](openspec/adrs/ADR-0010-visual-explanation-panel.md):12-27
- **S2.4** · сверка kit · чеклист среза (modified) — навык, шаблон и опорное решение совпадают с дельтой сопоставления; слот исследования и намёк в разборе не сверялись. [`.cursor/skills/visual-explanation/SKILL.md`](.cursor/skills/visual-explanation/SKILL.md):26-88

## Explain scope (handoff)

- source: apply
- change: visual-explanation-composition
- focus: slice-S2
- files:
  - path: .cursor/skills/visual-explanation/SKILL.md
  - path: .cursor/skills/visual-explanation/fixtures/panel-shell.md
  - path: openspec/adrs/ADR-0010-visual-explanation-panel.md
- report: openspec/changes/visual-explanation-composition/reports/code-map.md

