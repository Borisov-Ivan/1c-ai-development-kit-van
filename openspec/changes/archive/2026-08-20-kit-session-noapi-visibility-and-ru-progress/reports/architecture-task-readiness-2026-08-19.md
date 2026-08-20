---
report_type: architecture
generated_at: 2026-08-19
agent: onec-code-architect
mode: task-readiness
scope:
  change: kit-session-noapi-visibility-and-ru-progress
  files:
    - .cursor/rules/model-selection.mdc
    - .cursor/rules/tool-name-guard.mdc
    - .cursor/rules/session-discipline.mdc
    - .cursor/docs/faq-kit.md
    - .cursor/rules/chat-output-budget.mdc
    - .cursor/rules/chat-output-budget-full.mdc
    - .cursor/docs/opsx-output-style.md
    - .cursor/rules/model-grok4.mdc
    - .cursor/rules/model-adaptation.mdc
    - .cursor/skills/openspec-verify-change/SKILL.md
    - .cursor/skills/openspec-new-change/SKILL.md
    - .cursor/docs/templates/brief-card.md
confidence: high
open_questions_count: 0
---

# Task Readiness: kit-session-noapi-visibility-and-ru-progress

## Вердикт

**ГОТОВО С ЗАМЕЧАНИЯМИ**

Артефакты позволяют исполнителю (оркестратор, прямая правка markdown-правил) пройти S1–S3 без возврата к архитектуре. Три замечания — уточнение формулировок задач, а не пересмотр решений; все закрываются вставкой текста в `tasks.md` (сниппеты ниже).

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость задач (markdown-правил) | **GAP** | 12 из 13 правочных задач называют файл, якорь и наблюдаемый результат; целевые файлы и якоря существуют (`model-selection.mdc` «Режим сессии» и «Закрытая эскалация Fable»; `tool-name-guard.mdc` п.2 чеклиста; `session-discipline.mdc` «Режим сессии (выбор модели)»; `chat-output-budget.mdc` «Progress marker (§6)» / «Pre-send self-check (§1b)»; `chat-output-budget-full.mdc` §1b/§6; `opsx-output-style.md` §2; `model-adaptation.mdc` «Precedence»; `model-grok4.mdc` MUST NOT; verify SKILL шаг progress marker; new-change SKILL шаг 1.5; `brief-card.md` «Metadata Gate»). Исключение — **S1.4**: глагол «вынести рядом» не задаёт наблюдаемый результат (см. GAP-1). |
| 2 | Реализуемость форм и метаданных | **n/a (OK)** | `form_mode: n/a` в proposal, метаданных 1С нет, `src/` / `cfe/` в scope не входят. Ни одна задача не требует Конфигуратора и не создаёт XML. Противоречий с Mode Gate нет. |
| 3 | Разрешённость решений | **OK** | D1–D11 закрыты, «Открытые вопросы: нет блокирующих». Ни одна задача не оставляет выбор исполнителю: все «или» в тексте задач — условия применимости (S3.1 «`.bsl` **или** модули в `src/` / расширении»), не развилки. Отклонённые варианты 2–7 в `## Implementation Options` не всплывают в задачах. |
| 4 | Полнота покрытия | **OK** | 4 дельта-спеки, 5 requirements, 9 сценариев. Покрытие: `session-api-mode` (3 req / 5 сцен) → S1.1–S1.3, S1.7 + сверки S1.8–S1.12; `chat-surface-clarity` (1 req / 2 сцен) → S2.1–S2.3, S2.7 + S2.8–S2.9; `chat-model-profiles` (1 req / 1 сцен) → S2.5, S2.6 + S2.10; `sequential-gate-questions` (1 req / 2 сцен) → S3.1, S3.2 + S3.3–S3.4. Обратная сверка: каждый файл из `## Impact` имеет задачу. Имена ADDED-requirements не совпадают с существующими в `openspec/specs/**` — коллизий нет. Примечание (не GAP): пункт 5 `## What Changes` (два сигнала не смешивать) отражён только задачами S1.4 / S2.7, отдельного Requirement под него нет — это уточнение существующего поведения, дельта не обязана его дублировать. |
| 5 | Согласованность | **GAP** | tasks ↔ design ↔ spec совпадают по срезам, именам сценариев и файлам; бюджет сложности design (~12 файлов kit) равен фактическому числу целевых файлов задач; все задачи говорят «Добавить / Дописать» по существующим файлам — расхождений «создать» ↔ состояние репо нет; D10 («`command-session-persistence.mdc` не трогать») явно продублирован в S1.6. Два расхождения по факту правки: счётчик пунктов §1b (GAP-2) и внутреннее противоречие в `openspec-new-change/SKILL.md` после S3.1 (GAP-3). |
| 6 | Связность и порядок задач | **OK** | В каждом срезе порядок «правки → статическая сверка → приёмка», ровно один `S<N>.accept`, ровно один маркер `slice-gate` после каждой приёмки, формулировка маркера совпадает с Primary acceptance среза. Файловые множества срезов не пересекаются, граф зависимостей пуст — заявленная независимость подтверждается. Мягкая связь: S2.7 ссылается на канон из `model-selection.mdc`; канон в файле уже есть до правок S1, поэтому порядок S2 → S1 тоже допустим. S1.13 (регрессионная сверка таблицы ролей) стоит последней среди сверок — корректно. |
| 7 | Архитектурная эстетика (Design Smells) | **OK** | Нового механизма нет: 0 новых режимов сессии, 0 новых гейтов, 0 файлов. Все правки — дописывание существующих секций; альтернативы «печатать `-noapi`», «файл-состояние», «третий режим», «HALT-список глаголов» разобраны и отклонены с обоснованием. Дублирование stub ↔ full (S2.1–S2.3) — существующая конвенция репозитория, прикрыта сверкой S2.8. Риск (не smell): перечень английских каркасов в S2.1 не должен переехать в top-20 §7 — D5 это запрещает, задача цитирует D5. |
| 8 | User Task Contract + Precedent Coherence | **OK** | User runtime-spike в нумерации `S<N>.<M>` отсутствует: все 19 нумерованных задач исполняет оркестратор (правка текста или чтение текста), приёмка каждого среза заявлена как чтение правил «без информационной базы 1С». Precedent: `## Blast Radius` заполнен (12 строк, вердикт **extends**, supersedes нет). ADR-0004 не отменяется — таблица ролей, двухшаговая цепочка, in-flight шаг 2, sticky-множество и «токен — слово пользователя» сохранены, S1.13 добавляет регрессионную сверку таблицы. ADR-0001 не отменяется — канон без слага и без имени модели. Архивы `kit-session-api-mode`, `chat-surface-clarity`, `sequential-ui-mode-questions` расширяются, ни один Scenario архива не переписывается (D11 — только ADDED). |

## Пробелы

### GAP-1 — S1.4: нет наблюдаемого результата

- **Задача:** `S1.4 Вынести рядом русскую одну строку про эскалацию, недоступную в сборке, отдельно от канона лимита; слаг не угадывать (D7)`.
- **Что отсутствует:** глагол «вынести» читается как перенос текста, но переносить нечего: строка «одна строка, что самая дорогая эскалация в этой сборке недоступна» уже присутствует в `model-selection.mdc` (таблица закрытой эскалации Fable) и уже по-русски. D7 требует другого: зафиксировать, что это **второй, отдельный** сигнал, который не смешивается с каноном лимита и не заменяет его. Исполнитель без design не поймёт, что должно измениться в файле; задача не покрыта ни одним Scenario и не входит в `S1.accept`.
- **Рекомендация:** переформулировать через результат «в файле есть явное разграничение двух сигналов».
- **Сниппет (замена строки S1.4 в `tasks.md`):**

```markdown
- [ ] S1.4 Записать в `.cursor/rules/model-selection.mdc` рядом с каноном лимита, что строка «самая дорогая эскалация в этой сборке недоступна» — отдельный русский сигнал: она не заменяет канон лимита, канон лимита не заменяет её, обе строки без слага модели; новую формулировку не сочинять, использовать существующую (D7)
```

### GAP-2 — S2.2 / S2.3: счётчик и нумерация §1b разъедутся

- **Задача:** `S2.2` (два пункта в §1b стаба) и `S2.3` (то же в `chat-output-budget-full.mdc`).
- **Что отсутствует:** сейчас §1b — ровно 8 пунктов в обоих файлах, причём в полном теле счёт зашит в заголовок: `### 1b. Pre-send self-check (оркестратор → чат, 8 пунктов)`, а в стабе — нумерованный inline-список `1. HALT-подстроки 2. Non-events … 8. Decision-block inline`. После добавления двух пунктов заголовок и оба списка станут неверными, а сверка S2.8 проверяет только §6. Это ровно тот класс расхождения stub ↔ full, который срез объявляет своей целью.
- **Рекомендация:** дописать обязанность синхронизации в S2.3 и расширить сверку S2.8.
- **Сниппет (замена S2.3 и S2.8 в `tasks.md`):**

```markdown
- [ ] S2.3 Дописать то же в `.cursor/rules/chat-output-budget-full.mdc` §6 и §1b, чтобы stub и полное тело не разъехались; в полном теле обновить счёт пунктов в заголовке §1b (`8 пунктов` → фактическое число), в стабе — нумерованный перечень пунктов §1b (D5)
```

```markdown
- [ ] S2.8 Верифицировать по тексту `.cursor/rules/chat-output-budget.mdc` и `chat-output-budget-full.mdc`: §6 требует русский progress; список пунктов §1b и счёт в заголовке полного тела совпадают между stub и полным телом (Scenario «Progress на русском», D5)
```

### GAP-3 — S3.1: guardrail и анти-паттерн new-change останутся противоречить пропуску вопроса

- **Задача:** `S3.1 Дописать в .cursor/skills/openspec-new-change/SKILL.md шаг Metadata Gate…`.
- **Что отсутствует:** в том же скилле есть два места, которые после правки шага 1.5 начнут противоречить новому поведению: `**Guardrail:** openspec new change до завершения Metadata Gate для **нового** change запрещён` (шаг 1.5) и анти-паттерн `**Metadata Gate MUST NOT be silently skipped** (новый change): не вызывать openspec new change без ответа на Metadata Gate`. При ЗНИ без BSL ответа пользователя не будет вовсе, и исполнитель окажется перед выбором «нарушить guardrail или задать лишний вопрос» — то есть ровно тот возврат на уточнение, который оценка должна исключить. Формулировку нужно поправить в той же задаче (плейсхолдеров `<ФИО>` при пропуске не возникает — записывается `developer: n/a`, поэтому WARNING сводки не срабатывает и его трогать не нужно).
- **Рекомендация:** добавить в S3.1 явный пункт «гейт закрывается ответом **или** обоснованным пропуском».
- **Сниппет (дополнение к S3.1 — отдельная строка после неё в `tasks.md`):**

```markdown
- [ ] S3.1a Согласовать в `.cursor/skills/openspec-new-change/SKILL.md` формулировки guardrail шага 1.5 и анти-паттерна «Metadata Gate MUST NOT be silently skipped»: гейт считается закрытым либо ответом пользователя, либо обоснованным пропуском при отсутствии BSL в scope (`developer: n/a`, `marker_style: minimal`); молчаливый пропуск при BSL в scope по-прежнему запрещён (D8)
```

## KB references

`## Existing Knowledge` во входном промпте пуст (taxonomy отсутствует, Discovery без совпадений) — ссылок нет, конфликтов нет.

## Источники

- `openspec/changes/kit-session-noapi-visibility-and-ru-progress/proposal.md`
- `openspec/changes/kit-session-noapi-visibility-and-ru-progress/design.md`
- `openspec/changes/kit-session-noapi-visibility-and-ru-progress/tasks.md`
- `openspec/changes/kit-session-noapi-visibility-and-ru-progress/specs/{session-api-mode,chat-surface-clarity,chat-model-profiles,sequential-gate-questions}/spec.md`
- `openspec/specs/session-api-mode/spec.md` (существующие Requirements — проверка коллизий имён и противоречий)
- `openspec/specs/{chat-surface-clarity,chat-model-profiles,sequential-gate-questions}/spec.md`
- `.cursor/rules/model-selection.mdc`, `tool-name-guard.mdc`, `session-discipline.mdc`, `chat-output-budget.mdc`, `chat-output-budget-full.mdc`, `model-adaptation.mdc`, `model-grok4.mdc`
- `.cursor/docs/faq-kit.md`, `.cursor/docs/opsx-output-style.md`, `.cursor/docs/templates/brief-card.md`
- `.cursor/skills/openspec-new-change/SKILL.md`, `.cursor/skills/openspec-verify-change/SKILL.md`
