---
verify_mode: pre-apply
change: tz-tech-project
date: 2026-09-23
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
  repair_attempt: 1
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  last_challenge_at: "2026-09-23T10:59:00"
  artifact_hashes: {}
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints: {}
  rules_versions: {}
  check_cache: {}
  invalidation_map:
    design-challenge: "design axis text changed by repair attempt 1"
    scenario-coverage: "new scenario about missing object and answer protocol"
classifier:
  implementation_invariant:
    - two-options-on-question
    - hours-lower-bound-times-coefficient
    - preserve-answers-same-wording
    - template-edit-does-not-change-run
    - do-not-copy-overview-entry-pause
  dropped:
    - two-phase-output: "один запуск по-прежнему пишет оба файла"
    - one-file-output: "ось двух файлов сохранена"
    - template-runtime-ssot: "ось копий в навыке сохранена"
  supersedes: none
  repair_next: "repair-from-verify attempt 2, затем полный re-verify"
---

## Резюме для разработчика

tz-tech-project — постановка ещё раз дополняется без смены выбранной команды. В требованиях зафиксированы два варианта у вопроса, правило часов из справочника, сохранение ответов и то, что правка папки шаблонов не меняет следующий запуск.

**Следующий шаг:** после дописывания постановки проверка повторяется сама.

## Что доработать в постановке

### Рекомендации

- Пункт листа: формулировка, не меньше двух вариантов, место для ответа.
- Часы из прозы: нижняя граница строки справочника, умноженная на коэффициент; надбавка только если фактор назван в задании. Таблица в документ не попадает.
- Повторный запуск не стирает ответ у вопроса с той же формулировкой.
- Правка только `template/Техпроект` не меняет часы и дыры следующего запуска.
- В навык копируются каркас и голос обзора, не ожидание подтверждения в чате.

Развилка «сначала только лист, техпроект после ответов» не выносится: один запуск по-прежнему пишет оба файла.

## Что меняется в постановке

Команда `/opsx:techproject` и навык пишут `<имя>-вопросы.md` и `<имя>-техпроект.md` рядом с файлом задания. Выгрузка `src/КАСК/cf/` только читается. Файлы обзора не меняются.

## Технический аудит (для движка OpenSpec)

- Layer 2: PASS по `reports/quality-control-2026-09-23-3.md` (вердикт OK) до второй правки. После правки покрытие пересчитывается следующим прогоном.
- Layer 2.5: PASS. AcceptLoop=0. В `debug.md` две секции Extend, не Slice Gate.
- Layer 4: CHALLENGE `reports/design-challenge-2026-09-23-2.md`. Classifier: только implementation_invariant. Равноправных развилок архитектор не оставил. Repair attempt 2.
- Layer 5: PASS, триггер ручной конфигурации и неизвестного перехвата не сработал.
- Хэши входов этого прогона не зафиксированы до второй правки; следующий отчёт считает хэши заново.

## Источники

- `reports/quality-control-2026-09-23-3.md`
- `reports/design-challenge-2026-09-23-2.md`
