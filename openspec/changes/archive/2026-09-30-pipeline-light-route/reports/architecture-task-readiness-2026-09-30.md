---
report_type: task-readiness
generated_at: 2026-09-30
agent: onec-code-architect
mode: task-readiness
scope:
  change: pipeline-light-route
  slices: [S1, S2, S3]
  files:
    - openspec/changes/pipeline-light-route/tasks.md
    - openspec/changes/pipeline-light-route/design.md
    - openspec/changes/pipeline-light-route/proposal.md
    - openspec/changes/pipeline-light-route/specs/pipeline-light-route/spec.md
    - .cursor/skills/openspec-verify-change/SKILL.md
    - .cursor/skills/openspec-extend-change/SKILL.md
    - .cursor/skills/openspec-archive-change/SKILL.md
    - .cursor/skills/openspec-apply-change/SKILL.md
    - .cursor/skills/openspec-verify-change/templates/report-header.md
    - .cursor/skills/openspec-verify-change/templates/executive-summary.md
    - .cursor/skills/openspec-verify-change/templates/chat-summary.md
    - .cursor/rules/sdd-workflow.mdc
    - .cursor/rules/task-triage.mdc
    - openspec/specs/verify-stop-repeat/spec.md
  capabilities: [pipeline-light-route]
  contracts: [EC-1]
confidence: high
open_questions_count: 0
layer_result: PASS
verdict: PASS
Gaps: []
---

# Task Readiness — pipeline-light-route

## Task

Оценка реализуемости as-is всех задач `tasks.md` (первый pre-apply, cache miss). Затронутый контракт: EC-1 (Behavior Contract 1 — замена утверждённого значения без проверки постановки). Код 1С / метаданные / формы не затрагиваются (kit-only).

## Precedent Coherence (criterion 8)

- Текущая дельта capability `pipeline-light-route` — только **ADDED** (`specs/pipeline-light-route/spec.md`). Отмены архивных ADDED нет.
- Задача **S1.19** создаёт `specs/verify-stop-repeat/spec.md` (MODIFIED к «Ответ не перезапускает всё») **после** архивации соседней ЗНИ — по design D3 / Assumptions 1. Файла дельты сейчас нет **по замыслу**, не из-за пробела постановки.
- Main-spec `openspec/specs/verify-stop-repeat/spec.md` с требованием «Ответ не перезапускает всё» уже существует (синхронизация соседней ЗНИ). S1.19 читает его после архивации и добавляет исключение — реализуемо.
- **GAP по precedent нет:** отсутствие MODIFIED-файла до apply не делает задачу нереализуемой.

## Criteria evaluation

### 1. Task-readability (файл + секция/процедура + бизнес-результат)

| Задачи | Вердикт |
|--------|---------|
| S1.1–S1.23 | PASS — глагол + путь (`.cursor/skills/...`, `templates/...`, rules) + секция (§1c, §7, §8, Novelty Check, Save report и т.д.) + результат; опорные D1–D6 в скобках |
| S1.24–S1.25, S2.10–S2.13, S3.1, S3.9–S3.10 | PASS — конкретные каталоги учебных ЗНИ / Grep-scope / критерий артефакта |
| S2.1–S2.9, S3.2–S3.8 | PASS |
| S1.accept / S2.accept / S3.accept | PASS (исключение readability; Primary + Scenario-буллеты на месте) |

Непрозрачных «Реализовать D*» без файла нет.

### 2. Data-contract guards

Не применимо: ЗНИ kit-only, контрактов данных 1С / `&После` / `Свойство()` нет. Guards в задачах не предписаны. **PASS.**

### 3. Plan fixes the stated loss (not a side symptom)

| Потеря (proposal Why / design Context) | Закрытие задачами |
|----------------------------------------|-------------------|
| Extend всегда → полный verify при замене значения | S1.2–S1.15, S1.17–S1.18 → EC-1 / BC 1–2 |
| Verify / граница среза уходят в full из-за ответа «меняющего правило» и оси | S1.3–S1.8, S1.16 |
| Archive rerun из-за галочек приёмки | S2.1–S2.4, S2.8 |
| Второй финал / silent_ok с устаревшим советом | S2.5–S2.7 |
| Копии шапки / журналов / пересказа постановки в повторном отчёте | S3.2–S3.6 |

Симптомные обходы (урезанный new, ослабление первой полной проверки, обход Code-Truth) в Non-Goals и в задачах не появляются. **PASS.**

### 4. Task order / object creation / S1.1 stop

- Внутри срезов зависимости направлены назад: S1.2→S1.1; S1.3→S1.2; S1.4–S1.7→S1.3; S1.8→S1.7; S1.10→S1.3; S1.11→S1.10; S1.12→S1.3+S1.9; …; фикстуры после текстовых правок.
- S2 правит общие файлы после приёмки S1 (шапка tasks); S3.1 — уборка после приёмки S2. Объектов, которые «создаёт поздняя задача, а ранняя уже требует», нет: учебные ЗНИ создают S1.24 / S2.10 / S3.9 до своих прогонов.
- **S1.1 stop — реализуем as written:** критерий требует `openspec/changes/archive/` для `value-efficient-verify` и `verify-stop-repeat`, четыре опоры в §1c и main-spec «Ответ не перезапускает всё»; иначе стоп + сообщение пользователю, дальше не идти. На момент отчёта обе ЗНИ ещё в `openspec/changes/` (не archive) — apply закономерно остановится на S1.1 до их архивации. Это штатный gate Assumptions 1, не дефект формулировки.

**PASS.**

### 5. User Task Contract

- В `S<N>.<M>` нет DENY-маркеров (`тестовой ИБ`, `на стенде`, `runtime-verify`, `спайк`, `в консоли`, `отладчик`).
- Прогоны verify/apply/archive учебных ЗНИ в S1.25, S2.11–S2.13, S3.9–S3.10 — **работа агента** («по скиллу», подготовка фикстур); шапка среза явно: учебные ЗНИ готовят и убирают задачи агента.
- Команды `/opsx:verify`, `/opsx:apply`, `/opsx:archive`, сценарии дополнения — только в **S1.accept / S2.accept / S3.accept** (Primary + optional).

**PASS.**

### 6. Manual configuration

Подтверждение оркестратора: маркеров ручной конфигурации в `tasks.md` нет.

Повторная сверка: нет «Ручное конфигурирование», «Конфигуратор», adopt, «создать реквизит», «выгрузить», pause-wait метаданных, form_mode. Единственное «вручную» — в метаданных сценария S1 («проверка, вызванная вручную») = вызов команды пользователем, не конфиг 1С.

**PASS — refute не требуется; markers отсутствуют.**

### 7. Precedent / deferred MODIFIED

См. § Precedent Coherence. S1.19 не unrealizable из-за отсутствия файла до apply. **PASS / no GAP.**

## Per-slice readiness summary

| Срез | Задачи | Результат |
|------|--------|-----------|
| S1 | S1.1–S1.25 + accept | Реализуемо; старт блокируется только явным стопом S1.1 до архива соседей |
| S2 | S2.1–S2.13 + accept | Реализуемо после S1; ключи хэша и archive §2a привязаны к существующим секциям (`## Slice Gate Decisions` уже пишет apply) |
| S3 | S3.1–S3.10 + accept | Реализуемо после S2; S3.2 stop при найденном читателе `accepted_tasks`/`closed_decisions` — реализуемый safety-gate |

## Named targets exist (spot-check)

| Цель из задач | Статус |
|---------------|--------|
| `openspec-verify-change/SKILL.md` §1c «Verify depth», «Между срезами», «Стык глубины», Novelty Check, Save report, Update snapshot, Output to chat | Есть |
| `templates/report-header.md` (axis hash, accepted_tasks, closed_decisions, artifact_hashes) | Есть |
| `templates/executive-summary.md`, `templates/chat-summary.md` | Есть |
| `openspec-extend-change/SKILL.md` §5 Architect Gate, §7 Verification Gate, §8 Handoff | Есть; §7 сейчас единственный исход `/opsx:verify` — цель S1.12 |
| `openspec-archive-change/SKILL.md` §2a freshness | Есть |
| `openspec-apply-change/SKILL.md` граница среза → verify §1c; `## Slice Gate Decisions` | Есть (S1.16 / S2.1 опираются на факт) |
| `sdd-workflow.mdc`, `task-triage.mdc` | Цели однострочных правок |
| Main `openspec/specs/verify-stop-repeat/spec.md` «Ответ не перезапускает всё» | Есть (вход для S1.19 после archive) |

## Simplicity Check

- **Viable alternatives:**
  1. **Как в tasks (выбран)** — одна строка класса в §1c + применение в extend + нормализованные ключи хэша + ветки archive §2a + урезание шапки не-full; учебные ЗНИ агентом; без новых агентов/файлов механизмов.
  2. **Отдельный классификатор в extend** — второй источник правды глубины; design D2 отклонил.
  3. **Один нормализованный ключ `tasks.md` для всех читателей** — ломает кэш/границу среза; design D4 отклонил.
  4. **Цепочка дельт снимка (D6 A)** — меняет всех читателей; design выбрал C.
- **Selected simplest viable design:** вариант 1 — расширение Existing Mechanisms без параллельных правил.
- **Why not simpler:** ещё проще (только «не звать verify из extend» без строки §1c / без оси на границе / без ключей архива) не закрывает EC-1 на границе среза и перед archive, ни копий отчётов (Goals 1, 3, 4).
- **Complexity budget:**
  - Files touched: ~10 kit-файлов (+ учебные ЗНИ, удаляемые)
  - Hooks/intercepts 1С: 0
  - New procedures/functions 1С: 0
  - Conditional branches / feature flags: класс D1 + 3 исхода extend + 3 ветки archive §2a + состав снимка не-full; отдельных feature-flag файлов нет

## Gaps

**Gaps: []** — CRITICAL gaps отсутствуют. WARNING gaps по неясности, блокирующей apply, отсутствуют.

## Observations (non-gaps)

1. На дату отчёта `value-efficient-verify` и `verify-stop-repeat` не в `openspec/changes/archive/` — S1.1 остановит apply до архивации; это задумано.
2. S1.4 правит описание полей отчёта в SKILL (не новый раздел шаблона) — согласовано с design: новый раздел отчёта вводит только S3.
3. S3.6 не имеет явной строки «Зависимости»; порядок среза и S3.7→S3.4/S3.6 достаточны; не WARNING.

## Verdict

**PASS** — все задачи реализуемы as-is относительно design D1–D6, EC-1 и названных файлов. Блокирующих GAP нет.
