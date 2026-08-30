---
verify_mode: pre-apply
change: last-slice-review-or-archive
date: 2026-08-30
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
    proposal.md: "2026-08-30T09:28:02"
    design.md: "2026-08-30T09:27:58"
    tasks.md: "2026-08-30T09:28:21"
    specs/chat-surface-clarity/spec.md: "2026-08-30T09:01:34"
  last_challenge_at: "2026-08-30T09:27:58"
---

## Резюме для разработчика

last-slice-review-or-archive — можно запускать apply. После «принято» на последнем срезе ЗНИ с кодом расширения в чате три слова: `ревью`, `архив`, `стоп`; `ревью` печатает `/release-review` с именем ЗНИ и не запускает ревью в этой сессии.

План правит скилл реализации: один вопрос и на фразе «принято», и при возврате в сессию, и если открыть реализацию, когда всё уже принято. Слова `архив` и `стоп` как сейчас. Без кода расширения третьего слова нет. Прямая команда архива из нового чата по-прежнему без этого вопроса.

Подправил в постановке: закрыл вход «все задачи уже закрыты», который иначе снова предлагал бы только архив.

**Следующий шаг:** `/opsx:apply last-slice-review-or-archive`

Полный отчёт: openspec/changes/last-slice-review-or-archive/reports/verification-2026-08-30.md

## Что меняется в постановке

**Расширение / конфигурация:** продуктовый `src/` не трогается. Правки в `.cursor/skills/openspec-apply-change/SKILL.md`, `.cursor/docs/review-guide.md`, `.cursor/docs/opsx-output-style.md`.

**Точки изменения:**

- Скилл реализации, шаг 6 шортката «принято» — бинарный вопрос архива становится развилкой из трёх слов при коде расширения.
- Там же шаг 7 шортката — разбор `ревью` / `архив` / `стоп`; на `ревью` одна команда `/release-review <имя-ЗНИ>`.
- Шаг 5, ветка «Принят» — последний срез ведёт на ту же развилку.
- Шаг 3, состояние «все задачи закрыты» — не печатает своё «предлагаю архив», а после признака кода расширения идёт на карточку завершения.
- Карточка «реализация завершена» (чат) — та же развилка; файл `reports/handoff-final-*.md` — перечень команд без вопроса.
- Памятка оформления, строка варианта `final` — согласована со скиллом.
- Памятка ревью, таблица «Когда что вызывать» — строка про момент после последнего среза.

**Что НЕ меняется:** слот следующего шага проверки постановки после реализации (по-прежнему команда архива); поведение `архив` и `стоп`; автоархив по слову `архив`; обычное `/review`; прикладная конфигурация 1С.

**Связанные ADR / KB / архив:** ADR-0002 применяется (предложить команду, не запускать); ADR-0001 и ADR-0003 не отменяются. Класс `extends` к `archive/2026-08-09-explain-after-review-apply-scope`. Дельта spec — ADDED к `chat-surface-clarity`, без отмены main-спеки.

### Подправил в постановке

- Дописал вход «открыли реализацию, а все задачи уже закрыты»: не отдельный текст про архив, а та же развилка после признака кода расширения.
- Разделил чат и файл завершения: вопрос — только в чат; в файле — перечень команд.
- Согласовал строку финала в памятке оформления со скиллом.
- Зафиксировал: прямая команда архива из нового чата предрелиз не предлагает.

### К сведению

- При правке строки `final` в памятке оформления можно одной фразой уточнить примеры в правиле «один сигнал ответственности» (финал с развилкой — ответ в чате, не команда). Отдельная задача не нужна.
- Повторный вход в полностью принятую ЗНИ в тот же день может дать второй файл `handoff-final` с суффиксом — как у действующего правила записи handoff, на чат не влияет.
- Маркеров ручной конфигурации 1С нет; `form_mode: n/a`. Таксономия KB в kit отсутствует.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы, один `S1.accept`, `<!-- slice-gate -->`, fences, `form_mode: n/a`. Авто-гигиена не применялась.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-30-3.md` (`OK`, алертов нет). User Task Contract pre-check: none. Precedent 2.4: дельта spec только ADDED, нет пары ADDED→MODIFIED/REMOVED; Load-Bearing ADR-0001 не Supersedes; KB index отсутствует. Code-Truth: kit markdown, `openspec/project.md` нет; 1С-символов в контракте нет.
- **Layer 2.5 (Loop Detection):** PASS. `S1.accept` = `[ ]`; `debug.md` без Slice Gate Decisions; AcceptLoop/PatchRounds = 0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт Requirement «Last-slice acceptance offers prerelease or archive»; 8 Scenario; все в `## Slices` и в S1 (accept или S1.9). Implementation-leak в THEN нет. `comment_suffix` пуст при `marker_style: minimal`.
- **Layer 4 (Independent Challenge):** APPROVE. Первый прогон `reports/design-challenge-2026-08-30.md` — CHALLENGE (непокрытый `all_done` шага 3, развилка в файле handoff, молчание про прямой архив). Repair-from-verify закрыл три пробела. Повтор `reports/design-challenge-2026-08-30-2.md` — APPROVE. `last_challenge_at` = mtime design.md.
- **Layer 5 (Implementation Readiness):** PASS. Первый прогон `reports/architecture-task-readiness-2026-08-30.md` — READY_WITH_NOTES (два GAP покрытия). После repair `reports/architecture-task-readiness-2026-08-30-2.md` — READY, `gaps_count: 0`. Manual-config маркеров нет. Mechanical apply.

### Авто-исправлено (Layer 1)

не применялось

### Repair Loop

- attempt: 1
- class: implementation_invariant (без смены оси Chosen)
- sources: design-challenge-2026-08-30.md, architecture-task-readiness-2026-08-30.md
- debug: `## Verify repair — implementation invariant — 2026-08-30`

### Развёрнутые карточки развилок

нет (после classifier и repair)

## Источники

- `reports/quality-control-2026-08-30-3.md`
- `reports/design-challenge-2026-08-30.md` (CHALLENGE, закрыт repair)
- `reports/design-challenge-2026-08-30-2.md` (APPROVE)
- `reports/architecture-task-readiness-2026-08-30.md` (GAP, закрыты repair)
- `reports/architecture-task-readiness-2026-08-30-2.md` (READY)
- `debug.md` § Verify repair — implementation invariant — 2026-08-30
