---
report_type: design-challenge
generated_at: 2026-08-01
agent: onec-code-architect
mode: design-challenge
scope:
  change: sequential-ui-mode-questions
  design_mtime: "2026-07-31T23:09:17Z"
verdict: CHALLENGE
confidence: medium
---

# Design Challenge — sequential-ui-mode-questions

## KB references

- Discovery выполнен, совпадений нет — not relevant: KB-фактов для опоры нет; выводы только из proposal / design / specs и текущего кода гейтов.

## Адверсариальная установка

Независимый прогон после сужения оси (forms-only / per-form). Прочитаны `proposal.md`, `design.md`, `specs/sequential-gate-questions/spec.md`, `specs/split-form-layout-modes/spec.md`; для verified code facts — текущие `.cursor/rules/forms-mxl-mode-gate.mdc` и фрагменты `openspec-new-change` / `openspec-apply-change`. Собственные `reports/architecture-*.md` как источник истины не использовались. Closed decisions приняты как ось; reopen только при доказательстве из кода.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** (1) оркестратор может выдать два выбора в одном сообщении (маркер + способ поставки формы); (2) единый `artifact_mode` не даёт разные режимы **разным формам** в одной ЗНИ — заказчик не понимает, как отвечать, и не может выбрать «одна форма вручную, другая программно».
- **Design адресует:**
  - Why(1) → Decisions 3–4 + Behavior Contract: один выбор за ход, END TURN, Metadata и Mode не в одном сообщении; self-check HALT при ≥2 AskQuestion; Mode не смешивать с Design Gate selection.
  - Why(2) → Decisions 1–2, 8 + per-form `form_mode` на design: N форм → N вопросов с END TURN; разные режимы допустимы; apply следует режиму **этой** формы; запрет копирования режима соседней формы.
  - Сужение макетов (What Changes / closed) → Decisions 6, 9: Mode-вопрос только про форму; макет вне Mode Gate new; default manual + разрешение на apply.
- **Покрытие:** полное по боли из Why. Симптом «склейка форму/макет» в текущем gate (см. код ниже) закрывается Decision 6; это согласовано с Why про формы, а не подмена проблемы.

### Q2 — Optimality

- **Выбранный путь:** Option D — per-form `form_mode` на design + последовательные вопросы; макеты — apply-политика без Mode Gate в new; legacy lone `artifact_mode` → fallback в `form_mode`.
- **Альтернативы (включая не упомянутые в design `## Implementation Options`):**
  1. **Cascade «один режим на все формы?»** — сначала один выбор «одинаковый режим для всех / разные»; при «одинаковый» — один Mode-вопрос и запись на все формы scope; при «разные» — текущий цикл per-form. Плюс: меньше ходов при N формах с одинаковым режимом (риск из design Risks). Минус: лишний вопрос; ветка «одинаковый для всех» отменяет обязательный вопрос **по каждой** форме. **reopen-blocked: per_form_mode_on_design**. Внутри closed оси допустим только смягчающий UX (подсказка «как у предыдущей формы» в тексте варианта), не замена цикла.
  2. **Режимы в explore-handoff / `## Постановка ЗНИ`** — зафиксировать `form_mode` до `/opsx:new`; в new Mode Gate только дозаполняет пробелы (validate + вопрос лишь для форм без режима). Плюс: меньше трения в new. Минус: explore становится Mode-aware; не снимает sequential invariant и per-form запись. Не лучше D как замена — дополнение; в design/spec не зафиксировано как контракт handoff.
  3. **Инференс режима из формулировок задач** («программные элементы» → `bsl-only`, «compile» → `assisted`) без Mode Gate. Плюс: ноль вопросов. Минус: хрупко, молчаливый выбор режима — прямо противоречит Why (заказчик должен осознанно выбрать) и текущему инварианту gate «не выбирать assisted молча». Хуже D.
  4. **Вернуть Mode-вопрос макета в new (dual-channel / `layout_mode`)** — как Option B. **reopen-blocked: forms_only_no_layout_mode_gate** / `acceptance_loop_s2_path`. Код сегодня ещё держит единый `artifact_mode` на Form+Template (`forms-mxl-mode-gate.mdc`: вопрос «форму/макет», таблица Apply для Template.xml) — это аргумент *за переход*, не за откат сужения: сужение как раз развязывает Form от Template. Откат увеличил бы шум и снова смешал бы каналы.
  5. **SSOT режимов в `.openspec.yaml` / маркерах tasks вместо секции proposal** — плюс: ближе к apply-маркерам `[mxl:…]`. Минус: proposal уже SSOT Metadata/режимов для verify; маркеры `[form:…]` в Non-Goals/Follow-up. Не лучше для Primary этой ЗНИ.
- **Вердикт по Q2:** при удержании closed axis выбранный D **оптимален** среди жизнеспособных; неупомянутые альтернативы либо reopen-blocked, либо слабее/дополнительны. Оптимальность упирается не в смену оси, а в **недоспецифицированные инварианты реализации** (см. Gaps).

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками
- **Причины:**
  - Да: Why ↔ design ↔ specs выровнены; sequential + per-form прямо лечат оба пункта Why; сужение макетов согласовано с What Changes и closed ledger.
  - Да: точки правки названы (new skill, Mode Gate SSOT, apply/verify readers) без прикладного BSL — реалистично для kit-evolution.
  - Оговорка: до apply нет канонической схемы записи per-form, алгоритма «формы в scope», семантики legacy×N форм и формы «явного разрешения» на макет — без этого readers apply/verify разъедутся.

## Verdict

**CHALLENGE** — решение бьёт в Why и оптимально под closed axis, но перед apply нужно закрыть implementation_invariant gaps (схема per-form, scope enumeration, legacy×multi-form, permission-on-apply), иначе Behavior Contract неоднозначен для исполнителей.

## Gaps for design.md

1. **Схема записи per-form `form_mode` (implementation_invariant).** Decision 2 говорит «машиночитаемый список путь/имя → mode» и допускает скаляр при одной форме, но нет канонического примера (YAML map / список / таблица), канона ключа (метапуть `Document.X.Form.Y` vs путь `src/.../Form.xml` vs синоним) и правила нормализации. Добавить в design (и отразить в `split-form-layout-modes` spec) обязательный пример + правило «один канонический ключ на форму».
2. **Алгоритм «формы в scope» на design (implementation_invariant).** Не сказано, из чего строится список для цикла Mode: Why/What Changes, упомянутые Form.xml, будущие tasks, handoff. Без этого N вопросов нестабилен. Зафиксировать источник enumeration и момент (после scaffold / при стабилизации design scope).
3. **Lone legacy `artifact_mode` при N>1 формах (implementation_invariant).** Spec Scenario «Legacy…» мапит одно значение на `form_mode` для форм в scope; Behavior Contract запрещает копировать режим *соседней* формы при пустом режиме. Явно выбрать: (a) lone legacy распространяется на все формы scope как одинаковый валидный режим без переспроса, или (b) при N>1 lone legacy недостаточен → Mode-вопросы per-form. Сейчас читается как (a); если так — одна фраза в design Decision 7.
4. **Форма «явного разрешения» на non-manual макет в apply (implementation_invariant).** Decision 9 / spec «Layout stays manual…» не задают артефакт разрешения (свободный текст в чате, одноразовый AskQuestion, маркер `[mxl:assisted]` в tasks, запись в proposal). Нужна одна норма для apply/verify, без resurrect Mode Gate в new. **Не** fork оси `forms_only_no_layout_mode_gate`.
5. **Имя секции proposal vs текущий код.** Design: `## Forms mode`; код/skill сейчас: `## Forms & layouts mode` + `artifact_mode`. В design явно: целевое имя секции, совместимость со старым заголовком при чтении, запрет писать новый единый `artifact_mode` как SSOT.
6. **Согласование S1 acceptance с design-stage Mode.** Design Decision 3: Mode на этапе design после scaffold, до Design Gate AskQuestion. S1 primary / tasks формулировка «после ответа на маркер следующий вопрос — режим формы» может читаться как немедленный следующий ход без уточнения стадии. Одна фраза: первый *selection* Mode — на design; между Metadata и Mode допустимы сообщения без выбора; Mode ≠ Design Gate AskQuestion.

## Architectural alternatives

Равноправных архитектурных развилок по коду/поведению **вне** closed axis нет. Ниже — только помеченные reopen (не выбирать без снятия ledger):

### Per-form vs cascade
**A. Строгий цикл per-form (closed):** N форм → N вопросов. Trade-off: больше ходов, явный выбор на форму.  
**B. Cascade «все одинаковые?»:** меньше ходов при гомогенном scope. Trade-off: ослабляет «вопрос по каждой форме». `reopen-blocked: per_form_mode_on_design`

### Макет: вне new vs Mode в new
**A. Политика apply-only (closed):** нет Mode-вопроса макета в new; default manual. Trade-off: нет структурированного выбора макета до apply.  
**B. Dual Mode Gate / `layout_mode` в new:** снова выбор поставки макета в new. Trade-off: шум и склейка каналов. `reopen-blocked: forms_only_no_layout_mode_gate`

## Источники

- proposal.md — `## Why` (два выбора; единый artifact_mode vs разные формы); `## What Changes` (sequential; form_mode per-form; макеты вне Mode Gate; legacy fallback)
- design.md — Goals/Non-Goals; Decisions 1–9; Behavior Contract; Implementation Options A/B/C/D; Slices S1–S2; «Решения verify (зафиксировано)»
- specs/sequential-gate-questions/spec.md — One selection question; Metadata without Mode; Second gate after answer; Dual blocked
- specs/split-form-layout-modes/spec.md — Per-form modes; multi-form sequential; no layout Mode in new; layout manual unless permission; legacy→form_mode; kit n/a; empty form mode blocks
- Код (verified) — `.cursor/rules/forms-mxl-mode-gate.mdc`: единый `artifact_mode`, вопрос «Как поставляем форму/макет…», секция `## Forms & layouts mode`, Apply-таблица Form+Template; `.cursor/skills/openspec-new-change/SKILL.md` шаг 1.55 Mode Gate до design-stage цикла; `.cursor/skills/openspec-apply-change/SKILL.md` Template ветка по `artifact_mode` / маркерам `[mxl:…]`
