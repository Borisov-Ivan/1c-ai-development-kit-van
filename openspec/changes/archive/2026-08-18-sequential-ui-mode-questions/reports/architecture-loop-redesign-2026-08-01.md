---
report_type: deep-analysis
generated_at: 2026-08-01
agent: onec-code-architect
mode: deep-analysis
scope:
  change: sequential-ui-mode-questions
  slices: [S2]
  files:
    - openspec/changes/sequential-ui-mode-questions/proposal.md
    - openspec/changes/sequential-ui-mode-questions/design.md
    - openspec/changes/sequential-ui-mode-questions/tasks.md
    - openspec/changes/sequential-ui-mode-questions/debug.md
    - openspec/changes/sequential-ui-mode-questions/specs/split-form-layout-modes/spec.md
    - openspec/changes/sequential-ui-mode-questions/specs/sequential-gate-questions/spec.md
  modules: []
  capabilities:
    - split-form-layout-modes
related_reports:
  - reports/design-challenge-2026-07-31.md
  - reports/design-challenge-2026-07-31-2.md
  - reports/design-challenge-2026-07-31-3.md
  - reports/architecture-task-readiness-2026-07-31.md
  - reports/architecture-task-readiness-2026-07-31-2.md
  - reports/architecture-extend-coherence-2026-08-01.md
  - reports/quality-control-2026-08-01.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Loop Redesign Audit — S2 «Раздельные режимы Form/Template»

## KB references

- Discovery выполнен, совпадений нет — секция Existing Knowledge пуста; конфликт с KB отсутствует.

## Метрика петли (вход)

| Показатель | Значение |
|------------|----------|
| Срез | S2 |
| S2.accept | `[ ]` (не подписан; apply не начинался) |
| AcceptLoop(S2) | 0 (нет Slice Gate Decisions / awaiting-acceptance) |
| PatchRounds(S2) | 3 (три секции `## Extend` в `debug.md`, правившие задачи S2) |
| Порог | `acceptance_loop_max = 3` → `max(0, PatchRounds) >= 3` — **сработало** |

**Классификация петли:** это **pre-apply design/repair thrashing**, не thrashing приёмки среза. Пользователь ещё не входил в Slice Gate; «петля» = повторные `repair-from-verify` / `user-extend`, уточнявшие контракт S2 до apply.

## Адверсариальная установка

Цель аудита — ответить: один корень или N независимых дефектов, и нужна ли consolidation vs минимальная заморозка. Источники истины: `proposal` / `design` / `tasks` / `debug` / delta-specs + связанные challenge/task-readiness/coherence/QC. Не использовались как авторитет: прошлые self-review как «уже одобрено» без перепроверки артефактов.

## Хронология раундов → что чинили

| # | Дата / тип | Триггер | Суть правок S2 | Кластер |
|---|------------|---------|----------------|---------|
| 1 | 2026-07-31 repair-from-verify | challenge-1 + task-readiness-1 | Decisions 3/6–8; Empty mode scenario; S2.1–S2.5 (формулировки, resume, kit-template, empty STOP); стык Mode vs Design Gate | **A — полнота протокола/reader** |
| 2 | 2026-07-31 repair 2 | challenge-2 | Empty включает `n/a`+UI; Pair override; Decision 7 precedence; S2.3/S2.4 | **A — те же края state space** |
| 3 | 2026-08-01 user-extend | Scope Gate + `architecture-extend-coherence-2026-08-01` (вариант 1) | Асимметрия enum; Decision 9; legacy `bsl-only` ≠ layout; S2.1/S2.3/S2.4 | **B — семантика каналов** |

После раунда 2 challenge-3 дал **APPROVE** (контракт Empty/`n/a`/Pair закрыт). Раунд 3 — не откат APPROVE, а **семантическое углубление** Why («макет программно не правят»), вскрытое Scope Gate / coherence как `drift-warning` симметричного enum.

## Root Cause Analysis

### Вердикт по корню

**Один концептуальный корень (R1), два кластера проявления (A и B) — не N независимых дефектов продукта.**

**R1 — Incomplete dual-channel mode state space at first design.**  
Первый design зафиксировал ось Option B (`form_mode` + `layout_mode` + sequential questions), но **не закрыл полную модель состояний** чтения/записи режимов:

1. порядок относительно Design Gate AskQuestion;
2. SSOT двух текстов вопросов;
3. empty / `n/a` + UI-in-scope;
4. precedence пара vs legacy;
5. асимметрия допустимых значений каналов + legacy `bsl-only` при Template;
6. guidance MXL/СКД без нового AskQuestion.

Раунды 1–2 заполняли пункты (1)–(4) инкрементально (каждый challenge находил следующий незакрытый край того же reader-контракта). Раунд 3 закрыл (5)–(6) — латентное следствие Why/What Changes, не отдельная capability и не новая цель ЗНИ.

### Почему не «три независимых бага»

| Гипотеза «независимый дефект» | Опровержение |
|-------------------------------|--------------|
| «Плохой S2.5 / resume» отдельно от Empty | Оба — пробелы выравнивания tasks↔Behavior Contract той же модели режимов |
| Pair override отдельно от Empty/`n/a` | Одна таблица precedence reader: когда legacy жив, когда пара побеждает, что значит `n/a` |
| Асимметрия enum «другая фича» | Та же capability `split-form-layout-modes`; усиливает Why про смешанные режимы; Non-Goals не ломает (сужение layout, не новый enum) — см. coherence 2026-08-01 |
| Accept-петля | AcceptLoop=0; S2.accept ни разу не подписывался |

### Усилитель процесса (не отдельный дефект постановки)

Verify Layer 4 / repair-from-verify по умолчанию чинит **ближайший gap**, не пересобирает state machine целиком → предсказуемый `PatchRounds` на контракте с многими комбинациями (empty × n/a × legacy × pair × bsl-only × Form/Template scope). Это объясняет 3 раунда при одном корне.

## Текущее состояние контракта S2 (после раунда 3)

Сверка артефактов (не «память» прошлых отчётов):

| Ось | Статус в артефактах |
|-----|---------------------|
| Раздельные поля + запись без `artifact_mode` | design Decisions 1–2, 7; tasks S2.1–S2.2 |
| Sequential Mode на design; до Design Gate | Decision 3–4; S2.2 |
| Empty / `n/a` + UI → STOP | Behavior Contract; spec Empty; S2.1/S2.3/S2.4 |
| Pair overrides legacy | Decision 7; spec Pair; S2.3/S2.4 |
| `layout_mode` без `bsl-only` | proposal What Changes; Decision 6/9; spec Layout rejected + Mixed |
| Legacy `bsl-only` ≠ layout | Decision 7; spec Legacy bsl-only; Primary S2.accept |
| Guidance MXL/СКД без AskQuestion | Decision 9; Non-Goals |
| QC Layer 2 (2026-08-01) | `OK` — 9 scenarios S2 покрыты |

**Открытых дыр state space, требующих четвёртого thin-extend, по артефактам не видно.** OQ1 coherence (silent `manual` vs STOP по layout) закрыт в сторону STOP/Mode-вопрос (Decision 7 + spec).

## Simplicity Check

- **Viable alternatives (на уровне реакции на петлю):**
  1. **Продолжить патчи** — ещё один repair-from-verify при любом мелком gap Layer 4/5.
  2. **Consolidation** — один проход: явная Mode State Matrix (все комбинации empty/`n/a`/lone legacy/pair/illegal layout bsl-only) + `closed_decisions` в `debug.md` для Decisions 6–7–9; tasks не трогать без расхождения с матрицей.
  3. **Minimal freeze** — признать state space закрытым раундом 3; запретить новые S2-extend без code-truth / apply-evidence; идти в verify → apply.
- **Selected simplest viable design (реакция):** **minimal freeze** — артефакты уже согласованы (QC OK); дополнительная перепись S2 не даёт нового наблюдаемого поведения.
- **Why not simpler than freeze:** «ничего не делать и снова thin-repair» проще на один ход, но снова поднимет PatchRounds без смены оси.
- **Why not full consolidation now:** consolidation оправдана, если ожидается ещё ≥1 раунд gaps того же state space; сейчас gaps A+B закрыты текстом. Полная пересборка design/tasks = лишний объём при уже выровненных 9 scenarios.
- **Complexity budget (S2 as-is):** 1 capability; 5 implementable tasks + accept; 0 cf/cfe; mechanical apply; Closed decisions ledger всё ещё пуст (`decision_round: 0`) — единственная дешёвая страховка от повторного reopen: при следующем verify занести Decisions 6/7/9 в ledger как `implementation_invariant`, **без** правок tasks.

## Consolidation vs минимум — сравнение

| Критерий | Consolidation | Minimal freeze | Продолжить патчи |
|----------|---------------|----------------|------------------|
| Новый наблюдаемый контракт | Нет (документирует уже записанное) | Нет | Риск микро-дрейфа формулировок |
| Стоимость | Средняя (матрица + ledger + риск лишнего diff tasks) | Низкая | Высокая (PatchRounds++, fatigue verify) |
| Защита от 4-го round | Высокая | Средняя (зависит от дисциплины «не reopen без evidence») | Низкая |
| Соответствие AcceptLoop=0 | Избыточна для приёмки | Адекватна | Маскирует design-thrashing под «прогресс» |

## Рекомендация

**`minimal`**

**Обоснование:**

1. Корень **один** (R1) — неполная dual-channel mode model; три раунда — последовательное закрытие одного state space (кластеры A→B), не три независимые ЗНИ.
2. После user-extend 2026-08-01 артефакты S2 и QC согласованы; AcceptLoop=0 — пользовательскую приёмку ещё не крутили.
3. Четвёртый thin-patch без apply-evidence повторит антипаттерн Layer-4 incrementalism.
4. Consolidation (Mode State Matrix + `closed_decisions`) — **опциональная страховка**, не обязательный redesign: если следующий verify снова откроет край того же reader-контракта → тогда один consolidation-pass вместо ещё одного точечного extend. Сейчас — **заморозить S2 и идти дальше по workflow** (полный verify → apply S1/S2).

**Явно отклонено:** `продолжить патчи` — порог уже достигнут; инкрементальные repair без новой оси увеличивают шум без выигрыша Why.

**Условный триггер на upgrade minimal → consolidation:** любой новый gap Layer 4/5 по комбинациям режимов Form/Template/legacy **без** смены Option B → не third/fourth repair bullet в S2.3, а одна матрица состояний в `design.md` + запись в Verify decision ledger.

## Источники

- `debug.md` — три `## Extend`, ledger пуст
- `proposal.md` / `design.md` Decisions 1–9 / Behavior Contract / матрица приёмки S2
- `tasks.md` S2.1–S2.5, S2.accept
- `specs/split-form-layout-modes/spec.md` — 9 scenarios
- `reports/design-challenge-2026-07-31.md` (+2, +3)
- `reports/architecture-task-readiness-2026-07-31.md` (+2)
- `reports/architecture-extend-coherence-2026-08-01.md`
- `reports/quality-control-2026-08-01.md` — Slice Coherence OK
