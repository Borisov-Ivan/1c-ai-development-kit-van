---
name: openspec-extend-change
description: Controlled scope extension for an existing OpenSpec change. Reads user text and optional source reports/files, shows a mandatory brief, updates change artifacts only after confirmation, then hands off to verify/apply.
license: MIT
compatibility: Does not call writer/reviewer and never edits BSL/XML metadata. May delegate read-only analysis to onec-code-architect / onec-code-explorer when gates require it.
metadata:
  author: project
  version: "1.1"
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
  - `--from-report <path>` — `openspec/sessions/<slug>/analysis.md` (итог `/opsx:explore`; RCA, рецепт, fix-задачи)
  - `--from-explore <path>` — legacy Explore Summary (`temp/explore-summary-*.md`)
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
4. Прочитать `openspec/project.md` и артефакты change из `contextFiles`: `proposal.md`, `design.md`, `tasks.md`, `specs/**` при наличии; для расширения scope также прочитать `debug.md` (если есть) — нужен для счётчика Scope Coherence Audit и записей `## Extend`.
5. Прочитать только явно переданные source-файлы (`--from-*`, `@path`, пути в запросе). Трассы — через `/opsx:explore` (профиль bug). `--from-report` принимает `openspec/sessions/<slug>/analysis.md` (замена capture из удалённого `/opsx:debug`). Если указан `--code-sync`, source = артефакты change + `debug.md` + отчёты `reports/**` + результаты Code-Truth Gate; чтение BSL/XML до брифа всё равно запрещено.
5a. Для секции **KB в scope** брифа: прочитать `openspec/knowledge/_index.yaml` и при необходимости `_taxonomy.yaml` и выбранные KB `.md` — по алгоритму Entry Protocol шаг 1.5 `.cursor/skills/openspec-explore/SKILL.md` (anchor-paths из путей в уже прочитанных артефактах и source-файлах; бюджет Top-10; при отсутствии совпадений — «нет совпадений по anchor-paths и домену» или «Discovery не требовался» при явном отсутствии релевантных путей).
6. Сформировать и показать **бриф extend** по шаблону ниже.
7. **END TURN.** До подтверждения пользователя запрещены: запись артефактов, вызовы writer/reviewer, вызовы architect/explorer, чтение BSL/XML для анализа логики.

Разрешённые действия до брифа: чтение этого скилла, `openspec list --json`, `openspec instructions apply --json`, чтение `project.md`, чтение артефактов change, чтение явно переданных markdown/text/source-report файлов, чтение `openspec/knowledge/_index.yaml` / `_taxonomy.yaml` и выбранных KB `.md` только для поля «KB в scope» (шаг 5a).

### Шаблон брифа (T-BRIEF)

Единый каркас — `.cursor/docs/opsx-output-style.md` §5.1 в **чате**. Заголовок: `## Бриф: /opsx:extend | change: <name>`. Файлы `temp/briefs/*.md` не создаются.

**Обязательные секции §5.1:** Контекст; Что я понял; **KB в scope** (Discovery по anchor-paths из артефактов change и source-файлов или явное «нет совпадений / Discovery не требовался»); **План**; **Подтвердить?**

**Дополнительно для extend (всегда в том же сообщении, после опциональных секций §5.1):**

```markdown
**Предлагаемое изменение артефактов**
1. `proposal.md`: …
2. `design.md`: …
3. `specs/**`: …
4. `tasks.md`: …
5. `debug.md`: …

**Соответствие исходному scope**
- Усиливает пункт Why: …
- Затрагивает Non-Goals: yes / no — …
- Меняет Behavior Contract: yes / no — …
- Отменяет архивный инвариант: yes / no — …
- Drift-check: pass / drift-warning / scope-violation
```

Секция **План** того же сообщения (после блоков выше или до них — на усмотрение, но один раз): 1) уточнить неоднозначности через AskQuestion при необходимости; 2) проверить гейты архитектуры и факты в коде; 3) при `--code-sync` — после подтверждения делегировать исследователя кода и сохранить `reports/exploration-code-sync-YYYY-MM-DD.md`; 4) обновить артефакты change; 5) передать на `/opsx:verify <name>`. Завершить **Подтвердить?** по §5.1.

Self-check перед выводом: слои разделены; в UX-полях §5.1 нет `S<N>.T<M>` / `D<N>` / номеров задач; списки нумерованы; поле **Вход** / **Факты** — только факты; каждое поле ≤3 строк или ≤7 пунктов; **KB в scope** присутствует; блок **«Соответствие исходному scope»** заполнен всеми **пятью** строками (Why, Non-Goals, Behavior Contract, Отменяет архивный инвариант, Drift-check).

**Развилки в чате после брифа:** любые варианты выбора до или после подтверждения (AskQuestion, неоднозначный `Drift-check` и т.п.) выводить блоками **«Решение N — …»** с метками `<N>a` / `<N>b` / `<N>c` по образцу `.cursor/skills/openspec-verify-change/templates/chat-summary.md`, чтобы пользователь мог ответить одной строкой; варианты **в чате**, не только в длинном теле брифа.

### Соответствие исходному scope — критерии заполнения (оркестратор)

Источник правды: текущие `proposal.md` (`## Why`, `## What Changes`) и `design.md` (`## Behavior Contract`, `## Goals / Non-Goals`).

**Затрагивает Non-Goals: yes** — предлагаемое изменение явно описывает или подразумевает действие, перечисленное или запрещённое в `## Non-Goals` design.md.

**Меняет Behavior Contract: yes** — предлагается добавить новый пункт в `## Behavior Contract`, удалить существующий пункт или изменить формулировку пункта так, что меняется наблюдаемое поведение (не просто уточнение терминологии).

**Drift-check:**
- `pass` — ответ **no** по Non-Goals и Behavior Contract **и** «Отменяет архивный инвариант: **no**» **и** «Усиливает пункт Why» указывает конкретный пункт `## Why` (не «не относится напрямую»).
- `drift-warning` — `Затрагивает Non-Goals: yes` **или** `Меняет Behavior Contract: yes` **или** «Усиливает пункт Why: не относится напрямую» **или** осознанное расширение при сохранении архивных контрактов (Behavior Contract меняется, но инвариант не отменяется — пояснить в брифе).
- `scope-violation` — любое из: оркестратор не находит ни одного пункта Why, который усиливается предлагаемым изменением, **и** при этом хотя бы одно из полей Non-Goals / Behavior Contract = **yes**; **или** `Отменяет архивный инвариант: **yes**` при отсутствии заполненной секции `## Blast Radius` в `design.md` (нет таблицы контракт / источник / бизнес-эффект / альтернативы / обоснование). В этом случае **не** использовать `drift-warning` — только `scope-violation`.

Если классификация неоднозначна до подтверждения брифа — `AskQuestion` с тремя вариантами итогового `Drift-check`: `pass` / `drift-warning` / `scope-violation`; результат отразить в брифе.

---

## Per-turn Delegation Gate

На каждом follow-up ходе:

1. Если запрос требует обследования кода, трассировки вызовов, проверки метаданных или анализа 3+ модулей — не читать `.bsl`/XML самостоятельно.
2. Сформировать бриф и делегировать:
   - `onec-code-explorer` — для обследования кода;
   - `onec-code-architect` — для выбора/пересмотра подхода;
   - `onec-trace-analyst` не используется в extend; трассы перенаправлять в `/opsx:explore` (профиль bug).
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
| `report` | `openspec/sessions/*/analysis.md`, секции RCA / Verified facts / Рекомендации / Fix tasks | root cause, verified facts, рецепт, задачи для `debug.md` и `tasks.md`, slice placement |
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

- Прочитать `proposal.md`, `design.md`, `tasks.md`, `specs/**`, `debug.md` (если существует).
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
- Заполнить блок **«Соответствие исходному scope»** по критериям из секции под шаблоном T-BRIEF (сопоставить предлагаемые изменения с `## Why`, `## Non-Goals`, `## Behavior Contract`).
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

#### 5a. Scope Coherence Audit (режим `scope-coherence-audit`)

Цель — обнаружить расползание ЗНИ (scope drift) до дорогого `/opsx:verify`. Отчёт: `reports/architecture-extend-coherence-YYYY-MM-DD.md`. Шаблон промпта: `.cursor/skills/1c-agent-patterns/architect.md`, секция **Architect — scope coherence audit (extend)**.

**Триггер 1 (семантический, из брифа):** в блоке «Соответствие исходному scope» зафиксирован `Drift-check: drift-warning` или `Drift-check: scope-violation`.

**Триггер 2 (объективный, счётчик Extend без архитектора):**

1. Выполнить по `openspec/changes/<name>/debug.md`:
   ```bash
   rg -c "Architect Gate:\\s*(не вызывался|не требовался|declined|—)" debug.md
   ```
   Обозначить результат как **M**.

2. Выполнить `Glob` по `openspec/changes/<name>/reports/architecture-extend-coherence-*.md`.

3. Триггер 2 срабатывает, если **M ≥ 3** и выполняется одно из условий:
   - файлов `architecture-extend-coherence-*.md` **нет**;
   - **или** дата из заголовка последней секции `## Extend — YYYY-MM-DD` в `debug.md` (парсинг ГГГГ-ММ-ДД из строки заголовка) **строго новее** даты из имени новейшего файла `architecture-extend-coherence-*.md` (по дате в суффиксе имени).

Примечание: **M** — число строк в `debug.md`, где поле `Architect Gate:` совпадает с шаблоном «Extend без архитектора» (маркеры выше); это приближение к числу секций `## Extend —`, после которых архитектор не вызывался.

**Если сработал Триггер 1 или Триггер 2:**

**Грейс-исключение (антидубль):** если в ответ на **этот же** подтверждённый бриф уже записан файл `reports/architecture-extend-coherence-YYYY-MM-DD.md`, повторный Scope Coherence Audit до завершения handoff не вызывать. Следующий прогон `/opsx:extend` — новый бриф, грейс не действует.

**Если грейс не применим:**

1. Выполнить ADR Discovery и KB Discovery (как ниже для обычного architect).
2. Вызвать `Task(subagent_type="onec-code-architect")` с `mode=scope-coherence-audit` и шаблоном из `1c-agent-patterns/architect.md`. Оркестратор передаёт блок «Соответствие исходному scope» из брифа, полные тексты артефактов, при наличии — фрагмент исходного `proposal.md` из git (`git show <hash>:openspec/changes/<name>/proposal.md`, где `<hash>` — коммит создания change или первый коммит с каталогом change; если недоступно — явно указать в промпте «исторический proposal недоступен»).
3. Сохранить полный отчёт в `openspec/changes/<name>/reports/architecture-extend-coherence-YYYY-MM-DD.md`.
4. Добавить в `debug.md` запись:
   ```markdown
   ## Extend Coherence Audit — YYYY-MM-DD

   - Триггер: semantic | counter | both
   - Drift-check из брифа: pass | drift-warning | scope-violation
   - Вердикт архитектора: coherent | drift-warning | scope-violation
   - Отчёт: `reports/architecture-extend-coherence-YYYY-MM-DD.md`
   - Решение пользователя: accepted recommendations | partial | rejected — <кратко>
   ```
   Поле «Решение пользователя» заполняется после `AskQuestion`, если вердикт архитектора требует решения.

**Если вердикт архитектора в отчёте — `scope-violation`:** до обновления остальных артефактов остановиться и через `AskQuestion` предложить: (a) принять рекомендации архитектора (например отделить часть в новую ЗНИ через `/opsx:ff`), (b) отклонить и зафиксировать риск в `debug.md`, (c) свернуть extend без правок.

Simplicity Check для режима `scope-coherence-audit` **не требуется** (см. `.cursor/rules/architect-gate.mdc`).

---

Architect обязателен также по общим правилам Gate (ниже). Обычный отчёт расширения без coherence сохранять в `reports/architecture-extend-YYYY-MM-DD.md`, если вызывается архитектор по классическим триггерам **после** или **вместо** coherence — не дублировать два полных прохода без необходимости; при одновременном срабатывании 5a и классических триггеров достаточно **одного** вызова с приоритетом шаблона **scope coherence audit**, если пользователь не запросил явно отдельное архитектурное решение по API/перехватам.

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

Если архитектор вызывался **только** по п. 5a (Scope Coherence Audit), полный отчёт уже сохранён в `reports/architecture-extend-coherence-YYYY-MM-DD.md`. Иначе сохранить полный отчёт расширения в `openspec/changes/<name>/reports/architecture-extend-YYYY-MM-DD.md`.

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
- следующий шаг для пользователя: `/opsx:verify <name>` (не дублировать в чат длинный handoff — см. п. 8).

### 8. Handoff

Финальный вывод в **чат** — **§3a** [`.cursor/rules/chat-output-budget.mdc`](../../rules/chat-output-budget.mdc):

- Если после подтверждения брифа **нет** изменений ни в одном артефакте (`proposal` / `design` / `specs` / `tasks` / `debug`) — **одна строка:** «Артефакты ЗНИ соответствуют запросу, правок не потребовалось.» Без `Drift-check: OK`, без перечня проверенных файлов.
- Если артефакты **изменены** — **одна строка:** «Обновлено: `<path1>`[, `<path2>`…]. Дальше: `/opsx:verify <name>`.»

Полный перечень правок, цитаты и заметки — в `debug.md` (`## Extend — YYYY-MM-DD`) и при необходимости `reports/extend-summary-<name>-YYYY-MM-DD.md`, **не** в чат.

Если изменения не внесены из-за неоднозначности — краткая карточка с 2–3 вариантами (развилка — исключение из однострочного режима).

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
- `architect-gate.mdc`: scope-drift триггеры и закрытие Gate через `architecture-extend-coherence-*.md` (см. п. 5a).

---

## Common Follow-up Recommendations

Команды семейства `/opsx:*` должны ссылаться на extend, когда вывод показывает необходимость изменить scope:

- `/review`: `Architecture findings` или findings, противоречащие `design.md` → `/opsx:extend <name> --from-review <report-path>`.
- `/opsx:explore` + `analysis.md`: RCA и рецепт → `/opsx:extend <name> --from-report openspec/sessions/<slug>/analysis.md`.
- `/opsx:verify`: Phase B требует решения по scope/design/tasks → `/opsx:extend <name> --from-verify <report-path>`.
- `/opsx:apply`: реализация выявила scope mismatch → `/opsx:extend <name>`.
- `/opsx:explore`: есть активный change и обсуждение даёт новое требование → `/opsx:extend <name>`.
