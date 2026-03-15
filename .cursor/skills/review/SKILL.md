---
name: review
description: Full code review by request context (module, files, extension) with optional fix via writer and reviewer. APPLY GATE exception — см. .cursor/rules/1c-agent-delegation.mdc (секция APPLY GATE).
license: MIT
compatibility: Delegates to onec-code-reviewer, onec-code-writer. Requires Task tool.
metadata:
  author: project
  version: "1.0"
---

Провести полное подробное ревью кода в объёме по контексту запроса пользователя, делегировать ревью **onec-code-reviewer**, сохранить отчёт, затем по подтверждению пользователя передать замечания **onec-code-writer** для устранения с обязательным повторным ревью (макс. 2 итерации).

**Input**: путь к модулю (.bsl), список файлов, имя расширения, «текущий файл» или файлы change — по контексту запроса.

---

## Шаг 1. Resolve scope

Определить scope по приоритету из контекста запроса:

1. **Явно указанные пути** — пользователь указал путь(и) к .bsl или перечислил файлы (например «ревью модуля формы КД_НастройкаМЧД»). Нормализовать пути относительно корня репозитория.
2. **Текущий/открытый файл** — формулировки «ревью этого модуля», «review current file» и т.п. Взять путь из открытого в IDE файла (recently viewed / current file из контекста). Проверить, что файл — .bsl.
3. **Расширение** — указано имя расширения или «ревью расширения X». Прочитать `openspec/project.md`, взять из секции «Структура репозитория» пути к cfe. Искать .bsl по путям из project.md (по пути к каталогу расширения + `**/*.bsl`) или Glob `src/**/cfe/<имя>/**/*.bsl`; если в project.md заданы явные пути — использовать их.
4. **Активный change** — scope не задан, но есть каталог в `openspec/changes/` (кроме `_template`, `archive`). AskQuestion: «Ревью только файлов, затронутых change, или всего расширения change?»
   - **Файлы change:** выполнить `git diff --name-only HEAD` и `git diff --name-only --cached`, отфильтровать по `*.bsl` в директории расширения этого change. Если diff пуст — парсить `openspec/changes/<id>/tasks.md` на упоминания путей к .bsl и взять уникальные файлы.
   - **Всё расширение:** определить расширение по change (из design.md или по пути) и взять все .bsl в нём.

**Валидация:** все пути должны существовать, расширение файлов — `.bsl`. Если scope неоднозначен — **AskQuestion**: один файл / список файлов / расширение / файлы change.

**Итог шага:** список путей к .bsl (нормализованные).

---

## Шаг 2. Контекст для ревьювера

- Прочитать `.cursor/rules/1c-coding-standards.mdc`. Ссылка на `.cursor/agents/onec-code-reviewer.md` для категорий и Phase 0.
- Сформировать бриф:
  - Список файлов (пути).
  - Стандарты: 1c-coding-standards.mdc.
  - Задача: «Полный подробный ревью (все категории). Без mode=prerelease.»
  - Для scope «расширение»: префикс расширения и полная директория расширения (для Grep по вызовам при проверке неиспользуемого кода) — если известны.
- **Для файлов с `&ИзменениеИКонтроль`:** прочитать `openspec/project.md`, взять путь к cf из секции «Структура репозитория». В пути к файлу расширения заменить сегмент `cfe/<ExtName>/` на путь к cf из project.md, сохраняя тот же родительский корень — получить полный base-путь. Передать в промпт reviewer: «Base-файл (для &ИзменениеИКонтроль): <полный путь к base>» по файлу (EXTENSION GATE из `1c-agent-delegation.mdc`).

---

## Шаг 3. Делегирование ревью

Вызвать **Task**(`subagent_type="onec-code-reviewer"`) с промптом по шаблону «Reviewer (ревью кода)» из `.cursor/skills/1c-agent-patterns/SKILL.md`:

- Файлы: список из шага 1.
- Стандарты: 1c-coding-standards.mdc.
- Диагностики линтера: «линтер не выявил ошибок» (до правок линт не запускался).
- Base-файл(ы): из шага 2 для файлов с &ИзменениеИКонтроль.
- **Resolved Contracts:** если это повторный вызов после шага 3.5 (Investigation Loop) — включить блок `## Resolved Contracts` из результата explorer. При первом вызове — без Resolved Contracts.
- Включить блоки: Reasoning focus (Phase 0), Стандартный фокус, Проверка соблюдения gates (HALT-compliance), Зрелость интеграции.
- **Не** передавать mode=prerelease.

**Батчи:** если файлов больше 5–8 — разбить на батчи по 5–8 файлов, запускать вызовы reviewer параллельно где возможно. Итоговый список замечаний — объединение выводов всех батчей с дедупликацией по «файл:строка:категория».

---

## Шаг 3.5. Investigation Loop (резолв контрактов по запросу ревьювера)

1. **Парсинг:** в выводе ревьювера искать секцию `## Investigation Request`. Если секция отсутствует — пропустить шаг, перейти к шагу 4.
2. **Если секция есть:** извлечь таблицу (Метод, Контекст вызова, Что нужно определить).
3. **Вызов explorer:** один вызов **Task**(`subagent_type="onec-code-explorer"`) по глубокому шаблону «Explorer — contract resolution (deep)» из `.cursor/skills/1c-agent-patterns/SKILL.md`. Передать всю таблицу из Investigation Request одним батчем. Explorer возвращает блок `## Resolved Contracts`.
3a. **Сохранение артифакта.** Сохранить полный вывод explorer (блок `## Resolved Contracts` + Evidence + вердикт) в файл:
   - При активном change: `openspec/changes/<id>/reports/resolved-contract-<scope-slug>-YYYY-MM-DD.md`
   - Без change: `temp/reports/resolved-contract-<scope-slug>-YYYY-MM-DD.md`
   Формат содержимого: заголовок (дата, scope, цель), затем блок Resolved Contracts целиком от explorer. Это артифакт ЗНИ — доступен в следующих сессиях.
4. **Повторное ревью:** вызвать **Task**(`subagent_type="onec-code-reviewer"`) — тот же scope (шаг 1), тот же контекст (шаг 2) + блок `## Resolved Contracts` из сохранённого файла (шаг 3a). Промпт: «Повторное ревью с Resolved Contracts. Обновить Phase 2.5 (Defensive Checks, Попытка Audit), Contract Map и findings. Секцию Investigation Request НЕ включать.»
5. **Максимум 1 итерация:** investigation loop выполняется не более одного раза (reviewer → explorer → reviewer). После второго прогона ревьювера — перейти к шагу 4 в любом случае.

**Сохранение отчёта первого прогона:** первый отчёт (с Investigation Request) сохраняется с суффиксом `-initial` в имени файла. Итоговый отчёт (после investigation loop) сохраняется без суффикса в шаге 4.

---

## Шаг 4. Отчёт

- Сохранить **полный** вывод reviewer в файл (собственное правило скилла; `preserve-subagent-reports.mdc` не применяется к reviewer):
  - При активном change: `openspec/changes/<id>/reports/review-<scope-slug>-YYYY-MM-DD.md`.
  - Иначе: `temp/reports/review-<scope-slug>-YYYY-MM-DD.md`.
  - `<scope-slug>` — короткий идентификатор (например имя модуля, имя расширения или `change-<id>`); YYYY-MM-DD — текущая дата.
- При выполненном шаге 3.5 — в reports/ также сохранён `resolved-contract-*.md` (артифакт ЗНИ). Упомянуть путь в сводке пользователю.
- Вывести пользователю сводку: количество замечаний по уровням (CRITICAL, HIGH, MEDIUM, LOW), разделение на кодовые и архитектурные (если reviewer явно пометил), путь к полному отчёту.

---

## Шаг 5. Предложение устранить

Если есть кодовые замечания (уровни critical / high / medium / low):

**AskQuestion:** «Устранить замечания через onec-code-writer? (Да / Нет, только отчёт)»

- **Нет** — перейти к шагу 7 (Итог), не вызывать writer.
- **Да** — перейти к шагу 6.

Если кодовых замечаний нет — перейти к шагу 7.

---

## Шаг 6. Устранение (при «Да»)

- **Архитектурные замечания** (новый объект, API, RLS, структура хранения) — не передавать writer. Вывести их списком пользователю с пометкой, что для них нужны отдельные решения.
- **Кодовые замечания** — отфильтровать: передавать writer только замечания с **Action: MUST_FIX**. Замечания VERIFIED_OK и OPTIONAL не передавать. Сгруппировать по файлам.

**Чеклист перед вызовом writer (если был шаг 3.5):**
- Файл `reports/resolved-contract-*.md` существует (сохранён на шаге 3a).
- Полный блок `## Resolved Contracts` из этого файла включён в промпт writer.
- Без блока вызов writer **не выполнять** для замечаний, затрагивающих контракты из Investigation Request.

Для каждого затронутого файла:
  1. Вызвать **Task**(`subagent_type="onec-code-writer"`) по шаблону **«Writer — review fix»** из `.cursor/skills/1c-agent-patterns/SKILL.md`. Для каждого замечания передать: ID, Severity, Procedure, Anchor, Issue, Fix. Если после шага 3.5 есть блок Resolved Contracts — **обязательно** включить его в промпт writer целиком (из сохранённого файла). Writer использует контракт для выбора стратегии (fixed — не добавлять проверки; dynamic — минимальная проверка).
  2. **LINT GATE:** ReadLints по изменённым .bsl. При ошибках — исправить (повторный writer или точечная правка), затем снова ReadLints.
  3. **API EXISTENCE CHECK:** по правилам из `1c-agent-delegation.mdc` (секция API EXISTENCE CHECK) проверить новые вызовы вида `МодульИмя.МетодИмя(` в diff. При WARNING — AskQuestion пользователю.
  4. При наличии `&ИзменениеИКонтроль` в файле — **EXTENSION VERIFICATION** (сравнение кода вне #Вставка/#Удаление с base в cf/). При расхождении — вернуть writer на исправление.
  5. Вызвать **Task**(`subagent_type="onec-code-reviewer"`) по изменённым файлам: передать контекст «ревью после устранения замечаний по отчёту /review», вывод линтера, base-пути при необходимости. Передать в промпт reviewer блок `## Resolved Contracts` из файла `reports/resolved-contract-*.md`. Reviewer использует для Phase 2.5 и Defensive Checks.
- При новых замечаниях после первого ревью — повторить цикл writer → LINT → API CHECK → (EXTENSION VERIFICATION) → reviewer. **Максимум 2 итерации** (первое устранение + один повтор). После этого перейти к шагу 7 даже при оставшихся замечаниях.

---

## Шаг 7. Итог

- Краткое резюме: что отрецензировано (scope), сколько замечаний устранено, путь к полному отчёту.
- Не устранённые архитектурные замечания — списком.
- Напомнить: при необходимости создания openspec change по замечаниям — вручную или через соответствующую команду.

---

## Интеграция

- **command-skill-gate.mdc:** первый и единственный инструмент в первом батче — Read этого скилла.
- **command-session-persistence.mdc:** протокол действует на каждом ходе сессии /review (resolve scope → review → report → ask fix → fix loop).
- **bsl-write-guard / 1c-agent-delegation:** правки .bsl только через onec-code-writer; после правок — обязательный onec-code-reviewer; LINT GATE и API EXISTENCE CHECK после writer; EXTENSION GATE и EXTENSION VERIFICATION при &ИзменениеИКонтроль. **Investigation Loop** (шаг 3.5) — reviewer запрашивает исследование контрактов, оркестратор делегирует explorer, перезапускает ревью с Resolved Contracts. Формат и шаблон — секция CONTRACT RESOLUTION в `1c-agent-delegation.mdc`.
- **APPLY GATE:** вызов writer и reviewer в рамках /review разрешён без /opsx:apply — см. исключение в `.cursor/rules/1c-agent-delegation.mdc` (секция APPLY GATE).

---

## Граничные случаи

- **Замечаний нет:** сообщить «Замечаний не найдено», указать путь к сохранённому отчёту.
- **Только архитектурные:** предложение устранить не показывать; вывести список архитектурных замечаний и перейти к шагу 7.
- **Нет открытого файла при «текущий файл»:** AskQuestion — указать путь вручную или выбрать другой scope.
