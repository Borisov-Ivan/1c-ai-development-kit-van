---
verify_mode: pre-apply
change: verify-model-bands
date: 2026-10-14
verdict: GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: WARNING
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: WARNING
  layer_4_independent_challenge: SKIPPED-novelty
  layer_5_implementation_readiness: PASS
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions:
    - id: readiness-unknown-signature
      summary: "Неизвестная сигнатура или контракт данных при сверке задач идёт на тяжёлую модель, вместе с неизвестным перехватом и неподтверждённым вызовом платформы. Ручная настройка и новая связь модулей остаются на модели чата."
      closed_at: "2026-10-14"
      source: verify-user-answer
      confirmed_by: user
      premise: none
    - id: multi-slice-counter
      summary: "Модель семейства GPT берётся, если в заявке больше одного среза, даже когда в этот запуск сверки попал один срез. Заявка из одного среза остаётся на модели чата."
      closed_at: "2026-10-14"
      source: verify-user-answer
      confirmed_by: user
      premise: none
  refuted_premises: []
  open_decision_id: null
  decision_round: 1
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-10-14T13:10:50+09:00"
    design.md: "2026-10-14T14:51:07+09:00"
    tasks.md: "2026-10-14T14:51:10+09:00"
    specs/subagent-model-mapping/spec.md: "2026-10-14T14:51:11+09:00"
    debug.md: "2026-10-14T14:51:15+09:00"
  last_challenge_at: "2026-10-14T14:47:00+09:00"
  artifact_hashes:
    proposal.md: 0051064cda309867bb4136def72329b932256da9af3055c56785282b1684c437
    design.md: 975caa9256eb6cc1c259d41db95e93e868cf1d86cf6639ee41c82ef457dc3fb5
    design.md#axis: 3716dc8eee5f6de9d1d44b03c9e4152698d5fcfade007456c408bd35b24d53f9
    tasks.md: 8b23b6f8431153bce82ba158b7f967b1f6b9eb3f049cbfd8004d84539605a126
    tasks.md#normalized: 8b23b6f8431153bce82ba158b7f967b1f6b9eb3f049cbfd8004d84539605a126
    specs/subagent-model-mapping/spec.md: 8aef4fe84c27f6469d2ddaf156f1d3964ffc6dc30e78d09fe7e95c8ca6e72697
    debug.md: 5fa9a1dd4e596be07e46f2f86232e28d9691ebb518d3ea1d8a7c1dbcbc34c285
    debug.md#without-slice-gate: 5fa9a1dd4e596be07e46f2f86232e28d9691ebb518d3ea1d8a7c1dbcbc34c285
  external_contract_digest: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  decision_fingerprints:
    readiness-unknown-signature: 9a8cc264670cccba4c9b5056f1d29dd5bd699bf8d69720d8f4ed5284bbd2ed4f
    multi-slice-counter: 879a8a126012df6340bec2e45fe3f8334afdda3e4d9115338e2ae3401682db8d
  rules_versions:
    .cursor/rules/vertical-slices.mdc: 949cf35de18db610774b6b7340f4c99f7a2f523ee224ab5b825bc719e7230bb9
    .cursor/rules/code-truth-gate.mdc: bf8b7f6e9695a9f36b513faff3d9ba78499f283ebf2aa0ef86cacec957b9754f
    .cursor/rules/precedent-regression-gate.mdc: 875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641
    .cursor/rules/openspec-specs-gate.mdc: 14459abbd63cdd7140cd58b8ac7d0321a563c29999d1e026805e37ec37a76610
    .cursor/rules/architect-gate.mdc: 003ecb1a433310823db9d8b8ebc09f6fb04b38a0925307f5f0251c22c451c7a7
    .cursor/skills/openspec-verify-change/SKILL.md: 5ed914bf54dd9b571564eef943ff6325208921719cc74922e1df632527ed3dff
  check_cache:
    hygiene-checkboxes: PASS
    slice-gate-markers: PASS
    user-task-contract: PASS
    external-contract-schema: PASS
    external-validity: PASS
    scenario-coverage: WARNING
    code-truth: PASS
    precedent-regression: INFO
    loop-detection: PASS
    problem-solution-trace: WARNING
    design-challenge: CHALLENGE-repaired
    task-readiness: PASS
    premise-reconciliation: PASS
    simplicity-check: PASS
  invalidation_map:
    hygiene-checkboxes: "текст tasks.md изменился"
    slice-gate-markers: "текст tasks.md изменился"
    user-task-contract: "текст tasks.md изменился"
    external-validity: "появилась секция Extend, развилки процессные"
    scenario-coverage: "изменились spec и design § Slices не менялся по именам"
    problem-solution-trace: "изменились spec и design"
    design-challenge: "хэш оси изменился до ремонта; после ремонта тема та же, повтор не запускался"
    task-readiness: "текст задач изменился, профильного триггера нет"
    loop-detection: "добавлена секция Extend repair"
---

## Резюме для разработчика

verify-model-bands — можно запускать apply. Первая проверка без тяжёлого признака идёт на тяжёлой модели, ревью — на семейство Gemini из списка вызова.

Уже зафиксировано: неизвестная сигнатура или контракт данных при сверке задач идёт на тяжёлую модель; модель семейства GPT берётся, если в заявке больше одного среза.

План правит правило назначения в одной таблице шагов. Независимый разбор без тяжёлого признака вызывает старшую модель семейства Opus, мажор 5, и строку «Разбор постановки (Opus 5)». С тяжёлым признаком — самую сильную модель и строку «Разбор постановки (Fable)», если она есть в списке вызова. Конфигурация 1С не меняется.

Подправил в постановке: пункт 3 записи о таблице шагов отдельно держит сверку с прошлым договором на самой сильной модели, а сценарий обычного вызова архитектора оставлен на обычной строке таблицы.

Заявка из нескольких срезов платит за сверку даже одного среза. Простая заявка без тяжёлого признака самую сильную модель не вызывает.

**Следующий шаг:** `/opsx:apply verify-model-bands`

Полный отчёт: openspec/changes/verify-model-bands/reports/verification-2026-10-14-2.md

Правка сидит в `.cursor/rules/model-selection.mdc`, чеклисте вызова `.cursor/rules/tool-name-guard.mdc` и в `openspec/adrs/ADR-0011-architect-step-model-table.md`. Тексты запуска, которые сами назначают модель, сверяются с этой таблицей. Путей в `src/` нет.

## Что меняется в постановке

Конфигурация 1С не меняется.

**Точки изменения:**

- `.cursor/rules/model-selection.mdc` — условие в строке независимого разбора, старшинство семейства Gemini для ревью, сверка заявки из нескольких срезов, три повода готовности задач.
- `.cursor/rules/tool-name-guard.mdc` — чеклист ссылается на эти строки и свой перечень моделей не разворачивает.
- `openspec/adrs/ADR-0011-architect-step-model-table.md` — пункт 2 уже сужен тремя поводами; пункт 3 и последствия правятся по задаче S1.2: сверка с прошлым договором остаётся на лестнице самой сильной модели, независимый разбор берёт её только при тяжёлом признаке, ревью и согласованность срезов больше не описаны прежним назначением.
- Тексты запуска, которые сами назначают модель. `AGENTS.md` план не меняет.

**Что остаётся:** запуск независимого разбора на первой проверке и при смене решения; самая сильная модель не становится запасом после сбоя тяжёлой; написание кода, обследование, разбор трассы, упрощение и рекомендация чата; ADR-0004.

**Связанные ADR / архив:** ADR-0011 (Accepted, не Load-Bearing), ADR-0004 (Load-Bearing, эта заявка его не отменяет). Архив `openspec/changes/archive/2026-09-23-model-tier-by-step/`.

### Подправил в постановке

В решении о одной таблице и в задаче правки ADR записан пункт 3: сверка с прошлым договором на лестнице самой сильной модели, независимый разбор берёт эту лестницу только при тяжёлом признаке, последствия не держат прежнюю модель ревью и согласованности срезов. У сценария обычного вызова архитектора условие оставлено на обычной строке и на независимом разборе без тяжёлого признака; ветки самой сильной модели в это условие не входят.

### К сведению

Восемь сценариев закрыты критерием рабочих задач и не повторены в поле связи среза. На запуск это не влияет.

## Технический аудит (для движка OpenSpec)

Повтор после ответов заказчика. Родитель: `reports/verification-2026-10-14.md`. Старт прогона `verify_depth: full`: хэш оси `design.md#axis` разошёлся с `8e26489968dcde7c567dcf893ce28469c7f8f7bc0581f336cf085e6337f6a440`. Класс «замена значения» не присвоен: прошлый полный прогон был NO-GO.

- Layer 1 Hygiene: PASS. Чекбоксы, один маркер конца среза, пустых буллетов и незакрытых блоков нет. `form_mode: n/a`. Автоправок гигиены нет.
- Layer 2 Internal Coherence: WARNING. Внешняя валидность: реестра нет. Секция `## Extend —` записывает процессные ответы (`premise: none`, без `authority` и без `EC-*`); детектор внешнего контракта молчит. User Task Contract pre-check: none. Опора на прошлый контроль среза S1: `reports/quality-control-2026-10-14.md` (вердикт OK, те же 18 названий сценариев, текст Primary не менялся). Детерминированное покрытие: те же 8 сценариев не названы в `design.md` `## Slices` и закрыты критерием S1.1/S1.2 — `scenario-orphan-design`. Code-truth: якорей процедур 1С нет, `openspec/project.md` нет, `phantom-symbol` нет. Precedent: три архива capability `subagent-model-mapping`, бюджет не превышен. Отмена «разбор всегда на Fable», «ревью = gemini-3.1-pro», «готовность всегда без model=», «сверка срезов всегда без model=» закрыта `## Blast Radius`. `precedent-documented` INFO. Индекса знаний нет. `Supersedes` Load-Bearing ADR нет. `.gate-override.yaml` с `gate: architect` Layer 4 не закрывает.
- Layer 2.5 Loop Detection: PASS. `PatchRounds` S1 = 2 (исходный extend и repair). `TopicReopen` G1–G5 = 0, G9 и G10 — первое упоминание. `AcceptLoop` = 0. Порог 3 не сработал. Секции `## Slice Gate Decisions` нет.
- Layer 3 Problem-Solution Trace: WARNING. Три боли `## Why` покрыты требованиями. У каждого требования есть сценарий. Срез S1 имеет рабочие задачи и один `S1.accept`. `scenario-orphan-slice` — те же 8 сценариев, не системный разрыв. Маркеров implementation-leak в `THEN` нет. `comment_suffix` пуст.
- Layer 4 Independent Challenge: первый вызов на старшей Fable 5 (`claude-fable-5-1-thinking-high`) вернулся лимитом, отчёт не записан. Шаг 2 цепочки — вызов без `model=`. Отчёт `reports/design-challenge-2026-10-14-2.md`, verdict CHALLENGE, confidence high. `## Premise conflicts` нет. После классификатора оба открытых разрыва — `implementation_invariant`. Повторный разбор после ремонта не запускался: дописка согласует уже выбранную лестницу, наблюдаемое правило не меняет. Закрывающий статус слоя — `SKIPPED-novelty` в смысле «тема после ремонта не поднимается заново». `last_challenge_at` обновлён, база оси — хэш после ремонта.
- Layer 5 Implementation Readiness: PASS. Профильный триггер не сработал: правки — тексты кита, не неизвестный перехват, ручная настройка, неподтверждённый вызов платформы как задача реализации, новая связь модулей 1С или неподтверждённый API. Маркеров ручной конфигурации нет. Новый вызов готовности не создавался. Прошлый `reports/architecture-task-readiness-2026-10-14.md` (ГОТОВО) не подставлен как результат этого запуска. Критерий 7 в нём не `SUBOPTIMAL`.

### Каскад дельты

- **verify_depth:** full на старте; после ремонта повторный независимый разбор не назначался.
- **recomputed:** гигиена, внешняя валидность, покрытие сценариев, трассировка Why, петля, прецедент.
- **reused:** контроль среза S1 — `reports/quality-control-2026-10-14.md`.
- **escalated:** design-challenge (смена хэша оси). task-readiness не запускался. QC повторно не запускался.

### Авто-исправлено (Layer 1)

Не применялось.

### Post-challenge classifier

- G1–G5 — закрыты текстом до ремонта. В чат не выносились.
- G6, G7, G8 — повтор, не разрыв. G8 с `reopen-blocked: readiness-unknown-signature` без нового факта — drop.
- G9 пункт 3 ADR-0011 склеивает лестницы: `implementation_invariant`. Repair: D5 и S1.2.
- G10 WHEN сценария «Вызов архитектора без ошибки enum» отдаёт тяжёлую модель ветке самой сильной: `implementation_invariant`. Repair: WHEN в дельте spec.
- Repair Loop attempt 1. Скрытой развилки нет. `repair_attempt` в снимке сброшен в 0 при GO.
- `refuted_premises` пуст. Оба закрытых решения с `premise: none`.

### Контроль простоты

Отчётов архитектора с `mode` из списка `design` / `plan-review` / `fix-quality` / `slice-decomposition` / `task-decomposition` / `deep-analysis` в этом прогоне нет. `design-challenge` и `task-readiness` секцию Simplicity Check не требуют. Строка «к сведению» по этому контролю не выдаётся.

## Источники

- `openspec/changes/verify-model-bands/reports/quality-control-2026-10-14.md`
- `openspec/changes/verify-model-bands/reports/design-challenge-2026-10-14.md` (леджер номеров)
- `openspec/changes/verify-model-bands/reports/design-challenge-2026-10-14-2.md`
- `openspec/changes/verify-model-bands/reports/architecture-task-readiness-2026-10-14.md` (прошлый прогон, в этот запуск не подставлен)
- `openspec/changes/verify-model-bands/reports/verification-2026-10-14.md`
- Алерты: `scenario-orphan-design`, `scenario-orphan-slice` (WARNING). Precedent: `precedent-documented`.
