---
report_type: design-challenge
generated_at: 2026-08-16
agent: onec-code-architect
mode: design-challenge
scope:
  change: kit-evolution-models-economy-profiles
  design_mtime: "2026-08-16T13:06:26+09:00"
verdict: APPROVE
confidence: high
---

# Design Challenge — kit-evolution-models-economy-profiles (post-repair)

## KB references

- Discovery выполнен, совпадений нет (нет `openspec/knowledge/_index.yaml`). Секция зафиксирована; на выводы KB-факты не влияли.

## Адверсариальная установка

Повтор после repair: список дыр 1–5 взят из `reports/design-challenge-2026-08-16-2.md` **только как чеклист закрытия**. Выводы построены заново по текущим `proposal.md`, `design.md` (mtime 2026-08-16T13:06:26+09:00), пяти delta specs, `tasks.md`, `debug.md` § Verify decision ledger, ADR-0001, ADR-0003, основному spec `review-quality-disposition`, живым always-apply файлам, `.gitignore` и описанию инструмента `Task` этой сборки. Отчёты `reports/architecture-*.md` как источник истины не использовались.

Закрытое решение `independent_challenge_carrier` не переоткрывается: живой enum `Task.model` по-прежнему без `claude-fable-5-thinking-high` (verified в этой сессии). Нового факта «слаг появился» нет. `reopen-blocked: independent_challenge_carrier`.

**Чеклист repair (дыры 1–5) — все закрыты:**

1. **Якорь поверхности.** `design.md` D6 адресаты: пункт (3) дословный MUST поверхности в always-apply delegation; `1c-utility-agents.mdc` и sidecar не заменяют якорь. `tasks.md` S2.10 — тот же остаток. `specs/always-apply-context-budget/spec.md` Scenario «Якорь поверхности после выноса процедуры». `## Blast Radius`: носитель процедуры — `review/SKILL.md`, якорь apply-time — delegation (семантика не меняется). Живой факт (до apply): MUST уже в always-apply `1c-agent-delegation.mdc` абзац «Поверхность»; `openspec-apply-change/SKILL.md` совпадений нет; `1c-utility-agents.mdc` — `alwaysApply: false`, без `globs`. Постановка больше не выносит MUST туда, куда apply не читает.
2. **S2.10 не вычищает merge S2.2.** Текст S2.10: вынос не удаляет три carve-out слияния `bsl-write-guard` (JSDoc/шапка метода, контекст apply/review, Mechanical Mode) и правило «post-reviewer fixes только через writer». Живой факт: carve-out сейчас в `bsl-write-guard.mdc`; «Без прямого StrReplace» / spot-check через writer — в delegation § АВТО-ИСПРАВЛЕНИЕ. Задача явно запрещает снести их вместе с полной процедурой.
3. **Gate check в переносимом минимуме.** `design.md` D6 и `tasks.md` S2.1: на каждом ходе — проверка активной команды, ограничений скилла и СТОП при нарушении. Живой факт: операционный детектор сейчас только в `command-session-persistence.mdc` правило 2; `session-discipline.mdc` несёт лозунг «протокол на каждом ходе» без трёх вопросов. Repair как раз копирует детектор в якорь до разжалования — это и требовалось.
4. **Эталон reviewer.** `design.md` таблица S3, `proposal.md` § Impact, `tasks.md` S3.1 / S3.accept: фрагменты BSL из `.cursor/docs/standard/std-06-code-modules.md` (файл поставки; новый `.bsl` не создаётся; `temp/` не в scope). Файл существует; в репозитории 0 `*.bsl`; `temp/` в `.gitignore`. Конфликта с write-guard нет.
5. **S1.10 ∩ D1a ∩ D3.** `tasks.md` S1.10 / S1.accept / slice-gate: независимый разбор — Fable **при наличии слага в enum**, иначе Opus 5 + одна строка. Согласовано с `design.md` D1a, `proposal.md` § What Changes, spec `subagent-model-mapping` Scenario «Независимый разбор постановки идёт на Fable».

Новых verified дыр того же класса нет. Историческая строка в `debug.md` (первый Extend: `temp/fixtures/reviewer-diet-baseline.bsl`) — журнал прошлой дельты; живые proposal/design/tasks её не несут.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** (1) таблица ролей ссылается на слаги вне живого enum — вызов архитектора падает и молча деградирует; новые модели (Opus 5, Fable 5, GPT-5.6) не задействованы; (2) always-apply ~54 КБ с ~20 КБ дублей, обязательства не должны пропасть; (3) нет адаптации под модель чата. Источник: `proposal.md` § Why.
- **Design адресует:** D1/D2/D3 — живой мэппинг + двухшаговая цепочка + самосверка enum; D1a — Fable как закрытая эскалация, условная по enum; D6/D7 — упаковка с always-apply якорями D6 (в) и диета reviewer; D4/D5 — пирамида профилей с MUST NOT.
- **Покрытие:** полное. Ядро Why закрыто; пять дыр прошлого прохода закрыты в постановке, не обходом.

Покрытие по пунктам Why:

1. **Мёртвые слаги → ошибка enum.** D1 ставит обычного архитектора на `claude-opus-5-thinking-high` (слаг **есть** в живом enum этой сборки). D3 запрещает подставлять отсутствующий слаг. Ежедневный сбой `claude-opus-4-8-thinking-high` этим лечится. **Закрыто.**
2. **Fable 5 как новая модель.** Why хочет «задействовать», не «вызвать с отсутствующим слагом». Дельта делает Fable *желаемой* целью D1a. На этой сборке независимый разбор идёт на Opus 5 — закрытое решение `independent_challenge_carrier`, совместимо с D3 и с Why (не воспроизводить Invalid model selection). **Закрыто; ось не переоткрывать.** `reopen-blocked: independent_challenge_carrier`.
3. **Диета без потери обязательств.** D6 (в) выполнен для диалоговых детекторов: KB-однострочник; carve-out ADR-0003; MUST поверхности; Gate check в переносимом минимуме; carve-out write-guard и post-reviewer через writer остаются в always-apply после выноса полной процедуры. Приёмка S2: замер факта + обязательство-diff + smoke в чистом окне. **Закрыто.**
4. **Адаптация под модель чата.** D4/D5 + spec профилей (профиль чата не копируется; MAY модели Primary в intent-брифе; MUST NOT chat-facing / ADR-0001). Три конфликтных сценария в S4 Primary. **Закрыто.**

### Q2 — Optimality

- **Выбранный путь:** живой мэппинг + самосверка + условная эскалация Fable; диета разжалованием с always-apply якорями D6 (в); пирамида профилей; точечные усиления делегирования.
- **Альтернативы (включая не упомянутые в design):**
  1. **Не разжаловать `command-session-persistence.mdc` (не упомянута).** Оставить детектор follow-up целиком always-apply. Плюс: Gate check не зависит от полноты копии. Минус: целый файл против цели ≤ 34 КБ. **Хуже Chosen после repair:** операционный детектор теперь в переносимом минимуме D6 / S2.1 дословно; держать второй always-apply файл ради того же текста — лишний бюджет без новой семантики.
  2. **Дублировать MUST поверхности ещё и в `openspec-apply-change/SKILL.md` как второй полный носитель (не упомянута).** Плюс: входной протокол apply видит правило сразу. Минус: два SSOT; длинная сессия apply вытесняет текст скилла — ровно то, от чего D6 (в) защищает always-apply якорем. Blast Radius уже отверг «полный вынос без якоря» и разрешил apply-скиллу *ссылаться* на якорь, не быть единственным носителем. Второй полный носитель не сильнее Chosen.
  3. **Не сливать `bsl-write-guard.mdc`, оставить отдельным always-apply (не упомянута).** Плюс: carve-out JSDoc / apply-context / Mechanical не пересекаются с выносом § АВТО-ИСПРАВЛЕНИЕ. Минус: дубль запрета Write `.bsl` и бюджет. **Хуже Chosen после repair:** S2.2 принимает содержание в delegation, S2.10 явно не вычищает carve-out и post-reviewer через writer; отдельный файл больше не нужен как страховка.
  4. **Независимый разбор на `gpt-5.6-sol-medium`, пока Fable нет в enum.** Слаг есть в живом enum; разводит «постановка vs атака» по модели. **`reopen-blocked: independent_challenge_carrier`** — заказчик закрыл носитель как Opus 5, не GPT-5.6 и не inherit. Без нового факта из enum не переоткрывать.
- **Вердикт по Q2:** оптимален. Каркас (мэппинг, самосверка, условный Fable, профили) тот же, что выдержал прошлую атаку. Упаковка S2.10 после repair совпадает с приёмом, которым уже спасли ADR-0003: полная процедура в скилле `/review`, дословный MUST в always-apply. Отклонённые в design варианты (чат = Opus/Fable; Fable на любой Architect Gate; трёхступенчатые цепочки; файл-состояние профиля) по-прежнему хуже.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** да.
- **Причины:**
  - Конфликт «Fable MUST vs нет слага в enum» снят честно (Opus 5 + строка, приёмка текстом правил, S1.10 копирует оговорку). Это не повтор исходного дефекта Invalid model selection.
  - Вынос авто-исправления больше не ослабляет apply-time обязательства: якорь поверхности, carve-out write-guard, post-reviewer через writer и Gate check persistence записаны в D6 / tasks / spec / Blast Radius тем же правилом D6 (в).
  - Эталон диеты reviewer — файл поставки `std-06-code-modules.md`, без `temp/` и без нового `.bsl`. Свежий взгляд не видит скрытого Write в gitignore.
  - Профили с конституцией MUST NOT и тремя конфликтными приёмками закрывают риск «адаптация = выключить гейт». Направление (Grok 4 в чате, дорогие модели на субагентах) согласовано с Why.

## Verdict

**APPROVE** — ядро Why закрыто; пять дыр прошлого разбора дописаны в постановку; новых verified дыр нет; ось `independent_challenge_carrier` держится.

Это не молчаливое согласие: атакованы носитель поверхности, слияние write-guard, Gate check persistence, эталон reviewer и формулировка S1.10; рассмотрены три неупомянутых альтернативы упаковки плюс GPT-5.6 как носитель независимого разбора. Ни одна не лучше Chosen после repair. Равноправной развилки по коду/поведению нет.

## Gaps for design.md

Нет.

## Architectural alternatives

Нет равноправной развилки. Ось `independent_challenge_carrier` держится. Альтернатива «носитель независимого разбора = GPT-5.6» помечена `reopen-blocked: independent_challenge_carrier`.

## Источники

- proposal.md — § Why; § What Changes (D1a ∩ D3, якоря D6 (в)); § Metadata (кода 1С нет); § Impact (эталон `std-06-code-modules.md`, без `temp/`, без нового `.bsl`).
- design.md — § Context (Fable не член enum); D1a; D5; D6 адресаты, переносимый минимум (Gate check), MUST поверхности; D7; Behavior Contract; Slices S1–S3; § Решения verify; § Blast Radius (ADR-0003 + якорь поверхности).
- debug.md — closed_decisions.independent_challenge_carrier; Extend repair-from-verify (дыры 1–5).
- tasks.md — S1.10 / S1.accept; S2.1 / S2.2 / S2.10; S3.1 / S3.accept.
- specs/subagent-model-mapping/spec.md — условный Fable; приёмка текстом правил.
- specs/always-apply-context-budget/spec.md — Scenario якоря apply-reviewer; Scenario якоря поверхности.
- specs/chat-model-profiles/spec.md — чат не копируется; MAY Primary; MUST NOT chat-facing.
- specs/delegation-safeguards/spec.md, specs/rules-hygiene/spec.md — вне атаки этой дельты; противоречий с Why нет.
- ADR-0001 — граница chat-facing vs agent-facing.
- ADR-0003 — `openspec/adrs/ADR-0003-review-quality-disposition.md`; `openspec/specs/review-quality-disposition/spec.md` Requirement «Apply-reviewer does not run disposition AskQuestion».
- Код kit (verified, до apply): `.cursor/rules/1c-agent-delegation.mdc` абзацы «Поверхность» и «Без прямого StrReplace»; `.cursor/rules/bsl-write-guard.mdc` три carve-out + post-reviewer через writer; `.cursor/rules/session-discipline.mdc` vs `.cursor/rules/command-session-persistence.mdc` правило 2; `.cursor/rules/1c-utility-agents.mdc` `alwaysApply: false`, без globs; `.cursor/skills/openspec-apply-change/SKILL.md` — нет поверхности; `.cursor/docs/standard/std-06-code-modules.md` существует; `.gitignore` (`temp/`); поиск `**/*.bsl` — 0 файлов.
- Verified runtime fact (эта сессия): enum `Task.model` = inherit, claude-opus-5-thinking-high, composer-2.5-fast, cursor-grok-4.5-high, cursor-grok-4.6-xhigh, gemini-3.1-pro, gpt-5.6-sol-medium. Нет `claude-fable-5-thinking-high`, нет `claude-opus-4-8-thinking-high`.
