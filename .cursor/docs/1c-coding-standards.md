---
description: Стандарты кода 1С/BSL — обязательны при любой работе с кодом 1С
globs: "**/*.bsl"
---

# 1C Coding Standards

Стандарты написания кода на платформе 1С:Предприятие (BSL).

**Приоритет**: 150 (высокий)  
**Применяется**: Всегда при работе с кодом 1С

Полный справочник стандартов (именование, запросы, обработка ошибок, структура модулей, защитные проверки и т.д.) — в вендорских доменных файлах `.cursor/docs/standard/std-NN-<domain>.md`. Индекс: `.cursor/docs/standard/1c-standards-navigator.md`.

Для architect и reviewer: чеклисты — `.cursor/skills/1c-vendor-standards/SKILL.md`; детали — Read соответствующий доменный файл из `.cursor/docs/standard/`. Платформенная документация: `.cursor/docs/platform/Оглавление-1С-документации.md`. Антипаттерны: `.cursor/docs/antipatterns/bsl-antipatterns.md`.

**FIRST ACTION**: При написании или ревью кода 1С обязательно прочитай релевантный доменный файл из `.cursor/docs/standard/` (через navigator) и `.cursor/docs/antipatterns/bsl-antipatterns.md`.

## Release-hygiene и маркеры ЗНИ (rule 17)

Комментарии, попадающие под **Whitelist предрелиза** (baseline `.cursor/docs/marker-canon.md` + строки в [openspec/project.md](../../openspec/project.md), секция «Форматы и соглашения по комментариям BSL») в рамках scope glob, **exempt от удаления** по AP-040..AP-045 — **кроме AP-053** (содержимое `domain_label` в whitelist-строках: rewrite, не delete). При отсутствии project whitelist — строгая гигиена (marker-canon). Навигация: [.cursor/docs/bsl-comment-formats-project.md](bsl-comment-formats-project.md), [.cursor/docs/marker-layers-guide.md](marker-layers-guide.md), [.cursor/docs/marker-canon.md](marker-canon.md).

### Семейство Comment Hygiene и язык комментариев (AP-054)

Гигиена комментариев `//` (включая JSDoc) — семейство **AP-040** (артефакты процесса), **AP-044** (пересказ оператора), **AP-045** (дата+время), **AP-051** (сжатие смежных маркеров), **AP-053** (содержимое open-маркера `domain_label`), **AP-054** (англицизм/непрозрачный термин в тексте).

**Язык (AP-054):** код и комментарии — экспортный артефакт для непосвящённого читателя; текст комментариев, шапок JSDoc и тело блоков `// +++`/`// ---` — на **русском доменном языке** (std-06 §1, §7.1). Механизм — детектор латиницы в прозе, **не** словарь стоп-слов; allow-list (backtick-идентификатор, протокол/аббревиатура, имя веб-сервиса/продукта, `TODO`/`FIXME`) полон по построению. Whitelist защищает пару маркеров от удаления, но **не** освобождает текст внутри блока от требования русского языка.

**SSOT правила AP-054** — карточка в [.cursor/docs/antipatterns/bsl-antipatterns.md](antipatterns/bsl-antipatterns.md) (не `project.md`). `openspec/project.md` лишь **опционально расширяет** allow-list доменными аббревиатурами проекта.