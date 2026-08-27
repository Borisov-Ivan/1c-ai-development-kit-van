# Поставка kit-шаблона в проект 1С

Как копировать и развивать Cursor-kit (**van**): поставка в sandbox/проект заказчика и эволюция самого шаблона.

## Что копировать

Обязательная поставка в проект 1С:

| Артефакт | Назначение |
|----------|------------|
| `.cursor/` | rules, skills, agents, docs, commands, заготовки `templates/seed/` |
| `AGENTS.md` | навигационный индекс в корне проекта |

После копирования — **Reload Window** в Cursor. Внешние runtime (npm, Python) для базового контура `/opsx:*` **не** требуются. Скрипты обязательного контура — PowerShell 5.1.

Не копировать в consumer-проект как «часть поставки»:

- `README.md` репозитория kit (устройство веток; сценарии живут в `.cursor/docs/quick-start.md`);
- `openspec/` репозитория kit (specs/ADR/архивы эволюции шаблона);
- `tools/`;
- локальные `temp/`, отчёты исследования вне `.cursor`.

В проекте 1С каталог `openspec/` создаёт `/init-project` из заготовок `.cursor/templates/seed/`.

## Эволюция kit (метапроект)

Это правило **репозитория шаблона kit**, не цикл ЗНИ в проекте 1С. В конфигурации заказчика ветки `develop`/`main` kit не заводить.

1. **`develop`** — линия разработки kit: открытые ЗНИ эволюции и их архивы (`openspec/changes/`, `openspec/changes/archive/`), утилиты `tools/`. Короткую фича-ветку сразу сливать в `develop`, не оставлять домом архива.
2. **`main`** — поставка шаблона: `.cursor/**`, `AGENTS.md`, `README.md`, `openspec/specs/`, `openspec/adrs/`. Без рабочих папок `openspec/changes/<имя>`, без `openspec/changes/archive/`, без `tools/`. Заготовка шаблона ЗНИ — `.cursor/templates/seed/changes/_template/`.
3. **Обновление поставки** (только из репозитория kit):
   - рабочее дерево чистое, нужные правки уже на `develop`;
   - `git checkout main`;
   - `git merge develop`;
   - удалить с `main`: `openspec/changes/archive/`, рабочие `openspec/changes/<имя>` (если влились), каталог `tools/`;
   - коммит снятия архивов и утилит;
   - `git push origin main` (обычный push, без `--force`);
   - в consumer-проект снова скопировать только `.cursor/` + `AGENTS.md`.
4. На `main` содержательные коммиты не делать: только merge из `develop` и cleanup-коммит снятия архивов/утилит.
5. Приёмка срезов эволюции — в **sandbox**: копия `.cursor`+`AGENTS.md` с `develop` (или с фича-ветки до слияния) → Reload → учебный сценарий из Primary среза.

## Forms / MXL

Режим поставки **управляемой формы** в прикладной ЗНИ задаётся Mode Gate на этапе design `/opsx:new` — per-form `form_mode` / map `forms:` (см. `.cursor/rules/forms-mxl-mode-gate.mdc`). Макет (Template/MXL) в new не спрашивается; default на apply — вручную, non-manual только с разрешением. В метапроекте эволюции kit: `form_mode: n/a`.

## Связь

- Устройство репозитория и веток: `README.md` (в корне репо kit; в рабочий проект 1С не копируется)
- Сценарии и команды: `.cursor/docs/quick-start.md` (едет в поставку)
- Индекс команд и SSOT: `AGENTS.md`
- Mode Gate: `.cursor/rules/forms-mxl-mode-gate.mdc`
- Целостность поставки (перед version-cut): `.cursor/docs/delivery-integrity.md`
- FAQ: `.cursor/docs/faq-kit.md`
