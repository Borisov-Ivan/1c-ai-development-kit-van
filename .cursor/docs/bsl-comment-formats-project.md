# Соглашения по комментариям BSL — навигация

**SSOT механики (kit):** [marker-canon.md](marker-canon.md) — грамматика маркера, MERGE-001, PLACEMENT-001, baseline запреты domain_label, дефолтный FORMAT, CRC, zero-config.

**SSOT значений (project):** [openspec/project.md](../../openspec/project.md) — `defaultDeveloper`, `cfMarkerPrefix`, строки **Whitelist предрелиза** и **Обязательный контроль**.

Таблица Whitelist в project.md — **project-level overlay** для rule 17 в `.cursor/docs/1c-coding-standards.md` и release-hygiene: комментарии в whitelist **exempt от удаления** (AP-040); **содержимое** domain_label — AP-053 (baseline запреты — `marker-canon.md`); **язык** — AP-054.

**Обзор четырёх слоёв:** [marker-layers-guide.md](marker-layers-guide.md). Снимок по change: `/opsx:status <name>`.

Фреймворк использует плейсхолдеры `{developer}`, `{cfMarkerPrefix}`, `<ФИО>` — значения из project.md и proposal.md; механика — из `marker-canon.md`.

## Whitelist (колонки)

| Колонка | Смысл |
|--------|--------|
| **Префикс после `//`** | После `//` и пробелов комментарий начинается с подстроки → строка в whitelist. |
| **Regex на всю строку `//…`** | Вся строка комментария удовлетворяет шаблону → whitelist. |
| **Scope (glob)** | Путь файла в выгрузке; строка применяется только в этом scope. |

При **отсутствии** таблицы или пустой таблице — kit default: строгая гигиена без exempt (см. `marker-canon.md` § Whitelist).

## Обязательный контроль (колонки)

| Колонка | Смысл |
|--------|--------|
| **Где проверять** | Scope: перехваты, первый комментарий после `#Вставка`, весь модуль и т.д. |
| **Regex допустимой строки `//…`** | Для mandatory control в `/review` и `/release-review`: первая значимая строка `//` после `#Вставка` должна совпадать; иначе — замечание. |
| **Уровень / kind** | Попадает в отчёт и в tasks при создании change. |

## Project overlay (что можно добавить в project.md)

| Тип | Пример |
|-----|--------|
| Whitelist regex | Legacy `// НАЧАЛО` в scope конкретного расширения |
| AP-054 allow-list | Доменные аббревиатуры (`Диадок`, провайдер ЭДО) |
| domain_label allow | Продуктовые термины, не входящие в kit baseline |

Проект **расширяет** kit baseline, **не сокращает** (CRC § LIST).
