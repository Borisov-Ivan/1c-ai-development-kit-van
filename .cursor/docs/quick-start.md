# Quick start — kit-van

Минимальный маршрут после копирования `.cursor` + `AGENTS.md` в проект 1С.

Обзор фреймворка и типовых сценариев: корневой [`README.md`](../../README.md).

## 1. Поставка

Скопируйте в корень проекта:

- каталог `.cursor/`
- файл `AGENTS.md`

Reload Window в Cursor. Папку `openspec/changes/` из шаблонного репо **не** копируйте как обязательную поставку (см. [kit-template-workflow.md](./kit-template-workflow.md)).

## 2. Первый сценарий

Единый вход разбора — `/opsx:explore` (в т.ч. сырой текст заказчика и дефект). Подробнее — [`README.md`](../../README.md).

| Задача | Команда |
|--------|---------|
| Разобрать дефект / вопрос / сырой запрос / идею | `/opsx:explore` |
| Создать ЗНИ | `/opsx:new <slug>` |
| Проверить постановку | `/opsx:verify <slug>` |
| Реализовать | `/opsx:apply <slug>` |
| Сохранить сессию и уйти | `/session-save` → в новом чате `/session-restore` |
| Ретроспектива сессии | `/session-retro` |

## 3. Формы и макеты

На ЗНИ с **управляемой формой** `/opsx:new` спросит по-русски: **вручную** / **автоматически** (правки Form.xml в репозитории) / **программно**. Пустой ответ → вручную (`form_mode: manual`). Макет на new **не** спрашивается. Подробнее: `.cursor/rules/forms-mxl-mode-gate.mdc`. FAQ: [faq-kit.md](./faq-kit.md).

## 4. Каталог skills (частое)

| Skill | Зачем |
|-------|-------|
| `1c-forms` | info / validate / patterns; правка Form.xml — при режиме «автоматически» (`assisted`) |
| `1c-mxl` | макеты на apply (по разрешению); не вопрос Mode на new |
| `1c-agent-patterns` | шаблоны промптов агентов |
| `session-save` / `restore` / `retro` | непрерывность чата и ретро; **не** авто-apply |
| Кейсбуки | `.cursor/docs/casebooks/` |

Полный индекс workflow — в корневом `AGENTS.md`.
