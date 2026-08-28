# Карта правок — scenario-map-canvas

# Срез S1 — Карта сценария по просьбе и намёк на выходе разбора (2026-08-27)

- **S1.1–S1.7** · скилл карты сценария · SKILL.md (created) — контракт панели, пороги, fallback в журнал, эталон узлов. [`.cursor/skills/scenario-map-canvas/SKILL.md`](../../../../.cursor/skills/scenario-map-canvas/SKILL.md)
- **S1.8** · диспетчер гейтов · gate-dispatcher.mdc (modified) — триггер просьбы и подавление системного canvas. [`.cursor/rules/gate-dispatcher.mdc`](../../../../.cursor/rules/gate-dispatcher.mdc)
- **S1.9–S1.10a** · разбор explain · SKILL.md, exit-card.md, explain-report.md (modified) — просьба в середине прохода, намёк в «Следующий шаг», секция журнала. [`.cursor/skills/openspec-explain/SKILL.md`](../../../../.cursor/skills/openspec-explain/SKILL.md)
- **S1.11** · словарь · chat-lexicon.md, openspec/glossary.md (modified/created) — разведены «карта точек» и «карта сценария». [`.cursor/docs/chat-lexicon.md`](../../../../.cursor/docs/chat-lexicon.md)
- **S1.12** · индекс кита · AGENTS.md (modified) — указатель на скилл карты сценария. [`AGENTS.md`](../../../../AGENTS.md)
- **S1.13** · сверка · — (verified) — отдельной команды нет; проверка inventory-card снята в S3.2.

# Срез S2 — Карта показывает причинность (2026-08-28)

- **S2.1–S2.4a** · скилл карты · SKILL.md (modified) — шапка, узлы, связи, виды, словарь, порог после двух отсевов, создание панели с нуля. [`.cursor/skills/scenario-map-canvas/SKILL.md`](../../../../.cursor/skills/scenario-map-canvas/SKILL.md)
- **S2.1b / S2.4b / S2.8a / S2.13** · регистрация родителя · SKILL.md, агент, canvas-shell.md (modified/created) — манифест картографа, файл пишет родитель, штатная кнопка среды, `openFile`, без `newComposerChat`. [`.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`](../../../../.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md)
- **S2.2–S2.3** · эталоны · map-good-causal.md, map-bad-accordion.md (created) — граф со слоями, `evidence_ref` у рёбер, запрет списка без рёбер. [`.cursor/skills/scenario-map-canvas/fixtures/map-good-causal.md`](../../../../.cursor/skills/scenario-map-canvas/fixtures/map-good-causal.md)
- **S2.5** · журнал разбора · explain-report.md, SKILL.md, exit-card.md (modified) — секция «Схема (текстовый резерв)». [`.cursor/skills/openspec-explain/templates/explain-report.md`](../../../../.cursor/skills/openspec-explain/templates/explain-report.md)
- **S2.6** · диспетчер · gate-dispatcher.mdc (modified) — рисовать по просьбе или согласию; намёк только предлагает. [`.cursor/rules/gate-dispatcher.mdc`](../../../../.cursor/rules/gate-dispatcher.mdc)
- **S2.8–S2.11** · картограф · агент, таблица ролей, указатели (created/modified) — манифест на модели чата. [`.cursor/agents/onec-scenario-map-designer.md`](../../../../.cursor/agents/onec-scenario-map-designer.md)

## Explain scope (handoff)

- source: apply
- change: scenario-map-canvas
- focus: slice-S2
- files:
  - path: .cursor/skills/scenario-map-canvas/SKILL.md
  - path: .cursor/agents/onec-scenario-map-designer.md
- report: openspec/changes/scenario-map-canvas/reports/code-map.md

# Срез S3 — Команды предлагают схему по топологии (2026-08-28)

- **S3.1** · скилл карты · SKILL.md (modified) — проверка топологии как единственный контракт предложения. [`.cursor/skills/scenario-map-canvas/SKILL.md`](../../../../.cursor/skills/scenario-map-canvas/SKILL.md)
- **S3.2** · карта точек · inventory-card.md (modified) — вариант «сразу карту» в строке подтверждения. [`.cursor/skills/openspec-explain/templates/inventory-card.md`](../../../../.cursor/skills/openspec-explain/templates/inventory-card.md)
- **S3.3–S3.4** · выход разбора · exit-card.md, explain SKILL.md (modified) — намёк по топологии, без замеров; отложенная постройка. [`.cursor/skills/openspec-explain/templates/exit-card.md`](../../../../.cursor/skills/openspec-explain/templates/exit-card.md)
- **S3.5** · исследование · explore SKILL.md (modified) — в «Дальше» схема или разбор, не оба. [`.cursor/skills/openspec-explore/SKILL.md`](../../../../.cursor/skills/openspec-explore/SKILL.md)
- **S3.6** · словарь · chat-lexicon.md, glossary.md (modified) — три имени: карта точек, карта сценария, текстовый резерв. [`.cursor/docs/chat-lexicon.md`](../../../../.cursor/docs/chat-lexicon.md)

## Explain scope (handoff)

- source: apply
- change: scenario-map-canvas
- focus: slice-S3
- files:
  - path: .cursor/skills/openspec-explore/SKILL.md
  - path: .cursor/skills/openspec-explain/templates/inventory-card.md
- report: openspec/changes/scenario-map-canvas/reports/code-map.md
