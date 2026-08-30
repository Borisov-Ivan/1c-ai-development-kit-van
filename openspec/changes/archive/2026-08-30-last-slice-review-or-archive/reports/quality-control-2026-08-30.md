# Quality Control — last-slice-review-or-archive

Date: 2026-08-30  
Report: `quality-control-2026-08-30.md`  
Mode: **proposed-slice** (`design.md` `## Slices`; `tasks.md` **не существует**)  
Scope (prompt): criteria **1, 3, 5, 5b, 8, 8b, 9, 10, 11** from `.cursor/rules/vertical-slices.mdc` QUALITY CONTROLLER — SLICE COHERENCE, Slice Generation Gate `/opsx:new`  
Also filled (output format): independence, dependency graph, rework, task readability (N/A)  
Out of scope: исполнимость приёмки «прямо сейчас» на живой сессии / ИБ; тестовые данные; эталоны ИБ; качество кода и выбор варианта A

Context: kit-only change (скилл реализации, памятка ревью, дельта `chat-surface-clarity`). Продуктовый `src/**` / `.bsl` не требуется. `form_mode: n/a`. Приёмка — чат kit, не прикладная конфигурация. **`no-slices` not emitted as a blocker:** оценивается предложенная декомпозиция в `## Slices`. Критерий 8 — смысловое суждение, без grep по спискам слов. Критерий 8b — ложная граница → сливать, не откладывать.

Sources: `proposal.md`, `design.md` (`## Slices`), `specs/chat-surface-clarity/spec.md` (8 `#### Scenario:`), `.cursor/rules/vertical-slices.mdc`, `.cursor/rules/task-readability.mdc`. Cross-check: `reports/architecture-2026-08-30.md` (not a second SoT).

Mechanical pre-check (prompt): none. Manual config checklist: none. User Task Contract pre-check: none.

Repository (prompt): `.cursor/skills/openspec-apply-change/SKILL.md` и `.cursor/docs/review-guide.md` существуют.

## Verdict

`OK`

Один предложенный срез вертикален, самодостаточен и не является foundation+gate. Primary — наблюдаемый чат после «принято» на последнем срезе: три слова, затем `ревью` даёт команду предрелиза, каталог ЗНИ на месте. Все восемь сценариев дельты размещены. Отдельный срез «памятка» отвергнут в `## Slices` — это закрывает ложную границу (критерии 8b и 9). Объединение срезов не требуется.

## Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1: Развилка после последнего среза | После «принято» на последнем срезе ЗНИ с кодом расширения — три слова; `ревью` даёт команду предрелиза; архив и стоп как сегодня | ещё нет (`tasks.md` отсутствует); слои по design: скилл реализации, памятка ревью | S1.accept предложен (1 mandatory Primary + optional / S1.M); **8/8** Scenario из дельты размещены | нет | предложен один accept на границе среза; маркер `<!-- slice-gate -->` в design нет (формат `tasks.md`; см. критерий 5) |

Notes:

- Порог: Lite / нижняя граница Standard (два файла, три точки в скилле + строка памятки; ожидаемо ≤5–8 задач). По `vertical-slices.mdc` § ТРИГГЕРЫ — **1 срез по умолчанию**. Второй срез не обоснован: один самостоятельный исход (развилка в чате). Согласовано с `## Slices`: «Отдельный срез „памятка“ без развилки в чате не принимается самостоятельно».
- `form_mode: n/a`. Продуктовый BSL / Form / XML не требуется.
- Архитектурные фазы 1–3 (`architecture-2026-08-30.md`) — группы работ внутри S1, не отдельные срезы; QC их не штрафует.
- `**Режим apply:**` в design не указан; для kit markdown допустим `mechanical` на этапе генерации `tasks.md` — вне запрошенных критериев.
- Колонка «Scenarios из spec» в первой таблице = «см. матрицу ниже». Имена Scenario живут в таблице покрытия — покрытие есть; при генерации `tasks.md` поле `**Связь со spec:**` SHALL перечислить все восемь имён буквально (SUGGESTION).

## Scenario Coverage

8 `#### Scenario:` в `openspec/changes/last-slice-review-or-archive/specs/chat-surface-clarity/spec.md`. Capability: `chat-surface-clarity` (ADDED, одно требование).

| Scenario | Covered by (proposed) | Status |
|---|---|---|
| Последний срез — развилка из трёх слов | S1 Primary (Given/When того же пути) | OK — covered-by-Primary |
| Ответ ревью даёт команду предрелиза | S1 Primary (Then того же пути: `ревью` → команда, ЗНИ активна) | OK — covered-by-Primary |
| Ответ архив без изменений | S1 optional / S1.M | OK — covered-by-optional |
| Ответ стоп без изменений | S1 optional / S1.M | OK — covered-by-optional |
| Без кода расширения слова ревью нет | S1 optional / S1.M | OK — covered-by-optional |
| Возврат в сессию — та же развилка | S1 optional / S1.M | OK — covered-by-optional |
| Карточка завершения — та же развилка | S1 optional / S1.M | OK — covered-by-optional |
| Проверка постановки после apply не меняется | S1 задача сверки шаблона (agent static / «по тексту») | OK — covered-by-task (implementation-only / инвариант «не менять»; не отдельный accept) |

Имена в таблице «Покрытие Scenarios» совпадают с заголовками `#### Scenario:` буквально. Пропусков нет. `accept-bullets-missing-scenario` **не** эмитируется.

Implementation-only путь для «Проверка постановки после apply не меняется» согласован с Non-Goals п.1 и proposal Out of scope: слот не правится, агент сверяет шаблон проверки постановки. User IB/runtime spike в середине среза не заявлен.

Два spec-сценария в Primary («развилка из трёх слов» и «ответ ревью») — **шаги одного** user-journey (принять → увидеть три слова → ответить `ревью` → увидеть команду), не два blocking-прохода. См. критерий 10.

## Dependency Graph

```mermaid
flowchart LR
  S1[S1 Развилка после последнего среза]
```

- Cycles: none.
- Forward acceptance dependencies: none (единственный срез; критерий 8b не срабатывает механикой пары S1/S2).
- Undeclared predecessors: none (`### Граф зависимостей`: S1 → нет).
- Intra-slice (projected, по Migration Plan / архитектору): формулировка развилки в скилле реализации (ручная приёмка) → ветка «принят» при возврате в сессию → карточка «реализация завершена» → строка в памятке ревью → сверка шаблона проверки постановки (без правки) → `S1.accept`. Цикла нет. Соседние ЗНИ про карту сценария в граф не входят (proposal Out of scope).

## Criterion 8b — Primary достижим силами этого среза

Пары соседних срезов нет. Семантика: каждый элемент обязательного осмотра имеет включающий слой в заявленных файлах S1.

| Элемент Primary | Слой того же среза (design / architecture) | Достижимость |
|---|---|---|
| Принять последний срез фразой «принято» | скилл реализации, хук ручной приёмки | да, тот же S1 |
| В чате три слова, ничего не заархивировано | та же формулировка развилки; условие показа через уже считаемый признак кода расширения | да |
| Ответить `ревью` | разбор трёх ответов в том же скилле | да |
| Одна команда предрелиза, каталог ЗНИ на месте | печать команды и завершение сессии реализации; предрелиз не стартует | да |

Наблюдаемый исход не заимствован у более позднего среза. Памятка ревью **не** входит в Then Primary: строка проверяется вместе с чатом (явный отказ от отдельного среза). Возврат в сессию и карточка завершения — другие входы в **ту же** развилку; вынос в S2 дал бы дубль journey → ложная граница. Сейчас оба в optional S1. Верно.

Нужда в «чужой» ЗНИ с кодом расширения как фикстуре прогона — **transient** (среда приёмки), не structural unreachability внутри среза. Не эмитируется как 8b.

`slice-accept-not-self-achievable` **не** эмитируется. Объединение срезов не требуется: декомпозиция уже один срез. Запрещённое «процедурно не подписывать accept до следующего среза» не предлагается.

## Criterion 10 — один обязательный осмотр или несколько?

В матрице приёмки **один** mandatory-буллет: принять последний срез → три слова → `ревью` → команда предрелиза, ЗНИ активна. Optional / S1.M: без кода расширения; возврат в сессию; карточка завершения; `архив` и `стоп`.

Сплетение «три слова + ответ ревью» — **один осмотр одной сессии реализации**, не два обязательных прохода:

1. Given: ЗНИ с кодом расширения, последний срез.
2. When: принять фразой «принято», затем ответить `ревью`.
3. Then (тот же ход/сессия): в чате были три слова, каталог не уехал в архив; после `ревью` — одна команда предрелиза.

Это не несколько journey: нет второго экрана, нет второго Given «другая ЗНИ» в mandatory Then. Имена двух Scenario в одном Then — покрытие связанных сценариев одним путём (как «включить флаг → сохранить → переоткрыть»).

Секция «Критерии приёмки по срезам» в одном SHALL дописывает «без кода расширения слова `ревью` нет». Это **не** второй mandatory в матрице: матрица относит путь без расширения в optional. Риск при генерации tasks — скопировать весь SHALL в два+ обязательных буллета (SUGGESTION).

`acceptance-simplicity-overload` **не** эмитируется. Разворачивать восемь имён в восемь обязательных буллетов **запрещено** remediation критерия 10.

## Checklist Results

| # | Criterion | Result |
|---|---|---|
| 1 | Scenario Coverage | **Pass** — 8/8. Primary (2 имени как шаги одного пути) / optional (5) / agent-сверка шаблона (1). User runtime только на границе `S1.accept` (projected) |
| 2 | Slice Independence | **Pass** (информативно, не в запросе) — принимать S1 можно без несуществующего S2+ |
| 3 | Slice Completeness | **Pass** — слои kit, нужные для Primary «принято → три слова → `ревью` → команда», в колонке «Файлы» названы: скилл реализации (развилка, разбор ответов), памятка ревью (совпадение формулировки; не слой Then, но в том же срезе). Три точки скилла (ручная приёмка, возврат, карточка) — один файл; для optional-входов слой тот же, не дыра. Шаблон проверки постановки **не** слой реализации (инвариант «не менять») — сверка, не пропуск. Метаданных/форм 1С нет и не требуется. Целевые файлы в репозитории есть |
| 4 | Slice Dependency Graph | **Pass** (информативно) — S1 → нет |
| 5 | Slice Gate Integrity | **Pass (projected)** — предложен **ровно один** `S1.accept`. Дубля нет. Маркер `<!-- slice-gate -->` — артефакт `tasks.md`, в `## Slices` его нет по формату design; **не** эмитирован CRITICAL (нет `# Срез` в tasks). При генерации tasks — ровно один accept + один маркер (SUGGESTION). `legacy-acceptance-format` N/A |
| 5b | Acceptance Checklist Coverage | **Pass** — Primary в колонке таблицы и в матрице есть → `primary-acceptance-missing` не срабатывает. Тела `S1.accept` ещё нет → `accept-checklist-empty` N/A (hint: первый sub-bullet = `**Primary (обязательно):**` из матрицы). `accept-bullet-foreign-scenario` N/A (один срез). `accept-bullets-missing-scenario` нет (8/8) |
| 6 | Rework Risk | **Pass** (информативно) — один срез снимает риск «принята развилка без памятки» или «принята памятка без чата». Три входа в одну формулировку — намеренно в одном срезе; не rework между срезами |
| 8 | Slice Verticality | **Pass** — mandatory Primary: принять последний срез в чате реализации → увидеть три слова, ЗНИ не в архиве → ответить `ревью` → увидеть одну команду предрелиза. Это black-box (чат kit как продукт), не вызов функции в отладчике / код-ревью контракта API. Programmatic (сверка скилла и шаблона проверки постановки) вынесены из Primary в колонку «Приёмка» / задачу агента — верно. Отдельный срез «только памятка» был бы невертикален; он отвергнут |
| 8b | Self-Achievable Acceptance | **Pass** — нет пары S1/S2. Наблюдаемый исход не заимствован у более позднего среза. Все включающие слои Primary (хук приёмки, условие показа, разбор `ревью`) заявлены в том же S1. Отказ от среза «памятка» закрывает этот критерий |
| 9 | Foundation slice with gate | **Pass** — нет S_k с programmatic accept и зависимого S_k+1 с UX. Черновик «срез памятка» отвергнут в `## Slices` со ссылкой на отсутствие самостоятельной приёмки |
| 10 | Acceptance Simplicity | **Pass (projected)** — задуман **один** mandatory black-box journey. Два Scenario happy-path — шаги одного Then. Optional не помечены обязательными. Риск: SHALL среза и восемь имён матрицы покрытия развернуть в несколько mandatory sub-bullet → тогда сработает overload (SUGGESTION) |
| 11 | User Task Contract | **Pass (projected)** — строк `S<N>.<M>` нет, DENY-grep не к чему применить. Prompt: mechanical / user-task pre-check = none. Приёмка «ручной прогон чата» стоит на границе среза (колонка «Приёмка» / Assumptions п.3) — **допустимо** в `S1.accept`. «Сверка текста скилла» заявлена рядом с прогоном; при генерации это **задача агента** (по тексту), не user-spike в середине среза. CRITICAL не ставить до появления запрещённых формулировок в tasks |

Task readability: **N/A** — нет `- [ ] S1.<M>`. Критерий 7 не в запросе; при генерации tasks действует `.cursor/rules/task-readability.mdc`.

## Alerts

**CRITICAL / WARNING:** нет.

### 1. `slice-gate-pending-tasks`

- affected: S1 (generation of `tasks.md`)
- alert type: (informational for criterion 5; not in the removed-alert list)
- severity: `SUGGESTION`
- evidence: `## Slices` задаёт один `S1.accept` и критерии приёмки; HTML-маркер конца среза в design не пишется.
- recommendation: в `tasks.md` — `# Срез S1: Развилка после последнего среза`, блок метаданных с `**Primary acceptance:**` из таблицы, `**Связь со spec:**` со всеми восемью именами буквально, ровно один `- [ ] S1.accept …` с `**Primary (обязательно):**` из матрицы, затем `<!-- slice-gate: после «принято» на последнем срезе ЗНИ с кодом расширения в чате три слова; ревью даёт команду предрелиза, ЗНИ активна -->`.

### 2. `acceptance-simplicity-guard`

- affected: S1.accept (projected)
- alert type: профилактика критерия 10 (`acceptance-simplicity-overload`)
- severity: `SUGGESTION`
- evidence: Primary одним предложением закрывает развилку и ответ `ревью` (два Scenario — один путь). SHALL среза дописывает путь без кода расширения. Матрица покрытия помечает все восемь имён как S1.
- recommendation: в теле `S1.accept` оставить **один** mandatory sub-bullet: ЗНИ с кодом расширения → «принято» на последнем срезе → три слова, каталог на месте → `ревью` → `/release-review <имя>`, ЗНИ активна. «Без кода расширения…», «Возврат в сессию…», «Карточка завершения…», «Ответ архив…», «Ответ стоп…» — «(опционально)». «Проверка постановки после apply не меняется» — `S1.<M>` «верифицировать по тексту шаблона», не буллет accept. Имена двух шагов happy-path не превращать в две строки без пометки «опционально».

### 3. `user-task-contract-guard`

- affected: будущие `S1.<M>`
- alert type: профилактика критерия 11
- severity: `SUGGESTION`
- evidence: колонка «Приёмка» = ручной прогон чата + сверка текста скилла; Assumptions п.3 — прогон на ЗНИ с кодом расширения и на kit-only. DENY-маркеров в design нет.
- recommendation: живой прогон реализации (фраза «принято», ответ `ревью` / `архив` / `стоп`, возврат в сессию, карточка завершения, ЗНИ без кода расширения) держать только в `S1.accept`. Правки markdown и «верифицировать по тексту скилла / памятки / шаблона проверки постановки» — агентские `S1.<M>` (ALLOW-agent). Не писать в `S1.<M>` «на стенде», «на тестовой ИБ», «runtime-verify», «в консоли», условные «после verify».

### 4. Completeness — явные задачи слоёв

- affected: S1 task generation
- alert type: профилактика критерия 3
- severity: `SUGGESTION`
- evidence: колонка «Файлы» достаточна семантически; архитектор перечисляет три точки в `openspec-apply-change/SKILL.md` (ручная приёмка; ветка «принят»; карточка завершения) и одну строку в `review-guide.md`. Шаблон проверки постановки — сверка без правки.
- recommendation: в группах S1 до accept явно закрыть: (1) единая формулировка развилки и разбор трёх слов в скилле реализации; (2) возврат в сессию на ту же развилку, если срез последний; (3) карточка завершения при коде расширения печатает ту же развилку; (4) строка в памятке ревью; (5) агент: слот следующего шага проверки постановки после apply по-прежнему команда архива.

### 5. `spec-link-literal-names`

- affected: metadata S1 в будущем `tasks.md`
- alert type: профилактика 5b / читаемости accept
- severity: `SUGGESTION`
- evidence: колонка «Scenarios из spec» = «см. матрицу ниже», а не перечень имён.
- recommendation: в `**Связь со spec:**` перечислить восемь имён как в spec. В optional-буллетах `S1.accept` имена в ёлочках — буквально.

**Не эмитировано:** `no-slices`; `primary-acceptance-missing`; `accept-checklist-empty`; `accept-bullets-missing-scenario`; `accept-bullet-foreign-scenario`; `slice-not-vertical`; `slice-accept-not-self-achievable`; `slice-foundation-with-gate`; `acceptance-simplicity-overload`; `user-task-contract-violation`; `legacy-acceptance-format`; `deprecated-phase-gate`.

## Recommendations

**Automatic fix**

Нет обязательной правки `design.md` до генерации `tasks.md`. Покрытие 8/8, один срез, Primary заполнен.

**Tasks generation**

1. Один `# Срез S1`, один `S1.accept` с одним mandatory Primary, `<!-- slice-gate -->`.
2. Optional / agent для остальных шести Scenario (пять optional-входов + сверка шаблона).
3. Глагол + файл + результат в `S1.<M>` (`.cursor/rules/task-readability.mdc`).

**Decision required**

Нет. Критерий 8b / объединение срезов не требуется: декомпозиция уже один срез. Переписывать Primary на другой путь не нужно.

**Do not**

- Не вводить второй срез «памятка», «возврат в сессию» или «карточка завершения» (критерии 8b и 9: тот же исход, другие входы).
- Не ставить два+ mandatory black-box journey в `S1.accept`.
- Не откладывать `S1.accept` «пока не будет S2».
- Не класть живой прогон чата в `S1.<M>` как обязанность пользователя.
