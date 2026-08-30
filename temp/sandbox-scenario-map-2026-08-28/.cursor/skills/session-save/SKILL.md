---
name: kit-session-save
description: Сохранить компактные заметки текущей сессии в temp/session-notes.md для продолжения в новом чате. Без apply и без правок кода. Вызов пользователя — команда /session-save.
---

# session-save

Сохранить контекст сессии в `temp/session-notes.md` (каталог `temp/` уже в `.gitignore`).

## Когда

Пользователь просит сохранить сессию / handoff / «продолжу в другом чате» / `/session-save`.

## Шаги

1. Создать `temp/` при необходимости.
2. Записать (перезаписать) `temp/session-notes.md`:

```markdown
# Session notes — <YYYY-MM-DD HH:MM>

## Current
<1–3 предложения: что сделано / где остановились>

## Next
1. <императивный следующий шаг>
2. …

## Decisions
- <зафиксированные решения сессии; если нет — «нет»>

## Links
- <пути к proposal/design/tasks/reports — только ссылки>
```

3. **Не** запускать `/opsx:apply`, writer, reviewer, правки `.bsl` / XML.
4. В чат: одна строка — путь к файлу + «для продолжения: `/session-restore`».

## Guardrails

- Не дублировать содержимое артефактов OpenSpec — только ссылки.
- Не писать секреты / строки подключения к ИБ.
