---
verify_mode: pre-apply
change: fix-route-from-analysis
date: 2026-11-05
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: FAIL
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: NOT-RUN
  layer_4_independent_challenge: NOT-RUN
  layer_5_implementation_readiness: NOT-RUN
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks:
    - S1.1
    - S1.2
    - S1.3
    - S1.4
    - S1.5
  closed_decisions:
    - id: card_rule_binding
      summary: "Правило карточки обязательно. Починка с прежней суммой и справкой остаётся в открытой приёмке, без вопроса о срезе и без отдельного шага проведения. Вариант, который проведение не выполняет, в карточку не ставится. Убрать это правило из текста можно только новым ответом."
      closed_at: "2026-11-05T14:12:00+09:00"
      source: verify-user-answer
      confirmed_by: user
      authority: customer-direct
      external_contract_id: EC-1
      premise:
        claim: "Правило уже стоит в тексте заявки; ответ делает его обязательным, чтобы снять его можно было только новым ответом."
        anchor: "openspec/changes/fix-route-from-analysis/debug.md#Extend — 2026-11-05"
  refuted_premises:
    - decision_id: card_rule_binding
      refuting_anchor: "openspec/changes/fix-route-from-analysis/debug.md:27"
      report: "openspec/changes/fix-route-from-analysis/reports/design-challenge-2026-11-05.md"
      detected_at: "2026-11-05T15:45:04+09:00"
      fingerprint: "f4628a6134ec0a040c684c985e197a09c6b5a0a0ff727e92cc0455c67d0be39a"
  open_decision_id: EC-1
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "подтвердить обязательность правила карточки: дополнение от 2026-11-05 не содержит фразы, что убрать правило можно только новым ответом"
  artifacts_mtime:
    proposal.md: "2026-11-05T16:42:00+09:00"
    design.md: "2026-11-05T16:42:10+09:00"
    tasks.md: "2026-11-05T16:42:37+09:00"
    debug.md: "2026-11-05T16:42:42+09:00"
    specs/pipeline-light-route/spec.md: "2026-11-05T16:42:18+09:00"
  last_challenge_at: "2026-11-05T15:45:04+09:00"
  artifact_hashes:
    proposal.md: "30067a756f9fd5eee4babf0638612a818eb30abf673193baecb6f14e207fa68a"
    design.md: "163cdcce7c38749ba006c3854509612618125a01c9d85192f350428d289123c9"
    design.md#axis: "fd3351e8d2a5b629256afa506b28d29eb0fb5b3df31afc343599c73c347e16f3"
    tasks.md: "287f06a5cd582e7d555747d4f29c49a1d821ad7fced96bcc818bbd9ea188815f"
    tasks.md#normalized: "e63c9469e971ee00ecc3d4a37a4f86ea1df57a292e363c33a26e93eb7b2ed6b6"
    specs/pipeline-light-route/spec.md: "52dcc73f93cb6e2128893ffed9af164f9947ce5ea3b7cf0b2b2be55439f30a44"
    debug.md#without-slice-gate: "a57e4ed4067bfe9c45de43316cb8b5532f1651161170ebf06ee26bfa113804a8"
  external_contract_digest: "b3aa96ace1d1dedafed03fcccde69cc381ac062f81642a21b57e72ac954d892f"
  decision_fingerprints:
    card_rule_binding: "a75ac88cc6891d4196c37dda5c0ed971555d7c83ae5ec786dc8fbe119a1efedf"
  rules_versions:
    .cursor/skills/openspec-verify-change/SKILL.md: "b650e6a2021b1d359c49b169a488cd7235d99ceb8f43eb62cae3e17a71d7e720"
    .cursor/skills/openspec-extend-change/SKILL.md: "a307c68b009b7857032d4aebb291db697dc3b4abddee5f6d9c3b82ce2cf3d1da"
    .cursor/rules/vertical-slices.mdc: "2c819ad1565f9a4817c1528c1340f99c33e2429a0d335415f564f21043446bd9"
    .cursor/rules/openspec-specs-gate.mdc: "14459abbd63cdd7140cd58b8ac7d0321a563c29999d1e026805e37ec37a76610"
    .cursor/rules/code-truth-gate.mdc: "bf8b7f6e9695a9f36b513faff3d9ba78499f283ebf2aa0ef86cacec957b9754f"
    .cursor/rules/precedent-regression-gate.mdc: "875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641"
    .cursor/rules/architect-gate.mdc: "733c4498f4bcded131a12f0a44818254b5da077af3438a51240a1e8ab5e9f000"
  check_cache:
    hygiene-checkboxes@tasks: PASS
    slice-gate-markers@S1: PASS
    external-validity@change: FAIL
    loop-detection@S1: PASS
    premise-reconciliation@card_rule_binding: REFUTED
  invalidation_map:
    external-validity: "EC-1 closed_at раньше detected_at опровержения; тема высокого авторитета снова открыта"
    premise-reconciliation: "ответа новее detected_at по card_rule_binding нет; тот же fingerprint"
    design-challenge: "ось fd3351e8 отличается от 1ca6adf3; не запущен: остановка до разбора"
    scenario-coverage: "добавлен сценарий про слова вопроса; не пересчитан"
    task-readiness: "добавлена S1.10; не запущен"
    problem-solution-trace: "не пересчитан: остановка до связей"
    code-truth: "не пересчитан"
    precedent-regression: "не пересчитан"
    user-task-contract: "не пересчитан"
    loop-detection: "пересчитан: TopicReopen 0, PatchRounds 3 при идентичности тем"
scope_gate_decision: silent
classifier:
  blocker: premise-refuted
  decision_id: card_rule_binding
  external_contract_id: EC-1
  gaps_deferred:
    - id: G9
      class: implementation_invariant
      reason: "вход не называет оставшийся шаг; прошлый разбор, в этом прогоне не переоткрывался"
    - id: G10
      class: implementation_invariant
      reason: "образец пакета по-прежнему зовёт первую проверку; прошлый разбор"
    - id: G11
      class: implementation_invariant
      reason: "фраза про мёртвую ветвь в общем шаблоне не ограничена карточкой проверки; прошлый разбор"
    - id: G12
      class: implementation_invariant
      reason: "подтверждение без номера не стыкуется с запретом голого да; прошлый разбор"
  repair_next: "не в этом проходе: сначала ответ пользователя; затем user-extend --from-verify"
---

## Резюме для разработчика

fix-route-from-analysis — до старта нужен ваш выбор по логике обязательности правила карточки.

Уже зафиксировано: починка с прежней суммой и справкой остаётся в открытой приёмке, без вопроса, куда её положить, и без отдельного шага «проводится». Вариант, который проведение не выполняет, в карточку не ставится.

Новый вопрос: дополнение, на которое опирается запрет снять это правило, самой запрещающей фразы не содержит. Текст правил в заявке от этого ответа не переписывается.

**Что решить: остаётся ли запрет снимать правило карточки без нового ответа**

Ответ уже записан так: правило карточки обязательно, и снять его можно только новым ответом. Опора — дополнение от 5 ноября. В нём сказано, что в заявку дописали границу живой ветви и что следом нужна полная проверка (`openspec/changes/fix-route-from-analysis/debug.md:30`). Фразы «убрать правило можно только новым ответом» в этом дополнении нет. Она стоит в разделе зафиксированных решений и ссылается на то же дополнение. Пока опора не подтверждена заново, запрет снимать правило этой записью не держится.

- **A. Запрет остаётся** — починка с прежней суммой по-прежнему не спрашивает, куда её положить, и вариант без проведения в карточку не попадает. Снять правило из текста позже без нового ответа будет нельзя.
- **B. Запрет снимается** — текст правил сейчас не трогаем. Если правило потом выпадет из заявки, проверка может не остановиться вопросом.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify fix-route-from-analysis`.

Как задавать вопрос словами уже записанного результата, в заявку уже внесено. Эту добавку разберём после ответа.

Полный отчёт: openspec/changes/fix-route-from-analysis/reports/verification-2026-11-05-3.md

Модулей конфигурации эта заявка не касается. Меняются тексты правил набора: куда класть починку, какие варианты карточки спрашивать, какими словами показывать вопрос и откуда брать следующий шаг после ответа.

## Что доработать в постановке

### Рекомендации

- **Опора обязательности:** нужен новый ответ, держится ли запрет снять правило карточки без нового ответа. Текст правил этим ответом не переписывается.

### Развилки

#### 1. Опора обязательности правила карточки

**Цель ЗНИ:** починка с прежним проведением, суммой и справкой не спрашивает, куда её положить. Обе ветки этот текст сейчас не трогают. A закрепляет запрет снять его без нового ответа. B этот запрет снимает.

**Что в тексте сейчас.** Дополнение от 5 ноября (`debug.md:30`) описывает границу живой ветви и полную проверку следом. Фразы, что убрать правило можно только новым ответом, там нет. Эта фраза стоит в `design.md`, раздел «Решения verify (зафиксировано)», и в журнале решений, который ссылается на то же дополнение.

**Что предлагает план.** В пару попадают только варианты, которые выполняют уже сказанное. Починка с прежней суммой остаётся в открытой приёмке. Отдельная фраза об обязательности в самом дополнении не стоит.

**Почему это развилка.** Ссылка опоры не доходит до места, где возникает обязательность. Закрыть это правкой проверки нельзя: нужен новый ответ.

**Варианты решения.**

- **A. Запрет остаётся** — починка с прежней суммой не спрашивает, куда её положить; вариант без проведения в карточку не попадает. **Компромисс:** снять правило из текста позже без нового ответа будет нельзя.
- **B. Запрет снимается** — текст правил не трогаем. **Компромисс:** если правило потом выпадет из заявки, проверка может не остановиться вопросом.

**Влияет на:** останется ли сегодняшний ответ обязательным, когда текст правил снова поменяют.

**Что изменится после выбора.** Новый ответ записывается поверх этой опоры. Тексты правил этим выбором не переписываются. Затем проверка запускается снова.

**Источники** *(техническое):* `premise-refuted`; `card_rule_binding`; `EC-1`; `reports/design-challenge-2026-11-05.md` § Premise conflicts. Поля ответа человека этим прогоном не менялись. `confirmed_by: user` заново не ставился.

## Что меняется в постановке

Починка с прежним проведением, суммой и справкой не становится отдельным шагом. Спрашивают, только когда оба варианта выполняют уже сказанное и расходятся в результате или в моменте, когда результат уже можно принять. Один живой вариант продолжается в том же запуске. После настоящего ответа следующий шаг берётся из таблицы глубины. Вопрос, который всё же задаётся, показывается словами уже записанного результата; путь к заметке остаётся в отчёте.

**Расширение / конфигурация:** конфигурация 1С не меняется.

**Точки изменения:**

- `.cursor/rules/vertical-slices.mdc` — куда класть починку с прежним результатом. Уже записано.
- `.cursor/skills/openspec-verify-change/SKILL.md` — состав карточки, вход проверки, слова вопроса перед показом. Ещё не закрыто задачами.
- `.cursor/docs/templates/decision-block.md` — та же граница пары и слова вопроса.
- `.cursor/skills/openspec-verify-change/templates/chat-summary.md` и `card-decision.md` — следующий шаг из таблицы глубины и слова вопроса.
- `.cursor/skills/openspec-extend-change/SKILL.md` — подтверждение без номера, когда заявка и правило уже названы.

**Что НЕ меняется:** уже подписанная приёмка; полная проверка при смене формулы, момента правила, порядка шагов или сценария; вопрос на втором возврате одной и той же темы. Разбор, создание, пошаговый разбор, реализация и архив в это правило не входят.

**Связанные ADR / KB / архив:** ADR-0014, ADR-0013, ADR-0012.

## К сведению

Четыре стыка текста из прошлой независимой проверки плана по-прежнему ждут дописки после ответа и отдельным вопросом не стоят. Добавка про слова вопроса в этом прогоне не разбиралась: открытая опора останавливает прогон раньше. Приёмка среза «Маршрут починки с прежним результатом» открыта. Порог повторных правок не остановил прогон: три дополнения относятся к разным темам.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Hygiene):** PASS. Автоправок нет. Чекбоксы у S1.1–S1.10 и S1.accept на месте. Один `<!-- slice-gate -->`. `form_mode: n/a`. Маркеров ручной конфигурации в этом проходе не искали: остановка раньше.
- **Layer 2 (Internal Coherence):** FAIL, класс decision. Блокер `premise-refuted` / `external-contract-open` по EC-1. `closed_at` 2026-11-05T14:12:00 раньше `detected_at` 2026-11-05T15:45:04. Записи ответа новее `detected_at` по `card_rule_binding` нет. `open_decision_id` остаётся EC-1. Поля `closed_decisions`, `confirmed_by`, `confirmation` не переписывались. QC, code-truth и precedent не запускались.
- **Layer 2.5 (Loop Detection):** PASS. `AcceptLoop(S1)` = 1. `PatchRounds(S1)` = 3 (`## Extend —` 2026-10-16, 2026-11-05, 2026-11-05 вопрос словами задачи). `acceptance_loop_max` = 3. Запасной стоп не сработал: у дополнений есть идентичность (G1–G8, G9, EC-2). `TopicReopen` = 0. Возврат по опровергнутой предпосылке в `TopicReopen` не входит. Редизайн не запускался.
- **Layer 3 (Problem-Solution Trace):** NOT-RUN. Дешёвый блокер раньше связей.
- **Layer 4 (Independent Challenge):** NOT-RUN. Триггер есть: ось `design.md#axis` `fd3351e8…` разошлась с `1ca6adf3…` в `verification-2026-11-05-2.md`, добавлен сценарий. Вызов не создавался: дешёвый блокер раньше разбора. Прошлый `design-challenge-2026-11-05.md` как результат этого запуска не подставлялся. `last_challenge_at` не обновлялся.
- **Layer 5 (Implementation Readiness):** NOT-RUN. Текст задач изменился (S1.10). Вызов не создавался. Прошлый отчёт готовности не подставлялся.

### Каскад дельты

- **verify_depth:** `full`. Новый сценарий и смена оси. Класс «замена значения» не присвоен. Первая строка таблицы глубины не применена: сценарий добавлен. `lite` недоступен: `open_decision_id` не пуст. Открытое опровержение быстрый путь запрещает.
- **EC-2:** схема валидна, `confirmation: confirmed`, `confirmed_by: user`, отпечаток сигнала совпал. Это указание из дополнения, не ответ на развилку проверки. Повторный вопрос по словам вопроса не задаётся. В `closed_decisions` парной записи нет; это не понижение авторитета и не второй сигнал EC-1.
- **Дайджест внешнего контракта:** SHA-256 от `EC-1|matches|confirmed|<fingerprint>\nEC-2|matches|confirmed|<fingerprint>`. Отпечаток `card_rule_binding` совпал с прошлым снимком (`id|closed_at|source`).
- **recomputed:** hygiene, slice-gate markers, external-validity, loop-detection, premise-reconciliation.
- **reused:** нет.
- **escalated:** none — QC, design-challenge и task-readiness не запускались.
- **Сверка предпосылок:** новых отчётов с полем premise после `verification-2026-11-05-2.md` нет. Отчёты слоёв этого прогона не создавались. Прежняя запись `refuted_premises[]` сохранена, не дублировалась.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

Единственная открытая тема — опровержение предпосылки `card_rule_binding` / EC-1. Тот же `fingerprint` `f4628a61…`. Ответа с `closed_at` позже `detected_at` нет. G9–G12 остаются `implementation_invariant` прошлого разбора и в чат не выносились. Repair Loop не запускался: decision раньше repair.

## Источники

- `openspec/changes/fix-route-from-analysis/reports/verification-2026-11-05-2.md`
- `openspec/changes/fix-route-from-analysis/reports/design-challenge-2026-11-05.md`
- Алерты: `premise-refuted`, `external-contract-open`
