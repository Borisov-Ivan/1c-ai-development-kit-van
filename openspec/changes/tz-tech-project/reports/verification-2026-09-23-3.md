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
  repair_attempt: 2
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "каркас техпроекта: обзор, не разделы шаблона архитектура/алгоритм"
    - "часы: не формула §8 и не середина диапазона; неоднозначная строка справочника — дыра в листе"
    - "порядок надбавки к нижней границе"
    - "одна фраза пустого листа"
  artifacts_mtime:
    proposal.md: "2026-09-23T10:55:17"
    design.md: "2026-09-23T11:01:36"
    tasks.md: "2026-09-23T11:02:18"
    specs/tz-tech-project/spec.md: "2026-09-23T11:01:21"
    debug.md: "2026-09-23T11:01:51"
  last_challenge_at: "2026-09-23T11:06:13"
  artifact_hashes:
    proposal.md: "cfe7f927e92be24ba4cfd388a2b2dc58b1fb37322fbe4bae23742bb585f33699"
    design.md: "46513f169b6cd783fbff5c912ddc12f82027146b6ee6ee2be571d0fd67cf4a13"
    design-axis: "d140ebd0e5998af19481fa2686b04dca65caeea40b74323a91650a194131e6c7"
    tasks.md: "4d0bd89c12c15966a44a5a6b49968eda757c92f11c6a51c13680e8c8aa818558"
    specs/tz-tech-project/spec.md: "95e17d4c3cabda57bbbe47c6ba1ce7a72540fc9c6d32ebe566c6e0eb24eeccf1"
    debug.md: "6e0b92b89ea203068f8609c7da6829b4079727d6ceeac3d71fe75eb9756c58ad"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints: {}
  rules_versions: {}
  check_cache:
    scenario-coverage: "quality-control-2026-09-23-4 OK"
    user-task-contract: "none"
  invalidation_map: {}
classifier:
  implementation_invariant:
    - skeleton-from-overview-not-template-technical
    - labor-standards-ignore-section-8-and-midpoint
    - ambiguous-catalog-row-is-question-hole
    - surcharge-order
    - empty-sheet-phrase
  dropped:
    - midpoint-or-section-8-as-axis-change: "ломает уже записанную нижнюю границу"
    - template-runtime-ssot: "ломает ось копий в навыке"
  supersedes: none
  repair_next: "terminal after repair_attempt 2"
---

## Резюме для разработчика

tz-tech-project — apply пока нельзя: не удалось автоматически дописать постановку за 2 итерации.

По файлу задания команда должна положить рядом лист вопросов и техпроект с часами, без таблицы нормативов и без вопросов по одному в чат. Не сошлось, откуда брать каркас текста и как выбрать число часов, если справочник даёт диапазон и отдельную формулу: реализация может собрать старые разделы «архитектура / алгоритм» или посчитать часы иначе, чем записано. Конфигурация и обзор уже созданной задачи при этом не меняются.

**Следующий шаг:** опишите в чате, как поступить, или `/opsx:extend tz-tech-project`.

Полный отчёт: openspec/changes/tz-tech-project/reports/verification-2026-09-23-3.md

Команда `/opsx:techproject` и навык `openspec-techproject` ещё не созданы. Выгрузка `src/КАСК/cf/` только для сверки имён. Файлы `.cursor/skills/openspec-overview/**` не правятся.

## Что доработать в постановке

### Рекомендации

- **Каркас текста:** сюжет берётся из обзора. Разделы шаблона «архитектура / алгоритм / интеграции» в выход не переносятся. В перечне того, что забирается из папки шаблонов, каркас сюжета не числится.
- **Часы:** при копировании справочника явно запрещены формула полного расчёта и середина диапазона из примеров. Для команды остаётся нижняя граница строки, умноженная на коэффициент. Если описание подходит под две строки справочника — дыра в листе, без молчаливого выбора более тяжёлой строки.
- **Надбавка:** одна база. Либо к произведению нижней границы и коэффициента прибавляется нижняя граница фактора, либо иначе — но одно правило, если фактор прямо назван в задании.
- **Пустой лист:** одна и та же фраза в постановке, в задачах и в требованиях. Сейчас рядом живут «вопросов нет» и «дыр нет».

Равноправной развилки по числу файлов и по месту хранения правил нет: один запуск пишет два файла, правила лежат в навыке.

## Что меняется в постановке

Появляется обёртка команды и навык. Рядом с файлом задания — `<имя>-вопросы.md` и `<имя>-техпроект.md`. Обзор остаётся компилятором готовой задачи. Папка `template/Техпроект` после переноса командой не читается. Конфигурация не меняется.

## К сведению

Автоматически уже вписаны имена двух файлов, ответы из листа, дыра если имени нет в выгрузке, два варианта у вопроса и нижняя граница часов. Этого не хватило, чтобы справочник и старый каркас шаблона не спорили с этим правилом.

## Технический аудит (для движка OpenSpec)

- Layer 1 Hygiene: PASS. Автоправок формы нет.
- Layer 2 Internal Coherence: PASS. `reports/quality-control-2026-09-23-4.md`, verdict OK. Критерии 1–6, 8, 8b, 9–11 PASS. User Task Contract: none. Code-Truth pre-apply: якорей процедур нет. Precedent: MODIFIED/REMOVED нет; invariant KB нет; Supersedes нет.
- Layer 2.5: PASS. AcceptLoop(S1)=0. Секции Extend есть, Slice Gate Decisions нет.
- External validity: реестра нет, события закрытого перечня нет. PASS.
- Layer 3: PASS. Why покрыт. У требований есть Scenario. Маркеров implementation-leak в THEN нет. Пустой comment_suffix не совпал с запретным суффиксом.
- Layer 4: CHALLENGE `reports/design-challenge-2026-09-23-3.md`. Classifier: только implementation_invariant, равноправных развилок нет. Repair attempt уже 2 → terminal, третий repair не запускался.
- Layer 5: PASS без вызова. Триггер ручной конфигурации, неизвестного перехвата и неподтверждённого API не сработал.
- verify_depth: full. repair_attempt: 2.
- Модель разбора: слаг архитектора из таблицы отсутствует в enum сборки; вызовы без `model=`.

## Источники

- `reports/quality-control-2026-09-23-4.md`
- `reports/design-challenge-2026-09-23-3.md`
- Предыдущие прогоны: `reports/verification-2026-09-23.md`, `reports/verification-2026-09-23-2.md`, `reports/design-challenge-2026-09-23.md`, `reports/design-challenge-2026-09-23-2.md`
- Алерты: Layer 4 CHALLENGE, класс implementation_invariant, repair exhausted.
