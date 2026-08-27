# Поставка kit-шаблона в проект 1С

Как публиковать и развивать Cursor-kit (**van**). Этот документ — для того, кто **развивает** kit. Как поставить kit в проект 1С — [kit-as-submodule.md](./kit-as-submodule.md).

## Две ветки

| Ветка | Что в ней | Кто пользуется |
|-------|-----------|----------------|
| `develop` | Разработка kit: `.cursor/`, `AGENTS.md`, `openspec/` (спеки, ADR, ЗНИ эволюции), `doc/`, `tools/` | вы, когда правите kit |
| `main` | Поставка: `.cursor/**`, `AGENTS.md`, `README.md` витрины. Больше ничего | модуль git в проектах 1С |

Ветки **не сливаются**: деревья разные. `main` обновляется только публикацией. `push --force` по `main` запрещён.

## Публикация: «опубликуй»

В чате репозитория kit — `/opsx:publish` или просто «опубликуй». Скилл проверяет, что это репозиторий kit, показывает состав поставки, ждёт подтверждения и обновляет `main` одним коммитом.

Вручную то же самое: `pwsh tools/publish-dist.ps1 -DryRun`, затем без `-DryRun`. На Linux/macOS — `tools/publish-dist.sh`.

Состав поставки (allow-list, SSOT — спека `kit-distribution` в `openspec/specs/` репозитория kit):

| Что | Откуда |
|-----|--------|
| `.cursor/**` | `.cursor/` ветки `develop` |
| `AGENTS.md` | корень `develop` |
| `README.md` | шаблон `tools/dist-readme.md` + дата и исходный коммит |

Не публикуется: `openspec/`, `doc/`, `tools/`, `temp/`, `.bsl-language-server.json.example`.

## Самодостаточность поставки

На `main` нет каталога `openspec/`, поэтому всё, к чему обращаются команды и скиллы, лежит внутри `.cursor/`:

- глоссарий — `.cursor/docs/glossary.md`;
- заготовки для целевого проекта — `.cursor/templates/seed/` (таксономия базы знаний, шаблон каталога ЗНИ);
- `openspec/project.md`, `openspec/specs/architecture.md`, `openspec/config.yaml` — создаёт `/init-project` **в проекте**, в kit их нет по дизайну.

Новая ссылка из `.cursor/**` на путь вне `.cursor/` — дефект поставки (кроме файлов, которые создаёт `/init-project`). Проверка — [delivery-integrity.md](./delivery-integrity.md).

## Эволюция kit (метапроект)

Это правило **репозитория шаблона kit**, не цикл ЗНИ в проекте 1С. В конфигурации заказчика ветки `develop`/`main` kit не заводить.

1. Правки kit — на `develop` (короткую фича-ветку сразу сливать в `develop`).
2. ЗНИ эволюции и их архивы живут в `openspec/changes/` на `develop` и в поставку не попадают.
3. Приёмка срезов эволюции — в **sandbox**: поставка с `develop` (или с фича-ветки) → Reload Window → учебный сценарий из Primary среза.
4. Публикация — после мержа в `develop`, командой (см. выше). Тег `vX.Y.Z` ставится на коммит `main`, не `develop`.

## Forms / MXL

Режим поставки **управляемой формы** в прикладной ЗНИ задаётся Mode Gate на этапе design `/opsx:new` — per-form `form_mode` / map `forms:` (см. `.cursor/rules/forms-mxl-mode-gate.mdc`). Макет (Template/MXL) в new не спрашивается; default на apply — вручную, non-manual только с разрешением. В метапроекте эволюции kit: `form_mode: n/a`.

## Связь

- Установка в проект: [kit-as-submodule.md](./kit-as-submodule.md)
- Обзор / памятка: `README.md` (в корне репо kit; в рабочий проект 1С не копируется)
- Индекс команд и SSOT: `AGENTS.md`
- Mode Gate: `.cursor/rules/forms-mxl-mode-gate.mdc`
- Целостность поставки (перед version-cut): [delivery-integrity.md](./delivery-integrity.md)
- Quick start / FAQ: [quick-start.md](./quick-start.md), [faq-kit.md](./faq-kit.md)
