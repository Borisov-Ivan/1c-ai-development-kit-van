---
verify_mode: pre-apply
change: kit-protocol-coherence
date: 2026-10-04
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: PASS
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions:
    - id: batch-on-sliced-change
      choice: run-all-slices-accept-at-end
      summary: "Явный пакет на заявке со срезами прогоняет оставшиеся срезы без паузы, приёмка один раз в конце."
      authority: customer-direct
      premise:
        claim: "иногда нужно прогнать все срезы и принять в конце"
        anchor: ".cursor/commands/opsx-apply.md:21"
      decided_at: "2026-10-04"
    - id: acceptance-one-journey
      choice: narrow-primary-keep-slices
      summary: "Обязательный ход приёмки среза один, остальные сценарии необязательны."
      authority: customer-direct
      premise:
        claim: "обязательный ход приёмки среза один, остальные сценарии необязательны"
        anchor: "openspec/changes/kit-protocol-coherence/reports/quality-control-2026-10-04.md"
      decided_at: "2026-10-04"
  refuted_premises: []
  open_decision_id: null
  decision_round: 2
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-10-04T20:36:15"
    design.md: "2026-10-04T21:48:24"
    tasks.md: "2026-10-04T21:50:23"
    specs/kit-protocol-coherence/spec.md: "2026-10-04T20:55:15"
    debug.md: "2026-10-04T21:49:16"
  last_challenge_at: "2026-10-04T22:13:00+09:00"
  artifact_hashes:
    proposal.md: bf4dbd9e147b3fe6054b85ce65925e06cbf97c0a6978603a53f4089c6af1a1be
    design.md: 36e4afa05e8883ae71debf358eebdb6f0ffc19131edbc13bcfcb34609bc33bfa
    design.md#axis: d7fc1b1013e882e2a1165ce8bb5853d1921cf8413149cc32095c9730fbbe640f
    tasks.md: 80ec16f5522f028c4d1b5430f2ce473b00aae514b41f3bdac4356b61a3f728e3
    tasks.md#normalized: 80ec16f5522f028c4d1b5430f2ce473b00aae514b41f3bdac4356b61a3f728e3
    specs/kit-protocol-coherence/spec.md: d2b4cb3c0134677a312c65018032ee2a6648200b380745774e2f6ccf33bb3f06
    debug.md: 3c429985b3a99f7b1dca11e09242706b96d1c498b2727997e5197658da986475
    debug.md#without-slice-gate: 3c429985b3a99f7b1dca11e09242706b96d1c498b2727997e5197658da986475
  external_contract_digest: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  decision_fingerprints:
    batch-on-sliced-change: 6c5a93ad2ec589f11279903e290fb014602c53303d9f36ea6ea784ace9d8e3fe
    acceptance-one-journey: c9f6b6dbb18a3723670acb00e23139305b6847624a265ac0803e96ac13e25ac3
  rules_versions:
    .cursor/rules/vertical-slices.mdc: 9f73d8c12d29024a5f7a3e4e0671811ac605bad10ddafac8794682b7f7899ff8
    .cursor/rules/code-truth-gate.mdc: bb7ecbbf53bd3b877b36b184eab851ca9f3f24db5f657f154df22029354ce579
    .cursor/rules/precedent-regression-gate.mdc: 875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641
    .cursor/rules/openspec-specs-gate.mdc: 9724d7079e9630844d16bce0b5b664e29929da2136fb3a8f19f3b61e1a52c867
    .cursor/rules/architect-gate.mdc: 0ce5315d471bbe04e960571413bb39198ed48e0209c79aab727393d7bce728ac
    .cursor/skills/openspec-verify-change/SKILL.md: cfa64b41802f642342084931ef14b6a093b0a6b9d66cdada1e8308059ed1f141
  check_cache:
    hygiene-checkboxes: PASS
    slice-gate-markers: PASS
    user-task-contract: PASS
    external-contract-schema: PASS
    external-validity: PASS
    scenario-coverage: PASS
    code-truth: PASS
    precedent-regression: PASS
    loop-detection: PASS
    problem-solution-trace: PASS
    design-challenge: CHALLENGE
    task-readiness: PASS
    premise-reconciliation: PASS
  invalidation_map:
    hygiene-checkboxes: "первый прогон, кэша нет"
    slice-gate-markers: "первый прогон, кэша нет"
    user-task-contract: "первый прогон, кэша нет"
    external-contract-schema: "первый прогон, кэша нет"
    external-validity: "первый прогон, кэша нет"
    scenario-coverage: "первый прогон, кэша нет"
    code-truth: "первый прогон, кэша нет"
    precedent-regression: "первый прогон, кэша нет"
    loop-detection: "первый прогон, кэша нет"
    problem-solution-trace: "первый прогон, кэша нет"
    design-challenge: "первый прогон, кэша нет"
    task-readiness: "первый прогон, кэша нет"
    premise-reconciliation: "первый прогон, кэша нет"
---

## Резюме для разработчика

kit-protocol-coherence — до старта нужен ваш выбор по логике конца пакетного запуска.

Уже зафиксировано: явный пакет на заявке со срезами прогоняет оставшиеся срезы без паузы, приёмка один раз в конце; без флага пауза на каждом срезе остаётся. Обязательный ход приёмки одного среза — один, остальные сценарии того же среза необязательны.
Новый вопрос: что показывает эта одна приёмка в конце. Прежние решения не пересматриваются.

**Что решить: что человек видит, когда пакет дошёл до конца**

Возврат к разработке берёт самую раннюю незакрытую передачу и спрашивает про один срез (`.cursor/skills/openspec-apply-change/SKILL.md:151`). Правило срезов на передаче тоже заканчивает сессию одним срезом (`.cursor/rules/vertical-slices.mdc:176`). План обещает одну приёмку в конце пакета, но не говорит, видны ли в ней главные проверки всех прогнанных срезов или только последнего. Пока это не записано, два текста снова разойдутся, и ранний срез можно закрыть не глядя.

- **A. Все прогнанные срезы в одной карточке** — один вопрос в конце, в нём главная проверка каждого среза; один ответ принимает их вместе или возвращает вместе. Карточка длиннее, зато ранний срез не проходит мимо глаз.
- **B. Только последний срез** — вопрос один и короткий. Ранние срезы в него не входят, их главную проверку в этот момент не видно.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify kit-protocol-coherence`.

Полный отчёт: openspec/changes/kit-protocol-coherence/reports/verification-2026-10-04.md

План сводит расхождения текстов команд и правил в `.cursor/`: одно место остаётся хозяином шага, второе на него ссылается. Код конфигурации, формы и макеты не меняются.

## Решения до apply

### Конец пакетного запуска

**Цель:** один и тот же момент маршрута не должен требовать двух разных действий. Обе ветки оставляют уже выбранное: пакет идёт без паузы на каждом срезе, вопрос один в конце.

**Что в текстах сейчас.** Возврат к разработке в `.cursor/skills/openspec-apply-change/SKILL.md:151` ищет самую раннюю запись ожидания и спрашивает про один срез. Передача в `.cursor/rules/vertical-slices.mdc:176` заканчивает сессию карточкой одного среза и не спрашивает в том же ходе. Правило срезов о пакете не знает (`.cursor/rules/vertical-slices.mdc:173`).

**Что предлагает план.** Явный пакет прогоняет оставшиеся срезы без этих пауз и отдаёт одну приёмку в конце. Форма этой одной приёмки не записана.

**Почему это выбор.** «Одна приёмка» одинаково читается как карточка на все прогнанные срезы и как карточка только последнего. От этого зависит, что человек увидит и какие срезы закроет одним ответом.

**Варианты.**

- **A. Все прогнанные срезы в одной карточке** — в конце один вопрос с главной проверкой каждого среза; один ответ принимает их вместе или возвращает вместе. **Компромисс:** карточка длиннее.
- **B. Только последний срез** — вопрос один и короткий. **Компромисс:** главную проверку ранних срезов в этот момент не видно.

**Влияет на:** что показывает чат, когда пакетный запуск дошёл до конца и приёмка ещё не подписана.

**Что изменится после выбора.** В постановке появится один наблюдаемый конец пакета, и тексты команды, скилла разработки и правила срезов будут ссылаться на него.

## Что меняется в постановке

Меняются тексты команд, скиллов и правил маршрута в `.cursor/`. Точка правки — абзац, который агент читает в этот момент: команда на входе, обзор маршрута, всегда включённое правило. Код конфигурации не затрагивается. Решения ADR-0001, ADR-0007 и ADR-0014 не отменяются. Архив про нейтральность поставки эта заявка не расширяет.

### К сведению

В разборе плана нет сравнения двух более простых вариантов рядом с обоснованием. На этот выбор это не влияет.

## Технический аудит (для движка OpenSpec)

Первый прогон, `verify_depth: full`. Прошлого `verification-*.md` нет. Прошлый `quality-control-2026-10-04.md` не переиспользован: обязательный пункт приёмки после него сужен.

- Layer 1 Hygiene: PASS. Чекбоксы, маркеры конца среза и режим форм на месте. Автоправок нет.
- Layer 2 Internal Coherence: PASS. Внешний контракт: секции реестра нет, события из закрытого перечня с `EC-*` нет. Срезы: `reports/quality-control-2026-10-04-2.md`, вердикт OK, алертов нет. Code-truth: технических якорей процедур нет, `openspec/project.md` нет, phantom-symbol нет. Precedent: в дельте нет `MODIFIED`/`REMOVED`; `openspec/knowledge/_index.yaml` нет; `Supersedes` load-bearing ADR в design нет.
- Layer 2.5 Loop Detection: PASS. Записей `## Slice Gate Decisions` и `## Extend —` нет. `TopicReopen` 0, `PatchRounds` 0.
- Layer 3 Problem-Solution Trace: PASS. Семь требований покрывают Why. У каждого требования есть сценарий. 25 сценариев названы в срезах и в приёмке. Маркеров implementation-leak в `THEN` нет. `comment_suffix` пуст.
- Layer 4 Independent Challenge: CHALLENGE. Отчёт `reports/design-challenge-2026-10-04.md`. `last_challenge_at` обновлён.
- Layer 5 Implementation Readiness: PASS. `reports/architecture-task-readiness-2026-10-04.md`, вердикт готово, пробелов нет. Маркеров ручной конфигурации нет. Критерий 7 не `SUBOPTIMAL`.

### Post-challenge classifier

- Снять пакет для заявки со срезами: drop, `reopen-blocked: batch-on-sliced-change`. В чат не выносилось.
- G1 конец пакета: после классификатора это выбор наблюдаемого поведения (карточка на все срезы или только последний). Закрытая ось «приёмка один раз в конце» оба варианта допускает и ни один не назначает. Класс decision. Repair не запускался.
- G2 отсылка из правила срезов и хозяин флага, G3 поле «исход дополнения», G5 строка границы в Non-Goals: `implementation_invariant`. В смешанном отчёте ждут ответа по G1, в этом проходе не правились.
- G4 строка диспетчера: упрощение без одного рецепта «убрать» со ссылкой на строку. Решение 6 постановки строку предписывает. В чат не выносилось. Удаление не делалось.
- Предпосылки закрытых решений не опровергнуты. `## Premise conflicts` в отчёте разбора нет.

### Контроль простоты

`reports/architecture-new-2026-10-04.md` (`mode: plan-review`) не содержит `## Simplicity Check`. Строка «к сведению» выше. В постановку не писалось.

## Источники

- `openspec/changes/kit-protocol-coherence/reports/quality-control-2026-10-04-2.md`
- `openspec/changes/kit-protocol-coherence/reports/design-challenge-2026-10-04.md`
- `openspec/changes/kit-protocol-coherence/reports/architecture-task-readiness-2026-10-04.md`
- Алерты: нет блокирующих кодов Layer 2. Решение: `batch-end-card` (наблюдаемый конец пакета).
