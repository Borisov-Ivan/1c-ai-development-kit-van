# Framework overlay — управляемые секции project.md

> **Не копировать целиком в project.md.** Этот шаблон — baseline kit для Framework Contract Sync (`/init-project`).  
> SSOT механики: [`.cursor/docs/marker-canon.md`](../docs/marker-canon.md).  
> Текущая версия kit: **`framework_contract_version: 2026-06`**

---

## Шапка project.md (добавить после `# OpenSpec:`)

```markdown
framework_contract_version: 2026-06
```

При sync init-project сравнивает это поле с версией kit и предлагает merge только управляемых секций ниже.

---

## Соглашения → Разработчик по умолчанию (VALUE — заполнить в интервью)

```markdown
#### Разработчик по умолчанию

- **defaultDeveloper:** <Фамилия И.О.> — ФИО в маркерах cfe (`// +++ …`).
- **cfMarkerPrefix:** `<ФамилияИО>:` — префикс whitelist cf (без пробелов в инициалах, с двоеточием).

См. `.cursor/docs/marker-canon.md` — дефолтный FORMAT и MECHANISM; `.cursor/docs/marker-layers-guide.md` — обзор слоёв.
```

---

## Форматы и соглашения по комментариям BSL (overlay — строки таблиц)

**Не дублировать** § Канон domain_label, MARKER-MERGE-001, MARKER-PLACEMENT-001 — они в `marker-canon.md`.

```markdown
## Форматы и соглашения по комментариям BSL

**Baseline (kit):** `.cursor/docs/marker-canon.md` — грамматика, MERGE-001, PLACEMENT-001, baseline запреты domain_label, дефолтный FORMAT `+++`/`---`.

**Project overlay:** таблицы ниже — только распознавание (Whitelist) и mandatory control; опционально — расширения allow-list AP-054.

### Whitelist предрелиза

| Имя формата | Пример | Префикс после `//` | Regex | Scope (glob) | Назначение |
|-------------|--------|---------------------|-------|--------------|------------|
| <из Block 7 init-project> | ... | ... | ... | ... | ... |

### Обязательный контроль (соблюдение формата)

| ID | Где проверять | Требование | Regex | Уровень | kind |
|----|---------------|------------|-------|---------|------|
| <из Block 7 init-project> | ... | ... | ... | ... | ... |

### Расширения allow-list AP-054 (опционально)

| Термин | Обоснование |
|--------|-------------|
| | |

Проект **расширяет** kit baseline, **не сокращает** (CRC § LIST).
```

---

## Что НЕ входит в overlay (остаётся продуктовым текстом)

- `# OpenSpec:` описание, ## Продукт, ## Назначение, ## Область, ## Внешние зависимости
- ## Структура репозитория (пути cf/cfe)
- Принципы, ключевые возможности, доменные термины

Framework Contract Sync **не перезаписывает** эти секции.
