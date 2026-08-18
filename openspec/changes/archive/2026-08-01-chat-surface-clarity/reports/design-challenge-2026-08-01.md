---
report_type: design-challenge
generated_at: 2026-08-01
agent: onec-code-architect
mode: design-challenge
scope:
  change: chat-surface-clarity
  design_mtime: "2026-08-01T05:42:37Z"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — chat-surface-clarity

## KB references

- Discovery выполнен, совпадений нет — секция Existing Knowledge пуста; конфликтов с KB нет.

## Адверсариальная установка

Challenge независим от истории explore/new: прочитаны только `proposal.md`, `design.md`, `specs/chat-surface-clarity/spec.md` и точечно текущие kit-файлы (Mode Gate, decision-block, lexicon, opsx-output-style). Отчёты `reports/architecture-*.md` и QC **не** использовались как источник истины. Closed decisions отсутствуют (ledger пуст).

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** оркестратор копирует в чат каноны и AskQuestion, которые сами нарушают Тест понятности (жаргон kit: skill, гейты, Schema, имена агентов; процессные преамбулы); правка одного Mode Gate не закрывает утечки в new/apply/verify/status/review (`proposal.md` ## Why).
- **Design адресует:**
  - Why «каноны учат жаргону» → Decision 2 + S1: переписать chat-канон Mode Gate на три русских варианта; вычистить эталоны «хорошо» в decision-block/lexicon/faq (`design.md` Decisions 2, Slices S1).
  - Why «утечки в командах» → S2: AskQuestion/thin-chat в new/apply/status/review/verify без Gate/Schema/onec-code-* (`design.md` S2; Behavior Contract).
  - Why «конфликты SSOT» → Decisions 4–5 + S3: KB не в брифе; бан slug агентов; сверка opsx с brief-card/lexicon.
  - Why «недостаточно одного Mode Gate» → Option B явно отклонён; волны S1→S2→S3 покрывают Impact-список proposal.
- **Покрытие:** **частичное → почти полное**, с пробелами приёмки, не постановки.
  - Симптом и зона лечения совпадают: точка правки — copy-paste SSOT, не runtime-stub alone (`design.md` Design Rationale) — это ровно то, что Why описывает как механизм поломки.
  - Подтверждение симптома в kit (не из design): `.cursor/docs/templates/decision-block.md` эталон «Хорошо» содержит «через skill»; `.cursor/rules/forms-mxl-mode-gate.mdc` chat-формулировка смешивает «автоматически» со `skill compile/edit`; `.cursor/docs/opsx-output-style.md` §2 разрешает slug агентов в backticks, а §3.1/таблица банов — запрещает; §7.7 п.7 требует «KB в scope» в чат-брифе explore/extend — прямо против Decision 4 / brief-card.
  - Не закрыто на уровне design↔spec: Behavior Contract перечисляет токены приёмки (`Пошаговая пауза`, Architect/Slice/Mode Gate в copy-paste), а ADDED Requirements в spec не фиксируют отдельный сценарий на «Пошаговая пауза» и не задают **операциональный** список зон grep (что считать chat-facing внутри одного `.mdc`/SKILL). Proposal обещает «зафиксировать grep-приёмку», design S3 ссылается на «список приёмки из proposal/plan», но в `proposal.md` перечислимого бан-листа/зон нет — только общая фраза. Без этого Primary S3 («grep пуст») не фальсифицируем из артефактов design/spec alone.

### Q2 — Optimality

- **Выбранный путь:** четыре волны правок chat-facing текстов по карте Impact + финальная grep-приёмка (Option A); без нового параллельного гайда стиля и без сужения до одного Mode Gate.
- **Альтернативы (включая не упомянутые в design ## Implementation Options):**
  1. **Runtime-only HALT / redaction** — усилить always-apply `chat-output-budget` и post-send self-check, не переписывая эталоны «хорошо». Плюс: меньший diff skills. Минус: оркестратор обязан «копировать как есть» (`design.md` Design Rationale); плохие каноны продолжают обучать модель; Why прямо говорит, что правка одного gate не закрывает copy-paste. **Отклонена:** не лечит источник копирования.
  2. **Механический replace_all запрещённых токенов** по `.cursor/**` без семантического канона Mode Gate (1/2/3 на языке Конфигуратор/репозиторий/модуль). Плюс: быстро. Минус: agent-facing таблицы `form_mode`/`skill` должны остаться (Decision 1); слепая замена либо ломает guards, либо оставляет бессмысленный русский без понятного выбора — нарушает Scenario «Mode Gate question is product language». **Отклонена:** не проходит Тест понятности.
  3. **Единый модуль `chat-canon.md` + thin pointers** из skills/rules (не «новый гайд стиля» Option C, а вынос уже существующих канонов в один файл). Плюс: одна точка правки Mode Gate/AskQuestion. Минус: массовая перекладка ссылок, риск рассинхрона пока pointers живы, по сути тот же объём правок + миграция структуры; proposal Impact уже перечисляет распределённые SSOT — волны A совпадают с фактической топологией kit. **Не превосходит A** по Blast Radius текста; усложняет поставку kit без выигрыша для Why.
  4. *(контрольная)* **Только Mode Gate / только новый гайд** — уже в design как B/C; B опровергается Why; C плодит четвёртый SSOT рядом с opsx/lexicon/decision-block.
- **Вердикт по Q2:** **оптимален** среди жизнеспособных путей для kit chat-surface: лечить copy-paste источники волны по Impact — минимально достаточный способ закрыть Why. Неупомянутые A1–A3 не лучше по инвазивности×полноте покрытия.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** **с оговорками** (не «чистый да»).
- **Причины:**
  - **Да:** проблема и решение совпадают (каноны → чат); Non-Goals защищают agent-facing verify/XML/BSL; отклонение B/C честное; срезы S1→S2→S3 читаются как вертикальные сценарии с Primary на языке разработчика 1С; Decisions 1–5 однозначны.
  - **Оговорка 1:** design не фиксирует **операциональную границу** chat-facing vs agent-facing внутри тех же файлов (например `forms-mxl-mode-gate.mdc`: какая секция — «копировать в чат», какая — skill/HALT для агента). Без маркера/правила риск: модель снова скопирует agent-абзац или grep «по `.cursor/**`» потребует либо ложных срабатываний на agent-таблицы, либо ручного «на глаз».
  - **Оговорка 2:** grep-приёмка обещана в proposal/design/Behavior Contract, но **канонический список токенов + карта зон** не закреплены в `design.md` / `spec.md` (частично размазаны по будущим tasks — tasks не являются Behavior Contract). Для fresh-eye постановка недозакрыта до apply.
  - **Оговорка 3:** ссылка на внешний план `mode_gate_chat_wording` (волны 1–4) в Context без якоря в репозитории — волны S1–S3 в design самодостаточны как таблица, но трассировка «аудит → срез» для ревьюера не проверяема из change-папки.

## Verdict

**CHALLENGE** — путь Option A решает Why и оптимален против рассмотренных альтернатив, но до apply в `design.md`/`spec.md` нужно добить приёмку и границу chat-facing (implementation_invariant), иначе S3 Primary и grep остаются договорённостью «на глаз».

## Gaps for design.md

1. **Список grep-приёмки (токены + зоны)** — перенести из размытой отсылки «proposal/plan» в `design.md` (Behavior Contract или приложение) и/или ADDED Scenario в spec: перечислить запрещённые подстроки для chat-facing и явное правило, что agent-only секции (таблицы `form_mode`/skill, технические HALT) **исключены** из grep или помечаются маркером «не копировать в чат».
2. **Операциональная граница Decision 1** — в design для Mode Gate (и аналогичных dual-language файлов) указать: какой заголовок/секция = единственный copy-paste в чат; остальное = agent-facing. Это снимает риск повторной утечки skill из соседнего абзаца.
3. **Выровнять Behavior Contract ↔ spec** — либо добавить Scenario на «Пошаговая пауза» / process-label в apply copy-paste, либо сузить Behavior Contract до токенов, уже покрытых ADDED Requirements (чтобы Primary не обещал больше, чем capability).
4. **Кумулятивный grep S3 vs приёмка S1/S2** — явно в design: финальный grep — closure change (точечные остатки в файлах S1/S2 без переоткрытия оси решения) **или** сузить S3 grep до зон вне Primary S1/S2. Иначе порядок срезов конфликтует с «accept уже пройден».
5. **Убрать или локализовать зависимость от `mode_gate_chat_wording`** — либо вложить краткую карту волн в design, либо не ссылаться на внешний план как на основание Context.

## Architectural alternatives

Равноправной развилки по **наблюдаемому поведению чата** нет: цель — одни и те же формулировки без жаргона kit. Различия A vs «единый chat-canon файл» — структура поставки kit, не другой UX для разработчика 1С. Workflow-варианты (когда apply) не рассматриваются.

## Источники

- `openspec/changes/chat-surface-clarity/proposal.md` — ## Why, ## What Changes, ## Impact, ## Scope
- `openspec/changes/chat-surface-clarity/design.md` — Goals/Non-Goals, Decisions 1–5, Implementation Options A/B/C, Behavior Contract, Slices S1–S3, Design Rationale, Risks
- `openspec/changes/chat-surface-clarity/specs/chat-surface-clarity/spec.md` — ADDED Requirements и Scenarios (Mode Gate, Good examples, Process preamble, AskQuestion/handoff, SSOT KB/agents, FAQ)
- Kit (verified): `.cursor/rules/forms-mxl-mode-gate.mdc` (chat-формулировка + skill), `.cursor/docs/templates/decision-block.md` (эталон «через skill»), `.cursor/docs/chat-lexicon.md` (замена assisted → «через skill»), `.cursor/docs/opsx-output-style.md` (§2 slug в backticks vs §3.1 бан; §7.7 п.7 KB в scope)
