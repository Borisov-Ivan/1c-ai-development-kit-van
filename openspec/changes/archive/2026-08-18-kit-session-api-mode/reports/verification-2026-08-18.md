---
verify_mode: pre-apply
change: kit-session-api-mode
date: 2026-08-18
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
  closed_decisions: []
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-08-18T08:42:20"
    design.md: "2026-08-18T08:44:24"
    tasks.md: "2026-08-18T08:44:18"
    specs/session-api-mode/spec.md: "2026-08-18T08:43:17"
  last_challenge_at: "2026-08-18T08:44:24"
---

## Резюме для разработчика

kit-session-api-mode — можно запускать apply. Ключ `-noapi` направляет следующие дорогие вызовы на модель чата; после лимита без повторного удара. Таблица ролей на месте.

**Следующий шаг:** `/opsx:apply kit-session-api-mode`

План дописывает режим сессии в `.cursor/rules/model-selection.mdc`: токены `-noapi` / `-api` (и с двумя дефисами) как целые слова после разбиения по пробелам, память только после лимита / недоступности / ошибки выбора модели, пропуск первого шага цепочки на новых вызовах. Cue на каждом ходе — в `.cursor/rules/session-discipline.mdc` и чеклисте `.cursor/rules/tool-name-guard.mdc`. Справка — FAQ kit и одна строка в палитре дорогих команд. Кода 1С и метаданных нет.

Подправил в постановке: разбор ключа как отдельного слова, запрет повторной строки после лимита, ключ на дешёвой команде всё равно переключает режим, палитра включает explore и extend.

## Что меняется в постановке

**Расширение / конфигурация:** kit-метапроект, только `.cursor/**`. Выгрузки 1С нет.

**Точки изменения:**

- `.cursor/rules/model-selection.mdc` — секция режима сессии поверх таблицы ролей и двухшаговой цепочки.
- `.cursor/rules/tool-name-guard.mdc` — пункт чеклиста: в режиме без API не передавать платную модель.
- `.cursor/rules/session-discipline.mdc` — cue: перед каждым вызовом с конкретной моделью проверить токены сообщения, затем память, затем таблицу ролей.
- `.cursor/docs/faq-kit.md` — как включить / выключить ключом и чем это не пропуск архитектора.
- `.cursor/commands/opsx-new.md`, `opsx-verify.md`, `opsx-apply.md`, `opsx-extend.md`, `opsx-explore.md`, `review.md`, `release-review.md` — одна строка, что ключ пишется в чате и не флаг команды.

**Что НЕ меняется:** таблица «Роли и Task.model», запрет эскалации как запаса после сбоя, самосверка имён моделей, `openspec/project.md`, код 1С.

**Связанные ADR / KB / архив:** ADR-0001 (строка без слага после лимита); ось `kit-evolution-models-economy-profiles` (двухшаговая цепочка) расширяется, не отменяется.

### К сведению

- Новый чат снова начинается «с API»: если лимита нет — напишите `-noapi` в первом сообщении.
- Сетевой таймаут сам по себе режим на весь чат не включает.
- `-noapi` не заменяет `--skip-architect` и не создаёт обход гейта.
- Таксономии базы знаний в kit нет; Discovery пуст.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте, `<!-- slice-gate -->` на S1 и S2, `form_mode: n/a`, `<!-- phase-gate -->` нет, fences сбалансированы.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-18-2.md` (15/15 Scenario, CRITICAL нет). User Task Contract 2.1a: none. Code-Truth: n/a (нет символов BSL; пути `.cursor/**` существуют). Precedent: только ADDED `session-api-mode`; Blast Radius документирует extends `kit-evolution-models-economy-profiles` → INFO `precedent-documented`. Invariant KB: taxonomy отсутствует.
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` без Slice Gate Decisions / awaiting-acceptance; AcceptLoop=0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт четырьмя Requirement; у каждого Requirement ≥1 Scenario; 15 Scenario в design § Slices и в S1/S2 (accept или `S<N>.<M>`). `scenario-implementation-leak`: нет. `process-only-marker-suffix`: `comment_suffix` пустой + `marker_style: minimal` — допустимо.
- **Layer 4 (Independent Challenge):** APPROVE (после Repair Loop). Первый прогон: CHALLENGE / implementation_invariant (`reports/design-challenge-2026-08-18.md`). Repair закрыл 6 gaps. Повтор: APPROVE (`reports/design-challenge-2026-08-18-2.md`). last_challenge_at = mtime design.md.
- **Layer 5 (Implementation Readiness):** PASS. `reports/architecture-task-readiness-2026-08-18-2.md` — ГОТОВО; GAP нет. Manual config 5.1: маркеров не найдено.

### Авто-исправлено (Layer 1)

mechanical-замечаний не обнаружено

### Repair Loop

- attempt 1: repair-from-verify по gaps design-challenge (токен=слово; дешёвая команда не глотает сигнал; без повторной строки после памяти; cue на каждый ход; палитра explore/extend; разовый слаг+токен). Артефакты: proposal.md, design.md, spec.md, tasks.md, debug.md. Decision blockers не всплыли.
- attempt 2: не требовался.

### Развёрнутые карточки развилок

Нет.

## Источники

- `reports/quality-control-2026-08-18-2.md` (прогон 1: `quality-control-2026-08-18.md`)
- `reports/design-challenge-2026-08-18.md`, `reports/design-challenge-2026-08-18-2.md`
- `reports/architecture-task-readiness-2026-08-18-2.md` (прогон 1: `architecture-task-readiness-2026-08-18.md`)
- `reports/architecture-new-2026-08-17.md` — не источник Layer 4
- Алерты: `precedent-documented` (INFO)
