## Срез S2 — передача на приёмку: kit-session-api-mode

**Change:** kit-session-api-mode
**Schema:** spec-driven
**Прогресс:** 9/10 задач среза S2 [x] (приёмка `S2.accept`: [ ]); срез S1 принят (manual shortcut)

### 1. Что реализовано

- [x] S2.1 — в FAQ kit: как включить `-noapi` / `--noapi`, как выключить `-api` / `--api`, и что это не пропуск архитектора; файл: `.cursor/docs/faq-kit.md`
- [x] S2.2–S2.8 — одна строка в палитре дорогих команд: ключ пишется в чате и не флаг команды; не в списках «Флаги» / Optional flag; файлы: `opsx-new.md`, `opsx-verify.md`, `opsx-apply.md`, `opsx-extend.md`, `opsx-explore.md`, `review.md`, `release-review.md`
- [x] S2.9 — в описании `/opsx:status` ключ не объявлен флагом и не параметром ввода; файл без правки: `.cursor/commands/opsx-status.md`

### Карта правок (перед тестом)

См. `reports/code-map.md`, секция «Срез S2 — Подсказка в палитре».

- **S2.1** · FAQ kit · секция «Режим без API» (created) — как включить и выключить ключом и чем это не пропуск архитектора. [`.cursor/docs/faq-kit.md`](.cursor/docs/faq-kit.md):12-16
- **S2.2** · палитра `/opsx:new` · строка про ключ (created) — не в Optional flag. [`.cursor/commands/opsx-new.md`](.cursor/commands/opsx-new.md):10
- **S2.4** · палитра `/opsx:apply` · строка про ключ (created) — не в списке «Флаги». [`.cursor/commands/opsx-apply.md`](.cursor/commands/opsx-apply.md):10
- **S2.7** · палитра `/review` · строка про ключ (created) — не в списке «Флаги». [`.cursor/commands/review.md`](.cursor/commands/review.md):10
- **S2.9** · палитра `/opsx:status` · сверка (без правки) — `-noapi` не флаг и не параметр ввода. [`.cursor/commands/opsx-status.md`](.cursor/commands/opsx-status.md):17-22

Кода 1С в срезе нет — секция Explain scope не требуется.

### 2. Что проверить СЕЙЧАС

1. В FAQ kit есть как включить режим ключом в чате, как выключить, и чем это не является пропуском архитектора.

Опционально: открыть описание `/opsx:new` или `/opsx:apply` — видна одна строка про ключ, и её нет в списке флагов команды.

### 3. Следующие задачи

| Задача | Действие | Тип | Исполнитель | Зависит от | Статус |
|--------|----------|-----|-------------|------------|--------|
| `S2.accept` | Принять срез «Подсказка в палитре» — в FAQ видно включение, выключение и отличие от пропуска архитектора | Ручной тест | пользователь | `S2.1`–`S2.9` | [ ] |

### 4. Как вернуться

`/opsx:apply kit-session-api-mode` — начнётся с запроса вердикта по срезу S2. Это последний срез ЗНИ.

### 5. Blockers

Нет.

### 7. Short-cut

Если уже проверено и принято — напишите обычной фразой («принято», «срез S2 принят»).
