---
report_type: design-challenge
generated_at: 2026-08-09
agent: onec-code-architect
mode: design-challenge
scope:
  change: explain-after-review-apply-scope
  design_mtime: "2026-08-09T14:41:04.2520822+09:00"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — explain-after-review-apply-scope

## Адверсариальная установка

Повторный независимый challenge после repair-from-verify. Прочитаны только `proposal.md`, `design.md`, `specs/explain-post-implementation-scope/spec.md`, `tasks.md` и актуальный эталон kit `openspec-explain/templates/entry-brief.md` (для факта текущего HALT). Предыдущий `reports/design-challenge-2026-08-09.md` использован **только** как чеклист gaps D1/D2/D2a/D4/D5 — не как доказательство оптимальности. `reports/architecture-*.md` не использовались. Closed decisions: пусто.

## Проверка закрытия gaps предыдущего challenge

| Gap (challenge-1) | Статус после repair | Доказательство |
|---|---|---|
| D2a: propose vs «одна команда» / MUST_FIX | **закрыт** | design `### D2a`; tasks S1.3; spec Scenario «Review offers explain» — «нет нерешённого MUST_FIX ask» |
| D1: SSOT apply = code-map; handoff = копия/ссылка | **закрыт** | design D1 канон; spec Scenario «Apply artifacts…»; tasks S1.2 |
| D4: Охват UX / path только в Контекст | **закрыт в design** | design `### D4`; proposal «пути — в Контекст»; tasks Primary acceptance |
| D5: MVP only new format; OQ1–OQ2 | **закрыт** | design D5 + «Открытые вопросы» 1–2 зачёркнуты |
| D2: без MUST-порога 12 | **закрыт** | design D2: «≤12 файлов — только guidance… не MUST» |

Остаётся **новый** verified конфликт design↔spec по формулировке Requirement HALT (ниже) — ось решения не меняется.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** после `/review`, `/release-review` и `/opsx:apply` нет перехода в `/opsx:explain` с уже известным списком обработанного кода; бриф explain приходится заполнять вручную, хотя охват уже лежит в отчёте ревью или `code-map`; нужны handoff и автозаполнение Охвата в entry-брифе для подтверждения.
- **Design адресует:**
  - Why «нет перехода» → D2/D2a propose с приоритетом ниже MUST_FIX/extend.
  - Why «охват уже есть, но не в брифе» → D1 секция `## Explain scope` + D3 prefill.
  - Why «подтверждение рамки» → D3/D4 + spec «No mass Read before confirm».
  - Конфликт текущего HALT «Список модулей… не в бриф» (`entry-brief.md`) → D4 точечная правка (UX в Охват, path в Контекст).
- **Покрытие:** полное по Why. Gaps предыдущего challenge по propose/канону apply/MVP/порогу 12 закрыты. Частичный риск исполнения: нормативный текст Requirement «Brief HALT…» всё ещё допускает пути **в слоте Охват**, что расходится с D4/proposal/Scenario — см. Gaps.

### Q2 — Optimality

- **Выбранный путь:** handoff-секция внутри существующих артефактов + propose ниже блокеров + prefill B-explain (Охват XOR Варианты, path в Контекст) без отдельного файла и без автопрогона карты.
- **Альтернативы (включая не упомянутые в design):**
  1. **Парсинг code-map / «Что отрецензировано» без секции** — explain извлекает path из текущего формата code-map и review. Плюсы: меньше писателей. Минусы: нет единого machine-readable контракта для review; хрупкая эвристика; Why просит явный handoff. Хуже D1/D5.
  2. **Shortcut как explore (без второго брифа)** — сразу карта по `@review`/`@code-map`. Плюсы: меньше трения. Минусы: рамка huge release/широкого review неочевидна; Why и Non-Goal требуют подтверждения брифа. Хуже для post-review/apply.
  3. **Липкий scope только в чате** — без записи в отчёт. Плюсы: zero-churn формата. Минусы: ломает explain в новом чате; нет audit trail. Хуже.
  4. **Отдельный `temp/explain-handoff-*.md`** — уже Non-Goal; orphan и рассинхрон с отчётом-источником. Хуже.
- **Вердикт по Q2:** ось оптимальна; лучшей альтернативы по поведению kit нет. Оставшийся gap — согласование нормативного текста spec с уже выбранной осью D4, не развилка.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговоркой
- **Причины:**
  - Да: боль подтверждается текущим kit HALT («Список модулей… не в бриф») и отсутствием propose explain в финалах review/apply.
  - Да: после repair решения D1/D2a/D5/порог 12 достаточно конкретны для mechanical apply (tasks S1.2–S1.4 согласованы).
  - Оговорка: до apply нужна одна правка текста Requirement «Brief HALT…», иначе writer S1.7 может положить path-list в Охват вопреки D4 и proposal.

## Verdict

**CHALLENGE** — предыдущие implementation_invariant gaps закрыты, ось handoff+prefill оптимальна, но остаётся одно расхождение нормативного текста spec HALT с D4/proposal/Scenario; смена архитектуры не требуется.

## Gaps for design.md

1. **Spec Requirement «Brief HALT allows compact post-implementation scope» vs D4.** Сейчас MUST: «разрешать компактные пути и имена процедур … **в слотах Охват и Контекст**». D4, proposal («пути — в Контекст») и Scenario «Compact paths allowed» требуют: Охват = только UX-абзац; полный маркированный список `path` (+ опц. процедуры) — **только** в Контекст. Исправить формулировку Requirement (и при необходимости связать с эталоном C / S1.7), чтобы не разрешать inventory path в слоте Охват.

## Architectural alternatives

Равноправной развилки по коду/поведению kit **нет**. Ось (секция внутри отчёта + prefill + confirm до карты) остаётся Chosen; gap выше — `implementation_invariant`.

## Источники

- proposal.md — `## Why`, `## What Changes` (пути в Контекст), `## Scope`
- design.md — D1 (канон apply), D2/D2a, D3, D4, D5; открытые вопросы 1–2 закрыты; Slices/Primary acceptance
- specs/explain-post-implementation-scope/spec.md — Explain scope section; Propose; Prefill; **Brief HALT** (конфликт строки Requirement); Compact paths Scenario; Explore intact
- tasks.md — S1.2–S1.4, S1.7, Primary acceptance
- Kit (verified): `.cursor/skills/openspec-explain/templates/entry-brief.md` — HALT «Список модулей (`pav…`, M01…)» в бриф
