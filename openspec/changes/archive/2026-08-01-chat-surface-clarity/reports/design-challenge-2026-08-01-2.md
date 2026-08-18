---
report_type: design-challenge
generated_at: 2026-08-01
agent: onec-code-architect
mode: design-challenge
scope:
  change: chat-surface-clarity
  design_mtime: "2026-08-01T05:51:25Z"
verdict: APPROVE
confidence: high
---

# Design Challenge — chat-surface-clarity

## KB references

- Discovery выполнен, совпадений нет — not relevant: KB-фактов для опоры нет; выводы только из proposal / design / specs / kit-файлов.

## Адверсариальная установка

Независимый проход после Repair Loop (attempt 1): перечитаны `proposal.md`, обновлённый `design.md`, `specs/chat-surface-clarity/spec.md`; точечно сверены текущие утечки в kit (`forms-mxl-mode-gate.mdc` § «Формулировка вопроса (чат)», `decision-block.md`, `chat-lexicon.md`, `opsx-output-style.md` §2 / §7.7). Прошлые `reports/architecture-*.md` и `design-challenge-2026-08-01.md` **не** использованы как источник истины. Closed decisions: ledger пуст.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** оркестратор копирует в чат каноны и AskQuestion-шаблоны с жаргоном kit (`skill`, гейты, Schema, имена агентов) и процессными преамбулами; правка одного Mode Gate не закрывает утечки в new/apply/verify/status/review.
- **Design адресует:**
  - Why → жаргон в канонах → Decision 1–2 + S1 (секция «Формулировка вопроса (чат)» + зеркала decision-block / lexicon / faq / quick-start / handoff).
  - Why → AskQuestion / copy-paste команд → Decision 1 (dual-language skills) + S2 (new/apply/status/review/verify templates).
  - Why → SSOT-конфликты (агенты, KB в брифе) → Decision 4–5 + S3.1 (opsx ↔ brief-card / lexicon).
  - Why → системность / приёмка → Behavior Contract + явный «Список grep-приёмки» + кумулятивный grep S3.4; Option B отвергнут как недостаточный.
  - Why → non-events перед вопросом режима → Behavior Contract + spec «Mode question has no process preamble» + S1.5.
- **Покрытие:** полное. После repair закрыты разрывы приёмки: токены/зоны grep, граница Mode Gate chat vs agent, Scenario «Apply pause label is product language» ↔ матрица S2, кумулятивный grep без переоткрытия оси, Context без внешней карты как SoT (срезы S1→S2→S3 в самом design).

### Q2 — Optimality

- **Выбранный путь:** Option A — четыре волны правок chat-facing текстов (S1 канон → S2 copy-paste команд → S3 SSOT + grep-приёмка) без нового параллельного гайда и без переписывания agent-facing слоёв verify / XML·BSL guards.
- **Альтернативы (включая не упомянутые в design):**
  1. **Option B (в design, отклонён)** — только Mode Gate. Плюс: минимальный diff. Минус: Why явно требует new/apply/verify/status/review; текущий kit подтверждает утечки вне Mode Gate (`decision-block` эталон «через skill», `opsx` §2 допускает slug агентов, §7.7 требует KB в брифе). Не закрывает Why.
  2. **Option C (в design, отклонён)** — новый параллельный гайд стиля. Плюс: чистая поверхность. Минус: четвёртый SSOT рядом с budget / opsx / lexicon; оркестратор продолжит копировать старые каноны «как есть».
  3. **Runtime-HALT only** (не в Implementation Options) — усилить только `chat-output-budget` / self-check без переписывания эталонов. Плюс: мало файлов. Минус: Why про copy-paste канонов; kit уже имеет Тест понятности (`opsx-output-style` § «Тест понятности»), а эталоны «хорошо» всё ещё учат jargon — HALT не заменяет источник копирования.
  4. **CI/lint-скрипт grep как единственная мера** (не в Options) — автоматизировать запрет токенов без волн правок. Плюс: повторяемость. Минус: не даёт русские каноны 1/2/3 и AskQuestion; ломает agent-facing таблицы `form_mode`/skill без границы Decision 1. Может дополнять S3.4, не заменяет Option A.
  5. **Единый chat-surface.md + thin redirects** (не в Options) — вынести все user-facing формулировки в один файл. Плюс: одна точка правки. Минус: близко к Option C (новый SSOT); skills всё равно держат AskQuestion inline — двойная синхронизация.
- **Вердикт по Q2:** оптимален. Минимальная инвазивность при полном покрытии Why: править то, что оркестратор обязан копировать; agent-only оставить; приёмка — явный grep-список.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** да
- **Причины:**
  - Граница chat-facing / agent-facing операциональна: для Mode Gate названа конкретная секция kit («Формулировка вопроса (чат)»); agent-таблицы skill явно исключены из grep — совпадает со структурой текущего `forms-mxl-mode-gate.mdc`.
  - Behavior Contract ↔ spec ↔ slices согласованы, включая Apply pause label и кумулятивную приёмку S3 без архитектурной вилки.
  - Ось Decisions 1–5 / Option A достаточна для apply; оставшиеся уточнения (какие именно § opsx считать user-facing при grep) — уровень tasks/S3.4, не смена решения.

## Verdict

**APPROVE** — design после repair решает Why из proposal полным Option A, оптимален относительно отвергнутых и трёх незаявленных альтернатив, и с первого взгляда готов к реализации без обязательных gaps в постановке.

## Gaps for design.md

(нет — вердикт APPROVE)

## Architectural alternatives

(нет равноправной развилки по наблюдаемому поведению: закрытая ось Option A / Decisions 1–5 удерживается; CI-grep и единый chat-surface.md — дополнения/хуже, не конкуренты по коду kit.)

### Проверка gaps прошлого challenge (по артефактам, не по старому отчёту)

| Заявленный gap | Статус в текущих артефактах |
|----------------|----------------------------|
| Список grep (токены + зоны + исключения) | Закрыт — design § «Список grep-приёмки (chat-facing)» |
| Граница chat-facing Mode Gate | Закрыта — Decision 1 + имя секции |
| Behavior ↔ spec (pause label) | Закрыт — spec Scenario «Apply pause label…» + матрица / S2 |
| S3 cumulative grep | Закрыт — Behavior Contract + S3.4 / S3.accept |
| Внешний план как SoT | Закрыт — Context: внешние черновики не SoT; карта = срезы в design |

Мелкая формулировка Option A («по карте аудита») не создаёт второй SoT при наличии таблицы Slices в том же файле — не поднимается до gap.

## Источники

- proposal.md — `## Why`, `## What Changes`, `## Scope` / Impact
- design.md — Decisions 1–5, Implementation Options A–C, Behavior Contract, Список grep-приёмки, Slices / матрица, Context
- specs/chat-surface-clarity/spec.md — все ADDED Requirements / Scenarios, в т.ч. Apply pause label
- kit (verified current leaks) — `.cursor/rules/forms-mxl-mode-gate.mdc` (§ «Формулировка вопроса (чат)» с skill compile/edit); `.cursor/docs/templates/decision-block.md` (эталон «через skill»); `.cursor/docs/chat-lexicon.md` (замена `assisted`); `.cursor/docs/opsx-output-style.md` (§2 slug агентов; §7.7 KB в брифе; § Тест понятности)
