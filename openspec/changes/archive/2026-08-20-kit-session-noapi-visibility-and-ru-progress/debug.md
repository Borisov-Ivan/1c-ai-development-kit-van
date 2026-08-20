# Debug: kit-session-noapi-visibility-and-ru-progress

## Verify decision ledger

```yaml
closed_decisions: []
open_decision_id: null
decision_round: 0
decision_round_max: 2
verify_depth: full
assumptions_accepted: []
repair_attempt: 0
```

## Extend — 2026-08-19

- Источник: `--from-verify` (internal repair-from-verify), `reports/design-challenge-2026-08-19.md` + `reports/architecture-task-readiness-2026-08-19.md`
- Что добавлено/изменено:
  - Why: канон уже есть в правиле; сбой — on-demand vs момент после сбоя
  - Триггер канона → always-apply бюджет чата §5 (S1.14)
  - Приоритет языка → бюджет чата §6; гайд стиля — отсылка
  - Дельта `chat-surface-clarity`: английские каркасы как примеры, не MUST NOT-список
  - D8: эвристика по постановке на шаге 1.5; пропуск `n/a` закрывает гейт
  - Поздний BSL: `n/a` = плейсхолдер на apply, S3.6, Scenario «Поздний BSL — вопрос на apply»
  - Приёмка S1: чтение §5, не «смоделированный лимит»
  - S1.4 / S2.2 / S2.3 / S2.8: наблюдаемый результат и счёт §1b
- Disposition: accepted (implementation_invariant, ось D1–D11 не менялась)
- Architect Gate: не требовался
- Отчёты: `reports/design-challenge-2026-08-19.md`, `reports/architecture-task-readiness-2026-08-19.md`, `reports/quality-control-2026-08-19.md`
- Следующий шаг: повтор verify (слои 1–5), repair_attempt=1

## Extend — 2026-08-19 (нейтральная строка архитектора)

- Источник: реплика заказчика в чате — «Самая дорогая эскалация в этой сборке недоступна» звучит коряво и носит оттенок проблемы; предложено нейтральное «Модель архитектора: opus»
- Что добавлено/изменено:
  - D7: канон в чат — «Модель архитектора: Opus 5»; без «недоступна» / «эскалация» / «сборка»; канон лимита не менять
  - proposal п.5 и Modified `subagent-model-mapping`
  - S1.4 / S1.15 / S2.7 / S2.9; Scenario «Нет слага сильной модели — строка про Opus 5»
  - дельта `specs/subagent-model-mapping/spec.md`; Scenario «Verify без английского progress»
- Disposition: accepted (пересмотр формулировки D7 по заказчику; политика вызова Opus 5 без угадывания семейства сохраняется)
- Architect Gate: не требовался (чат-facing copy, не новая ось)
- Следующий шаг: `/opsx:verify kit-session-noapi-visibility-and-ru-progress`

## Verify repair — implementation invariant

- Дата: 2026-08-19
- Alerts: Layer 4 CHALLENGE gaps 1–5; Layer 5 GAP-1/2/3 (формулировки задач)
- Files touched: proposal.md, design.md, tasks.md, specs/session-api-mode/spec.md, specs/chat-surface-clarity/spec.md, specs/sequential-gate-questions/spec.md, debug.md

## Extend — 2026-08-19 (repair-from-verify, attempt 2)

- Источник: `--from-verify` (internal repair-from-verify), `reports/design-challenge-2026-08-19-3.md` + `reports/architecture-task-readiness-2026-08-19-2.md`
- Что добавлено/изменено:
  - D2: дословный канон в always-apply §5; первая строка хода; исключение verify из «одно сообщение»; §1b пункт «канон» — срез сигнала
  - D5/D6: вводная английская речь = тот же провал, что английский progress; §1b пункт «язык» — срез progress
  - D8: пропуск маркера только при доказанном kit-only; Scenario «Деловая постановка без .bsl — вопрос маркера»
  - S1.16 / S1.17 / S1.18; S3.7; режим mechanical у S1; apply: сначала разработчик по умолчанию
  - Дельты session-api-mode, chat-surface-clarity, sequential-gate-questions
- Disposition: accepted (implementation_invariant; ось D1–D11 сохранена, эвристика D8 уточнена без смены цели)
- Architect Gate: reports/design-challenge-2026-08-19-3.md
- Следующий шаг: повтор verify (слои 1–5), repair_attempt=2

## Verify repair — implementation invariant (attempt 2)

- Дата: 2026-08-19
- Alerts: независимый разбор — приоритет канона vs одно сообщение verify; фраза в always-apply; первая строка; охват языка; полярность пропуска маркера; владение §1b
- Files touched: proposal.md, design.md, tasks.md, specs/session-api-mode/spec.md, specs/chat-surface-clarity/spec.md, specs/sequential-gate-questions/spec.md, debug.md

## Slice Gate Decisions

### Slice S1 — Сигнал лимита (2026-08-20)
Срез: S1 — Сигнал лимита
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary (чтение правил kit, без ИБ).
Изменения tasks: нет (S1.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S1-2026-08-20.md

### Slice S2 — Русский progress (2026-08-20)
Срез: S2 — Русский progress
Решение: awaiting-acceptance
Обоснование: рабочие задачи S2.1–S2.10 реализованы; пользователь отложил приёмку всех срезов на конец apply.
Изменения tasks: S2.1–S2.10 [x]; S2.accept остаётся [ ]
Связанный отчёт: reports/handoff-acceptance-S2-2026-08-20.md

### Slice S3 — Маркер только при BSL (2026-08-20)
Срез: S3 — Маркер только при BSL
Решение: awaiting-acceptance
Обоснование: рабочие задачи S3.1–S3.7 реализованы; пользователь отложил приёмку всех срезов на конец apply.
Изменения tasks: S3.1, S3.2, S3.6, S3.3, S3.4, S3.7, S3.5 [x]; S3.accept остаётся [ ]
Связанный отчёт: reports/handoff-acceptance-S3-2026-08-20.md

### Slice S1 — Сигнал лимита (2026-08-20)
Срез: S1 — Сигнал лимита
Решение: принят (manual shortcut)
Обоснование: пользователь: «принято, архив»; Primary — чтение правил kit, без ИБ.
Изменения tasks: отмечены [x]: S1.accept
Связанный отчёт: reports/slice-acceptance-S1-2026-08-20.md

### Slice S2 — Русский progress (2026-08-20)
Срез: S2 — Русский progress
Решение: принят (manual shortcut)
Обоснование: пользователь: «принято, архив»; Primary — чтение правил kit, без ИБ.
Изменения tasks: отмечены [x]: S2.accept
Связанный отчёт: reports/slice-acceptance-S2-2026-08-20.md

### Slice S3 — Маркер только при BSL (2026-08-20)
Срез: S3 — Маркер только при BSL
Решение: принят (manual shortcut)
Обоснование: пользователь: «принято, архив»; Primary — чтение правил kit, без ИБ.
Изменения tasks: отмечены [x]: S3.accept
Связанный отчёт: reports/slice-acceptance-S3-2026-08-20.md

