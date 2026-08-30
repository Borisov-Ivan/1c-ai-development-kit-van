# Срез S1 — Визуальное объяснение вместо карты сценария (2026-08-31)

- **S1.1** · скилл визуального объяснения · протокол просьбы и автопанели (created) — прямая просьба открывает панель из текущего ответа; на проверке постановки и ревью сами не открываем. [`.cursor/skills/visual-explanation/SKILL.md`](.cursor/skills/visual-explanation/SKILL.md):25-54
- **S1.2** · шаблон панели · рендер `flow` / `table` / `hierarchy` / `card` (created) — форма по содержанию, без графа с абсолютной раскладкой. [`.cursor/skills/visual-explanation/fixtures/panel-shell.md`](.cursor/skills/visual-explanation/fixtures/panel-shell.md):1-18
- **S1.3** · диспетчер · указатель просьбы (modified) — «покажи схему» ведёт к новому скиллу. [`.cursor/rules/gate-dispatcher.mdc`](.cursor/rules/gate-dispatcher.mdc):28-28
- **S1.4–S1.5** · делегирование и таблица моделей · роль сборщика снята (modified) — данные и файл пишет родитель. [`.cursor/rules/1c-agent-delegation.mdc`](.cursor/rules/1c-agent-delegation.mdc):29-29
- **S1.6** · исследование / разбор / описание · экзамен топологии и «текстовый резерв» сняты (modified) — предложение панели только если картинка упрощает ответ.
- **S1.7 / S1.12** · словари kit · визуальное объяснение вместо статьи старой карты (modified) — [`.cursor/docs/glossary.md`](.cursor/docs/glossary.md):21-21; таксономия `visual-explanation`.
- **S1.8** · старый конвейер · каталог скилла, агент и шаблон промпта (removed).
- **S1.9** · ADR-0010 · несущая замена ADR-0008 и ADR-0009 (created). [`openspec/adrs/ADR-0010-visual-explanation-panel.md`](openspec/adrs/ADR-0010-visual-explanation-panel.md):1-15
- **S1.10** · журнал соседней ЗНИ · продукт снят, не реализовывать (modified).
- **S1.11** · сверка kit · старого каталога и ссылок на него в рабочих глоссариях нет.

## Explain scope (handoff)

- source: apply
- change: universal-visual-explanation
- focus: slice-S1
- files: []
- note: срез без `.bsl`; разбор кода 1С не требуется
- report: openspec/changes/universal-visual-explanation/reports/code-map.md
