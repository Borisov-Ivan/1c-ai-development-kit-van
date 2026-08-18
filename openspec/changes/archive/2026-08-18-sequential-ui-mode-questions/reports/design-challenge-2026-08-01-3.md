---
report_type: design-challenge
generated_at: 2026-08-01
agent: onec-code-architect
mode: design-challenge
scope:
  change: sequential-ui-mode-questions
  design_mtime: "2026-08-01T08:17:46.3842831+09:00"
verdict: APPROVE
confidence: high
---

# Design Challenge — sequential-ui-mode-questions

## KB references

- Discovery выполнен, совпадений нет — not relevant: KB-фактов для опоры/конфликта нет; challenge опирается на proposal/design/specs и текущий код `.cursor/**`.

## Адверсариальная установка

Независимый post-repair прогон: прочитаны только `proposal.md`, `design.md`, оба `specs/**/spec.md`; для verified code facts — актуальные `forms-mxl-mode-gate.mdc`, фрагменты `openspec-new-change` / `openspec-apply-change`. Собственные прошлые `reports/architecture-*` и `design-challenge-*` как источник истины не использовались. Позиция: отвергнуть design, если Why не закрыт, путь неоптимален или артефакты после repair снова дырявые.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** (1) в одном сообщении два выбора (маркер автора и способ поставки формы); (2) единый `artifact_mode` не даёт разные режимы **разным формам** одной ЗНИ → заказчик не понимает, как отвечать, и не может выбрать «одна форма вручную, другая программно».
- **Design адресует:**
  - Why (1) → Decision 3/4 + Behavior Contract: один вопрос выбора за ход, END TURN, Metadata и Mode не в одном сообщении; Mode не с Design Gate selection (`sequential-gate-questions` scenarios Metadata / Dual / Second gate).
  - Why (2) → Decision 2/3/3a + Option D: per-form `form_mode` / map `forms:` с каноническим ключом метаданных; на design — один вопрос на форму; разные режимы допустимы (`split-form-layout-modes` scenarios Form Mode / Multiple forms).
  - Сужение макетов вне Mode Gate (Decision 6/9, closed `forms_only_no_layout_mode_gate`) **не** входит в Why как боль; Why про склейку выбора и per-form — не про Template Mode Gate.
- **Покрытие:** полное — оба пункта Why закрыты наблюдаемым контрактом; Non-Goals/closed decisions не вырезают проблему Why.

### Q2 — Optimality

- **Выбранный путь:** per-form `form_mode` на design (последовательные вопросы + END TURN) + макеты = apply-политика (manual default / явное разрешение), без поля `layout_mode` как выбора.
- **Альтернативы (включая не упомянутые в design `## Implementation Options`):**
  1. **Default-then-override** — один вопрос «режим по умолчанию для всех форм в scope», затем опционально «у каких форм другой режим». Плюс: меньше ходов при гомогенном N. Минус: два типа вопросов, риск молчаливого наследования на позднюю форму (прямо запрещён Decision 8). Хуже инварианта «одна форма → один явный ответ». Отклонена относительно D.
  2. **Task-marker-first** — SSOT режимов через обязательные `[form:…]` в tasks; AskQuestion только при отсутствии маркера. Плюс: режимы рядом с задачами apply. Минус: proposal Why требует понятный выбор на этапе постановки; design явно выносит `[form:…]` в Follow-up/Non-Goals. Не закрывает UX «как отвечать на гейте» без дублирования канала. Отклонена.
  3. **Mode Gate на шаге 1.55 (до design), но sequential per-form** — сохранить текущую точку skill (`openspec-new-change` 1.55), лишь разбить на N вопросов. Плюс: меньше переноса протокола. Минус: verified — сейчас вопрос ещё до стабилизации form-scope; Decision 3a требует enumeration после scaffold/What Changes. При нестабильном списке — ложные/повторные вопросы. Хуже D по timing. Не reopen closed `per_form_mode_on_design` без доказанного контракта, что scope форм всегда известен до design (в текущем skill такого контракта нет).
  4. **Вернуть dual-channel `layout_mode` + Mode Gate макета** (Option B из таблицы) — `reopen-blocked: forms_only_no_layout_mode_gate` / `acceptance_loop_s2_path`. Why этого не требует; увеличивает Blast Radius UX без выигрыша по Why.
- **Вердикт по Q2:** оптимален — D минимален по ветвлениям при полном закрытии Why и closed axis; альтернативы либо слабее по инварианту наследования/enumeration, либо blocked closed decisions.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** да
- **Причины:**
  - Why ↔ Behavior Contract ↔ specs трассируются без «похожего, но другого» решения (sequential + per-form, не dual layout).
  - Post-repair закрывает прежние дыры канона: `## Forms mode`, map/ключ метаданных, Decision 3a enumeration, legacy×N гомогенный fallback, permission-on-apply + `debug.md` § Apply permissions, timing Mode на design до приёмки.
  - Текущий код (склейка «форму/макет», единый `artifact_mode`, Mode на 1.55) подтверждает, что design чинит реальный протокол kit, а не выдуманную модель.

## Verdict

**APPROVE** — после repair design решает оба пункта Why оптимальным per-form sequential путём при осознанном сужении макетов вне Mode Gate; существенных gaps для apply нет.

## Architectural alternatives

Нет равноправной развилки по коду/поведению, требующей выбора пользователя: closed axis держится; отличия Default-then-override / 1.55-timing — implementation-prefer D, не fork.

## Источники

- proposal.md — `## Why` (два выбора; нет per-form); `## What Changes` (sequential; form_mode per-form; макеты вне Mode Gate; legacy fallback).
- design.md — Goals/Non-Goals; Decisions 1–9; Behavior Contract; Implementation Options A/B/C/D; Slices S1/S2; «Решения verify».
- specs/ — `sequential-gate-questions/spec.md` (один вопрос / dual blocked / second after answer); `split-form-layout-modes/spec.md` (per-form, no layout Mode, legacy×N, empty blocks, layout permission).
- Код (verified baseline, до apply этой ЗНИ) — `.cursor/rules/forms-mxl-mode-gate.mdc` (вопрос «форму/макет», секция `## Forms & layouts mode`, `artifact_mode`); `.cursor/skills/openspec-new-change/SKILL.md` шаг 1.55; `.cursor/skills/openspec-apply-change/SKILL.md` (Template ↔ `artifact_mode` / `[mxl:…]`).
