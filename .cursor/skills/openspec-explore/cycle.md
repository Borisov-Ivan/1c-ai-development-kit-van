# Цикл /opsx:explore (после утверждения брифа)

Выполняется **только** после ответа пользователя «да» (или эквивалента) **текстом в чате** на бриф Entry Protocol §3 — не через `AskQuestion` для утверждения плана.

## 3.0. Каталог сессии и TodoWrite

1. `<session-slug>` = `<ГГГГ-ММ-ДД>-<slug>` — только `[a-z0-9-]`.
2. Создать каталоги: `openspec/sessions/<session-slug>/temp/`.
3. **`Write`** `openspec/sessions/<session-slug>/brief.md` — текст брифа из чата + YAML:

```yaml
---
session-slug: <session-slug>
profile: <explore-bug | explore-doc | explore-question>
user-goal: <кратко — из секции Цель брифа>
success-criteria: <критерий «решено» из брифа>
---
```

4. `Glob` → `Read` по найденному пути. `<SESSION_DIR>` = `openspec/sessions/<session-slug>/`.
5. **Первым** вызовом после записи — `TodoWrite` (`merge: false`):
   - `explore-bug` + трасса/PERF в артефактах — **первым** «Разбор трассы».
   - Дословно пункты **Маршрут** из утверждённого брифа.
   - **Последним:** «Собрать и проверить отчёт».

## 3.1. Разбор трассы

- `Task` → `onec-trace-analyst` (без `model=`).
- Промпт: путь к трассе (не содержимое), контекст брифа (`user-goal`, `success-criteria`), пути cf/cfe из `openspec/project.md`.
- Промпт: в отчёт обязательна секция **`## Для заказчика`** (1 абзац: вердикт + нужен ли разбор кода).
- Результат: сохранить отчёт в `<SESSION_DIR>/temp/trace-analysis.md` (оркестратор Write из ответа агента или путь из `reports/` — скопировать в session temp).

### 3.1a. Контрольная точка после trace

Сразу после сохранения `trace-analysis.md` — в чат (**обязательно**):

1. **T-EXPLORE-SVOD** из trace (свод по трассе; 5–10 строк).
2. **T-EXPLORE-NAV** (≤6 строк).
3. Вопрос текстом: **«Достаточно для решения?»** — «да, хватит» / «копаем код (следующий шаг маршрута)» / уточнение.

Если пользователь «хватит» / «достаточно»:

- Пропустить оставшиеся explorer-шаги маршрута (кроме «Собрать отчёт»).
- `Task` → `openspec-composer` с `early-close: trace-sufficient` в промпте; минимальный набор step-paths: `trace-analysis.md` + краткий step от оркестратора при необходимости.
- Финал: T-EXPLORE-DECISION в чате, затем `analysis.md`.

Иначе — продолжить §3.2.

## 3.2. Узкие шаги (onec-code-explorer)

Для каждого пункта TodoWrite, кроме «Разбор трассы» и «Собрать и проверить отчёт»:

1. `TodoWrite`: текущий — `in_progress`.
2. `SAVE_PATH` = `<SESSION_DIR>/temp/step-<step-id>-<slug>.md`.
3. `Task` → `onec-code-explorer` с `model` по `.cursor/rules/model-selection.mdc`.
4. Промпт обязан содержать:
   - `brief-path`, `SAVE_PATH`, `target-section`, `step-id`
   - `user-goal`, `success-criteria` из `brief.md`
   - `prev-step-paths[]` из `Glob` `<SESSION_DIR>/temp/step-<prev>-*.md`
   - `trace-analysis-path` если есть
   - блок `## Existing Knowledge` из брифа/KB Discovery
   - **Контракт step-result:** YAML front-matter + `### Объекты` + content + **`### Для заказчика`** (2–4 строки: вердикт шага, влияние на `success-criteria`); `Write` в `SAVE_PATH`.
5. Между шагами в чат — **обязательно** (см. `opsx-output-style.md` §5.1a):
   - **T-EXPLORE-SVOD** (5–10 строк) — самодостаточный свод шага.
   - **T-EXPLORE-NAV** (≤6 строк).
   - Одна строка: `детали: <SAVE_PATH>` (**не** заменяет SVOD).
6. При `scope-expansion` от агента — пересобрать бриф в чате, снова ждать подтверждение текстом, `TodoWrite` заново (`merge: false`).

### Мини-проверка перед `completed`

- `Glob` `SAVE_PATH` — файл существует, не пустой, есть YAML `target-section` и `### Для заказчика`.

При двойном провале explorer — stub `*.stub.md` + T-EXPLORE-SVOD с ограничением «шаг не завершён» + одна строка пользователю.

## 3.3. Architect (по триггерам)

Если срабатывает `.cursor/rules/architect-gate.mdc` во время сессии — `Task` → `onec-code-architect` до продолжения маршрута; отчёт в `<SESSION_DIR>/temp/` или `reports/`. После отчёта — T-EXPLORE-SVOD + NAV в чате.

## 4a. Per-turn Delegation Gate

На follow-up после утверждения: обследование кода → только `Task` (explorer/trace-analyst/architect), не Grep/Read .bsl в оркестраторе.

## Повторное утверждение брифа

Правки пользователя или scope-expansion → новый бриф в чат → подтверждение текстом → `Write brief.md` → `TodoWrite` полностью заменить.
