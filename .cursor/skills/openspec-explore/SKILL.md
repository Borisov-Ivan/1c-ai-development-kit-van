---
name: openspec-explore
description: Единая точка входа — исследование задачи, дефекта или вопроса; финал openspec/sessions/<slug>/analysis.md
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "2.0"
---

# `/opsx:explore` — единая точка входа

Любой свободный текст пользователя (без другой команды) = вход в explore.

**Ценность:** заказчик получает **решение в чате** (свод на каждом шаге + финальная карточка); `openspec/sessions/<slug>/analysis.md` — зеркало для handoff и деталей. ЗНИ (`/opsx:ff`, `/opsx:new`, `/opsx:apply`) — отдельный трек после отчёта.

**Не делает:** правки BSL, создание `openspec/changes/` целиком, полный набор артефактов ЗНИ без `/opsx:ff`.

Детали цикла — [`cycle.md`](cycle.md). Сборка отчёта — [`compose.md`](compose.md). Сессии — [`.cursor/rules/openspec-sessions.mdc`](../../rules/openspec-sessions.mdc).

---

## Bootstrap (первый ход новой темы)

1. `Glob openspec/sessions/*/brief.md` — висячие сессии (есть `brief.md`, нет `analysis.md`).
2. Если висячая — **один** AskQuestion: продолжить / оставить открытой / закрыть и начать новую (§1.5).
3. Иначе — **одна строка** в чат:

   «Готов разобрать задачу, дефект или вопрос. Опишите, с чем работаем — выдам короткий бриф и согласуем маршрут.»

Список команд **не** показывать (только по явному `/help`).

---

## Entry Protocol (MANDATORY)

До утверждения брифа **запрещено:** `Task`, `TodoWrite`, Read `.bsl`/трассы/модулей, Grep по `src/`.

**Допустимо до брифа:** Read этого SKILL, `openspec/project.md`, KB Discovery (`openspec/knowledge/_index.yaml`), `Glob` по **именам** из постановки (1–3 вызова), `openspec list --json`, `AskQuestion` **только** для §1.5 (висячая сессия) и §2 (неоднозначная именная сверка) — **не** для утверждения плана.

### 0. Активные ЗНИ (контекст, не redirect)

`openspec list --json`. Если есть change и вход — баг/трасса: **одна строка** в брифе «Контекст ЗНИ: `<name>`» (при необходимости Read только `proposal.md` §Why — 1 абзац). **Не** предлагать `/opsx:debug` (команда удалена). Capture fix — после отчёта: `/opsx:extend <change> --from-report <path>`.

### 1. Профиль

| Профиль | Маркеры | Канва |
|---------|---------|--------|
| `explore-bug` | `.pff`, `*_TRACE_*.txt`, `*_PERF.txt`, стек, «не работает», «падает», «ошибка», «баг», «регресс» | [`profiles/bug.md`](profiles/bug.md) |
| `explore-question` | «как работает», «почему», «можно ли», «в чём разница» | [`profiles/question.md`](profiles/question.md) |
| `explore-doc` | «нужно сделать», «добавить», «изменить поведение», постановка | [`profiles/doc.md`](profiles/doc.md) |

Смешанный вход с дефектом → `explore-bug`. Профиль пользователю не называть.

### 1.5. Resume висячей сессии

1. **Продолжить** — Read `brief.md`, восстановить TodoWrite по `cycle.md`. В **том же сообщении** (5–7 строк): тема, `user-goal` / **Цель**, `success-criteria` / **Решено, когда**, текущий шаг TodoWrite, что уже в `temp/`; затем `AskQuestion` (продолжить / оставить / закрыть). **Бриф целиком не повторять**; к первому `pending`.
2. **Оставить открытой** — новая тема: §1 → §2.
3. **Закрыть** — `brief.md` → `brief.closed.md`, Delete `brief.md`, §1 → §2.

### 1.6. Knowledge Discovery

По `.cursor/skills/openspec-explore` / `architect-gate.mdc` / `1c-agent-delegation.mdc` §KB CONTEXT. В бриф — **не более 3 строк** «KB в scope» или «нет совпадений…». Полный список — в промпты агентов после «да».

### 2. Именная сверка (лёгкая)

1–3× `Glob`/`Grep` **только по именам** из постановки. Не читать `.bsl`. Не найдено / неоднозначно → **один** AskQuestion → снова сверка → бриф.

**Verify-or-hypothesis:** без сверки — только в **Гипотезы**, не в **Факты**.

### 3. Компактный бриф в чате (END TURN)

Заголовок: `Бриф для исследования: <тема>` (не `## Бриф: /opsx:explore`).

**Обязательные секции** (лимит **14–22 строки** тела **в сообщении пользователю** — `.cursor/rules/chat-output-budget.mdc`):

- **Контекст** — 1 предложение.
- **Что я понял** — 1–2 предложения.
- **Цель** — одна фраза: что должно измениться для заказчика (не для кода).
- **Решено, когда** — 1–2 критерия «исследование завершено».
- **Маршрут** — нумерованный план; формат пункта: `N. <название> (target: <секция>; prev: — или номера)`.
- **Шаг 1 — детали для агента** — роль (`onec-code-explorer` / `onec-trace-analyst`), что искать (3–5 пунктов), ограничения.
- **Подтвердить?** — 1–2 строки **текстом** в том же сообщении: «Утверждаем план? Напишите «да» или что поправить.» Ответ пользователя — обыным сообщением; **`AskQuestion` для утверждения плана не использовать**.

Если цель неочевидна — один уточняющий вопрос в брифе (текстом), до END TURN. Шаблоны свода в чате — `.cursor/docs/opsx-output-style.md` §5.1a.

**Опционально** (пустые — опустить): Сценарий, Факты, Гипотезы, Технический контекст, Артефакты, Открытые вопросы (≤2 блокирующих).

**Запрещено:** второй заголовок брифа, «Карта прояснённости», KB больше 3 строк, `temp/briefs/*.md`, вызов **только** `AskQuestion` без полного текста брифа в том же ответе (**HALT**).

После брифа в чате — **END TURN**. Без `Task`/`TodoWrite`.

**HALT перед отправкой:** если в ответе есть `AskQuestion` для утверждения плана или нет напечатанных секций Контекст / Что я понял / Маршрут / Шаг 1 / Подтвердить? — переписать ответ.

### 4. После «да»

1. Read [`cycle.md`](cycle.md), [`compose.md`](compose.md).
2. Выполнить §3.0 `cycle.md` (Write `brief.md`, TodoWrite).
3. Цикл шагов → [`compose.md`](compose.md).

---

## Per-turn Delegation Gate

После утверждения брифа: обследование кода → только `Task` (`onec-code-explorer`, `onec-trace-analyst`, `onec-code-architect`). Оркестратор не читает `.bsl` для анализа. До 3 Read артефактов OpenSpec для брифа — допустимо.

---

## Change Creation Gate

«Создай ЗНИ» / полный набор артефактов → **СТОП.** Explore Summary в `temp/explore-summary-<date>.md` → предложить `/opsx:ff`. Не Write proposal/design/tasks вручную.

Новое требование в **существующий** change → `/opsx:extend`. Точечный capture в design — только по явной просьбе.

---

## Architect Gate / Verified Cause

Триггеры — `.cursor/rules/architect-gate.mdc`, `.cursor/rules/verified-cause-gate.mdc`. При срабатывании — `onec-code-architect` (Task + model по `model-selection.mdc`). Отчёт в `<SESSION_DIR>/temp/` или `reports/`.

---

## Capture (по запросу)

«Зафиксируй в проекте» → `.cursor/rules/capture-to-project.mdc`. Решение в change → `/opsx:extend`.

---

## Вывод в чат (после утверждения брифа)

На **каждом** ходе (кроме entry END TURN) — **обязательно** в чате:

1. **T-EXPLORE-SVOD** — Свод, Вердикт, Сейчас (5–10 строк).
2. **T-EXPLORE-NAV** — где мы, следующий шаг, строка «детали: …» (≤6 строк).

**HALT:** только путь к файлу без SVOD.

Финал: **T-EXPLORE-DECISION** (10–14 строк) в чате **до** или **вместе с** `Write analysis.md`; путь к `analysis.md` — **последняя** строка. См. [`compose.md`](compose.md), `opsx-output-style.md` §5.1a.

## Handoff после `analysis.md`

| Профиль | Следующий шаг |
|---------|----------------|
| doc / bug | Команды ЗНИ — только в слоте **Позже** финального DECISION, если нужен код: `/opsx:ff <name>` или `/opsx:extend <change> --from-report openspec/sessions/<slug>/analysis.md` |
| question | Свод в чате достаточен; файл — по запросу |

Если есть свежий `analysis.md` — `/opsx:ff` и `/opsx:new` **опускают** entry-бриф (одна строка + подтверждение).

---

## Guardrails

- BSL write guard, tool-name-guard, 1c-agent-delegation — без исключений.
- `openspec-composer` / `openspec-quality-controller` — не для обследования BSL.
- Сохранять полные отчёты субагентов — `preserve-subagent-reports.mdc` (в session `temp/` или change `reports/`).
- Explore **не** реализует; `/opsx:apply` — отдельная команда.

---

## Self-check брифа

1. Тело брифа **напечатано** в ответе пользователю (14–22 строки)?
2. Есть секции: Контекст, Что я понял, **Цель**, **Решено, когда**, Маршрут, Шаг 1, Подтвердить?
3. **Нет** `AskQuestion` для утверждения плана (допустим только §1.5 / §2)?
4. Нет жаргона движка в UX-полях (`.cursor/docs/opsx-output-style.md` §3.1)?
5. Маршрут закрывает обязательные секции профиля?
6. Один бриф, без дубля?
7. Нет `Task`/`TodoWrite` до ответа «да»?

## Self-check хода explore (после брифа)

1. В чате есть **T-EXPLORE-SVOD** (Свод + Вердикт + Сейчас)?
2. Есть **T-EXPLORE-NAV** с одним «следующим шагом»; путь к файлу — **после** свода?
3. Финал: **T-EXPLORE-DECISION** в чате; не только «готов отчёт: …»?
