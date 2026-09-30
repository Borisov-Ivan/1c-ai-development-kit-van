# Срез S1 — Замена значения без проверки (2026-09-30)

Кода 1С в срезе нет. Ниже — правки текстов kit.

- **S1.2–S1.7** · проверка постановки · таблица глубины (modified) — класс «замена значения» и точечный проход, который сверяет только значение. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md):92-116
- **S1.8** · снимок отчёта · база оси (modified) — после замены значения в снимок пишется текущий хэш оси, время разбора не меняется. [`.cursor/skills/openspec-verify-change/templates/report-header.md`](.cursor/skills/openspec-verify-change/templates/report-header.md):93-93
- **S1.9–S1.15** · дополнение постановки · замена значения (modified) — оценка воздействия, поиск старого значения, три исхода, итог в чат. [`.cursor/skills/openspec-extend-change/SKILL.md`](.cursor/skills/openspec-extend-change/SKILL.md):424-467
- **S1.17–S1.18** · маршрут команд (modified) — замена утверждённого значения идёт к реализации без проверки постановки. [`.cursor/rules/sdd-workflow.mdc`](.cursor/rules/sdd-workflow.mdc):17-17
- **S1.19** · требование «Ответ не перезапускает всё» (created) — исключение: замена значения полного разбора не даёт. [`openspec/changes/pipeline-light-route/specs/verify-stop-repeat/spec.md`](openspec/changes/pipeline-light-route/specs/verify-stop-repeat/spec.md):1-12
- **S1.24–S1.25** · учебная памятка `fixture-light-route-color` (created) — два среза, первый принят; полная проверка позволяет реализовывать.

# Срез S2 — Архив без повторного прогона (2026-09-30)

Кода 1С нет.

- **S2.2–S2.3** · снимок · ключи хэша (modified) — сырой и нормализованный ключ `tasks.md`, ключ `debug.md` без секции приёмки. [`.cursor/skills/openspec-verify-change/templates/report-header.md`](.cursor/skills/openspec-verify-change/templates/report-header.md)
- **S2.4–S2.7** · проверка · отметка приёмки (modified) — строка «Между срезами» читает нормализованный ключ; быстрый путь учитывает текущий режим. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md)
- **S2.8** · архив · свежесть финала (modified) — три ветки, без повторного прогона если постановка не менялась. [`.cursor/skills/openspec-archive-change/SKILL.md`](.cursor/skills/openspec-archive-change/SKILL.md)

# Срез S3 — Отчёт повторного прогона без копий (2026-09-30)

Кода 1С нет.

- **S3.3–S3.6** · отчёт повторного прогона (modified) — из снимка неполной глубины убраны копии списка задач и журнала решений, добавлена ссылка на предыдущий отчёт, вместо пересказа постановки — что изменилось. [`.cursor/skills/openspec-verify-change/SKILL.md`](.cursor/skills/openspec-verify-change/SKILL.md), [`.cursor/skills/openspec-verify-change/templates/report-header.md`](.cursor/skills/openspec-verify-change/templates/report-header.md), [`.cursor/skills/openspec-verify-change/templates/executive-summary.md`](.cursor/skills/openspec-verify-change/templates/executive-summary.md)
- **S3.9–S3.10** · учебная сводка `fixture-light-route-delta-report` (created) — полный отчёт, затем повторный после ответа заказчика внутри выбранного подхода.


