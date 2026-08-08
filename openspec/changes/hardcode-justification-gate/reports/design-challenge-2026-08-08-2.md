---
report_type: design-challenge
generated_at: 2026-08-08
agent: onec-code-architect
mode: design-challenge
scope:
  change: hardcode-justification-gate
  design_mtime: "2026-08-08T05:40:06Z"
verdict: APPROVE
confidence: high
---

# Design Challenge — hardcode-justification-gate (повтор после repair)

## Адверсариальная установка

Независимый повторный проход после repair-from-verify: прочитаны `proposal.md`, `design.md`, `specs/hardcode-justification-gate/spec.md`, `tasks.md` (сверка поверхности файлов). Prior `reports/design-challenge-2026-08-08.md` использован **только** как список gaps 1–5 для проверки закрытия, не как источник истины по решению. Отчёты `reports/architecture-*.md` не привлекались. Closed decisions: пусто.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** architect предлагает allow-list имён форм как «тонкий» охват хука; writer вливает литералы; reviewer без выделенного прохода — отклоняет заказчик; в kit нет зеркала каркаса Попытка (реестр + HALT + выделенный проход + completeness) для runtime-фильтра по строкам метаданных/форм.
- **Design адресует:**
  - Why «нет каркаса» → AP-055 + Identity Filter Gate + writer G21 + reviewer Phase 2.6 (completeness) — зеркало G14/G19/Phase 2.5.
  - Why «architect сам рекомендует список» → HALT из трёх вопросов + секция Hardcode Justification до Chosen; SSOT шаблона в `existing-mechanism-priority.mdc`.
  - Why «writer вливает / reviewer не ловит» → G21 + Phase 2.6 с детекторами и MUST_FIX при contradiction «без хардкода».
  - Граница consumer / protocol literals → Non-Goals + spec scenario «Protocol literals are out of class by default» + явные детекторы «не литерал-фильтр».
- **Покрытие:** полное. Расхождение матрицы Primary/optional из первого challenge устранено: Phase 2.6 completeness и Contradiction = Primary на S3.

### Q2 — Optimality

- **Выбранный путь:** полный 4-слойный каркас (AP + architect Gate + writer G21 + reviewer Phase 2.6) одним change, три среза (Option A).
- **Альтернативы (включая не упомянутые в design ## Implementation Options):**
  1. **Option D — Расширить Phase 2.5 / Contract Map вместо Phase 2.6** — identity-literals как ещё одна completeness-таблица внутри Попытка & Contract Audit. Плюсы: меньше фаз. Минусы: смешивает ортогональные классы; Why требует выделенный проход. Отклонена: хуже Fit.
  2. **Option E — Оркестраторский mechanical grep в writer-pipeline (паттерн AP-054) без Phase 2.6** — evidence `ИмяФормы = "` до reviewer. Плюсы: дешёвый сигнал. Минусы: не закрывает зеркало каркаса (Gate + G21 + Phase); open question уже откладывает verify-grep. Отклонена.
  3. **Option F — Только запах Scope-as-literals + существующий G20** — без G21/Phase 2.6. Плюсы: минимум правок. Минусы: повторяет дыру «запись без прохода» (близко к Option C). Отклонена.
  4. **Option H — Жёсткий запрет allow-list без Hardcode Justification** — всегда только callee/API. Плюсы: бинарный вердикт. Минусы: шире Why; ломает легитимный закрытый набор «навсегда». Отклонена как overreach.
- **Вердикт по Q2:** Option A оптимален; неупомянутые альтернативы не превосходят по Fit + Blast Radius + обратимости. Поверхность поставки после repair согласована с Behavior Contract / spec.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** да
- **Причины:**
  - Why ↔ design ↔ spec согласованы; зеркало Попытка минимально достаточное для kit-эволюции без прикладного BSL.
  - Граница protocol/enum и out-of-scope consumer зафиксированы; детекторы и SSOT шаблона снимают двусмысленность поставки.
  - Матрица S3 Primary и явный перечень файлов (mdc+docs AP, `review/SKILL.md`, writer patterns) устраняют оговорку первого challenge о формальном закрытии среза без completeness-прохода.

## Verdict

**APPROVE** — ось Option A держится; gaps 1–5 первого challenge закрыты implementation_invariant правками; свежий взгляд согласовал бы design без обязательных доработок до apply.

## Закрытие gaps prior challenge

| # | Gap (prior) | Статус | Доказательство в текущих артефактах |
|---|-------------|--------|-------------------------------------|
| 1 | Матрица: Phase 2.6 / Contradiction были optional на S3 | **закрыт** | design ## Slices матрица: оба сценария — Primary на S3; Primary acceptance S3 требует completeness и MUST_FIX |
| 2 | Поверхность реестра AP: mdc vs docs-карточка | **закрыт** | design S1 файлы: mdc (индекс + Writer bulletin) + `docs/antipatterns/bsl-antipatterns.md`; proposal Impact; tasks S1.1 / S1.1b |
| 3 | SSOT пути шаблона Hardcode Justification | **закрыт** | design Behavior Contract: SSOT = `existing-mechanism-priority.mdc`; S1.4 — вставка шаблона туда |
| 4 | Проводка Phase 2.5 → 2.6 (`review/SKILL`, writer patterns) | **закрыт** | design S3 + proposal Impact: `review/SKILL.md`, `1c-agent-patterns/writer.md`; tasks S3.2 / S3.6 |
| 5 | Детекторы AP-055 / Phase 2.6 шаг A | **закрыт** | design § «Детекторы identity-filter» + граница «не литерал-фильтр»; ссылки из S1.1b / S3.3 |

## Gaps for design.md

Нет обязательных gaps. Опциональный follow-up (verify grep post-apply) остаётся Open Question / tasks Follow-up — не блокер первой поставки и не меняет ось.

## Architectural alternatives

Нет равноправной развилки по коду/поведению kit: Option A остаётся Chosen. Альтернативы D/E/F/H рассмотрены в Q2 и отклонены; reopen closed decisions не применим (ledger пуст).

## Источники

- proposal.md — `## Why`, `## What Changes`, `## Impact`, `## Scope`
- design.md — Goals/Non-Goals, Decisions, Implementation Options A–C, Behavior Contract (+ шаблон SSOT, детекторы), Slices + матрица Primary, Open Questions
- specs/hardcode-justification-gate/spec.md — ADDED: registry AP, Architect Gate, Writer halt, Reviewer completeness + contradiction, Scope-as-literals
- tasks.md — S1.1/S1.1b/S1.3/S1.4, S2.*, S3.1–S3.6 (сверка поверхности)
- prior challenge (только checklist gaps) — `reports/design-challenge-2026-08-08.md` Gaps 1–5
