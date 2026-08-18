---
report_type: design-challenge
generated_at: 2026-07-31
agent: onec-code-architect
mode: design-challenge
scope:
  change: sequential-ui-mode-questions
  design_mtime: "2026-07-31T14:19:07Z"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — sequential-ui-mode-questions

## Адверсариальная установка

Независимый аудит постановки метапроекта (протоколы `.cursor/**`, не BSL). Прочитаны только `proposal.md`, `design.md`, оба delta-spec и текущие SSOT (`forms-mxl-mode-gate.mdc`, фрагменты `openspec-new-change/SKILL.md`, apply/verify/skills forms-mxl) как verified code facts. Отчёты `reports/architecture-*.md` и self-review **не** использовались как источник истины.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** (1) в одном сообщении два выбора — маркер автора и способ поставки формы/макета; (2) форма и макет склеены в один `artifact_mode`, нельзя задать разные режимы (пример: макет вручную, форма программно); заказчик не понимает, как ответить.
- **Design адресует:**
  - (1) → инвариант «один вопрос выбора за ход» + END TURN + HALT при ≥2 AskQuestion; Metadata и Mode Gate не смешиваются; Mode Gate переносится на этап design после Metadata/scaffold (Decisions 3–4, Behavior Contract, S1).
  - (2) → раздельные `form_mode` / `layout_mode`, вопросы по одному и только при scope; mixed ответ направляет apply независимо; legacy `artifact_mode` → одинаковый маппинг на оба поля (Decisions 1–2, Behavior Contract, S2).
- **Покрытие:** полное по двум болям Why. Опциональный `[form:…]` в Why помечен как опциональный — design честно выносит в Follow-up (Decision 5), не маскируя как Primary.

### Q2 — Optimality

- **Выбранный путь:** `form_mode` + `layout_mode` + последовательные вопросы на design-stage; legacy fallback; без обязательного `[form:…]`.
- **Альтернативы из design (A/C):** A (один `artifact_mode` + текст в design) — нет машиночитаемого split, не закрывает Why(2). C (всегда два вопроса) — шум без UI. Отклонение обосновано.
- **Альтернативы, не упомянутые в `## Implementation Options`:**
  1. **Sequential only @ 1.55, без переноса Mode Gate на design** — оставить Mode Gate сразу после Metadata (как сейчас шаг 1.55 в `openspec-new-change/SKILL.md`), но жёсткий END TURN между ними; split полей всё равно нужен. Плюс: меньше сдвиг протокола new, раньше известен режим. Минус: вопрос до ясного Form-vs-Template scope → лишние/неверные вопросы (ровно то, зачем proposal переносит «когда ясно, что трогаем»). Хуже Why по точности scope; не превосходит B.
  2. **Асимметрия: общий `artifact_mode` + опциональный override только при расхождении** (например `layout_mode` только если ≠ форме). Плюс: проще миграция старых proposal, меньше полей в типичном case. Минус: два SSOT-пути чтения на apply/verify, хуже симметрия с уже раздельными путями Form vs Template в apply; риск «забыли override». Не лучше B для машиночитаемости и Why(2).
  3. **Отложить Mode Gate до входа в apply** (первый раз при задаче Form/Template). Плюс: new короче. Минус: противоречит frontload 1.56 и боли «понять при создании ЗНИ»; режимы всплывают поздно. Хуже Why.
  4. **Вложенная карта по артефакту** (`modes: { Form.xml: bsl-only, Template.xml: manual }`). Плюс: масштабируется на N артефактов. Минус: избыточно для двух фиксированных каналов kit; ломает простой YAML proposal. Не лучше B в этом scope.
- **Вердикт по Q2:** выбранный путь оптимален среди жизнеспособных; неупомянутые альтернативы либо ухудшают UX/frontload, либо усложняют чтение без выигрыша по Why. Равноправной архитектурной развилки нет — только уточнения протокола (см. Gaps).

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками
- **Причины:**
  - Да: Why ↔ split полей ↔ уже раздельное поведение apply по типу файла — выравнивание proposal/UX с кодом протокола, минимальная инвазивность (только `.cursor/**`).
  - Да: sequential + END TURN бьёт verified факт текущей склейки вопроса «форму/макет» в `forms-mxl-mode-gate.mdc` и соседство Metadata (1.5) / Mode Gate (1.55) без жёсткой паузы.
  - Оговорка: в design недостаточно зафиксирован порядок относительно **других** вопросов выбора на этапе design (в т.ч. AskQuestion приёмки срезов) и нет SSOT-текстов двух раздельных вопросов — без этого оркестратор снова смешает выборы или оставит старую склейку «форму/макет».

## Verdict

**CHALLENGE** — решение закрывает Why и оптимально по сути, но перед apply в design/specs нужно закрыть протокольные gaps (порядок vs Design Gate AskQuestion, формулировки двух вопросов, extend, явный blocker пустых режимов).

## Gaps for design.md

1. **Порядок vs Design Gate AskQuestion:** явно зафиксировать, что вопросы `form_mode` / `layout_mode` завершаются (запись в proposal) **до** любого AskQuestion приёмки срезов / «Принять design», и что Mode Gate **никогда** не идёт в одном сообщении с Design Gate selection. Сейчас Decision 3 описывает Metadata → scaffold → Form → Template → запись, но не стык с AskQuestion срезов в `openspec-new-change` (шаги Design Gate).
2. **SSOT формулировок двух вопросов:** в design (или явным указателем на правку Mode Gate) описать замену одной склейки «Как поставляем форму/макет…» на два независимых текста (только форма / только макет). Иначе S2/spec «form-only / layout-only» нечем реализовать без импровизации.
3. **`/opsx:extend` при появлении UI-scope:** Behavior Contract resume покрывает валидные поля; не хватает правила «scope впервые получил Form и/или Template → задать недостающий Mode-вопрос(ы) по одному, не молчать и не наследовать чужой канал».
4. **Spec alignment — пустые режимы:** design требует блокер apply/verify при пустом режиме и UI на артефакт; в `split-form-layout-modes/spec.md` нет сценария missing/empty `form_mode`|`layout_mode` (есть только legacy single `artifact_mode`). Добавить ADDED scenario или ослабить design до текущего info-уровня verify — сейчас расхождение design ↔ spec.
5. **implementation_invariant (мелочь):** уточнить, что при записи новых proposal поле `artifact_mode` не пишется (Decision 2), а readers apply/verify проверяют сначала пару `form_mode`/`layout_mode`, затем fallback — одной строкой в design, чтобы не плодить третий SSOT.

## Architectural alternatives

(нет — неупомянутые пути рассмотрены в Q2 и не равноправны выбранному B по коду/наблюдаемому поведению; reopen closed decisions не применим, ledger пуст.)

## Источники

- proposal.md — `## Why`, `## What Changes`, capabilities `sequential-gate-questions` / `split-form-layout-modes`
- design.md — Goals, Decisions 1–5, Behavior Contract, Implementation Options A–C, Slices S1–S2
- specs/sequential-gate-questions/spec.md — one question per turn; Metadata alone; dual blocked
- specs/split-form-layout-modes/spec.md — form-only / layout-only / mixed / legacy / kit n/a
- Код (verified) — `.cursor/rules/forms-mxl-mode-gate.mdc` (единый вопрос «форму/макет», `artifact_mode`); `.cursor/skills/openspec-new-change/SKILL.md` шаги 1.5 Metadata / 1.55 Mode Gate / 1.56 frontload; apply Task Dispatch по типу Form vs Template при одном `artifact_mode`
