---
name: /opsx:extend
id: opsx-extend
category: Workflow
description: Контролируемое расширение scope существующего change (новые задачи и требования; порядок — в скилле дописывания)
---

Контролируемо расширить scope активного change: пользователь описывает **новое требование**. Порядок чтения, обновление артефактов и следующий шаг читаются из скилла дописывания.

Ключ `-noapi` / `-api` пишется в любом сообщении чата и не является флагом этой команды.

Отделена от `/opsx:verify` — verify read-only для user-path; **repair-from-verify** — internal only (verify Repair Loop, без чата).

**Режимы:**
- **user-extend** — бриф + confirm → handoff на языке эффекта. Следующий шаг читается из скилла.
- **repair-from-verify** — internal из verify; **без** сообщений в чат; вызывается только из Repair Loop verify SKILL.

**Первое действие:** прочитать `.cursor/skills/openspec-extend-change/SKILL.md` и далее идти по его шагам. До прочтения скилла — никаких других чтений артефактов, отчётов, трасс или модулей.

**Input:** имя заявки, текст расширения и допустимые пути флага отчёта — абзац Input скилла дописывания. Без имени при ровно одной открытой заявке дописывается она. Свой перечень путей флага команда не держит.

**Примеры:**

- `/opsx:extend sample-change --from-review openspec/changes/sample-change/reports/review-sample-change-2026-04-29-subagent-raw.md "Пересмотреть решение по представлению роли"`
- `/opsx:extend add-auth --from-report temp/reports/trace-analysis-2026-04-29-token-rotation.md "Добавить требование по ротации токенов"`
- `/opsx:extend add-auth @temp/explore-handoff-2026-04-29-token-rotation.md "Учесть найденный риск"`

Своего списка шагов в этой команде нет.

**Ограничения:**
- Не вызывает writer/reviewer — реализация остаётся за `/opsx:apply`.
- Не применяется к архивным change.
