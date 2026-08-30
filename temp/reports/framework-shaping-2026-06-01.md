# Шлифовка фреймворка — отчёт о принятых решениях

Дата: 2026-06-01. Исполнение плана `framework_shaping_6a1400b7`. Принцип: добавляя/перенося правило — удалять источник дубля и чинить ссылки.

## Волна 1 — гигиена контекста (DONE)

### Удалены 8 always-apply редиректов
`conversational-discipline`, `orchestrator-as-navigator`, `anti-slop`, `command-skill-gate`, `command-session-persistence`, `context-strategy-gate`, `bsl-write-guard`, `1c-xml-write-guard` (`.cursor/rules/*.mdc`).

Содержимое влито в SSOT:
- Навигатор-принцип → `chat-output-budget.mdc` §9 (был циклический редирект сам на себя).
- 5 принципов диалога → `chat-output-budget.mdc` §1a (с указанием параграфов).
- anti-slop pre-send → `chat-output-budget.mdc` §1b.4 + `stop-slop/SKILL.md`; словарь — `chat-lexicon.md`.
- session-discipline уже консолидировал три gate-редиректа (убрана строка «держать legacy-файлы»).
- BSL guard — уже покрыт `1c-agent-delegation.mdc` (LIGHT/MECHANICAL/ИСКЛЮЧЕНИЯ).

### Восстановлена потерянная гарантия (buried gem)
**Шаблон инструкции ручного конфигурирования Form.xml** был утерян в commit `f3e4005` (XML guard схлопнут в редирект без тела). Восстановлен из `a1bd005` и вложен в `1c-agent-delegation.mdc` → новая секция `## XML WRITE GUARD` (таблица делегирования XML + шаблон). Все ссылки скиллов (apply, prerelease, 1c-forms, 1c-bsp, utility-agents) перенаправлены сюда — раньше указывали на пустой редирект.

### Ссылки перенаправлены
extend/review/ff SKILL → `session-discipline.mdc`; XML-ссылки → `1c-agent-delegation.mdc § XML WRITE GUARD`. CHANGELOG.md (историческая запись про onec-form-generator) оставлен как есть.

### AGENTS.md: 211 → 72 строки
Убраны встроенные мини-мануалы (полный абзац reviewer, 5-слойный verify, output-style портянка, дублирующие command-gate секции). Оставлены: диспетчеры, decision tree команд, компактная карта SSOT (один якорь на тему).

### Phantom-ссылки
- `openspec/glossary.md` — **создан** (термины: ЗНИ, срез, S<N>.accept, slice-gate, verify-слои, агенты, cf/cfe, phantom-symbol).
- `/opsx:migrate-acceptance` — **вычищен** (команды нет): заменён на ручное объединение `S<N>.T<M>` → `S<N>.accept` в QC-агенте, vertical-slices, verify SKILL, task-readability.
- `--from-verify-prompt` — **вычищен**: заменён на `/opsx:extend <name>` (передать текст требования).
- `/help` — **вычищен**: «если пользователь явно попросит перечень команд».

### Замер контекста (always-apply строк/ход)
- До: AGENTS 211 + 8 редиректов (~72) + session 38 + chat 142 + delegation 202 + gate 32 ≈ **697**.
- После: AGENTS 72 + session 36 + chat 142 + delegation 228 + gate 32 ≈ **510**.
- Экономия ≈ **187 строк/ход**; 0 always-apply редиректов; 0 висячих ссылок на удалённые файлы.

## Волна 2 — согласованность workflow (DONE)

### Единое имя отчёта verify
Канон: `reports/verification-YYYY-MM-DD.md` (фаза — в YAML `verify_mode`, не в имени). Убраны вариативные имена у потребителей:
- apply pre-flight: glob `verification-*.md` + чтение `verify_mode` (вместо `slice-pre`/`legacy-pre`/`legacy-mixed`).
- archive: glob `verification-*.md` + `verify_mode: post-apply` (вместо `slice-post-final`/`legacy-post`).
- status: тип «verification (pre-apply)»; vertical-slices: убран `verification-slice-S<N>-*`.
- Контрадикции в sdd-workflow, code-truth-gate, opsx-output-style §T-STATUS, opsx-status.md, пример chat-summary — приведены к `pre-apply`/`post-apply` и канону имени.

### Единая модель состояния
Фаза = `pre-apply` / `post-apply` (из `tasks.md`); приёмка среза = `awaiting-acceptance` (из `debug.md`). Убраны `slice-pre`/`slice-post`/`legacy mixed` как отдельные значения в status SKILL (стали «Фаза» + «Структура: срезы/legacy»).

### Один формат приёмки `S<N>.accept`
`openspec-continue-change` больше не генерирует legacy `S<N>.T<M>` — генерирует `S<N>.accept` с буллет-чеклистом (как ff). Inside-slice/fix-срез логика в continue переведена на `S<N>.accept`. Legacy `S<N>.T<M>` поддерживается только для ранее мигрированных ЗНИ.

### Handoffs
- `continue` при завершённых артефактах → **`Следующий шаг: /opsx:verify <name>`** (вместо «реализуй или архивируй»).
- `explore` Change Creation Gate и Handoff-таблица → явная **вилка**: быстро (`/opsx:ff`) vs пошагово (`/opsx:new` → `/opsx:continue`); алиас «создай ЗНИ» больше не выбирает путь молча.

## Волна 3 — стиль чата и брифы (DONE)

### Словарь запретов перестроен (две аудитории)
`chat-lexicon.md`: жёсткий бан — **только коды движка** (Слой 1: GO/NO-GO/PASS/FAIL/Layer N/snapshot/design-challenge/phantom-symbol/имена агентов и гейтов). Workflow-слова («срез», «постановка», «область задачи», имя процедуры, «что сломается») — **разрешены** разработчику (Слой 2). Снят прямой конфликт: раньше Слой 2 запрещал «срез», а `opsx-output-style §3.1b` объявлял его корректным термином. Англицизмы (Слой 3) — мягкое предпочтение. Аудитории: workflow-чат → разработчик 1С; полная расшифровка → документы заказчику и ТЗ.

### Снят конфликт No-Acknowledgement
`opsx-output-style §7 п.14` требовал «Понял: …» перед инструментами — прямо противоречил `chat-output-budget §4` (No Acknowledgement). Победил No Acknowledgement: п.14 переписан, «Понял:» убран и в verify-user-communication (перефраз выбора без префикса «Понял»).

### Дедуп правил чата
Chat Surface Contract — один SSOT (`opsx-output-style §2.6`); зеркало в `chat-output-budget §7` свёрнуто до ссылки. `§3.1` помечен как расширение к `chat-lexicon` (SSOT), убраны устаревшие строки `slice-pre`/`slice-post`/`slice-transition`.

### Единый бриф-скелет
В `opsx-output-style §5.1` — таблица единого каркаса: **От вас / Цель / План / На выходе / Ок?** (explore использует исследовательские названия тех же 5 слотов). Один лимит **8–12 строк (escape 14)** для всех (снят конфликт с «14–22» в §6-парах). Внутренние поля (список файлов, Drift-check, Behavior Contract, KB-discovery) **вынесены из чат-брифа** в файл/внутренний шаг — это была главная «каша» брифа extend. ff/new приведены к тому же каркасу (KB-discovery — внутренний шаг до брифа).

### Человеческая развилка
Шаблоны verify (`chat-summary` 3a-decision, `verdict-card`, `card-decision`, `conversation-shape`, пример §2.5): убран робот-стек «Что нужно от вас / Вопрос к вам / Ответьте в чате». Развилка = один заголовок **«Что решить»** + связный абзац (проблема и влияние сплетены) + A/B + одна строка «какой ближе». GO/terminal-варианты — без строки «Что нужно от вас».

## Волна 4 — восстановленные гарантии (DONE)

### Metadata Validation BSL-гейт (восстановлен из `3525165~1`)
Новый `.cursor/rules/1c-metadata-validation.mdc` (globs `**/*.bsl`, on-demand): имена объектов/типов/значений перечислений (`Перечисления.X.Y`, `Тип("СправочникСсылка.X")`, `Метаданные.<Kind>.<Name>`) проверять по выгрузке `src/` до использования; нет в выгрузке → STOP (опечатка или создание метаданных по `1c-no-metadata-creation.mdc`). Адаптирована секция SOURCE OF TRUTH под текущий фреймворк: гейт встроен в writer pipeline рядом с API EXISTENCE CHECK (раньше ссылался на удалённый openspec-debug). Прописан в `1c-writer-pipeline.mdc` (поток + строка про метаданные) и в `AGENTS.md`.

### Precedent/Regression-слой в verify (восстановлен из `e46d93a~1`, облегчённо)
Бывший «шаг 9b» вернулся как **Layer 2.4 Cross-Archive Regression Audit** в новой 5-слойной модели verify: механический скан архивных `ADDED` против текущих `MODIFIED`/`REMOVED`, invariant KB, Load-Bearing ADR; матрица severity (`precedent-regression`/`invariant-drift`/`load-bearing-adr-bypass` = CRITICAL → decision/NO-GO; `precedent-restructure`/`precedent-documented` = INFO; бюджет ≤10 архивов). Все ссылки «verify 9b» обновлены на «Layer 2.4» (`precedent-regression-gate.mdc`, `architect-gate.mdc`, `verified-cause-gate.mdc`, `openspec-archive-change`).

### Manual-config таблица-доказательство (Layer 5)
Шаг **5.1 Manual Configuration Sufficiency**: если `tasks.md` содержит маркеры ручной конфигурации, в `design.md` обязана быть дословная таблица (имена объектов, типы, элементы формы). Нет полной таблицы при наличии требования = `manual-config-incomplete` CRITICAL → NO-GO. Страховка от «apply встал, потому что неясно что создавать руками».

### gate-override expiry (Layer 4)
`.gate-override.yaml gate: design-challenge`: читается `timestamp`. ≤7 дней — пропуск с предупреждением и счётчиком «истекает через N дней»; **>7 дней — override игнорируется**, Layer 4 запускается, в info `gate-override-expired`. Убран молчаливый бессрочный обход независимого аудита.

### Опционально (облегчённо)
- Блок `## Для /opsx:ff` в explore: добавлено поле **«Срезы (черновик)»** (1–3 предполагаемых вертикальных среза подсказкой для ff) и развёрнут статус **«Architect / verify»** (да/нет + ссылка на отчёт архитектора).
- **Readiness Check** в explore Entry Protocol (§0.5): для слишком сырой постановки — один уточняющий вопрос до брифа, без выдумывания «Что вижу / Хочу понять»; при наличии симптома+области пропускается как non-event.

## Принятые по умолчанию решения (на ваше ревью)

- **Acknowledgement** — оставлен No Acknowledgement; «человечность» несёт сам бриф (перефраз задачи в строке «Что вижу»), отдельная строка «Понял:» убрана.
- **Словарь запретов** — жёсткий бан только на коды движка; повседневные workflow-слова и право называть процедуру/что сломается разрешены разработчику; строка «Источники:» сохраняется даже под лимитом.
- **Аудитории** — два режима явно: workflow-чат → разработчику 1С; полная расшифровка терминов → только пользовательские итоги и ТЗ.
- **Phantom-команды** — по умолчанию вычищены (migrate-acceptance, --from-verify-prompt, /help); `glossary.md` создан как дёшево-полезный.
- **Волна 4 опц.** — сделана облегчённо (slice-hints как подсказка, Readiness Check в один вопрос), без тяжёлого intake-подрежима.

## Что НЕ воскрешали (осознанно удалено ранее — оставлено удалённым)

MCP/admin-инструменты, генераторы форм из JSON (`onec-form-generator`), phase-gates как модель декомпозиции, hypothesis-gate. Эти удаления были корректными; план их не откатывает.

## Замер итога

- Always-apply правил: **4** (`1c-agent-delegation` 162, `chat-output-budget` 87, `session-discipline` 24, `gate-dispatcher` 23) + `AGENTS.md` 73. Было 12 always-apply (8 из них — пустые редиректы).
- 0 always-apply редиректов, 0 висячих ссылок на удалённые файлы и phantom-команды.
- Восстановлены исполняемые гарантии: метаданные (BSL-гейт), precedent/regression (Layer 2.4), manual-config доказательство (Layer 5.1), gate-override expiry (Layer 4).
