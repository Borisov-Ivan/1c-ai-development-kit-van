---
report_type: task-readiness
generated_at: 2026-08-08
agent: onec-code-architect
mode: task-readiness
scope:
  change: hardcode-justification-gate
  slices: [S1, S2, S3]
  files:
    - .cursor/rules/bsl-antipatterns.mdc
    - .cursor/docs/antipatterns/bsl-antipatterns.md
    - .cursor/rules/existing-mechanism-priority.mdc
    - .cursor/rules/architect-gate.mdc
    - .cursor/agents/onec-code-architect.md
    - .cursor/agents/onec-code-writer.md
    - .cursor/agents/onec-code-reviewer.md
    - .cursor/docs/standard/reviewer-checks.md
  capabilities: [hardcode-justification-gate]
related_reports:
  - reports/exploration-2026-08-08-hardcode-justification-gate.md
  - reports/architecture-task-decomposition-2026-08-08.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Task Readiness — hardcode-justification-gate

## Контекст оценки

Эволюция kit (markdown/rules/agents в `.cursor/`), `form_mode: n/a`, прикладной BSL вне scope, `openspec/project.md` отсутствует. Оценена целостная реализуемость артефактов силами агентов + приёмка пользователя по чтению/grep канона — без оценки «исполняемости приёмки прямо сейчас».

### Вердикт

**НЕ ГОТОВО**

Агенты могут править перечисленные в `tasks.md` файлы, но канон реестра AP в kit — **двухфайловый**: индекс `.cursor/rules/bsl-antipatterns.mdc` + полная карточка `.cursor/docs/antipatterns/bsl-antipatterns.md` (явно указано в шапке `.mdc`). Карточка AP-055 в Impact/design/tasks отсутствует → реализация as-is оставит норму без полной карточки (разрыв с прецедентом AP-054 и со Scenario «Registry describes identity-filter class»).

### Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | GAP | Задачи S1.1–S1.2 / S2.* / S3.* однозначно указывают пути `.mdc`/`.md` агентов и rules; правки исполнимы. **Пробел:** нет `S1.x` на `.cursor/docs/antipatterns/bsl-antipatterns.md` (SSOT полных карточек). Agent по `tasks.md` as-is не создаст карточку AP-055. |
| 2 | Реализуемость форм и метаданных | OK | `proposal.md` / Forms mode: `form_mode: n/a`; метаданные и Form.xml вне scope; маркеров ручной конфигурации нет. |
| 3 | Разрешённость решений | OK | Decisions 1–5 и Option A зафиксированы; имя Phase 2.6 канонизировано; AP-055 с mitigation перенумерации на apply; Open Questions (grep verify) явно non-blocker / Follow-up. Нет развилки, блокирующей текст gates. |
| 4 | Полнота покрытия requirements из spec | GAP | Architect / Writer / Reviewer / Scope-as-literals / protocol-literals boundary покрыты S2–S3 и S1.2–S1.4. Requirement «Identity-filter has a named anti-pattern…» + Scenario Registry — **неполное покрытие файловой поверхности реестра**: только индекс `.mdc`, без полной карточки в `docs/antipatterns`. |
| 5 | Согласованность tasks↔design↔spec | GAP | Срезы S1→S3, Behavior Contract, Primary acceptance и spec scenarios в целом согласованы. **Расхождение:** proposal Impact и design Slices перечисляют `bsl-antipatterns` / `.mdc`, но не `docs/antipatterns/bsl-antipatterns.md`, хотя сам индекс объявляет полные карточки там. Матрица design помечает Phase 2.6 / contradiction как `(optional)` при том, что Primary S3 и tasks включают их в обязательную приёмку — замечание не блокирует, но путает optional vs Primary. |
| 6 | Связность и порядок задач S1→S2→S3; slice-gate | OK | Зависимости S1→S2→S3; внутри срезов порядок реестр→запах→шаблон / agent→gate→anti-bypass / writer→reviewer→sync docs; `<!-- slice-gate -->` после каждого accept; Follow-up вне срезов. |
| 7 | Архитектурная эстетика | OK | Зеркало каркаса Попытки (AP + HALT + Phase + completeness); Preference Hierarchy уровень 2–3 без нового «движка»; инвазивность только в kit-процессе; Options B/C отклонены обоснованно. |
| 8 | User Task Contract | OK | Все `S<N>.<M>` — правки файлов kit агентом. Пользователь только в `S1.accept` / `S2.accept` / `S3.accept` (чтение/grep канона). Нет IB / Конфигуратор / отладчик / runtime-spike в теле `S<N>.<M>`. |

### Пробелы

#### GAP-1 — полная карточка AP-055 вне tasks (критерии 1, 4, 5)

- **Задача / артефакт:** `tasks.md` S1; `proposal.md` Impact; `design.md` Slices/S1 files; spec Requirement «Identity-filter has a named anti-pattern…»
- **Что отсутствует:** целевой файл `.cursor/docs/antipatterns/bsl-antipatterns.md` и задача на карточку AP-055 (детекторы, remediation, граница protocol/enum) рядом с индексом в `.mdc`.
- **Рекомендация:** добавить задачу в S1 (после S1.1 или как S1.1b) и строку в proposal Impact / design S1 files; Primary S1.accept — проверить и карточку, и индекс.
- **Сниппет для вставки в `tasks.md`** (после S1.1):

```markdown
- [ ] S1.1b В `.cursor/docs/antipatterns/bsl-antipatterns.md`: добавить полную карточку AP-055 Hardcoded Identity Filter (детекторы runtime-фильтра по `ИмяФормы` / литералу `ОткрытьФорму` / allow-list имён в хуке; remediation API/настройка или `## Hardcode Justification`; граница «не путать» с литералами протокола/enum), синхронно с индексом/таблицей в `bsl-antipatterns.mdc` (SSOT карточек — шапка `.mdc`)
```

- **Сниппет для `proposal.md` Impact (дополнить список файлов):**

```markdown
`.cursor/docs/antipatterns/bsl-antipatterns.md`,
```

#### Замечание (не GAP) — матрица optional vs Primary S3

В `design.md` матрице приёмки строки Phase 2.6 и contradiction помечены `(optional)`, тогда как Primary acceptance S3 и `S3.accept` требуют их обязательно. Имеет смысл выровнять матрицу на Primary, чтобы optional относился только к scenario-sub-bullets в accept, не к самому наличию Phase/MUST_FIX.

## Precedent / KB

Отдельного `## Blast Radius` / precedent-coherence-отчёта не требуется для вердикта готовности: change — эволюция kit; прикладные контракты archive/consumer явно Non-Goals; отмены archived ADDED-контрактов постановка не обещает. KB в промпте не передавалась.

## Источники

- `proposal.md`, `design.md`, `tasks.md`, `specs/hardcode-justification-gate/spec.md`
- `.cursor/rules/bsl-antipatterns.mdc` (строки про полные карточки → `docs/antipatterns`)
- Прецедент поставки AP-054 (индекс `.mdc` + карточка в `docs/antipatterns`)
- `reports/architecture-task-decomposition-2026-08-08.md`
