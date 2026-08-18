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

Это правило **репозитория шаблона kit**, не цикл ЗНИ в проекте 1С. В конфигурации заказчика ветки `develop`/`main` kit не заводить.

1. **`develop`** — линия разработки kit: открытые ЗНИ эволюции и их архивы (`openspec/changes/`, `openspec/changes/archive/`). Короткую фича-ветку сразу сливать в `develop`, не оставлять домом архива.
2. **`main`** — поставка шаблона: `.cursor/**`, `AGENTS.md`, `README.md`, `openspec/specs/`, `openspec/adrs/`, `openspec/changes/_template`. Без рабочих папок `openspec/changes/<имя>` и без `openspec/changes/archive/`.
3. Обновление поставки: слить в `main` с `develop` и убрать с `main` архивы/WIP ЗНИ. В consumer-проект по-прежнему копируют только `.cursor/` + `AGENTS.md`.
4. Приёмка срезов эволюции — в **sandbox**: копия `.cursor`+`AGENTS.md` с `develop` (или с фича-ветки до слияния) → Reload → учебный сценарий из Primary среза.

## Forms / MXL

Режим поставки **управляемой формы** в прикладной ЗНИ задаётся Mode Gate на этапе design `/opsx:new` — per-form `form_mode` / map `forms:` (см. `.cursor/rules/forms-mxl-mode-gate.mdc`). Макет (Template/MXL) в new не спрашивается; default на apply — вручную, non-manual только с разрешением. В метапроекте эволюции kit: `form_mode: n/a`.

## Связь

- Обзор / памятка: `README.md` (в корне репо kit; в рабочий проект 1С не копируется)
- Индекс команд и SSOT: `AGENTS.md`
- Mode Gate: `.cursor/rules/forms-mxl-mode-gate.mdc`
- Целостность поставки (перед version-cut): `.cursor/docs/delivery-integrity.md`
- Quick start / FAQ: `.cursor/docs/quick-start.md`, `.cursor/docs/faq-kit.md`
