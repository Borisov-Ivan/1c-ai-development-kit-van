# Целостность поставки kit-van

Перед объявлением версии (version-cut) — системный проход. На приёмке срезов — только **дельта** затронутых файлов (optional hygiene), не полный независимый аудит постановки.

## Системный чеклист

1. **Copy-smoke:** копируются только `.cursor/` + `AGENTS.md`; нет обязательных npm/Python deps.
2. **Связи:** commands ↔ skills ↔ rules ↔ `AGENTS.md` — нет осиротевших ссылок на удалённые пути.
3. **Язык чата:** учебные сценарии / handoff не требуют жаргона движка как единственного языка.
4. **Mode Gate / XML guard:** согласованы; Form assisted только через skill.
5. **Кейсбуки** отдельно от `std-*`.
6. **session-restore** не авто-запускает apply.
7. **Бюджет always-apply:** сумма `.cursor/rules/*.mdc` с `alwaysApply: true` плюс `AGENTS.md` **≤ 34 КБ**; полный бюджет чата — on-demand `chat-output-budget-full.mdc`.
8. **Тонкий AGENTS:** нет Decision tree; ссылка «Сценарии» ведёт внутрь `.cursor/` (`.cursor/docs/quick-start.md`); глоссарий — `.cursor/docs/glossary.md`; вход исследования — `/opsx:explore`.
9. **README без лишнего:** нет `/opsx:intake`, `/opsx:debug`, пользовательских ключей команд (в т.ч. `--lite`). README описывает устройство репозитория и веток, не дублирует таблицы сценариев.
10. **Отсутствие intake/debug:** нет `.cursor/commands/opsx-intake.md`, `opsx-debug.md`; нет каталогов `.cursor/skills/openspec-intake/`, `openspec-debug/`.
11. **Ориентиры commands/skills:** `init-project` — тонкий вход + SSOT `.cursor/docs/init-project-protocol.md`; топ-skills (verify/new/…) при обрезке — страховка `templates/` (см. `command-skill-gate.mdc`).
12. **Grep-критерий scrub:** в поставке `.cursor/` + корневые `AGENTS.md`/`README.md` — **0** рабочих рекомендаций `/opsx:intake`|`/opsx:debug` как входа (исторические CHANGELOG / change-отчёты — исключение).
13. **Дисциплина веток:** `git log develop..main` содержит только merge-коммиты публикации и cleanup-коммиты снятия архивов/утилит; содержательных прямых коммитов на `main` нет.
14. **Состав `main`:** нет каталога `openspec/` (specs/ADR/архивы живут на `develop`), нет `tools/`; заготовка шаблона ЗНИ — `.cursor/templates/seed/`.
15. **Фильтр охвата маркеров:** в скилле реализации нет путей конкретной выгрузки как классификатора; класс — сегменты `cf`/`cfe` в путях этой ЗНИ.

См. также: [kit-template-workflow.md](./kit-template-workflow.md), [quick-start.md](./quick-start.md), [faq-kit.md](./faq-kit.md). Опциональные smoke-docs: [mxl-roundtrip-fixture.md](./mxl-roundtrip-fixture.md), [proportional-surface.md](./proportional-surface.md). Каталог `temp/fixtures/` создаётся локально при проверке (не часть поставки kit).
