# Срез S1 — Развилка после последнего среза (2026-08-30)

Kit meta-change (без продуктового BSL). Карта правок скилла реализации, памятки оформления и памятки ревью.

- **S1.1** · скилл реализации · шаг 6 шортката «принято» (modified) — единственная формулировка развилки: подтверждение приёмки, фраза про допись постановки, три слова. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):422-425
- **S1.2** · скилл реализации · условие `ревью` (modified) — слово только при `marker_scope` `cfe` или `mixed`; пустой и `cf-ea` — прежний вопрос `архив` / `стоп`. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):423-424
- **S1.3** · скилл реализации · шаг 7 разбор ответа (modified) — `ревью` печатает `/release-review <имя>` без запуска предрелиза; `архив` и `стоп` как раньше. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):426-429
- **S1.4** · скилл реализации · ветка «принят» (modified) — последний срез ведёт на ту же развилку, не на следующий срез и не на отдельную карточку. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):165-165
- **S1.5** · скилл реализации · вход «все задачи закрыты» (modified) — после признака кода расширения ход идёт на карточку завершения, без своего «предлагаю архив». [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):69-69
- **S1.6** · скилл реализации · карточка завершения (modified) — в чате та же развилка; в файле handoff — перечень команд без вопроса. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):534-534
- **S1.7** · памятка оформления · строка `final` (modified) — при коде расширения сигнал «ответьте в чате», без кода расширения — строка архива. [`.cursor/docs/opsx-output-style.md`](.cursor/docs/opsx-output-style.md):390-390
- **S1.8** · памятка ревью · таблица «Когда что вызывать» (modified) — строка после приёмки последнего среза, команда `/release-review <change>`. [`.cursor/docs/review-guide.md`](.cursor/docs/review-guide.md):29-29
- **S1.9** · шаблон проверки постановки (check) — слот следующего шага после реализации по-прежнему `/opsx:archive`; развилки нет. [`.cursor/skills/openspec-verify-change/templates/chat-summary.md`](.cursor/skills/openspec-verify-change/templates/chat-summary.md):12-12
- **S1.10** · сверка единства (check) — формулировка в одном месте шага 6; возврат, ранний выход и карточка ссылаются на неё; новых команд и детекторов нет.
