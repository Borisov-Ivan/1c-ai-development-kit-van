---
verify_mode: pre-apply
change: kit-session-noapi-visibility-and-ru-progress
date: 2026-08-19
verdict: GO
layer_status:
  layer_1_hygiene: AUTOFIXED
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: APPROVE
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
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "2026-08-19T19:21:21+09:00"
    design.md: "2026-08-19T19:10:14+09:00"
    tasks.md: "2026-08-19T19:21:20+09:00"
    specs/chat-model-profiles/spec.md: "2026-08-19T14:01:42+09:00"
    specs/chat-surface-clarity/spec.md: "2026-08-19T19:06:50+09:00"
    specs/sequential-gate-questions/spec.md: "2026-08-19T19:06:50+09:00"
    specs/session-api-mode/spec.md: "2026-08-19T19:06:41+09:00"
    specs/subagent-model-mapping/spec.md: "2026-08-19T15:46:42+09:00"
  last_challenge_at: "2026-08-19T19:10:14+09:00"
---

## Резюме для разработчика

kit-session-noapi-visibility-and-ru-progress — можно запускать apply. После лимита в чат уходит канон первой строкой; команды `/opsx:*` говорят по-русски; на ЗНИ без кода 1С вопрос маркера не задаётся.

План дописывает правила kit, не код 1С: бюджет чата, правило выбора моделей, протоколы `/opsx:new` / `/opsx:apply` / `/opsx:verify`. Третьего режима сессии нет, токен `-noapi` оркестратор по-прежнему не печатает.

Подправил в постановке: канон — первая строка и не ждёт финала проверки; вопрос маркера пропускается только когда ясно, что правятся правила kit; в задачи среза сигнала добавлены два места со старой фразой про модель разбора.

**Следующий шаг:** `/opsx:apply kit-session-noapi-visibility-and-ru-progress`

## Что меняется в постановке

- После липкого сбоя (лимит / недоступность / ошибка выбора модели) первая строка хода — «дорогие модели недоступны — дальше на модели чата». Фраза живёт в always-apply бюджете чата, не только в on-demand правиле выбора моделей.
- В `/opsx:verify` эта строка и «Модель архитектора: Opus 5» уходят до карточки вердикта.
- Progress и вводная речь `/opsx:*` — только русские.
- Metadata Gate: пропуск вопроса маркера только при доказанном kit-only; деловая постановка без `.bsl` — спросить.
- Не меняется: таблица ролей, ADR-0004, печать `-noapi`, файл-состояние режима, код 1С.

Связанные решения: ADR-0004 (режим сессии), ADR-0001 (строка без слага). Архив: `kit-session-api-mode`, `kit-evolution-models-economy-profiles`.

### Подправил в постановке

- Дописал в постановку: канон — первая строка; фраза дословно в бюджете чата; исключение verify из «одно сообщение»; §1b разведён на «канон» и «язык».
- Уточнил пропуск маркера: только доказанный kit-only; добавлен сценарий деловой постановки без `.bsl`.
- В задачи среза сигнала добавил протокол `/opsx:verify` и правило коммуникации verify, где ещё жила старая фраза про модель разбора.

### К сведению

- На apply среза сигнала и среза языка не смешивать абзацы одного файла бюджета: сигнал владеет §5 и пунктом «канон», язык — §6 и пунктом «язык». Счёт пунктов §1b править по факту после своего среза.
- Канон — первая строка **первого** сообщения хода; карточка вердикта verify сохраняет своё требование «вердикт в первой строке».
- При `developer: n/a` снимок сессии не должен показывать предпросмотр маркера с «n/a» — на apply среза маркера учесть, если трогаете `openspec-status`.
- Precedent: MODIFIED `subagent-model-mapping` — extends, Blast Radius заполнен; таблица ролей не отменяется.

## Технический аудит (для движка OpenSpec)

### Авто-исправлено (Layer 1)

| # | Что | Было | Стало |
|---|-----|------|-------|
| 1 | Покрытие файлов S1.4 / S1.15 | SKILL verify не в списке замены «дорогая эскалация недоступна» | Добавлен `.cursor/skills/openspec-verify-change/SKILL.md` |
| 2 | Покрытие файлов S1.16 / S1.18 | Исключение «канон не ждёт финала» без `verify-user-communication.mdc` | Добавлен `.cursor/rules/verify-user-communication.mdc` |

Чекбоксы, slice-gate, form_mode n/a, fences — без дефекта формы.

### Слои

- Layer 1 hygiene: AUTOFIXED
- Layer 2 internal coherence: PASS (`quality-control-2026-08-19-4.md` Verdict OK, 14/14 Scenario, alerts нет)
- Layer 2.5 loop detection: PASS (нет Slice Gate Decisions / awaiting-acceptance)
- Layer 3 problem-solution: PASS (Why покрыт; у каждого Requirement есть Scenario; implementation-leak в THEN нет; comment_suffix пустой)
- Layer 4 independent challenge: APPROVE (`design-challenge-2026-08-19-4.md`, confidence high)
- Layer 5 implementation readiness: WARNING (`architecture-task-readiness-2026-08-19-3.md` READY_WITH_REMARKS; GAP покрытия файлов закрыт авто-вставкой в tasks; остаток — инварианты формулировок на apply, не блокеры)

### Layer 2.4 precedent

- MODIFIED `subagent-model-mapping` vs archive `2026-08-18-kit-evolution-models-economy-profiles`: чатовая строка при отсутствии слага, таблица ролей сохранена. `## Blast Radius` = extends. Алерт: `precedent-documented` (INFO).
- ADDED дельты session-api-mode / chat-surface-clarity / chat-model-profiles / sequential-gate-questions: extends архивных контрактов, без REMOVED.
- Load-Bearing ADR-0004 / ADR-0001: Supersedes нет.
- Invariant KB: taxonomy отсутствует, Discovery пропущен.

### Code-Truth

- status: OK
- kit-метапроект, `openspec/project.md` нет; технических символов BSL нет.

### User Task Contract pre-check

- none (ALLOW-agent static «верифицировать по тексту»)

### Repair Loop

- attempt 1: prior cycle (debug)
- attempt 2: internal repair-from-verify по `design-challenge-2026-08-19-3.md` (implementation_invariant) → повтор слоёв → Layer 4 APPROVE
- post-L5 snippets: file-list completeness в tasks (не новый цикл repair)

## Источники

- `openspec/changes/kit-session-noapi-visibility-and-ru-progress/reports/quality-control-2026-08-19-4.md`
- `openspec/changes/kit-session-noapi-visibility-and-ru-progress/reports/design-challenge-2026-08-19-4.md`
- `openspec/changes/kit-session-noapi-visibility-and-ru-progress/reports/architecture-task-readiness-2026-08-19-3.md`
- alerts: `precedent-documented` (INFO)
