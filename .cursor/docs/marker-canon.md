# Marker Canon — SSOT механики маркеров ЗНИ (kit)

Единое поле смысла: **`domain_label`** (= `comment_suffix` в `proposal.md`).

**Разделение SSOT:**
- **Этот файл (kit)** — MECHANISM, дефолтный FORMAT, baseline-списки, инварианты MERGE/PLACEMENT, CRC.
- **[openspec/project.md](../../openspec/project.md)** — VALUE (`defaultDeveloper`, `cfMarkerPrefix`, пути) и project overlay (строки Whitelist предрелиза, расширения списков).

Обзор четырёх слоёв: [marker-layers-guide.md](marker-layers-guide.md). Навигация по project-таблицам: [bsl-comment-formats-project.md](bsl-comment-formats-project.md).

---

## Config Resolution Contract (CRC)

```
effective(X) = kit_baseline(X) ⊕ project_overlay(X)

  VALUE     (пути cf/cfe, defaultDeveloper, cfMarkerPrefix) → project; нет дефолта → спросить
  LIST      (allow-list AP-054, запреты domain_label, строки whitelist) → kit ∪ project
  FORMAT    (конкретные токены маркера; marker_style) → kit DEFAULT ⊕ project override
  MECHANISM (грамматика маркера, MERGE-001, PLACEMENT-001, гигиена AP,
             «нет whitelist → строгая гигиена») → только kit; работает НАД объявленным форматом
```

**Правило LIST:** проект **расширяет** baseline kit, **не сокращает**.

**Zero-config:** при отсутствии `openspec/project.md` или пустых overlay-секций потребители работают на kit baseline. Обязательны только VALUE, которые нельзя дефолтить: пути cf/cfe и `defaultDeveloper` (или ФИО из Metadata change).

---

## Грамматика маркера (MECHANISM)

Любой whitelisted-маркер ЗНИ — **open/close-пара** вокруг изменённого фрагмента кода.

**Слоты open-маркера (семантика, не привязка к конкретным токенам):**

| Слот | Смысл |
|------|--------|
| Автор | ФИО разработчика (`developer` из Metadata или `defaultDeveloper` из project.md) |
| Дата | Дата apply (`dd.MM.yyyy`) |
| `domain_label` | Одна фраза по-русски: **что** меняем и **зачем** (доменное пояснение для читателя кода) |
| `[ID#NNNN]` | Опционально; при merge — ключ группировки смежных блоков |

**Close-маркер:** закрывает пару; для конца процедуры/функции — см. MARKER-PLACEMENT-001.

**Исключение Metadata:** `marker_style: minimal` — пустой `comment_suffix` допустим (только автор + дата в transport).

---

## Дефолтный формат (FORMAT — kit DEFAULT)

Kit генерирует маркеры в `/opsx:apply` (transport) и передаёт writer §3a.

### cfe (расширения)

| Роль | Шаблон |
|------|--------|
| open | `// +++ {developer} {date}` или `// +++ {developer} {date} {comment_suffix}` |
| close | `// --- {developer}` |

### cf (базовая конфигурация)

| Роль | Шаблон |
|------|--------|
| open | `// {cfMarkerPrefix} {comment_suffix} +++` |
| close | `// {cfMarkerPrefix без двоеточия} ---` |
| однострочный cf | `// {cfMarkerPrefix} {domain_label}` (без `+++`, для целой процедуры) |

`cfMarkerPrefix` — **VALUE** из project.md (например `ПР_РС_ОбновлениеЕРПУХ_БорисовИГ:`).

### Поверхность override проекта (Вариант A)

Проект **может** переопределить:

| Ручка | Где | Эффект |
|-------|-----|--------|
| `cfMarkerPrefix` | project.md § Разработчик по умолчанию | Значение префикса cf-маркера |
| `marker_style` | proposal.md Metadata | `canonical` (с domain_label) \| `minimal` (без suffix) |
| Regex распознавания | project.md § Whitelist предрелиза | Дополнительные/legacy форматы **exempt от удаления** AP-040 |

Проект **не может** задать произвольную форму **генерации** writer'om (cfe-токены `+++`/`---` фиксированы в transport). Полный **Marker Format Descriptor** — будущее расширение kit.

---

## MARKER-MERGE-001 (MECHANISM)

Whitelisted-маркеры одного изменения не дробят каждый оператор отдельной парой.

**Объединять**, если подряд идут блоки с:
- одним `[ID#NNNN]`, **или**
- одним `domain_label` + `developer` + той же семантикой изменения

→ один внешний open перед фрагментом, один close после. При разных датах — **поздняя**; автор — из последнего open.

**Не объединять:** разные ID/смысл; чужой код или комментарий между блоками; маркеры **вне** whitelist (там AP-040 delete, не merge).

AP-карточка: [bsl-antipatterns.md](antipatterns/bsl-antipatterns.md) § AP-051.

---

## MARKER-PLACEMENT-001 (MECHANISM)

Закрывающий маркер **конца процедуры/функции** — **в одной строке** с `КонецПроцедуры`/`КонецФункции`:

```bsl
КонецПроцедуры // --- {developer}
```

**Не** выносить close на отдельную строку после `КонецПроцедуры`/`КонецФункции`. Причина: при сравнении/объединении в Конфигураторе маркер на отдельной строке отрывается от тела метода.

Inline-close — **валидная** форма; не считать разрывом пары для AP-051.

---

## Канон domain_label — baseline запреты (LIST, kit)

`domain_label` / `comment_suffix` — **русская** фраза о **предметной области**, не о процессе разработки.

### Требования (GOOD)

- Одна фраза «что меняем и зачем» для коллеги без доступа к ЗНИ.
- Осмысленное доменное пояснение в open-маркере и однострочных cf-строках.

### Baseline-запреты process-лексики (без доменного смысла)

Совпадение suffix или основного содержимого маркера → **AP-053** (rewrite, не AP-040 delete):

| Класс | Примеры |
|-------|---------|
| Ревью/процесс | `release-review`, `prerelease-review`, `findings`, `review`, `verify`, `apply`, `archive` |
| Артефакты OpenSpec | `design`, `proposal`, `ЗНИ`, `ADR`, `spec`, `tasks`, `debug`, `reports`, `openspec` |
| Исследование | `exploration`, `root cause`, `trace-analysis`, `RCA`, `architecture` |
| Идентификаторы процесса | kebab-case **имя change** как основное содержимое; `Decision N`, `Design §`, `п. 3.1` (номер задачи) |
| Пустота | нет текста после автора/даты/префикса (кроме `marker_style: minimal`) |

**Project overlay:** project.md может **добавить** доменные или legacy-термины в allow-list domain_label или в Whitelist regex — **не удалять** baseline-запреты kit.

Потребители: `/opsx:new` Metadata Gate, `/opsx:apply` domain_label validation, `/opsx:verify` WARNING `process-only-marker-suffix`, `/opsx:status` флаг process-only, AP-053 в reviewer.

---

## Whitelist и «нет whitelist → строгая гигиена» (MECHANISM)

**Whitelist** (строки в project.md § Whitelist предрелиза): комментарии, matching regex/prefix в scope glob, **exempt от удаления** AP-040..AP-045 — **кроме AP-053** (содержимое domain_label) и **AP-054** (язык текста/JSDoc/тела блока).

**Если секции Whitelist нет или таблица пуста:** строгая гигиена — changelog-маркеры вне kit baseline не exempt; process-метки удаляются (AP-040).

Колонки таблиц Whitelist / Обязательный контроль — [bsl-comment-formats-project.md](bsl-comment-formats-project.md).

---

## Allow-list AP-054 (baseline LIST, kit)

Расширяется project.md (доменные аббревиатуры продукта). SSOT детектирования — карточка AP-054 в [bsl-antipatterns.md](antipatterns/bsl-antipatterns.md).

Встроенный baseline (без project.md):

1. Идентификатор кода в backticks
2. Протоколы/аббревиатуры: HTTP, HTTPS, JSON, XML, XDTO, GUID, UUID, SQL, URL, RLS, TLS, API, RMQ, UI, БСП
3. Имена веб-сервисов/полей внешних систем (std-06 §1)
4. Имена продуктов/компаний (std-02 §1.3)
5. TODO, FIXME

---

## Связь с AP (гигиена)

| AP | Роль |
|----|------|
| AP-040 | Артефакты процесса в `//`; whitelist exempt delete |
| AP-044 | Пересказ оператора |
| AP-045 | Дата+время без обоснования |
| AP-051 | MARKER-MERGE-001 |
| AP-053 | Содержимое domain_label (baseline запреты — этот файл) |
| AP-054 | Язык текста/JSDoc/тела блока; allow-list — § выше |

Индекс: `.cursor/rules/bsl-antipatterns.mdc`.

---

## Версия контракта

`framework_contract_version: 2026-06` — управляемые секции project.md синхронизируются через `/init-project` (Framework Contract Sync). Шаблон overlay: [`.cursor/templates/project-overlay.template.md`](../templates/project-overlay.template.md).
