# Срез S1: Пауза apply ведёт, а не ссылается

**Сценарий:** apply останавливается: в выгрузке нет объектов, код писать некуда; разработчик читает чат и идёт в Конфигуратор по списку.
**Primary acceptance:** в правилах и шаблонах pause-wait чат содержит «где мы», нумерованный список «что создать» и якорь раздела «Что создать в Конфигураторе»; ссылка на файл без списка — провал; decision-block для этой паузы не используется.
**Приёмка:** ручная сверка текстов правил и шаблонов (без информационной базы 1С); опционально — изолированный чат E4 на ЗНИ без метаданных в `src/`.
**Связь со spec:** Requirement «Apply pause-wait is a navigator card» — все Scenario; Requirement «Pause-wait file leads with the recipe» — Scenario «Первый раздел файла — что создать»; Requirement «Command AskQuestion and handoff stay user-facing» — Scenario «Apply pause-wait lists objects in chat».
**Зависимости:** нет.

## 1. Бюджет и стиль

- [x] S1.1 В `.cursor/rules/chat-output-budget.mdc` и `.cursor/rules/chat-output-budget-full.mdc` развести `acceptance`/`final` и pause-wait: инвентарь до 7 пунктов вне лимита 4–8; тест понятности — «можно начать работу»; исключение 3 — ссылка без списка провал (D2, D3).
- [x] S1.2 В `.cursor/docs/opsx-output-style.md` §2.6 и §5.2 заменить одну строку `pause` на pause-wait / pause-decision, уточнить самодостаточность чата и слоты файла паузы (D1, D2).

## 2. Шаблоны и скилл

- [x] S1.3 Добавить `.cursor/skills/openspec-apply-change/templates/pause-wait-chat.md` и `pause-wait-file.md`: эталон чата и каркас файла с разделом «Что создать в Конфигураторе» первым (D2).
- [x] S1.4 В `.cursor/skills/openspec-apply-change/SKILL.md` шаг 7 классифицировать паузу; для wait не копировать «прогресс + ничего в коде»; согласовать `.cursor/rules/1c-no-metadata-creation.mdc` и `.cursor/rules/1c-xml-write-guard.mdc` (чат vs файл) (D1, D4).

## 3. Приёмка стиля

- [x] S1.5 В `.cursor/docs/ux-acceptance-isolated-chat.md` добавить сценарий E4 и анти-паттерн «только ссылка на handoff-pause» (Requirement «Apply pause-wait is a navigator card»).
- [x] S1.6 Записать delta spec `chat-surface-clarity` со Scenario наблюдаемого чата (не implementation-leak).

## 4. Приёмка

- [ ] S1.accept Принять срез S1 «Пауза apply ведёт, а не ссылается» — по тексту правил pause-wait в чате есть список объектов и имя раздела файла:
  - **Primary (обязательно):** открыть `pause-wait-chat.md` и §5.2 `opsx-output-style.md` → в чате обязательны «где мы», список «что создать», якорь раздела «Что создать в Конфигураторе»; ссылка без списка запрещена
  - Scenario «Apply pause-wait lists objects in chat» (опционально): apply при отсутствии объектов → чат не состоит из «0/N» и XML-дампа
  - Scenario «Pause-wait is not a decision fork» (опционально): в заголовке нет A/B «чеклист / имена другие»
  - Scenario «Первый раздел файла — что создать» (опционально): каркас `pause-wait-file.md` начинается с «Что создать в Конфигураторе»

<!-- slice-gate: pause-wait в чате — список объектов и имя раздела файла, не ссылка без списка -->
