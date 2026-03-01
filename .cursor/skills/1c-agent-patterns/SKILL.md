---
name: 1c-agent-patterns
description: Reference guide for 1C agent delegation patterns - complexity assessment, prompt templates, specialized skill integration. Use when planning agent delegation for 1C development tasks.
---

# 1C Agent Patterns (справочник)

Паттерны делегирования задач специализированным агентам 1С. Не workflow — справочник для использования в OpenSpec explore/apply.

---

## ОЦЕНКА СЛОЖНОСТИ

| Сложность | Признаки | Агенты |
|-----------|----------|--------|
| **Простая** | 1-2 файла, очевидная реализация, нет архитектурных решений | 1 explorer, 1 writer, 1 reviewer |
| **Средняя** | 3-5 файлов, требует понимания архитектуры, несколько модулей | 1-2 explorer, 1 architect, 1 writer, 1 reviewer |
| **Сложная** | 5+ файлов, несколько подсистем, интеграции | 2-4 explorer (параллельно), 2 architect (мультисэмплинг), writer + reviewer |
| **Критичная** | Архитектурные изменения, высокие риски, много зависимостей | 4+ explorer (итеративно), 2-3 architect, writer + reviewer + architect-ревью |

---

## КОГДА КАКОЙ АГЕНТ

### onec-code-explorer
- Контекст из 3+ модулей
- Понять потоки вызовов и зависимости
- Найти паттерны в существующем коде
- Подготовка к архитектурному решению

### onec-code-architect
- Проектирование плана реализации (design.md)
- Выбор подхода (минимальные изменения / чистая архитектура / баланс)
- Ревью design.md перед реализацией
- Ревью соответствия кода дизайну (для средних/сложных)
- Мультисэмплинг: запустить 2-3 с разными подходами, выбрать лучший

### onec-code-writer
- Реализация задач из tasks.md
- Исправление замечаний reviewer
- Только существующие .bsl файлы

### onec-code-reviewer
- Обязательно после каждого writer
- mode=prerelease при предрелизной проверке
- Категории: performance, security, БСП, аннотации, структура модуля

### onec-trace-analyst
- Файл трассы (PFF/TRACE) или стек ошибки 3+ строк
- Перед вызовом: подготовить бриф (см. openspec-debug/SKILL.md шаг 3.5)

---

## ШАБЛОНЫ ПРОМПТОВ

### Explorer (исследование кода)

```
Task(
  description="Исследовать код [область]",
  prompt="Проанализируй существующий код для [область].
         Найди паттерны, архитектуру, похожие доработки.
         Верни: entry points, потоки выполнения, зависимости, список ключевых файлов.
         
         Контекст задачи: [из proposal/design или описания пользователя]",
  subagent_type="onec-code-explorer",
  model="fast"
)
```

### Architect (проектирование)

```
Task(
  description="Спроектировать [feature]",
  prompt="Спроектируй архитектуру для [feature].
         
         Артефакты: [пути к proposal.md, design.md если есть]
         Результат исследования: [резюме от explorer]
         Подход: [минимальные изменения / чистая архитектура / баланс]
         
         Создай план с этапами реализации (атомарные, с критериями приемки).
         Используй Mermaid диаграммы.",
  subagent_type="onec-code-architect"
)
```

### Architect (ревью плана)

```
Task(
  description="Ревью плана [feature]",
  prompt="Проверь design.md для [feature].
         
         Артефакты: [пути к proposal.md, design.md, tasks.md]
         
         Фокус: полнота, корректность, реалистичность, соответствие требованиям,
         чёткость критериев приемки, правильность зависимостей.
         Все задачи на verified facts? Если на hypotheses — есть ли задача верификации?
         
         Если проблемы — опиши и предложи исправления.",
  subagent_type="onec-code-architect"
)
```

### Writer (реализация задачи)

```
Task(
  description="Реализовать задачу N [feature]",
  prompt="Реализуй задачу N для [feature].
         
         Design: [путь к design.md]
         Задача: [описание и критерии из tasks.md]
         
         Ограничение: только правка существующих .bsl, без новых файлов и метаданных.
         При отсутствии нужного модуля/объекта — СТОП с указанием что добавить.
         Следуй 1c-coding-standards.mdc. Проведи самоконтроль.",
  subagent_type="onec-code-writer",
  model="fast"
)
```

### Reviewer (ревью кода)

```
Task(
  description="Ревью кода [feature]",
  prompt="Проверь качество кода для [feature].
         
         Файлы: [список изменённых .bsl]
         Стандарты: 1c-coding-standards.mdc
         
         Фокус: баги, БСП compliance, производительность, безопасность,
         аннотации расширений, структура модуля, документация методов.",
  subagent_type="onec-code-reviewer",
  model="fast"
)
```

---

## ИНТЕГРАЦИЯ СО СПЕЦИАЛИЗИРОВАННЫМИ СКИЛЛАМИ

При реализации задач из tasks.md определить тип и загрузить скилл:

| Тип задачи | Скилл | Что делает |
|------------|-------|------------|
| Создание формы | `1c-forms/SKILL.md` | scaffold → compile → validate |
| Печатная форма | `1c-mxl/SKILL.md` | compile → validate |
| Настройка прав | `1c-roles/SKILL.md` | compile из JSON DSL |
| Интеграция с БСП | `1c-bsp/SKILL.md` | registration + commands + patterns |
| Расширения (аннотации) | `1c-extensions/SKILL.md` | выбор аннотации, перенос правок |
| Оптимизация запросов | `1c-query-optimization/SKILL.md` | temp tables, JOIN, индексы |
| Общая BSL-задача | onec-code-writer напрямую | |

---

## АВТО-ИСПРАВЛЕНИЕ ЗАМЕЧАНИЙ РЕВЬЮ

При critical/high от reviewer:

1. **Кодовые замечания** (performance, стиль, ошибки, безопасность) → автоматически onec-code-writer с замечаниями → повторный reviewer. Максимум 2 итерации.
2. **Архитектурные замечания** (новый объект, изменение API, структуры хранения, прав/RLS) → СТОП, к пользователю.

---

## DELEGATION GATE (подробности)

### Порядок при BSL-задаче

1. Прочитать артефакты (design, tasks)
2. Определить агента (architect / writer / explorer) по типу
3. Сформулировать промпт из артефактов + пути к ключевым файлам
4. Вызвать Task tool — агент сам читает код

### Антипаттерн

```
Задача: «Делегировать architect; вход — design.md, ДействияСервер»
Read Module.bsl → Grep вызовов → Read ManagerModule.bsl → SemanticSearch → Read ещё 3 файла → ... (агент не вызван)
```

### Правильно

```
Задача: «Делегировать architect; вход — design.md, ДействияСервер»
Read design.md → Glob путь к ДействияСервер → Task(onec-code-architect, prompt=задача + пути)
```

---

## EXPLORE MODE

В режиме explore (opsx-explore) аналитические агенты работают как обычно:
- Трасса/стек → trace-analyst → explorer/architect
- Код 3+ модулей → explorer
- Архитектурный вопрос → architect

**Реализационные агенты (writer, reviewer) в explore НЕ запускаются.**

---

**Last updated**: 2026-03-01
**Version**: 1.0
**Source**: Extracted from 1c-feature-dev-enhanced v2.2 (Phase 0-8 workflow replaced by OpenSpec)
