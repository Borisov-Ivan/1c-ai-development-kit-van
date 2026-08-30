Проверил указатели в `AGENTS.md`, `.cursor/rules`, `.cursor/commands`, `.cursor/skills/**/SKILL.md` + `templates/`, `.cursor/agents`, `.cursor/docs` (верх) и `.cursor/docs/templates`. Каталоги `docs/platform/` и `docs/standard/` как справочники не разбирал; ссылки **на** них проверены.

Ниже только то, что ломает навигацию агента. Плейсхолдеры (`YYYY-MM-DD`, `<name>`), артефакты ЗНИ (`proposal.md` / `design.md`) и заведомо отсутствующий в kit `openspec/project.md` в таблицы не попали.

## Сломанные ссылки на файлы

| Источник | Целевой путь | Статус |
|---|---|---|
| `.cursor/rules/1c-agent-delegation.mdc:84` | агент `onec-code-trace-analyst` | **файла нет**. Канон: `onec-trace-analyst` (`.cursor/agents/onec-trace-analyst.md`, так же в `tool-name-guard.mdc` / `1c-error-analysis.mdc` / `1c-halt-triggers.mdc`) |
| `.cursor/docs/onec-infrastructure.md:27` | `docs/onec-dev-container.md` | **нет** ни в корне, ни в `.cursor/docs/` |
| `.cursor/docs/delivery-integrity.md:20` | `temp/fixtures/README.md` | **нет** каталога `temp/fixtures/` |
| `.cursor/docs/proportional-surface.md:21` | `temp/fixtures/README.md` + `temp/fixtures/proportional-surface-noisy-module.bsl` | **нет** |
| `.cursor/docs/mxl-roundtrip-fixture.md:3` | `temp/fixtures/README.md` | **нет** |
| `.cursor/rules/chat-output-budget-full.mdc:31` | `templates/explain-report.md` | **нет от rules/**. Реальный файл: `.cursor/skills/openspec-explain/templates/explain-report.md` |
| `.cursor/rules/chat-output-budget-full.mdc:75` | `pause-wait-file.md` (без базы) | **нет от rules/**. Файл есть: `.cursor/skills/openspec-apply-change/templates/pause-wait-file.md` |
| `.cursor/skills/openspec-overview/templates/customer-overview.md:6–8` | `fixtures/golden-88781-overview.md`, `fixtures/voice-good-stage.md`, `templates/style-checklist.md` | эталоны лежат в **`../fixtures/`**; `style-checklist.md` — **сосед** в `templates/`, не `templates/templates/` |
| `.cursor/skills/openspec-explain/templates/exit-card.md:3` | `fixtures/voice-good-exit.md` | файл есть в `../fixtures/`, из `templates/` путь не резолвится |
| `.cursor/skills/openspec-explain/templates/point-card.md:3` | `fixtures/voice-good-point.md` | то же |
| `.cursor/commands/init-project.md:8`, `.cursor/docs/init-project-protocol.md:416+` | `openspec/specs/architecture.md` | **нет в kit** (в `knowledge-init` чтение помечено «если есть»; в init-project — как обязательный ориентир) |
| `.cursor/rules/capture-to-project.mdc:19` | `openspec/config.yaml` | **нет в kit** (ожидаемый артефакт проекта, в карте SSOT это не оговорено так же явно, как для `project.md`) |
| `.cursor/docs/delivery-integrity.md:16` | `.cursor/commands/opsx-intake.md`, `opsx-debug.md` | **нет** — это чеклист *отсутствия*, не рабочая ссылка |

`openspec/project.md` из `AGENTS.md:53` — намеренно отсутствует в kit. Не дефект.

Относительные `templates/*.md` в `command-skill-gate.mdc:29–30` валидны **только** после Read соответствующего `SKILL.md` (файлы `card-decision.md`, `handoff-contract.md` и др. на месте). С корня репозитория не резолвятся.

## Сломанные ссылки на секции

Запрошенные якоря **живые**:

| Файл | Секция / шаг | Есть? |
|---|---|---|
| `1c-halt-triggers.mdc` | LIGHT MODE, MECHANICAL MODE, ИСКЛЮЧЕНИЯ | да (`## LIGHT MODE`, `## MECHANICAL MODE`, `## ИСКЛЮЧЕНИЯ`) |
| `1c-writer-pipeline.mdc` | LINT GATE, ПРОМПТ WRITER, IDENTIFIER HYGIENE CHECK | да |
| `review/SKILL.md` | 1.8, 1.9, 1.10, 3.5, 4.5, 6.4 | да |
| `opsx-output-style.md` | §5.1, §2.6, §5.1a, §5.2 | да (`### 5.1`, `## 2.6`, `### 5.1a`, `### 5.2`) |
| `chat-output-budget-full.mdc` | §1, §1b, §1c, §3a, §4, §5, §6, §7 | да |
| шаблоны pause-wait / entry-brief / brief-card / decision-block / marker-canon / chat-lexicon / kit-template-workflow / delivery-integrity / quick-start / faq-kit | файлы | все существуют |

Реальные разрывы секций:

| Источник | Цель | Статус |
|---|---|---|
| `.cursor/rules/verify-user-communication.mdc:62` | `chat-output-budget.mdc` §**5a** | в **stub** есть только `### Subagent (§5)`. `#### 5a` — в **full** (`chat-output-budget-full.mdc:159`) |
| `.cursor/skills/openspec-apply-change/templates/pause-wait-chat.md:5` | `chat-output-budget.mdc` §**1d** | в stub **нет** §1d; в full есть `### 1d` (строка 58) |
| `.cursor/rules/chat-output-budget-full.mdc:49` и `:93` | два разных заголовка **`### 1c`** | якорь §1c **двусмыслен** (карта правок vs тест понятности) |
| `review/SKILL.md` | шаг **1.8** | текст есть, но **после** 1.9 (стр. 227) и 1.10 (стр. 259): шаг 1.8 на стр. 288. Поиска «шаг 1.8» хватает, линейное чтение сбивает |
| `review/SKILL.md` | шаг **1.7** | **нет** (прыжок 1.6 → 1.9). Сейчас на 1.7 никто не ссылается |

Ложные срабатывания парсера (не чинить как битые секции): «`1c-halt-triggers.mdc` § LIGHT MODE / MECHANICAL MODE» — две секции в одной фразе; `reviewer-checks.md` Phase 2.5 — секция есть (`.cursor/docs/standard/reviewer-checks.md:697`).

## Отсутствующие агенты/команды/скиллы

**Агенты на диске (7):** `onec-code-architect`, `onec-code-explorer`, `onec-code-reviewer`, `onec-code-writer`, `onec-code-simplifier`, `onec-trace-analyst`, `openspec-quality-controller`.

| Упоминание | Файл агента | Вердикт |
|---|---|---|
| `onec-code-trace-analyst` в таблице делегирования | нет | **рассинхрон имени** (см. выше) |
| `onec-code-architect-2nd`, `openspec-doc-writer` | нет | только `agents-CHANGELOG.md`; из ротации сняты **намеренно** |

**Команды `AGENTS.md:14` ↔ `.cursor/commands/` ↔ `SKILL.md`:** все перечисленные в индексе имеют command-файл и скилл. `/init-project` скилла не имеет — протокол `.cursor/docs/init-project-protocol.md` (так задумано).

| Разрыв | Суть |
|---|---|
| `/opsx:explain`, `/opsx:overview` | command + skill **есть**, в списке команд `AGENTS.md:14` **нет** |
| `.cursor/skills/1c-help-mcp/`, `mcp-tools/`, `openspec-onboard/` | **пустые каталоги**, `SKILL.md` нет, из правил не ссылаются |

Доменные скиллы из `AGENTS.md:58` (`1c-bsp`, `1c-extensions`, `1c-forms`, `1c-mxl`, `1c-roles`, `1c-query-optimization`) на месте. `1c-vendor-standards`, `context-strategy`, `stop-slop`, `1c-agent-patterns` — тоже есть, в строке «доменные навыки» не перечислены (это индекс, не обязательно дыра).

Ссылки навигатора `.cursor/docs/standard/1c-standards-navigator.md` на `std-01`…`std-12` — файлы есть.

## Осиротевшие файлы

Строгий критерий: basename **нигде** не упомянут среди правил/команд/скиллов/агентов/доков/AGENTS.md, и правило не `alwaysApply`.

- **`.cursor/rules/`:** осиротевших нет. Always-apply: `1c-agent-delegation.mdc`, `chat-output-budget.mdc`, `gate-dispatcher.mdc`, `session-discipline.mdc`.
- **`.cursor/docs/templates/`:** `brief-card.md` и `decision-block.md` входят в карту SSOT.

Не осиротели, но **выпали из карты `AGENTS.md`** (входящие ссылки есть):

| Файл | Кто ссылается |
|---|---|
| `.cursor/docs/architect-report-schema.md` | `onec-code-architect.md` |
| `.cursor/docs/bsl-comment-formats-project.md`, `marker-layers-guide.md` | `marker-canon.md`, `1c-coding-standards.md` |
| `.cursor/docs/init-project-protocol.md` | `delivery-integrity.md`, команда init-project |
| `.cursor/docs/mxl-roundtrip-fixture.md`, `proportional-surface.md` | `delivery-integrity.md` |
| `.cursor/docs/ux-acceptance-isolated-chat.md` | `opsx-output-style.md:200` |
| `.cursor/docs/agents-CHANGELOG.md` | `AGENTS.md:35` (есть в индексе) |

Пустые каталоги скиллов — фактические сироты (см. выше).

## Рекомендации

**R1.** В `.cursor/rules/1c-agent-delegation.mdc:84` заменить `onec-code-trace-analyst` на `onec-trace-analyst`. Это единственный активный указатель на несуществующий `subagent_type`.

**R2.** В `AGENTS.md` (блок команд, строка 14) добавить `/opsx:explain` и `/opsx:overview` — иначе индекс SSOT врёт относительно `.cursor/commands/`.

**R3.** Либо дописать в stub `chat-output-budget.mdc` якоря §1d и §5a (хотя бы одна строка-указатель на full), либо поменять ссылки в `pause-wait-chat.md` и `verify-user-communication.mdc` на `chat-output-budget-full.mdc`.

**R4.** В `chat-output-budget-full.mdc` переименовать один из двух `### 1c` (карта правок ≠ тест понятности). Сейчас любой «см. §1c» двусмыслен.

**R5.** В `review/SKILL.md` вернуть порядок шагов 1.8 → 1.9 → 1.10 (сейчас 1.8 стоит после 1.10).

**R6.** Починить относительные пути эталонов: в overview/explain `templates/` писать `../fixtures/…`; `style-checklist.md` без префикса `templates/`. В full-бюджете — полные пути к `explain-report.md` и `pause-wait-file.md`.

**R7.** `onec-infrastructure.md`: убрать или заменить `docs/onec-dev-container.md`. Smoke-ссылки на `temp/fixtures/README.md` — либо завести stub, либо пометить «создаётся локально», как уже сделано в `mxl-roundtrip-fixture.md` для JSON.

**R8.** Удалить пустые `.cursor/skills/1c-help-mcp/`, `mcp-tools/`, `openspec-onboard/` либо восстановить `SKILL.md` и вписать в индекс.

**R9.** Для `openspec/specs/architecture.md` и `openspec/config.yaml` — та же оговорка, что у `project.md`: «в kit нет, появляется после `/init-project`». Иначе init-project выглядит как битая ссылка.

**R10.** Добавить в карту SSOT `AGENTS.md` хотя бы по строке на `init-project-protocol.md`, `architect-report-schema.md`, `marker-layers-guide.md` — сейчас навигатор их не знает, хотя на них опираются агент и протокол.init.