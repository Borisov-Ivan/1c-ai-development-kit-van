## Срез S1 — передача на приёмку: sequential-ui-mode-questions

**Change:** sequential-ui-mode-questions  
**Schema:** spec-driven  
**Прогресс:** 3/3 рабочих задач [x]; `S1.accept` — `[ ]` (ручная приёмка)

### 1. Что реализовано

В протоколе `/opsx:new` закреплён инвариант: один вопрос выбора за ход чата. После вопроса про описание маркера оркестратор обязан завершить ход и не смешивать Mode Gate / Design Gate в том же сообщении. В карточке Metadata и в Guardrails — явный запрет соседних выборов и dual-selection self-check.

### Карта правок (перед тестом)

1. После вопроса маркера — пауза до ответа; Mode Gate только отдельным сообщением — [`94:129:.cursor/skills/openspec-new-change/SKILL.md`](.cursor/skills/openspec-new-change/SKILL.md)
2. В шаблоне Metadata — запрет соседних Mode/Design в том же сообщении — [`45:45:.cursor/docs/templates/brief-card.md`](.cursor/docs/templates/brief-card.md)
3. Перед отправкой: два выбора в черновике → не отправлять — [`382:382:.cursor/skills/openspec-new-change/SKILL.md`](.cursor/skills/openspec-new-change/SKILL.md)

Полная карта: `openspec/changes/sequential-ui-mode-questions/reports/code-map.md`

### 2. Что проверить СЕЙЧАС

**Primary acceptance:**
1. Учебный прогон `/opsx:new` (или сверка текста протокола): после ответа на вопрос про маркер (или его пропуск) вопрос про режим формы **не** появляется в том же сообщении.
2. Первый вопрос режима формы — отдельным сообщением на этапе design (между Metadata и Mode допустимы сообщения без выбора).

Опционально: по тексту SKILL dual AskQuestion запрещён в self-check (Guardrails).

### 3. Следующие задачи

| Задача | Действие | Тип | Исполнитель | Зависит от | Статус |
|--------|----------|-----|-------------|------------|--------|
| `S1.accept` | принять срез «Один вопрос за ход» | Ручной тест | пользователь | `S1.1`–`S1.3` | [ ] |
| `S2.1` | Mode Gate только форм + `form_mode` / `forms:` | Проверка | оркестратор | `S1.accept` | [ ] |
| `S2.2` | Mode Gate форм на design (цикл per-form) | Проверка | оркестратор | `S2.1` | [ ] |

### 4. Как вернуться

`/opsx:apply sequential-ui-mode-questions` — новая сессия начнётся с запроса вердикта по срезу S1.

### 5. Blockers

Нет.

### 7. Short-cut

Если уже проверено и принято — напишите обычной фразой («принято», «срез S1 принят»), отмечу без полного handoff.
