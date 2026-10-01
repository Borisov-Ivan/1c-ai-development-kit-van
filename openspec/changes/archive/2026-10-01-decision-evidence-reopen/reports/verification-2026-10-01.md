---
verify_mode: pre-apply
change: decision-evidence-reopen
date: 2026-10-01
verdict: GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: APPROVE
  layer_5_implementation_readiness: PASS
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 1
  accepted_tasks: []
  closed_decisions:
    - id: apply_refuted_premise_no_stop
      summary: "Реализация не останавливается при опровержении предпосылки закрытого решения; срез дописывается, опровержение подхватывает следующая проверка."
      closed_at: "2026-10-01"
      source: verify-user-answer
    - id: archive_always_asks_quality_traces
      summary: "Архив всегда показывает открытые замечания качества и задаёт вопрос, даже после ответа архив на развилке последнего среза."
      closed_at: "2026-10-01"
      source: verify-user-answer
    - id: acceptance_card_shows_remainder
      summary: "Карточка передачи на приёмку показывает номер среза, последний ли он и что осталось."
      closed_at: "2026-10-01"
      source: verify-user-answer
    - id: untested_acceptance_mark
      summary: "Фраза «принято без проверки» принимает срез и записывает отсутствие прогона."
      closed_at: "2026-10-01"
      source: verify-user-answer
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-10-01T22:17:46"
    design.md: "2026-10-01T22:18:34"
    tasks.md: "2026-10-01T22:18:43"
    debug.md: "2026-10-01T22:18:46"
    specs/chat-surface-clarity/spec.md: "2026-10-01T19:04:42"
    specs/review-quality-disposition/spec.md: "2026-10-01T18:17:37"
    specs/value-efficient-verify/spec.md: "2026-10-01T18:17:28"
    specs/verify-stop-repeat/spec.md: "2026-10-01T22:17:49"
  last_challenge_at: "2026-10-01T22:09:11"
  artifact_hashes:
    proposal.md: "4ebad2cb8798a92f231f46ad043e8d1616d0bd9b61c4fcd4c007134858c5e3dd"
    design.md: "093af2ef55426d98847805409f9bbc1a32cd484538169d680f4da927e6843eb6"
    tasks.md: "24a2c42ad94207a5241554cfde3884eb529dcdc39a4bd9c22293d05d009bebc9"
    tasks.md#normalized: "24a2c42ad94207a5241554cfde3884eb529dcdc39a4bd9c22293d05d009bebc9"
    debug.md#without-slice-gate: "7fddb2c7e5d713fefeaace85f47baa58d02cbf57c62e2b1f5187806aee50b272"
    specs/chat-surface-clarity/spec.md: "3cf7f4e6c6cda898797b90a32796a3cdab6173d1c79e7b9aa1240006afae2f8b"
    specs/review-quality-disposition/spec.md: "022c99684d8611b0201d9f11b9c5846fd97e0c3939e1b8443af7084ae589caed"
    specs/value-efficient-verify/spec.md: "c2bca7ea928ccc12cb58d98610958d9537ea3879f842574ecbd3077e26bf5864"
    specs/verify-stop-repeat/spec.md: "5bf215c4b8d73ad2cd9d66ab509dc131801f5fb95f034b1590c0d757b376d546"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints:
    apply_refuted_premise_no_stop: "daeff81a7573f67225e73db1c8a2ffc65fbfa69764a2f2cfd509c48dd85204f3"
    archive_always_asks_quality_traces: "06511820b81d555548212b3011b042f87707c8da494b0ee2d4c9483338e0eab0"
    acceptance_card_shows_remainder: "9c9c5dcb7921aa01d890140ea52cfe760dd93b4f0384b42de4a94798bfc3d9f1"
    untested_acceptance_mark: "9c5b415d5ec20a66cc08576585e97a7ca4e99c4db2ccb4368208001e003603ab"
  rules_versions:
    .cursor/rules/vertical-slices.mdc: "f379aa3f82c1d84ef02906b8f14917dff0a84c9967c101f90a6094fec587170c"
    .cursor/rules/openspec-specs-gate.mdc: "9724d7079e9630844d16bce0b5b664e29929da2136fb3a8f19f3b61e1a52c867"
    .cursor/rules/code-truth-gate.mdc: "bb7ecbbf53bd3b877b36b184eab851ca9f3f24db5f657f154df22029354ce579"
    .cursor/rules/precedent-regression-gate.mdc: "875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641"
    .cursor/rules/architect-gate.mdc: "0018ef689c9fbe515cb458c1203f09a08c11287ee2f7435b7007980ef2e6116a"
  check_cache:
    hygiene-checkboxes: pass
    slice-gate-markers: pass
    user-task-contract: none
    external-contract-schema: absent-no-event
    external-validity: pass
    scenario-coverage: "46/46"
    code-truth: ok-pre-apply
    precedent-regression: precedent-documented
    loop-detection: pass
    problem-solution-trace: pass
    design-challenge: "repaired-from-challenge"
    task-readiness: pass
  invalidation_map:
    hygiene-checkboxes: first-run
    slice-gate-markers: first-run
    user-task-contract: first-run
    external-validity: first-run
    scenario-coverage: first-run
    code-truth: first-run
    precedent-regression: first-run
    loop-detection: first-run
    problem-solution-trace: first-run
    design-challenge: first-axis
    task-readiness: first-run
---

## Резюме для разработчика

decision-evidence-reopen — можно запускать apply. В карточке выбора утверждение о текущем поведении стоит рядом со ссылкой на место в коде, а если код потом это опровергает — заказчику один раз возвращается тот же вопрос.

План меняет скиллы проверки, постановки, реализации, ревью и архива. Меняются только тексты скиллов и правил kit. Дописал в постановку, откуда берётся опровержение, когда внешнее условие снова блокирует продолжение и какие архитектурные отчёты дают строку о непроверенной простоте.

Тестовые каталоги fixture останутся видны в списке задач. Лишняя защита убирается из задач только если в замечании есть рецепт, что именно убрать; иначе записывается причина оставить как есть.

**Следующий шаг:** `/opsx:apply decision-evidence-reopen`

Полный отчёт: openspec/changes/decision-evidence-reopen/reports/verification-2026-10-01.md

## Что меняется в постановке

Правки идут в шаблон карточки выбора, журнал решений проверки, скилл проверки, создание и дополнение задачи, реализацию, ревью, архив и правило простоты архитектурных отчётов. Код конфигурации 1С не входит в объём.

Четыре среза независимы по приёмке. Сначала возврат решения по опровергнутой предпосылке, затем сигнал упрощения, затем след замечания качества до архива, затем строка места среза в передаче на приёмку.

Связанные решения: ADR-0003, ADR-0012, ADR-0013, ADR-0014. Контракты архива не отменяются: таблица последствий в постановке фиксирует дополнение. База знаний проекта не заведена.

## К сведению

Каталоги `fixture-*` остаются в репозитории и попадают в обзор, статус и массовый архив. Отдельного исключения в этой задаче нет.

## Технический аудит (для движка OpenSpec)

Первый прогон, `verify_depth: full`, кэша не было. `verify_mode: pre-apply`. Реестра внешнего контракта нет, события из закрытого перечня нет — контроль внешней валидности PASS без вопроса.

Layer 1: PASS. Чекбоксы, маркеры `<!-- slice-gate -->` у S1–S4, `form_mode: n/a`. Автоправок гигиены нет.

Layer 2: PASS.
- User Task Contract pre-check: none.
- Опора на прошлый контроль среза S1–S4: взят `reports/quality-control-2026-10-01.md` (verdict OK, 46/46). Набор названий сценариев и текст обязательного пункта приёмки после дописки не менялись. Новый полный контроль с нуля не создавался.
- Code-Truth: `openspec/project.md` нет, якорей процедур BSL нет. pre-apply, phantom-symbol нет.
- Precedent: MODIFIED к архивным ADDED (`verify-stop-repeat`, `value-efficient-verify`, `review-quality-disposition`, `chat-surface-clarity`) дополняют WHEN/THEN. `## Blast Radius` заполнен. INFO `precedent-documented`. Invariant KB нет. Supersedes Load-Bearing ADR нет.
- Ручных маркеров конфигурации нет.

Layer 2.5: PASS. `TopicReopen` = 0, `PatchRounds` = 1 на S1/S2/S4 (одна секция Extend), порог 3 не достигнут.

Layer 3: PASS. Пункты Why покрыты требованиями, у требований есть сценарии, сценарии сидят в срезах и приёмке. Маркеров implementation-leak нет. `comment_suffix` пуст.

Layer 4: сырой отчёт `reports/design-challenge-2026-10-01.md` — CHALLENGE, confidence high, architectural_forks 0. Классификатор: G1–G6 `implementation_invariant`, G7 `assumption_deferrable`. Закрытые решения не оспаривались, reopen-blocked нет. Дописка в том же прогоне (`repair_attempt: 1`) закрыла G1–G6 в design/tasks/spec; G7 записан в Assumptions как известный остаток. Повторный независимый разбор не запускался: те же темы, наблюдаемое правило сценариев не сменено. Для формулы итога слой закрыт допиской (`APPROVE` в YAML). `last_challenge_at` — время отчёта разбора.

Layer 5: первый отчёт `architecture-task-readiness-2026-10-01.md` — ГОТОВО С ЗАМЕЧАНИЯМИ, GAP по списку режимов простоты. После дописки повтор `architecture-task-readiness-2026-10-01-2.md` — ГОТОВО, открытых вопросов 0. PASS.

## Источники

- `reports/quality-control-2026-10-01.md`
- `reports/design-challenge-2026-10-01.md`
- `reports/architecture-task-readiness-2026-10-01.md`
- `reports/architecture-task-readiness-2026-10-01-2.md`

Алерты: `precedent-documented` (INFO). `external-contract-open` и родственные не сработали.
