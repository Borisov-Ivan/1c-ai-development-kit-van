# Карта правок

# Срез S1 — Место среза и шаг принять (2026-10-15)

- **S1.1** · правило чата · абзац фразы места (modified) — на передаче видно, последний это срез или промежуточный, и рядом три ответа сдачи. [`.cursor/docs/opsx-output-style.md`](.cursor/docs/opsx-output-style.md):387-393
- **S1.2** · карточка ожидания объектов · слот фразы места (modified) — номер среза стоит перед списком «что создать», список не сокращается. [`.cursor/skills/openspec-apply-change/templates/pause-wait-chat.md`](.cursor/skills/openspec-apply-change/templates/pause-wait-chat.md):9-10
- **S1.8** · разработка · карточка сдачи (modified) — если сдача предполагается, три ответа, сессия заканчивается, ответ на следующем запуске. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):396-400
- **S1.9** · правило срезов · отметка «приёмка в конце» (modified) — отдельная сдача только у изолированного блока; у промежуточного среза с отметкой статус не спрашивается. [`.cursor/rules/vertical-slices.mdc`](.cursor/rules/vertical-slices.mdc):194-198
- **S1.10** · проверка · граница сдачи (modified) — на границе три ответа, а пока рабочие задачи пустые, остаётся «можно запускать apply». [`.cursor/rules/verify-user-communication.mdc`](.cursor/rules/verify-user-communication.mdc):29-32
- **S1.16** · проверка · маска отметок (modified) — смена только отметок рабочих задач не открывает новый вопрос и не снимает паузу приёмки. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):167-167

# Срез S2 — Вопрос только при смене результата (2026-10-15)

- **S2.1** · пакет вопросов · состав карточки (modified) — в карточке только темы, чьи ответы меняют результат; тема без смены результата отдельно не спрашивается. [`.cursor/docs/templates/decision-block.md`](.cursor/docs/templates/decision-block.md):137-140
- **S2.2** · доказательство · место возникновения (modified) — если объекта ещё нет, карточка говорит, что вопрос о тексте плана. [`.cursor/docs/templates/decision-block.md`](.cursor/docs/templates/decision-block.md):44-44
- **S2.6** · проверка · пустая предпосылка (modified) — пустая предпосылка молча пропускается только у решения без смены результата. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):168-168
- **S2.10** · проверка · сохранение ответа (modified) — абзац, который только хранит уже данный ответ, не открывает вопрос про отдельную запись. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):236-236
- **S2.11** · пакет вопросов · смена результата с ответа (modified) — в той же карточке видно, что было в ответе и что стало. [`.cursor/docs/templates/decision-block.md`](.cursor/docs/templates/decision-block.md):139-139

# Срез S3 — Свежесть проверки и цена прогона (2026-10-15)

- **S3.1** · вход в разработку · признак проверки (modified) — если отчёта проверки нет, шаг говорит, что проверка не выполнялась, и вне карточки сдачи оставляет выбор. [`.cursor/skills/openspec-apply-change/SKILL.md`](.cursor/skills/openspec-apply-change/SKILL.md):89-94
- **S3.2** · снимок состояния · тот же признак (modified) — человек видит, что проверки не было или она устарела. [`.cursor/skills/openspec-status/SKILL.md`](.cursor/skills/openspec-status/SKILL.md):67-70
- **S3.3** · полный разбор · объём (modified) — уже закрытое без нового факта не пересказывается. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):364-364
- **S3.5** · глубина прогона · локальная дельта (modified) — один изменённый приёмочный атрибут не запускает полный прогон. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):110-110
- **S3.6** · карточка проверки · предупреждение (modified) — предупреждение стоит одним предложением после шага и не выглядит выбором. [`.cursor/skills/openspec-verify-change/templates/chat-summary.md`](.cursor/skills/openspec-verify-change/templates/chat-summary.md):134-134
