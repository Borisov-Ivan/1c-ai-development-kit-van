## Verify decision ledger

```yaml
closed_decisions: []
open_decision_id: null
decision_round: 0
decision_round_max: 2
verify_depth: full
assumptions_accepted: []
repair_attempt: 1
last_challenge_at: "2026-09-01T03:08:37Z"
last_verification: reports/verification-2026-09-01-3.md
```

## Extend — 2026-09-01

- Источник: `--from-verify` (internal repair-from-verify), `reports/design-challenge-2026-09-01.md`
- Режим: repair-from-verify (implementation_invariant; ось Chosen A не менялась)
- Что изменено:
  - `design.md`: сужены положительные признаки «только модуль»; смесь форм — один ход (запись программно + один вопрос из трёх); поясняющая строка MAY, отсутствие не дефект; Decisions 8–9; закрыт открытый вопрос; зеркало в «Решения verify»
  - `specs/split-form-layout-modes/spec.md`: токены module-only; Mixed THEN; Informing line — отсутствие строки не дефект
  - `tasks.md`: S1.1 / S1.2 / S1.3 / optional-буллеты accept
- Architect Gate: не требовался (технические инварианты классификатора и протокола чата, без смены оси)
- Следующий шаг: продолжение verify (полный повтор слоёв, repair_attempt=1)

## Verify repair — implementation_invariant — 2026-09-01

- Gaps из независимой проверки плана: (1) сузить «обработчики»/«видимость» без «в модуле»; (2) согласовать Mixed с одним вопросом выбора за ход; (3) закрыть MAY поясняющей строки
- Files touched: design.md, specs/split-form-layout-modes/spec.md, tasks.md

## Apply — S1 — 2026-09-01

- Срез: S1 — Пропуск холостого вопроса поставки
- Режим: mechanical (kit markdown)
- Задачи: S1.1–S1.8 [x]; S1.accept [ ]

### Регрессии (agent static)

- S1.6 Layout stays manual unless apply permission: § «Политика макетов» в `forms-mxl-mode-gate.mdc` — без разрешения `manual` + WAIT, без `1c-mxl/compile`. Apply skill: default manual, без молчаливого assisted. Текст не менялся этой ЗНИ.
- S1.7 Layout non-manual requires recorded apply permission: разрешение = чат apply / AskQuestion / `[mxl:…]` + запись в `debug.md` § Apply permissions. Apply skill guardrail Template.xml совпадает. Текст не менялся этой ЗНИ.
- S1.8 Legacy single artifact_mode maps to form_mode: Mode Gate «Legacy fallback»; apply skill fallback lone `artifact_mode`; verify skill `legacy-artifact-mode-fallback`. Текст не менялся этой ЗНИ.

## Slice Gate Decisions

### Slice S1 — Пропуск холостого вопроса поставки (2026-09-01)
Срез: S1 — Пропуск холостого вопроса поставки
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: S1.1–S1.8 [x]; S1.accept остаётся [ ]
Связанный отчёт: reports/handoff-acceptance-S1-2026-09-01.md
