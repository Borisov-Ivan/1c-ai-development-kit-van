# AGENTS.md — навигационный индекс

**Главный диспетчер:** `.cursor/rules/1c-agent-delegation.mdc` — HALT-условия, делегирование агентам, BSL/XML write guard.
**Диспетчер on-demand гейтов:** `.cursor/rules/gate-dispatcher.mdc` — подгружает архитектурные и верификационные гейты по триггерам.

## OpenSpec Workflow

`.cursor/rules/sdd-workflow.mdc` — explore → new/ff → verify → apply → verify → archive.

Команды: `/opsx:explore` (точка входа; свободный текст = explore), `/opsx:new`, `/opsx:ff`, `/opsx:verify`, `/opsx:apply`, `/opsx:archive`, `/opsx:extend`, `/opsx:continue`, `/opsx:status`, `/opsx:migrate-slices`, `/opsx:estimate`, `/opsx:doc-tz`, `/opsx:knowledge-add`, `/opsx:sync`, `/opsx:bulk-archive`, `/review`, `/prerelease-review`, `/init-project`.

### Decision tree команд

Полный глоссарий терминов: `openspec/glossary.md`.

| Задача пользователя | Команда | Чем отличается |
|---------------------|---------|----------------|
| Любой вопрос, дефект, идея, постановка (в т.ч. свободный текст) | `/opsx:explore` | Единая точка входа; бриф-чекпойнт; итог — блок `## Для /opsx:ff` в чате |
| Создать change целиком разом (задача понятна) | `/opsx:ff <name>` | Все артефакты сразу |
| Создать change пошагово | `/opsx:new <name>` → `/opsx:continue <name>` | По одному артефакту за шаг |
| Где я в этом change | `/opsx:status <name>` | Read-only снимок |
| Можно ли запускать apply | `/opsx:verify <name>` | Pre-flight + self-repair; один вердикт в первой строке |
| Добавить новое требование | `/opsx:extend <name>` | Бриф → правки → подсказка verify |
| Учесть отчёт ревью/архитектора | `/opsx:extend <name> --from-review` / `--from-architecture` | Классификация findings → правки артефактов |
| Код упростили вручную, артефакты отстали | `/opsx:extend <name> --code-sync` | explorer читает факт → артефакты догоняют |
| Мигрировать старый tasks.md в срезы | `/opsx:migrate-slices <name>` | Реструктуризация + подтверждение diff |
| Реализовать задачи | `/opsx:apply <name>` | Делегирует writer/reviewer; пауза на приёмке среза |
| Архивировать завершённый change | `/opsx:archive <name>` | Финализация + извлечение ADR/KB |
| Сгенерировать ТЗ по ЗНИ | `/opsx:doc-tz <name>` | Отдельно от verify |
| Оценить трудозатраты | `/opsx:estimate <name>` | PERT по tasks.md |
| Ревью кода | `/review` | Без аргумента — git diff; с аргументом — файл/модуль/расширение/ЗНИ |
| Финальная проверка перед релизом | `/prerelease-review` | Расширение целиком или change scope |
| Зафиксировать факты вне ЗНИ | `/opsx:knowledge-add <path>` | Без ЗНИ; source + KB-карточка |

## Карта SSOT (один якорь на тему)

**Чат и стиль:**
- Лимиты, non-events, HALT-жаргон, 5 принципов диалога, роль навигатора → `.cursor/rules/chat-output-budget.mdc`.
- Язык, тон, шаблоны вывода, Chat Surface Contract (§2.6) → `.cursor/docs/opsx-output-style.md`.
- Словарь запретов (SSOT) → `.cursor/docs/chat-lexicon.md`; каталог AI-tells → `.cursor/skills/stop-slop/SKILL.md`.

**Делегирование и код 1С:**
- HALT, делегирование, APPLY/LIGHT/MECHANICAL MODE, LINT GATE, API CHECK, BSL+XML write guard → `.cursor/rules/1c-agent-delegation.mdc`.
- Writer pipeline (API/extension/contract) → `.cursor/rules/1c-writer-pipeline.mdc` (globs `**/*.bsl`).
- Запрет создания метаданных → `.cursor/rules/1c-no-metadata-creation.mdc`; валидация имён метаданных по выгрузке `src/` до использования → `.cursor/rules/1c-metadata-validation.mdc` (globs `**/*.bsl`).
- Инструмент субагентов = Task → `.cursor/rules/tool-name-guard.mdc`; модели → `.cursor/rules/model-selection.mdc`.
- Анализ ошибок (трасса → trace-analyst) → `.cursor/rules/1c-error-analysis.mdc`.
- Утилитарные агенты, формы → `.cursor/rules/1c-utility-agents.mdc`, `.cursor/skills/1c-forms/SKILL.md`.
- Паттерны промптов агентов → `.cursor/skills/1c-agent-patterns/SKILL.md`; промпты → `.cursor/agents/*.md` (changelog `.cursor/agents/CHANGELOG.md`).

**Сессии и стратегия:**
- Skill-first, persistence, context-strategy → `.cursor/rules/session-discipline.mdc`.
- Прямое чтение vs субагенты → `.cursor/skills/context-strategy/SKILL.md`.
- Сохранение отчётов субагентов → `.cursor/rules/preserve-subagent-reports.mdc`.

**Гейты качества:**
- Архитектурное ревью (триггеры, Simplicity Check) → `.cursor/rules/architect-gate.mdc`.
- Root cause + impact перед фиксом → `.cursor/rules/verified-cause-gate.mdc`.
- Приоритет существующих механизмов → `.cursor/rules/existing-mechanism-priority.mdc`.
- Code-Truth (phantom-symbol) → `.cursor/rules/code-truth-gate.mdc`; precedent/regression → `.cursor/rules/precedent-regression-gate.mdc`.
- Delta specs → `.cursor/rules/openspec-specs-gate.mdc`; срезы → `.cursor/rules/vertical-slices.mdc`.
- Антипаттерны BSL (reviewer-only) → `.cursor/rules/bsl-antipatterns.mdc`; стандарты → `.cursor/docs/1c-coding-standards.md`, `.cursor/skills/1c-vendor-standards/SKILL.md`.

**Знания и решения:**
- ADR → `openspec/adrs/` + `.cursor/rules/adr-format.mdc`.
- Knowledge Base → `openspec/knowledge/` + `.cursor/rules/knowledge-format.mdc`.
- Маркеры разработчика → `openspec/project.md`; фиксация договорённостей → `.cursor/rules/capture-to-project.mdc`.
- Пути к выгрузке (cf/cfe) → `openspec/project.md` + `.cursor/rules/project-paths.mdc`.
- Словарь лексики ТЗ → `.cursor/docs/tz-lexicon-dictionary.md`; запрет ROI/оценок → `.cursor/rules/no-roi-estimates.mdc`.
- Инфраструктура 1С → `.cursor/docs/onec-infrastructure.md`.

**Доменные навыки 1С:** `1c-bsp`, `1c-extensions`, `1c-forms`, `1c-mxl`, `1c-roles`, `1c-query-optimization` — через `available_skills` и `.cursor/skills/*/SKILL.md`. Справочники: `.cursor/docs/platform/`, `.cursor/docs/standard/`.
