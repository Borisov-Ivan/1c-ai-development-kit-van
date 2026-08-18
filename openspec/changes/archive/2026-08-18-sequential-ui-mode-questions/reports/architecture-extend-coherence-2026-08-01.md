---
report_type: architecture
generated_at: 2026-08-01
agent: onec-code-architect
mode: scope-coherence-audit
scope:
  change: sequential-ui-mode-questions
  slices: [S1, S2]
  files:
    - openspec/changes/sequential-ui-mode-questions/proposal.md
    - openspec/changes/sequential-ui-mode-questions/design.md
    - openspec/changes/sequential-ui-mode-questions/tasks.md
    - openspec/changes/sequential-ui-mode-questions/specs/split-form-layout-modes/spec.md
    - openspec/changes/sequential-ui-mode-questions/specs/sequential-gate-questions/spec.md
    - .cursor/rules/forms-mxl-mode-gate.mdc
  modules: []
  capabilities:
    - sequential-gate-questions
    - split-form-layout-modes
confidence: high
open_questions_count: 1
superseded_by: null
---

# Scope Coherence Audit — sequential-ui-mode-questions

## Context

Подтверждённый user-extend (вариант 1): асимметрия enum каналов Form vs Template.

| Канал | Допустимые значения |
|-------|---------------------|
| `form_mode` | `manual` \| `assisted` \| `bsl-only` \| `n/a` |
| `layout_mode` | `manual` \| `assisted` \| `n/a` (**без** `bsl-only`) |

Дополнительно (без нового AskQuestion): в Mode Gate / design зафиксировать guidance — MXL обычно `assisted`; СКД с оговорками; в сложных случаях — инструкция + точечные правки. Тип макета берётся из design/scope, отдельный вопрос «MXL или СКД» **не** вводить.

Бриф: Drift-check = `drift-warning`; усиливает Why; Non-Goals не ломает новыми enum; Behavior Contract меняется (Template не идёт в bsl-only path); архивный инвариант не отменяет.

Исторический proposal из git в промпте недоступен; сравнение с текущим `proposal.md` / `design.md` / specs / tasks как зафиксированным исходным замыслом до apply этого extend.

## Verdict

**drift-warning**

Расширение остаётся одной целью ЗНИ и усиливает Why («смешанные режимы», нельзя обещать «программно» для макета). Это не `scope-violation`: новых capability / новых enum-значений / отдельного AskQuestion нет. Но текущие артефакты всё ещё описывают **симметричный** enum `manual|assisted|bsl-only|n/a` для обоих каналов — до синхронизации proposal/design/specs/tasks/Mode Gate есть содержательный drift Behavior Contract.

## Findings

### 1. Tasks ↔ Why

| Задача / срез | Соответствие Why | Отклонение относительно подтверждённого extend |
|---------------|------------------|------------------------------------------------|
| S1 (один вопрос за ход) | Да — закрывает склейку Metadata+Mode | Нет |
| S2.1–S2.5 (split modes, readers, skills) | Да — закрывает склейку `artifact_mode` и смешанные режимы | Тексты предполагают одинаковый enum и 3 варианта вопроса и для макета (включая «программно» → `bsl-only`) |
| F1/F2 Follow-up | Вне Primary; Why не ломают | Нет |

Значимых задач «мимо Why» нет. Отклонение — не лишние задачи, а **недосуженная асимметрия** в формулировках S2 после подтверждённого extend.

### 2. Non-Goals

Текущий Non-Goal design: «Введение новых режимов кроме `manual` | `assisted` | `bsl-only` | `n/a`».

- Подтверждённый extend **не** вводит новых значений → формально Non-Goal не нарушен.
- Сужение `layout_mode` (исключение `bsl-only`) — уточнение закрытого множества **по каналу**, не расширение scope.
- Guidance MXL/СКД без AskQuestion — документация Mode Gate / design, не новая capability и не новый вопрос выбора → Non-Goals не нарушает.

**Риск формулировки:** после extend Non-Goal «одинаковый закрытый набор для обоих каналов» станет ложным, если не переписать: явно «без новых значений сверх `manual|assisted|bsl-only|n/a`; для `layout_mode` значение `bsl-only` недопустимо».

### 3. Decisions — согласованность (текущие vs extend)

Тихие противоречия **после** применения extend (сейчас артефакты ещё симметричны):

| Место | Сейчас | После extend (нужно) |
|-------|--------|----------------------|
| proposal What Changes | оба канала `…\|bsl-only\|n/a` | `form_mode` с `bsl-only`; `layout_mode` без |
| design Decision 6 / формулировки вопросов | два текста, но mapping с «программно» для макета | вопрос макета: только вручную / автоматически (+ n/a вне scope) |
| design Behavior Contract | пример «форма программно, макет вручную» | плюс инвариант: Template **никогда** не направляется в bsl-only path; выбор/запись `layout_mode: bsl-only` — STOP/ошибка |
| design Non-Goals | общий enum | асимметричный закрытый набор |
| spec Requirement | оба поля с `bsl-only` | enum `layout_mode` без `bsl-only`; scenario на отказ/нормализацию |
| forms-mxl-mode-gate (цель S2.1) | таблица `artifact_mode` с bsl-only для Template.xml | колонка/ветка layout без bsl-only |

Решения 1–5, 7–8 (имена полей, последовательность, END TURN, legacy precedence, extend/поздний UI) с асимметрией **совместимы**; правка точечная в Decision 6 + Behavior Contract + Non-Goals + spec.

### 4. Behavior Contract vs S\<N\>.accept

Текущий Behavior Contract уже шире симметричного enum только примером mixed (Form bsl-only / Template manual), но **не запрещает** `layout_mode: bsl-only`.

После extend контракт сужается по Template:

- наблюдаемо: вопрос макета без варианта «программно»; apply/verify не принимают `layout_mode: bsl-only`;
- S2.accept / Primary («разные режимы») остаётся валидным, но optional/учебные сценарии и mapping в S2.1 должны исключить bsl-only для layout.

Чеклисты S1.accept / S2.accept **покрывают** Primary Why; gap — отсутствие явного сценария «layout bsl-only запрещён / legacy bsl-only → layout не bsl-only» до правки specs/tasks.

### 5. Extend без архитектурного сопровождения

В `reports/` нет предыдущих `architecture-extend-coherence-*.md`. Семантический триггер брифа (`drift-warning`) отработан этим отчётом. Классических Extend-секций, раздувающих объём без architect, в переданном контексте нет (audit по подтверждённому брифу варианта 1).

### 6. Одна цель или расползание?

**Одна цель.** Ось ЗНИ прежняя: sequential selection + split `form_mode`/`layout_mode` + legacy fallback. Extend — уточнение семантики канала layout (честный контракт «макет программно не правят»), плюс guidance MXL/СКД без нового UI-вопроса. Отдельная ЗНИ не требуется.

## Recommendations

1. **proposal.md — What Changes:** явно асимметричные enum; одна фраза, что `layout_mode` не включает `bsl-only` (макет не поставляется «программно» как режим канала).
2. **design.md:**
   - Non-Goals: закрытый набор без новых значений; `bsl-only` только у `form_mode`.
   - Decision (новый или правка п.6): тексты/mapping вопроса Template — `manual` / `assisted` / (scope→`n/a`); без варианта 3 для макета.
   - Behavior Contract: Template не идёт в bsl-only path; запись `layout_mode: bsl-only` недопустима.
   - Guidance (1 абзац): MXL обычно `assisted`; СКД — с оговорками; сложные случаи — инструкция + точечные правки; тип макета из design/scope — **без** AskQuestion «MXL или СКД».
3. **specs/split-form-layout-modes/spec.md:** Requirement — разные допустимые множества; ADDED Scenario: при попытке `layout_mode: bsl-only` (или ответе «программно» на вопрос макета) — STOP / переспрос / отказ записи, не silent coerce в `assisted` без правила.
4. **tasks.md S2.1 (+ при необходимости S2.3/S2.4):** Mode Gate SSOT и readers учитывают асимметрию; вопрос макета без «программно».
5. **Legacy `artifact_mode: bsl-only` (открытый пункт — зафиксировать одной строкой в design Decision 7):** рекомендуемый инвариант реализации: lone legacy `bsl-only` → `form_mode: bsl-only`, `layout_mode: manual` (или STOP, если в scope есть Template и нельзя молча выбрать) — **не** копировать `bsl-only` в `layout_mode`. Предпочтительнее явный STOP/Mode-вопрос только для layout-канала при Template in scope, чтобы не маскировать выбор.
6. **Не** добавлять capability, срез или AskQuestion про тип макета.

## Closes

- Семантический Drift-check брифа extend (`drift-warning`) — отчёт `architecture-extend-coherence-2026-08-01.md`.
- Грейс антидубля для **этого** подтверждённого брифа (повторный audit до handoff не нужен).
- Не закрывает: фактическое обновление артефактов (шаг Artifact update `/opsx:extend` после принятия recommendations).

## Open question (не блокер цели ЗНИ)

- **OQ1 — Legacy lone `artifact_mode: bsl-only` при Template in scope:** `layout_mode: manual` молча vs STOP + один Mode-вопрос только по макету. Нужна одна фраза в design Decision 7 до apply S2. Рекомендация аудита: STOP/вопрос layout (consistent с empty-mode), не silent `bsl-only`→`manual` без фиксации в design.
