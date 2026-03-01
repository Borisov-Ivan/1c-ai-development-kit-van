---
name: 1c-forms
description: Complete toolkit for 1C managed forms - create, edit, analyze, validate, compile from JSON DSL. Integrates with MCP user-1c-forms-* tools. Use when working with any 1C managed forms (DataProcessor, Document, Catalog, Register, etc).
---

# 1C Forms - Complete Toolkit

Полный набор инструментов для работы с управляемыми формами 1С. Объединяет практические skills с MCP инструментами для максимальной эффективности.

Платформенный референс по формам: `.cursor/docs/platform/Глава 7. Формы.md` (Grep+Read, не читать целиком).

---

## Quick Start

### Создать новую форму
```bash
# 1. Создать структуру формы
1c-forms scaffold add Documents/ЗаказКлиента.xml ФормаДокумента Object "Форма заказа"

# 2. Спроектировать форму (JSON DSL)
# Создать form-design.json с описанием элементов

# 3. Скомпилировать Form.xml
1c-forms compile form-design.json Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml

# 4. Валидировать
1c-forms validate Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml
```

### Редактировать существующую форму
```bash
# 1. Проанализировать структуру
1c-forms info Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml

# 2. Добавить элементы
1c-forms edit Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml --add-input "Комментарий" --add-button "Печать"

# 3. Валидировать изменения
1c-forms validate Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml
```

---

## 📦 Включенные Skills

### 1. scaffold - Создание/удаление форм
**Файл**: `1c-forms/scaffold/SKILL.md`

**Что делает**:
- Создает структуру формы (metadata XML + Form.xml + Module.bsl)
- Регистрирует форму в метаданных объекта
- Удаляет формы с очисткой метаданных
- Поддерживает все типы объектов (Document, Catalog, DataProcessor, Register, etc)

**Когда использовать**:
- Добавление новой формы к объекту
- Удаление существующей формы
- Создание форм для EPF/ERF

**MCP интеграция**: Использует `user-1c-forms-get_xsd_schema` для валидации структуры

### 2. compile - Генерация Form.xml из JSON DSL
**Файл**: `1c-forms/compile/SKILL.md`

**Что делает**:
- Компилирует компактный JSON (20-50 строк) в полный Form.xml (100-500+ строк)
- Автоматически генерирует companion элементы
- Присваивает последовательные ID
- Добавляет корректные namespace

**Когда использовать**:
- Проектирование формы с нуля
- Быстрое создание типовых форм
- Генерация форм по шаблону

**MCP интеграция**: 
- Использует `user-1c-forms-get_json_schema` для валидации JSON
- Использует `user-1c-forms-get_xsd_schema` для валидации результата

### 3. edit - Редактирование существующих форм
**Файл**: `1c-forms/edit/SKILL.md`

**Что делает**:
- Добавляет элементы в существующий Form.xml
- Добавляет реквизиты с правильными типами
- Добавляет команды с обработчиками
- Автоматически выделяет свободные ID

**Когда использовать**:
- Добавление полей в форму
- Добавление кнопок и команд
- Расширение существующей формы

**MCP интеграция**: Использует `user-1c-forms-get_xsd_schema` для валидации

### 4. info - Анализ структуры формы
**Файл**: `1c-forms/info/SKILL.md`

**Что делает**:
- Читает Form.xml и выводит компактную сводку
- Показывает дерево элементов с типами
- Перечисляет реквизиты с типами данных
- Показывает команды и события

**Когда использовать**:
- Изучение незнакомой формы
- Поиск элементов и реквизитов
- Документирование структуры формы

**MCP интеграция**: Нет (чтение XML)

### 5. validate - Валидация Form.xml
**Файл**: `1c-forms/validate/SKILL.md`

**Что делает**:
- Проверяет структурные ошибки Form.xml
- Проверяет уникальность ID
- Проверяет наличие companion элементов
- Проверяет корректность ссылок DataPath и команд

**Когда использовать**:
- После создания/редактирования формы
- Перед коммитом изменений
- При отладке проблем с формой

**MCP интеграция**: Использует `user-1c-forms-get_xsd_schema` для валидации

### 6. patterns - Паттерны проектирования форм
**Файл**: `1c-forms/patterns/SKILL.md`

**Что делает**:
- Справочник архетипов форм (Object, List, Choice, Record)
- Соглашения именования элементов
- Продвинутые паттерны (master-detail, wizard, search)
- Best practices для форм

**Когда использовать**:
- Проектирование формы с нуля (5+ элементов)
- Выбор правильного архетипа
- Изучение best practices

**MCP интеграция**: Использует `user-1c-forms-get_instructions` для интеграции

---

## 🔄 Workflow: Создание формы с нуля

### Шаг 1: Планирование (используй patterns)
```
Загрузи: 1c-forms/patterns/SKILL.md

Определи:
- Архетип формы (Object, List, Choice, Record)
- Основные элементы (поля, таблицы, кнопки)
- События и обработчики
```

### Шаг 2: Создание структуры (используй scaffold)
```bash
Загрузи: 1c-forms/scaffold/SKILL.md

Выполни:
powershell -NoProfile -File .cursor/skills/1c-forms/scaffold/scripts/form-add.ps1 `
  -ObjectPath "Documents/ЗаказКлиента.xml" `
  -FormName "ФормаДокумента" `
  -Purpose "Object" `
  -Synonym "Форма заказа клиента" `
  -SetDefault
```

### Шаг 3: Проектирование (создай JSON DSL)
```json
{
  "title": "Заказ клиента",
  "properties": {
    "autoTitle": false,
    "commandBarLocation": "Top"
  },
  "events": {
    "OnCreateAtServer": "ПриСозданииНаСервере"
  },
  "elements": [
    {
      "group": "vertical",
      "name": "ГруппаШапка",
      "title": "Шапка документа",
      "elements": [
        { "input": "Дата", "title": "Дата" },
        { "input": "Контрагент", "title": "Контрагент" },
        { "input": "Сумма", "title": "Сумма", "readOnly": true }
      ]
    },
    {
      "table": "Товары",
      "title": "Товары",
      "on": ["OnStartEdit", "OnEditEnd"]
    },
    {
      "group": "horizontal",
      "name": "ГруппаКоманды",
      "elements": [
        { "button": "Провести", "title": "Провести" },
        { "button": "Печать", "title": "Печать" }
      ]
    }
  ],
  "attributes": [
    { "name": "Дата", "type": "Date" },
    { "name": "Контрагент", "type": "CatalogRef.Контрагенты" },
    { "name": "Сумма", "type": "Number", "precision": 15, "scale": 2 }
  ],
  "commands": [
    { "name": "Провести", "action": "ПровестиДокумент" },
    { "name": "Печать", "action": "НапечататьДокумент" }
  ]
}
```

### Шаг 4: Компиляция (используй compile)
```bash
Загрузи: 1c-forms/compile/SKILL.md

Выполни:
powershell -NoProfile -File .cursor/skills/1c-forms/compile/scripts/form-compile.ps1 `
  -JsonPath "form-design.json" `
  -OutputPath "Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml"
```

### Шаг 5: Валидация (используй validate)
```bash
Загрузи: 1c-forms/validate/SKILL.md

Выполни:
powershell -NoProfile -File .cursor/skills/1c-forms/validate/scripts/form-validate.ps1 `
  -FormPath "Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml"
```

### Шаг 6: Доработка (используй edit если нужно)
```bash
Если нужны дополнительные элементы:

Загрузи: 1c-forms/edit/SKILL.md

Выполни:
powershell -NoProfile -File .cursor/skills/1c-forms/edit/scripts/form-edit.ps1 `
  -FormPath "Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml" `
  -AddInput "НовоеПоле" `
  -AddButton "НоваяКоманда"
```

---

## 🔄 Workflow: Редактирование существующей формы

### Шаг 1: Анализ (используй info)
```bash
Загрузи: 1c-forms/info/SKILL.md

Выполни:
powershell -NoProfile -File .cursor/skills/1c-forms/info/scripts/form-info.ps1 `
  -FormPath "Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml"

Изучи:
- Существующие элементы
- Реквизиты и их типы
- Команды и обработчики
- Используемые ID
```

### Шаг 2: Редактирование (используй edit)
```bash
Загрузи: 1c-forms/edit/SKILL.md

Выполни:
powershell -NoProfile -File .cursor/skills/1c-forms/edit/scripts/form-edit.ps1 `
  -FormPath "Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml" `
  -AddInput "Email" `
  -AddButton "ОтправитьEmail"
```

### Шаг 3: Валидация (используй validate)
```bash
Загрузи: 1c-forms/validate/SKILL.md

Выполни:
powershell -NoProfile -File .cursor/skills/1c-forms/validate/scripts/form-validate.ps1 `
  -FormPath "Documents/ЗаказКлиента/Forms/ФормаДокумента/Ext/Form.xml"
```

---

## 🎓 MCP Integration

### Доступные MCP инструменты

1. **user-1c-forms-get_xsd_schema**
   - Получить XSD схему для валидации Form.xml
   - Используется в: scaffold, compile, edit, validate

2. **user-1c-forms-get_json_schema**
   - Получить JSON схему для валидации JSON DSL
   - Используется в: compile

3. **user-1c-forms-get_instructions**
   - Получить инструкции по интеграции форм в метаданные
   - Используется в: scaffold, patterns

### Когда вызывать MCP

```yaml
Перед созданием формы:
  - get_xsd_schema: Получить актуальную схему
  - get_instructions: Понять структуру метаданных

Перед компиляцией из JSON:
  - get_json_schema: Валидировать JSON DSL
  - get_xsd_schema: Валидировать результат

После редактирования:
  - get_xsd_schema: Валидировать изменения

При изучении паттернов:
  - get_instructions: Узнать best practices
```

---

## 📋 Чеклист качества формы

### Структура
- [ ] Форма зарегистрирована в метаданных объекта
- [ ] Все файлы созданы (metadata XML, Form.xml, Module.bsl)
- [ ] UUID уникальны и корректны
- [ ] Namespace объявлены правильно

### Элементы
- [ ] Все ID уникальны и последовательны
- [ ] Companion элементы созданы (ExtInfo, ContextMenu, etc)
- [ ] DataPath ссылаются на существующие реквизиты
- [ ] Команды имеют обработчики

### Реквизиты
- [ ] Типы данных корректны
- [ ] MainAttribute установлен для основного реквизита
- [ ] Табличные части имеют правильную структуру

### Модуль
- [ ] 5 регионов присутствуют
- [ ] ПриСозданииНаСервере реализован
- [ ] Обработчики событий созданы
- [ ] Нет синтаксических ошибок (проверить через BSL LSP)

### Валидация
- [ ] XSD валидация пройдена
- [ ] Структурные проверки пройдены
- [ ] Нет предупреждений от validate

---

## Интеграция с OpenSpec apply

Когда в tasks.md есть задача "Создать форму":

```yaml
1. Загрузить: 1c-forms/patterns/SKILL.md
   - Выбрать архетип
   - Определить структуру

2. Загрузить: 1c-forms/scaffold/SKILL.md
   - Создать структуру формы

3. Создать JSON DSL с описанием формы

4. Загрузить: 1c-forms/compile/SKILL.md
   - Скомпилировать Form.xml

5. Загрузить: 1c-forms/validate/SKILL.md
   - Валидировать результат

6. Если нужны доработки:
   - Загрузить: 1c-forms/edit/SKILL.md
   - Добавить элементы

7. Финальная валидация
```

---

## 📚 Дополнительные ресурсы

### Документация
- XSD схема: `user-1c-forms-get_xsd_schema`
- JSON схема: `user-1c-forms-get_json_schema`
- Инструкции: `user-1c-forms-get_instructions`

### Примеры и структура
- Примеры JSON DSL и архетипы форм см. в подскиллах `1c-forms/compile/SKILL.md` и `1c-forms/patterns/SKILL.md`.
- Формат Form.xml и JSON DSL описан в этих же SKILL и в `.cursor/docs/platform/Глава 7. Формы.md`.

---

## ⚠️ Критические правила

1. **Всегда используй MCP перед созданием/редактированием**
   - get_xsd_schema для валидации
   - get_json_schema для JSON DSL
   - get_instructions для интеграции

2. **Валидируй после каждого изменения**
   - Используй validate skill
   - Проверяй через BSL LSP

3. **Следуй архетипам**
   - Загружай patterns для сложных форм (5+ элементов)
   - Используй правильный Purpose

4. **Сохраняй JSON DSL**
   - Храни JSON описание формы в репозитории
   - Используй для документации и регенерации

5. **Не редактируй Form.xml вручную**
   - Используй edit skill для изменений
   - Или регенерируй через compile

6. **Проверяй интеграцию с метаданными**
   - Форма зарегистрирована в объекте
   - DefaultForm установлен корректно

---

## 🎯 Быстрые команды

```bash
# Создать форму
1c-forms scaffold add <ObjectPath> <FormName> [Purpose] [Synonym]

# Скомпилировать из JSON
1c-forms compile <JsonPath> <OutputPath>

# Добавить элементы
1c-forms edit <FormPath> --add-input <Name> --add-button <Name>

# Проанализировать
1c-forms info <FormPath>

# Валидировать
1c-forms validate <FormPath>

# Изучить паттерны
1c-forms patterns [archetype]
```

---

**Last updated**: 2026-02-11  
**Version**: 1.0  
**Source**: Творческое объединение cursor_rules_1c + наши MCP интеграции
