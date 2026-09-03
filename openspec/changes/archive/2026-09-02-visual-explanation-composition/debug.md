## Verify decision ledger

```yaml
closed_decisions:
  - id: hint-slots-explain-overview
    summary: "Намёк на схему в пошаговом разборе и в обзоре проекта в эту поставку не входит; схему там запрашивают прямой просьбой. Свободный чат и исследование получают критерий путаницы частей, слоёв или случаев."
    closed_at: "2026-08-31"
    source: verify-user-answer
  - id: two-pictures-or-one-signoff
    summary: "Две отдельные приёмки: после слоёв подписывают скелет и одну сцену; сопоставление классов — отдельный осмотр. Срезы не сливать."
    closed_at: "2026-09-01"
    source: verify-user-answer
open_decision_id: null
decision_round: 2
decision_round_max: 2
verify_depth: full
assumptions_accepted: []
last_challenge_at: "2026-09-01T04:35:12Z"
repair_attempt: 0
```

## Extend — 2026-08-31

- источник: `--from-verify` (после выбора B в чате), отчёт `reports/verification-2026-08-31.md`; gaps 2–6 `reports/design-challenge-2026-08-31.md` и замечание шаблона `reports/architecture-task-readiness-2026-08-31.md`
- что добавлено/изменено:
  - proposal: What Changes п. 1, Impact, Scope, Acceptance 1, Decisions п. 5 — намёк в пошаговом разборе и обзоре вне поставки, прямая просьба
  - design: Goals 1, Non-Goals 6, Existing Mechanisms 2–5, Behavior 2–4 и 7, Implementation Options (четырёхзначная форма, скелет по умолчанию), секция «Решения verify (зафиксировано)», Risks, Assumptions (без `Grid`/`Callout`)
  - spec `visual-explanation`: авто/намёк — свободный чат и исследование; Scenario «Разбор механизма слоями» сужен; «Unreadable» — порог «больше шести частей в одной сцене → другая сцена или свёртка»; «одна сцена» — только скелет со сценами
  - tasks: Primary Given сужен; S1.1–S1.2, S1.5; Follow-up на explain/overview
- disposition: accepted (выбор B) + implementation_invariant (gaps 2–6, замечание `presentation.form`)
- Architect Gate: не требовался (запись выбора пользователя, исходный объём сохранён, уточнения внутри выбранного носителя)
- следующий шаг: `/opsx:verify visual-explanation-composition`

## Extend — 2026-08-31 (repair-from-verify)

- источник: `--from-verify` (internal Repair Loop, attempt 1); gaps G1–G6 `reports/design-challenge-2026-08-31-2.md`; пробелы 2–5 `reports/architecture-task-readiness-2026-08-31-2.md`
- что добавлено/изменено:
  - spec: значения формы vs вид скелета; порог шести частей только для скелета; осмотр полотна не триггер; «наивный шаг» — когда такая попытка была в ответе
  - proposal: Acceptance 3 выровнен с тем же условием
  - design: авто в свободном чате — через `description` навыка, диспетчер не расширять; скобка в разборе снимается без смены локального критерия; скелет для `flow`/`hierarchy`; «в этом шаге» = текст сцены; тусклость — вариантом компонента
  - tasks: S1.1 (раздел «Предложение», «Смысл», скобка в разборе); S1.2 (ветки формы, роль/сцена, тусклость); S1.5 (сверка этих пунктов)
- disposition: accepted (implementation_invariant). Пробел 1 про строку диспетчера — deferred: авто свободного чата закрывается полем `description` (S1.1), расширение диспетчера — always-apply и вне исходного Scope
- Architect Gate: не требовался (уточнения исполнения внутри выбранного носителя, ось не менялась)
- следующий шаг: re-verify слоёв согласованности и готовности

## Slice Gate Decisions

### Slice S1 — Читаемое объяснение на панели (2026-08-31)
Срез: S1 — Читаемое объяснение на панели
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: нет (S1.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S1-2026-08-31.md

### Slice S1 — Читаемое объяснение механизма слоями (2026-09-01)
Срез: S1 — Читаемое объяснение механизма слоями
Решение: принят
Обоснование: пользователь подтвердил приёмку в `/opsx:apply` (вариант «принят»).
Изменения tasks: S1.accept [x]
Связанный отчёт: reports/slice-acceptance-S1-2026-09-01.md

### Slice S2 — Полотно как спутник сопоставления (2026-09-01)
Срез: S2 — Полотно как спутник сопоставления
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: нет (S2.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S2-2026-09-01-2.md

### Apply patch — правило усиления панели (2026-09-01)

- источник: живая критика приёмки S2 (каталог рецептов, дубль абзаца); разборы в `reports/critique-panel-rule-2026-09-01.md`
- что изменено: навык — экзамен восприятия тех же частей; шаблон — группировка классов, пустой `Main` не публикация; spec/design — просьба без усиления, текущий вопрос, слои после классов
- `[x]` не открывались; S2.accept не ставился
- следующий шаг: ручная приёмка S2

### Code-Truth — S1.1 — 2026-08-31
- task: S1.1
- symbols:
  - visual-explanation SKILL @ `.cursor/skills/visual-explanation/SKILL.md`:3-77, annotation=n/a, action=modified
  - openspec-explain hint parenthesis @ `.cursor/skills/openspec-explain/SKILL.md`:137-139, annotation=n/a, action=modified
- verification: grep/read OK
- source: orchestrator kit-markdown apply

### Code-Truth — S1.2 — 2026-08-31
- task: S1.2
- symbols:
  - panel-shell DATA/scenes/SkeletonChrome @ `.cursor/skills/visual-explanation/fixtures/panel-shell.md`:1-361, annotation=n/a, action=modified
- verification: grep/read OK (`form: "flow"`, `scenes:`, TableView retained, no Grid/Callout import)
- source: orchestrator kit-markdown apply

### Code-Truth — S1.3 — 2026-08-31
- task: S1.3
- symbols:
  - explore Дальше slot @ `.cursor/skills/openspec-explore/SKILL.md`:217, annotation=n/a, action=modified
- verification: grep/read OK
- source: orchestrator kit-markdown apply

### Code-Truth — S1.4 — 2026-08-31
- task: S1.4
- symbols:
  - ADR-0010 Protects-invariants + Решение @ `openspec/adrs/ADR-0010-visual-explanation-panel.md`:8-30, annotation=n/a, action=modified
- verification: grep/read OK (no new ADR file; README index unchanged)
- source: orchestrator kit-markdown apply

## Explore — 2026-09-01 (PavDO: не та картина)

- источник: `/opsx:explore` после подтверждения брифа; бриф `C:\GitHub\PavDO\temp\reports\canvas-universal-skill-brief-2026-09-01.md`; полный отчёт `temp/reports/exploration-2026-09-01-canvas-wrong-picture.md`
- профиль: explore-bug; user-goal: что в навыке всё ещё заставляет рисовать не ту картину
- ## Verified facts: живой провал PavDO (конвейер, затем таблица с кнопками, идеал — три колонки без интерактива); kit-навык `flow|table|hierarchy|card` + скелет по умолчанию + запрет Grid + ItemButton/TableView; composition Behavior «случай = шаг, не колонка» / Scenario «плакат случаев»; S1.accept открыт
- ## Hypotheses: нет блокирующих
- ## Root Cause: контракт «одна из четырёх форм + рассказ устройства механизма», нет критерия «язык картинки = отношение в тексте»; Chosen скелет делает удачное сопоставление нелегальным. Маркер: [verified]
- ## Architectural Impact: UX-значимый + системный (навык, шаблон, ADR-0010). Точечный фикс TableView недостаточен
- связь с архивом: composition — directly-related; `2026-08-31-universal-visual-explanation` — directly-related; карта 2026-08-28 — adjacent
- Architect Gate: report `reports/architecture-2026-09-01-canvas-companion.md` (копия `temp/reports/architecture-2026-09-01-canvas-wrong-picture.md`); Chosen = extend, не закрывать S1.accept на текущем тексте, не `/opsx:new`
- следующий шаг: блок постановки в чате → `/opsx:extend visual-explanation-composition`

## Extend Coherence Audit — 2026-09-01

- Триггер: semantic
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-09-01.md`
- Решение пользователя: accepted recommendations — вариант 1 (дополнить эту поставку: скелет = рецепт механизма; сопоставление = классы сразу без конвейера и пачки кнопок)

## Extend — 2026-09-01

- источник: user-extend, вариант 1 в чате; RCA `reports/exploration-2026-09-01-canvas-wrong-picture.md`; Chosen `reports/architecture-2026-09-01-canvas-companion.md`; аудит `reports/architecture-extend-coherence-2026-09-01.md`
- что добавлено/изменено:
  - proposal: Why (язык = отношение в тексте); What Changes п.3 BREAKING extend; Impact/Scope (два среза одной цели); Acceptance 1–5 (механизм vs сопоставление); Decisions п.6
  - design: Goals 2; BC 1–9; D2 сужен; D8/D9; E-D1…E-D6; Hardcode Justification; Blast Radius; Slices S1+S2; Risks; Migration 6–8; Open Question про фикстуру S2 (не блокер)
  - spec `visual-explanation`: «Form follows the content» — четыре формы = рецепты, не мир; снят MUST «неизвестный жанр → ближайшая из четырёх»; таблица без обязательной кнопки на имени; «Panel tells one scene…» сужен до работы «последовательность/слои»; Scenario «Плакат всех случаев не публикуется» — запрет каталога шагов процесса, классификация сразу = успех (имя Scenario не менялось); ADDED «Graphic language matches the relation in the text»; новые Scenario «Сопоставление уже сказанных классов», «Смешанный источник не даёт конвейер», «Таблица свойств без обязательных кнопок»
  - tasks: заголовок/Primary/`S1.accept`/slice-gate S1 сужены (без универсального «не плакат»); S1.1–S1.5 остаются `[x]`; добавлен срез S2 mechanical (S2.1 навык работа/язык/носитель; S2.2 шаблон-библиотека; S2.3 ADR-0010 инвариант формы; S2.4 сверка против новой дельты) + `S2.accept`; Follow-up explain/overview не поднят в рабочие задачи
- disposition: accepted (вариант 1)
- Architect Gate: `reports/architecture-extend-coherence-2026-09-01.md`
- следующий шаг: `/opsx:verify visual-explanation-composition`

## Loop Detection — 2026-09-01

- Триггер: verify Layer 2.5
- Срез: S1
- AcceptLoop / PatchRounds: 1 / 3 (порог acceptance_loop_max=3)
- Отчёт редизайна: `reports/architecture-loop-redesign-2026-09-01.md`
- Рекомендация архитектора: minimal — не сливать срезы; суженная приёмка механизма слоями остаётся; спутник сопоставления — отдельный исход; семь Scenario в `S1.accept` пометить «опционально» письмом, не новым продуктом
- Решение пользователя: accepted redesign — два вида, две подписи (вариант B в чате)

## Extend — 2026-09-01 (from-verify, два вида)

- источник: `--from-verify` (после выбора B в чате), отчёт `reports/verification-2026-09-01.md`; рекомендация `reports/architecture-loop-redesign-2026-09-01.md`
- что добавлено/изменено:
  - design: § «Решения verify (зафиксировано)» — две отдельные приёмки, срезы не сливать
  - tasks: в `S1.accept` семь Scenario с «покрыто S1.1» помечены «опционально»; в `S2.accept` одноимённый Scenario «Сопоставление уже сказанных классов» помечен «опционально». Primary обоих срезов без изменений. Рабочие `[x]` не трогались
- disposition: accepted (выбор B: два вида, две подписи)
- Architect Gate: `reports/architecture-loop-redesign-2026-09-01.md`
- следующий шаг: `/opsx:verify visual-explanation-composition`

## Extend — 2026-09-01 (repair-from-verify, умолчание шаблона)

- источник: `--from-verify` (internal Repair Loop, attempt 1); gaps 1–4 `reports/design-challenge-2026-09-01.md`; дописки якорей `reports/architecture-task-readiness-2026-09-01.md`
- что добавлено/изменено:
  - design: Existing Mechanisms 1 — копия шаблона не падает в поток/скелет при сопоставлении или пустом поле формы; Behavior 1 — голая «покажи схему» не выбирает поток из цепочек отчёта; Behavior 7 — пустые связи не делают поток языком классов; D5/E-D5 — пункт «Решение» 3 ADR как подсказка рецепта; Implementation Options — хвост «всё остальное → поток» не умолчание библиотеки
  - spec: Scenario «Смешанный источник не даёт конвейер» — WHEN без обязательного слова «отличия»; требование «Graphic language…» — пустые связи ≠ классы
  - tasks: якоря S2.1; S2.2 умолчание копии и снятие запрета `Callout`; S2.3 пункт «Решение» 3; S2.4 сверка этих пунктов; optional accept смешанного источника
- disposition: accepted (implementation_invariant). Ось E1/D8 и closed decisions не менялись
- Architect Gate: не требовался (уточнение исполнимого маршрута внутри выбранного носителя)
- следующий шаг: re-verify слоёв согласованности, независимого разбора и готовности

## Verify repair — template default — 2026-09-01

- alerts: implementation_invariant (умолчание копируемого шаблона; поток без связей; смешанный источник; ADR пункт 3)
- files touched: `design.md`, `specs/visual-explanation/spec.md`, `tasks.md`
- `[x]` не открывались; accept не ставился

## Verify repair — slice acceptance — 2026-09-01

- alerts: `acceptance-simplicity-overload` (S1.accept); format hygiene S2 Primary restatement
- files touched: `tasks.md` (пометы «опционально»); `design.md` (зеркало решения)
- `[x]` не открывались; accept не ставился

### Code-Truth — S2.1 — 2026-09-01
- task: S2.1
- symbols:
  - visual-explanation SKILL work-then-language @ `.cursor/skills/visual-explanation/SKILL.md`:26-80, annotation=n/a, action=modified
- verification: grep/read OK (экзамен восприятия; текущий вопрос; пустой Main не ClassificationView; перечень слоёв не отменяет скелет)
- source: orchestrator kit-markdown apply

### Code-Truth — S2.2 — 2026-09-01
- task: S2.2
- symbols:
  - panel-shell recipe library @ `.cursor/skills/visual-explanation/fixtures/panel-shell.md`:15-23, annotation=n/a, action=modified
  - ClassificationView group @ `.cursor/skills/visual-explanation/fixtures/panel-shell.md`:276-309, annotation=n/a, action=modified
  - Main form fallback @ `.cursor/skills/visual-explanation/fixtures/panel-shell.md`:391-403, annotation=n/a, action=modified
- verification: grep/read OK (нет ClassificationView на !formIsStarter; group колонка = класс)
- source: orchestrator kit-markdown apply

### Code-Truth — S2.3 — 2026-09-01
- task: S2.3
- symbols:
  - ADR-0010 form invariant @ `openspec/adrs/ADR-0010-visual-explanation-panel.md`:12-27, annotation=n/a, action=modified
- verification: grep/read OK (пункт «Решение» 3 — подсказка рецепта; Blast Radius про 0008/0009 не переписан; нового ADR нет)
- source: orchestrator kit-markdown apply

### Code-Truth — S2.4 — 2026-09-01
- task: S2.4
- symbols: []
- verification: grep/read OK against S2.4 checklist; explore/explain/overview hint alignment not in scope
- source: orchestrator kit-markdown apply

