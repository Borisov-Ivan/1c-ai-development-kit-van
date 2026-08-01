# Поставка kit-шаблона в проект 1С

Как копировать и развивать Cursor-kit (**van**): поставка в sandbox/проект заказчика и эволюция самого шаблона.

## Что копировать

Обязательная поставка в проект 1С:

| Артефакт | Назначение |
|----------|------------|
| `.cursor/` | rules, skills, agents, docs, commands |
| `AGENTS.md` | навигационный индекс в корне проекта |

После копирования — **Reload Window** в Cursor. Внешние runtime (npm, Python) для базового контура `/opsx:*` **не** требуются. Скрипты обязательного контура — PowerShell 5.1.

Не копировать в consumer-проект как «часть поставки»:

- `openspec/changes/<имя-эволюции-kit>/` (рабочая ЗНИ эволюции шаблона);
- локальные `temp/`, отчёты исследования вне `.cursor`.

## Эволюция kit (метапроект)

1. ЗНИ эволюции (например Mode Gate, forms DX) ведётся **на ветке** репозитория kit.
2. В PR в `main` шаблона: изменения `.cursor/**` и `AGENTS.md`.
3. **Папку change** `openspec/changes/<kit-evolution-…>/` в `main` **не мержить** (или удалять при merge) — иначе consumer получает чужой WIP постановки.
4. Приёмка срезов эволюции — в **sandbox**: копия `.cursor`+`AGENTS.md` с ветки → Reload → учебный сценарий из Primary среза.

## Forms / MXL

Режим поставки **управляемой формы** в прикладной ЗНИ задаётся Mode Gate на этапе design `/opsx:new` — per-form `form_mode` / map `forms:` (см. `.cursor/rules/forms-mxl-mode-gate.mdc`). Макет (Template/MXL) в new не спрашивается; default на apply — вручную, non-manual только с разрешением. В метапроекте эволюции kit: `form_mode: n/a`.

## Связь

- Обзор / памятка: `README.md` (в корне репо kit; в рабочий проект 1С не копируется)
- Индекс команд и SSOT: `AGENTS.md`
- Mode Gate: `.cursor/rules/forms-mxl-mode-gate.mdc`
- Целостность поставки (перед version-cut): `.cursor/docs/delivery-integrity.md`
- Quick start / FAQ: `.cursor/docs/quick-start.md`, `.cursor/docs/faq-kit.md`
