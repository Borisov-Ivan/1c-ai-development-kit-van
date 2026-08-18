## Срез S1 — передача на приёмку: explain-after-review-apply-scope

**Change:** explain-after-review-apply-scope  
**Schema:** spec-driven  
**Прогресс:** 9/9 рабочих задач [x]; приёмка среза S1.accept: [ ]

### 1. Что реализовано

В kit после `/review`, `/release-review` и apply с BSL появляется секция `## Explain scope` (в review-отчёте и в `code-map.md` как SSOT). Финалы могут предложить `/opsx:explain` ниже приоритета fix/extend. При входе explain с `@` на такой артефакт бриф B-explain заполняет Охват (или Варианты для huge release) и пути в Контекст; карта точек ждёт подтверждения.

- [x] S1.1 — Explain scope в review main report  
- [x] S1.2 — Explain scope SSOT в code-map + handoff  
- [x] S1.3 — propose explain в review/release-review  
- [x] S1.4 — опциональный explain в T-HANDOFF  
- [x] S1.5 — строки в commands + review-guide  
- [x] S1.6 — prefill ветка в openspec-explain  
- [x] S1.7 — эталон C + HALT  
- [x] S1.8 — brief-card + примеры команды  
- [x] S1.9 — grep-верификация kit  

### Карта правок (перед тестом)

См. полную секцию в [`reports/code-map.md`](code-map.md). Ключевые файлы: `review/SKILL.md`, `openspec-apply-change/SKILL.md`, `openspec-explain/SKILL.md`, `entry-brief.md`, `opsx-output-style.md`, команды review/release-review/explain, `review-guide.md`, `brief-card.md`.

### 2. Что проверить СЕЙЧАС

**Primary acceptance:** Given отчёт review или code-map/handoff с секцией `## Explain scope`; When вызван `/opsx:explain` на этот артефакт; Then в чате B-explain со слотом Охват (или Варианты), путями в Контекст, и карта точек не начинается до «да».

1. Вызвать `/opsx:explain @openspec/changes/explain-after-review-apply-scope/reports/code-map.md` (или смоделировать по skill: бриф с Охватом из секции Explain scope + path в Контекст).
2. Убедиться: до ответа «да» карта точек не стартует; в Охвате нет сырого полного dump path (path — в Контекст).

Опционально: финал review/apply skill допускает propose explain; в explore строка propose explain на месте; trivial light-review не обязан propose.

### 3. Следующие задачи

| Задача | Действие | Тип | Исполнитель | Зависит от | Статус |
|--------|----------|-----|-------------|------------|--------|
| `S1.accept` | Принять срез — бриф explain с охватом из Explain scope | Ручной тест | пользователь | S1.1–S1.9 | [ ] |

### 4. Как вернуться

`/opsx:apply explain-after-review-apply-scope` — продолжит с запроса вердикта приёмки.

### 5. Blockers

Нет.

### 7. Short-cut

Если уже проверено и принято — напишите обычной фразой («принято» или «срез S1 принят»), отмечу без повторной простыни в чате.
