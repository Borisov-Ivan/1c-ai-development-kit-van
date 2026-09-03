---
report_type: design-challenge
generated_at: 2026-09-02
agent: onec-code-architect
mode: design-challenge
scope:
  change: explore-reports-into-change
  design_mtime: "2026-09-02T12:20:20+09:00"
verdict: APPROVE
confidence: high
---

# Design Challenge — explore-reports-into-change

## Адверсариальная установка

Повторный независимый разбор **после repair**: читались только текущие `proposal.md`, `design.md`, `specs/explore-report-intake/spec.md`, `specs/explore-report-promote/spec.md`, `tasks.md` и живые правила kit (`preserve-subagent-reports.mdc`, `openspec-new-change/SKILL.md`, `openspec-explore/SKILL.md` Continuity, `openspec-explain/templates/explain-report.md`, ADR-0001). Предыдущие `reports/architecture-*.md` и `reports/design-challenge-2026-09-02.md` **не** использовались как источник истины. Ось «переезд + шапка в файле, чат без перечня путей» не переоткрывалась: новых verified-фактов, отменяющих Decisions 1–12, в коде нет.

## KB references

- KB Discovery пропущен, taxonomy отсутствует — not relevant: на выводы по постановке не влияет.

## Дельта: шесть уточнений контракта

| # | Уточнение | Где закрыто | Статус |
|---|-----------|-------------|--------|
| 1 | Кандидат файла передачи: `temp/explore-handoff-*.md` в корне `temp/`, не только `temp/reports/` | proposal What Changes п.3; design Behavior Contract п.2, Decision 11, Risks; spec promote Scenario «Handoff file moves only if it exists»; tasks S1.1, S1.9, S1.accept | закрыто |
| 2 | Положительный allowlist имён (не префикс `architecture-*`); deny служебных отчётов проверки/приёмки; тот же набор у Continuity | design п.3 и п.9, Decision 11, Implementation Options; spec promote Continuity AND; tasks S1.1, S1.5, S1.9 | закрыто |
| 3 | «Исходный запрос» при дописывании шапки: слот «Вопрос» или сжатие 1–2 предложения, не полная реплика чата | proposal Decision 5 + Acceptance 2; design п.12, 15, Decision 5 и 12; spec intake «Original request…» и AND у «Missing header…»; tasks S2.1, S2.5, S2.10, S2.accept | закрыто |
| 4 | Пятипольная шапка обязательна у отчётов исследования, не у служебных отчётов проверки постановки | design п.11, Decision 12; spec intake «Intake header…» MUST NOT у служебных; tasks S2.1, S2.4, S2.10 | закрыто |
| 5 | Переезд до записи proposal/design и до проверки постановки на design — MUST | design Behavior Contract п.1 (**до** записи proposal/design и **до** проверки); Existing Mechanisms п.3; tasks S1.2 (тот же порядок, не ослаблен) | закрыто |
| 6 | После переезда журнала разбора href на `src/` с глубины каталога ЗНИ (`../../../../src/`) | design п.6; spec promote Scenario «Reports of this topic…» AND; tasks S1.1, S1.7, S1.9 | закрыто |

Ослабления MUST по пункту 5 в design/tasks нет. Spec promote фиксирует наблюдаемый исход (файл в каталоге ЗНИ, рабочая ссылка журнала), порядок относительно проверки постановки держит design+S1.2 — этого достаточно для оси, отдельная scenario «до проверки постановки» не меняет код/поведение относительно уже записанного MUST.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** исследование кладёт полный отчёт в `temp`, при создании ЗНИ файл остаётся снаружи каталога задачи (`temp` не в git); открыв отчёт позже, нельзя вспомнить объект проблемы — в файле есть разбор кода, нет исходных вводных.
- **Design адресует:**
  - Why «файл снаружи / не в git» → переезд (не копия) кандидатов темы в `openspec/changes/<name>/reports/` сразу после появления каталога, до записи артефактов и до проверки постановки; после успеха исходника в `temp` нет; поле `report:` переписывается на путь внутри ЗНИ (п.1, 6–8).
  - Why «в отчёте нет вводных» → шапка `## Вводные` у обследования / трассы / архитектурного разбора исследования: понятный исходный запрос, область, объекты/пути, симптом, вопрос (п.11–15); журнал разбора — Мета, без второй шапки (п.16).
- **Покрытие:** полное.
  - Why говорит о потере фактуры → design адресует через переезд + поиск продолжения по каталогам ЗНИ с тем же allowlist (п.9). Живой код это подтверждает: сейчас Continuity без имени ЗНИ смотрит только `temp/reports/*.md` (`openspec-explore/SKILL.md:35–36`); проверка постановки ищет `architecture-*.md` уже в `reports/` ЗНИ (`openspec-new-change/SKILL.md:288–296`) — без переезда до этой проверки отчёт исследования остаётся в `temp`.
  - Why говорит о «с каким объектом пришли» → design адресует шапкой из названного пользователем, не из найденного кода (п.13).
  - Why не требует перечень путей в чате — design п.7, 19 и ADR-0001 extends (Blast Radius).

### Q2 — Optimality

- **Выбранный путь:** переезд по цитатам сессии + запасной glob 48 ч ∩ тема с положительным allowlist; отдельный корень `temp/` для опционального файла передачи; шапка в файле (агент пишет, оркестратор дописывает без вставки полной реплики); чат без списка файлов.
- **Альтернативы (включая не упомянутые в design `## Implementation Options`):**
  1. **Снять игнор с `temp/reports/` (или whitelist `exploration-*` в git) без переезда в каталог ЗНИ.** Реализуется правкой `.gitignore`. Плюс: меньше точек правки в new/extend. Минус: фактура не привязана к задаче; параллельные темы остаются общей кучей; «продолжи вчерашний» без имени ЗНИ не знает, какой файл чей; Why явно: «файл остаётся снаружи каталога задачи». Отклонена: закрывает только git, не каталог ЗНИ.
  2. **Вклеить тело отчёта или шапку вводных в `proposal.md` как приложение, файлы оставить в `temp`.** Плюс: один git-файл постановки. Минус: proposal раздувается; Continuity по-прежнему ищет `exploration-*`; открытие исходного отчёта Why не лечит; дублирование с `reports/`. Отклонена: бьёт не в тот артефакт.
  3. **Копия в каталог ЗНИ + оригинал в `temp`.** Упомянута в Options и отвергнута постановкой («переезжал»). После копий Continuity находит дубли. Не лучше.
  4. **Префикс `architecture-*` без deny.** Упомянута и отвергнута. Живой факт: в каталоге этой же ЗНИ уже лежат `architecture-task-readiness-*` и `design-challenge-*` рядом с исследовательским `architecture-YYYY-MM-DD-<тема>.md`. Префикс для переезда и Continuity подмешал бы служебное. Положительный allowlist лучше.
- **Вердикт по Q2:** оптимален. Ни одна неназванная альтернатива не даёт меньший Blast Radius при полном покрытии Why: переезд переиспользует уже существующие save/ingest/выход агентов; шапка не тащит служебное в чат (ADR-0001); allowlist закрывает дыру Continuity после переезда.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** да
- **Причины:**
  - Две боли Why мапятся на два механизма без лишнего контура (нет каталога сессий, нет обязательного файла передачи, нет поля «Отчёты» в чат-блоке).
  - Порядок «каталог → переезд → proposal/design → проверка постановки» совпадает с дырой в текущем `openspec-new-change` (проверка смотрит `reports/` ЗНИ, запись исследования — в `temp/reports/`).
  - Repair добил операционные дыры (корень handoff, allowlist≠префикс, слот «Вопрос» вместо полной реплики, шапка не на служебных отчётах, href журнала), не сменив ось.

## Verdict

**APPROVE** — шесть уточнений закрыты в design/specs/tasks, Why покрыт полностью, ось переезда и шапки в файле подтверждается живым кодом kit, равноправной лучшей альтернативы нет.

## Gaps for design.md

(нет)

## Architectural alternatives

(нет равноправных путей по коду: копия, git-only `temp`, вклейка в proposal меняют наблюдаемое поведение хуже Why; reopen Decisions 1–12 без нового verified-факта запрещён.)

## Источники

- proposal.md — `## Why`; What Changes п.1–5; Scope / Out of scope; Acceptance 1–5; Decision 5
- design.md — Goals/Non-Goals; Existing Mechanisms п.1–3; Behavior Contract п.1–20; Implementation Options; Decisions 1–12; Blast Radius; Slices S1/S2
- specs/explore-report-intake/spec.md — Intake header; Original request; Missing header AND про слот «Вопрос»
- specs/explore-report-promote/spec.md — Reports move; Handoff в корне `temp/`; Continuity AND про служебные отчёты; AND про href журнала
- tasks.md — S1.1–S1.9, S1.accept; S2.1, S2.4, S2.5, S2.10, S2.accept
- Код (verified) — `preserve-subagent-reports.mdc:18–21` (есть ЗНИ → change/reports, нет ЗНИ → temp/reports, переезда нет); `openspec-new-change/SKILL.md:33` (`Glob temp/explore-handoff-*.md`); `openspec-new-change/SKILL.md:288–296` (проверка постановки: `architecture-*.md` в `reports/` ЗНИ после записи design); `openspec-explore/SKILL.md:35–36` (Continuity без имени ЗНИ — только `temp/reports`); `openspec-explain/templates/explain-report.md:31–34` (канон глубин `../../src/` vs `../../../../src/`); `openspec/adrs/ADR-0001-chat-facing-vs-agent-facing.md` (thin chat vs файл — extends)
