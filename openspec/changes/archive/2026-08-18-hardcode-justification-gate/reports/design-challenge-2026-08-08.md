---
report_type: design-challenge
generated_at: 2026-08-08
agent: onec-code-architect
mode: design-challenge
scope:
  change: hardcode-justification-gate
  design_mtime: "2026-08-08T05:31:12Z"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — hardcode-justification-gate

## Адверсариальная установка

Независимый проход: прочитаны только `proposal.md`, `design.md`, `specs/hardcode-justification-gate/spec.md`; для проверки зеркала каркаса Попытка и поверхности поставки — точечная сверка текущих `.cursor` (Phase 2.5 в reviewer/reviewer-checks, AP-054 как последний номер, индекс `bsl-antipatterns.mdc` → полные карточки в docs). Отчёты `reports/architecture-*.md` **не** использовались как источник истины. Closed decisions отсутствуют (первый verify).

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** architect предлагает allow-list имён форм как «тонкий» охват; writer вливает литералы; reviewer без выделенного прохода; на приёмке отклоняет заказчик; в kit нет зеркала каркаса Попытка (реестр + HALT + выделенный проход + completeness) для runtime-фильтра по строкам метаданных/форм.
- **Design адресует:**
  - Why «нет каркаса» → AP-055 + Identity Filter Gate + writer G21 + reviewer Phase 2.6 (completeness) — явное зеркало G14/G19/Phase 2.5.
  - Why «architect сам рекомендует список» → HALT из трёх вопросов + секция Hardcode Justification до Chosen.
  - Why «reviewer не ловит до приёмки» → Phase 2.6 + MUST_FIX при contradiction с «без хардкода».
  - Граница «не трогать consumer / не путать с литералами протокола» → Non-Goals + spec scenario «Protocol literals are out of class by default».
- **Покрытие:** полное по заявленному Why. Частичный риск — не в постановке, а в **доставке**: матрица срезов ослабляет обязательность Phase 2.6 / contradiction относительно Behavior Contract и spec (см. Gaps).

### Q2 — Optimality

- **Выбранный путь:** полный 4-слойный каркас (AP + architect Gate + writer G21 + reviewer Phase 2.6) одним change, три среза (Option A).
- **Альтернативы (включая не упомянутые в design ## Implementation Options):**
  1. **Option D — Расширить Phase 2.5 / Contract Map вместо Phase 2.6** — identity-literals как ещё одна completeness-таблица внутри Попытка & Contract Audit. Плюсы: меньше фаз, один «аудитный» якорь. Минусы: смешивает ортогональные классы (внешний фактор / контракт данных vs охват UI литералами); Why и Behavior Contract требуют **выделенный** проход по аналогии с 2.5, не растворение. Отклонена: хуже Problem-Solution Fit.
  2. **Option E — Оркестраторский mechanical grep в writer-pipeline (как AP-054 Comment Hygiene) без Phase 2.6** — evidence `ИмяФормы = "` / `ОткрытьФорму("` до reviewer. Плюсы: дешёвый сигнал, паттерн уже есть для Export Language. Минусы: Попытка-каркас держится на agent gates + выделенном Phase, не на единственном orchestrator grep; open question design уже откладывает verify-grep; без G21/Gate остаётся протекание на этапе Chosen design. Отклонена: не закрывает Why «зеркало каркаса».
  3. **Option F — Только запах Scope-as-literals + существующий G20** — без нового G21 и Phase 2.6. Плюсы: минимум правок. Минусы: повторяет дыру «запись в standards без прохода» (близко к отклонённому Option C); G20 завязан на конфликт с уже существующей нормой — без AP/Phase нормы нет. Отклонена.
  4. **Option H — Жёсткий запрет allow-list (без Hardcode Justification)** — всегда только callee/API/настройка. Плюсы: проще бинарный вердикт. Минусы: шире Why (нужен justification gate, не абсолютный запрет); ломает легитимный закрытый набор «навсегда» из Gate-вопросов. Отклонена как overreach.
- **Вердикт по Q2:** выбранный Option A оптимален среди жизнеспособных путей для заявленного Why; ни одна неупомянутая альтернатива не превосходит по сочетанию Fit + Blast Radius + обратимости. Недостатки — в полноте поверхности поставки (implementation_invariant), не в выборе оси.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками
- **Причины:**
  - Да: Why ↔ design ↔ spec согласованы; зеркало Попытка узнаваемо и минимально достаточное для kit-эволюции без прикладного BSL.
  - Да: граница protocol/enum и out-of-scope consumer зафиксированы — снижает ложные MUST_FIX.
  - Оговорка: до apply нужно устранить расхождение «Primary vs optional» в матрице срезов и явно перечислить файлы зеркала Phase 2.5 (docs-карточка AP, writer bulletin, `review/SKILL.md` / `1c-agent-patterns`), иначе поставка может формально закрыть S3 по G21, не включив обязательный completeness-проход в местах, где сегодня зашит только 2.5.

## Verdict

**CHALLENGE** — ось решения верная и оптимальная, но перед apply остаются implementation_invariant gaps (матрица приёмки S3 и поверхность файлов зеркала Попытка), без которых Behavior Contract / spec могут не доехать до runtime агентов.

## Gaps for design.md

1. **Матрица срезов vs Behavior Contract / spec:** в таблице Scenario × Slice строки «Reviewer Phase 2.6 completeness» и «Contradiction Why = MUST_FIX» помечены `(optional)` на S3, тогда как Behavior Contract, Primary acceptance S3 и spec Requirements «Reviewer audits…» / «Contradiction… blocking» требуют обязательности. Исправить матрицу: оба сценария — Primary (или явная зависимость «S3 не accepted без обоих»), убрать optional.
2. **Поверхность реестра AP:** proposal/Impact называют `.cursor/rules/bsl-antipatterns.mdc`; полные карточки живут в `.cursor/docs/antipatterns/bsl-antipatterns.md`, а mdc — индекс + Writer bulletin. В S1/Impact явно: карточка AP-055 в docs **и** однострочник в Writer bulletin mdc (иначе writer/reviewer читают разные слои).
3. **Каноническое место шаблона Hardcode Justification:** сейчас шаблон только в `design.md` этой ЗНИ; S1 говорит «в docs/rules» без пути. Зафиксировать SSOT-путь (например фрагмент в `architect-gate` / `existing-mechanism-priority` / docs template) — куда копировать в design прикладных ЗНИ.
4. **Проводка зеркала Phase 2.5:** текущий kit ссылается на Phase 2.5 из `onec-code-reviewer.md`, `reviewer-checks.md` и `review/SKILL.md` (trivial-skip / appendix). Impact не включает `review/SKILL.md` (и при необходимости `1c-agent-patterns` для списка gates G14/G19 → +G21). Добавить в S3/Impact: Phase 2.6 упоминается везде, где сейчас обязателен/скипается 2.5, иначе «выделенный проход» останется только в agent body.
5. **Детекторы AP-055 (implementation_invariant):** Behavior Contract перечисляет `ИмяФормы = "…"`, `ОткрытьФорму("…")`, allow-list метаданных; в design Decisions/Slices нет минимального чеклиста детекторов для карточки AP и Phase 2.6 шаг A (что считать литералом-фильтром vs Evidence protocol). Добавить короткий bullet-список в design или в задачу S1/S3 — без смены оси.

## Architectural alternatives

Нет равноправной развилки по коду/поведению kit: Option A остаётся Chosen. Альтернативы D/E/F/H рассмотрены в Q2 и отклонены с обоснованием; reopen closed decisions не применим (ledger пуст).

## Источники

- proposal.md — `## Why`, `## What Changes`, `## Impact`, `## Scope` / Out of scope
- design.md — `## Goals / Non-Goals`, `## Decisions`, `## Implementation Options` A–C, `## Behavior Contract`, `## Slices` + матрица, `## Open Questions`
- specs/hardcode-justification-gate/spec.md — ADDED Requirements: registry AP, Architect Gate, Writer halt, Reviewer completeness + contradiction, Scope-as-literals
- Код/kit (verified, не architecture-reports) — Phase 2.5 в `.cursor/agents/onec-code-reviewer.md` / `.cursor/docs/standard/reviewer-checks.md` / `.cursor/skills/review/SKILL.md`; индекс vs карточки `bsl-antipatterns.mdc` → `.cursor/docs/antipatterns/bsl-antipatterns.md`; последний AP в docs — AP-054
