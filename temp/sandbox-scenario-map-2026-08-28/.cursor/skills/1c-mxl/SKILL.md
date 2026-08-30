---
name: 1c-mxl
description: Complete toolkit for 1C spreadsheet templates (MXL) - compile from JSON DSL, decompile to JSON, analyze structure, validate. Use when working with print forms and tabular documents.
---

# 1C MXL - Spreadsheet Templates Toolkit

Полный набор инструментов для работы с макетами табличных документов 1С (Template.xml). Поддержка JSON DSL для быстрого создания печатных форм.

**Политика макета:** `.cursor/rules/forms-mxl-mode-gate.mdc` § Политика макетов. Mode Gate `/opsx:new` **не** спрашивает способ поставки макета. Default — **manual**. Non-manual — только с разрешением на apply.

## Политика поставки Template/MXL

| Режим | Template.xml | Действие |
|-------|--------------|----------|
| **manual** (default) | Не compile агентом | Инструкция / WAIT; правки в Конфигураторе + выгрузка |
| **assisted** (только с разрешением apply) | Через skill | `1c-mxl/compile` → `validate`; **без** сырого Write Template.xml |
| код заполнения без XML | Не менять | Код заполнения макета без правки Template.xml — без Mode-вопроса |

Compile Form.xml: см. `1c-forms` + per-form `form_mode`. Запрет form-add / ChildObjects / `-FromObject` — в SKILL compile/edit и halt-triggers.

**Разрешение non-manual (apply):** маркер `[mxl:assisted]` / явная запись в tasks **или** утвердительный ответ / AskQuestion в чате apply; факт — в `debug.md` § `## Apply permissions`. Без разрешения — только manual (WAIT). Не resurrect Mode Gate макета в `/opsx:new`.

## Quick Start

### Создать макет из JSON (только `assisted`)
```bash
# 1. Создать JSON описание макета
# 2. Скомпилировать в Template.xml
1c-mxl compile template-design.json Documents/ЗаказКлиента/Templates/ПечатнаяФорма/Ext/Template.xml
# 3. Валидировать
1c-mxl validate Documents/ЗаказКлиента/Templates/ПечатнаяФорма/Ext/Template.xml
```

### Декомпилировать существующий макет
```bash
# Преобразовать Template.xml в компактный JSON
1c-mxl decompile Documents/ЗаказКлиента/Templates/ПечатнаяФорма/Ext/Template.xml template.json
```

## Включенные Skills

### 1. compile - Компиляция из JSON DSL
**Путь**: `1c-mxl/compile/SKILL.md`
- Компилирует JSON (20-30 строк) в Template.xml (200-500+ строк)
- Автоматически создает области, параметры, колонки
- Поддержка всех типов ячеек (Text, Number, Date, Picture)
- На apply: только при записанном разрешении non-manual (`[mxl:assisted]` / Apply permissions)

### 2. decompile - Декомпиляция в JSON DSL
**Путь**: `1c-mxl/decompile/SKILL.md`
- Обратная операция к compile
- Извлекает структуру в компактный JSON
- Сохраняет форматирование и параметры

### 3. info - Анализ структуры
**Путь**: `1c-mxl/info/SKILL.md`
- Выводит именованные области
- Показывает параметры
- Перечисляет наборы колонок

### 4. validate - Валидация
**Путь**: `1c-mxl/validate/SKILL.md`
- Проверяет структурные ошибки
- Валидирует ссылки на области
- Проверяет параметры

## Workflow

```yaml
Создание печатной формы (non-manual, только с разрешением apply):
  1. Разрешение apply зафиксировано (чат / [mxl:assisted] / debug § Apply permissions)
  2. Спроектировать структуру (JSON DSL)
  3. Скомпилировать: 1c-mxl compile
  4. Валидировать: 1c-mxl validate
  5. Интегрировать в конфигурацию

manual (default, без Mode-вопроса в new):
  1. Инструкция Конфигуратор + выгрузка (WAIT)
  2. Без compile оркестратором
```

