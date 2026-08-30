# Доменные кейсбуки (kit-van)

On-demand справочники по типовым решениям проектирования. Канон пути: `.cursor/docs/casebooks/`.

**Не** смешивать с вендорским `.cursor/docs/standard/std-*` / `1c-standards-navigator.md` (D2). Без MCP как обязательного пути.

| Файл | Назначение |
|------|------------|
| [locks-and-transactions.md](./locks-and-transactions.md) | Управляемые блокировки, границы транзакций, порядок блокировок, deadlock |
| [logging-strategy.md](./logging-strategy.md) | Журнал регистрации: когда писать, уровни, структура события |
| [registers-design.md](./registers-design.md) | Выбор и проектирование регистров |
| [dcs-design.md](./dcs-design.md) | Проектирование отчётов СКД (не XML-механика) |
| [async-methods.md](./async-methods.md) | `Асинх` / `Ждать` и legacy `ОписаниеОповещения` |
| [platform-solutions.md](./platform-solutions.md) | Типовые ловушки платформы и рабочие шаблоны |
| [form-module-notes.md](./form-module-notes.md) | Модуль формы: события, reserved names, данные формы |
| [metadata-xml-workarounds.md](./metadata-xml-workarounds.md) | Частые ошибки XML при **ручных** правках / инструкциях Конфигуратора |

Router: секция «Доменные кейсбуки» в `.cursor/docs/1c-coding-standards.md`.
