# AGENTS.md — навигационный индекс

**Диспетчер 1С:** `.cursor/rules/1c-agent-delegation.mdc`. **Гейты:** `.cursor/rules/gate-dispatcher.mdc`. **Чат:** `.cursor/rules/chat-output-budget.mdc` + `.cursor/docs/chat-lexicon.md`. Рекомендуемый чат — Grok 4; модели субагентов — только `.cursor/rules/model-selection.mdc` (архитектор Opus 5, ревьюер Gemini, упрощение Composer).

**Поставка:** установка — `.cursor/docs/kit-as-submodule.md`; публикация (`/opsx:publish`) — `.cursor/docs/kit-template-workflow.md`. Памятка: `README.md` · `.cursor/docs/quick-start.md` · `.cursor/docs/faq-kit.md` · `.cursor/docs/delivery-integrity.md`.

## Команды

`.cursor/rules/sdd-workflow.mdc` — explore → new → verify → apply → verify → archive. Вход исследования: `/opsx:explore`.

`/opsx:explore`, `/opsx:new`, `/opsx:verify`, `/opsx:apply`, `/opsx:archive`, `/opsx:extend`, `/opsx:status`, `/opsx:explain`, `/opsx:overview`, `/opsx:knowledge-add`, `/opsx:knowledge-init`, `/opsx:knowledge-audit`, `/opsx:sync`, `/opsx:bulk-archive`, `/review`, `/release-review`, `/init-project`, `/session-save`, `/session-restore`, `/session-retro`, `/opsx:publish` (только репо kit).

Сценарии — `README.md`. Термины — `.cursor/docs/glossary.md`. Init — `.cursor/docs/init-project-protocol.md`. Схема отчёта архитектора — `.cursor/docs/architect-report-schema.md`. Слои маркеров — `.cursor/docs/marker-layers-guide.md`.

## Карта SSOT

- Профили чата → `model-adaptation.mdc` + `model-*.mdc`. HALT-жаргон → `chat-lexicon.md`. Бриф → `.cursor/docs/templates/brief-card.md`. Стиль авторов скиллов → `opsx-output-style.md`.
- HALT BSL → `1c-halt-triggers.mdc`. Pipeline → `1c-writer-pipeline.mdc`. XML → `1c-xml-write-guard.mdc`. Task/модели → `tool-name-guard.mdc` / `model-selection.mdc`. Агенты → `.cursor/agents/*.md`. Журнал → `.cursor/docs/agents-CHANGELOG.md`.
- Сессия → `session-discipline.mdc`. Context-strategy → `.cursor/skills/context-strategy/SKILL.md`. Отчёты субагентов → `preserve-subagent-reports.mdc`.
- Forms → `forms-mxl-mode-gate.mdc`. Архитектура / RCA → `architect-gate.mdc` / `verified-cause-gate.mdc`. Specs/срезы → `openspec-specs-gate.mdc` / `vertical-slices.mdc`. AP → `bsl-antipatterns.mdc`.
- ADR → `openspec/adrs/` + `adr-format.mdc`. KB → `openspec/knowledge/` + `knowledge-format.mdc`. Маркеры → `marker-canon.md`. Пути cf/cfe → `openspec/project.md` (после `/init-project`; в kit нет) + `capture-to-project.mdc` + `project-paths.mdc`.
- Ревью: `.cursor/docs/review-guide.md`; `/review`; `.cursor/skills/review/SKILL.md`. Disposition — `openspec/specs/review-quality-disposition/spec.md`, ADR-0003.
