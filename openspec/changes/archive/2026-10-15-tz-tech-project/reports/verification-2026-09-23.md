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
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-09-23T10:21:05"
    design.md: "2026-09-23T10:25:02"
    tasks.md: "2026-09-23T10:30:03"
    specs/tz-tech-project/spec.md: "2026-09-23T10:24:53"
  last_challenge_at: "2026-09-23T10:53:40"
  artifact_hashes:
    proposal.md: "915df3c4a775a1bccc158e3abcf5239263fb69440b36a3323a03095694c6a862"
    design.md: "b8ea7fd060ff4273ecbdcfa6ffa4552bd330958907c58035eb0e7503241a1c3c"
    design-axis: "9989a904388bd70783516a25d4e5cb489f5f0cca2304144e384c80d9a45d80c9"
    tasks.md: "45f6c41e8f9a2f1096fc341b1ecadf6d743c44339a616ed43d96110b64996897"
    specs/tz-tech-project/spec.md: "89d4b4c9338bbdc8abfc922f93cf209a0ee1c3d5facb297ff2a48ae9ef6cfd33"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints: {}
  rules_versions: {}
  check_cache: {}
  invalidation_map:
    design-challenge: "first verify, no prior snapshot"
    scenario-coverage: "first verify, no prior snapshot"
    user-task-contract: "first verify, no prior snapshot"
classifier:
  implementation_invariant:
    - answer-protocol
    - output-paths
    - missing-object-hole
    - question-item-shape
    - hours-from-prose
    - template-not-second-source
  dropped:
    - one-file-output: "противоречит отдельному листу для отправки; ось двух файлов сохраняется"
    - template-runtime-ssot: "ось «копии в навыке, папка командой не читается» сохраняется; в миграцию добавляется предупреждение, не смена источника"
  supersedes: none
  repair_next: "internal repair-from-verify, затем полный re-verify"
---

## Резюме для разработчика

tz-tech-project — постановка дополняется, выбранная команда не меняется. Рядом с файлом задания фиксируются два имени файлов, ответы читаются из листа, а не из чата, отсутствующее в выгрузке имя становится дырой в листе.

**Следующий шаг:** после дописывания постановки проверка повторяется сама.

Команда `/opsx:techproject` и навык `openspec-techproject` читают файл частного задания и пишут лист вопросов и техпроект. Модули конфигурации не меняются. Обзор задачи остаётся компилятором уже созданной задачи.

## Что доработать в постановке

### Рекомендации

- **Откуда берутся ответы:** повторный запуск читает заполненный лист вопросов рядом с заданием. Чат не источник ответов.
- **Имена файлов:** `<имя задания>-вопросы.md` и `<имя задания>-техпроект.md` рядом с заданием; повторный запуск обновляет те же пути.
- **Нет объекта в выгрузке:** сверка по `src/КАСК/cf/`. Если имени нет или выгрузка недоступна — дыра в листе, реквизит и проводка не выдумываются, команда не останавливается целиком.
- **Пункт листа:** вопрос, не меньше двух вариантов, место для ответа. Нет дыр — одна фраза.
- **Часы из прозы:** уже заполненные строки не затираются. Если таблицы работ нет, строки собираются по тексту задания через справочник навыка; в документ попадают работа, часы и обоснование, без таблицы нормативов.
- **Папка шаблонов:** после переноса команда её не читает. Правки нормативов — только в копии внутри навыка. Папка не удаляется этой задачей.

Развилка по хранению правил и по одному файлу вместо двух не выносится: выбранный путь команды сохраняется.

## Что меняется в постановке

Появляется обёртка `.cursor/commands/opsx-techproject.md` и навык `.cursor/skills/openspec-techproject/`. Голос берётся из обзора, файлы `.cursor/skills/openspec-overview/**` не правятся. Правила и `labor_standards.md` копируются из `template/Техпроект` в навык. Выгрузка `src/КАСК/cf/` только читается для сверки имён.

## К сведению

В колонке среза в постановке был назван один сценарий, хотя таблица покрытия и приёмка содержали все четыре. Колонка дополняется вместе с новым сценарием про отсутствующее имя.

Маркеров ручной настройки конфигуратора в задачах нет. Отдельный разбор исполнимости задач не запускался: в задачах нет неизвестного перехвата, ручного реквизита и неподтверждённого программного интерфейса.

## Технический аудит (для движка OpenSpec)

- Layer 1 Hygiene: PASS. Автоправок нет.
- Layer 2 Internal Coherence: PASS. QC `reports/quality-control-2026-09-23-2.md`, verdict OK. Критерии 1–6, 8, 8b, 9–11 PASS. User Task Contract pre-check: none. Code-Truth: технических якорей процедур нет (пути и `/opsx:*` отфильтрованы), pre-apply. Precedent: множество MODIFIED/REMOVED пусто; `invariant: true` в `_index.yaml` не найден; Supersedes нет.
- Layer 2.5 Loop Detection: PASS. `debug.md` не было; AcceptLoop(S1)=0, PatchRounds(S1)=0.
- External validity: реестра нет, события из закрытого перечня нет. PASS.
- Layer 3 Problem-Solution Trace: PASS. Why покрыт двумя Requirement. У каждого Requirement есть Scenario. Срез S1 имеет задачи и один `S1.accept`. Маркеров implementation-leak в THEN нет. `comment_suffix` пуст — `process-only-marker-suffix` не сработал.
- Layer 4 Independent Challenge: CHALLENGE (`reports/design-challenge-2026-09-23.md`). Post-challenge classifier: все блокирующие пробелы — `implementation_invariant`. Альтернатива одного файла отброшена (ломает отдельный лист). Альтернатива runtime-чтения `template/Техпроект` не меняет ось D4; закрывается предупреждением в миграции. `supersedes` нет. Repair Loop attempt 0 → 1.
- Layer 5 Implementation Readiness: PASS без вызова архитектора. Триггер D7 не сработал. Шаг 5.1: маркеров ручной конфигурации нет. Читаемость задач — QC PASS.
- verify_depth: full (первый прогон).
- Модель разбора: слаг архитектора из таблицы отсутствует в enum сборки; вызов без `model=`.

## Источники

- `reports/quality-control-2026-09-23-2.md`
- `reports/design-challenge-2026-09-23.md`
- Алерты: нет FAIL-кодов слоёв 1–3 и 5. Layer 4: CHALLENGE → implementation_invariant (answer-protocol, output-paths, missing-object-hole, question-item-shape, hours-from-prose, template-not-second-source).
