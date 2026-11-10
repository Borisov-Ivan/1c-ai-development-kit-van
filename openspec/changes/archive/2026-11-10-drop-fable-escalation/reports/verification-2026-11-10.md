---
verify_mode: pre-apply
change: drop-fable-escalation
date: 2026-11-10
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
  accepted_tasks: []
  closed_decisions: []
  refuted_premises: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-11-10T18:29:29+09:00"
    design.md: "2026-11-10T19:20:27+09:00"
    tasks.md: "2026-11-10T19:20:32+09:00"
    debug.md: "2026-11-10T19:27:11+09:00"
    specs/chat-model-profiles/spec.md: "2026-11-10T17:48:05+09:00"
    specs/chat-surface-clarity/spec.md: "2026-11-10T17:47:54+09:00"
    specs/delegation-safeguards/spec.md: "2026-11-10T18:27:36+09:00"
    specs/kit-protocol-coherence/spec.md: "2026-11-10T18:26:50+09:00"
    specs/sequential-gate-questions/spec.md: "2026-11-10T18:26:43+09:00"
    specs/session-api-mode/spec.md: "2026-11-10T17:48:00+09:00"
    specs/subagent-model-mapping/spec.md: "2026-11-10T19:08:20+09:00"
  last_challenge_at: "2026-11-10T19:04:00+09:00"
  artifact_hashes:
    proposal.md: "8e59a10cf194422634031df3b101f7635492cb058943f9a7a704afd17aecee73"
    design.md: "4e21f9ae5d21cd1a5fb412b5334996fa55d02f79a6d3eb2cc54ace5722a2698c"
    design.md#axis: "9fa00ab51db9c488045058176a00dc788477f88c593be03d01239c5db0ad0d0b"
    tasks.md: "31ab177f8724b90e729200f6270d90b58af001b4ef366e72230c729a55d6570d"
    tasks.md#normalized: "31ab177f8724b90e729200f6270d90b58af001b4ef366e72230c729a55d6570d"
    debug.md: "25f080a8ee23660957dcbdeb53fa6532aa67103ffcb995d623ed45b933800886"
    debug.md#without-slice-gate: "25f080a8ee23660957dcbdeb53fa6532aa67103ffcb995d623ed45b933800886"
    specs/chat-model-profiles/spec.md: "5182de951b97bcad23e445c9999e66f20ee052f860efdd4a5c8c2909e87ec64c"
    specs/chat-surface-clarity/spec.md: "0db80d9c464a813a17e26eacf55a56c5374cf61cf868cb1a224f66a9cf77bee1"
    specs/delegation-safeguards/spec.md: "27282fce8a2feeced07f5a3c8153f1bbb444f21944195ab3f278134c87712f0a"
    specs/kit-protocol-coherence/spec.md: "86feafebaddf21b8bb05834dbe8d298639a9bea0caf4c4b5c92bd1bb89c6a04e"
    specs/sequential-gate-questions/spec.md: "cb58a4a1b163a1ca17ea19b05e458b0ef0f379620dba52c089e00f88ccfa02bc"
    specs/session-api-mode/spec.md: "70c06abd757d32bc3a2254f51b238be0dbc9c2e81dfdf0c3148852bf1657144a"
    specs/subagent-model-mapping/spec.md: "1b90f56fabe77b9dd5cdb16b4dfc76fe17db25286dc8c9a8cc8b68ba535da0ff"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints: {}
  rules_versions:
    .cursor/rules/vertical-slices.mdc: "2c819ad1565f9a4817c1528c1340f99c33e2429a0d335415f564f21043446bd9"
    .cursor/rules/model-selection.mdc: "cab4e9a9c7ec9a7111e951eb60a12835c6f6ea522083cf3c3ab57de10f9a9f5f"
    .cursor/rules/precedent-regression-gate.mdc: "875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641"
    .cursor/rules/code-truth-gate.mdc: "bf8b7f6e9695a9f36b513faff3d9ba78499f283ebf2aa0ef86cacec957b9754f"
    .cursor/rules/openspec-specs-gate.mdc: "14459abbd63cdd7140cd58b8ac7d0321a563c29999d1e026805e37ec37a76610"
    .cursor/rules/architect-gate.mdc: "733c4498f4bcded131a12f0a44818254b5da077af3438a51240a1e8ab5e9f000"
    .cursor/skills/openspec-verify-change/SKILL.md: "e6824713118e985d580faa00d9773dc503e316cb57b97dc49657523a3f4ba81e"
  check_cache:
    hygiene-checkboxes@tasks: PASS
    slice-gate-markers@S1-S2: PASS
    user-task-contract@tasks: none
    external-validity@none: PASS
    scenario-coverage@current: PASS
    code-truth@kit: OK
    precedent-regression@documented: INFO
    loop-detection@S1-S2: PASS
    problem-solution-trace@why: PASS
    design-challenge@axis: closed-by-repair
    task-readiness@no-trigger: PASS
  invalidation_map:
    scenario-coverage: "specs/subagent-model-mapping narrowed; tasks S1.5 S2.11; S2 primary narrowed"
    design-challenge: "axis unchanged after repair; G1-G4 closed in text; not re-run"
    slice-coherence-S2: "primary text changed, rechecked in quality-control-2026-11-10-4"
    slice-coherence-S1: "reused quality-control-2026-11-10-3"
---

## Резюме для разработчика

drop-fable-escalation — можно запускать apply. Тяжёлый разбор, сверка с прошлым договором и просьба самой сильной модели описаны старшим Opus.

План меняет правило назначения моделей и тексты команд набора. В конфигурации 1С ничего не меняется. Если чат сам открыт на Fable, манера ответа чата остаётся; в вызовы ролей этот профиль не идёт.

Подправил в постановке: договор больше не копирует чужие фразы про проверку нескольких частей, а обязательный осмотр второго шага — это перечень агентов.

**Следующий шаг:** `/opsx:apply drop-fable-escalation`

Соседняя незакрытая заявка про проверку нескольких частей правит то же правило назначения; её абзац эта работа оставляет как есть. Уже запущенный вызов эта работа не отменяет.

## Что меняется в постановке

Меняются тексты правил набора: назначение моделей, бюджет реплик, команды создания и дописывания, перечень агентов. Кода конфигурации нет, `src/` не затрагивается.

Не меняется модель контроля заявки из нескольких частей: живое правило уже отдаёт её старшему Opus, основной договор ещё говорит про профиль GPT-5.6, и эту фразу ведёт соседняя заявка `slice-check-opus`. Файл профиля Fable остаётся.

Связанные записи: ADR-0005 и ADR-0011, обе без статуса load-bearing. Отмена лестницы Fable и запрета на имя раздела записана в радиусе.

### Подправил в постановке

Из дельты мэппинга убраны предложения, которые эта заявка не меняет, в том числе профиль контроля нескольких срезов. В радиус дописаны имя раздела, одна реплика про Opus 5 и отказ переписывать контроль нескольких срезов. Обязательный осмотр второго шага сужен до перечня агентов; команда дописывания осталась отдельной задачей и необязательным пунктом.

### К сведению

Отчёт разбора плана при создании заявки (`reports/architecture-new-2026-11-10.md`, режим plan-review) не содержит раздел сравнения более простого варианта. На постановку это не пишется.

Архивов с теми же договорами больше десяти. Сверены те, которые постановка прямо отменяет: лестница сильной модели, сверка с прошлым договором, реплика до карточки, профиль в брифе роли. Остальные не блокируют.

## Технический аудит (для движка OpenSpec)

- Layer 1 Hygiene: PASS. Чекбоксы на месте, оба `slice-gate` закрыты, `phase-gate` нет, `form_mode: n/a`.
- Layer 2 Internal Coherence: PASS. Опора на прошлый контроль среза S1: взят результат `reports/quality-control-2026-11-10-3.md`, новый полный контроль S1 с нуля не создавался. S2 перепроверен в `reports/quality-control-2026-11-10-4.md`: обязательный пункт один, прежний `acceptance-simplicity-overload` снят. User Task Contract: none. Code-Truth: технических имён процедур нет, `openspec/project.md` нет, статус OK. External validity: реестра нет, структурированного события из закрытого перечня нет, PASS. Precedent: отмены закрыты `## Blast Radius` (`precedent-documented`, INFO). Бюджет архивов превышен (`precedent-audit-budget-exceeded`, INFO), блокировки нет.
- Layer 2.5 Loop Detection: PASS. Одна секция `## Extend —`, `PatchRounds` = 1, `TopicReopen` тем G1–G4 не достиг 2. Порога нет.
- Layer 3 Problem-Solution Trace: PASS. Why закрыт бывшими сильными шагами на Opus и снятием второго порядка. У каждого требования дельты есть сценарий. Сценарии названы в `## Slices`. Маркеров implementation-leak нет. `comment_suffix` пуст.
- Layer 4 Independent Challenge: первый прогон записал `reports/design-challenge-2026-11-10.md` с вердиктом CHALLENGE (G1–G4). Классификатор: все четыре пункта закрываются правкой текста без смены оси Decisions / Behavior Contract (`implementation_invariant`). Дописка их закрыла. Повторный полный разбор не назначался: ось не менялась, уже названные темы новым разрывом не поднимались. Статус слоя этого итога: SKIPPED-novelty. `last_challenge_at` обновлён, потому что CHALLENGE ушёл в repair.
- Layer 5 Implementation Readiness: PASS. Маркеров ручной конфигурации нет. Триггер неизвестного перехвата, сигнатуры или нового вызова платформы не сработал, отдельный отчёт готовности не запускался.

## Источники

- `reports/quality-control-2026-11-10-3.md`
- `reports/quality-control-2026-11-10-4.md`
- `reports/design-challenge-2026-11-10.md`
- `reports/architecture-new-2026-11-10.md`
- Алерты, закрытые допиской: `accept-bullets-missing-scenario`, `slice-dependency-mismatch`, `rework-risk`, `acceptance-simplicity-overload`
- Разбор: G1, G2, G3, G4 — закрыты текстом
