## Срез S1 — передача на приёмку: chat-surface-clarity

**Change:** chat-surface-clarity  
**Schema:** spec-driven  
**Прогресс:** 5/5 рабочих задач S1 [x]; `S1.accept` — `[ ]` (ручная приёмка)

### 1. Что реализовано

1. [x] S1.1 — канон вопроса режима формы: вручную / автоматически (Form.xml в репозитории) / программно; skill — agent-only  
   - Файл: `.cursor/rules/forms-mxl-mode-gate.mdc`
2. [x] S1.2 — эталоны decision-block и замены lexicon без «через skill» как хорошего примера  
   - Файлы: `.cursor/docs/templates/decision-block.md`, `.cursor/docs/chat-lexicon.md`
3. [x] S1.3 — faq и quick-start на `form_mode`, макет на new не обещают  
   - Файлы: `.cursor/docs/faq-kit.md`, `.cursor/docs/quick-start.md`
4. [x] S1.4 — ярлыки режима формы в handoff explore без «через skill»  
   - Файл: `.cursor/skills/openspec-explore/templates/handoff-block.md`
5. [x] S1.5 — HALT процессных преамбул перед вопросом режима формы в new  
   - Файл: `.cursor/skills/openspec-new-change/SKILL.md`

### Карта правок (перед тестом)

1. Канон вопроса формы — три варианта на языке Конфигуратор / репозиторий / модуль — [`.cursor/rules/forms-mxl-mode-gate.mdc`](.cursor/rules/forms-mxl-mode-gate.mdc)
2. Эталоны «хорошо» и словарь — без «через skill» — [`.cursor/docs/templates/decision-block.md`](.cursor/docs/templates/decision-block.md), [`.cursor/docs/chat-lexicon.md`](.cursor/docs/chat-lexicon.md)
3. FAQ / quick-start — `form_mode`, без макета в new — [`.cursor/docs/faq-kit.md`](.cursor/docs/faq-kit.md), [`.cursor/docs/quick-start.md`](.cursor/docs/quick-start.md)
4. Handoff explore и HALT преамбул в new — [`.cursor/skills/openspec-explore/templates/handoff-block.md`](.cursor/skills/openspec-explore/templates/handoff-block.md), [`.cursor/skills/openspec-new-change/SKILL.md`](.cursor/skills/openspec-new-change/SKILL.md)

Полная карта: `openspec/changes/chat-surface-clarity/reports/code-map.md`

### 2. Что проверить СЕЙЧАС

1. Открыть канон Mode Gate («Формулировка вопроса (чат)») — три варианта без `skill compile`, «через skill», «уже в поставке»
2. Просмотреть эталоны decision-block / lexicon / faq — нет «через skill» как обязательной формулировки; faq на `form_mode`
3. (Опционально) В new SKILL есть явный HALT преамбул перед вопросом режима формы

Остальные сценарии — см. `tasks.md` у `S1.accept`.

### 3. Следующие задачи

| Задача | Действие | Тип | Исполнитель | Зависит от | Статус |
|--------|----------|-----|-------------|------------|--------|
| `S1.accept` | принять срез S1 — канон и зеркала без жаргона kit | Ручной тест | пользователь | S1.1–S1.5 | [ ] |
| `S2.1` | убрать имя внутреннего гейта архитектуры из user-facing new | Проверка | оркестратор | S1.accept | [ ] |
| `S2.2` | переписать AskQuestion приёмки среза в apply | Проверка | оркестратор | S1.accept | [ ] |

### 4. Как вернуться

`/opsx:apply chat-surface-clarity` — новая сессия начнётся с запроса вердикта по S1.

### 5. Blockers

Нет.

### 7. Short-cut

Если уже проверено и принято — напишите обычной фразой («принято», «срез S1 принят»), отмечу без полного handoff.
