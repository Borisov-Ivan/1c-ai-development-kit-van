---
name: /review
id: review
category: Quality
description: Full code review by request context (module, files, extension) with option to fix findings via writer and reviewer
---

Провести полное подробное ревью кода в объёме по контексту запроса (модуль, файлы, расширение), затем по желанию — устранение замечаний через onec-code-writer с повторным ревью.

**Input**: Опционально — путь к модулю (.bsl), список файлов, имя расширения или «текущий файл». Если не указано — определить по контексту или уточнить у пользователя.

**FIRST AND ONLY action**: Read `.cursor/skills/review/SKILL.md`.
Do NOT read any other files, traces, or modules in the same tool call.
After reading the skill, follow its instructions step by step before taking any other action.
