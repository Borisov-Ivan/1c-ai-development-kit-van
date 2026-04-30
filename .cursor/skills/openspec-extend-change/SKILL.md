---
name: openspec-extend-change
description: Controlled scope extension for an existing OpenSpec change. Reads user text and optional source reports/files, shows a mandatory brief, updates change artifacts only after confirmation, then hands off to verify/apply.
license: MIT
compatibility: Does not call writer/reviewer and never edits BSL/XML metadata. May delegate read-only analysis to onec-code-architect / onec-code-explorer when gates require it.
metadata:
  author: project
  version: "1.0"
---

Контролируемо расширить или пересмотреть scope существующего OpenSpec change по новому требованию, отчёту ревью, debug/RCA, verify-отчёту, архитектурному отчёту или Explore Summary.

**Extend правит только артефакты change**: `proposal.md`, `design.md`, `specs/**`, `tasks.md`, `debug.md`, `reports/**`. Код BSL, XML метаданных и реализация остаются за `/opsx:apply`.

---

## Input (free-form)

Пользователь может передать:

- `<change-name>` — имя change. Если не указано, определить по `openspec list --json`; при неоднозначности — `AskQuestion`.
- Текст нового требования / пересмотра / замечания.
- Ссылки на файлы в любом виде:
  - `@path/to/file.md`
  - относительный или абсолютный путь
  - `--from-review <path>` — отчёт `/review`
  - `--from-debug <path>` — `debug.md` или RCA-отчёт
  - `--from-verify <path>` — отчёт `/opsx:verify`
  - `--from-architecture <path>` — отчёт архитектора
  - `--from-explore <path>` — Explore Summary
  - `--code-sync` — штатная синхронизация OpenSpec-артефактов с фактическим кодом после ручного упрощения, writer/apply или Code-Truth Gate (`phantom-symbol`, устаревшие имена процедур, drift design/tasks/debug).

Если текст требования отсутствует, но указан файл — извлечь намерение из файла и показать в брифе. Если намерение неоднозначно — спросить пользователя после брифа, до правок.

---

## Entry Protocol (MANDATORY)

Первый шаг команды:

1. Прочитать этот `SKILL.md` (обеспечивает command-skill-gate).
2. Определить change:
   - если `<change-name>` указан — использовать его;
   - иначе выполнить `openspec list --json` и выбрать активный / спросить пользователя.
3. Выполнить `openspec instructions apply --change "<name>" --json`.
4. Прочитать `openspec/project.md` и артефакты change из `contextFiles`: `proposal.md`, `design.md`, `tasks.md`, `specs/**` при наличии.
5. Прочитать только явно переданные source-файлы (`--from-*`, `@path`, пути в запросе). Это не трассы; трассы остаются за `/opsx:debug`. Если указан `--code-sync`, source = артефакты change + `debug.md` + отчёты `reports/**` + результаты Code-Truth Gate; чтение BSL/XML до брифа всё равно запрещено.
6. Сформировать и показать **бриф extend** по шаблону ниже.
7. **END TURN.** До подтверждения пользователя запрещены: запись артефактов, вызовы writer/reviewer, вызовы architect/explorer, чтение BSL/XML для анализа логики.

Разрешённые действия до брифа: чтение этого скилла, `openspec list --json`, `openspec instructions apply --json`, чтение `project.md`, чтение артефактов change, чтение явно переданных markdown/text/source-report файлов.

### Шаблон брифа (T-BRIEF)

```markdown
---
**Бриф для расширения ЗНИ (change: <name>)**

- **Контекст:** <1 предложение из proposal: зачем существует change; без внутренних ID>
- **Сценарий:** <что должно измениться в постановке / какую область уточняем; без внутренних ID>
- **Вход:** <факты из сообщения пользователя и/или source-файлов; без “должно быть”>
- **Технический контекст:** <пути артефактов, модули/процедуры из отчётов в backticks, без чтения кода>
- **Артефакты:**
  - <path>
- **KB в scope:** <KB-NNNN ... или “нет совпадений / Discovery не требовался для extend”>

**Предлагаемое изменение артефактов**
1. `proposal.md`: <что добавить/уточнить или “без изменений”>
2. `design.md`: <какое решение / rationale / existing mechanisms уточнить>
3. `specs/**`: <Requirement/Scenario: ADDED/MODIFIED/REMOVED или “без изменений”>
4. `tasks.md`: <inside-slice / fix-срез / новый срез; что добавить>
5. `debug.md`: <запись Extend с источником>

**План**
1. Уточнить неоднозначности (если есть) через AskQuestion.
2. Проверить Architect Gate / Code-Truth Gate.
3. Если `--code-sync` — после подтверждения делегировать `onec-code-explorer` на фактический код и сохранить отчёт `reports/exploration-code-sync-YYYY-MM-DD.md`.
4. Обновить артефакты change.
5. Передать на `/opsx:verify <name>`.

Бриф верный? Подтвердите — начну обновление артефактов.
---
```

Self-check перед выводом: слои разделены; в UX-полях нет `S<N>.T<M>` / `D<N>` / номеров задач; списки нумерованы; поле «Вход» содержит только факты; каждое поле ≤3 строк или ≤7 пунктов; поле «KB в scope» присутствует.

---

## Per-turn Delegation Gate

На каждом follow-up ходе:

1. Если запрос требует обследования кода, трассировки вызовов, проверки метаданных или анализа 3+ модулей — не читать `.bsl`/XML самостоятельно.
2. Сформировать бриф и делегировать:
   - `onec-code-explorer` — для обследования кода;
   - `onec-code-architect` — для выбора/пересмотра подхода;
   - `onec-trace-analyst` не используется в extend; трассы перенаправлять в `/opsx:debug`.
3. До делегирования допустимо читать только OpenSpec-артефакты и явно переданные отчёты.

---

## Source File Classification

После чтения явно переданных файлов классифицировать источник:

| Source | Признаки | Что извлекать |
|--------|----------|---------------|
| `review` | `review-*.md`, `code-review-*.md`, секции `Findings`, `Action`, `Type`, `Severity` | findings, disposition, `ARCHITECTURE`, `MUST_FIX`, противоречия design, пути/anchors |
| `debug` | `debug.md`, `trace-analysis-*`, RCA, `Verified facts`, `Hypotheses`, `Root cause` | verified facts, hypotheses, root cause, target slice |
| `verify` | `verification-*.md`, `Phase B`, `Decision`, `CRITICAL/WARNING/SUGGESTION` | decision cards, scope/design/task issues, recommended remediation |
| `architecture` | `architecture-*.md`, `architecture-review-*` | рекомендуемые изменения design/spec/tasks/ADR, alternatives |
| `explore` | `explore-summary-*`, `Explore Summary`, `Decisions`, `Open questions` | сформулированные требования, slice hints, unresolved questions |
| `code-sync` | флаг `--code-sync`, `phantom-symbol`, расхождения `design/tasks/debug` с фактическим кодом | фактические символы, устаревшие рецепты, какие артефакты догнать до кода |
| `other` | markdown/text без явных маркеров | факты и open questions; если непонятно — AskQuestion |

Если файл содержит несколько типов (например raw review + reasoning appendix) — извлечь все, но в брифе отделить факты от рекомендаций.

---

## Workflow Steps

### 1. Resolve change

- Проверить, что `openspec/changes/<name>/` существует и не находится в `archive/`.
- Если change не найден — спросить пользователя или предложить `/opsx:ff <name>`.
- Вывести `Using change: <name>` и способ переопределения.

### 2. Load context

- Прочитать `proposal.md`, `design.md`, `tasks.md`, `specs/**`.
- Прочитать `openspec/project.md` и извлечь пути cf/cfe (для возможного architect/explorer).
- Прочитать явно переданные source-файлы.
- Не читать BSL/XML для анализа логики на этом шаге.

### 3. Prepare and show brief

- Сопоставить вход с текущим scope change.
- Определить тип изменения:
  - новое требование;
  - уточнение существующего требования;
  - пересмотр архитектурного решения;
  - постановочный дефект по результатам review/debug/verify;
  - перенос open question в решение.
- Для `--code-sync`: перечислить потенциальные drift-точки без чтения BSL/XML: имена процедур из `tasks.md`/`debug.md`, отчёты writer/reviewer/explorer, файлы `src/**`, которые потребуется прочитать через `onec-code-explorer` после подтверждения.
- Показать бриф и остановиться до подтверждения.

### 4. Ambiguity Gate

После подтверждения, но до правок, задать `AskQuestion`, если неясно:

- менять существующий `Requirement` или добавить новый;
- inside-slice, fix-срез или новый срез;
- принимать рекомендацию review/architecture или оставить как rejected/deferred;
- требуются ли изменения specs;
- считать source finding дефектом кода, постановки или ложным срабатыванием.

### 5. Architect Gate

Проверить `.cursor/rules/architect-gate.mdc`.

Architect обязателен, если:

- source содержит `ARCHITECTURE` finding;
- предлагается изменить точку расширения (`&Перед`, `&После`, `&Вместо`, `&ИзменениеИКонтроль`);
- меняется контракт/export/API;
- требуется новый объект метаданных;
- есть несколько альтернатив реализации без выбранного решения;
- пересматривается уже зафиксированный `design.md` approach;
- решение затрагивает 2+ файла или UX-сценарий.

Для `--code-sync` architect **не обязателен**, если не меняется Behavior Contract / ADR / точка расширения, а артефакты только догоняют фактический код. Если фактический код вводит новый подход (новая точка перехвата, новый контракт, сосуществование расширений), проверить обычные триггеры выше.

Перед вызовом architect:

- выполнить ADR Discovery по `openspec/adrs/`;
- выполнить KB Discovery по `openspec/knowledge/_index.yaml` / `_taxonomy.yaml`, если файлы есть;
- передать `## Existing Knowledge` по правилам проекта.

Сохранить полный отчёт в `openspec/changes/<name>/reports/architecture-extend-YYYY-MM-DD.md`.

Если пользователь явно отказался от architect — записать отказ в `debug.md` / `reports/extend-decision-*.md` и продолжать только если правила допускают отказ.

### 6. Artifact update rules

Порядок правок:

1. `proposal.md` — если меняется scope / Why / What Changes / Impact.
2. `specs/**/spec.md` — delta spec (`ADDED`, `MODIFIED`, `REMOVED`), минимум один Scenario на Requirement.
3. `design.md` — `Existing Mechanisms`, `Design Rationale`, `Decisions`, `Slices`, `Risks`, `Open Questions`.
4. `tasks.md` — slice-aware вставка:
   - непринятый срез → inside-slice перед `S<N>.T<M>`;
   - принятый срез → fix-срез;
   - новая функциональность → новый срез или расширение непринятого, только после Ambiguity Gate;
   - legacy → подходящая секция или «Рефакторинг и качество».
5. `debug.md` — секция `## Extend — YYYY-MM-DD`:
   - источник (`--from-review`, `--from-debug`, ...);
   - что добавлено/изменено;
   - disposition по findings: `accepted`, `rejected`, `deferred`;
   - ссылки на отчёты architect/explorer;
   - следующий шаг.

### 6b. Code-sync update rules (`--code-sync`)

После подтверждения брифа:

1. Делегировать `onec-code-explorer` с точным списком файлов из `tasks.md`/`debug.md`/reports; запросить:
   - реальные процедуры/функции/аннотации;
   - порядок вызовов;
   - расхождения `artifact says` vs `code says`;
   - цитаты `file:line` для каждого вывода.
2. Сохранить полный отчёт в `reports/exploration-code-sync-YYYY-MM-DD.md`.
3. Оркестратор перепроверяет ключевые цитаты точечным `Read` перед правкой артефактов.
4. Обновлять `proposal.md`, `design.md`, `specs/**`, `tasks.md`, `debug.md` так, чтобы они отражали код как source of truth.
5. Если код противоречит Behavior Contract, не «догонять» артефакты молча: остановиться, сформировать decision card (код править через `/opsx:apply` или менять scope через extend).

### 7. Verification Gate

После обновления артефактов:

- проверить, что tasks/spec/design согласованы по названиям срезов и сценариев;
- если specs менялись — пройти Delta Specs Gate;
- если добавлены задачи фикса — проверить defect placement invariant из `vertical-slices.mdc`;
- если запуск был `--code-sync` — выполнить Code-Truth Gate из `.cursor/rules/code-truth-gate.mdc`; `phantom-symbol` после синхронизации = BLOCKER до повторной правки артефактов;
- вернуть пользователю handoff на `/opsx:verify <name>`.

### 8. Handoff

Финальный вывод — T-CONFIRM:

```markdown
**Действие:** Scope change `<name>` обновлён по <source>.

**Изменённые файлы**
1. `openspec/changes/<name>/proposal.md`
2. `openspec/changes/<name>/design.md`
3. `openspec/changes/<name>/tasks.md`

**Следующий шаг:** `/opsx:verify <name>` — проверить согласованность обновлённого scope; затем `/opsx:apply <name>` для реализации.
```

Если изменения не внесены из-за неоднозначности — T-CONFIRM с результатом «требуется решение пользователя» и 2–3 вариантами.

---

## Integration

- `command-skill-gate.mdc`: первым tool call при `/opsx:extend` должен быть Read этого скилла.
- `command-session-persistence.mdc`: протокол extend действует на каждом follow-up ходе.
- `bsl-write-guard.mdc` / `1c-agent-delegation.mdc`: extend не реализует BSL и не вызывает writer/reviewer.
- `1c-xml-write-guard.mdc`: extend не правит XML метаданных.
- `openspec-specs-gate.mdc`: при изменении specs соблюдать delta-формат.
- `vertical-slices.mdc`: все изменения `tasks.md` slice-aware.
- `code-truth-gate.mdc`: `--code-sync` — штатный remediation path для `phantom-symbol` и drift code↔artifacts.
- `verified-cause-gate.mdc`: если вход — defect/RCA, разделять Verified facts и Hypotheses.
- `preserve-subagent-reports.mdc`: сохранять полные отчёты architect/explorer.

---

## Common Follow-up Recommendations

Команды семейства `/opsx:*` должны ссылаться на extend, когда вывод показывает необходимость изменить scope:

- `/review`: `Architecture findings` или findings, противоречащие `design.md` → `/opsx:extend <name> --from-review <report-path>`.
- `/opsx:debug`: RCA показывает постановочный дефект → `/opsx:extend <name> --from-debug <debug-path>`.
- `/opsx:verify`: Phase B требует решения по scope/design/tasks → `/opsx:extend <name> --from-verify <report-path>`.
- `/opsx:apply`: реализация выявила scope mismatch → `/opsx:extend <name>`.
- `/opsx:explore`: есть активный change и обсуждение даёт новое требование → `/opsx:extend <name>`.
