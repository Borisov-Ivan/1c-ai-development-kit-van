## Срез S1 — передача на приёмку: hardcode-justification-gate

**Change:** hardcode-justification-gate
**Schema:** spec-driven
**Прогресс:** 5/5 рабочих задач S1 [x]; приёмка S1.accept: [ ]

### 1. Что реализовано

В каноне kit появился именуемый класс Hardcoded Identity Filter (AP-055): краткий индекс и Writer bulletin в `bsl-antipatterns.mdc`, полная карточка в `docs/antipatterns`. Рядом с Existing Mechanisms — запах Scope-as-literals и SSOT-шаблон секции Hardcode Justification для копирования в design прикладных ЗНИ. Граница с литералами протокола/enum зафиксирована явно.

### Карта правок (перед тестом)

1. В индексе антипаттернов добавлен AP-055 (bulletin + таблица). [`73:73:.cursor/rules/bsl-antipatterns.mdc`](.cursor/rules/bsl-antipatterns.mdc)
2. Полная карточка AP-055 с детекторами и out-of-class. [`2928:3028:.cursor/docs/antipatterns/bsl-antipatterns.md`](.cursor/docs/antipatterns/bsl-antipatterns.md)
3. Запах Scope-as-literals и SSOT Hardcode Justification. [`88:110:.cursor/rules/existing-mechanism-priority.mdc`](.cursor/rules/existing-mechanism-priority.mdc)

Полная карта: `openspec/changes/hardcode-justification-gate/reports/code-map.md`

### 2. Что проверить СЕЙЧАС

**Primary acceptance:**

1. Открыть `.cursor/rules/bsl-antipatterns.mdc` (индекс + Writer bulletin) и `.cursor/docs/antipatterns/bsl-antipatterns.md` — есть AP-055 (Hardcoded Identity Filter) с детекторами и remediation.
2. Открыть `.cursor/rules/existing-mechanism-priority.mdc` — есть Scope-as-literals и SSOT шаблона Hardcode Justification.

Опционально: граница «не путать с литералами протокола/enum»; запах стоит в блоке анти-паттернов Existing Mechanisms.

### 3. Следующие задачи

| Задача | Действие | Тип | Исполнитель | Зависит от | Статус |
|--------|----------|-----|-------------|------------|--------|
| `S1.accept` | Принять срез «Реестр и запах» | Ручной тест | пользователь | S1.1–S1.4 | [ ] |
| `S2.1` | Identity Filter Gate в architect | Проверка | оркестратор | S1.accept | [ ] |
| `S2.2` | Триггер в architect-gate | Проверка | оркестратор | S2.1 | [ ] |
| `S2.3` | Запрет обхода «временный список» | Проверка | оркестратор | S2.1 | [ ] |
| `S2.accept` | Принять срез Architect HALT | Ручной тест | пользователь | S2.1–S2.3 | [ ] |

### 4. Как вернуться

`/opsx:apply hardcode-justification-gate` — новая сессия начнётся с запроса вердикта по S1.

### 5. Blockers

Нет.

### 7. Short-cut

Если уже проверено и принято — напишите «принято» / «срез S1 принят».
