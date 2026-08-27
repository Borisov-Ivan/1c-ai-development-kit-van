# kit-van

Набор правил и команд Cursor для разработки 1С: сначала понятная постановка, потом проверка, потом код и приёмка.

**Заявка на изменение (ЗНИ)** — папка с постановкой и задачами по одной доработке. Её заводят командой, а не «на глаз» в чате.

Этот файл описывает **репозиторий kit**. В проект 1С его не копируют. Сценарии работы в проекте — [`.cursor/docs/quick-start.md`](.cursor/docs/quick-start.md).

## Что копировать в проект 1С

- каталог `.cursor/`
- файл `AGENTS.md`

Затем в Cursor — Reload Window. Внешние среды вроде npm для обычной работы не нужны. Каталог `openspec/` из этого репозитория **не** копируют: в проекте 1С его создаёт `/init-project`.

В чате ассистент ведёт по шагам и командам. Модули `.bsl` пишет специализированный агент. Разметку формы агент сам «сырым» XML-файлом не правит: либо вы правите в Конфигураторе по инструкции, либо явно выбираете режим со скриптом.

## Как устроен репозиторий

| Путь | Зачем | Едет в проект 1С |
|------|--------|------------------|
| `.cursor/` | команды, правила, навыки, документы, заготовки | да |
| `AGENTS.md` | навигационный индекс | да |
| `README.md` | устройство этого репозитория | нет |
| `openspec/specs/`, `openspec/adrs/` | требования и решения самого kit | нет |
| `openspec/changes/` и `archive/` | рабочие ЗНИ эволюции kit | нет |
| `tools/` | утилиты разработки kit (парсер трасс) | нет |
| `.cursor/templates/seed/` | заготовки, которые `/init-project` копирует уже **в проекте** | да (внутри `.cursor/`) |

## Ветки

| Ветка | Роль |
|-------|------|
| `develop` | разработка kit: правила, навыки, открытые ЗНИ, архивы, `tools/` |
| `main` | чистая поставка: то же содержимое `.cursor/` и `AGENTS.md`, плюс specs/ADR kit; без архивов ЗНИ и без `tools/` |

Правило: на `main` содержательные правки не делают. Сначала `develop`, потом публикация (слияние + снятие архивов). Короткую фича-ветку сразу сливают в `develop`, не оставляют домом архива.

```text
правка на develop → слияние в main → снять archive/ и tools/ → push main
                              ↓
              клонировать main → скопировать .cursor/ и AGENTS.md в проект
```

## Установка в проект 1С

```text
git clone -b main --depth 1 <url-этого-репозитория> kit-van
скопировать kit-van\.cursor  →  <проект>\.cursor
скопировать kit-van\AGENTS.md →  <проект>\AGENTS.md
в Cursor: Reload Window
```

Дальше — [quick-start](.cursor/docs/quick-start.md): `/init-project` при первом заходе, затем `/opsx:explore`.

## Обновление поставки (из репозитория kit)

1. Все правки уже на `develop`, рабочее дерево чистое.
2. `git checkout main` → `git merge develop`.
3. Удалить с `main`: `openspec/changes/archive/`, рабочие папки `openspec/changes/<имя>` (кроме того, что живёт в `.cursor/templates/seed/`), каталог `tools/`.
4. Коммит «Публикация поставки: снять архивы и утилиты с main» → `git push origin main`.
5. В каждом проекте 1С снова скопировать `.cursor/` и `AGENTS.md` с обновлённого `main`.

Полный рецепт и приёмка срезов эволюции — [`.cursor/docs/kit-template-workflow.md`](.cursor/docs/kit-template-workflow.md). Чеклист перед объявлением версии — [`.cursor/docs/delivery-integrity.md`](.cursor/docs/delivery-integrity.md).

## Документы

- сценарии и команды — [`.cursor/docs/quick-start.md`](.cursor/docs/quick-start.md)
- частые вопросы — [`.cursor/docs/faq-kit.md`](.cursor/docs/faq-kit.md)
- поставка и эволюция kit — [`.cursor/docs/kit-template-workflow.md`](.cursor/docs/kit-template-workflow.md)
- индекс якорей — [`AGENTS.md`](AGENTS.md)
