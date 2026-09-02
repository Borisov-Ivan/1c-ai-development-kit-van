---
verify_mode: pre-apply
change: explore-reports-into-change
date: 2026-09-02
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
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-09-02T12:21:27+09:00"
    design.md: "2026-09-02T12:20:20+09:00"
    tasks.md: "2026-09-02T12:21:27+09:00"
    specs/explore-report-intake/spec.md: "2026-09-02T12:19:52+09:00"
    specs/explore-report-promote/spec.md: "2026-09-02T12:19:30+09:00"
  last_challenge_at: "2026-09-02T12:20:20+09:00"
---

## Резюме для разработчика

explore-reports-into-change — можно запускать apply. Правки только markdown kit: правило сохранения отчётов, скиллы создания/дополнения/исследования, шаблоны агентов.

После исследования с отчётом создание ЗНИ переносит файлы темы в `openspec/changes/<name>/reports/` и убирает их из `temp`. В начале отчёта обследования / трассы / архитектурного разбора исследования — шапка с объектом и понятной формулировкой запроса, не дословной цитатой чата. Список путей в чат-постановку не добавляется.

**Следующий шаг:** `/opsx:apply explore-reports-into-change`

Приёмка первого среза: создать ЗНИ по теме с превью отчёта и открыть каталог задачи. Приёмка второго: открыть файл отчёта и прочитать шапку. Код 1С и конфигурация не меняются.

### К сведению

- Кода 1С нет, `form_mode: n/a`, ручной конфигурации в Конфигураторе нет.
- Apply mechanical: правки markdown правил и скиллов.
- Опциональный файл передачи ищется в корне `temp/` (`explore-handoff-*.md`), не в `temp/reports/`. Переезд и поиск «продолжи вчерашний» берут только имена из allowlist, не любой `architecture-*`.

## Что меняется в постановке

**Расширение / конфигурация:** не затрагивается. Меняется kit: `.cursor/rules/preserve-subagent-reports.mdc`, скиллы `openspec-new-change` / `openspec-extend-change` / `openspec-explore` / `openspec-explain`, три файла агентов, стиль чата.

**Точки изменения:**

- правило сохранения отчётов — переезд кандидатов в каталог ЗНИ сразу после появления папки change, до записи постановки;
- скилл создания ЗНИ — тот же переезд + перепись `report:` на путь внутри ЗНИ;
- скилл дополнения — переезд, если источник ещё в `temp`;
- поиск «продолжи вчерашний» — каталоги ЗНИ за 7 дней по тому же списку имён;
- шаблоны вывода агентов и страховка оркестратора — шапка `## Вводные`.

**Что НЕ меняется:** граница тонкий чат / полный материал в файле (ADR-0001); архивная ЗНИ `kit-evolution-models-economy-profiles`; каталог сессий; обязательный файл передачи; сохранение брифа в `temp/briefs/`.

**Связанные ADR / KB / архив:** ADR-0001 (extends); архив `2026-08-01-chat-surface-clarity`; архив `2026-08-18-kit-evolution-models-economy-profiles` (adjacent).

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы, по одному `S<N>.accept` и `<!-- slice-gate -->` на срез, префиксы ID, `form_mode: n/a`.
- **Layer 2 (Internal Coherence):** PASS; QC: `reports/quality-control-2026-09-02-3.md` (Verdict OK; CRITICAL/WARNING нет). User Task Contract pre-check: none. Precedent: дельты ADDED, не MODIFIED/REMOVED; ADR-0001 extends с `## Blast Radius` → INFO `precedent-documented`. Code-truth: kit markdown, `openspec/project.md` отсутствует, символы BSL не заявлены.
- **Layer 2.5 (Loop Detection):** PASS. `S1.accept` / `S2.accept` = `[ ]`, записей awaiting-acceptance нет.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт двумя capability; у каждого Requirement есть Scenario; implementation-leak в THEN нет; comment_suffix пуст.
- **Layer 4 (Independent Challenge):** APPROVE; отчёт: `reports/design-challenge-2026-09-02-2.md` (шесть уточнений контракта закрыты). Первый прогон `reports/design-challenge-2026-09-02.md` был CHALLENGE → internal repair-from-verify (`repair_attempt: 1`).
- **Layer 5 (Implementation Readiness):** PASS; отчёт: `reports/architecture-task-readiness-2026-09-02-2.md` (ГОТОВО, GAP нет). Маркеров ручной конфигурации не найдено.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

нет (после repair Layer 4 APPROVE)

## Источники

- `reports/quality-control-2026-09-02-3.md`
- `reports/design-challenge-2026-09-02.md` (CHALLENGE → repair)
- `reports/design-challenge-2026-09-02-2.md` (APPROVE)
- `reports/architecture-task-readiness-2026-09-02-2.md`
- `debug.md` § Extend — 2026-09-02
- алерты: none blocking; `precedent-documented` (INFO)
