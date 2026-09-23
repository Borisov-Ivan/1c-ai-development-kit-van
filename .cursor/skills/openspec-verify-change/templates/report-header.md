# YAML frontmatter отчёта verify

Копируется в начало `reports/verification-YYYY-MM-DD.md` (плейсхолдеры заменить):

```yaml
---
verify_mode: <pre-apply | post-apply>
change: <имя-change>
date: YYYY-MM-DD
verdict: <GO | NO-GO>
layer_status:
  layer_1_hygiene: <PASS | AUTOFIXED | FAIL>
  layer_2_internal_coherence: <PASS | WARNING | FAIL>
  layer_2_5_loop_detection: <PASS | acceptance-loop-detected | SKIPPED-override>
  layer_3_problem_solution: <PASS | WARNING | FAIL>
  layer_4_independent_challenge: <APPROVE | CHALLENGE | REJECT | SKIPPED-novelty | SKIPPED-override>
  layer_5_implementation_readiness: <PASS | WARNING | FAIL>
snapshot:
  acceptance_loop_max: 3
  # порог петли приёмки — SSOT .cursor/rules/vertical-slices.mdc § ДЕТЕКТОР ПЕТЛИ ПРИЁМКИ
  repair_attempt: 0
  # счётчик internal repair-from-verify в текущем цикле (см. SKILL.md § Repair Loop)
  accepted_tasks:
    - S1.1
    - S1.accept
  closed_decisions: []
  # agent-only: id (snake_case), summary (prose), closed_at (ISO date), source (verify-user-answer | repair-from-verify)
  open_decision_id: null
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  # full | incremental | lite — см. SKILL.md § verify depth
  assumptions_accepted: []
  open_known_questions: []
  artifacts_mtime:
    proposal.md: "YYYY-MM-DDTHH:mm:ss"
    design.md: "YYYY-MM-DDTHH:mm:ss"
    tasks.md: "YYYY-MM-DDTHH:mm:ss"
    specs/<capability-folder>/spec.md: "YYYY-MM-DDTHH:mm:ss"
  last_challenge_at: "YYYY-MM-DDTHH:mm:ss"  # ISO успешного Layer 4; сравнение оси — по artifact_hashes, не по mtime
  artifact_hashes: {}
  # SHA-256 нормализованного содержимого proposal/design/tasks/specs/** и структурных секций debug
  external_contract_digest: "<sha256>"
  # SHA-256 упорядоченных EC-*, их решений и отпечатков первичных событий
  decision_fingerprints: {}
  # ключ = id закрытого решения; значение = SHA-256(id + closed_at + source)
  rules_versions: {}
  # ключ = путь файла правила; значение = SHA-256 нормализованного файла
  check_cache: {}
  # ключ результата: check_id + scope_anchor + ordered_input_hashes + rules_version + evidence_digest
  invalidation_map: {}
  # check_id → причина инвалидации (артефакт / EC-* / версия правила)
---
```

## Правила полей

### `verify_mode`

Только два значения:

- **`pre-apply`** — есть хотя бы одна `[ ]` задача (включая `S<N>.accept`); реализация не завершена.
- **`post-apply`** — все задачи `[x]`, все `S<N>.accept` приняты.

Узкий охват одного среза, переход между срезами и смешанный режим — **частные случаи `pre-apply`**, выводятся из текста запроса пользователя и состояния `tasks.md`. Отдельных значений `slice-pre`, `slice-post`, `slice-scoped`, `slice-transition`, `legacy-pre`, `legacy-mixed` **нет** — они удалены.

### `verdict`

Только **GO** или **NO-GO**. Бинарный.

- **GO** — безопасно запускать `/opsx:apply`. Допускает Layer 1 автоправки (статус `AUTOFIXED`) и Layer 2/5 WARNING без блокеров.
- **NO-GO** — есть содержательное сомнение в Layer 3 (Problem-Solution Trace), Layer 4 (Independent Challenge с вердиктом CHALLENGE/REJECT) или критический FAIL в любом другом слое. Требуется обсуждение и/или `/opsx:explore` / `/opsx:extend` до повторного verify.

### `layer_status`

Пять полей, по одному на слой. Возможные значения:

- **Layer 1 (Hygiene):** `PASS` (нечего править), `AUTOFIXED` (автоправки применены), `FAIL` (немеханические проблемы формата).
- **Layer 2 (Internal Coherence):** `PASS`, `WARNING` (несущественные несостыковки артефактов), `FAIL` (циклы зависимостей, несовпадение spec ↔ tasks).
- **Layer 2.5 (Loop Detection):** `PASS` (петли нет / уже разобрана редизайном), `acceptance-loop-detected` (петля → NO-GO, запущен `deep-analysis`), `SKIPPED-override` (действующий `.gate-override.yaml gate: acceptance-loop`).
- **Layer 3 (Problem-Solution Trace):** `PASS`, `WARNING` (орфаны без блокера), `FAIL` (Requirement без задач или задача без Requirement).
- **Layer 4 (Independent Challenge):** `APPROVE`, `CHALLENGE`, `REJECT`, `CHALLENGE-saturated`, `SKIPPED-novelty`, `SKIPPED-override`, `SKIPPED-lite`.
- **Layer 5 (Implementation Readiness):** `PASS`, `WARNING` (мелкие GAP реализуемости), `FAIL` (задача не реализуема as-is).

### `snapshot.last_challenge_at`

ISO-метка момента последнего **успешного** прогона Layer 4 (вердикт APPROVE или CHALLENGE с принятым к работе через `--from-verify`). Решение «нужен ли challenge заново» — по **хэшу архитектурной оси** в `artifact_hashes`, не по сравнению одного `mtime` с этой меткой:

- Хэш оси изменился относительно снимка последнего успешного Layer 4 → Layer 4 запускается.
- Хэш оси совпал и нет профильного триггера → Layer 4 пропускается (`layer_status.layer_4_independent_challenge: SKIPPED-novelty`).
- `mtime(design.md)` изменился, хэш тот же → вызов **не** создаётся.

При первом verify по ЗНИ `last_challenge_at` отсутствует → Layer 4 обязателен.

При вердикте REJECT в Layer 4 — `last_challenge_at` **не обновляется**, чтобы повторный verify снова запустил challenge.

### `snapshot.accepted_tasks`

Полный упорядоченный список идентификаторов строк `tasks.md` с `- [x]`. Форматы:

- `S<N>.<M>` — рабочая задача среза N.
- `S<N>.accept` — приёмочная задача среза N (один на срез).
- `F<k>` — Follow-up.

Старый формат `S<N>.T<M>` (несколько приёмочных задач на срез) поддерживается в legacy-режиме — verify читает оба формата, но новые ЗНИ через `/opsx:new` генерируют только `S<N>.accept`.

### `snapshot.acceptance_loop_max`

Порог детектора петли приёмки (Layer 2.5), по умолчанию **3**. SSOT определения метрик `AcceptLoop` / `PatchRounds` и условий закрытия — `.cursor/rules/vertical-slices.mdc` § ДЕТЕКТОР ПЕТЛИ ПРИЁМКИ. Значение переносится из снапшота в снапшот; меняется только осознанно (например, при `.gate-override.yaml`).

### `snapshot.repair_attempt`

Счётчик проходов internal repair-from-verify в текущем цикле verify (см. SKILL.md § Repair Loop). Сохраняется в снапшоте, чтобы повторный verify знал номер попытки и не зациклил авторемонт. Сбрасывается в `0` при вердикте GO или после user-decision.

### `snapshot.artifacts_mtime`

ISO-8601 строка до секунды для `proposal.md`, `design.md`, `tasks.md` и каждого `openspec/changes/<name>/specs/**/*.md`. **`mtime` решает только**, нужно ли пересчитать хэш содержимого; сравнение новизны и кэш — по `artifact_hashes`, не по одной метке времени.

### Нормализация и ключ кэша (SSOT)

Нормализация перед SHA-256: перевод перевода строк в LF, снятие хвостовых пробелов, **включая** YAML front-matter файла. Старый snapshot без `artifact_hashes` / `check_cache` — **cache miss** (полный пересчёт затронутых контролей, не ошибка).

**Отпечаток постановки** (сравнение «запись ответа выглядит как смена постановки») считается по `proposal.md`, `design.md`, `tasks.md` и `specs/**` **без** секции `design.md` `## Решения verify (зафиксировано)` и **без** `debug.md` § `## External Contract Ledger`. Эти два куска живут в `decision_fingerprints` и `external_contract_digest` и в хэш постановки не входят. Правка выбранного подхода, контракта поведения или вариантов реализации в вычет не попадает и по-прежнему меняет отпечаток.

**Ключ результата** `check_cache`:

```text
check_id + scope_anchor + ordered_input_hashes + rules_version + evidence_digest
```

`rules_versions[path]` = SHA-256 нормализованного файла правила. `decision_fingerprints[id]` = SHA-256 от `id + closed_at + source`. `external_contract_digest` = SHA-256 упорядоченных `EC-*`, их `parity`/`confirmation` и `source_fingerprint` первичных событий.

### Канонический перечень контролей

| `check_id` | Входные артефакты | Файлы правил |
|---|---|---|
| `hygiene-checkboxes` | `tasks.md` | этот скилл § Layer 1 |
| `slice-gate-markers` | `tasks.md` | `.cursor/rules/vertical-slices.mdc` |
| `user-task-contract` | `tasks.md` | `.cursor/rules/vertical-slices.mdc` § User Task Contract |
| `external-contract-schema` | `debug.md` § External Contract Ledger | этот скилл § Load artifacts |
| `external-validity` | `debug.md` ledger + реестр; `design.md` § «Решения verify»; `reports/slice-acceptance-S*-*.md` | этот скилл § External validity |
| `scenario-coverage` | `specs/**`, `design.md` ## Slices, `tasks.md` | `.cursor/rules/vertical-slices.mdc`, `.cursor/rules/openspec-specs-gate.mdc` |
| `code-truth` | backticks в design/tasks/specs/debug | `.cursor/rules/code-truth-gate.mdc` |
| `precedent-regression` | `specs/**`, archive | `.cursor/rules/precedent-regression-gate.mdc` |
| `loop-detection` | `debug.md` Slice Gate / Extend | `.cursor/rules/vertical-slices.mdc` § Loop Detection |
| `problem-solution-trace` | `proposal.md`, `specs/**`, `tasks.md` | этот скилл § Layer 3 |
| `design-challenge` | `proposal.md`, `design.md`, `specs/**`, `external_contract_digest` | `.cursor/rules/architect-gate.mdc` |
| `task-readiness` | `tasks.md`, `design.md` (изменившиеся задачи) | `.cursor/rules/architect-gate.mdc` |

### Точечная инвалидация

1. Новое структурированное внешнее событие → `external-validity`, связанная запись `EC-*`, детектор повторения; `design-challenge` — только при конфликте с design.
2. Изменение одного Scenario → его связи, внешний контракт этой оси, семантика связанного среза.
3. Изменение одной задачи → её `task-readiness`, зависимые задачи, связанный срез только если изменился результат приёмки.
4. Изменение только отметки `[x]`/`[ ]` → прогресс и проверка реализации, не архитектурный план.
5. Изменение версии правила → только контроли, объявившие этот файл в таблице выше.
6. Дополнение только фиксирует ответ заказчика внутри выбранного подхода (меняется зеркало решений или реестр контрактов, ось Decisions / Behavior Contract и варианты реализации не меняются) → точечный прогон затронутых тем; `design-challenge` в `invalidation_map` не ставить и полный независимый разбор не запускать. В отчёте прямо написать, что прогон точечный.

Недоказанная локальность → консервативно инвалидировать **затронутый срез**, не весь пакет. Неизвестная граница → `verify_depth: full`.

## Что хранится только в YAML и НЕ дублируется в чат

- `verify_mode`, `verdict`, `layer_status` — внутреннее техническое состояние.
- `tier` (если используется во внутренних метриках) — только в YAML.
- В первой строке секции `## Резюме для разработчика` (см. `templates/executive-summary.md`) — формулировка `<change-name> — можно запускать apply.` либо `<change-name> — до apply нужно решение: <одна техническая фраза>` (см. `templates/verdict-card.md`), а не `verdict: GO` / `verdict: NO-GO`.

## Порядок блоков файла (после YAML)

YAML — **первый** блок файла (нужен фильтру новизны и аудиту). Сразу за ним — **читаемый человеком** контент в следующем порядке:

1. `## Резюме для разработчика` — на языке кода 1С, зеркало чата.
2. `## Решения до apply` — только при `verdict: NO-GO`.
3. `## Что меняется в постановке` — карточка изменений для разработчика.
4. `### Подправил в постановке` — авто-правки гигиены простыми словами (если были).
5. `### К сведению` — мелочи, не блокирующие apply (если есть).
6. `## Технический аудит (для движка OpenSpec)` — статусы слоёв, технические алерты. **Только здесь** допустимы имена `Layer N`, `PASS/FAIL`, `CHALLENGE`, `design-challenge`, `task-readiness`. Если контроль среза взят по опоре (прошлый контроль в порядке, тот же упорядоченный набор названий сценариев, тот же нормализованный текст обязательного пункта приёмки) — отдельная строка: «опора на прошлый контроль среза S\<N\>: взят прошлый результат `reports/quality-control-….md`, новый полный контроль с нуля не создавался». Это не молчаливое совпадение отпечатков всего текста.
7. `## Источники` — пути к дочерним отчётам (`quality-control-*.md`, `design-challenge-*.md`, `architecture-task-readiness-*.md`), технические коды алертов.

Полный шаблон каждой секции — `templates/executive-summary.md`.
