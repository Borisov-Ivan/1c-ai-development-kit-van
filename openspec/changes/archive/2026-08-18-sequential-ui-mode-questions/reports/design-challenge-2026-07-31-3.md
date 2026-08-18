---
report_type: design-challenge
generated_at: 2026-07-31
agent: onec-code-architect
mode: design-challenge
scope:
  change: sequential-ui-mode-questions
  design_mtime: "2026-07-31T22:41:55Z"
verdict: APPROVE
confidence: high
---

# Design Challenge — sequential-ui-mode-questions

## Адверсариальная установка

Независимый третий прогон: прочитаны только `proposal.md`, `design.md`, оба delta-spec и `tasks.md`. Прошлые `reports/architecture-*.md` / prior challenge не использовались как источник истины. Цель — отвергнуть решение, если Why не закрыт или есть лучший путь по наблюдаемому поведению.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** в одном ходе два выбора (маркер автора + способ поставки формы/макета); форма и макет склеены в один `artifact_mode` — заказчик не понимает, как отвечать, и не может задать разные режимы (макет вручную / форма программно).
- **Design адресует:**
  - Why «два выбора в одном сообщении» → Decisions 3–4 + Behavior Contract + capability `sequential-gate-questions` (один selection-вопрос, END TURN, HALT dual AskQuestion; Mode Gate на design, не с Metadata).
  - Why «склейка artifact_mode / нельзя разные режимы» → Decisions 1–2, 6–8 + Option B: `form_mode` / `layout_mode`, два SSOT-текста вопросов, вопросы только при scope, mixed → независимый apply; Empty/`n/a`+UI-in-scope — STOP без копирования соседнего канала.
  - Why (совместимость старых proposal) → Decision 7 + scenarios Legacy / Pair override: lone `artifact_mode` только если обоих новых полей нет; при любом новом поле пара побеждает, legacy игнорируется.
- **Покрытие:** полное — оба болевых пункта Why имеют прямое наблюдаемое поведение в design + specs; краевые случаи `n/a`+UI и конфликт пары с legacy зафиксированы в `split-form-layout-modes`.

### Q2 — Optimality

- **Выбранный путь:** раздельные машиночитаемые `form_mode`/`layout_mode` + строго последовательные selection-вопросы на design-stage; legacy lone fallback только при отсутствии обоих новых полей; пустой/`n/a` при UI-in-scope — блокер.
- **Альтернативы (включая не упомянутые в design):**
  1. **Sparse override (общий `artifact_mode` + override только при расхождении)** — писать общий режим и одно поле override. Плюс: короче типичный proposal. Минус: два SSOT-пути чтения, сложнее resume/verify, риск снова склеить UX-вопрос. Хуже B для Why(2) и уже раздельных путей Form vs Template в apply.
  2. **Режимы только маркерами tasks (`[form:…]` / `[mxl:…]`) без полей proposal** — плюс: симметрия с существующим `[mxl:…]`. Минус: Mode Gate/`/opsx:new` теряют SSOT до tasks; verify/apply читают proposal Metadata сегодня — сдвиг якоря. Не закрывает Why про вопросы на входе/design лучше, чем B; `[form:…]` осознанно Follow-up (Decision 5).
  3. **Оба новых поля обязательны для precedence; иначе legacy на «пустой» канал** — при `form_mode` задан, а `layout_mode` нет, читать layout из `artifact_mode`. Плюс: мягче полу-миграция. Минус: split-brain (форма из пары, макет из legacy) и молчаливое наследование — прямо против Behavior Contract «не копировать соседний/legacy канал». Decision 7 («хотя бы один» → пара побеждает) строже и предсказуемее.
- **Вердикт по Q2:** оптимален — B минимален по точкам правки (протоколы + Mode Gate), даёт машиночитаемый split и однозначный reader-контракт; перечисленные альтернативы либо слабее по Why, либо добавляют двусмысленность apply/verify.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** да
- **Причины:**
  - Why ↔ design ↔ specs выровнены: sequential gates, split modes, Empty с `n/a`+UI-in-scope, Pair override, Legacy только при отсутствии обоих новых полей.
  - Поверхность изменений — документы/skills оркестратора, без прикладного BSL/XML; Non-Goals соблюдены.
  - Decisions 7–8 + tasks S2.3/S2.4 дают implementer однозначный алгоритм чтения без архитектурной вилки.

## Verdict

**APPROVE** — постановка закрывает Why целиком; выбранный путь остаётся самым простым жизнеспособным; residual ambiguity по precedence/`n/a` снята Decision 7 и scenarios Pair/Empty.

## Gaps for design.md

(нет — verdict APPROVE)

## Architectural alternatives

(нет — равноправных путей по коду/наблюдаемому поведению Primary нет; рассмотренные альтернативы Q2 уступают по ясности reader-контракта или по покрытию Why.)

## Источники

- proposal.md — `## Why`, `## What Changes`, capabilities `sequential-gate-questions` / `split-form-layout-modes`
- design.md — Goals; Decisions 1–8; Behavior Contract; Implementation Options A–C; матрица приёмки (pair overrides / empty mode blocks)
- specs/sequential-gate-questions/spec.md — One selection question; Metadata without Mode; Dual blocked
- specs/split-form-layout-modes/spec.md — Form-only / Layout-only / Mixed; Legacy; Pair fields override; Empty mode blocks (`n/a`+UI-in-scope); Kit evolution
- tasks.md — S1.1–S1.3; S2.1–S2.5 (pair wins, empty/`n/a` STOP); S2.accept optional Pair/Empty
