# AGENTS.md — BSL Code Gate (навигационный индекс)

**Главный диспетчер:** `.cursor/rules/1c-agent-delegation.mdc` — HALT-условия + делегирование агентам.

## OpenSpec Workflow
`.cursor/rules/sdd-workflow.mdc` — explore → new/ff → verify → apply → verify → archive.
Команды: `/opsx:explore` (точка входа по умолчанию; свободный текст = explore), `/opsx:new`, `/opsx:ff`, `/opsx:apply`, `/opsx:verify`, `/opsx:archive`, `/opsx:estimate`, `/prerelease-review`, `/review`, `/opsx:status`, `/opsx:extend`, `/opsx:migrate-slices`, `/opsx:knowledge-add`.
`/review` — ревью по контексту запроса (модуль/файлы/расширение/ЗНИ) с опцией устранения замечаний; скилл `.cursor/skills/review/SKILL.md`. **Review Focus Boundaries:** без аргументов — scope по изменённым `.bsl` в git (`diff-focused`, границы по процедурам из diff); явный файл/каталог/расширение — полное ревью (`full`); ЗНИ — `diff-focused` по `tasks.md` `[x]` + git diff и маппинг на процедуры; в промпт ревьювера передаётся `## Review Boundaries` (протокол в `.cursor/agents/onec-code-reviewer.md`).
Дополнительные: `/opsx:continue`, `/opsx:sync`, `/opsx:bulk-archive`, `/init-project`.
Паттерны агентов: `.cursor/skills/1c-agent-patterns/SKILL.md`.
Документы: `/opsx:doc-tz <name>` (ТЗ по ЗНИ с архитектурным ревью и контролем качества артефактов) — `.cursor/skills/openspec-docs/SKILL.md`. Шаблон: `.cursor/skills/openspec-docs/prompts/change-tz.md`.

**Output style (единый стиль выводов opsx):** `.cursor/docs/opsx-output-style.md` — 3 слоя (UX / код / процесс), типография, запрет внутренних ID (`S<N>.T<M>`, `D<N>`, `R<N>`, номера задач) в пользовательских полях, запрет жаргона движка (`Blast Radius`, `precedent-regression`, `Phase A/B`, `verdict:`, `verify_mode:`, `Tier`, `Standard / Lite / Full`, `когерентность`, `low-confidence`, `capability`, `checkpoint`, `step-by-step` — см. §3.1; вместо `Tier` — «Объём», вместо «когерентность» — «согласованность»), запрет имён агентов (`onec-code-*`, `openspec-*`) и гейтов (`Architect Gate`, `Slice Gate`, `Implementation Impact Gate`, `Code-Truth Gate`, `Precedent Regression Gate`) в чате — заменяются на «агент / архитектор / ревьюер / оркестратор» и описание результата проверки соответственно, полные имена остаются только в строке «Источники: …» и в файлах отчётов `reports/`. **Non-events в чат не выводятся** — §3a `.cursor/rules/chat-output-budget.mdc`. Запрет голого `S<N>` без названия среза (правило §10 «Срез всегда с названием»); первое упоминание задачи `S<N>.<M>` / `S<N>.T<M>` в заголовке — с коротким описанием в «ёлочках» (§10.1). T-HANDOFF «Следующие задачи» — обязательная колонка «Действие»; «Тип» / «Исполнитель» — только из русских наборов (§5.2). Дисциплина правок ЗНИ (§8: decision → `/opsx:extend`, hygiene → ручная правка с обязательным повторным verify), 5 внутренних макетов сообщений (имена для авторов скиллов; в сообщения пользователю не цитируются — см. §5 и §9). Перед каждым пользовательским выводом opsx-скилл обязан проходить self-check (§7 гайда), включая «канонический переход» (п.6), «срез всегда с названием» (п.9), HALT жаргона и **бюджет чата** (п.10–13, плюс always-apply `.cursor/rules/chat-output-budget.mdc`), для verify — «Суть» в **файле** отчёта и тонкий чат по умолчанию (п.11, флаг `--verbose`). Роль оркестратора — навигатор: `.cursor/rules/orchestrator-as-navigator.mdc`.

### Decision tree команд

Краткая навигация — какую команду использовать. Полный глоссарий: `openspec/glossary.md`.

| Задача пользователя | Команда | Чем отличается от соседних |
|---------------------|---------|----------------------------|
| Любой вопрос, дефект, постановка (в т.ч. свободный текст) | `/opsx:explore` | Единая точка входа; компактный бриф 8–12 строк; итог — блок `## Для /opsx:ff` **в чате**; опциональный handoff `temp/explore-handoff-*.md` по словесной просьбе; профиль bug обогащает бриф трассой/PERF |
| «Обсудить идею, пока change нет» | `/opsx:explore` | Диалог в чате без `openspec/sessions/`; полные отчёты `Task` — `temp/reports/`; не writer/reviewer; capture → `/opsx:ff` (берёт блок из чата) или `/opsx:extend --from-report <temp/reports/...>` |
| «Создать новый change пошагово» | `/opsx:new <name>` | Пошаговая последовательность артефактов |
| «Создать change целиком разом» | `/opsx:ff <name>` | Все артефакты сразу, для уже понятной задачи |
| «Быстро понять, где я в этом change» | `/opsx:status <name>` | Read-only снимок, без верификаций и субагентов |
| «Проверить артефакты до реализации, могу ли запустить apply» | `/opsx:verify <name>` | Бинарный вердикт GO/NO-GO в первой строке; пять слоёв (гигиена, согласованность, Why→Solution, независимый аудит, реализуемость); не модифицирует артефакты |
| «Добавить новое требование в существующий change» | `/opsx:extend <name>` | Контролируемо обновляет proposal/specs/tasks; начинает с брифа и verify-handoff |
| «Учесть отчёт ревью / архитектора в существующем change» | `/opsx:extend <name> --from-review <path>` / `--from-architecture <path>` | Анализирует файл-источник, классифицирует findings, при необходимости запускает Architect Gate и обновляет артефакты ЗНИ |
| «Код упростили вручную, артефакты отстали от факта» | `/opsx:extend <name> --code-sync` | Code-Truth sync: explorer читает фактический код, затем design/tasks/spec/debug догоняют выгрузку |
| «Добавить одну задачу / создать следующий артефакт» | `/opsx:continue <name>` | Пошаговое продолжение, без большого расширения scope |
| «Мигрировать старый tasks.md (plain/phase) в срезы» | `/opsx:migrate-slices <name>` | Architect restructuring + подтверждение diff |
| «Реализовать задачи» | `/opsx:apply <name>` | Делегирует writer/reviewer; slice-gate paused |
| «Разобрать дефект, обновить план» | `/opsx:explore` → `/opsx:extend <name> --from-report` | Исследование (профиль bug) → блок `## Для /opsx:ff` в чате / `temp/reports/*.md` / `temp/explore-handoff-*.md` → capture fix-задач в change |
| «Сгенерировать ТЗ по ЗНИ» | `/opsx:doc-tz <name>` | ТЗ отдельно от verify (verify генерирует как часть gate при пороге) |
| «Финальная проверка перед релизом» | `/prerelease-review` | Tier 1 + Tier 2 расширения или change scope |
| «Ревью кода» | `/review` | Без change — по git diff; с аргументом — по файлу/модулю/расширению/ЗНИ |
| «Оценить трудозатраты» | `/opsx:estimate <name>` | PERT по tasks.md |
| «Архивировать завершённый change» | `/opsx:archive <name>` | В slice mode при `[ ]` на `S<N>.T<M>` — AskQuestion: подтвердить приёмку и отметить `[x]` (если все рабочие задачи среза закрыты), отложить, или **`--force-legacy`** |
| «Зафиксировать verified-факты из отчёта/файлов вне ЗНИ» | `/opsx:knowledge-add <path>` | Не требует ЗНИ; bundle source + KB-карточка |

## Conversational Discipline
`.cursor/rules/conversational-discipline.mdc` — 5 принципов осознанного диалога: Acknowledgement Layer, Adaptive Brief (entry-бриф в чат по §5.1 `opsx-output-style.md`), Risk Surfacing, Honest Subagent Handling, Progress Marker. Приоритет над длинными отчётами скиллов. Карта SSOT (лимиты, шаблоны, запреты) — в `.cursor/rules/chat-output-budget.mdc` §1a. Шаблоны вывода — в `.cursor/docs/opsx-output-style.md` и `templates/` соответствующих скиллов.

## Глоссарий
`openspec/glossary.md` — единый словарь ключевых терминов (ЗНИ, срез, slice-gate, tier, режимы verify, acceptance handoff и др.). Использовать для сверки терминологии в артефактах, отчётах и сообщениях пользователю.

## Фиксация договорённостей
`.cursor/rules/capture-to-project.mdc` — «зафиксируй в проекте» → Read `openspec/project.md` → адаптация под формат секции → подтверждение → запись.

## Маркеры разработчика
Секция в `openspec/project.md`; метаданные — в `proposal.md` (Metadata); размещение — `onec-code-writer.md`; проверка пар — reviewer/prerelease/archive, scope = diff по zni_id.

## BSL write guard
`.cursor/rules/bsl-write-guard.mdc` — глобальный инвариант: правка .bsl только через onec-code-writer + обязательный onec-code-reviewer (любой диалог). `.cursor/rules/1c-agent-delegation.mdc` — детальная диспетчеризация: APPLY GATE, DELEGATION GATE, LINT GATE, API CHECK, EXTENSION GATE.

## Пути к выгрузке
Базовая конфигурация и расширения заданы в `openspec/project.md` (секция «Структура репозитория»). При поиске кода в src/ и проверке выгрузки использовать эти пути; не предполагать `src/cf/` и `src/cfe/`. См. `.cursor/rules/project-paths.mdc`.

## Code reviewer (onec-code-reviewer)
`.cursor/agents/onec-code-reviewer.md` — ревью кода BSL. **Приоритет рассуждения над каталогом:** сначала Phase 0 (Intent & Reasoning Analysis) — артефакты Intent Map, Contract Map, Knowledge Assessment; замечания по логике (DISPROPORTIONATE_COMPLEXITY, CONTRACT_INCONSISTENCY, CONTRACT_INFERENCE, KNOWLEDGE_DEFICIT, CLARITY_DEFICIT, AUTHORITY_MISPLACEMENT). Каталог антипаттернов (AP-NNN) — вспомогательный шаг. **AP-040 (release-hygiene):** kebab-case имена change и пути к артефактам OpenSpec (`reports/…`, `openspec/…`, сноски `(см. …)` с `.md`) в комментариях и **JSDoc** над процедурами — MUST_FIX; пары `// +++`/`// ---` из whitelist `openspec/project.md` не флагать как AP-040. Мета-имена (постановка вместо домена): AP-031. Локальная подмена владельца поведения вместо делегирования: AUTHORITY_MISPLACEMENT + AP-047. Отчёт: секция Reasoning Analysis (Phase 0), затем Standards & Patterns. **Формат замечаний:** каждое замечание содержит стабильные якоря (Procedure, Anchor — для поиска после правок) и поле Action (MUST_FIX / VERIFIED_OK / OPTIONAL); при устранении через /review writer получает только MUST_FIX. **Investigation Request:** ревьювер может запросить резолв контрактов через секцию `## Investigation Request` в отчёте (Phase 2.5 шаг D); оркестратор делегирует explorer и перезапускает ревью с Resolved Contracts (шаг 3.5 review/SKILL.md). **Resolved Contracts (артифакт ЗНИ):** результат investigation loop сохраняется в `reports/resolved-contract-<scope-slug>-YYYY-MM-DD.md`. Содержит верифицированные контракты (тип, ключи, fixed/dynamic, Evidence). Передаётся writer при review-fix и reviewer при повторном ревью. Writer и reviewer знают формат и правила использования (см. агентские промпты). При отсутствии блока в промпте reviewer проверяет `reports/resolved-contract-*.md` по change (fallback). **Принцип «Уточни, не защищайся»:** Свойство()/ТипЗнч() при невыясненном контракте без попытки резолва = AP-004 (компенсация незнания). Writer обязан сначала установить контракт; reviewer проверяет наличие обоснования. См. `.cursor/docs/1c-coding-standards.md` и раздел AP-004 в `.cursor/docs/antipatterns/bsl-antipatterns.md`. **Unverified API:** информационная секция в отчёте — вызовы, определение которых не найдено в src/.

## API Existence Check
`.cursor/rules/1c-agent-delegation.mdc` (секция API EXISTENCE CHECK) — проверка существования вызываемых методов общих модулей в src/ (cf + cfe) после writer, до reviewer. AskQuestion при ненайденном методе.

## XML write guard
`.cursor/rules/1c-xml-write-guard.mdc` — запрет прямой записи/генерации Form.xml, Template.xml, Rights.xml и прочих XML в src/. Form.xml → инструкция ручного конфигурирования или программное создание элементов в BSL модуля формы; read-only навыки `1c-forms/info` и `1c-forms/validate` допустимы для анализа выгрузки. Template.xml, Rights.xml — через скиллы 1c-mxl, 1c-roles.

## Tool Name Guard
`.cursor/rules/tool-name-guard.mdc` — для вызова субагентов использовать инструмент **Task**. При `Invalid enum value` проверить имя инструмента (должен быть Task) и subagent_type; не переключаться на generalPurpose.

## Запрет создания метаданных
`.cursor/rules/1c-no-metadata-creation.mdc` — СТОП, блокер пользователю.

## Анализ ошибок 1С
`.cursor/rules/1c-error-analysis.mdc` — trace-analyst → explorer/architect.

## Architect Gate
`.cursor/rules/architect-gate.mdc` — единые триггеры архитектурного ревью (объективные маркеры, семантические, структурные). **UX-значимый фикс** (меняет что видит/делает пользователь) — семантический триггер; локальная реализация поведения, владельцем которого является база/БСП/платформа/общий модуль, вместо делегирования владельцу — семантический триггер Substituted Authority. **Simplicity Check:** каждый architecture-отчёт фиксирует простейший viable design, альтернативы и complexity budget; отсутствие секции ловит verify. **Explore (профиль bug):** при срабатывании триггеров architect обязателен в маршруте (не AskQuestion с пропуском), шаблон «Architect — fix quality review» в `1c-agent-patterns/architect.md`. Проверяется в explore, verify (pre-apply, шаг 9 + fix check по задачам из debug.md), apply (soft redirect на verify).

## Verify (независимое согласование перед apply)
`.cursor/skills/openspec-verify-change/SKILL.md` — `/opsx:verify [<name>]`. Главный вопрос пользователя: «**могу ли я безопасно запустить apply?**» Ответ — **бинарный** (`GO` / `NO-GO`) в первой строке чата (`templates/verdict-card.md`). Аргумент команды — только имя ЗНИ (или одна активная); режим (`pre-apply` / `post-apply`) и узкий охват выводятся из артефактов, дат изменения и свободной формы запроса — без флагов CLI.

**Пять слоёв проверки** (порядок строгий):
1. **Гигиена артефактов** — авто-исправление мелких дефектов формы, без вопросов пользователю.
2. **Внутренняя согласованность** — Quality Controller (Slice Coherence + Acceptance Checklist Coverage) + Code-Truth (механический поиск phantom-symbol) + Spec ↔ Tasks ↔ Design coverage.
3. **Problem-Solution Trace** — Why → Requirements → Scenarios → Slices → Tasks/Acceptance: каждый уровень ссылается на предыдущий без orphan-узлов.
4. **Independent Challenge** — `onec-code-architect` в режиме `design-challenge` (адверсариальный аудит «решает ли это Why оптимально»). Запускается на **первом** pre-apply прогоне ЗНИ или при `mtime(design.md) > snapshot.last_challenge_at` (после `/opsx:extend`). Вердикт `APPROVE` / `CHALLENGE` / `REJECT` маппится на статус слоя.
5. **Implementation Readiness** — `onec-code-architect` в режиме `task-readiness`: задачи реализуемы as-is, чеклист `S<N>.accept` выполним, нет «фикса симптома».

**Бинарный вердикт:**
- `GO` — все слои в `PASS / WARNING / AUTOFIXED / APPROVE / SKIPPED-novelty`.
- `NO-GO` — любой `FAIL` в Layer 2/3/5 либо `CHALLENGE` / `REJECT` в Layer 4.

**Вывод пользователю:** первая строка — вердикт по `templates/verdict-card.md`. Далее — `templates/chat-summary.md`: «тихий» вариант для `silent_ok` (нет новизны после фильтра — новый файл отчёта не создаётся) или «информативный» с блоками «Что нашли», «Сама поправила», «Что обсудим» (только при NO-GO, разговорный блок прозой), «По плану». Запрещены имена слоёв, `verdict:`, `PASS/FAIL`, коды выбора `<N>a` (см. `chat-output-budget.mdc` §7).

**Snapshot и фильтр новизны:** YAML отчёта содержит `accepted_tasks`, `artifacts_mtime` каждого артефакта, `last_challenge_at`. Если все три не изменились с прошлого запуска — путь `silent_ok` без слоёв и без нового файла.

**Что verify НЕ делает:** не правит артефакты (только Layer 1 — авто-гигиена); не генерирует ТЗ (это `/opsx:doc-tz`); не мигрирует приёмку из `S<N>.T<M>` в `S<N>.accept` (отдельная команда `/opsx:migrate-acceptance` — в плане); не выполняет apply.

**Scope Gate:** verify не расширяет scope сам. Если в запросе помимо команды есть новое требование — AskQuestion: дополнить артефакты через `/opsx:extend --from-verify-prompt`, запустить as-is, или зафиксировать TODO в отчёте.

**Legacy compat (acceptance):** активные ЗНИ с `S<N>.T<M>` без `S<N>.accept` обрабатываются без падений; QC выдаёт `legacy-acceptance-format` (SUGGESTION с предложением `/opsx:migrate-acceptance <name>`); Layer 3 ищет Scenario либо в чеклисте `S<N>.accept`, либо в legacy `S<N>.T<M>` через хвостовую скобку `(Scenario: «…»)`.

**Делегирование:** Layer 2 — `openspec-quality-controller` (Task без `model=`). Layer 4 — `onec-code-architect` mode=`design-challenge` по цепочке моделей `model-selection.mdc`. Layer 5 — `onec-code-architect` mode=`task-readiness` по той же цепочке.

Коммуникация с пользователем: `.cursor/rules/verify-user-communication.mdc` (бинарный вердикт + 5 слоёв + правила «Что обсудим»). Полный SKILL — `.cursor/skills/openspec-verify-change/SKILL.md`. Шаблоны — `openspec-verify-change/templates/`. Бюджет чата — `.cursor/rules/chat-output-budget.mdc` §1.

## Behavior vs Implementation и Code-Truth
`design.md` для UX/UI/интеграций разделяет **Behavior Contract** (наблюдаемое поведение и инварианты) и **Implementation Options** (варианты реализации и выбранный простейший viable design). `tasks.md` формулируется через результат; конкретные новые имена процедур — только verified, публичный контракт или явно «например».
`.cursor/rules/code-truth-gate.mdc` — механический gate после apply/verify/archive: технические имена из `design.md`, `tasks.md`, `debug.md`, `specs/**` должны существовать в коде либо быть помечены как примеры. `phantom-symbol` в принятом срезе блокирует archive; штатное исправление — `/opsx:extend <name> --code-sync`.

## Verified Cause Gate
`.cursor/rules/verified-cause-gate.mdc` — root cause + impact перед фиксом. Масштаб: точечный (не меняет UX) / **UX-значимый** (меняет сценарий пользователя) / системный; UX-значимый и системный → architect обязателен. Fix Quality Gate: анти-паттерн «фикс симптома»; verify шаг 7.7 — критерий 6 (качество фиксов), шаг 9 — Debug fix check (задачи из debug без architecture-*.md → CRITICAL).

## Приоритет существующих механизмов
`.cursor/rules/existing-mechanism-priority.mdc` — Preference Hierarchy, Mandatory Discovery, anti-patterns. Срабатывает при создании нового объекта или интеграции с базой. Обязательная секция Existing Mechanisms в design.md / architecture-отчёте. Substituted Authority — локальная подмена владельца поведения вместо делегирования (второй источник истины) — запрещена без обоснования уровня 4.

## Quality Controller (OpenSpec)
`.cursor/agents/openspec-quality-controller.md` — домен-агностичный readonly-агент для Slice Coherence (включая Acceptance Checklist Coverage 5b). Вызов `Task` **без** `model=` (наследование чата; см. `.cursor/rules/model-selection.mdc`). Критерии — в `vertical-slices.mdc`; вызывается из `/opsx:verify` Layer 2.

## Session Handoff и Step-by-step mode
`.cursor/skills/openspec-apply-change/SKILL.md` (шаги 5.6, 6, 7) — Session Handoff Summary (три секции: код / действия пользователя / следующие задачи), Step-by-step mode (пауза после каждой задачи с подтверждением, обработка ручных тестов с ожиданием результата). Триггеры step-by-step: явный запрос; debug-сессия (`debug.md` изменялся сегодня); slice-mode с ожидающим приёмочным тестом (`S<N>.T<M>`) в текущей пачке; fix-срез (`S<N>.fix`); размер среза ≥ 5 задач.

## Сохранение отчётов субагентов
`.cursor/rules/preserve-subagent-reports.mdc` — полные отчёты в reports/.

## Утилитарные агенты
`.cursor/rules/1c-utility-agents.mdc` — инструкции по формам (Form.xml), запросы, тесты, упрощение, метаданные, администрирование. Загружается по необходимости (не always-apply).

## Предрелизное ревью
`.cursor/skills/prerelease-review/SKILL.md` — `/opsx:prerelease-review`. В режиме **`change-scoped`** Tier 1 использует **Review Boundaries** (diff-focused по изменённым процедурам, шаг 1.3b скилла); механические проверки 1.7/1.7b фильтруют совпадения по строкам границ; Tier 2 — по-прежнему всё расширение.

## Стандарты вендора 1С
`.cursor/skills/1c-vendor-standards/SKILL.md` — чеклисты для architect/reviewer.

## Delta Specs Gate
`.cursor/rules/openspec-specs-gate.mdc` — полнота артефакта specs.

## Command → Skill Read Gate
`.cursor/rules/command-skill-gate.mdc` — сначала Read скилла, потом файлы.

## Command Session Persistence
`.cursor/rules/command-session-persistence.mdc` — протокол команды действует на каждом ходе сессии, не только на первом.

## Architecture Decision Records (ADR)
`openspec/adrs/` — постоянное хранилище архитектурных решений проекта.
`.cursor/rules/adr-format.mdc` — формат, именование, критерии, жизненный цикл.
Индекс: `openspec/adrs/README.md`. Создаются при archive (шаг 5), обнаруживаются при explore/ff/new (ADR Discovery).
Интеграция: `architect-gate.mdc` (ADR Discovery при срабатывании), `1c-agent-patterns/architect.md` (шаблон extraction).

## Knowledge Base
`openspec/knowledge/` — структурированная база знаний с механизмом read-repair.
`.cursor/rules/knowledge-format.mdc` — структура KB-файла, anchor spec, статусы, TTL.
Индекс: `openspec/knowledge/_index.yaml`. Создаются при archive (шаг 5.5), `/opsx:knowledge-add` и audit.
Интеграция: `/opsx:explore` (Knowledge Discovery), `architect-gate.mdc` (Knowledge Discovery), `/opsx:knowledge-add` (standalone capture из reports/markdown вне ЗНИ), `/opsx:knowledge-audit` (сверка и обновление), `/opsx:knowledge-init` (bootstrap таксономии).

## Оценка трудозатрат
`.cursor/skills/openspec-estimate/SKILL.md` — `/opsx:estimate <name>`. Трёхточечная PERT-оценка по tasks.md. Авторежимы: первичная оценка / переоценка / калибровка по факту. Ставки встроены в скилл, опциональный оверрайд — `openspec/estimate-rates.md`.

## Стратегия анализа файлов
`.cursor/skills/context-strategy/SKILL.md` — планирование: прямое чтение vs субагенты.
`.cursor/rules/context-strategy-gate.mdc` — триггер при 3+ файлах, данных, крупных модулях.

## Стандарты BSL
`.cursor/docs/1c-coding-standards.md` — стандарты кода 1С/BSL. `.cursor/rules/1c-coding-standards.mdc` — только thin loader по `**/*.bsl`, без полного тела стандартов.

## Реестр антипаттернов BSL
`.cursor/rules/bsl-antipatterns.mdc` — краткий индекс (AP-NNN ID, detection rule, severity). **Reviewer-only** (`alwaysApply: false`, без `globs`), не загружается для writer. Writer не должен видеть антипаттерны — они могут быть неверно интерпретированы как паттерны.
`.cursor/docs/antipatterns/bsl-antipatterns.md` — полные карточки с примерами BAD/GOOD, ссылками на стандарты.
Пополняется из `/opsx:explore` (профиль bug, секция отчёта) по подтверждению пользователя.
Ревьювер читает индекс динамически (Phase 2, step 16 в `onec-code-reviewer.md`). Новые AP подхватываются автоматически без правки агентских промптов. AP-047 — обобщённая карточка Substituted Authority: локальная реализация поведения, у которого есть владелец (база/БСП/платформа/общий модуль), вместо делегирования владельцу.

## Словарь лексики ТЗ
`.cursor/docs/tz-lexicon-dictionary.md` — запрещённые слова (англицизмы, жаргон, опечатки) с заменами и Grep-паттернами. Единый источник для генерации (`change-tz.md`, п.2 и п.11), ревью архитектора (`1c-agent-patterns/architect.md`, секция «Architect — ТЗ quality review», пункт 6), механической проверки (`verify`, шаги 7.8 и 11). Пополняется из `/opsx:doc-tz` (ревью архитектора → предложение → подтверждение пользователя).

## Выбор модели
`.cursor/rules/model-selection.mdc` — SSOT: таблица `Task.model` по ролям; во frontmatter агентов `inherit`; детали и fallback — в правиле и в `tool-name-guard.mdc`. Полная цепочка fallback (включая финальный вызов `Task` без `model=`) и запрет подмены аналитического отчёта текстом оркестратора — раздел **«Целостность цепочки Task»** в том же файле; протокол сбоя субагента в чате — `chat-output-budget.mdc` §5.

## Запрет ROI-оценок
`.cursor/rules/no-roi-estimates.mdc` — запрет на расчёт ROI и временных оценок (кроме `/opsx:estimate`).

## Инфраструктура 1С
`.cursor/docs/onec-infrastructure.md` — серверы 1С, PostgreSQL, HASP, Dev Container.

## Доменные навыки 1С
Навыки доступны через `available_skills`; вызываются из правил и агентов по типу задачи.
- **1c-bsp** — `.cursor/skills/1c-bsp/SKILL.md` (и подскиллы command, patterns, registration): регистрация в БСП «Дополнительные отчёты и обработки», команды, паттерны подсистем.
- **1c-extensions** — `.cursor/skills/1c-extensions/SKILL.md`: аннотации расширений (&Перед/&После, &ИзменениеИКонтроль, &Вместо), синтаксис директив.
- **1c-forms** — `.cursor/skills/1c-forms/SKILL.md` (подскиллы **info**, **validate**, **patterns**): управляемые формы — анализ и валидация выгрузки `Form.xml`, справочник паттернов; **без** генерации/правки `Form.xml` из JSON (генераторы удалены из фреймворка). Изменение форм — Конфигуратор + выгрузка и/или программное создание элементов в BSL модуля формы.
- **1c-mxl** — `.cursor/skills/1c-mxl/SKILL.md` (и подскиллы compile, decompile, info, validate): табличные макеты (MXL) — компиляция, декомпиляция, анализ.
- **1c-roles** — `.cursor/skills/1c-roles/SKILL.md` (и подскиллы compile, info): роли и права доступа — создание из JSON, анализ Rights.xml.
- **1c-query-optimization** — `.cursor/skills/1c-query-optimization/SKILL.md`: продвинутые паттерны запросов (временные таблицы, DCS).

## Справочная документация
`.cursor/docs/` — справочники для агентов и генерации документов.
- **platform/** — документация платформы 1С (оглавление, главы по формам, запросам, расширению конфигурации и др.). Используется в `.cursor/docs/1c-coding-standards.md`, onec-code-explorer.
- **standard/** — `.cursor/docs/standard/1c-standards-navigator.md`, `std-01-metadata.md` … `std-11-general.md`: вендорские стандарты 1С. Ссылается `1c-vendor-standards/SKILL.md`.

## Системные промпты агентов
`.cursor/agents/*.md` — промпты для onec-code-writer, onec-code-reviewer, onec-code-architect, onec-code-explorer, onec-trace-analyst, onec-code-simplifier, openspec-quality-controller, openspec-doc-writer.
Changelog: `.cursor/agents/CHANGELOG.md`.
