# Целостность поставки kit-van

Перед объявлением версии (version-cut) — системный проход. На приёмке срезов — только **дельта** затронутых файлов (optional hygiene), не полный независимый аудит постановки.

## Системный чеклист

1. **Манифест поставки:** на ветке поставки только `.cursor/**`, `AGENTS.md`, витринный `README.md`; нет `openspec/`, `doc/`, `tools/`; нет обязательных npm/Python deps. SSOT состава — `openspec/specs/kit-distribution/spec.md`.
1a. **Самодостаточность:** ссылки из `.cursor/**` не ведут за пределы `.cursor/` — исключение только файлы, которые создаёт `/init-project` в проекте (`openspec/project.md`, `openspec/specs/architecture.md`, `openspec/config.yaml`) и рабочие пути ЗНИ проекта (`openspec/changes/**`, `openspec/knowledge/**`, `openspec/adrs/**`). Заготовки — `.cursor/templates/seed/`.
2. **Связи:** commands ↔ skills ↔ rules ↔ `AGENTS.md` — нет осиротевших ссылок на удалённые пути.
3. **Язык чата:** учебные сценарии / handoff не требуют жаргона движка как единственного языка.
4. **Mode Gate / XML guard:** согласованы; Form assisted только через skill.
5. **Кейсбуки** отдельно от `std-*`.
6. **session-restore** не авто-запускает apply.
7. **Бюджет always-apply:** сумма `.cursor/rules/*.mdc` с `alwaysApply: true` плюс `AGENTS.md` **≤ 34 КБ**; полный бюджет чата — on-demand `chat-output-budget-full.mdc`.
8. **Тонкий AGENTS:** нет Decision tree; ссылка на `README.md`; вход исследования — `/opsx:explore`.
9. **README без лишнего:** нет `/opsx:intake`, `/opsx:debug`, пользовательских ключей команд (в т.ч. `--lite`).
10. **Отсутствие intake/debug:** нет `.cursor/commands/opsx-intake.md`, `opsx-debug.md`; нет каталогов `.cursor/skills/openspec-intake/`, `openspec-debug/`.
11. **Ориентиры commands/skills:** `init-project` — тонкий вход + SSOT `.cursor/docs/init-project-protocol.md`; топ-skills (verify/new/…) при обрезке — страховка `templates/` (см. `command-skill-gate.mdc`).
12. **Grep-критерий scrub:** в поставке `.cursor/` + корневые `AGENTS.md`/`README.md` — **0** рабочих рекомендаций `/opsx:intake`|`/opsx:debug` как входа (исторические CHANGELOG / change-отчёты — исключение).

См. также: [kit-template-workflow.md](./kit-template-workflow.md), [kit-as-submodule.md](./kit-as-submodule.md), [quick-start.md](./quick-start.md), [faq-kit.md](./faq-kit.md). Опциональные smoke-docs: [mxl-roundtrip-fixture.md](./mxl-roundtrip-fixture.md), [proportional-surface.md](./proportional-surface.md). Каталог `temp/fixtures/` создаётся локально при проверке (не часть поставки kit).
