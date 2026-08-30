# Sidecar-промпты Task (kit-van)

Стабильные шаблоны структуры промпта для субагентов. **Не** размещать здесь MUST плотности / «не закрывать без simplifier» — это политика S8 (агент + delegation/review).

Использование: оркестратор вставляет блоки в `Task` prompt.

## explorer-impact

```markdown
## Sidecar: explorer-impact
Цель: blast radius / кто вызывает / что сломается.
Выход: список символов + файлы + вердикт impact (low/med/high) + пути отчёта.
Не предлагать form-add / ChildObjects / заимствование.
```

## explorer-patterns

```markdown
## Sidecar: explorer-patterns
Цель: найти существующий механизм в коде/конфигурации до изобретения нового.
Выход: кандидаты механизмов + почему подходит/нет + ссылки на строки.
```

## worker-bounded-edit

```markdown
## Sidecar: worker-bounded-edit
Граница: только файлы/процедуры из задачи; не расширять scope.
Запрет: сырой Write XML; создание метаданных; -FromObject / form-add.
После правок: вернуть created_or_modified_symbols.
```

## reviewer-diff-first

```markdown
## Sidecar: reviewer-diff-first
Сначала diff / touched procedures, потом каталог AP.
Phase 0 по Intent/Contract; не пропускать доменный тест имён в touched-scope.
Не закрывать «шум поверхности» только Elegance Score — см. агент reviewer (политика S8 вне sidecar).
```

## Связь с session-save

Поля handoff **Current / Next / Decisions** совпадают с шаблоном `/session-save` → `temp/session-notes.md`. При наличии S3: после длинной сессии предлагать `/session-save` перед сменой чата.
