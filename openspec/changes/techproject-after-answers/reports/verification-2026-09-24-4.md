---
verify_mode: pre-apply
change: techproject-after-answers
date: 2026-09-24
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
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions:
    - id: existing-change-postanovka
      summary: "Для уже существующей задачи файл постановки не пишется. Лист, согласование и технический проект пишутся."
      closed_at: "2026-09-24"
      source: verify-user-answer
      confirmed_by: user
    - id: refined-hours-reconfirm
      summary: "Если уточнённая цифра расходится с подтверждённой, технический проект пишется сразу. В нём обе цифры и ответ, который изменил объём. Второго подтверждения нет."
      closed_at: "2026-09-24"
      source: verify-user-answer
      confirmed_by: user
    - id: rollout-rollback-questions
      summary: "Внедрение и откат не вопрос аналитику. Без сведений раздел пишется «в задании не указано», вопроса в листе нет, пометка не сбрасывается. Из списка объектов не выводятся."
      closed_at: "2026-09-24"
      source: verify-user-answer
      confirmed_by: user
    - id: existing-change-read-source
      summary: "Заданием остаются «зачем» и «что меняется», решения задачи закрывают пробел со ссылкой на номер. Способ реализации требованием не становится. Постановки нет."
      closed_at: "2026-09-24"
      source: verify-user-answer
      confirmed_by: user
    - id: existing-change-lookup
      summary: "Задача ищется как в обзоре, включая архив. Выходы в её каталоге под именем каталога."
      closed_at: "2026-09-24"
      source: verify-user-answer
      confirmed_by: user
  open_decision_id: null
  decision_round: 2
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-09-24T15:07:43"
    design.md: "2026-09-24T15:13:00"
    tasks.md: "2026-09-24T15:13:18"
    specs/techproject-after-answers/spec.md: "2026-09-24T15:13:11"
    debug.md: "2026-09-24T15:17:36"
  last_challenge_at: "2026-09-24T15:16:10"
  artifact_hashes:
    proposal.md: "2905f635197611e6a7733769a51baaa07c1788f4d4b8fd9a84e6e0733a0b4f37"
    design.md: "1955af9c95bacaccfdbe9a70cf1fe3935114facb49ac25be3a3fcab114ce7e9c"
    design_axis: "59f3094f80d3ee3be02ab90171e7a013d7db48068cd272efaa47106cd2313ace"
    tasks.md: "47da05c454bda86ed90877886c180cf4e47cf4eb8d07c007f3dc1da4eb8d36c0"
    specs/techproject-after-answers/spec.md: "3d50d18b84b4462afe3defc1b321a892a07846d4e7f9efd3e86457dbcc841109"
    debug.md: "4d8cae27d377cac8d61ccfe013cf5017df217047032c828f5388b2d01ec19d48"
  external_contract_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  decision_fingerprints:
    existing-change-postanovka: "6294871953c753eb3e9313f71de1085718a8e330e6e6d92271bd27689c82df36"
    refined-hours-reconfirm: "ce6844aef119866795478f13b00cca5718d560b9f67281b6dfd0d31be497ee26"
    rollout-rollback-questions: "4ec9d899e4e638c28b98d14041cc8e0d6996fec417e4fc33fe386dc2b0693348"
    existing-change-read-source: "366c802faccbcbd039bdaadb8400ca5641215cdda21851ff83a360d3c5fa8da5"
    existing-change-lookup: "f518e077167458d7abb3b7545673b30e9396f2540376c49b497ed566768833b3"
  rules_versions:
    .cursor/rules/vertical-slices.mdc: "17615576ce482f01b9a286bb0206f22baddccd8f1f6045f14c35bfbbdab19e63"
    .cursor/rules/openspec-specs-gate.mdc: "e97cf9ad3a76132a05c88bf183b44410320547c9b84cf07e6f73fcea7aced6d4"
    .cursor/rules/code-truth-gate.mdc: "20f25dae70359466cfeec4ac8ec1210867919c3b775f2cd8b597cd7ba7bd85f0"
    .cursor/rules/precedent-regression-gate.mdc: "3921384b52ed58bc1ffa0167b3c5d5ef6f1ca8e73976de9d7d8af06c35b7b148"
    .cursor/rules/architect-gate.mdc: "7927fe8d7d4c2ed61321dadf6cce0174fd1fa70fbf0ad717940f1ffeb7bb3813"
    .cursor/skills/openspec-verify-change/SKILL.md: "d55ad7220eda11e390e1a73ada025065e635c3f0c8201645f5bab937e23e0528"
  check_cache:
    hygiene-checkboxes@tasks: PASS
    slice-gate-markers@S1: PASS
    user-task-contract@S1: PASS
    external-validity@none: PASS
    scenario-coverage@S1: PASS
    code-truth@change: PASS
    precedent-regression@change: PASS
    loop-detection@S1: PASS
    problem-solution-trace@change: PASS
    design-challenge@change: APPROVE
    task-readiness@S1: PASS-no-trigger
  invalidation_map:
    hygiene-checkboxes: recomputed, tasks.md hash changed
    slice-gate-markers: recomputed, tasks.md hash changed
    user-task-contract: recomputed, tasks.md hash changed
    external-validity: recomputed, no EC-*
    scenario-coverage: titles and primary unchanged, QC reused
    code-truth: recomputed, no procedure symbols
    precedent-regression: recomputed, spec still ADDED only
    loop-detection: recomputed, themes identified, threshold not applied
    problem-solution-trace: recomputed, scenario titles unchanged
    design-challenge: recomputed, design axis hash changed
    task-readiness: recomputed, trigger not fired
  design_axis_span: "normalized design.md from ## Decisions through the line before ## Risks"
  decision_fingerprint_recipe: "SHA-256 of id|closed_at|source"
---

## Резюме для разработчика

techproject-after-answers — можно запускать apply.

Команда техпроекта отдаёт аналитику лист только по смыслу задания и сразу называет предварительную оценку. Уточнённая оценка появляется в техническом проекте после пометки в листе. Если на входе уже существующая задача, файл постановки не пишется: лист, согласование и проект ложатся в её каталог.

Правка навыка начнётся после приёмки задачи `tz-tech-project`.

**Следующий шаг:** `/opsx:apply techproject-after-answers`

Полный отчёт: openspec/changes/techproject-after-answers/reports/verification-2026-09-24-4.md

Меняются текст команды техпроекта и навык `.cursor/skills/openspec-techproject/SKILL.md`. Обзор задачи не меняется. Формула часов и порог пометки сохраняются.

## Что меняется в постановке

**Конфигурация:** не меняется. Правки в `.cursor/skills/openspec-techproject/SKILL.md` и `.cursor/commands/opsx-techproject.md`.

**Точки изменения:**

- Лист вопросов — только смысл задания, без часов, вида работы, демонстрации, внедрения и отката.
- Часы — предварительная оценка в чате и в согласовании; уточнённая — в техническом проекте.
- Технический проект — разделы для разработчика: объекты, алгоритм, интеграции, внедрение, откат, уточнённая оценка.
- Вход из уже существующей задачи — лист, согласование и проект в её каталоге, без файла постановки.

**Что НЕ меняется:** формула часов, перенос уже указанных в задании часов, запрет показывать таблицу нормативов, порог пометки в листе, команда обзора.

**Связанные ADR / KB / архив:** нет. Рядом открыта задача `tz-tech-project` с прежним правилом листа. В основной каталог оба требования как два добавленных не попадают.

### Подправил в постановке

Уточнены уже принятые правила: путь к каталогу задачи читается как вход из задачи; часы, названные в чате по работе без строки справочника, входят в итог проекта, если состав работы не изменился; открытая задача ищется раньше архива.

### К сведению

В требовании про пересчёт часов из чата нет короткой оговорки «кроме работы без строки справочника»: частное правило стоит ниже и читается как уточнение. В пункте про архив одна фраза звучит наоборот своему продолжению; по продолжению открытая задача архив не смотрит. Оба места поведения не меняют.

Пока в `tz-tech-project` не отмечена приёмка, навык этой задачей не переписывается. Это уже записано в задачах.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы есть, один `S1.accept`, маркер `<!-- slice-gate -->` есть, phase-gate нет, `form_mode: n/a`.
- **Layer 2 (Internal Coherence):** PASS. Опора на прошлый контроль среза S1: взят `reports/quality-control-2026-09-24-4.md` (OK, 14/14), новый полный контроль с нуля не создавался. Набор названий сценариев и текст Primary не изменились. External validity: секции реестра нет, записей `EC-*` нет. User Task Contract pre-check: none. Code-truth pre-apply: технических имён процедур нет. Precedent: в дельте только ADDED.
- **Layer 2.5 (Loop Detection):** PASS. AcceptLoop(S1)=0. PatchRounds(S1)=4. Темы идентифицированы номерами разрывов, запасной порог к ним не применяется. TopicReopen не достиг 2: дописки закрывали темы.
- **Layer 3 (Problem-Solution Trace):** PASS. Пункты Why покрыты требованиями. У каждого требования есть сценарий. Четырнадцать сценариев названы в `## Slices` и в `S1.accept`. Маркеров implementation-leak в THEN нет.
- **Layer 4 (Independent Challenge):** APPROVE. Отчёт: `reports/design-challenge-2026-09-24-5.md`. Остаток G15 и G17 — формулировки без смены поведения, в чат не выносились. Продуктовых развилок нет. `last_challenge_at` обновлён.
- **Layer 5 (Implementation Readiness):** PASS. Trigger D7 не сработал. Маркеры ручной конфигурации не найдены.

### Каскад дельты

- **verify_depth:** full на прогоне после дописки, потому что изменился текст оси. Итог — APPROVE.
- **reused:** контроль среза S1 по названиям сценариев и тексту Primary.
- **escalated:** design-challenge. task-readiness не запускался. quality-control заново не запускался.

### Авто-исправлено (Layer 1)

не применялось

## Источники

- `reports/quality-control-2026-09-24-4.md` — контроль среза, опора, OK
- `reports/design-challenge-2026-09-24-5.md` — независимый разбор, APPROVE
- `reports/verification-2026-09-24-3.md` — предыдущий проход этого запуска, ушёл в дописку текста
- Алерты: нет FAIL. `external-contract-*` не поднимались. `phantom-symbol` нет. `precedent-regression` нет. `scenario-implementation-leak` нет. `acceptance-loop-detected` нет. `manual-config-incomplete` нет.
