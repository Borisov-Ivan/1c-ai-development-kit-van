---
report_type: design-challenge
generated_at: 2026-08-09
agent: onec-code-architect
mode: design-challenge
scope:
  change: explain-after-review-apply-scope
  design_mtime: "2026-08-09T05:46:49Z"
verdict: APPROVE
confidence: high
---

# Design Challenge — explain-after-review-apply-scope

## Адверсариальная установка

Независимый финальный challenge после repair-2: прочитаны только `proposal.md`, `design.md`, `specs/explain-post-implementation-scope/spec.md`. Предыдущие `reports/architecture-*.md` / `design-challenge-*.md` не использовались как источник истины. Цель атаки — проверить закрытие gap «path в Охват» и optimality оси handoff → B-explain.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** после review / release-review / apply нет перехода в `/opsx:explain` с уже известным списком обработанного кода; бриф заполняют вручную, хотя охват уже в отчёте или `code-map`.
- **Design адресует:** секция `## Explain scope` в существующих артефактах (D1); propose из финалов с приоритетом ниже fix/extend (D2/D2a); prefill B-explain с UX-Охватом и путями в Контекст (D3); уточнённый HALT без сырого inventory как замены Сценарию (D4); MVP без эвристики старых отчётов (D5).
- **Покрытие:** полное — Why (handoff + автозаполнение рамки на подтверждение) закрыт Goals 1–3 и requirements Propose / Prefill / Brief HALT / Explore intact. Non-goals (отдельный handoff-файл, автостарт без «да», disposition) не размывают Why.

**Repair-2 gap (path в Охват):** закрыт.

| Артефакт | Норма после repair-2 | Согласованность |
|----------|----------------------|-----------------|
| design D4 | Охват = только UX-абзац без полного списка path; path (+ процедуры) только в Контекст; эталон C без путей в Охвате; явная норма совпадения со spec | OK |
| design D3 | Охват = UX; Контекст = пути отчёта + полный список path | OK с D4 |
| spec Requirement «Brief HALT…» | Охват = только UX-абзац (без полного списка path); path/procedures только в Контекст | OK с D4 |
| spec Scenario Compact paths | UX в Охват + маркированный path в Контекст; «полный список path не размещается в слоте Охват» | OK с D4 |
| proposal What Changes | «пути — в Контекст»; HALT запрещает сырой dump, разрешает компактный охват | OK |

Противоречия «path одновременно в Охват и Контекст» в текущих текстах нет.

### Q2 — Optimality

- **Выбранный путь:** handoff внутри `review-*.md` / `code-map` (+ ссылка/копия в handoff-acceptance) → propose → B-explain (Охват UX XOR Варианты; path в Контекст) → подтверждение → карта.
- **Альтернативы (включая не упомянутые в design):**
  1. **Отдельный `temp/explain-handoff-*.md`** — дублирует охват вне отчёта ревью/apply; больше артефактов и рассинхрон со SSOT. Хуже обратимости и простоты; proposal/design осознанно out of scope.
  2. **Prefill без брифа (как explore shortcut)** — быстрее, но ломает обязательное подтверждение рамки для post-review/apply (Non-Goal / Goal 3). Ухудшает контроль огромного release scope.
  3. **Эвристический парсинг старых отчётов без секции** — шире совместимость, но хрупкий парсер и ложные Охваты; D5 корректно откладывает за пределы MVP.
- **Вердикт по Q2:** оптимален для Why: минимальная инвазивность (секция в существующих отчётах), сохранение бюджета B-explain и приоритета fix/extend, явное разделение UX-рамки и machine path-list.

Равноправной архитектурной развилки по коду/поведению нет: kit-метаизменение без продуктового BSL; ось handoff-in-report vs отдельный файл уже решена в пользу меньшей поверхности.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** да
- **Причины:**
  - Why ↔ design ↔ spec сходятся: propose + `## Explain scope` + prefill с подтверждением до карты.
  - Repair-2 устранил единственный зафиксированный разрыв D4 ↔ Brief HALT (слоты Охват/Контекст).
  - Бюджет ≤6 слотов, XOR Охват/Варианты и приоритет MUST_FIX/extend сохранены — нет скрытого расширения scope.

## Verdict

**APPROVE** — gap «path в Охват» закрыт согласованными D3/D4 и Requirement/Scenario Brief HALT; выбранная ось handoff → prefill → confirm остаётся оптимальной, новых implementation_invariant для design/spec не выявлено.

## Gaps for design.md

(нет)

## Architectural alternatives

(нет равноправной развилки)

## Источники

- proposal.md — `## Why`, `## What Changes` (handoff, Охват, пути в Контекст, HALT)
- design.md — D1–D5; особенно D3 Prefill, D4 HALT модулей (норма совпадения со spec)
- specs/explain-post-implementation-scope/spec.md — Requirement «Brief HALT allows compact post-implementation scope»; Scenario Compact paths; Prefill / Propose / Explore intact
- Код — не требовался (kit meta-change; closed decisions: none)
