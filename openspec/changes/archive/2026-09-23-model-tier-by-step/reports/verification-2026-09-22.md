---
verify_mode: pre-apply
change: model-tier-by-step
date: 2026-09-22
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: WARNING
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: WARNING
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: WARNING
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "Как записать, какая модель у какого шага архитектора: пояснения в существующих абзацах или одна таблица шагов."
  artifacts_mtime:
    proposal.md: "2026-09-22T05:53:55Z"
    design.md: "2026-09-22T06:00:41Z"
    tasks.md: "2026-09-22T06:00:41Z"
    specs/subagent-model-mapping/spec.md: "2026-09-22T05:54:32Z"
  last_challenge_at: "2026-09-22T15:19:17+09:00"
  artifact_hashes:
    proposal.md: "988dfedc779735f4013a5d1788b917fcf919c5ec2286d2e65968040b5001e666"
    design.md: "58efd77d52b0f814be14342d3120e803c5d8007d2cd6de70cba1c5f0209682f3"
    design-axis: "cf2ce86fef8674c6b168184c5cba9fb5db4ae388111c2eebf03c48c47294e4bb"
    tasks.md: "de28113dd593d6c6104149e357dd51f86950a215164c9ceaac2259b44986feab"
    specs/subagent-model-mapping/spec.md: "df1cd4f6cc92c842cf95db65aa59914454f7ae8ce4939f08d8535e6fb11fe8a5"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints: {}
  rules_versions:
    .cursor/rules/vertical-slices.mdc: "ae7299668199f606222fcb969922dfc821ccb95c38180b0099256864ec700978"
    .cursor/rules/openspec-specs-gate.mdc: "9724d7079e9630844d16bce0b5b664e29929da2136fb3a8f19f3b61e1a52c867"
    .cursor/rules/code-truth-gate.mdc: "bb7ecbbf53bd3b877b36b184eab851ca9f3f24db5f657f154df22029354ce579"
    .cursor/rules/precedent-regression-gate.mdc: "875bb7841d2ff3e85dc4a8c66c22a413edccc7c6c5536650f1e7e5c9b6aa7641"
    .cursor/rules/architect-gate.mdc: "ba2b3add96503d98649bd11c60f1f6be61cb74962a62811fcdd38961d8c6deae"
    .cursor/rules/model-selection.mdc: "6abe07aaa8986cd211e971c62e09d49fbc01626a2536e43f58b2502399bbaf84"
    .cursor/skills/openspec-verify-change/SKILL.md: "ff9ace29759aa5085b1d112917a69cacdfa0bc9709d6219db0e23521580977cd"
  check_cache:
    hygiene-checkboxes@tasks.md: "PASS|de28113dd593d6c6104149e357dd51f86950a215164c9ceaac2259b44986feab"
    slice-gate-markers@tasks.md: "PASS|de28113dd593d6c6104149e357dd51f86950a215164c9ceaac2259b44986feab"
    user-task-contract@tasks.md: "PASS|none"
    external-validity@none: "PASS|empty-ledger"
    scenario-coverage@all: "PASS|qc-2026-09-22-2"
    code-truth@pre-apply: "OK|no-1c-symbols"
    precedent-regression@subagent-model-mapping: "INFO|precedent-documented"
    loop-detection@none: "PASS|no-debug"
    problem-solution-trace@proposal-specs: "WARNING|scenario-orphan-slice-regression"
    design-challenge@axis: "CHALLENGE|cf2ce86fef8674c6b168184c5cba9fb5db4ae388111c2eebf03c48c47294e4bb"
    task-readiness@all: "WARNING|architecture-task-readiness-2026-09-22"
  invalidation_map:
    hygiene-checkboxes: "cache miss, first verify"
    slice-gate-markers: "cache miss, first verify"
    user-task-contract: "cache miss, first verify"
    external-validity: "cache miss, first verify"
    scenario-coverage: "cache miss, first verify"
    code-truth: "cache miss, first verify"
    precedent-regression: "cache miss, first verify"
    loop-detection: "cache miss, first verify"
    problem-solution-trace: "cache miss, first verify"
    design-challenge: "first pre-apply, no last_challenge_at"
    task-readiness: "cache miss, all tasks new"
---

## Резюме для разработчика

model-tier-by-step — до старта нужен ваш выбор по логике записи исключения модели.

**Что решить: как записать, какая модель у какого шага архитектора**

План ставит сверку уже написанных задач на модель чата, а сверку «правка не отменяет прошлый договор» — на ту же лестницу, что разбор постановки. Сейчас это несколько пояснений в правиле назначения. Рядом остаётся фраза, что обычный вызов архитектора начинается с тяжёлой модели, и одно чтение этой фразы снова отправит сверку задач на неё.

- **A. Дописать пояснения в существующих абзацах** — исключение видно рядом с сегодняшним текстом, но следующее исключение снова нужно не пропустить в тех же местах.
- **B. Собрать одну таблицу «шаг архитектора → модель»** — строка роли только ссылается на неё, но перечень шагов придётся держать и в таблице, и в описании архитектора.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify model-tier-by-step`.

Полный отчёт: openspec/changes/model-tier-by-step/reports/verification-2026-09-22.md

План правит правило назначения моделей и три текста, которые это правило вызывают: проверка постановки, остановка перед правкой и абзац про вызов архитектора. Код конфигурации, формы и модули не затрагиваются. Проверка кода, упрощение, обследование, разбор трассы, написание кода и согласованность срезов остаются как сейчас.

## Решения до apply

### 1. Как записать, какая модель у какого шага архитектора

**В чём проблема.** План закрывает исключение несколькими пояснениями, а фраза «обычный вызов архитектора начинается с тяжёлой модели» остаётся без оговорки про сверку уже написанных задач.

**На что влияет.** На проверке с рискованными задачами сверка исполнимости снова может уйти на тяжёлую модель, если читать одну эту фразу.

**Если выбрать A / B.** A — пояснения дописываются в те абзацы, которые уже есть, но следующий режим-исключение снова ищется по тем же местам. B — одна таблица шагов, на неё ссылается строка роли, но перечень шагов живёт и в таблице, и в описании архитектора.

**Что в коде сейчас.** В `.cursor/rules/model-selection.mdc` строка роли архитектора и цепочка обычных режимов относят сверку готовности задач к тяжёлой модели. В `.cursor/rules/architect-gate.mdc` абзац обычного вызова говорит то же без оговорки по режиму. Таблица закрытой эскалации прячет сверку с прошлым договором внутри «остальных режимов».

**Что предлагает план.** Исключение для сверки задач — вызов без явной модели. Сверка с прошлым договором — та же лестница, что независимый разбор постановки. Остальные шаги архитектора остаются на тяжёлой модели.

**Почему это развилка.** Независимый разбор подтвердил обе боли и не нашёл более дешёвого пути по охвату, но текущая запись не делает невозможным чтение «обычный вызов → тяжёлая модель». Таблица шагов убирает этот класс ошибки и меняет форму правила.

**Варианты решения.**

- **A. Дописать пояснения в существующих абзацах** — в правиле назначения и в абзаце обычного вызова появляется оговорка; для разработчика: правка локальная; для пользователя проверки: сверка задач читается как модель чата, если не пропустить абзац.
- **B. Собрать одну таблицу «шаг архитектора → модель»** — строка роли только ссылается на таблицу; для разработчика: одно место правды и второе место, где перечислены шаги; для пользователя проверки: чтение одной строки роли больше не возвращает тяжёлую модель на сверку задач.

**Что изменится после выбора.** Выбор записывается в постановку. При A в охват первого среза добавляется оговорка в абзаце обычного вызова. При B три пояснения заменяются таблицей, а тексты запуска на неё ссылаются. Затем снова проверка постановки.

**Источники** *(техническое, не для разработчика):* `reports/design-challenge-2026-09-22.md` (CHALLENGE, альтернатива «таблица режимов»); classifier: decision, не repair.

## Что меняется в постановке

**Расширение / конфигурация:** нет. Меняются правила kit, не выгрузка конфигурации.

**Точки изменения:**

- `.cursor/rules/model-selection.mdc` — исключение для сверки уже написанных задач и лестница для сверки с прошлым договором.
- `.cursor/skills/openspec-verify-change/SKILL.md` — запуск сверки задач без явной модели и поведение, если этот вызов сорвался.
- `.cursor/rules/verified-cause-gate.mdc` — отсылка сверки с прошлым договором к той же лестнице.
- `.cursor/rules/architect-gate.mdc` — перечень лестницы заменяется отсылкой к таблице назначения.

**Что НЕ меняется:** модель проверки кода, упрощения, обследования, разбора трассы, написания кода и согласованности срезов; обычные шаги архитектора остаются на тяжёлой модели; строка в чате у независимого разбора постановки не переписывается.

**Связанные ADR / KB / архив:** архив `2026-08-18-kit-evolution-models-economy-profiles`, требование про назначение моделей и требование про лестницу самой сильной модели. Отмена цели «не звать отсутствующий слаг и не подменять отчёт» не заявляется. Базы знаний в kit нет.

### К сведению

- Оба среза правят один файл правила в разных местах и идут по очереди. Приёмка каждого среза от этого не зависит.
- Регрессионные сценарии живого требования покрыты задачами сверки текста, в карточке среза в design названы только новые сценарии.
- В этой сборке самой сильной модели в перечне вызова нет, поэтому лестница сверки с прошлым договором на экране совпадёт с сегодняшней тяжёлой моделью. Приёмка смотрит на текст лестницы.
- После выбора останутся точечные уточнения постановки: ячейка таблицы запуска в проверке, текст про сбой единственного вызова рядом с переиспользованием прошлого отчёта, чеклист вызова. Это запишется вместе с выбором, отдельного вопроса нет.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы, маркеры срезов, `form_mode: n/a` на месте. Автоправок нет.
- **Layer 2 (Internal Coherence):** WARNING. QC: `reports/quality-control-2026-09-22-2.md`. Критерии 1, 2, 3, 5, 5b, 8, 8b, 9, 10, 11 — PASS. Критерий 4 и 6 — WARNING (`undeclared-slice-dependency`, `rework-risk-shared-artifact`): S2 пишет «Зависимости: нет», но S2.1/S2.2 сохраняют правки S1 в том же файле. Forward acceptance dependency нет, 8b PASS. User Task Contract pre-check: none. External validity: реестра нет, событий из закрытого перечня нет — PASS. Code-truth pre-apply: якорей процедур 1С нет, `openspec/project.md` нет — phantom-symbol нет. Precedent: два архива capability `subagent-model-mapping`, бюджет не превышен; семантическое изменение закрыто `## Blast Radius` — INFO `precedent-documented`. Индекс KB отсутствует. Load-bearing ADR этот change не supersede. Предыдущий `quality-control-2026-09-22.md` — pre-tasks, не reused.
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` на старте прогона не было. AcceptLoop = 0, PatchRounds = 0.
- **Layer 3 (Problem-Solution Trace):** WARNING. Why покрыт двумя MODIFIED requirements. У каждого requirement есть сценарии. У каждого среза есть рабочие задачи и ровно один accept. Implementation-leak маркеров в THEN нет. `comment_suffix` пуст. `scenario-orphan-slice`: регрессионные сценарии не названы в `design.md` ## Slices, покрытие есть в `tasks.md` (S1.7, S2.6) и в QC — не FAIL.
- **Layer 4 (Independent Challenge):** CHALLENGE. Отчёт: `reports/design-challenge-2026-09-22.md`. Trigger: first pre-apply. Модель вызова: Opus 5, слага Fable в enum сборки нет. Classifier: архитектурная альтернатива «проза с отсылками / таблица режимов» — decision, одна развилка в чат. G1/G1b/G2/G3/G4 — implementation_invariant, в этот ход не чинились: decision имеет приоритет. G5 низкий, на исполнимость не влияет. Closed decisions нет, reopen-blocked нет. `last_challenge_at` обновлён.
- **Layer 5 (Implementation Readiness):** WARNING. Отчёт: `reports/architecture-task-readiness-2026-09-22.md`. Trigger: cache miss, все задачи новые. Вердикт файла: ГОТОВО С ЗАМЕЧАНИЯМИ. Задачи исполнимы as-is. CRITICAL GAP и `manual-config-incomplete` нет. Маркеров ручной конфигурации нет.

### Каскад дельты

- **verify_depth:** full.
- **recomputed:** все `check_id` — cache miss.
- **reused:** none.
- **escalated:** QC sync; design-challenge background; task-readiness sync.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

Единственная развилка в чат — форма записи исключения (проза vs таблица режимов). Post-challenge classifier не перевёл её в repair и не отфильтровал как reopen-closed. GO-saturated не применяется: `decision_round` = 0.

Пробелы, которые уйдут в постановку после ответа, без второго вопроса:

- G1: `architect-gate.mdc` абзац обычного вызова не оговаривает готовность задач; файл сейчас в срезе лестницы, не в срезе сверки задач.
- G1b: `tool-name-guard.mdc` чеклист вызова не называет исключение.
- G2: колонка Mode таблицы запуска уже занята именем режима; буквальная вставка «без model» в ту же ячейку, что у согласованности срезов, неисполнима без уточнения формы.
- G3: поведение «сбой единственного вызова блокирует продолжение» расходится с типом readiness «без блокировки этапа»; в постановке это уже выбрано в D1 и должно быть названо явно, без смены оси.
- G4: шаблон промпта готовности задач модель не задаёт; соседние шаблоны задают. Либо одна строка-отсылка, либо явная причина, почему мера риска к этому тексту не применяется.
- Пробел готовности S1.6: запрет подставлять прошлый отчёт не должен отменить переиспользование отчёта, когда вызов не запускался.

### Universal policy self-check

Реестр внешнего контракта не создавался: секции не было и события из закрытого перечня нет. Авторитет по прозе не угадывался. Абсолютные проектные пути в правило не вносились.

## Источники

- `openspec/changes/model-tier-by-step/reports/quality-control-2026-09-22-2.md`
- `openspec/changes/model-tier-by-step/reports/design-challenge-2026-09-22.md`
- `openspec/changes/model-tier-by-step/reports/architecture-task-readiness-2026-09-22.md`
- Алерты: `undeclared-slice-dependency`, `rework-risk-shared-artifact`, `scenario-orphan-slice`, `precedent-documented`
