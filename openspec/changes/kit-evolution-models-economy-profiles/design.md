# Design: kit-evolution-models-economy-profiles

## Context

Kit — метапроект (правила, скиллы, агенты Cursor для 1С-разработки). Исследование 2026-08-16 (`temp/reports/exploration-2026-08-16-kit-critical-review.md`) зафиксировало: Primary архитектора и enum-пример в `model-selection.mdc` мертвы для актуальной сборки Cursor; always-apply набор + `AGENTS.md` = 53,7 КБ на каждый запрос при ~20 КБ дублей; адаптации поведения под модель чата нет. Референс `ai_rules_1c` (разбор — `temp/reports/exploration-2026-08-16-ai-rules-1c-model-adaptation.md`) даёт рабочие образцы: тонкие профили моделей поверх модель-нейтрального свода, граница MAY/MUST NOT, запрет молчаливой коэрции, intent-брифы, запрет built-in Explore.

Актуальный enum `Task.model` (evidence сессии 2026-08-16): `inherit`, `claude-fable-5-thinking-high`, `claude-opus-5-thinking-high`, `composer-2.5-fast`, `cursor-grok-4.5-high`, `cursor-grok-4.6-xhigh`, `gemini-3.1-pro`, `gpt-5.6-sol-medium`.

## Goals / Non-Goals

**Goals:**

- Рабочий мэппинг ролей субагентов на живые модели + механизм самосверки enum (устойчивость к апдейтам Cursor).
- Always-apply набор вместе с `AGENTS.md` ≤ 34 КБ без потери ни одного обязательства (экономия упаковкой, не ослаблением).
- Слой профилей модели чата. Основной оркестратор — Grok 4 (сейчас `cursor-grok-4.6-xhigh`). Fable 5 — не чат и не обычный архитектор: только закрытая эскалация на самых ответственных архитектурных разборах. GPT-5.6 / Opus 5 — Primary субагентов по таблице, без смены чата команд. Конституционный запрет ослаблять гейты.
- Точечные усиления делегирования и гигиена свода по образцам референса.

**Non-Goals:**

- UI-тестовая инфраструктура (agent-browser, Playwright, Windows-MCP) — нет потребителя в kit.
- Портирование `.dev.env` / установщика / doctor из референса — чужая инфраструктура.
- Отрезание legacy-слоёв `vertical-slices.mdc` и `artifact_mode` — отдельная мажорная ревизия.
- Изменение состава агентов и OpenSpec workflow.

## Decisions

**D1. Мэппинг ролей.** Рекомендуемая модель чата оркестратора — семейство Grok 4, слаг сборки на момент ЗНИ: `cursor-grok-4.6-xhigh` (extra high). Команды `/opsx:*` **не** требуют сессии на Fable 5 / GPT-5.6 / Opus 5 — это дорого и не нужно. Те модели — Primary вызовов `Task` для тяжёлых ролей.

Таблица: architect (обычный) → `claude-opus-5-thinking-high`; simplifier → `composer-2.5-fast`; reviewer → `gemini-3.1-pro`; writer / explorer / trace-analyst / QC → без `model=` (inherit = модель чата, то есть Grok 4 при рекомендованной сессии). Альтернатива «reviewer → `gpt-5.6-sol-medium`» отклонена: нет свидетельств преимущества, дороже. Альтернатива «оркестратор = Opus/Fable/GPT» отклонена: пользователь явно выбрал Grok extra high как основной (2026-08-16).

**D1a. Fable — закрытая эскалация, не роль по умолчанию.** Слаг `claude-fable-5-thinking-high` слишком дорог для штатного делегирования. Fable SHALL вызываться только как архитектор и только по закрытому списку (механическая проверка `mode` + триггер, не «кажется важным»):

1. `mode=design-challenge` — всегда Fable (независимый разбор постановки).
2. `mode=deep-analysis` — Fable, только если одновременно сработал тяжёлый архитектурный триггер: новый объект метаданных, перехват базовой процедуры, Identity Filter, конфликт с архивным контрактом (Blast Radius / прецедент), петля приёмки среза. Иначе `deep-analysis` идёт на Opus 5.
3. Явная просьба пользователя («на Fable», «самая сильная/дорогая»).

Всё остальное — не Fable: обычный `design`, `slice-decomposition`, `task-readiness`, `task-decomposition`, аудиты coherence, writer / explorer / reviewer / simplifier / QC. Сбой Opus **не** эскалирует на Fable (иначе авария модели становится счётом за самую дорогую). Цепочка эскалации Fable: Primary Fable → без `model=` (не «Fable как запасной после Opus»). На один сработавший гейт — не больше одного вызова Fable, пока пользователь не попросит повтор. Перед вызовом — одна строка в чат, что разбор идёт на самой дорогой модели; `AskQuestion` каждый раз не нужен: политика уже задана.

Отклонено: «всегда спрашивать» — лишняя пауза на уже согласованном правиле. Отклонено: «Fable на любой Architect Gate» — Gate срабатывает часто (в том числе на декомпозицию срезов), цена не оправдана.

**D2. Цепочки сокращаются до двух шагов: Primary → без `model=`.** Двухступенчатые fallback были компенсацией мёртвых слагов; при самосверке enum (D3) они не нужны. Альтернатива «оставить трёхступенчатые» отклонена — лишние failed-вызовы и шум.

**D3. Enum не хардкодить.** `model-selection.mdc` перестаёт содержать «пример enum»; вместо него правило: актуальный список слагов — в описании инструмента `Task` текущей сборки; перед первым вызовом с `model=` оркестратор сверяет слаг с этим списком; расхождение → вызов без `model=` + предложение обновить таблицу. Запрет подставлять «похожую» модель молча (no family guessing — перенос из референса). Утверждение «`inherit` в enum нет» удаляется как ложное.

**D4. Профили моделей: трёхуровневая пирамида.** Стаб-строка в `AGENTS.md` → роутер `.cursor/rules/model-adaptation.mdc` (селектор, precedence, MAY/MUST NOT) → файлы профилей `model-grok4.mdc` (основной оркестратор), `model-fable5.mdc`, `model-gpt56.mdc`, `model-opus5.mdc` (on-demand). Три волны из `temp/reports/exploration-2026-08-16-ai-rules-1c-model-adaptation.md` §13 — срезы **этой** ЗНИ (S4 / S5 / S6), не отдельные change.

Селектор оркестратора — self-knowledge модели **чата**. Файл-состояния нет. Опциональный override — строка в overlay `openspec/project.md`. Незнакомая модель = профиль не активен, действует базовый свод (это норма; никогда не спрашивать на обычной задаче). Соседний профиль «потому что похож» запрещён: Grok 4.6→4.7 остаётся в профиле `grok4` (то же семейство и мажор); Grok 5 / Opus 4 → opus5 — нет, это уже другая мажорная линия.

Профиль `model-gpt56.mdc` содержит явную оговорку: принцип «lean context / не читать индекс и детальный файл вместе» **не** распространяется на конструкцию kit «стаб → полное тело» (`chat-output-budget` → `chat-output-budget-full`, `gate-dispatcher` → файл гейта, командный вход → `templates/*.md` при обрезке). Чтение полного тела по триггеру стаба обязательно и не считается повторным чтением.

**D5. Граница профиля (конституция).** Профиль МОЖЕТ: длина ответа/отчёта, нарратив, глубина планирования, охота к делегированию (spawn eagerness), запрет самопридуманных перепроверок. Профиль НЕ МОЖЕТ ослаблять: BSL/XML write guard, LINT GATE, обязательность reviewer, HALT-триггеры, Metadata/Mode/Design/Architect гейты, лимиты итераций, chat-output-budget HALT. Формула из референса: обязательные вызовы валидаторов — tool evidence, не «self-verification». Любое чтение профиля, которое выглядит как ослабление гейта, — misread. Precedence: указания пользователя → project overlay → профиль → базовый свод; список MUST NOT выигрывает при любом порядке.

**Длина против лимита.** Профиль настраивает длину и плотность **внутри** лимитов таблицы `chat-output-budget.mdc`; сами лимиты, HALT-список жаргона и обязательные блоки (`**Следующий шаг:**`, карточка развилки) — вне охвата профиля. Формулировка профиля «выбирай понятность вместо краткости» относится к качеству текста в пределах лимита, а не к праву его превысить.

**Предписанная перепроверка — не self-verification.** Повторные проходы, предписанные протоколом (Layer 4 `/opsx:verify` с требованием независимости от собственных прошлых отчётов, spot-check отчётов субагентов против первоисточника, EXTENSION VERIFICATION, повторный reviewer после writer), профилем не снимаются. Профиль гасит только перепроверки, которые агент придумал себе сам.

**Область действия.** Профиль **чата** применяется к оркестратору. Свой профиль оркестратор в брифы субагентов не копирует. Если вызов `Task` идёт с Primary-слагом Fable 5 / GPT-5.6 / Opus 5, оркестратор **может** прочитать профиль **той** модели и учесть MAY в intent-брифе (длина отчёта, запрет «проверь мой дифф», evidence-аудит) — без микрошагов и без ослабления гейтов. Так дорогие модели используются точечно на субагентах, а чат команд остаётся на Grok 4.

**Нормализация имени.** Соответствие «модель → профиль» устанавливается по семейству и мажорной версии, без учёта регистра, разделителей, вендорских префиксов и суффиксов усилия (`cursor-grok-4.6-xhigh` → `grok4`, `claude-opus-5-thinking-high` → `opus5`). Неопознанная модель = профиля нет; это норма, а не дефект.

**D6. Экономия упаковкой, не ослаблением.** Каждое правило, уходящее из always-apply, сохраняет: (а) триггер загрузки в frontmatter (`globs` / `description`); (б) строку-cue в `gate-dispatcher.mdc` или карте SSOT `AGENTS.md`; **(в) само обязательство — в always-apply якоре, если триггер правила не наблюдается через путь файла (`globs`), а возникает из хода диалога.** Cue сообщает о существовании файла и не заменяет обязательство: правило, которое само является детектором своего триггера, не может рассчитывать на то, что будет прочитано вовремя.

**Переносимый минимум при разжаловании трёх session-правил** (в `session-discipline.mdc`, дословно, не пересказом): первый tool call командной сессии — только Read `SKILL.md`; запрет читать файлы пользователя до Entry Protocol; страховка при обрезке большого `SKILL.md` (дочитать `templates/*.md`); TodoWrite checkpoint; таблица антипаттернов follow-up (explore → «создай ЗНИ», explore → самостоятельный Grep по `.bsl`, apply → «а может лучше»).

Меры: `1c-xml-write-guard.mdc` → on-demand (компакт-версия уже в delegation); `command-skill-gate.mdc`, `command-session-persistence.mdc`, `context-strategy-gate.mdc` → on-demand (консолидированы в `session-discipline.mdc` с переносимым минимумом выше); `conversational-discipline.mdc` + `orchestrator-as-navigator.mdc` → слить в `chat-output-budget.mdc` (в `command-skill-gate.mdc:31` обновить висячую ссылку на conversational-discipline); `bsl-write-guard.mdc` → слить в `1c-agent-delegation.mdc` (принять не только заголовочный запрет, но и три carve-out: JSDoc/шапка метода, контекст apply/review, Mechanical Mode — и минимальный поток); из `1c-agent-delegation.mdc` вынести § KB CONTEXT, § АВТО-ИСПРАВЛЕНИЕ (carve-out) в on-demand.

**Адресаты выносимых секций:** § KB CONTEXT → `knowledge-format.mdc`; § АВТО-ИСПРАВЛЕНИЕ РЕВЬЮ (включая carve-out и DISPROPORTIONATE_SURFACE) → `review/SKILL.md`; таблица шагов § WRITER PIPELINE → `1c-writer-pipeline.mdc`. **Передача SSOT:** статус «единственный эталон сквозного потока» переходит от `1c-agent-delegation.mdc` к `1c-writer-pipeline.mdc`; обратные ссылки обновляются в `1c-writer-pipeline.mdc`, `review/SKILL.md`, `openspec-apply-change/SKILL.md`. В always-apply delegation остаётся однострочный поток `writer → ReadLints → … → reviewer` — он нужен до того, как `.bsl` попадёт в контекст и сработают `globs`.

**Методика замера бюджета:** факт = сумма байт файлов с `alwaysApply: true` + `AGENTS.md`, измеренная **после** всех правок среза; заявленные дельты мер не суммируются (перенос текста внутрь другого always-apply файла экономии не даёт). Ожидаемый нетто-результат ≈ 29–32 КБ при цели ≤ 34 КБ. Замер повторяется после S5 (усиление делегирования), потому что этот срез дописывает в delegation.

**D7. Диета reviewer.** `onec-code-reviewer.md` (67 КБ) режется до ядра протокола; чек-листы и справочники — on-demand файлы (`.cursor/docs/standard/reviewer-checks.md` и соседние), которые агент читает сам по типу задачи. Сравнение полноты чек-листов до/после — обязательный шаг приёмки. Соблюдение обеспечивается evidence-однострочником: отчёт reviewer обязан содержать строку `Checklists read: <перечень>`; отсутствие строки — дефект отчёта того же класса, что отсутствие Linter Signals. Аналогично (вторым приоритетом) — `onec-code-architect.md`: инструкции режимов выносятся в sidecar-файлы per-mode.

**D8. Запрет built-in Explore — только для 1С-кода.** Делегированное обследование `src/**`, `cfe/**`, `.bsl`, 1С XML — только `onec-code-explorer`; built-in `subagent_type: "explore"` для этих путей запрещён, молчаливый fallback = дефект. Для не-1С файлов (markdown, отчёты, данные) generic explore остаётся разрешён (наш `context-strategy` уже так маршрутизирует). Отличие от референса (тотальный бан): у нас есть легитимные не-1С сценарии.

**D9. Intent-брифы и эскалация.** В `1c-agent-patterns` / delegation: бриф субагенту = цель + ограничения + критерий готовности (не микрошаги); «2 неудачи субагента на ясной постановке → оркестратор решает сам или эскалирует пользователю» (существующие лимиты итераций не меняются); coverage-first в брифах reviewer (не «только critical» — фильтр в отчёте, не в охвате); аудит шаблонов промптов на просьбы пересказать рассуждения (reasoning-extraction) и «не думай долго».

**D10. Гигиена свода.** Шапка «Когда загружать» первой строкой каждого on-demand правила; принцип «индекс — routing cue, SSOT триггера — frontmatter файла»; decision shortcut (4 строки классификатора) в начало `task-triage.mdc`; секция safety floor («что не ослабляет ни один режим») + формализованные promotion triggers (транзакционные пути, контракт `Экспорт`, RLS, adopted-объекты) в `1c-halt-triggers.mdc`; формула «quick-fix снижает накладные расходы, не глубину проверки». Рудименты: `CHANGELOG.md` → из `.cursor/agents/` в `.cursor/docs/`; удалить `opsx-ff.md`, `opsx-continue.md`, `openspec-sessions.mdc` и упоминания.

**D11. Метаданные.** Маркеры не применяются (`marker_style: minimal`, developer n/a) — kit-метапроект без кода 1С (решение пользователя 2026-08-16). `form_mode: n/a`.

**D12. Ссылки на `openspec/project.md` в kit-репозитории.** Файл создаётся `/init-project` в целевом проекте и в kit-репо отсутствует по дизайну. В S2, при переписывании `AGENTS.md` и delegation: ссылку на термины перевести на существующий `openspec/glossary.md`; ссылки на пути и overlay сопроводить пометкой «создаётся `/init-project`; в kit-репозитории отсутствует — блок путей в промптах агентов опускается». Стартовый `project.md` в kit-репо не заводить: он попадёт в поставку и перезапишет настройки consumer-проекта.

## Existing Mechanisms

Новых механизмов хранения/состояния не создаётся. Профили используют штатный механизм `.cursor/rules` (alwaysApply / description / globs); выбор модели — штатный параметр `Task.model`; override — существующий overlay `openspec/project.md`. Отклонено: файл-состояние выбора профиля (аналог `.dev.env` референса) — в Cursor нет установщика, который бы им управлял, а self-knowledge покрывает 95% случаев.

## Behavior Contract

- Вызов обычного архитектора идёт на Opus 5 без ошибки enum; Fable не вызывается для декомпозиции срезов, task-readiness и прочих режимов вне закрытого списка D1a.
- Слаг вне enum сборки никогда не подставляется молча; «похожая» модель — только по явному выбору пользователя.
- Сбой Opus не переключает вызов на Fable; Fable не является запасной моделью ни для какой роли.
- При чате на Grok 4 оркестратор применяет `model-grok4.mdc`; команды `/opsx:*` не требуют сессии Fable / GPT / Opus. При `Task` с Primary Opus/Fable/GPT MAY той модели учитывается в intent-брифе, гейты MUST NOT не ослабляются.
- При модели чата Fable 5 / GPT-5.6 / Opus 5 (если пользователь сам так выбрал) активный профиль чата меняет только длину/нарратив/охоту к делегированию; каждый гейт из списка MUST NOT срабатывает идентично базовому своду.
- После диеты always-apply каждый сценарий-триггер (правка `.bsl` → writer pipeline; XML в `src/` → стоп; команда → Read SKILL; 3+ файлов → context-strategy) продолжает срабатывать.
- Обследование 1С-кода не уходит в built-in explore ни при каких сбоях кастомного агента — при недоступности `onec-code-explorer` оркестратор сообщает пользователю.

## Risks / Trade-offs

- [Разжалованное правило не подгрузится в редком сценарии] → триггеры в frontmatter + строки-cue в dispatcher/AGENTS.md + приёмочные smoke-сценарии на каждый триггер (S2.accept).
- [Разжалованное правило само является детектором своего триггера — cue не помогает] → обязательство переносится в always-apply якорь дословно (D6 (в)); поведенческий smoke в чистом окне на приёмке S2.
- [Профиль модели выключает on-demand слой через принцип lean context] → carve-out stub→full в `model-gpt56.mdc` (D4); негативная проверка в приёмке S4 (профили).
- [Диета reviewer потеряет проверки] → выносить, не удалять: чек-листы в on-demand файлы, которые reviewer обязан читать; diff-сравнение полноты чек-листов до/после в приёмке.
- [Профиль прочитан как разрешение ослабить гейт] → секция MUST NOT в каждом файле профиля + формула «misread» + precedence в роутере.
- [Enum снова уедет при апдейте Cursor] → D3 самосверка; в таблице остаются только Primary-слаги с пометкой «сверять с описанием Task».
- [Consumer-проекты со старой копией kit] → изменение только упаковки и аддитивные профили; обновление штатной поставкой `.cursor` + `AGENTS.md` (`kit-template-workflow.md`).
- [composer-2.5-fast окажется слаб для simplifier на сложном рефакторинге] → цепочка «Primary → без `model=`»: при неудовлетворительном результате повтор на модели чата; reviewer после simplifier обязателен как и сейчас.
- [Fable уйдёт в обычную декомпозицию срезов или станет запасной после сбоя Opus] → закрытый список D1a; запрет Fable-as-fallback; приёмка: вызов slice-decomposition на Opus, design-challenge на Fable.

## Migration Plan

Поставка штатная: копирование `.cursor/**` + `AGENTS.md` в consumer-проект, Reload Window. Папка `openspec/changes/kit-evolution-models-economy-profiles/` в `main` не мержится (`kit-template-workflow.md`). Откат — git revert ветки; независимых состояний нет.

## Open Questions

- Нужна ли команда `/opsx:rulesmodel` (ручная смена/просмотр профиля), или self-knowledge + override в project.md достаточно? Черновое решение: в S4 команду не делать, добавить `status`-строку в `/opsx:status`; команду — отдельным change при реальной потребности.
- Закрыто 2026-08-16: основной оркестратор — Grok 4 extra high. Fable — только закрытая эскалация архитектора (D1a), не чат команд и не запасная модель.

## Slices

| Срез | Имя | Сценарий (outcome) | Файлы (основные) | Primary acceptance |
|---|---|---|---|---|
| S1 | Живой мэппинг моделей | Делегирование идёт на актуальные модели без ошибок enum; Fable только на закрытой эскалации архитектора; самосверка защищает от будущего дрейфа | `.cursor/rules/model-selection.mdc`, `.cursor/rules/architect-gate.mdc`, `.cursor/rules/tool-name-guard.mdc` | Тестовый вызов обычного архитектора на Opus 5 без ошибки enum; `slice-decomposition` не идёт на Fable; `design-challenge` идёт на Fable с одной строкой в чат; в рантайм-употреблениях нет мёртвых слагов |
| S2 | Диета always-apply | Постоянный контекст ≤ 34 КБ; все гейты срабатывают как раньше | `chat-output-budget.mdc`, `session-discipline.mdc`, `1c-agent-delegation.mdc`, `1c-xml-write-guard.mdc`, `bsl-write-guard.mdc`, `conversational-discipline.mdc`, `orchestrator-as-navigator.mdc`, `command-skill-gate.mdc`, `command-session-persistence.mdc`, `context-strategy-gate.mdc`, `AGENTS.md`, `.cursor/docs/delivery-integrity.md` | (1) Замер факта: сумма байт файлов `alwaysApply: true` + `AGENTS.md` ≤ 34 КБ; (2) обязательство-diff — таблица «обязательство разжалованного файла → якорь в always-apply», без непокрытых строк; (3) поведенческий smoke в чистом окне (Reload): команда → первый tool call Read скилла; правка XML в `src/` → стоп; анализ 3+ файлов → context-strategy; правка `.bsl` → делегирование writer |
| S3 | Диета промпта reviewer | Ревью стоит меньше на каждом вызове при неизменном покрытии | `.cursor/agents/onec-code-reviewer.md`, `.cursor/docs/standard/reviewer-checks.md` и соседние | Diff полноты чек-листов до/после: ни один пункт не исчез, только переехал; один прогон reviewer на реальном диффе даёт строку `Checklists read:` и находки, сопоставимые с прогоном до диеты |
| S4 | Профили моделей | Чат команд на Grok 4; Fable/GPT/Opus — субагенты; гейты не ослаблены | новые `model-adaptation.mdc`, `model-grok4.mdc`, `model-fable5.mdc`, `model-gpt56.mdc`, `model-opus5.mdc`; стаб в `AGENTS.md` | Роутер и четыре профиля существуют, содержат MAY/MUST NOT и precedence; в `model-selection.mdc` / AGENTS.md указано: рекомендуемый чат оркестратора — Grok 4, без требования вести `/opsx:*` на Opus/Fable/GPT; сверка на трёх конфликтных примерах в пользу базового свода |
| S5 | Усиление делегирования | Обследование 1С не утекает в built-in explore; брифы субагентам — intent-формат | `1c-agent-delegation.mdc`, `.cursor/skills/1c-agent-patterns/*`, `context-strategy/SKILL.md` | Запрет built-in explore для 1С-путей записан в delegation и context-strategy; шаблон intent-брифа (цель / ограничения / scope / критерий готовности) в 1c-agent-patterns; явный запрет просить субагента пересказать ход рассуждений и «не думай долго» записан в шаблонах; правило эскалации после двух неудач субагента записано в delegation; контрольный замер бюджета always-apply после правок delegation ≤ 34 КБ |
| S6 | Гигиена свода | On-demand правила самоописывают триггер; triage быстрее; опасные пути защищены явным полом | `task-triage.mdc`, `1c-halt-triggers.mdc`, on-demand `.mdc` (шапки), `.cursor/agents/CHANGELOG.md`, `opsx-ff.md`, `opsx-continue.md`, `openspec-sessions.mdc` | Шапки «Когда загружать» в топ-10 on-demand правил; safety floor + promotion triggers в halt-triggers, сценарная проверка: правка контракта `Экспорт`-процедуры маршрутизируется в full-cycle независимо от Light Mode; рудименты удалены/перенесены; нет ссылок на удалённые в этом change пути |

**Зависимости срезов:** S1 — независим. S2 — независим от S1 (общие файлы с S4/S6: `AGENTS.md`, delegation — порядок S2 → S4 → S5 → S6 снижает конфликты). S3 (диета reviewer) — после S2, независим от S4–S6. S4 — после S2 (стаб в уже сжатый AGENTS.md). S5 — после S2 (правки в сжатый delegation; после S5 — контрольный замер бюджета). S6 — последний (шапки ставятся на финальный состав файлов; карта SSOT `AGENTS.md` финализируется здесь).

**Scope работы по legacy-сессиям в S6:** удалить `openspec-sessions.mdc` и снять упоминание в `session-discipline.mdc`; legacy read-only fallback в skills/commands остаётся (вне always-apply, 0 КБ постоянного контекста) — его отрезание относится к отдельной мажорной ревизии (Non-Goals).

**Матрица покрытия:** `subagent-model-mapping` → S1; `always-apply-context-budget` → S2 (+S3: бюджет промптов агентов); `chat-model-profiles` → S4; `delegation-safeguards` → S5; `rules-hygiene` → S6.

**Волны отчёта `ai_rules_1c` §13 в этой ЗНИ:** волна 1 (профили: grok4 как оркестратор + fable5/gpt56/opus5 для субагентов) → S4; волна 2 (запрет built-in Explore, spawn eagerness, эскалация, coverage-first, аудит шаблонов) → S5; волна 3 (шапки «Когда загружать», decision shortcut, safety floor) → S6. S1–S3 — мэппинг и диета из ревью kit, не отдельные change.

**Дельты спецификаций:** каждый срез создаёт свою `specs/<capability>/spec.md` в change: S1 → `subagent-model-mapping`; S2 → `always-apply-context-budget`; S4 → `chat-model-profiles`; S5 → `delegation-safeguards`; S6 → `rules-hygiene`. S3 (диета reviewer) своей дельты не создаёт — расширяет `always-apply-context-budget` разделом о бюджете промптов агентов.
