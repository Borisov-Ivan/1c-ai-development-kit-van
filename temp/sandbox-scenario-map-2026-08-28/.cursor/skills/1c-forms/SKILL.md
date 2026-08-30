---
name: 1c-forms
description: "Управляемые формы 1С — анализ/валидация выгрузки (info, validate), паттерны; compile/edit Form.xml — только при form_mode assisted (или legacy artifact_mode) и наличии skill (иначе HALT→manual / Конфигуратор / BSL модуля формы)."
---

# 1C Forms — анализ, валидация, режимы поставки

Платформенный референс: `.cursor/docs/platform/Глава 7. Формы.md` (Grep+Read, не целиком).  
Mode Gate: `.cursor/rules/forms-mxl-mode-gate.mdc`.

## Режимы (`form_mode` из proposal; per-form)

Источник: секция `## Forms mode` — скаляр `form_mode:` или map `forms:` (ключ метаданных → mode). Fallback: lone legacy `artifact_mode` → одинаковый режим на весь текущий form-scope.

| Режим | Form.xml | Что делать |
|-------|----------|------------|
| **manual** (default) | Не писать агентом | Инструкция Конфигуратор → выгрузка **или** программные элементы в `Module.bsl` |
| **assisted** | Только через skill | `1c-forms/compile` и/или `edit` при наличии skill; нет skill → HALT → manual |
| **bsl-only** | Не менять | UX только в модуле формы (BSL) |
| **n/a** | — | ЗНИ без форм / метапроект; при задаче на форму без режима — STOP/extend |

Сырой Write/StrReplace Form.xml оркестратором **запрещён** всегда (`1c-xml-write-guard.mdc`).

---

## Подскиллы

| Подскилл | Назначение | Статус |
|----------|------------|--------|
| **`1c-forms/info`** | Сводка по существующему `Form.xml` | Есть |
| **`1c-forms/validate`** | Структурная проверка `Form.xml` | Есть |
| **`1c-forms/patterns`** | Архетипы и соглашения UI (без генерации XML) | Есть |
| **`1c-forms/compile`** | Сборка Form.xml из DSL при `assisted` | Есть (только `-JsonPath`; без `-FromObject` / form-add) |
| **`1c-forms/edit`** | Правка существующего Form.xml при `assisted` | Есть |

Команды: `compile/SKILL.md`, `edit/SKILL.md`, `info/SKILL.md`, `validate/SKILL.md`.

**Запрещено в skills:** form-add, template-add, мутация ChildObjects объекта, `-FromObject`, borrow.

---

## MCP (опционально)

- **`user-1c-forms-get_xsd_schema`** — XSD для ориентира при разборе/валидации.
- **`user-1c-forms-get_instructions`** — интеграция форм в метаданные (справочно).

Не использовать MCP/JSON-схему как обход Mode Gate или сырой генератор Form.xml.

---

## OpenSpec / apply

1. Прочитать режим **этой** формы: `form_mode` / map `forms:` (+ fallback lone `artifact_mode`) — Mode Gate.
2. Пустой/`n/a` при задаче на форму без legacy → STOP/extend (не default молча).
3. **manual** — ручное конфигурирование + выгрузка и/или BSL модуля формы.
4. **assisted** — только skill compile/edit; нет skill → предложить manual.
5. **bsl-only** — без задач на правку Form.xml.
6. Заимствование / form-add / ChildObjects — всегда блокер человеку.
