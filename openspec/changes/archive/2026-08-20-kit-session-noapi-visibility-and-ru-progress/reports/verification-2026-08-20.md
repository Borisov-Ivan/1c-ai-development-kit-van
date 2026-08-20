---
verify_mode: pre-apply
change: kit-session-noapi-visibility-and-ru-progress
date: 2026-08-20
verdict: GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: SKIPPED-novelty
  layer_5_implementation_readiness: PASS
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks:
    - S1.1
    - S1.14
    - S1.16
    - S1.17
    - S1.2
    - S1.3
    - S1.4
    - S1.5
    - S1.6
    - S1.7
    - S1.8
    - S1.9
    - S1.10
    - S1.11
    - S1.12
    - S1.13
    - S1.15
    - S1.18
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: incremental
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-08-19T19:21:21+09:00"
    design.md: "2026-08-19T19:10:14+09:00"
    tasks.md: "2026-08-20T00:46:52+09:00"
    specs/session-api-mode/spec.md: "2026-08-19T19:06:41+09:00"
    specs/chat-surface-clarity/spec.md: "2026-08-19T19:06:50+09:00"
    specs/sequential-gate-questions/spec.md: "2026-08-19T19:06:50+09:00"
    specs/chat-model-profiles/spec.md: "2026-08-19T14:01:42+09:00"
    specs/subagent-model-mapping/spec.md: "2026-08-19T15:46:42+09:00"
  last_challenge_at: "2026-08-19T19:10:14+09:00"
---

## Резюме для разработчика

kit-session-noapi-visibility-and-ru-progress — срез «Сигнал лимита» готов к чтению правил. После лимита в чат уходит канон первой строкой; токен оркестратор не печатает.

**Следующий шаг:** прочитать бюджет чата §5 и правило выбора моделей; затем ответить в чате, принят ли срез (или снова `/opsx:apply kit-session-noapi-visibility-and-ru-progress`).

План по-прежнему дописывает правила kit, не код 1С. Срезы «Русский progress» и «Маркер только при BSL» ещё не начаты.

## Что меняется в постановке

На этом срезе постановка не менялась: правились только правила kit (бюджет чата, выбор моделей, FAQ, cue соседних правил, строка про Opus 5).

### К сведению

- Счёт пунктов §1b полного тела после этого среза = 9 (добавлен пункт «канон»). Пункт «язык» — зона следующего среза.
- В правиле выбора моделей и в промпте архитектора слово «эскалация» остаётся в названии политики «закрытая эскалация»; чатовая строка при отсутствии слага — «Модель архитектора: Opus 5», без «недоступна» / «сборка».
- `command-session-persistence.mdc` не трогали.

## Технический аудит (для движка OpenSpec)

Узкий прогон на границе среза S1 (incremental). Постановка не менялась (`mtime(design.md)` = `last_challenge_at`) → Layer 4 SKIPPED-novelty.

Статическая сверка Primary S1:

- Scenario «Канон в том же ходе»: stub §5 и полное тело §5 содержат дословный канон и триггер «первая строка»; `model-selection.mdc` § Видимость — тот же момент.
- Scenario «Токен не печатается»: оркестратор не пишет `-noapi` и не говорит «включился noapi».
- Scenario «Фон не отменяется»: вызов не отменяется; канон после фона не повторяется.
- Scenario «Токен не требует канона лимита»: явный `-noapi` без памяти не требует канона лимита.
- Scenario «FAQ токен и память»: два абзаца в `faq-kit.md`.
- Scenario «Нет слага сильной модели — строка про Opus 5»: канон в трёх файлах; старые чатовые фразы «дорогая эскалация недоступна» сняты.
- Таблица «Роли и Task.model»: Primary без изменений.
- Исключение verify из «одно финальное сообщение» / «ноль промежуточных» — stub §5, полное тело §1/§5a, `verify-user-communication.mdc`, SKILL verify, `templates/chat-summary.md`.
- §1b пункт «канон» есть; §6 не трогали (владение среза языка).

## Источники

- `reports/verification-2026-08-19.md` (pre-apply full)
- `reports/code-map.md` (срез S1)
- `reports/handoff-acceptance-S1-2026-08-20.md`
