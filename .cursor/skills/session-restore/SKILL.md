---
name: kit-session-restore
description: Прочитать temp/session-notes.md и предложить следующую команду. Запрещено авто-запускать apply/writer. Вызов пользователя — команда /session-restore.
---

# session-restore

Восстановить контекст из `temp/session-notes.md` **без** автоматического apply.

## Когда

`/session-restore` или «продолжи с сохранённой сессии».

## Шаги

1. Если `temp/session-notes.md` нет — сообщить и предложить `/session-save` или описать задачу заново. END.
2. Прочитать файл. Показать в чат краткий каркас:
   - **Current** (1–2 предложения)
   - **Next** (нумерованный список как есть)
   - **Decisions** (если не «нет»)
   - **Links** (пути)
3. Предложить **одну** следующую команду по смыслу Next (`/opsx:explore`, `/opsx:apply <name>`, `/opsx:verify <name>`, …) — **только текстом**, не выполнять.
4. **HALT / запрещено в этом скилле:**
   - вызов `/opsx:apply` или writer/reviewer;
   - любые Write/StrReplace по `.bsl` / `src/**/*.xml`;
   - «молча продолжить реализацию».

Пользователь сам вводит предложенную команду или уточняет фокус.

## Guardrails

Restore = навигация, не исполнение.
