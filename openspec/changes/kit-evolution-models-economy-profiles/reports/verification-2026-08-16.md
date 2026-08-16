---
verify_mode: pre-apply
change: kit-evolution-models-economy-profiles
date: 2026-08-16
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: WARNING
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: WARNING
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: FAIL
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: independent_challenge_carrier
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - independent_challenge_carrier
  artifacts_mtime:
    proposal.md: "2026-08-16T11:49:17+09:00"
    design.md: "2026-08-16T11:48:05+09:00"
    tasks.md: "2026-08-16T11:49:17+09:00"
    specs/always-apply-context-budget/spec.md: "2026-08-16T11:14:20+09:00"
    specs/chat-model-profiles/spec.md: "2026-08-16T11:40:26+09:00"
    specs/delegation-safeguards/spec.md: "2026-08-16T11:28:50+09:00"
    specs/rules-hygiene/spec.md: "2026-08-16T11:15:07+09:00"
    specs/subagent-model-mapping/spec.md: "2026-08-16T11:48:18+09:00"
  last_challenge_at: "2026-08-16T11:48:05+09:00"
---

## Резюме для разработчика

kit-evolution-models-economy-profiles — до старта нужен ваш выбор по логике независимой проверки постановки.

**Что решить: на какой модели вести независимый разбор постановки, пока в Cursor нет слага самой дорогой эскалации**

План требует, чтобы независимый разбор постановки шёл не на той же модели, что обычная постановка задач. В текущей сборке отдельного слага этой дорогой модели в списке вызова нет: передать отсутствующее имя — снова ошибка выбора модели, ради которой затеяна эта работа. Пока слага нет, разбор должен идти на модели из живого списка.

- **A. Как обычный архитектор** — независимый разбор на Opus 5, той же модели, что постановка задач; дешевле, но постановка и атака постановки временно не разведены по модели.
- **B. Другая модель из списка** — независимый разбор на GPT-5.6; постановка и атака на разных моделях, но это не самая дорогая; когда дорогая появится в списке, политика вернётся к ней.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify kit-evolution-models-economy-profiles`.

Полный отчёт: openspec/changes/kit-evolution-models-economy-profiles/reports/verification-2026-08-16.md#1-носитель-независимого-разбора-постановки

Это kit-метапроект: меняются `.cursor/rules`, промпты агентов и `AGENTS.md`, кода 1С нет. Ядро плана (живой мэппинг ролей, самосверка списка моделей, сжатие постоянного контекста, профили без ослабления гейтов) закрывает исходную боль. Блокирует не направление, а дыра: постановка печатает слаг, которого нет в списке вызова этой сборки.

## Что доработать в постановке

### Рекомендации

- **Слаг эскалации и самосверка:** в `design.md` § Context убрать утверждение, что `claude-fable-5-thinking-high` входит в живой enum. Политика D1a остаётся; фактический вызов — только если слаг есть в описании `Task`, иначе выбранный ниже носитель + одна строка предупреждения, без угадывания семейства (D3). Сценарии spec и приёмка первого среза — условные, не безусловный MUST живого вызова.
- **Carve-out качества ревью в always-apply:** вынос полной процедуры в `review/SKILL.md` допустим; в `1c-agent-delegation.mdc` остаётся дословный минимум apply-reviewer (weak / design-prescribed / agreement-override не авто-fix и не авто-waive). Иначе apply не загрузит скилл `/review` и потеряет пол ADR-0003. Добавить `## Blast Radius` (семантика не меняется, меняется носитель) либо оставить Modified Capabilities пустым после доказательства остатка.
- **KB CONTEXT:** при выносе формата в `knowledge-format.mdc` в always-apply delegation оставить однострочный якорь: при делегировании explorer / architect / trace — блок `## Existing Knowledge`.
- **Переносимый минимум session-правил:** в список «дословно» включить TRIGGER/ACTION/BYPASS стратегии контекста (3+ файлов) и persistence «протокол на каждом ходе» — иначе после разжалования гейта дымит приёмка «анализ 3+ файлов».
- **Спека профилей:** различить «профиль чата не копируется в бриф» и «MAY профиля модели Primary субагента можно учесть в intent-брифе». MUST NOT профилей явно включить границу chat-facing (ADR-0001): в чат не копировать имена субагентов, скиллов и гейтов.
- **Приёмка профилей:** убрать из обязательной проверки четвёртого среза пункт «архитектор идёт с Primary Opus 5» (это результат первого среза) либо объявить зависимость от первого среза. Для независимости первого среза предпочтительно сузить Primary.
- **Эталон для диеты ревьювера:** в kit нет `.bsl`; назвать путь фикстуры вне `src/` (например `temp/fixtures/reviewer-diet-baseline.bsl`) в задаче базовой линии и в приёмке.
- **Диета промпта архитектора:** D7 «вторым приоритетом sidecar per-mode» не попала в задачи — вынести в Non-Goals этой ЗНИ.

После ответа на развилку эти пункты дописываются в постановку вместе с выбранным носителем.

### Развилки

#### 1. Носитель независимого разбора постановки

**В чём проблема.** План требует передавать слаг самой дорогой эскалации на независимый разбор постановки, но в описании инструмента `Task` этой сборки этого слага нет. Передать его — снова ошибка выбора модели.

**На что влияет.** Каждый независимый разбор постановки либо падает на первом вызове, либо молча уходит на запасную модель — то же, что сейчас ломает обычного архитектора.

**Если выбрать A / B.** **A** — независимый разбор на Opus 5 (как обычная постановка задач); дешевле, но постановка и атака постановки временно на одной модели. **B** — независимый разбор на GPT-5.6 (слаг есть в списке); постановка и атака на разных моделях, но это не самая дорогая; когда дорогая появится в списке, D1a снова включает её.

**Цель ЗНИ:** вызовы субагентов идут на модели из живого списка, без ошибки выбора — **обе ветки закрывают**; развилка — только кто несёт независимый разбор, пока дорогой слаг отсутствует.

**Что в коде сейчас.** `.cursor/rules/model-selection.mdc` Primary архитектора — мёртвый `claude-opus-4-8-thinking-high`; `architect-gate.mdc` дублирует тот же слаг. Живой enum этой сессии: `inherit`, `claude-opus-5-thinking-high`, `composer-2.5-fast`, `cursor-grok-4.5-high`, `cursor-grok-4.6-xhigh`, `gemini-3.1-pro`, `gpt-5.6-sol-medium`. Нет `claude-fable-5-thinking-high`.

**Что предлагает план.** D1a: независимый разбор постановки всегда на Fable; D3: слаг вне enum не подставлять. На этой сборке два правила несовместимы, пока в D1a нет ветки «нет в enum → выбранный носитель».

**Почему это развилка.** Ось «Fable не роль по умолчанию и не запас после сбоя Opus» не пересматривается. Не закрыто, **чем** заменить Fable, пока слага нет: тем же Opus 5 или другой моделью из списка.

**Варианты решения.**

- **A. Opus 5** — тот же Primary, что у обычного архитектора; для разработчика меньше счетов; для пользователя команд разведение «постановка vs атака» по модели временно пропадает.
- **B. GPT-5.6** — другой Primary, чем у обычного design; для разработчика независимый разбор остаётся «не тем же вызовом»; для пользователя команд это всё ещё не «самая дорогая» модель из текста D1a.

**Что изменится после выбора.** В `design.md` D1a и в spec `subagent-model-mapping`: условный вызов Fable; fallback-носитель A или B; приёмка первого среза — текст правил, не успешный `Task` с отсутствующим слагом. Остальные рекомендации (carve-out, KB CONTEXT, эталон BSL, сужение Primary профилей) дописываются тем же ходом.

**Источники** *(техническое):* `reports/design-challenge-2026-08-16.md` Q2 альтернативы 1–2; `reports/architecture-task-readiness-2026-08-16.md` G1.

## Что меняется в постановке

**Расширение / конфигурация:** kit (`.cursor/**`, `AGENTS.md`); `src/` не затрагивается.

**Точки изменения:**

- `.cursor/rules/model-selection.mdc` — живая таблица ролей, самосверка enum, двухшаговые цепочки, закрытая эскалация архитектора.
- `.cursor/rules/1c-agent-delegation.mdc` — сжатие always-apply, якоря write-guard / carve-out / KB CONTEXT.
- `.cursor/rules/chat-output-budget.mdc` — слияние стабов навигатора и дисциплины диалога.
- Новые `model-adaptation.mdc` и профили `model-grok4.mdc` / `model-fable5.mdc` / `model-gpt56.mdc` / `model-opus5.mdc`.
- `.cursor/agents/onec-code-reviewer.md` — диета промпта, чек-листы on-demand.

**Что НЕ меняется:** состав агентов и OpenSpec workflow; write-guard BSL/XML, LINT GATE, обязательность reviewer, HALT-триггеры; семантика ADR-0001 (chat-facing) и ADR-0003 (disposition ревью) — упаковка, не отмена.

**Связанные ADR / KB / архив:** ADR-0001 (Load-Bearing), ADR-0003 (Load-bearing). Архивных delta specs с теми же capability нет.

### К сведению

- Таблица срезов в `design.md` маппит capabilities, а не имена Scenario; привязка есть в «Связь со spec» каждого среза.
- S3 своей дельты spec не создаёт — расширяет `always-apply-context-budget` (намеренно).
- `openspec/project.md` в kit-репо отсутствует по D12; `openspec/glossary.md` есть.
- Независимый разбор этой проверки выполнен на модели чата: запасная модель вызова упёрлась в лимит API.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы, `<!-- slice-gate -->` у S1–S6, fences, `form_mode: n/a`. Авто-исправлений нет.
- **Layer 2 (Internal Coherence):** WARNING. QC: `reports/quality-control-2026-08-16.md` verdict WARNING. Алерт `undeclared-dependency` (S4 Primary требует Opus 5 из S1). `scenario-orphan-design` SUGGESTION. 34/34 Scenario покрыты (accept или in-slice task). UTC: none. 8b self-achievable: S4 дыра backward, не `slice-accept-not-self-achievable`. Precedent 2.4: нет MODIFIED/REMOVED; invariant KB нет (`_index.yaml` отсутствует); Load-Bearing ADR не Supersedes. Code-Truth: kit-пути, не символы 1С; phantom-symbol не применялся.
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` до этого прогона не содержал Slice Gate Decisions; `S<N>.accept` все `[ ]`; AcceptLoop = 0.
- **Layer 3 (Problem-Solution Trace):** WARNING. Why покрыт capabilities; у каждого Requirement есть Scenario; implementation-leak маркеров в THEN нет; `comment_suffix` пуст. `scenario-orphan-design` (имена Scenario не в таблице `## Slices`).
- **Layer 4 (Independent Challenge):** CHALLENGE; отчёт: `reports/design-challenge-2026-08-16.md`. Classifier: architectural fork `independent_challenge_carrier` (A Opus 5 / B GPT-5.6) → decision; gaps 1, 3–8 → repair после ответа. Не REJECT (каркас Why жив). `last_challenge_at` обновлён (CHALLENGE ушёл в чат).
- **Layer 5 (Implementation Readiness):** FAIL; отчёт: `reports/architecture-task-readiness-2026-08-16.md` вердикт НЕ ГОТОВО. G1–G4 = repair-класс после decision.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

- `decision_id: independent_challenge_carrier`
- class: decision (приоритет над repair)
- repair after user-extend `--from-verify`: G1–G4 task-readiness + Layer 4 gaps 1, 3–8 + QC undeclared-dependency option B (сузить S4 Primary)

### Post-challenge classifier

- Drop reopen: нет closed_decisions.
- implementation_invariant: Fable∩D3 условный вызов; carve-out remainder; KB CONTEXT якорь; session-discipline TRIGGER; spec профилей MAY vs MUST NOT; ADR-0001 MUST NOT; S3.1 path; S4 Primary сужение.
- Architectural fork kept: носитель независимого разбора при отсутствии Fable в enum (A vs B).
- GO-saturated: не применяется (`decision_round=0`, Layer 5 FAIL, Layer 4 не assumption_deferrable).

## Источники

- `reports/quality-control-2026-08-16.md` — `undeclared-dependency`, `scenario-orphan-design`
- `reports/design-challenge-2026-08-16.md` — CHALLENGE, Q1–Q3, alternatives 1–2
- `reports/architecture-task-readiness-2026-08-16.md` — G1–G4
- `openspec/adrs/ADR-0001-chat-facing-vs-agent-facing.md`, `openspec/adrs/ADR-0003-review-quality-disposition.md`
- Verified runtime: enum `Task.model` этой сессии (без `claude-fable-5-thinking-high`)
