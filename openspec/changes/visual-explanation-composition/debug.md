## Verify decision ledger

```yaml
closed_decisions:
  - id: hint-slots-explain-overview
    summary: "Намёк на схему в пошаговом разборе и в обзоре проекта в эту поставку не входит; схему там запрашивают прямой просьбой. Свободный чат и исследование получают критерий путаницы частей, слоёв или случаев."
    closed_at: "2026-08-31"
    source: verify-user-answer
open_decision_id: null
decision_round: 1
decision_round_max: 2
verify_depth: incremental
assumptions_accepted: []
last_challenge_at: "2026-08-31T03:20:25Z"
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

