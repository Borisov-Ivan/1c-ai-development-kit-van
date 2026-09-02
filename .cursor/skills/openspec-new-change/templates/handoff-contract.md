# Handoff Contract — поля блока `## Постановка ЗНИ`

Полный список парсинга для `/opsx:new` (шаг Explore / Session Context Gate).

| Поле | Обязательность | Куда идёт |
|------|----------------|-----------|
| Симптом | да | `## Why` |
| Корневая причина (`[verified]` / `[hypothesis: план]`) | да | `## What Changes` |
| Что менять | да | scope / `## What Changes` |
| Файлы | да | `## Scope` |
| Приёмка | да | `## Acceptance Criteria` / scenarios |
| Связь с архивом (extends / новый / unrelated) | да | `## Decisions` (precedent) |
| Architect / verify (`required` \| `not-required` \| `report: <путь>`) | да | Design Gate |
| Тема маркера | опционально | Metadata Gate (черновик `comment_suffix`; без ФИО и даты) |
| Срезы (черновик) | опционально | подсказка slice decomposition |
| Открытые решения | опционально | `design.md` § Открытые вопросы + карточка решения до apply |

Для legacy-источников — `Architect Gate`, `Ключевые решения`, `Knowledge findings`, `Рекомендации по срезам`.

**Примечание к полю Architect / verify:** путь `report:` до создания ЗНИ может указывать на `temp/reports/…`. После переезда в каталог ЗНИ оркестратор переписывает его на `reports/<файл>` внутри ЗНИ; артефакты не ссылаются на `temp`. Отдельную обязательную строку таблицы (список отчётов) не добавлять.
