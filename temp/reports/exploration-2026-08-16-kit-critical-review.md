# Критичное ревью фреймворка 1C AI Development Kit — 2026-08-16

**Цель:** подготовка новой, более мощной, эффективной и экономичной версии фреймворка.
**Метод:** только чтение/анализ. Инвентарь размеров, аудит моделей, always-apply бюджета, структуры, противоречий.
**Актуальный enum `Task.model` (evidence оркестратора):** `inherit`, `claude-fable-5-thinking-high`, `claude-opus-5-thinking-high`, `composer-2.5-fast`, `cursor-grok-4.5-high`, `cursor-grok-4.6-xhigh`, `gemini-3.1-pro`, `gpt-5.6-sol-medium`.

---

## 1. Резюме

1. **Сломано сейчас:** Primary-модель архитектора `claude-opus-4-8-thinking-high` (и весь enum-пример в `model-selection.mdc`) невалидны в текущей сборке → каждый вызов архитектора начинается с `Invalid model selection` и уходит в fallback. Утверждение «`inherit` в enum нет» — теперь ложно.
2. **Постоянный контекст:** ~53,7 КБ (11 always-apply правил + AGENTS.md) грузится в каждый запрос; из них ~20 КБ — дублирование и кандидаты на on-demand (потенциал экономии ~35–40%).
3. **Битый SSOT:** `openspec/project.md` не существует в репозитории, при этом на него ссылаются **37 файлов** (~90 упоминаний), включая always-apply AGENTS.md и `1c-agent-delegation.mdc`.
4. **Gap:** нет никакой адаптации поведения kit под конкретную модель чата (профили, деградация, self-check enum).

---

## 2. Инвентарь

### 2.1. `.cursor/rules/*.mdc` — 41 файл, суммарно ≈ 415 КБ

Байты / строки (непустые) / статус загрузки:

| Файл | Байт | Строк | Загрузка |
|---|---|---|---|
| vertical-slices.mdc | 56 778 | 279 | on-demand |
| bsl-antipatterns.mdc | 45 043 | 147 | on-demand (reviewer-only) |
| knowledge-format.mdc | 38 200 | 354 | on-demand |
| chat-output-budget-full.mdc | 33 561 | 116 | on-demand |
| architect-gate.mdc | 26 010 | 139 | on-demand |
| 1c-writer-pipeline.mdc | 25 761 | 184 | globs `**/*.bsl` |
| **1c-agent-delegation.mdc** | **15 909** | 126 | **alwaysApply** |
| task-readability.mdc | 13 376 | 72 | on-demand |
| existing-mechanism-priority.mdc | 11 137 | 100 | on-demand |
| precedent-regression-gate.mdc | 10 838 | 64 | on-demand |
| forms-mxl-mode-gate.mdc | 10 317 | 87 | on-demand |
| tool-name-guard.mdc | 9 903 | 57 | on-demand |
| model-selection.mdc | 9 818 | 65 | on-demand |
| sdd-workflow.mdc | 9 423 | 61 | on-demand |
| adr-format.mdc | 7 799 | 86 | on-demand |
| verify-user-communication.mdc | 7 291 | 65 | on-demand |
| verified-cause-gate.mdc | 6 518 | 48 | on-demand |
| preserve-subagent-reports.mdc | 6 363 | 50 | on-demand |
| openspec-specs-gate.mdc | 5 773 | 46 | on-demand |
| **command-session-persistence.mdc** | **5 545** | 35 | **alwaysApply** |
| **chat-output-budget.mdc** | **5 232** | 46 | **alwaysApply** |
| 1c-halt-triggers.mdc | 5 177 | 49 | globs `**/*.bsl` |
| capture-to-project.mdc | 4 655 | 31 | on-demand |
| **1c-xml-write-guard.mdc** | **4 487** | 41 | **alwaysApply** |
| 1c-no-metadata-creation.mdc | 4 407 | 31 | on-demand |
| code-truth-gate.mdc | 4 137 | 51 | on-demand |
| **command-skill-gate.mdc** | **3 849** | 27 | **alwaysApply** |
| 1c-error-analysis.mdc | 3 311 | 22 | on-demand |
| **bsl-write-guard.mdc** | **2 890** | 25 | **alwaysApply** |
| **gate-dispatcher.mdc** | **2 693** | 31 | **alwaysApply** |
| **session-discipline.mdc** | **2 647** | 27 | **alwaysApply** |
| 1c-metadata-validation.mdc | 2 475 | 14 | on-demand |
| project-paths.mdc | 2 412 | 19 | on-demand |
| task-triage.mdc | 2 137 | 25 | globs |
| 1c-utility-agents.mdc | 1 828 | 18 | on-demand |
| **orchestrator-as-navigator.mdc** | **1 588** | 12 | **alwaysApply** |
| **conversational-discipline.mdc** | **1 492** | 15 | **alwaysApply** |
| no-roi-estimates.mdc | 1 452 | 18 | on-demand |
| **context-strategy-gate.mdc** | **1 323** | 20 | **alwaysApply** |
| openspec-sessions.mdc | 760 | 11 | on-demand (DEPRECATED) |
| 1c-coding-standards.mdc | 645 | 13 | globs `**/*.bsl` (loader) |

### 2.2. Always-apply бюджет (грузится в КАЖДЫЙ запрос)

| Компонент | Байт |
|---|---|
| 1c-agent-delegation.mdc | 15 909 |
| AGENTS.md | 6 085 |
| command-session-persistence.mdc | 5 545 |
| chat-output-budget.mdc | 5 232 |
| 1c-xml-write-guard.mdc | 4 487 |
| command-skill-gate.mdc | 3 849 |
| bsl-write-guard.mdc | 2 890 |
| gate-dispatcher.mdc | 2 693 |
| session-discipline.mdc | 2 647 |
| orchestrator-as-navigator.mdc | 1 588 |
| conversational-discipline.mdc | 1 492 |
| context-strategy-gate.mdc | 1 323 |
| **ИТОГО** | **53 740 Б (~54 КБ)** |

Оценочно **~12–16 тыс. токенов** постоянного контекста на каждый запрос (кириллица в UTF-8 токенизируется дорого). При правке `.bsl` добавляются globs-правила: `1c-writer-pipeline.mdc` (25,8 КБ) + `1c-halt-triggers.mdc` (5,2 КБ) + `1c-coding-standards.mdc` (0,6 КБ) — ещё ~31,6 КБ.

### 2.3. `.cursor/agents/*.md` — 7 агентов ≈ 223 КБ + CHANGELOG 17 КБ

| Агент | Байт | Оценка |
|---|---|---|
| onec-code-reviewer.md | 67 096 | **Раздут.** ~15–20 тыс. токенов системного промпта на каждый вызов reviewer, а reviewer вызывается чаще всех (каждая правка BSL, до 2 итераций) |
| onec-code-architect.md | 43 646 | Крупный; много режимов (design/task-readiness/design-challenge/slice-decomposition) в одном промпте |
| onec-code-writer.md | 38 432 | Крупный |
| onec-code-explorer.md | 30 264 | Приемлемо для роли |
| onec-trace-analyst.md | 22 647 | Приемлемо |
| CHANGELOG.md | 17 367 | **Рудимент в рантайм-каталоге** — истории версий не место в `.cursor/agents/` |
| onec-code-simplifier.md | 12 882 | ОК |
| openspec-quality-controller.md | 8 360 | ОК |

Frontmatter всех 7 агентов: `model: inherit` — **валидно** (соответствует SSOT-принципу model-selection).

### 2.4. `.cursor/commands/` — 22 команды (все < 6,3 КБ, тонкие обёртки — хорошо)

init-project, opsx-apply, opsx-archive, opsx-bulk-archive, **opsx-continue (alias-стаб)**, opsx-explain, opsx-explore, opsx-extend (6,2 КБ — самая большая), **opsx-ff (alias-стаб)**, opsx-knowledge-add/-audit/-init, opsx-new, opsx-overview, opsx-status, opsx-sync, opsx-verify, release-review, review, session-restore/-retro/-save.

### 2.5. `.cursor/skills/` — 42 SKILL.md ≈ 615 КБ

Топ по размеру: `openspec-apply-change` 68,7 КБ; `review` 61,6 КБ; `openspec-verify-change` 56,7 КБ; `openspec-new-change` 49,4 КБ; `openspec-extend-change` 45,5 КБ; `openspec-archive-change` 33,1 КБ; `openspec-explore` 31,7 КБ; `openspec-knowledge-add` 30,7 КБ. Все под порогом обрезки Read (~80 КБ; страховка в `command-skill-gate.mdc` уже описана), но apply/review близки к порогу и растут. Остальные 34 скилла — до 21 КБ, приемлемо.

---

## 3. Аудит моделей

### 3.1. Таблица: файл → слаг → валидность по актуальному enum

| Файл:строка | Слаг | Валиден |
|---|---|---|
| `.cursor/rules/model-selection.mdc:19,45` | `claude-opus-4-8-thinking-high` (Primary архитектора) | **НЕТ** |
| `.cursor/rules/model-selection.mdc:33` | `claude-4.6-sonnet-medium-thinking` | **НЕТ** |
| `.cursor/rules/model-selection.mdc:33` | `gpt-5.3-codex` | **НЕТ** |
| `.cursor/rules/model-selection.mdc:33` | `gpt-5.5-medium` | **НЕТ** |
| `.cursor/rules/model-selection.mdc:33` | `composer-2.5-fast` | да |
| `.cursor/rules/model-selection.mdc:22,23,33,46,58` | `gemini-3.1-pro` | да |
| `.cursor/rules/model-selection.mdc:35` | `default`, `claude-opus-4-7-thinking-xhigh`, `composer-2-fast` | упомянуты как «устаревшие, не использовать» — рудимент второго поколения |
| `.cursor/rules/model-selection.mdc:63` | «`model="inherit"` в enum обычно нет» | **ПРОТИВОРЕЧИЕ** — в актуальном enum `inherit` есть |
| `.cursor/rules/architect-gate.mdc:98` | `claude-opus-4-8-thinking-high` | **НЕТ** (дубль невалидного слага вне SSOT) |
| `.cursor/rules/tool-name-guard.mdc:25` | `composer-2`, `fast` | анти-примеры, допустимо |
| `.cursor/agents/CHANGELOG.md:66,72,79` | исторические слаги | не рантайм, допустимо |
| `.cursor/agents/*.md` frontmatter ×7 | `model: inherit` | да |

`openspec/project.md` — файл отсутствует (проверка невозможна); `AGENTS.md` — упоминаний слагов нет.

### 3.2. Фактическое поведение при текущем состоянии

- **Архитектор:** каждый вызов по цепочке начинается с невалидного Primary → гарантированный сбой `Invalid model selection` → переход на Fallback `gemini-3.1-pro`. Цепочка «случайно» работоспособна, но каждый вызов архитектора несёт мусорный failed-Task и шум в чате («одной строкой предупредить пользователя»).
- **Reviewer/simplifier:** `gemini-3.1-pro` валиден — работают штатно.
- **Writer/explorer/trace/QC:** без `model=` — работают штатно.
- **Не задействовано ни одной из новых моделей enum:** `claude-fable-5-thinking-high`, `claude-opus-5-thinking-high`, `cursor-grok-4.5-high`, `cursor-grok-4.6-xhigh`, `gpt-5.6-sol-medium` не упомянуты нигде в репозитории.

### 3.3. Системная проблема

`model-selection.mdc` заявлен как SSOT, но: (а) хардкодит enum-пример, который дрейфует с каждой сборкой Cursor; (б) невалидный слаг продублирован в `architect-gate.mdc:98` — при обновлении таблицы его легко забыть; (в) нет протокола самопроверки enum (оркестратор МОЖЕТ читать актуальный список слагов из описания инструмента Task в своей сессии — это нигде не используется).

---

## 4. Always-apply: дублирование и кандидаты на on-demand

### 4.1. Дубли внутри always-apply набора

**BSL write guard повторён минимум в 4 always-apply местах:**
1. `bsl-write-guard.mdc` — полное тело (2 890 Б);
2. `1c-agent-delegation.mdc` — § HALT CONDITIONS, § ТАБЛИЦА ДЕЛЕГИРОВАНИЯ, § WRITER PIPELINE (по сути тот же запрет + поток);
3. `session-discipline.mdc` — «Free-text entry… не править .bsl»;
4. `AGENTS.md` — «Карта SSOT: делегирование, BSL/XML write guard».
Плюс on-demand повторы: `1c-halt-triggers.mdc`, `1c-writer-pipeline.mdc`, `gate-dispatcher.mdc` (строка таблицы).

**XML write guard задублирован целиком:** `1c-agent-delegation.mdc` § XML WRITE GUARD — компактная версия, прямо говорящая «Полное тело guard — Read `1c-xml-write-guard.mdc`», т.е. полный файл спроектирован как on-demand, но его frontmatter `alwaysApply: true` — обе версии грузятся всегда. −4 487 Б при переводе полного тела в on-demand.

**Session-дисциплина существует в двух поколениях одновременно:** `session-discipline.mdc` (2 647 Б) в первой строке декларирует «Объединяет три аспекта: Command → Skill, Persistence, Context Strategy» — и при этом все три исходных файла (`command-skill-gate.mdc` 3 849 Б, `command-session-persistence.mdc` 5 545 Б, `context-strategy-gate.mdc` 1 323 Б) остались alwaysApply. Консолидация сделана, исходники не разжалованы. −до 10 717 Б (оставить консолидированный, детали трёх файлов — on-demand).

**Три стаба чат-стиля:** `conversational-discipline.mdc` (1 492 Б) и `orchestrator-as-navigator.mdc` (1 588 Б) — оба самоопределяются как «Runtime stub; полный контракт — chat-output-budget». Их содержимое (No Acknowledgement, роль навигатора, тишина) пересекается с самим `chat-output-budget.mdc` (5 232 Б). Слить два стаба в chat-output-budget → −~3 000 Б.

**`1c-agent-delegation.mdc` (15 909 Б) — самый тяжёлый файл набора.** Внутри: § WRITER PIPELINE — таблица шагов, дублирующая on-demand `1c-writer-pipeline.mdc`; § KB CONTEXT с форматом записи факта (нужен только при делегировании analytic-агентов — кандидат на on-demand); § АВТО-ИСПРАВЛЕНИЕ РЕВЬЮ с carve-out-политикой (нужна только в apply/review — уже есть в `review/SKILL.md`). Реалистично сжать до ~8–9 КБ, оставив триггеры и таблицу делегирования.

### 4.2. Итог потенциала экономии

| Мера | Экономия |
|---|---|
| `1c-xml-write-guard.mdc` → on-demand | −4,5 КБ |
| Убрать 3 файла, поглощённые session-discipline | −10,7 КБ |
| Слить 2 стаба в chat-output-budget | −3,0 КБ |
| Слить bsl-write-guard в delegation (1 якорь) | −2,0 КБ |
| Сжать 1c-agent-delegation (вынести KB CONTEXT, carve-out, дубль pipeline) | −6–7 КБ |
| **Итого** | **~20–22 КБ из 53,7 КБ (−37–40%)** |

Целевой always-apply бюджет новой версии: **~32–34 КБ** (≈8–10 тыс. токенов).

---

## 5. Структура: агенты, ссылки

### 5.1. Раздутые промпты агентов

- `onec-code-reviewer.md` 67 КБ — крупнейший потребитель токенов в workflow: вызывается после каждой правки BSL (плюс до 2 итераций цикла writer↔reviewer). Кандидат на декомпозицию: ядро протокола + on-demand чеклисты (часть уже вынесена в `.cursor/docs/standard/reviewer-checks.md` — но промпт всё равно 67 КБ, вероятно дублирование).
- `onec-code-architect.md` 43,6 КБ — все режимы (design, task-readiness, design-challenge, slice-decomposition, deep-analysis) в одном промпте; каждый вызов конкретного режима тащит инструкции всех остальных.
- `CHANGELOG.md` (17,4 КБ) лежит в `.cursor/agents/` — истории места в рантайм-каталоге нет (переместить в docs или корень).

### 5.2. Битые ссылки

**Главная: `openspec/project.md` не существует.** Ссылаются **37 файлов** (~90 упоминаний), в т.ч. always-apply `AGENTS.md` (5 упоминаний, включая живую markdown-ссылку и «Термины workflow — в openspec/project.md») и `1c-agent-delegation.mdc` § PROJECT PATHS («включать блок путей из openspec/project.md» — невыполнимо). По дизайну файл создаётся командой `/init-project` в целевом проекте — но kit-репозиторий сам является рабочим проектом (ЗНИ эволюции kit ведутся здесь, см. `kit-template-workflow.md`), и в нём SSOT путей и терминов повисает. Фактически термины лежат в `openspec/glossary.md` (существует), на который AGENTS.md не ссылается.

**Выборочная проверка 15+ cross-references из AGENTS.md и gate-dispatcher.mdc — все существуют:** все 9 gate-файлов из карты gate-dispatcher; `casebooks/README.md` + 8 кейсбуков; `chat-lexicon.md`, `opsx-output-style.md`, `brief-card.md`, `decision-block.md`, `marker-canon.md`, `kit-template-workflow.md`, `quick-start.md`, `faq-kit.md`, `delivery-integrity.md`, `review-guide.md`, `onec-infrastructure.md`; `openspec/specs/review-quality-disposition/spec.md`; `openspec/adrs/ADR-0003-*.md`; шаблоны `openspec-verify-change/templates/*` (10 шт., включая упомянутые в command-skill-gate), `openspec-new-change/templates/handoff-contract.md`, `openspec-explain/templates/*` (5 шт., включая entry-brief.md); `standard/std-01…12 + navigator + reviewer-checks`; `1c-agent-patterns/*` (8 файлов, включая sidecar.md). Гигиена ссылок в целом хорошая — кроме project.md.

---

## 6. Противоречия и рудименты

1. **`model-selection.mdc:63` vs реальность:** «`model="inherit"` в enum обычно нет» — в актуальном enum `inherit` присутствует. Инструкция «inherit достигается отсутствием model=» осталась рабочей, но обоснование ложно.
2. **`architect-gate.mdc:98`** дублирует конкретный слаг Primary вне SSOT — прямое нарушение собственного анти-паттерна model-selection («не дублировать таблицу без пометки о синхронизации»).
3. **`model-selection.mdc:35`** — «не использовать `default`, `claude-opus-4-7-thinking-xhigh`, `composer-2-fast`» — запреты на слаги, устаревшие два поколения назад; сами стали рудиментом.
4. **Legacy-алиасы команд:** `opsx-ff.md`, `opsx-continue.md` — стабы-редиректы; задокументированы в AGENTS.md как «устаревшие алиасы». В новой версии — удалить вместе со строкой в AGENTS.md.
5. **`openspec-sessions.mdc` (DEPRECATED):** стаб на 760 Б + упоминания `openspec/sessions/` в `chat-output-budget-full.mdc:100` и `session-discipline.mdc:20`. Каталога `openspec/sessions/` в репо нет. Если legacy read-only fallback (new/extend) больше не нужен — удалить весь слой.
6. **`vertical-slices.mdc` (56,8 КБ — крупнейший rule)** — заметная доля объёма ушла на legacy-совместимость: `S<N>.T<M>`, `--force-legacy`, `phase-gate`, «Фаза N», legacy acceptance (≥15 упоминаний legacy). Для новой версии — отрезать миграционный слой в отдельный migration-doc.
7. **`forms-mxl-mode-gate.mdc` / `1c-xml-write-guard.mdc`** — legacy `artifact_mode` поддерживается в 4+ местах; тот же кандидат на отрезание при мажорной версии.
8. **AGENTS.md vs факт:** «Термины workflow — в `openspec/project.md`» — файла нет, термины в `openspec/glossary.md`; ссылка битая в каждом запросе (AGENTS.md always-apply).
9. **`.cursor/agents/CHANGELOG.md:72,79`** упоминает агента `openspec-doc-writer`, которого в каталоге нет — допустимо для истории, но подтверждает, что CHANGELOG вводит в заблуждение при чтении каталога агентов.
10. **GAP — адаптация под модель чата: отсутствует полностью.** Grep по паттернам «модель чата / адаптация / profile» находит только правила выбора моделей СУБАГЕНТОВ (`model-selection.mdc`, `architect-gate.mdc`, `tool-name-guard.mdc`). Нет: (а) профилей «экономичный / качественный» для сессии; (б) правил деградации протокола, если чат ведёт слабая/быстрая модель (стоило бы, например, принудительно пиннить сильную модель архитектору и reviewer, если чат — composer/fast); (в) инструкции сверять фактический enum Task в начале сессии; (г) различий бюджета вывода/чтения для дешёвых и дорогих моделей.

---

## 7. Выводы и предложения

### (а) Критично — сломано сейчас

| # | Проблема | Действие |
|---|---|---|
| A1 | `model-selection.mdc:19,45` — Primary архитектора `claude-opus-4-8-thinking-high` невалиден | Заменить на `claude-opus-5-thinking-high` (ближайший преемник по классу); Fallback оставить `gemini-3.1-pro` |
| A2 | `model-selection.mdc:33` — enum-пример из 4/6 мёртвых слагов | Заменить актуальным списком ИЛИ (лучше) убрать хардкод: инструкция «актуальный enum — в описании инструмента Task текущей сессии; сверять перед первым вызовом» |
| A3 | `model-selection.mdc:63` — ложное «inherit в enum нет» | Переписать: `inherit` допустим и в enum, и через отсутствие `model=` |
| A4 | `architect-gate.mdc:98` — дубль мёртвого слага вне SSOT | Убрать слаг, оставить ссылку «цепочка — model-selection.mdc» |
| A5 | AGENTS.md → `openspec/project.md` (нет файла) | Поставить в kit-репо стартовый project.md (или переключить ссылку терминов на `openspec/glossary.md` + пометку «project.md создаётся /init-project») |

### (б) Экономия — сокращение постоянного контекста и токенов

| # | Мера | Эффект |
|---|---|---|
| Б1 | `1c-xml-write-guard.mdc` → `alwaysApply: false` (компакт-версия уже есть в delegation) | −4,5 КБ/запрос |
| Б2 | Удалить из always-apply `command-skill-gate`, `command-session-persistence`, `context-strategy-gate` (консолидированы в `session-discipline.mdc`; детали — on-demand) | −10,7 КБ/запрос |
| Б3 | Слить `conversational-discipline` + `orchestrator-as-navigator` в `chat-output-budget.mdc` | −3 КБ/запрос |
| Б4 | Слить `bsl-write-guard.mdc` в `1c-agent-delegation.mdc` (один якорь запрета) | −2 КБ/запрос |
| Б5 | Сжать `1c-agent-delegation.mdc`: § KB CONTEXT, § АВТО-ИСПРАВЛЕНИЕ (carve-out), дубль WRITER PIPELINE → on-demand | −6–7 КБ/запрос |
| Б6 | Итого always-apply: 53,7 → ~32–34 КБ | **−37–40% постоянного контекста** |
| Б7 | Диета `onec-code-reviewer.md` (67 КБ) — ядро + on-demand чеклисты | крупнейшая экономия на самом частом Task |
| Б8 | Разрезать `onec-code-architect.md` (43,6 КБ) по режимам (sidecar-файлы per-mode) | экономия на каждом вызове архитектора |
| Б9 | Убрать `CHANGELOG.md` из `.cursor/agents/`, alias-стабы `opsx-ff`/`opsx-continue`, `openspec-sessions.mdc` | гигиена поставки |
| Б10 | Отрезать legacy-слои (`S<N>.T<M>`, phase-gate, `artifact_mode`) из `vertical-slices.mdc` (56,8 КБ) и forms-gate в migration-doc | −15–20 КБ on-demand объёма |

### (в) Усиление — где добавить мощности

| # | Предложение |
|---|---|
| В1 | **Обновлённая таблица ролей под новый enum:** architect → `claude-opus-5-thinking-high`; reviewer → `gemini-3.1-pro` (или `cursor-grok-4.6-xhigh` как вариант для release-review); simplifier/mechanical-проверки → `composer-2.5-fast` (дёшево и достаточно); writer/explorer — inherit как сейчас |
| В2 | **Self-healing enum:** правило для оркестратора — актуальный список слагов читать из описания инструмента Task своей сборки; при несовпадении с таблицей model-selection — использовать fallback-цепочку и предложить обновить таблицу. Убирает главный источник поломок при апдейтах Cursor |
| В3 | **Профили сессии (economy / quality):** явный переключатель в project.md или команде — в economy-профиле explorer/simplifier на `composer-2.5-fast`, сокращённые превью в чат; в quality-профиле — пиннинг сильных моделей на architect/reviewer |
| В4 | **Адаптация под модель чата:** если чат ведёт быстрая/дешёвая модель — обязательный пиннинг сильной модели для architect и reviewer (не inherit); если чат ведёт топ-модель — writer/explorer могут работать на inherit без потерь. Сейчас поведение kit никак не зависит от модели чата — зафиксированный gap |
| В5 | **Бюджетный мониторинг:** в /session-retro добавить строку «сколько КБ always-apply + globs грузилось» — чтобы дрейф бюджета был виден при эволюции kit |

---

## Приложение: цифры одной строкой

- Rules: 41 файл, ~415 КБ; из них always-apply 11 файлов + AGENTS.md = **53,7 КБ/запрос** (~12–16 тыс. токенов); при `.bsl` ещё +31,6 КБ globs.
- Agents: 7 промптов, 223 КБ (reviewer 67 КБ — max) + рудимент CHANGELOG 17 КБ.
- Commands: 22, все тонкие (≤6,3 КБ), 2 legacy-стаба.
- Skills: 42 SKILL.md, ~615 КБ; максимум apply 68,7 КБ (под порогом обрезки 80 КБ).
- Невалидных слагов моделей: 4 уникальных в 2 рантайм-файлах (6 строк); валидных из нового enum задействовано 2 из 8.
- Битых ссылок: 1 системная (`openspec/project.md`, 37 файлов) + 1 смысловая (термины ≠ glossary); остальные 15+ проверенных cross-refs целы.
