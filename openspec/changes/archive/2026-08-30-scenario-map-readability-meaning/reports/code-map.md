# Срез S1 — Читаемая карта со смыслом (2026-08-29)

- **S1.1** · шаблон панели · `computeLayerBands` (created) — полосы собираются из поля слоя узлов, а не из ранга раскладки. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):157-185
- **S1.2** · шаблон панели · стрелки и легенда (modified) — маркер направления, цвет и пунктир по типу связи, легенда использованных типов, обратное ребро изгибом. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):408-460
- **S1.3** · шаблон панели · выбор узла (modified) — клик только выделяет узел; файл открывается кнопкой «Открыть доказательство». [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):468-478
- **S1.4** · шаблон панели · обязательные пункты (modified) — лимиты заголовка и подписи ребра, запрет кавычек кода и нового чата. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):5-23
- **S1.5** · скилл карты · шаг «Макет» (modified) — проверка смысла по манифесту до записи файла. [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):47-49
- **S1.6** · скилл карты · шаг «Регистрация» (modified) — чек-лист читаемости по записанному файлу. [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):50-52
- **S1.7** · скилл карты · контракт клика (modified) — выбор показывает эффект, файл открывается кнопкой. [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):50-50
- **S1.8** · скилл карты · текстовый резерв (modified) — провал смысла не уходит в резерв. [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):215-221
- **S1.9** · скилл карты · self-check `6a`/`6b`/`8a` (created). [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):270-289
- **S1.10** · скилл карты · `focus_node` и `modes` (created). [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):64-116
- **S1.11** · роль сборщика · несколько источников (modified). [`.cursor/agents/onec-scenario-map-designer.md`](.cursor/agents/onec-scenario-map-designer.md):18-26
- **S1.12** · роль сборщика · расхождения как кандидаты (modified). [`.cursor/agents/onec-scenario-map-designer.md`](.cursor/agents/onec-scenario-map-designer.md):48-62
- **S1.13** · эталон «граф без смысла» (created). [`.cursor/skills/scenario-map-canvas/fixtures/map-bad-no-insight.md`](.cursor/skills/scenario-map-canvas/fixtures/map-bad-no-insight.md):1-20
- **S1.14** · скилл карты · три эталона в связанных артефактах и разделе эталонов (modified). [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):19-19
- **S1.15** · шаблон панели · аннотации у якоря (created). [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):522-564
- **S1.16** · скилл карты · контракт `annotations` (created). [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):118-128
- **S1.17** · скилл карты · self-check `6c`/`6d` (created). [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):282-283
- **S1.18** · роль сборщика · возврат аннотаций (modified). [`.cursor/agents/onec-scenario-map-designer.md`](.cursor/agents/onec-scenario-map-designer.md):39-62
- **S1.19** · хороший эталон · короткий label, `focus_node`, аннотация ловушки (modified). [`.cursor/skills/scenario-map-canvas/fixtures/map-good-causal.md`](.cursor/skills/scenario-map-canvas/fixtures/map-good-causal.md):14-128
- **S1.20** · сверка контрактов (modified) — словари и запреты сохранены; соседняя дельта клика выровнена. [`openspec/changes/overview-map-offer/specs/scenario-map-canvas/spec.md`](openspec/changes/overview-map-offer/specs/scenario-map-canvas/spec.md):61-64
- **S1.21** · шаблон панели · проверка типов носителя (modified) — якорь аннотации сужается локально, `key` только на нативных обёртках. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):22-22
- **S1.22** · скилл карты · регистрация (modified) — прямая запись с чистой проверкой типов; дамп оболочки не регистрирует кнопку. [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):50-50

# Срез S1 — Читаемая карта со смыслом (2026-08-30)

- **S1.1** · шаблон панели · полосы по слою (modified) — узлы одного слоя в одной полосе; подпись — имя слоя, не ранг; смешанный ряд без подписи. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):165-198
- **S1.2** · шаблон панели · связи и легенда (modified) — маркер направления, цвет и пунктир по типу, легенда под графом; поле режимов убрано. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):1-25
- **S1.4** · шаблон панели · скрыть шапку (modified) — живой переключатель прячет заголовок и вывод, полотно и детали остаются. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):422-433
- **S1.9** · скилл карты · `6a` и `8a` (modified) — ответ при скрытой шапке; до записи только поля манифеста; бюджет разборчивости. [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):287-296
- **S1.10** · скилл карты · `header.medium` (modified) — граф или таблица; стартовый узел — исход или виновник; режимы сняты. [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):69-78
- **S1.11** · роль сборщика · несколько источников и `medium` (modified). [`.cursor/agents/onec-scenario-map-designer.md`](.cursor/agents/onec-scenario-map-designer.md):18-49
- **S1.13** · эталон «полотно без смысла» (modified) — вывод только в шапке; предикат скрытой шапки. [`.cursor/skills/scenario-map-canvas/fixtures/map-bad-no-insight.md`](.cursor/skills/scenario-map-canvas/fixtures/map-bad-no-insight.md):1-20
- **S1.14** · скилл карты · эталоны (modified) — граф, таблица, список без рёбер, полотно без смысла. [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):19-19
- **S1.15** · шаблон панели · аннотация у якоря (modified) — не правая колонка. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):280-292
- **S1.19** · хороший эталон графа (modified) — подписи рёбер до четырёх слов, стартовый исход, ловушка на событии сброса. [`.cursor/skills/scenario-map-canvas/fixtures/map-good-causal.md`](.cursor/skills/scenario-map-canvas/fixtures/map-good-causal.md):8-15
- **S1.23** · шаблон панели · бюджет разборчивости (modified) — натуральный размер, горизонтальная прокрутка, перенос ряда длиннее пяти. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):231-277
- **S1.24** · шаблон и скилл · таблица колонок (modified) — `header.medium`, колонки имя / слой / эффект / доказательство. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md):448-456
- **S1.25** · эталон таблицы (created) — правило о условиях отвечает на вопрос при скрытой шапке. [`.cursor/skills/scenario-map-canvas/fixtures/map-good-table.md`](.cursor/skills/scenario-map-canvas/fixtures/map-good-table.md):1-16
- **S1.26** · скилл и роль · порог по средству (modified) — граф отсекает без связи, таблица только без доказательства. [`.cursor/skills/scenario-map-canvas/SKILL.md`](.cursor/skills/scenario-map-canvas/SKILL.md):45-48
- **S1.20** · сверка контрактов (modified) — словари, порог, регистрация, ADR-0008/0009, эталоны. [`openspec/changes/scenario-map-readability-meaning/specs/scenario-map-canvas/spec.md`](openspec/changes/scenario-map-readability-meaning/specs/scenario-map-canvas/spec.md):1-40

## Explain scope (handoff)

- source: apply
- change: scenario-map-readability-meaning
- focus: slice-S1
- files:
  - path: .cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md
    procedures: [computeLayerBands, wrapLayout, annotationBox]
  - path: .cursor/skills/scenario-map-canvas/SKILL.md
  - path: .cursor/agents/onec-scenario-map-designer.md
  - path: .cursor/skills/scenario-map-canvas/fixtures/map-good-causal.md
  - path: .cursor/skills/scenario-map-canvas/fixtures/map-good-table.md
  - path: .cursor/skills/scenario-map-canvas/fixtures/map-bad-no-insight.md
- report: openspec/changes/scenario-map-readability-meaning/reports/code-map.md
