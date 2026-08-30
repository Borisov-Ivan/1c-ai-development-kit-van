# Маркеры ЗНИ — четыре слоя (обзор без скриптов)

Единое поле смысла: **`domain_label`** (= `comment_suffix` в `proposal.md`).

**SSOT механики и baseline:** [marker-canon.md](marker-canon.md) (kit).  
**SSOT значений проекта:** [openspec/project.md](../../openspec/project.md) (`defaultDeveloper`, `cfMarkerPrefix`, строки Whitelist).

## Четыре слоя

| Слой | Где | Что содержит |
|------|-----|--------------|
| **1. Metadata** | `openspec/changes/<name>/proposal.md` → `## Metadata (comment markers)` | `developer`, `comment_suffix` (domain_label), `marker_style` (`canonical` \| `minimal`) |
| **2. SSOT values** | `openspec/project.md` | `defaultDeveloper`, `cfMarkerPrefix`, строки Whitelist / Обязательный контроль, project-расширения списков |
| **2b. SSOT mechanism** | `.cursor/docs/marker-canon.md` | грамматика маркера, MARKER-MERGE-001, MARKER-PLACEMENT-001, baseline запреты domain_label, дефолтный FORMAT |
| **3. Transport** | Вычисляется в `/opsx:apply` | `open_marker` / `close_marker` (cfe или cf по scope задач) → writer §3a |
| **4. BSL + гигиена** | `src/**/*.bsl` | Фактические строки `// +++ …`, `// --- …`, `{cfMarkerPrefix} …`; AP-040 / AP-044 / AP-045 / AP-051 / AP-053 / AP-054 |

```text
Metadata (proposal) → values (project.md) + mechanism (marker-canon) → Transport (apply) → BSL (src) → Review (AP-*)
```

## Как посмотреть по change

**Команда:** `/opsx:status <name>` — блок **«Маркеры»**: developer, comment_suffix, marker_style, флаг process-only, preview open/close.

**Вручную:** открыть `openspec/changes/<name>/proposal.md`, секция `## Metadata (comment markers)`.

**Metadata Gate (`/opsx:new`):** согласует слой 1 — только `comment_suffix` (описание); ФИО из `defaultDeveloper` в project.md или отдельный текстовый шаг; preview с датой — иллюстрация transport, SSOT metadata — proposal. Полный scope-specific preview — в status/apply после tasks.

## Как посмотреть SSOT

**Kit (механика, baseline):** Read [marker-canon.md](marker-canon.md) — CRC, MERGE-001, PLACEMENT-001, baseline запреты domain_label, дефолтный формат `+++`/`---`.

**Project (значения):** Read [openspec/project.md](../../openspec/project.md):

- `#### Разработчик по умолчанию` — `defaultDeveloper`, `cfMarkerPrefix`
- `#### Whitelist предрелиза` — scope glob и regex/prefix (project overlay распознавания)
- опционально: расширения allow-list AP-054, дополнительные запреты/допуски domain_label

Навигация по таблицам: [bsl-comment-formats-project.md](bsl-comment-formats-project.md).

## Как посмотреть BSL (слой 4)

Поиск в IDE / ripgrep по scope из таблицы Whitelist в project.md (glob на строку таблицы).

Дефолтный kit-формат cfe: `// +++`, `// ---`. Cf: значение `cfMarkerPrefix` из project.md.

## Гигиена (семейство Comment Hygiene: AP-040 / AP-044 / AP-045 / AP-051 / AP-053 / AP-054)

| Правило | Смысл для whitelist-маркеров |
|---------|------------------------------|
| **AP-040** | Whitelist exempt — **не удалять** пару; process-метки вне whitelist — удалить |
| **AP-044** | Комментарий не пересказывает оператор снизу |
| **AP-045** | Без даты+времени без обоснования |
| **AP-051** | MARKER-MERGE-001 — сжимать смежные пары |
| **AP-053** | Содержимое domain_label осмысленное; baseline запреты — `marker-canon.md`; remediation — **переписать**, не delete |
| **AP-054** | **Текст** комментария/JSDoc и **тело** блоков `+++`/`---` — на русском; SSOT allow-list — карточка AP-054 + `marker-canon.md` |
| **MARKER-PLACEMENT-001** | Inline-close с `КонецПроцедуры`/`КонецФункции`; SSOT — `marker-canon.md` |

Change-scoped: `/review` с metadata из proposal. Полный scope: `/release-review`.

Каталог: [bsl-antipatterns.md](antipatterns/bsl-antipatterns.md), индекс — `.cursor/rules/bsl-antipatterns.mdc`.

## Whitelist vs содержимое (кратко)

> Whitelist защищает **пару от удаления** (AP-040) и задаёт **распознавание** формата (AP-051).  
> **Текст** открывающих и однострочных whitelist-строк (`domain_label`) проверяет **AP-053** (baseline — `marker-canon.md`).  
> **Язык** текста комментария, шапки JSDoc и тела блока `+++`/`---` проверяет **AP-054** — whitelist от этого не освобождает.
