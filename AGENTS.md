# AGENTS.md — навигационный индекс

**Главный диспетчер:** `.cursor/rules/1c-agent-delegation.mdc` — HALT-условия, делегирование агентам, BSL/XML write guard.
**Диспетчер on-demand гейтов:** `.cursor/rules/gate-dispatcher.mdc` — подгружает архитектурные и верификационные гейты по триггерам.
**Поставка шаблона в проект:** [`.cursor/docs/kit-template-workflow.md`](.cursor/docs/kit-template-workflow.md) — копирование `.cursor`+`AGENTS.md`; ЗНИ эволюции kit на ветке; change-папку не мержить в main.
**Памятка (обзор):** [`README.md`](README.md) · **Быстрый старт:** [`.cursor/docs/quick-start.md`](.cursor/docs/quick-start.md) · FAQ: [`.cursor/docs/faq-kit.md`](.cursor/docs/faq-kit.md) · Целостность поставки: [`.cursor/docs/delivery-integrity.md`](.cursor/docs/delivery-integrity.md).

## OpenSpec Workflow

`.cursor/rules/sdd-workflow.mdc` — explore → new → verify → apply → verify → archive.

**Единый вход исследования:** `/opsx:explore` (вопрос, дефект, сырой текст заказчика, идея). Дальше по сценарию: `/opsx:new` → `/opsx:verify` → `/opsx:apply` → `/opsx:archive`.

Команды: `/opsx:explore`, `/opsx:new`, `/opsx:verify`, `/opsx:apply`, `/opsx:archive`, `/opsx:extend`, `/opsx:status`, `/opsx:knowledge-add`, `/opsx:knowledge-init`, `/opsx:knowledge-audit`, `/opsx:sync`, `/opsx:bulk-archive`, `/review`, `/release-review`, `/init-project`.

Устаревшие алиасы: `/opsx:ff` и `/opsx:continue` → `/opsx:new <name>` (stub-redirect).

Справочник сценариев — в [`README.md`](README.md). Термины workflow — в [`openspec/project.md`](openspec/project.md).

## Карта SSOT (один якорь на тему)

**Чат и стиль:**
- Лимиты, non-events, HALT-жаргон, 5 принципов диалога, роль навигатора → `.cursor/rules/chat-output-budget.mdc` (полное тело — `chat-output-budget-full.mdc` по Read).
- Бриф = Sync Card (слоты B0–B3) → `.cursor/docs/templates/brief-card.md`; классификатор → `.cursor/docs/opsx-output-style.md` §5.1.
- Язык, тон, шаблоны вывода, Chat Surface Contract (§2.6) → `.cursor/docs/opsx-output-style.md`.
- Словарь запретов → `.cursor/docs/chat-lexicon.md`; AI-tells → `.cursor/skills/stop-slop/SKILL.md`.

**Делегирование и код 1С:**
- HALT (always-apply stub), делегирование, APPLY/XML write guard → `.cursor/rules/1c-agent-delegation.mdc`.
- HALT-таблица, Light/Mechanical → `.cursor/rules/1c-halt-triggers.mdc` (on-demand, globs `**/*.bsl`).
- LINT GATE, writer pipeline → `.cursor/rules/1c-writer-pipeline.mdc` (globs `**/*.bsl`).
- Запрет создания метаданных → `.cursor/rules/1c-no-metadata-creation.mdc`; валидация имён → `.cursor/rules/1c-metadata-validation.mdc`.
- Task → `.cursor/rules/tool-name-guard.mdc`; модели → `.cursor/rules/model-selection.mdc`.
- Трасса → `.cursor/rules/1c-error-analysis.mdc`; формы → `.cursor/rules/1c-utility-agents.mdc`, `.cursor/skills/1c-forms/SKILL.md`.
- Паттерны промптов → `.cursor/skills/1c-agent-patterns/SKILL.md`; агенты → `.cursor/agents/*.md`.

**Сессии и стратегия:**
- Skill-first, persistence, context-strategy → `.cursor/rules/session-discipline.mdc`.
- Прямое чтение vs субагенты → `.cursor/skills/context-strategy/SKILL.md`.
- Отчёты субагентов → `.cursor/rules/preserve-subagent-reports.mdc`.

**Гейты качества:**
- Forms/mxl Mode Gate → `.cursor/rules/forms-mxl-mode-gate.mdc`.
- Архитектура → `.cursor/rules/architect-gate.mdc`; root cause → `.cursor/rules/verified-cause-gate.mdc`.
- Existing mechanisms → `.cursor/rules/existing-mechanism-priority.mdc`.
- Code-Truth → `.cursor/rules/code-truth-gate.mdc`; precedent → `.cursor/rules/precedent-regression-gate.mdc`.
- Delta specs → `.cursor/rules/openspec-specs-gate.mdc`; срезы → `.cursor/rules/vertical-slices.mdc`.
- Антипаттерны BSL (reviewer-only) → `.cursor/rules/bsl-antipatterns.mdc`; стандарты → `.cursor/docs/1c-coding-standards.md`, `.cursor/skills/1c-vendor-standards/SKILL.md`.

**Знания и решения:**
- ADR → `openspec/adrs/` + `.cursor/rules/adr-format.mdc`.
- Knowledge Base → `openspec/knowledge/` + `.cursor/rules/knowledge-format.mdc`.
- Маркеры → [`.cursor/docs/marker-canon.md`](.cursor/docs/marker-canon.md); overlay → [`openspec/project.md`](openspec/project.md); capture → [`.cursor/rules/capture-to-project.mdc`](.cursor/rules/capture-to-project.mdc).
- Пути cf/cfe → `openspec/project.md` + `.cursor/rules/project-paths.mdc`.
- Запрет ROI → `.cursor/rules/no-roi-estimates.mdc`; инфраструктура → `.cursor/docs/onec-infrastructure.md`.

**Ревью:** [`.cursor/docs/review-guide.md`](.cursor/docs/review-guide.md); `/review`, `/release-review`; протокол → `.cursor/skills/review/SKILL.md`.

**Доменные навыки 1С:** `1c-bsp`, `1c-extensions`, `1c-forms`, `1c-mxl`, `1c-roles`, `1c-query-optimization` — через `available_skills` и `.cursor/skills/*/SKILL.md`. Справочники: `.cursor/docs/platform/`, `.cursor/docs/standard/`.
