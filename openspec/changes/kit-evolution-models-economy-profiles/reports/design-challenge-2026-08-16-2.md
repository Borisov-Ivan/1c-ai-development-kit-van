---
report_type: design-challenge
generated_at: 2026-08-16
agent: onec-code-architect
mode: design-challenge
scope:
  change: kit-evolution-models-economy-profiles
  design_mtime: "2026-08-16T12:35:33+09:00"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — kit-evolution-models-economy-profiles (incremental)

## KB references

- Discovery выполнен, совпадений нет (нет `openspec/knowledge/_index.yaml`). Секция зафиксирована; на выводы KB-факты не влияли.

## Адверсариальная установка

Incremental-проход: прошлый независимый разбор (`reports/design-challenge-2026-08-16.md`, design_mtime 2026-08-16T11:48:05) использован **только** как список уже атакованных дыр. Выводы построены заново по текущим `proposal.md`, `design.md`, пяти delta specs, `debug.md` § Verify decision ledger, ADR-0001, ADR-0003, основному spec `review-quality-disposition`, живым always-apply файлам и `.gitignore`. Отчёты `reports/architecture-*.md` как источник истины не использовались.

Закрытое решение `independent_challenge_carrier` не переоткрывается: живой enum `Task.model` этой сборки по-прежнему без `claude-fable-5-thinking-high` (verified 2026-08-16, тот же перечень, что в прошлый раз). Нового факта «слаг появился» нет.

**Что в дельте закрыто (не повторять как открытые дыры):**

1. § Context больше не печатает Fable членом enum; D1a ∩ D3: передавать слаг только если он есть в описании `Task`, иначе Opus 5 + одна строка; приёмка S1 — текст правил (`design.md` D1a, `specs/subagent-model-mapping/spec.md` Requirement «Fable только как закрытая эскалация», сценарий «Независимый разбор постановки идёт на Fable»).
2. Always-apply якорь carve-out apply-reviewer дословно + `## Blast Radius` на ADR-0003 (`design.md` D6 адресаты, Blast Radius; `specs/always-apply-context-budget/spec.md` Scenario «Якорь apply-reviewer после выноса процедуры»).
3. KB CONTEXT однострочник в always-apply (`design.md` D6).
4. Переносимый минимум session-правил включает persistence и TRIGGER/ACTION/BYPASS стратегии контекста (`design.md` D6).
5. Spec профилей: профиль чата не копируется; MAY модели Primary субагента в intent-брифе; MUST NOT chat-facing (`specs/chat-model-profiles/spec.md`; `design.md` D5).
6. Диета промпта архитектора — Non-Goals (`design.md` Goals / D7). Why этого не требовал.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** (1) таблица ролей ссылается на слаги вне живого enum — вызов архитектора падает и молча деградирует; новые модели не задействованы; (2) always-apply ~54 КБ с ~20 КБ дублей, обязательства не должны пропасть; (3) нет адаптации под модель чата. Источник: `proposal.md` § Why.
- **Design адресует:** D1/D2/D3 — живой мэппинг + самосверка + двухшаговая цепочка; D1a — Fable как закрытая эскалация **условная по enum**; D6/D7 — упаковка и диета reviewer; D4/D5 — профили.
- **Покрытие:** частичное — ядро Why закрыто, остаётся одна дыра того же класса, что уже чинили для ADR-0003.

Покрытие по пунктам Why:

1. **Мёртвые слаги → ошибка enum.** D1 ставит обычного архитектора на `claude-opus-5-thinking-high` (слаг **есть** в живом enum). D3 запрещает подставлять отсутствующий слаг. Ежедневный сбой `model-selection.mdc` (`claude-opus-4-8-thinking-high`) этим лечится. **Закрыто.**
2. **Fable 5 как новая модель.** Why хочет «задействовать», не «вызвать с отсутствующим слагом». Дельта делает Fable *желаемой* целью D1a, а не членом enum. На этой сборке независимый разбор идёт на Opus 5 — это закрытое решение `independent_challenge_carrier`, совместимо с D3 и с Why (не воспроизводить `Invalid model selection`). **Закрыто; ось не переоткрывать.** `reopen-blocked: independent_challenge_carrier`.
3. **Диета без потери обязательств.** D6 (в) сформулирован верно. Дельта закрыла carve-out ADR-0003 и KB-якорь. **Не закрыто:** в том же абзаце адресатов «полная процедура § АВТО-ИСПРАВЛЕНИЕ (включая DISPROPORTIONATE_SURFACE) → `review/SKILL.md`», а always-apply остаток перечисляет только лимит итераций и carve-out weak / design-prescribed. Правило «не закрывать apply при REFACTOR по поверхности без упрощения или waive» сейчас живёт в always-apply `1c-agent-delegation.mdc` (абзац «Поверхность»). Скилл `/review` его уже содержит (шаг 5), но **входной протокол apply — `openspec-apply-change/SKILL.md`, не `review/SKILL.md`**. Поиск по apply-скиллу: совпадений нет. `1c-utility-agents.mdc` повторяет MUST, но `alwaysApply: false` и **без `globs`** — диалоговый триггер «ревьювер вернул шум поверхности в apply» через путь файла не наблюдается. Это ровно D6 (в). Вынос без якоря = ослабление, не упаковка.
4. **Адаптация под модель чата.** D4/D5 + согласованный spec профилей. Три конфликтных сценария в S4 Primary закрывают риск «профиль выключил гейт». **Закрыто.**

### Q2 — Optimality

- **Выбранный путь:** живой мэппинг + самосверка + условная эскалация Fable; диета разжалованием с always-apply якорями; пирамида профилей; точечные усиления делегирования.
- **Альтернативы (включая не упомянутые в design):**
  1. **Однострочник поверхности в always-apply delegation (не упомянута).** Тот же приём, что Chosen уже сделал для carve-out ADR-0003: полная процедура — в `review/SKILL.md`; в `1c-agent-delegation.mdc` остаётся дословный MUST «полное ревью нового/переписанного модуля с REFACTOR по поверхности → не закрывать apply/`/review` без simplifier или явного waive». Плюс: D6 (в) выполнен, семантика не меняется, бюджет ~0,3 КБ внутри 34 КБ. Минус: чуть больше always-apply текста. **Почему лучше Chosen:** Chosen в S2.10 явно выносит этот MUST в скилл, который apply не читает; `openspec-apply-change/SKILL.md` правила не содержит. Это не равно упаковке carve-out — дыра в том же абзаце, который дельта «починила».
  2. **Носитель apply-обязательств — только `openspec-apply-change/SKILL.md` (не упомянута).** Команда apply всегда читает этот скилл (входной протокол). Плюс: 0 КБ always-apply. Минус: длинная сессия apply вытесняет текст скилла; D6 (в) как раз для обязательств, которые должны переживать давление контекста. **Хуже однострочника в always-apply**, лучше Chosen «только `review/SKILL.md`».
  3. **Не разжаловать `command-session-persistence.mdc` (не упомянута).** Оставить детектор follow-up always-apply. Плюс: Gate check «какая команда / какие ограничения / СТОП» не зависит от полноты копии в `session-discipline.mdc`. Минус: ~файл целиком против цели ≤ 34 КБ. **Не лучше**, если в переносимый минимум дословно попадёт Gate check (сейчас в списке D6 его нет — только лозунг «протокол на каждом ходе»). Текущий `session-discipline.mdc` Gate check **не** содержит; он только в `command-session-persistence.mdc` правило 2.
  4. **Эталон диеты reviewer — закоммиченный образец в `.cursor/docs/`, не `temp/fixtures/*.bsl` (не упомянута).** В репозитории **0** файлов `.bsl`; `temp/` в `.gitignore`; `proposal.md` § Metadata / Impact: кода 1С нет, список файлов без `temp/`. `bsl-write-guard.mdc` запрещает оркестратору Write/StrReplace по `.bsl`; writer не создаёт новые `.bsl` в несуществующих директориях. Плюс альтернативы: образец в поставке docs, без конфликта с запретом записи. Минус: tasks уже назвали `temp/fixtures/reviewer-diet-baseline.bsl`. Design-таблица S3 по-прежнему говорит «реальный дифф», без пути — дельта в tasks/debug не доведена до `design.md` § Slices.
  5. **Независимый разбор на `gpt-5.6-sol-medium`, пока Fable нет в enum.** Слаг есть в живом enum; разводит «постановка vs атака постановки» по модели. **`reopen-blocked: independent_challenge_carrier`** — заказчик закрыл носитель как Opus 5, не GPT-5.6 и не inherit. Без нового факта из enum не переоткрывать.
- **Вердикт по Q2:** каркас (мэппинг, самосверка, профили, условный Fable) оптимален. Упаковка S2.10 **не** оптимальна: альтернатива 1 обязана войти в Chosen тем же правилом D6 (в), которым уже спасли ADR-0003. Отклонённые в design варианты (чат = Opus/Fable; Fable на любой Architect Gate; трёхступенчатые цепочки; файл-состояние профиля) по-прежнему хуже.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками.
- **Причины:**
  - Да: конфликт «Fable MUST vs нет слага в enum» снят честно (Opus 5 + строка, приёмка текстом правил). Это больше не повтор исходного дефекта.
  - Да: якорь ADR-0003, KB-однострочник, TRIGGER стратегии контекста, разведение «профиль чата vs MAY субагента», MUST NOT chat-facing (ADR-0001) — дельта делает то, что прошлый разбор требовал.
  - Нет: нельзя согласовать вынос MUST поверхности в скилл `/review`, когда apply его не читает, а `1c-utility-agents.mdc` не always-apply и без globs. Свежий взгляд видит ту же ошибку носителя, что у carve-out до ремонта — только другое предложение того же параграфа.
  - Нет (слабее): эталон приёмки диеты reviewer в gitignore + новый `.bsl` вне Impact, при том что таблица S3 в `design.md` путь не фиксирует.

## Verdict

**CHALLENGE** — дельта закрыла конфликт Fable/enum и якорь ADR-0003; постановка всё ещё не готова к реализации, пока MUST «не закрывать apply при шуме поверхности без упрощения» не останется в always-apply якоре тем же приёмом D6 (в).

Это не отказ от направления и не пересмотр оси Fable. Нет равноправной замены «профили vs не профили». Блокирует конкретный остаток упаковки в D6/S2.10.

## Gaps for design.md

1. **implementation_invariant — якорь поверхности в always-apply.** В D6 адресаты, в S2.10 и в `specs/always-apply-context-budget/spec.md` (рядом со Scenario «Якорь apply-reviewer»): при выносе полной процедуры в `review/SKILL.md` в `1c-agent-delegation.mdc` SHALL остаться дословный MUST поверхности (новое/переписанное + REFACTOR по поверхности → не закрывать apply/`/review` без simplifier или явного waive). Добавить строку в `## Blast Radius`: семантика не меняется; носитель процедуры — skill `/review`, якорь apply-time — delegation. `1c-utility-agents.mdc` и sidecar **не** заменяют якорь (on-demand, без globs; sidecar явно исключён текущим текстом delegation). Указатель S2.12: apply-скилл может ссылаться на якорь, но не быть единственным носителем.
2. **implementation_invariant — S2.10 не вычищает merge S2.2.** Предложения из `bsl-write-guard.mdc` про контекст apply/review и «post-reviewer fixes только через writer» остаются в always-apply delegation после выноса § АВТО-ИСПРАВЛЕНИЕ. Иначе запрет прямого StrReplace уйдёт вместе с секцией.
3. **implementation_invariant — Gate check в переносимом минимуме.** В список D6 «дословно» добавить правило 2 `command-session-persistence.mdc`: на каждом ходе проверить активную команду, ограничения скилла, СТОП при нарушении. Сейчас минимум говорит «протокол на каждом ходе»; операционный детектор follow-up остаётся только в разжалуемом файле. TRIGGER стратегии контекста в минимуме уже есть — это тот же класс дыры, что закрывали в прошлый раз, только для persistence.
4. **Эталон диеты reviewer в scope.** Зафиксировать в `design.md` § Slices S3 и в `proposal.md` § Impact путь **внутри поставки** (например `.cursor/docs/standard/reviewer-diet-baseline.bsl` или markdown-образец с фрагментом BSL из `std-06`). Не опираться на `temp/` (gitignore). Не требовать от оркестратора Write нового `.bsl` (always-apply `bsl-write-guard.mdc`; writer не создаёт новые `.bsl`). Tasks S3.1/S3.accept согласовать с этим путём. Таблица S3 в design сейчас всё ещё «реальный дифф» — дельта debug/tasks не доехала до design.
5. **Согласовать tasks S1.10 с D1a ∩ D3.** Формулировка «независимый разбор постановки — Fable» без условия enum снова провоцирует хардкод отсутствующего слага в скиллах. Design/spec уже условные; задача должна копировать ту же оговорку. Не развилка.

## Architectural alternatives

Нет равноправной развилки по коду/поведению. Ось `independent_challenge_carrier` держится. Альтернатива «носитель независимого разбора = GPT-5.6» помечена `reopen-blocked: independent_challenge_carrier`. Вынос поверхности «целиком в `review/SKILL.md`» **не** равноправен якорю в always-apply — первый отменяет apply-time MUST. Это gap 1, не развилка.

## Источники

- proposal.md — § Why; § What Changes (D1a ∩ D3, always-apply якоря D6 (в)); § Metadata (кода 1С нет); § Impact (без `temp/`, без `.bsl`).
- design.md — § Context (Fable не член enum); D1a; D5; D6 адресаты и переносимый минимум; D7 Non-Goals; Behavior Contract; Slices S2/S3; § Решения verify; § Blast Radius (только ADR-0003).
- debug.md — closed_decisions.independent_challenge_carrier; Extend 2026-08-16 (список дельты).
- specs/subagent-model-mapping/spec.md — условный Fable; приёмка текстом правил.
- specs/always-apply-context-budget/spec.md — Scenario якоря apply-reviewer (поверхность не упомянута).
- specs/chat-model-profiles/spec.md — чат не копируется; MAY Primary; MUST NOT chat-facing.
- specs/delegation-safeguards/spec.md, specs/rules-hygiene/spec.md — вне атаки этой дельты.
- ADR-0001 — `openspec/adrs/ADR-0001-chat-facing-vs-agent-facing.md`.
- ADR-0003 — `openspec/adrs/ADR-0003-review-quality-disposition.md`; `openspec/specs/review-quality-disposition/spec.md` Requirement «Apply-reviewer does not run disposition AskQuestion».
- Код kit: `.cursor/rules/1c-agent-delegation.mdc` абзац «Поверхность» (always-apply); `.cursor/skills/review/SKILL.md` шаг 5 (поверхность); `.cursor/skills/openspec-apply-change/SKILL.md` — нет поверхности; `.cursor/rules/1c-utility-agents.mdc` alwaysApply false, без globs; `.cursor/rules/session-discipline.mdc` vs `.cursor/rules/command-session-persistence.mdc` правило 2 (Gate check); `.cursor/rules/bsl-write-guard.mdc` запрет Write `.bsl`; `.gitignore` (`temp/`); поиск `**/*.bsl` — 0 файлов.
- Verified runtime fact (эта сессия / промпт оркестратора): enum `Task.model` = inherit, claude-opus-5-thinking-high, composer-2.5-fast, cursor-grok-4.5-high, cursor-grok-4.6-xhigh, gemini-3.1-pro, gpt-5.6-sol-medium. Нет `claude-fable-5-thinking-high`, нет `claude-opus-4-8-thinking-high`.
