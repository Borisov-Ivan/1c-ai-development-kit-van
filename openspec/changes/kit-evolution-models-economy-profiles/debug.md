# Debug

## Verify decision ledger

```yaml
closed_decisions:
  - id: independent_challenge_carrier
    summary: "Пока в описании Task нет слага самой дорогой эскалации, независимый разбор постановки идёт на Opus 5 (Primary обычного архитектора), не на GPT-5.6 и не без model=. Слаг Fable не передаётся и не угадывается; когда появится в enum — снова D1a."
    closed_at: "2026-08-16"
    source: verify-user-answer
open_decision_id: null
decision_round: 1
decision_round_max: 2
assumptions_accepted: []
verify_depth: full
open_known_questions: []
```

## Extend — 2026-08-16

- Источник: `/opsx:verify kit-evolution-models-economy-profiles` после ответа A на развилку носителя независимого разбора; плюс repair из `reports/verification-2026-08-16.md`.
- Что добавлено/изменено:
  - D1a ∩ D3: Fable только при наличии слага в enum; иначе Opus 5 + одна строка; приёмка S1 — текст правил.
  - Evidence-enum в Context больше не утверждает Fable членом списка.
  - Always-apply якоря D6(в): KB CONTEXT однострочник; carve-out apply-reviewer дословно в delegation; Blast Radius ADR-0003 (семантика не меняется).
  - Переносимый минимум session-правил: persistence + TRIGGER стратегии контекста.
  - Spec профилей: профиль чата не копируется; MAY модели Primary субагента в intent-брифе; MUST NOT chat-facing (ADR-0001).
  - S4 Primary сужен (чат Grok + три конфликта; живой слаг архитектора остаётся в S1).
  - S3.1 / приёмка: фикстура `temp/fixtures/reviewer-diet-baseline.bsl`.
  - Диета промпта архитектора — Non-Goals.
  - Зеркало: `design.md` § Решения verify (зафиксировано).
- Disposition: `accepted` (выбор A + repair-класс из отчёта verify).
- Architect Gate: не требовался — ось D1a не менялась; независимый разбор уже в `reports/design-challenge-2026-08-16.md`; пользователь закрыл единственную развилку ответом A.
- Следующий шаг: `/opsx:verify kit-evolution-models-economy-profiles`.

## Extend — 2026-08-16 (repair-from-verify)

- Источник: internal Repair Loop `/opsx:verify` по `reports/design-challenge-2026-08-16-2.md` (gaps 1–5, class implementation_invariant).
- Что добавлено/изменено:
  - D6 адресаты / S2.10: always-apply якорь MUST поверхности (не закрывать apply при REFACTOR по поверхности без simplifier или waive); `1c-utility-agents` и sidecar не заменяют якорь.
  - S2.10 не вычищает carve-out слияния `bsl-write-guard` (S2.2) и «post-reviewer fixes только через writer».
  - Переносимый минимум session-правил / S2.1: Gate check (активная команда, ограничения скилла, СТОП).
  - Эталон диеты reviewer: `.cursor/docs/standard/std-06-code-modules.md` (поставка; не `temp/`, новый `.bsl` не создаётся). S3.1 / S3.accept / proposal Impact / таблица S3.
  - S1.10: независимый разбор — Fable только при наличии слага в enum, иначе Opus 5.
  - Spec: Scenario «Якорь поверхности после выноса процедуры»; Blast Radius — якорь поверхности.
- Disposition: `accepted` (repair-класс, ось D1a / independent_challenge_carrier не менялась).
- Architect Gate: не требовался — дописывание D6(в), не смена подхода.
- Следующий шаг: повтор слоёв verify (repair_attempt=1).

## Slice Gate Decisions

### Slice S1 — Живой мэппинг моделей (2026-08-16)
Срез: S1 — Живой мэппинг моделей
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: нет (S1.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S1-2026-08-16.md

### Slice S1 — Живой мэппинг моделей (2026-08-16) — вердикт
Срез: S1 — Живой мэппинг моделей
Решение: принят
Обоснование: без замечаний
Изменения tasks: S1.accept [x]
Связанный отчёт: reports/slice-acceptance-S1-2026-08-16.md

### Slice S2 — Диета always-apply (2026-08-16)
Срез: S2 — Диета always-apply
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: нет (S2.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S2-2026-08-16.md

### Apply session — continue-to-end (2026-08-16)
Срез: S2–S6
Решение: continue-to-end (пользователь: «выполняй до конца, приму всё вместе»)
Обоснование: рабочие задачи S2 закрыты; приёмка S2.accept остаётся [ ] до сводной передачи. Реализация S3–S6 без паузы на границе среза. Зависимость S3/S4/S5 от подписанной приёмки S2 снята явной просьбой продолжить.
Изменения tasks: нет
Связанный отчёт: будет reports/handoff-acceptance-S2-S6-2026-08-16.md


