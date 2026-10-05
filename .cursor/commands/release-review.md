---
name: /release-review
id: release-review
category: Quality
description: Предрелизное ревью расширения или change — Category 12, эскалация severity, Tier 2 explorer
---

Предрелизный контроль перед выкладкой: все `.bsl` расширения или change-scoped Tier 1 + архитектурный обзор всего расширения (Tier 2). Делегирование **onec-code-reviewer** с `mode=prerelease`.

Ключ `-noapi` / `-api` пишется в любом сообщении чата и не является флагом этой команды.

**Режим (фиксированно):** `release_mode = true` — см. шаг 0 в [`.cursor/skills/review/SKILL.md`](../skills/review/SKILL.md).

**Input**: разбор вызова, в том числе пустого, — шаг 1.0 скилла `.cursor/skills/review/SKILL.md`. Команда свой разбор «аргумент обязателен» и таблицу трёх вызовов не держит.

**Памятка заказчика:** [`.cursor/docs/review-guide.md`](../docs/review-guide.md) — когда `/review` vs `/release-review`, отличия от apply-reviewer.

**Первое действие:** прочитать `.cursor/skills/review/SKILL.md` с пометкой «вызов `/release-review` → `release_mode=true`» и далее идти по шагам skill. До прочтения скилла — никаких чтений артефактов, трасс, модулей.

После отчёта: тот же протокол disposition, что и `/review` (шаг 4.5 skill). Выбор as-designed на quality weak **не** снимает Category 12 / release-hygiene без отдельного waive. Ниже приоритета fix/extend финал MAY предложить `/opsx:explain` с **Вариантами** рамки — см. [review-guide.md](../docs/review-guide.md).
