---
name: openspec-knowledge-add
description: Add verified OpenSpec Knowledge Base facts from standalone reports or markdown sources outside a change archive.
---

# Skill: openspec-knowledge-add

## Назначение

`/opsx:knowledge-add` добавляет в `openspec/knowledge/` только верифицированные KB-факты из standalone-источников: аналитических отчётов, ручных markdown-заметок или уже стабильных reports. Команда не создаёт ЗНИ и не извлекает знания напрямую из BSL/XML-кода.

**Принцип:** либо полностью валидный KB с проверяемыми anchors, либо ничего. Если источник не даёт verified knowledge-worthy фактов, команда честно завершает работу без записи файлов.

## Размежевание

- `/opsx:archive <name>` — основной путь создания KB из reports активной ЗНИ.
- `/opsx:knowledge-audit --from-archive <name>` — повторное извлечение из уже архивированной ЗНИ.
- `/opsx:knowledge-add <path1> [path2 ...]` — произвольные источники вне ЗНИ (`temp/reports/...`, локальные markdown-заметки, одиночные reports).
- `/opsx:knowledge-audit` без `--from-archive` — TTL/drift/reindex/metrics; новые KB не создаёт.

## Input

```text
/opsx:knowledge-add <path1> [path2 ...] [--no-bundle] [--ttl <days>]
```

Без аргументов:

1. Не выполнять поиск по `temp/reports/`.
2. Не задавать AskQuestion со списком файлов.
3. Вывести краткую ошибку и примеры:

```text
/opsx:knowledge-add temp/reports/exploration-foo-2026-04-28.md
/opsx:knowledge-add temp/reports/report1.md temp/reports/report2.md
/opsx:knowledge-add openspec/changes/archive/2026-04-25-name/reports/exploration-2026-04-25.md --no-bundle
```

## Флаги

- `--no-bundle` — не копировать source. Допустим только если все входные пути уже стабильны:
  - `openspec/changes/archive/<YYYY-MM-DD-name>/reports/...`
  - `openspec/reports/knowledge-add/<YYYY-MM-DD-slug>/sources/...`
  Иначе остановиться: `Blocked — --no-bundle requires stable sources`.
- `--ttl <days>` — явный override TTL для всех сохраняемых кандидатов. Без флага TTL выбирать по таблице `knowledge-format.mdc` (`TTL POLICY`).

## Preflight

1. Прочитать `.cursor/rules/knowledge-format.mdc`.
2. Прочитать `openspec/knowledge/_taxonomy.yaml`.
   - Если файла нет → `Blocked — taxonomy missing`, предложить `/opsx:knowledge-init`, ничего не писать.
3. Прочитать `openspec/knowledge/_index.yaml`.
   - Если файл отсутствует или corrupt → предложить `/opsx:knowledge-audit --reindex`, ничего не писать.
4. Проверить, что каждый путь из input существует и читается.
   - Отсутствующие пути перечислить в ошибке, ничего не писать.
5. Выполнить structure check корня `openspec/knowledge/` по whitelist из `knowledge-format.mdc`.
   - Нарушения добавить в Warnings, но не блокировать extraction.

## Input Classification

Классифицировать каждый входной путь:

| Тип | Действие |
|-----|----------|
| `exploration-*.md`, `trace-analysis-*.md`, `resolved-contract-*.md`, `architecture-*.md`, `deep-analysis-*.md`, `design-review-*.md` | Пригоден как аналитический report |
| Markdown вне канонических масок | Пригоден только если содержит verified facts + anchors; добавить warning «вне канонических масок reports» |
| `openspec/knowledge/**/KB-*.md` | `Skipped — already a KB` |
| `.bsl`, `.xml`, `.mxl`, `.json`, `.txt`, трассы `.pff` / `*_TRACE_*.txt` | `Skipped — not a knowledge source`; подсказка: сначала `/opsx:explore` или `/opsx:debug`, затем `/opsx:knowledge-add <report>` |
| Каталог | `Skipped — directory input is not supported`; пользователь должен передать конкретные files |

Команда **не запускает** `onec-code-explorer` сама. Она работает с уже подготовленными источниками знаний, а не проводит обследование.

Если все входы skipped на этапе классификации → итог `Saved 0`, ничего не писать.

## Extraction Contract

Применяется к пригодным источникам.

1. Извлечь до 5 KB-кандидатов за сессию.
2. Кандидат должен удовлетворять критериям `knowledge-format.mdc`:
   - verified факт о поведении, контракте, цепочке вызовов, метаданных или стабильном имени;
   - не ADR (нет решения с trade-off);
   - не spec (не требование к будущему поведению);
   - не debug-контекст разового инцидента;
   - не тривиальное имя объекта без полезного контракта.
3. Если кандидатов больше 5:
   - выбрать top-5 по релевантности: verified в source, наличие конкретных anchors, отсутствие dedup-конфликта, ширина будущего переиспользования;
   - остальные перечислить в Warnings с `source:lines`.
4. Для каждого кандидата подготовить:
   - `title` ≤ 80 символов;
   - `domain` и `subdomain`;
   - `anchors`;
   - `source.report`, `source.lines`, `source.also-mentioned-in`;
   - `ttl-days`;
   - `why-knowledge`;
   - `supersedes` / `supersedes-by`, если это замена существующего KB;
   - текст секций `## Факт` и `## Почему это knowledge, а не ADR/spec`.

## Candidate Validation

Для каждого кандидата:

### Domain / Subdomain

1. Подобрать `domain` по `_taxonomy.yaml`: `anchor.path` должен попадать под `domain.source`.
2. Если anchors в нескольких зонах — домен выбирать по основному anchor, смежные факты отражать в `related.kb` только если есть существующие KB.
3. Если нельзя уверенно назначить domain/subdomain → `Blocked — taxonomy mismatch` для кандидата. Не создавать новый domain и не править taxonomy.

### Anchors

Допустимые типы anchors — только из `knowledge-format.mdc`:

- `procedure`
- `event-name`
- `metadata-object`
- `query-pattern`

Для `procedure` извлечь `fingerprint.declaration` и `fingerprint.body-head` по правилам `knowledge-format.mdc`.

### Verify

Проверить anchors против текущего `src/` по алгоритму `knowledge-format.mdc`.

- `verified` → кандидат может идти в карточку.
- `signature-drift`, `behavioral-drift`, `anchor-missing`, `count-drift` → `Skipped — stale anchors at extraction time`.
- `verify-failed` → `Skipped — unverified content`.

### Dedup

Проверить `_index.yaml` и файлы KB (включая `_archive/`):

- точное совпадение `anchor.path + name/value/signature`;
- близкий `title`;
- значимое пересечение `anchor-paths`.

Результат:

- существующий KB полностью покрывает факт → `Skipped — duplicate of KB-NNNN`;
- новый факт заменяет старый → карточка `SUPERSEDES KB-NNNN`;
- факты различны → кандидат остаётся.

### TTL

Без `--ttl` выбирать по `knowledge-format.mdc`:

- внешний API → 30;
- точка расширения типовой процедуры → 60;
- цепочка вызовов / поведение внутри расширения → 90;
- имя ЖР, константа, метаданные → 180.

### Why Knowledge

`why-knowledge` обязательно. Если невозможно написать честное предложение «почему это KB, а не ADR/spec/debug/project», кандидат отбрасывается: `Skipped — knowledge-worthy criterion not justified`.

## Source Bundle

KB хранит короткую карточку и ссылку на source, а не копию отчёта.

Стабильные sources:

- `openspec/changes/archive/<YYYY-MM-DD-name>/reports/...`
- `openspec/reports/knowledge-add/<YYYY-MM-DD-slug>/sources/...`

Все остальные sources считаются нестабильными и копируются в bundle **только после подтверждения сохранения**.

### Planned Source Path

До показа AskQuestion вычислить итоговый путь source:

```text
openspec/reports/knowledge-add/<YYYY-MM-DD>-<slug>/sources/<original-name>
```

Именно этот planned path показывать в карточке preview и записывать в будущий `source.report`.

### Bundle-on-save

При `yes` и хотя бы одном нестабильном source:

```text
openspec/reports/knowledge-add/<YYYY-MM-DD>-<slug>/
  sources/
    <original-name-1>
    <original-name-2>
  knowledge-add-report.md
```

Правила:

- bundle создаётся только при сохранении хотя бы одного KB;
- при `no` или `Saved 0` bundle не создаётся;
- `<slug>` брать из title первого сохраняемого KB или объединяющей темы;
- при коллизии каталога добавлять `-2`, `-3`;
- если один факт подтверждён несколькими sources, `source.report` — самый подробный source, остальные → `source.also-mentioned-in`.

## Preview / AskQuestion

Если после validation нет кандидатов:

1. Не задавать AskQuestion.
2. Ничего не писать.
3. Вывести `Saved 0` и список причин:
   - `No candidates after filters`
   - `Skipped — ...`
   - `Blocked — ...`

Если кандидаты есть, показать per-candidate карточки и один вопрос:

```markdown
### KB-<next-id-preview>: <title>
- **Domain / subdomain:** <domain> / <subdomain>
- **TTL:** <days>
- **Anchors:** <path>:<name> (+ дополнительные при наличии)
- **Why knowledge:** <one sentence>
- **Source:** <planned-stable-source>:<line-range>
- **Supersedes:** KB-NNNN (если применимо)
```

Единый вопрос: «Сохранить N KB-фактов?»

Options:

- `yes`
- `no`

Preview ID не считается зарезервированным. Окончательная нумерация выполняется только при save.

## Save Protocol

Только при `yes`.

1. Определить следующие номера: Glob `openspec/knowledge/**/KB-*.md` включая `_archive/`, max + 1.
2. Создать bundle, если нужен.
3. Создать `openspec/knowledge/<domain>/KB-NNNN-slug.md` для каждого кандидата.
4. Пересобрать `openspec/knowledge/_index.yaml` из фактических KB-файлов на диске.
5. Создать `knowledge-add-report.md` в bundle (если bundle был создан) со списком:
   - сохранённых KB;
   - skipped/blocked candidates;
   - structure warnings;
   - sources.

### Atomicity / Rollback

Если ошибка возникла до перезаписи `_index.yaml`:

- удалить созданные в этой сессии KB-файлы;
- удалить bundle этой сессии;
- оставить старый `_index.yaml`.

Если ошибка возникла после перезаписи `_index.yaml`:

- выполнить `/opsx:knowledge-audit --reindex`-совместимую пересборку индекса из disk-state;
- вывести warning о recovery.

Номер KB не переиспользуется только после успешного создания KB-файла. Preview номера не резервируются.

## Output

Использовать T-CONFIRM (`.cursor/docs/opsx-output-style.md` §5.5).

Итоговые состояния:

- `Saved N (KB-NNNN, ...)`
- `Declined by user`
- `Saved 0 — No candidates after filters`
- `Blocked — taxonomy missing`
- `Blocked — --no-bundle requires stable sources`

В summary показать:

- сохранённые KB-файлы;
- bundle path, если создан;
- обновление `_index.yaml`;
- Warnings только если есть;
- следующий шаг: `/opsx:knowledge-audit --metrics` или повторный `/opsx:knowledge-add <path>`.

Перед финальным выводом выполнить self-check-5 из `.cursor/docs/opsx-output-style.md`.

## Archive Integration

`openspec-archive-change` шаг 5.5 использует тот же extraction contract:

- inputs: `reports/exploration-*.md`, `reports/trace-analysis-*.md`, `reports/resolved-contract-*.md` из архивируемой ЗНИ;
- source считается стабильным planned archive path: `openspec/changes/archive/YYYY-MM-DD-<change>/reports/<report>.md`;
- bundle не создаётся;
- auto-yes policy archive сохраняется: если кандидаты есть, archive показывает карточки и единый AskQuestion только для KB-кандидатов, как было в шаге 5.5; при `no` archive продолжается со state `Declined by user`.

## Guardrails

- Не создавать и не изменять ЗНИ.
- Не писать в `src/`.
- Не создавать новые domain/subdomain в taxonomy.
- Не извлекать KB напрямую из BSL/XML/trace; сначала нужен аналитический report.
- Не создавать bundle и KB при `Saved 0` или `Declined by user`.
- Не скрывать причины отказа: каждый skipped/blocked candidate должен быть отражён в summary или `knowledge-add-report.md` (если bundle создан).
