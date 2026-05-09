---
name: framework-ux-cleanup
overview: Масштабная чистка фреймворка opsx. Удаляем мёртвый код, разделяем гигантские файлы, вводим прозрачный стандарт UX без жаргона и жёстко закрепляем корректировку ЗНИ только через /opsx:extend.
todos:
  - id: delete-dead-code
    content: Удалить мёртвые агенты, команды и документы (mcp-deploy, onec-admin, onec-code-simplifier, onboard, system-review, phase-gates)
    status: pending
  - id: clean-references
    content: Вычистить ссылки на удалённые файлы из правил (AGENTS.md, tool-name-guard и др.)
    status: pending
  - id: create-ux-standard
    content: Создать agent-to-user.mdc (единый стандарт UX) и удалить старые правила (verify-user-communication, opsx-output-style)
    status: pending
  - id: fix-verify-workflow
    content: "Переписать openspec-verify-change/SKILL.md: убрать жаргон, запретить ручные правки ЗНИ (оставить только /opsx:extend)"
    status: pending
  - id: split-patterns
    content: Разбить 1c-agent-patterns/SKILL.md на узкоспециализированные файлы по ролям
    status: pending
  - id: update-other-skills
    content: "Обновить остальные opsx-скиллы: вычистить T-коды, перевести на agent-to-user.mdc"
    status: pending
  - id: fix-precedent-terms
    content: Переименовать термины (Blast Radius и т.д.) в precedent-regression-gate.mdc для генерации понятных сообщений
    status: pending
  - id: test-verify
    content: Прогнать verify на текущем ЗНИ для проверки нового вывода
    status: pending
isProject: false
---

# План: UX-санитизация и подсушка фреймворка

## 1. Удаление мёртвого кода и связей
- Удалить неиспользуемые агенты: `mcp-deploy.md`, `onec-admin.md`, `onec-code-simplifier.md` (последний убираем для подсушки, так как явного использования нет).
- Удалить `openspec-onboard/SKILL.md` (включая каталог и команду `opsx-onboard.md`).
- Удалить мёртвые документы: `precedent-regression-system-review.md`, `instruction-system-map.md`, `phase-gates.mdc`.
- Вычистить ссылки на удалённые файлы из `AGENTS.md`, `tool-name-guard.mdc`, `1c-utility-agents.mdc`, `vertical-slices.mdc`, `command-session-persistence.mdc` и из списка команд.

## 2. Создание единого стандарта UX
- Создать `.cursor/rules/agent-to-user.mdc` (короткий файл, до 50 строк) с прозрачными правилами общения:
  - Строгий запрет внутренних кодов в чате (T-REPORT, 9b, Phase A, Blast Radius).
  - Сначала суть человеческим языком → влияние на код/пользователя → запрос решения.
  - Каждый вариант выбора должен содержать расшифровку «что я увижу/сделаю».
  - Включить два эталонных примера (блокер verify и handoff).
- Удалить старые перегруженные правила: `verify-user-communication.mdc` (130 строк) и `opsx-output-style.md` (231 строка).
- Переписать `verify` (`.cursor/skills/openspec-verify-change/SKILL.md`):
  - Убрать генерацию сообщений с T-REPORT.
  - **Меры контроля (качество и прозрачность процесса):** Убрать вариант ручных правок `design.md` для `decision`-класса проблем. Внедрить правило: **для любых корректировок ЗНИ после их создания используется строго `/opsx:extend`**.

## 3. Рефакторинг гигантских скиллов
- Разбить `.cursor/skills/1c-agent-patterns/SKILL.md` (1916 строк) на несколько изолированных модулей по ролям (например: `architect.md`, `writer.md`, `reviewer.md`, `explorer.md`).
- В самом `1c-agent-patterns/SKILL.md` оставить только навигатор со ссылками на разбитые модули.

## 4. Обновление остальных opsx-скиллов
- Вычистить ссылки на "T-*" (T-BRIEF, T-HANDOFF, T-REPORT) в скиллах `debug`, `explore`, `apply`, `extend`, `estimate`, `status`, заменить на ссылки на новый стиль `agent-to-user.mdc`.
- Отредактировать `.cursor/rules/precedent-regression-gate.mdc`: переименовать термины `Blast Radius` и `precedent-regression` для коммуникации в понятные человеческие фразы («отмена ранее принятого решения», «что меняется для пользователя»).

## 5. Контроль и калибровка
- Провести тестовый запуск обновлённого `/opsx:verify` на текущем ЗНИ (`do2-soglasovanie-povtor-forma-ux-v2`).
- Убедиться, что отчёт читается без словаря терминов и предлагает единственный корректный путь исправления — через `/opsx:extend`.