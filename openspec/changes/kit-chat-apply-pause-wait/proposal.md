## Why

Пауза `/opsx:apply` на ручном Конфигураторе сжималась правилом «тонкий чат» в статус «0 из N» и ссылку на файл. Разработчик не видел, где он и что создать, хотя рецепт уже лежал в `handoff-pause-*.md`. Человеческий слой §2.5–2.6 требовал самодостаточного чата; лимит 4–8 строк и шаблон «прогресс + ничего в коде» его перебивали.

Источник: прогон на PavDO `do2-pavlik-knopki-file-actions` (2026-08-17).

## Metadata (comment markers)

developer: n/a
comment_suffix:
marker_style: minimal

Маркеры не применяются: kit-метапроект, изменения только в `.cursor/**` и `openspec/specs`, кода 1С в scope нет.

## Forms mode

form_mode: n/a

## What Changes

1. Пауза apply делится на **pause-wait** (человек создаёт объекты / выгружает) и **pause-decision** (выбор A/B).
2. В чате pause-wait — карточка-навигатор: где мы, нумерованный список «что создать», ловушки записи, якорь **имени раздела** файла, как вернуться.
3. В файле паузы первым идёт раздел «Что создать в Конфигураторе»; дамп отсутствующих XML — приложение.
4. Тест понятности покрывает не только выбор A/B, но и «можно начать работу, не открывая файл, чтобы узнать задачу».
5. Сценарий изолированного чата E4 фиксирует приёмку стиля.

## Capabilities

### Modified Capabilities

- `chat-surface-clarity`: пауза apply на Конфигураторе — инвентарь в чате, рецепт в названном разделе файла; не ссылка без списка; не развилка A/B вместо списка.

## Impact

- Зона: `.cursor/rules/chat-output-budget.mdc` (+ full), `.cursor/docs/opsx-output-style.md`, `.cursor/skills/openspec-apply-change/`, `1c-no-metadata-creation.mdc`, `1c-xml-write-guard.mdc`, `ux-acceptance-isolated-chat.md`.
- Не трогать: verify/explore шаблоны оптом; `acceptance`-handoff кроме того, что pause больше не занимает его слот «тонкий чат на всё».
