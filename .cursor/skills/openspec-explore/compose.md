# Сборка отчёта /opsx:explore

Когда все пункты TodoWrite, кроме «Собрать и проверить отчёт», — `completed`.

## Preflight

1. `Glob` `<SESSION_DIR>/temp/step-*.md` — исключить `*.stub.md`, `*.prev-*.md`.
2. Для каждого `step-id` из маршрута брифа — ровно один канонический файл (при дублях — новейший по mtime).
3. Если обязательная `target-section` профиля без valid step — blocker до композиции.
4. Прочитать `brief.md`: `user-goal`, `success-criteria` — передать composer.

## Fast-path

**Условие:** `profile: explore-question` **и** в маршруте один исследовательский пункт **и** один valid `step-*.md`.

**Действие:** оркестратор `Read` step-файл → `Write` `<SESSION_DIR>/analysis.md` с шапкой + `## Для заказчика` + content. **Без** `openspec-composer`. Перед `Write` — **T-EXPLORE-DECISION** в чате из step + brief. Todo «Собрать…» — `completed`.

## Стандартный путь

1. Todo «Собрать и проверить отчёт» — `in_progress`.
2. `Task` → `openspec-composer` (без `model=`), промпт: `brief-path`, `step-paths[]`, `profile`, `topic`, `pass-number: 1`, пути draft/result; при early-close после trace — `early-close: trace-sufficient`.
3. `Read` `<SESSION_DIR>/temp/composer-result-pass1.md`.
4. `verdict: needs_fix` с blocker → пересборка затронутых шагов через explorer → `Task` composer `pass-number: 2` с `issues-from-prev-pass`.
5. `verdict: clean` → `Read` `draft-report.md`.
6. **Сформировать T-EXPLORE-DECISION в чате** из секций `## Для заказчика` и `## Свод` draft (10–14 строк). **HALT:** не переходить к п.7 без SVOD в чате.
7. `Write` `<SESSION_DIR>/analysis.md` из draft (первая секция после шапки — `## Для заказчика`).
8. Todo — `completed`.

## Финальное сообщение в чат

**Не** одна строка с путём к файлу.

Оркестратор выводит **T-EXPLORE-DECISION** (если не выведен на шаге 6 — повторить здесь). Путь к `analysis.md` — **последняя** строка блока **Детали**.

- `explore-doc` / `explore-bug`: команды `/opsx:ff` / `/opsx:extend --from-report` — только в слоте **Позже**, если вердикт требует кода.
- `explore-question`: без предложения `/opsx:new` по умолчанию.

Шаблон — `.cursor/docs/opsx-output-style.md` §5.1a.
