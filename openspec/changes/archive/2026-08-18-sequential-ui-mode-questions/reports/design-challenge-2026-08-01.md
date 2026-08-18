---
report_type: design-challenge
generated_at: 2026-08-01
agent: onec-code-architect
mode: design-challenge
scope:
  change: sequential-ui-mode-questions
  design_mtime: "2026-07-31T22:51:49Z"
verdict: CHALLENGE
confidence: medium
---

# Design Challenge — sequential-ui-mode-questions

## KB references

- Discovery выполнен, совпадений нет — not relevant: база знаний пуста по якорям ЗНИ; на вердикт не влияет.

## Адверсариальная установка

Независимый проход: прочитаны только `proposal.md`, `design.md`, оба delta-spec и текущие SSOT kit (`.cursor/rules/forms-mxl-mode-gate.mdc`, фрагменты `openspec-new-change/SKILL.md`, apply/verify/skills на `artifact_mode`). Собственные `reports/architecture-*.md` и прошлые `design-challenge-*.md` как источник истины не использовались. Цель — отвергнуть решение, если Why не закрыт или есть лучший путь по наблюдаемому поведению протоколов.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** (1) в одном сообщении могут оказаться два выбора (маркер автора и способ поставки формы/макета); (2) форма и макет склеены в один `artifact_mode`, нельзя задать разные режимы (например макет вручную, форма программно).
- **Design адресует:**
  - Why → два выбора в одном ходе → Decisions 3–4 + Behavior Contract: END TURN после любого выбора, HALT self-check при ≥2 AskQuestion, Mode Gate не в одном сообщении с Metadata и не с Design Gate selection; capability `sequential-gate-questions`.
  - Why → склейка режимов → Decisions 1–2, 6–9 + `form_mode`/`layout_mode`, запрет `layout_mode: bsl-only`, вопросы по одному и только при scope; capability `split-form-layout-modes`.
  - Why → «когда ясно, что трогаем» → перенос Mode Gate на этап design (не вместе с маркером на входе).
- **Покрытие:** полное по двум болям Why. Оговорка (не дыра Why, а уточнение контракта): текущий Mode Gate уже требует «отдельный вопрос» и «не смешивать с Metadata» (`forms-mxl-mode-gate.mdc`), но формулировка вопроса склеивает «форму/макет», а единый `artifact_mode`/`bsl-only` распространяется на оба канала — design усиливает enforcement (END TURN/HALT) и устраняет склейку данных. Это соответствует симптомам Why, а не подменяет проблему.

### Q2 — Optimality

- **Выбранный путь:** два машиночитаемых поля `form_mode`/`layout_mode` + по одному вопросу на канал на этапе design + sequential END TURN + legacy fallback с асимметрией `bsl-only` (Decision 7).
- **Альтернативы (включая не упомянутые в design `## Implementation Options`):**
  1. **Матрица одного выбора (compound AskQuestion)** — один вопрос с вариантами вроде «оба вручную / форма программно + макет вручную / …». Плюс: один ход вместо двух при Form+Template; сохраняет mixed modes. Минус: комбинаторный взрыв вариантов, хуже читается заказчиком, сложно расширять; не снимает нужду в раздельных полях в proposal. Отклонена: хуже UX ясности при том же контракте хранения.
  2. **Mode Gate остаётся на шаге 1.55, только END TURN + split-полей** — без переноса на design. Плюс: меньше сдвиг протокола new, быстрее закрыть «два вопроса в одном сообщении». Минус: Why явно хочет вопрос, когда scope UI уже ясен; на 1.55 scope часто ещё черновой → ложные/ранние вопросы. Отклонена относительно Why «на design».
  3. **SSOT только маркеры задач `[form:…]`/`[mxl:…]` без пары полей в proposal** — apply уже сверяет `[mxl:…]` с режимом. Плюс: меньше schema proposal. Минус: Why/What Changes требуют режимы в proposal для apply/verify до/вне текста tasks; resume и empty-mode blockers без proposal-полей слабее. Отклонена: не закрывает контракт proposal.
  4. **(из таблицы design, для полноты атаки)** Option A — один `artifact_mode` + текстовое уточнение в design: нет машиночитаемого split → не закрывает Why #2. Option C — всегда два вопроса без UI: шум, противоречит kit `n/a`.
- **Вердикт по Q2:** выбранный путь оптимален для пары «ясный UX + машиночитаемый split + совместимость legacy». Не названная альтернатива «матрица одного выбора» выигрывает число ходов при обоих артефактах, но проигрывает ясности и сопровождаемости — не превосходит B в целом.

**Существенное сомнение (не смена оси, implementation_invariant):** в текущем `forms-mxl-mode-gate.mdc` режим `bsl-only` для Template означает «не менять Template.xml; код заполнения без compile». Design/spec запрещают `layout_mode: bsl-only` и silent coerce, но **не фиксируют**, куда девается легитимный сценарий «только код заполнения макета, Template.xml вне правок»: через `layout_mode: n/a` (Template не в scope), через `manual`+инструкцию «не трогать XML», или иной правило apply. Без этой строки writer/apply могут разъехаться с сегодняшним смыслом `bsl-only` для макета.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками
- **Причины:**
  - Да: Why и Behavior Contract совпадают; split полей стыкуется с тем, что apply уже ветвит Form vs Template; legacy Decision 7 (`bsl-only` не копировать в layout) защищает от молчаливой порчи макета.
  - Да: перенос Mode Gate на design и запрет смешивания с приёмкой design — здравый ответ на «когда ясно, что трогаем» и на риск Frontload 1.56 = два AskQuestion в одном ходе.
  - Оговорка: до apply нужна явная строка про наследника Template-`bsl-only` (см. Gaps); иначе свежий ревьюер kit сочтёт регресс канала «программное заполнение без Template.xml».

## Verdict

**CHALLENGE** — решение закрывает Why и в целом оптимально, но перед apply в design/spec не дожат implementation_invariant для бывшего layout/`Template` пути `bsl-only` (код заполнения без правки Template.xml).

## Gaps for design.md

- В `design.md` (Decision 9 или Behavior Contract) явно описать наследника сценария «макет: только код заполнения, Template.xml не трогаем» без значения `layout_mode: bsl-only` (например: Template не в scope → `layout_mode: n/a`; при Template in scope допустимы только `manual`/`assisted`; «программно» на вопросе макета → STOP/переспрос — и как apply отличает fill-only BSL-задачи от XML-задач).
- В Primary acceptance S1 уточнить формулировку так, чтобы не читалась как «Mode сразу следующим сообщением после Metadata до design»: следующий *вопрос режима* — отдельным сообщением и не раньше design-stage (после scaffold), согласованно с Decision 3.
- В Impact/readers (или Decision 7): одна короткая каноническая таблица «чтение proposal» для apply/verify/skills (`pair wins` / lone legacy / half-pair + empty channel), чтобы синхронизация `1c-forms`/`1c-mxl`/`1c-xml-write-guard` не разъехалась на half-pair.

## Architectural alternatives

Равноправной развилки по оси «split fields + sequential» нет: compound-матрица и «Mode на 1.55 only» — trade-off UX/timing, не лучший закрывающий Why. Ось `layout_mode` без `bsl-only` зафиксирована в proposal What Changes; reopen не требуется (`closed_decisions: []`). Уточнение наследника Template-`bsl-only` — gap уровня implementation_invariant, не смена closed axis.

## Источники

- proposal.md — `## Why`, `## What Changes`, capabilities `sequential-gate-questions` / `split-form-layout-modes`
- design.md — Decisions 1–9, Behavior Contract, Implementation Options A/B/C, Slices S1–S2
- specs/sequential-gate-questions/spec.md — one question per turn; Metadata without Mode; dual blocked
- specs/split-form-layout-modes/spec.md — separate modes; layout rejects bsl-only; legacy mapping; empty mode blocks
- Код/SSOT kit — `.cursor/rules/forms-mxl-mode-gate.mdc` (склейка «форму/макет», единый `artifact_mode`, `bsl-only`→Template fill без XML); `.cursor/skills/openspec-new-change/SKILL.md` §1.55–1.56
