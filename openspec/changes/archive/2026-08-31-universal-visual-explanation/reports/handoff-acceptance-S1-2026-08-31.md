## Срез S1 — передача на приёмку: universal-visual-explanation

**Change:** universal-visual-explanation
**Schema:** spec-driven
**Прогресс:** 12/13 задач [x] (приёмка среза S1.accept: [ ])

### 1. Что реализовано

В kit появился скилл визуального объяснения: по просьбе «покажи, как устроено» панель собирается из текущего ответа, без порога «четыре сущности» и без обязательного журнала. Старый конвейер карты (скилл, фикстуры штампа, агент-сборщик) удалён; указатели сессий, словари и ADR-0010 ведут на новый скилл. Прикладной код 1С не менялся.

### Карта правок (перед тестом)

- **S1.1** · скилл визуального объяснения · протокол просьбы и автопанели (created) — прямая просьба открывает панель из текущего ответа. [`.cursor/skills/visual-explanation/SKILL.md`](.cursor/skills/visual-explanation/SKILL.md):25-54
- **S1.2** · шаблон панели · рендер по форме содержания (created) — поток, таблица, вложенная иерархия или карточка. [`.cursor/skills/visual-explanation/fixtures/panel-shell.md`](.cursor/skills/visual-explanation/fixtures/panel-shell.md):1-18
- **S1.3** · диспетчер · указатель «покажи схему» (modified). [`.cursor/rules/gate-dispatcher.mdc`](.cursor/rules/gate-dispatcher.mdc):28-28
- **S1.8** · старый конвейер карты (removed) — каталог скилла, агент и шаблон промпта удалены.
- **S1.9** · ADR-0010 · несущая замена (created). [`openspec/adrs/ADR-0010-visual-explanation-panel.md`](openspec/adrs/ADR-0010-visual-explanation-panel.md):1-15

Полная карта: `openspec/changes/universal-visual-explanation/reports/code-map.md`

## Explain scope (handoff)

- source: apply
- change: universal-visual-explanation
- focus: slice-S1
- files: []
- report: openspec/changes/universal-visual-explanation/reports/code-map.md

### 2. Что проверить СЕЙЧАС

**Primary (обязательно):** в чате есть обычный ответ на вопрос (не `/opsx:verify`, не `/review`). Попросить «покажи, как это устроено». Рядом с чатом открывается панель кнопкой среды — видны вопрос, вывод и структура ответа; в чате нет пути к файлу панели; это визуальное объяснение, не граф старой карты (нет отказа «мало сущностей» / «укажите отчёт»).

Остальные сценарии — см. `tasks.md` (опционально).

### 3. Следующие задачи

| Задача | Действие | Тип | Исполнитель | Зависит от | Статус |
|--------|----------|-----|-------------|------------|--------|
| `S1.accept` | Принять срез S1 «Визуальное объяснение вместо карты сценария» | Ручной тест | пользователь | рабочие задачи среза | `[ ]` |

### 4. Как вернуться

`/opsx:apply universal-visual-explanation` — новая сессия начнётся с запроса вердикта (принят / не принят / дефект в предыдущем срезе). Если нужно изменить постановку — `/opsx:extend universal-visual-explanation`; затем снова `/opsx:apply universal-visual-explanation`. Пока вы проверяете панель — оркестратор ничего не делает.

### 5. Blockers

Нет.

### 7. Short-cut

Если уже проверено и принято — напишите обычной фразой («принято», «срез S1 принят»), отмечу без полного handoff.
