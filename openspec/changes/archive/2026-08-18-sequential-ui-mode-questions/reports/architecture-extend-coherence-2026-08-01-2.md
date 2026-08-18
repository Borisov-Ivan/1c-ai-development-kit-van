---
report_type: architecture
generated_at: 2026-08-01
agent: onec-code-architect
mode: scope-coherence-audit
verdict: drift-warning
scope:
  change: sequential-ui-mode-questions
  slices: [S1, S2]
  files:
    - openspec/changes/sequential-ui-mode-questions/proposal.md
    - openspec/changes/sequential-ui-mode-questions/design.md
    - openspec/changes/sequential-ui-mode-questions/tasks.md
    - openspec/changes/sequential-ui-mode-questions/debug.md
    - openspec/changes/sequential-ui-mode-questions/specs/sequential-gate-questions/spec.md
    - openspec/changes/sequential-ui-mode-questions/specs/split-form-layout-modes/spec.md
  modules: []
  capabilities:
    - sequential-gate-questions
    - split-form-layout-modes
related_reports:
  - reports/architecture-extend-coherence-2026-08-01.md
confidence: high
open_questions_count: 1
superseded_by: null
---

# Scope Coherence Audit — sequential-ui-mode-questions (сужение: form-only Mode Gate)

## Context

Подтверждённое пользователем сужение scope (после dual-channel `form_mode`/`layout_mode` и асимметрии enum от 2026-08-01):

1. Макеты **вне** Mode Gate этой ЗНИ: вопрос Template/MXL не задаётся; `layout_mode` не предмет выбора в proposal.
2. Макеты по умолчанию только вручную; программная правка макета — только по явному разрешению **во время apply** (не вопрос Mode Gate в `/opsx:new`).
3. Режим поставки только для управляемых форм: `form_mode` ∈ {`manual`, `assisted`, `bsl-only`, `n/a`}.
4. Mode Gate формы — на этапе design, **по одной форме** на каждую форму в scope; END TURN между вопросами; не смешивать с Metadata и Design Gate selection.
5. Инвариант «один вопрос выбора за ход» (`sequential-gate-questions`) сохраняется.
6. Capability `split-form-layout-modes` сужается/переписывается под **form-delivery (per-form)**, не dual-channel form+layout.

Блок «Соответствие исходному scope» (internal): Why усиливается (склейка двух выборов + склейка режимов сужена до per-form); Non-Goals затрагиваются (макеты/Mode Gate макетов исключаются); Behavior Contract меняется; архивный инвариант не отменяется; Drift-check брифа = `drift-warning`.

Исторический proposal отдельно недоступен; база сравнения — текущие артефакты + Extend-секции в `debug.md`. KB/ADR: Discovery пуст.

## KB references

- Discovery выполнен, совпадений нет — секция фактов не применялась.

## Verdict

**drift-warning**

После принятия сужения ЗНИ **остаётся одной целью** (последовательные вопросы выбора + Mode Gate поставки **форм**), но текущие proposal/design/specs/tasks всё ещё описывают **dual-channel form+layout** (вопросы макета, `layout_mode`, mixed modes, Decision 9 MXL/СКД, S2 Primary про пару режимов). Это не `scope-violation`: сужение осознанно снимает макеты с Goals, не добавляет вторую независимую продуктовую ось. До синхронизации артефактов — содержательный drift Behavior Contract и S2.

## Answers (вопросы аудита)

### 1. Tasks ↔ Why — отклонения после сужения

| Задача / срез | Соответствие исходному Why | После подтверждённого сужения |
|---------------|----------------------------|-------------------------------|
| S1 (один вопрос за ход) | Да — Metadata ≠ Mode в одном сообщении | **Да** — ось сохраняется; формулировки S1.accept «форма/макет» нужно сузить до «форма» (и per-form при нескольких формах) |
| S2.1–S2.5 / S2.accept | Да — split `form_mode`/`layout_mode`, mixed, legacy pair | **Отклонение:** Primary и задачи про dual-channel, вопрос макета, `layout_mode`, асимметрию layout enum, Decision 9 — **вне** нового scope Mode Gate |
| F1/F2 Follow-up | Вне Primary | Не ломают Why; F2 `[form:…]` остаётся опциональным |

Значимых задач «мимо Why» как новых capability нет; риск — **недосуженный dual-channel S2** и отсутствие задач на **per-form** вопросы (по одной форме в scope).

### 2. Non-Goals

Текущие Non-Goals **не** исключают Mode Gate / режимы макетов; наоборот, Goals/Decisions их требуют.

После принятия сужения:

- Нарушение Non-Goals возникнет, если **оставить** в Primary сценарии/задачи «вопрос про макет», «смешанные form+layout», запись/`AskQuestion` по `layout_mode`.
- Правильная фиксация: в Non-Goals явно — «Mode Gate и выбор режима для Template/MXL вне этой ЗНИ»; политика «макет по умолчанию manual; programmatic только по явному разрешению на apply» — как инвариант/guidance apply, не как Mode Gate new.
- Non-Goal «без новых enum сверх form_mode» совместим; убирается отдельный enum-канал layout.

**Сейчас:** артефакты противоречат будущему Non-Goal → drift до переписи, не уже совершённый scope-violation реализации.

### 3. Decisions — тихие противоречия

| Decision / место | Текущий текст | Сужение (нужно) |
|------------------|---------------|-----------------|
| proposal Why / What Changes | склейка form+layout; раздельные `form_mode` **и** `layout_mode`; вопрос макета | Why: (1) два выбора в одном ходе; (2) склейка режимов → **per-form** `form_mode`; макеты не в Mode Gate |
| proposal Forms & layouts + Impact | `layout_mode: n/a`; readers form+layout | секция/поля: акцент на `form_mode` (и политика макета вне выбора); Impact без Mode Gate Template |
| design Goals | раздельные form+layout; вопросы по Form **и** Template | Goals: sequential + per-form `form_mode` на design; без Mode-вопроса макета |
| Decision 1–2 | пара полей, секция Forms & layouts | имена: `form_mode` остаётся; `layout_mode` как предмет выбора — снять или оставить только совместимость/default без вопроса (зафиксировать явно) |
| Decision 3, 8 | Form → END TURN → Template; extend недостающий layout-вопрос | только вопросы **форм** (1 форма = 1 вопрос); extend — недостающий `form_mode` по форме |
| Decision 6–7, 9 | тексты вопроса макета; pair/legacy layout; MXL/СКД | 6: только формулировки формы; 7: legacy → `form_mode` (+ политика макета без Mode-вопроса); 9 — **вне** Mode Gate этой ЗНИ или сжать в apply-инвариант «manual default / permission on apply» |
| Behavior Contract | «только макет — вопрос про макет»; mixed form/layout; layout enum | убрать layout AskQuestion и mixed modes из контракта; добавить per-form + END TURN; макет — default/apply-permission |
| Slices S2 / матрица | Form-only, Layout-only, mixed, layout rejects bsl-only… | переписать под form-delivery: form-only / multi-form sequential / legacy form / empty form mode; без layout-only/mixed как Primary |
| tasks S2.* | SSOT dual-channel + consumers layout | переписать под form_mode per-form; apply: макет manual default + явное разрешение programmatic |

Решения про END TURN / Metadata / Design Gate selection / один вопрос за ход — **согласованы** с сужением; противоречия сосредоточены в dual-channel и layout AskQuestion.

### 4. Behavior Contract vs accept-чеклисты

Текущий Behavior Contract **шире** и **иначе направлен**, чем подтверждённое сужение:

- обещает вопросы/режимы макета и смешанные form+layout;
- не обещает явный per-form цикл (N форм → N вопросов с END TURN).

S1.accept / S2.accept сейчас калиброваны под dual-channel Primary («разные `form_mode` и `layout_mode`»). После сужения accept **должен сузиться** (per-form `form_mode`, нет layout Mode-вопроса); иначе чеклисты тянут реализацию обратно в снятый scope.

Gap: нет accept-сценария «две формы в scope → два последовательных вопроса с разными режимами».

### 5. Extend-секции без архитектурного сопровождения

| Extend в debug.md | Architect |
|-------------------|-----------|
| 2026-07-31 repair 1–2 | не требовался (implementation_invariant) — ок для точечных сценариев |
| 2026-08-01 user-extend (асимметрия layout enum) | есть `architecture-extend-coherence-2026-08-01.md` |
| Loop Detection 2026-08-01 | redesign-отчёт есть; решение A/B ещё «ожидает» — **не** silent sprawl |
| **Это** сужение (form-only / per-form) | сопровождение = **этот** отчёт; до Artifact update артефакты не переписаны |

Классического «extend без architect при смене оси» по этому брифу нет — audit выполнен до принятия правок. Риск: если применить сужение частично (оставить S2 dual-channel + добавить per-form) без полной переписи — получится расползание на два контракта.

### 6. Одна цель или 2+ независимых?

**Одна цель** при полной переписи артефактов:

- ось A: `sequential-gate-questions` (один выбор за ход; Metadata ≠ Mode ≠ Design Gate);
- ось B (содержание Mode Gate): выбор поставки **управляемой формы** (per-form `form_mode`).

Политика макетов («default manual; programmatic только с явного разрешения на apply») — **сопровождающий инвариант**, не вторая capability, если не вводить отдельный Mode Gate / отдельный срез Primary под layout.

**Риск 2+ целей:** оставить dual-channel S2 **и** добавить per-form **и** отдельный продуктовый трек «разрешение programmatic layout на apply» как равноправный Primary — тогда нужен split ЗНИ. При подтверждённом сужении правильный путь — consolidation в form-delivery, layout убрать из Mode Gate/S2 Primary.

## Recommendations (при принятии сужения)

1. **proposal.md**
   - Why: оставить боль про два выбора в одном сообщении; боль про склейку режимов переформулировать как невозможность задать режим **формы** (и разные режимы **разных форм**), без обещания Mode Gate макета / mixed form+layout.
   - What Changes / Capabilities: `split-form-layout-modes` → form-delivery / per-form (или переименовать capability/папку spec согласованно); убрать обязательный выбор `layout_mode` и вопрос макета.
   - Секция proposal: `form_mode` как предмет Mode Gate; политика макета — коротко «вне выбора этой ЗНИ / default manual».
   - Impact: Mode Gate forms; apply — явное разрешение programmatic layout только на apply (не new Mode Gate).

2. **design.md**
   - Goals / Non-Goals: Non-Goals += Mode Gate Template/MXL и выбор `layout_mode` вне ЗНИ; Goals = sequential + per-form `form_mode` на design.
   - Decisions 1–3, 6–9: снять/переписать dual-channel и Decision 9 как Mode Gate; зафиксировать цикл «одна форма → один вопрос → END TURN»; стык с Design Gate без изменений по смыслу.
   - Behavior Contract: убрать layout AskQuestion / mixed modes Primary; добавить multi-form; макет — default manual + permission-on-apply.
   - Slices/матрица S2: сценарии form-only, multi-form sequential, legacy→form_mode, empty/`n/a` form blocks; без Layout-only / Mixed form+layout / Layout bsl-only как Primary.
   - Risks: убрать риски, завязанные только на layout Mode-вопрос; добавить риск N форм → N ходов.

3. **specs/**
   - `sequential-gate-questions`: заменить «форма или макет» на «поставка формы» (и при нескольких формах — следующий вопрос формы только после ответа); Metadata scenario без Mode формы.
   - `split-form-layout-modes` (или переименованный spec): Requirement про `form_mode` per-form; сценарии multi-form; legacy lone `artifact_mode` → `form_mode`; empty form mode blocks; **удалить/не Primary** Layout-only, Mixed form+layout, Layout bsl-only, Pair-с-layout как Mode Gate. Политику макета — отдельным тонким сценарием apply «без Mode-вопроса» или вынести в design Non-Goals + apply skill, не раздувая capability.

4. **tasks.md**
   - S1: accept-тексты без «макет» как объекта Mode Gate.
   - S2: переписать заголовок/Primary/S2.1–S2.5/S2.accept под form-delivery per-form; readers apply/verify — `form_mode` + legacy; строка про макет: default manual / programmatic только по явному разрешению на apply (не задача «спросить layout_mode в new»).
   - Добавить явный пункт/accept-bullet: несколько форм в scope → последовательные вопросы с END TURN.

5. **debug.md** (оркестратор после Artifact update): зафиксировать Extend с disposition accepted и ссылкой на этот отчёт; закрыть/пересмотреть pending Loop Detection A/B в свете сужения (dual-channel state space снимается — consolidation layout-ветки может стать obsolete).

6. **Не** вводить вторую ЗНИ, если layout остаётся инвариантом apply без Mode Gate; **не** оставлять параллельно старый S2 dual-channel и новый per-form без удаления первого.

## Closes

- Семантический Drift-check брифа сужения (`drift-warning`) — этот отчёт `architecture-extend-coherence-2026-08-01-2.md`.
- Не закрывает: фактический Artifact update proposal/design/specs/tasks; решение Loop Detection A/B в debug (пересмотреть после переписи S2).

## Open question (не блокер цели)

- **OQ1 — судьба поля `layout_mode` в proposal schema:** (a) полностью убрать из записи новых change и читать только политику apply; (b) оставлять `layout_mode: n/a`/`manual` без Mode-вопроса для совместимости readers. Нужна одна фраза в design Decision до apply S2. Рекомендация аудита: **(b) minimal** — писать `n/a` или фиксированный default без AskQuestion; не resurrect Mode Gate макета.
