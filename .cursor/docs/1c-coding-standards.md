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

## Доменные кейсбуки (on-demand)

Проектирование блокировок, журнала, регистров, СКД, async и типовых ловушек платформы — **не** вендорский `std-*`. Канон: [`.cursor/docs/casebooks/`](casebooks/README.md) (D2).

| Тема | Файл |
|------|------|
| Блокировки и транзакции | `.cursor/docs/casebooks/locks-and-transactions.md` |
| Журнал регистрации | `.cursor/docs/casebooks/logging-strategy.md` |
| Регистры | `.cursor/docs/casebooks/registers-design.md` |
| СКД (дизайн отчёта) | `.cursor/docs/casebooks/dcs-design.md` |
| Async на клиенте | `.cursor/docs/casebooks/async-methods.md` |
| Ловушки платформы | `.cursor/docs/casebooks/platform-solutions.md` |
| Модуль формы / reserved names | `.cursor/docs/casebooks/form-module-notes.md` |
| XML pitfalls (ручные инструкции) | `.cursor/docs/casebooks/metadata-xml-workarounds.md` |

## Release-hygiene и маркеры ЗНИ (rule 17)

Комментарии, попадающие под **Whitelist предрелиза** (baseline `.cursor/docs/marker-canon.md` + строки в [openspec/project.md](../../openspec/project.md), секция «Форматы и соглашения по комментариям BSL») в рамках scope glob, **exempt от удаления** по AP-040..AP-045 — **кроме AP-053** (содержимое `domain_label` в whitelist-строках: rewrite, не delete). При отсутствии project whitelist — строгая гигиена (marker-canon). Навигация: [.cursor/docs/bsl-comment-formats-project.md](bsl-comment-formats-project.md), [.cursor/docs/marker-layers-guide.md](marker-layers-guide.md), [.cursor/docs/marker-canon.md](marker-canon.md).

### Семейство Comment Hygiene и язык кода (AP-054 комментарии, AP-031 идентификаторы — Export Language)

Гигиена комментариев `//` (включая JSDoc) — семейство **AP-040** (артефакты процесса), **AP-044** (пересказ оператора), **AP-045** (дата+время), **AP-051** (сжатие смежных маркеров), **AP-053** (содержимое open-маркера `domain_label`), **AP-054** (англицизм/непрозрачный термин в тексте).

**Язык (AP-054):** код и комментарии — экспортный артефакт для непосвящённого читателя; текст комментариев, шапок JSDoc и тело блоков `// +++`/`// ---` — на **русском доменном языке** (std-06 §1, §7.1). Механизм — детектор латиницы в прозе, **не** словарь стоп-слов; allow-list (backtick-идентификатор, протокол/аббревиатура, имя веб-сервиса/продукта, `TODO`/`FIXME`) полон по построению. Whitelist защищает пару маркеров от удаления, но **не** освобождает текст внутри блока от требования русского языка.

**Экспортный язык распространяется и на идентификаторы (AP-031).** Требование «русский доменный экспортный язык» относится не только к тексту комментариев (AP-054), но и к **именам** — процедур, функций, переменных, параметров, ключей `ДополнительныеСвойства`, `#Область`. Это одно семейство **Export Language** с единым механизмом: детектор латиницы в имени (вкл. внутри кириллического: `БылиPreMatrixОтмены` → `PreMatrix`) + доменный тест (коллега без ЗНИ объясняет имя одной фразой) при закрытом по построению allow-list. `design.md`/`tasks.md` — источник фактов, **не** имён: терминология постановки не легитимизирует латиницу/непрозрачность в идентификаторе. Латиница из постановки в имени — AP-031, в комментарии — AP-054.

**SSOT правила AP-054** — карточка в [.cursor/docs/antipatterns/bsl-antipatterns.md](antipatterns/bsl-antipatterns.md) (не `project.md`); **SSOT AP-031** — там же. `openspec/project.md` лишь **опционально расширяет** allow-list доменными аббревиатурами проекта.