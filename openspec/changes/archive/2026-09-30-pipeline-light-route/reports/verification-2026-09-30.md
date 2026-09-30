---
verify_mode: pre-apply
change: pipeline-light-route
date: 2026-09-30
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
    - id: value_change_class_by_impact
      summary: "Класс «замена значения» определяется оценкой воздействия, а не закрытым перечнем атрибутов"
      closed_at: "2026-09-30"
      source: new-stage-user-answer
      confirmed_by: user
      authority: customer-direct
      external_contract_id: EC-1
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-09-30T21:17:51"
    design.md: "2026-09-30T21:46:03"
    tasks.md: "2026-09-30T21:46:20"
    specs/pipeline-light-route/spec.md: "2026-09-30T21:18:08"
    debug.md: "2026-09-30T21:48:36"
  last_challenge_at: "2026-09-30T21:42:00+09:00"
  artifact_hashes:
    proposal.md: abf41df943140661c89f16dd125102a326c170a3b6d009e64c93d8db5929a697
    design.md: cd0ff159bd40a0b074742b5706af768ec4bf4eb022813ee43e97e60dd4b0c2cc
    design_axis: 9b6d7d11a534f71cc40a5607841834333dd91e5611455beb659dd23424456f82
    tasks.md: 6f48c8b561bf1d4645ecab32b86a59a05d0716e5237fe565c06871b7525ddf5a
    specs/pipeline-light-route/spec.md: d71b19e13cd6019949cc144cd09a7e1ee2bd5361d3910bcb6142c336527f5c6e
    debug.md: 85058e6d888cbcfae7d0e8ffac6f8cbf7d0b573b402db2d73557017a02cbb6b6
  external_contract_digest: 6e14906e86b2fa2f8548895053fcb08a357b76191dd930d9b2fc79098ca5e4ff
  decision_fingerprints:
    value_change_class_by_impact: 600f3219a235c7424d1be4b5a3398de018117de686b6f2fb5f1acf4f8fc3d118
  rules_versions:
    .cursor/rules/vertical-slices.mdc: 17615576ce482f01b9a286bb0206f22baddccd8f1f6045f14c35bfbbdab19e63
    .cursor/rules/openspec-specs-gate.mdc: e97cf9ad3a76132a05c88bf183b44410320547c9b84cf07e6f73fcea7aced6d4
    .cursor/rules/code-truth-gate.mdc: 20f25dae70359466cfeec4ac8ec1210867919c3b775f2cd8b597cd7ba7bd85f0
    .cursor/rules/precedent-regression-gate.mdc: 3921384b52ed58bc1ffa0167b3c5d5ef6f1ca8e73976de9d7d8af06c35b7b148
    .cursor/rules/architect-gate.mdc: 7927fe8d7d4c2ed61321dadf6cce0174fd1fa70fbf0ad717940f1ffeb7bb3813
    .cursor/skills/openspec-verify-change/SKILL.md: d55ad7220eda11e390e1a73ada025065e635c3f0c8201645f5bab937e23e0528
  check_cache:
    scenario-coverage@S1-S3: "reused quality-control-2026-09-30.md after repair; scenario titles and Primary text unchanged; 19/19"
    design-challenge@axis: "design-challenge-2026-09-30.md CHALLENGE; G1 G2 implementation_invariant repaired; same observable rule; not re-run"
    task-readiness@all: "architecture-task-readiness-2026-09-30.md PASS"
    task-readiness@S1.2-S1.3-S2.8: "architecture-task-readiness-2026-09-30-2.md PASS"
  invalidation_map:
    design-challenge: "first pre-apply, cache miss"
    task-readiness: "tasks.md new, then S1.2 S1.3 S2.8 after repair"
    scenario-coverage: "first run; post-repair reused"
---

## Резюме для разработчика

pipeline-light-route — можно запускать apply. Замена уже утверждённого цвета в проверенной задаче идёт сразу к реализации, архив после отметок приёмки не запускает проверку заново.

Уже зафиксировано: класс замены определяется оценкой воздействия — меняется только то, что заказчик видит или получает. Если по постановке неясно, влияет ли значение на поведение, берётся короткое мнение об одной замене; если сомнение остаётся, идёт обычная проверка.

Дополнение называет один исход: проверка не нужна, хватит короткой сверки изменённого или нужна полная проверка. Повторный отчёт ссылается на предыдущий и не копирует журнал решений и пересказ постановки. Несколько замен подряд возвращаются в текст оси с конца; если подстановка неоднозначна, класс не даётся. Архив считает постановку прежней, когда совпали тексты требований, дизайна и задач без учёта галочек.

Границы:

- Применение остановится, пока `value-efficient-verify` и `verify-stop-repeat` не в архиве.
- Порог, формула и цвет, уже занятый другим состоянием, по-прежнему идут в проверку.
- Старое значение в коде ищет задача замены; сверка имён перед архивом эту строку не видит, остаток смотрит ручная приёмка.

**Следующий шаг:** `/opsx:apply pipeline-light-route`

Полный отчёт: openspec/changes/pipeline-light-route/reports/verification-2026-09-30.md

Правки лягут в скиллы дополнения, проверки и архива, в шаблон шапки отчёта проверки и в две строки маршрута команд. Кода конфигурации 1С нет.

## Что меняется в постановке

Меняются правила трёх команд kit, не объекты конфигурации.

- Дополнение постановки: три исхода. Замена значения, которое не меняет состав данных под правилом, ведёт сразу к реализации. Старое значение в тексте требований, дизайна и невыполненных задач заменяется до выбора исхода.
- Проверка: если с прошлого отчёта менялись только такие замены, проход точечный. Полный разбор, контроль срезов и оценка готовности задач не запускаются. После такого прохода текущий текст решений становится базой, и граница среза не уходит в полный проход из-за этой замены.
- Архив: если тексты требований, дизайна, спецификаций и задач (без учёта галочек) и журнал без записей приёмки совпали с прошлым отчётом, проверка не вызывается. Полноту требований и сверку имён с кодом архив делает своими шагами.
- Повторный отчёт проверки: ссылка на предыдущий, что изменилось, без копии списка принятых задач и журнала решений.

Связанных ADR нет. Дельта к требованию «Ответ не перезапускает всё» пишется задачей первого среза после архивации `verify-stop-repeat`.

### К сведению

- Старт реализации упирается в первую задачу: обе соседние ЗНИ ещё не в архиве. Остановка и сообщение пользователю записаны в критерии задачи.
- В обязательном пункте приёмки первого среза сценарий цвета покрыт текстом приёмки; отдельная подпись с именем сценария необязательна.

## Технический аудит (для движка OpenSpec)

- verify_mode: pre-apply. verify_depth первого прохода: full (кэша verification не было). repair_attempt: 1.
- Layer 1 Hygiene: PASS. Чекбоксы, закрывающие `<!-- slice-gate -->`, `form_mode: n/a` на месте. Автоправок нет.
- Layer 2 Internal Coherence: PASS.
  - External validity: EC-1 `customer-direct`, `parity: matches`, `confirmation: confirmed`, `confirmed_by: user`. Открытых тем высокого авторитета нет. `open_decision_id: null`. Repair-from-verify журнал контракта не менял.
  - User Task Contract pre-check: none. Единственное «вручную» — в описании сценария S1 (вызов проверки пользователем), не маркер ручной конфигурации метаданных. `manual-config-incomplete` не ставился.
  - QC: `reports/quality-control-2026-09-30.md`, verdict OK, 19/19 сценариев, CRITICAL/WARNING нет. Два SUGGESTION (`accept-primary-scenario-label`, `shared-surface-apply-order`) не блокируют.
  - Опора на прошлый контроль среза S1–S3: после repair взяты результаты `reports/quality-control-2026-09-30.md`. Набор названий сценариев и нормализованный текст Primary не менялись. Новый полный контроль с нуля не создавался.
  - Code-Truth: pre-apply, `openspec/project.md` нет, якорей процедур 1С в backticks нет. phantom-symbol: none.
  - Precedent regression: в текущих `specs/**` нет MODIFIED/REMOVED. Архивного `verify-stop-repeat` нет. `openspec/knowledge/_index.yaml` нет. Supersedes Load-Bearing ADR нет. Триггер не сработал.
- Layer 2.5 Loop Detection: PASS. Slice Gate Decisions нет. Одна секция `## Extend — 2026-09-30` меняет задачи S1 и S2. PatchRounds S1=1, S2=1, S3=0. acceptance_loop_max=3. TopicReopen G1=0, G2=0 (первое упоминание, не переоткрытие).
- Layer 3 Problem-Solution Trace: PASS. Why покрыт шестью Requirement, у каждого есть Scenario. Сценарии привязаны в design § Slices и в accept/задачах. `scenario-implementation-leak`: маркеров в THEN нет. `comment_suffix` пуст. `process-only-marker-suffix` не сработал.
- Layer 4 Independent Challenge: файл `reports/design-challenge-2026-09-30.md` имеет verdict CHALLENGE (G1, G2 открыты; G3–G5 закрыты). Post-challenge classifier: оба открытых разрыва `implementation_invariant`, ось заказчика не меняют, равноправных альтернатив нет. Repair Loop attempt 1 дописал D1 (несколько записей § Extend) и D5 ветку 2 (совпадение ключей снимка) и задачи S1.2, S1.3, S2.8. Наблюдаемый исход одной замены цвета и архива после отметок не менялся. Повторный design-challenge не запускался; G1/G2 как новый разрыв не поднимались. Итоговый статус слоя после ремонта: APPROVE. `last_challenge_at` обновлён, потому что CHALLENGE ушёл в repair.
- Layer 5 Implementation Readiness: PASS. Полный проход `reports/architecture-task-readiness-2026-09-30.md` (Gaps: []). Точечный повтор S1.2, S1.3, S2.8 — `reports/architecture-task-readiness-2026-09-30-2.md` (Gaps: []). Маркер «вручную» в сценарии S1 ручной конфигурацией не признан.
- Рецепт дайджестов: SHA-256 UTF-8 после LF и снятия хвостовых пробелов. `external_contract_digest` = SHA-256 строки `EC-1|matches|confirmed|`. `decision_fingerprints` = SHA-256 `id|closed_at|source`. `design_axis` = нормализованный фрагмент design.md от `## Decisions` до `## Design Rationale`.

## Источники

- openspec/changes/pipeline-light-route/reports/quality-control-2026-09-30.md
- openspec/changes/pipeline-light-route/reports/design-challenge-2026-09-30.md
- openspec/changes/pipeline-light-route/reports/architecture-task-readiness-2026-09-30.md
- openspec/changes/pipeline-light-route/reports/architecture-task-readiness-2026-09-30-2.md
- Алерты: нет блокирующих. SUGGESTION: `accept-primary-scenario-label`, `shared-surface-apply-order`.
