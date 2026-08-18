---
report_type: design-challenge
generated_at: 2026-08-01
agent: onec-code-architect
mode: design-challenge
scope:
  change: sequential-ui-mode-questions
  design_mtime: "2026-07-31T22:37:40Z"
verdict: CHALLENGE
confidence: medium
---

# Design Challenge — sequential-ui-mode-questions

## Адверсариальная установка

Повторный независимый challenge после internal repair: прочитаны только `proposal.md`, `design.md`, `specs/**/spec.md`, `tasks.md` и текущие якоря `.cursor/rules/forms-mxl-mode-gate.mdc` / `openspec-new-change` / `openspec-apply-change` (как evidence «как сейчас»). Отчёты `reports/architecture-*.md` и прошлый `design-challenge-*.md` **не** использовались как источник истины. Closed decisions: пусто.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** в одном ходе два выбора (маркер автора + способ поставки формы/макета); форма и макет склеены в один `artifact_mode` — заказчик не понимает ответ и не может задать разные режимы (макет вручную / форма программно).
- **Design адресует:**
  - Why «два выбора в одном сообщении» → Decisions 3–4 + Behavior Contract: один selection-вопрос за ход, END TURN, Mode Gate не в одном сообщении с Metadata и не с Design Gate AskQuestion.
  - Why «склейка artifact_mode» → Decisions 1–2, 6–7 + Option B: `form_mode` / `layout_mode`, два SSOT-текста вопросов, запись пары без `artifact_mode`, apply/verify читают пару с fallback.
  - What Changes «вопросы когда ясно, что трогаем» → Decision 3: Mode Gate на этапе design, только при UI-scope; Decision 8: поздний UI-scope в extend дозапрашивает недостающий канал.
  - Риск молчаливого default / копирования соседнего канала → Decision 2/8 + Behavior Contract + spec scenario Empty mode.
- **Покрытие:** полное по боли Why; **частичный зазор контракта** — Behavior Contract трактует `n/a` при задаче на UI-артефакт как блокер apply/verify, а spec `Empty mode blocks…` формулирует только «пусто» (без валидного legacy). Семантика `n/a`+UI-in-scope закрыта в design Decisions 2/8 как Mode/extend, но не зафиксирована симметрично в delta spec → риск расхождения readers apply/verify при реализации.

### Q2 — Optimality

- **Выбранный путь:** раздельные машиночитаемые `form_mode`/`layout_mode` + строго последовательные selection-вопросы; Mode Gate на design (и при позднем UI-scope); legacy lone `artifact_mode` → оба канала одинаково; новые proposal не пишут `artifact_mode`.
- **Альтернативы (включая не упомянутые в design `## Implementation Options`):**
  1. **Sparse override (общий `artifact_mode` + override только при расхождении)** — писать `artifact_mode` как default обоих каналов; `form_mode`/`layout_mode` только если отличаются. Плюс: меньше полей в типичном proposal, мягче миграция текстов. Минус: два источника истины, сложнее resume/verify («какое поле главное»), легко снова склеить UX-вопрос. Отклонена относительно B: Why требует явного независимого выбора каналов; B проще для apply-таблицы Form vs Template.
  2. **SSOT через маркеры задач (`[mxl:…]` + обязательный `[form:…]`), Mode Gate только при отсутствии маркеров** — режимы живут в `tasks.md`, proposal вторичен. Плюс: симметрия с уже существующим `[mxl:…]` в apply. Минус: design сознательно оставил `[form:…]` Follow-up (Decision 5); без него канал формы остаётся дырой; маркеры не закрывают dual AskQuestion на входе. Не превосходит B для Primary.
  3. **Lazy Mode Gate на первом Form/Template-шаге apply** — не спрашивать в new/design, спросить в apply. Плюс: shorter `/opsx:new`. Минус: прямо бьёт Non-Goal/Goals «собрать до apply» и Frontload 1.56; режимы появляются поздно, verify pre-apply слеп. Хуже по обратимости и Blast Radius протокола.
- **Вердикт по Q2:** выбранный путь оптимален среди жизнеспособных; альтернативы либо усложняют dual-SSOT, либо переносят боль в apply, либо зависят от Follow-up-маркеров вне Primary.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками
- **Причины:**
  - Да: прямо бьёт оба симптома Why; опирается на уже разделённый apply Form vs Template; минимальный набор режимов без новых enum.
  - Да: последовательность + запрет смешения с Design Gate selection снимает главный UX-антипаттерн батчинга AskQuestion (подтверждается текущим SKILL: Mode Gate 1.55 и Design Gate AskQuestion «Принять» — разные точки, сейчас без жёсткого END TURN/HALT ≥2).
  - Оговорка: до apply нужна доводка контракта readers на кейсах `n/a`+UI-in-scope и конфликт «пара полей + legacy `artifact_mode`» — иначе implementer может разъехаться между design Behavior Contract и spec Empty.

## Verdict

**CHALLENGE** — решение Why и выбор Option B оптимальны и имплементируемы после repair, но остаются два implementation_invariant зазора в контракте spec/readers; архитектурная развилка не требуется.

## Gaps for design.md

1. **Spec ↔ Behavior Contract: `n/a` при UI-in-scope.** В `specs/split-form-layout-modes/spec.md` scenario Empty сейчас только «пусто». Добавить явное наблюдаемое поведение: если артефакт в scope, а соответствующий режим `n/a` (и нет валидного lone legacy `artifact_mode`) — STOP/extend / Mode-вопрос, эквивалентно пустому (как design Decision 8 + Behavior Contract). Либо сузить Behavior Contract: блокер apply только для пустого, а `n/a`+UI всегда чинится Mode Gate до записи acceptance — но тогда это MUST быть одной фразой в design и tasks S2.3/S2.4.
2. **Precedence при сосуществовании пары и legacy.** Design говорит: readers «сначала пара, затем fallback lone `artifact_mode`»; не специфицирован конфликт (есть и пара, и `artifact_mode` с другим значением). Зафиксировать implementation invariant: при наличии любого из `form_mode`/`layout_mode` — legacy игнорировать (или HALT при противоречии). Предпочтительно: **пара побеждает, legacy только если обоих новых полей нет** — без архитектурной вилки, одной строкой в design Decisions 7 + verify Legacy scenario / apply tasks.

## Architectural alternatives

(нет — равноправных путей по наблюдаемому поведению Primary нет; residual gaps закрываются уточнением контракта без смены оси `form_mode`/`layout_mode` + sequential gates.)

## Источники

- proposal.md — `## Why`, `## What Changes`, capabilities `sequential-gate-questions` / `split-form-layout-modes`
- design.md — Decisions 1–8, Behavior Contract, Implementation Options A–C, Slices S1–S2
- specs/sequential-gate-questions/spec.md — One selection question per turn; Metadata / Second gate / Dual blocked
- specs/split-form-layout-modes/spec.md — Separate modes; Form-only; Layout-only; Mixed; Legacy; Kit evolution; Empty mode
- tasks.md — S1.1–S1.3, S2.1–S2.5 (стык Design Gate, extend, empty, запись без `artifact_mode`)
- Код/протокол (verified current state) — `.cursor/rules/forms-mxl-mode-gate.mdc` (`artifact_mode` SSOT); `.cursor/skills/openspec-new-change/SKILL.md` шаги 1.55–1.56, запись proposal; `.cursor/skills/openspec-apply-change/SKILL.md` сверка `[mxl:…]` с `artifact_mode`
