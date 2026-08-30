# Ревью связности слоёв kit

Ось: команда → скилл → шаблоны → агенты → спеки. Только чтение, правок нет.

---

## Команды vs индекс

**Файлы `.cursor/commands/` (20):**  
`opsx-explore`, `opsx-new`, `opsx-verify`, `opsx-apply`, `opsx-archive`, `opsx-extend`, `opsx-status`, `opsx-explain`, `opsx-overview`, `opsx-sync`, `opsx-bulk-archive`, `opsx-knowledge-add`, `opsx-knowledge-init`, `opsx-knowledge-audit`, `review`, `release-review`, `init-project`, `session-save`, `session-restore`, `session-retro`.

**Список в `AGENTS.md` (секция OpenSpec Workflow):**  
`/opsx:explore`, `/opsx:new`, `/opsx:verify`, `/opsx:apply`, `/opsx:archive`, `/opsx:extend`, `/opsx:status`, `/opsx:knowledge-add`, `/opsx:knowledge-init`, `/opsx:knowledge-audit`, `/opsx:sync`, `/opsx:bulk-archive`, `/review`, `/release-review`, `/init-project`, `/session-save`, `/session-restore`, `/session-retro`.

| Расхождение | Деталь |
|-------------|--------|
| Команды без файла | Нет. Все имена из `AGENTS.md` имеют файл. |
| Файлы без индекса `AGENTS.md` | **`/opsx:explain`**, **`/opsx:overview`**. В `README.md` (таблица «Команды») их тоже нет. `quick-start.md` знает explain; overview нет ни в README, ни в quick-start. `sdd-workflow.mdc` тоже молчит. Спека `rules-hygiene` требует: «список команд в AGENTS.md актуален». |
| Неверный `SKILL.md` | Не найдено. Все workflow-команды указывают на свой скилл. |
| Исключение по дизайну | `/init-project` → `.cursor/docs/init-project-protocol.md`, не `SKILL.md`. Совпадает с `command-skill-gate.mdc` (гейт срабатывает только если команда велит Read скилла). |

**Пути скиллов — все верные:**

| Команда | SKILL / протокол |
|---------|------------------|
| `/opsx:explore` | `openspec-explore/SKILL.md` |
| `/opsx:new` | `openspec-new-change/SKILL.md` |
| `/opsx:verify` | `openspec-verify-change/SKILL.md` |
| `/opsx:apply` | `openspec-apply-change/SKILL.md` |
| `/opsx:archive` | `openspec-archive-change/SKILL.md` |
| `/opsx:extend` | `openspec-extend-change/SKILL.md` |
| `/opsx:status` | `openspec-status/SKILL.md` |
| `/opsx:explain` | `openspec-explain/SKILL.md` |
| `/opsx:overview` | `openspec-overview/SKILL.md` |
| `/opsx:sync` | `openspec-sync-specs/SKILL.md` |
| `/opsx:bulk-archive` | `openspec-bulk-archive-change/SKILL.md` |
| `/opsx:knowledge-*` | соответствующие `openspec-knowledge-*/SKILL.md` |
| `/review`, `/release-review` | `review/SKILL.md` (+ флаг `release_mode`) |
| `/session-*` | `session-save` / `session-restore` / `session-retro` |
| `/init-project` | docs-протокол |

**Подсказка `-noapi` (спека session-api-mode):** строка есть у explore / new / verify / apply / extend / review / release-review. У status / sync / knowledge / session — нет, это совпадает со сценарием «команда без дорогих вызовов молчит». Пробел: **`opsx-archive.md`** — внутренний прогон verify зовёт архитектора, но строки про ключ нет (спека перечисляет дорогие команды без archive).

Устаревших файлов `opsx-ff.md` / `opsx-continue.md` в палитре нет — `rules-hygiene` здесь соблюдён.

---

## Скиллы: внутренняя целостность

Entry Protocol **именован** у: explore, extend (user-extend), explain, overview. У new / verify / apply / archive / status / review / session-* — роль EP играют «первые шаги»; `session-discipline.mdc` это допускает («Entry Protocol / первым шагам»). С бюджетом чата (B0–B3, B-explain, halt жаргона, pause-wait) основные скиллы согласованы.

**K1 — critical.** `.cursor/rules/1c-agent-delegation.mdc` (always-apply таблица делегирования).  
Цитата: «Ошибка с трассой/стеком | **onec-code-trace-analyst**».  
Агента с таким `name` нет. Живой файл — `onec-trace-analyst`. В том же always-apply файле правильного имени нет. `1c-error-analysis.mdc` и `tool-name-guard.mdc` пишут верно. Риск: оркестратор по таблице вызовет несуществующий `subagent_type`.

**K2 — high.** `.cursor/skills/openspec-new-change/SKILL.md` (обработка `failed`).  
Цитата: «For `failed`: Retry once. If retry fails, inform the user "Агент недоступен, делаю упрощённый вариант сам / откладываю" … or create minimal scaffold.»  
Противоречит `model-selection.mdc` / спеке `subagent-model-mapping`: цепочка = Primary → вызов **без** `model=`; после исчерпания — стоп, **не** подмена отчёта субагента текстом оркестратора.

**K3 — high.** `.cursor/skills/1c-agent-patterns/SKILL.md` § «ПРИ ОШИБКЕ ВЫЗОВА АГЕНТА».  
Цитата: «Если имя инструмента верное — повторить вызов Task 1 раз. … Если retry не помог — СТОП.»  
Нет шага «тот же `subagent_type` без `model=`». Для reviewer / architect / simplifier это ломает двухшаговую цепочку.

**K4 — high.** `.cursor/skills/openspec-new-change/SKILL.md` → `templates/brief-card.md`.  
Цитата: «бриф по `templates/brief-card.md` (§5.1 Sync Card)».  
В `openspec-new-change/templates/` есть только `handoff-contract.md`. Реальный бриф — `.cursor/docs/templates/brief-card.md`. При обрезке SKILL страховка `command-skill-gate` этот файл не подгрузит.

**K5 — medium.** `command-skill-gate.mdc` vs verify-шаблоны.  
Страховка обрезки велит читать `card-decision.md`, `card-hygiene.md`, `info-section.md`, `executive-summary.md`…  
Актуальный чат-SSOT verify — `verdict-card.md` + `chat-summary.md`; в списке страховки их **нет**. `conversation-shape.md` из SKILL не вызывается. Карточки hygiene/decision живы как файловые куски, но чат уже на `decision-block.md`.

**K6 — medium.** `AskUserQuestion` vs `AskQuestion`.  
`AskUserQuestion`: `openspec-apply-change/SKILL.md` (выбор change), `openspec-status/SKILL.md`, `openspec-sync-specs/SKILL.md`, `openspec-bulk-archive-change/SKILL.md`.  
Остальные скиллы — `AskQuestion`. Инструмент среды — `AskQuestion`. Риск срыва выбора change на apply/status/sync/bulk-archive.

**K7 — medium.** `.cursor/skills/openspec-apply-change/SKILL.md`.  
Цитата: `Always announce: "Using change: <name>"`.  
Английский каркас в чат-инструкции. Ломает ADR-0006 / `chat-surface-clarity` (progress и вводная `/opsx:*` только по-русски) и non-events (имя change — не отдельный служебный ping).

**K8 — medium.** `README.md` сценарий «Форма или макет».  
Цитата: «на `/opsx:new` выбрать **режим правки**: вручную (по умолчанию), со скриптом или только кодом модуля».  
Спеки `split-form-layout-modes` и `chat-surface-clarity`: Mode Gate на new — **только форма**; макет на new не спрашивается. FAQ уже правильный; README смешивает форму и макет.

**K9 — medium.** `sdd-workflow.mdc`.  
Цитата: «verify оценивает когерентность срезов (Quality Controller, **6 критериев**)».  
QC в verify SKILL: критерии 1–6, 8, **8b**, 9–11 (не шесть).

**K10 — low.** Writer-шаблон vs «ЧТО, не КАК».  
`1c-agent-patterns/writer.md` §7 самоконтроль: «Каждая Попытка обоснована внешним фактором (rule 20)».  
`1c-writer-pipeline.mdc` § ПРОМПТ WRITER запрещает оркестратору вкладывать обоснование Попытки в промпт. Частично смягчено блоком `ORCHESTRATOR_IMPLEMENTATION_GATE` («подсказка, не директива»).

**K11 — low.** Deprecated-стабы explore: `cycle.md`, `compose.md`, `profiles/doc.md`. Помечены «не использовать», из routing SKILL убраны. Шум при обрезке/Glob, не живой протокол.

**K12 — low.** Именованный Entry Protocol нет у apply / verify / archive / status / session-* / review. Для persistence это «первые шаги», не дыра; но verify/apply длинные, и «где стоп до брифа» читается хуже, чем у explore/extend.

**Шаблоны, упомянутые в SKILL и существующие:** explain (5/5 + fixtures), overview (2 templates + 3 fixtures), apply pause-wait chat/file, explore `handoff-block.md`, new `handoff-contract.md`, verify `verdict-card` / `chat-summary` / `layer-1-hygiene-table` / `executive-summary` / `report-header`. Битых ссылок на несуществующие файлы шаблонов, кроме K4, не видно.

**Согласование с session-discipline / chat-output-budget:** explore B3 + END TURN, extend B1/B2, explain B-explain, verify verdict-card + одно финальное сообщение + исключение канона лимита, apply pause-wait — совпадают с бюджетом. Канон «дорогие модели недоступны — дальше на модели чата» есть в stub бюджета §5.

---

## Агенты vs SSOT моделей

**`.cursor/agents/` (7), все `model: inherit`:**  
`onec-code-architect`, `onec-code-writer`, `onec-code-explorer`, `onec-code-reviewer`, `onec-code-simplifier`, `onec-trace-analyst`, `openspec-quality-controller`.

Поле `tools:` ни у кого не задано (наследование инструментов платформы). `model-selection.mdc` этого не требует.

**Таблица ролей vs frontmatter:** совпадает. Primary: architect `claude-opus-5-thinking-high`, reviewer `gemini-3.1-pro`, simplifier `composer-2.5-fast`; writer / explorer / trace-analyst / QC — без `model=`. Слаги есть в текущем enum `Task.model`. Fable — закрытая эскалация, не Primary.

**Упомянуты, файла нет:** `onec-code-trace-analyst` — только K1 (опечатка в always-apply). Других «призраков» нет.

**Файлы агентов, не упомянутые в правилах:** нет. Все семь есть в `model-selection` и `tool-name-guard`.

**`tool-name-guard.mdc`:** 1С-набор + generic `generalPurpose` / `explore` / `shell` + QC. Платформенные `cursor-guide`, `ci-investigator`, `bugbot`, `security-review`, `best-of-n-runner` не перечислены — не кастом kit; для 1С-контента их и не должно быть. Не пробел SSOT.

**INPUT CONTRACT writer vs pipeline / § ПРОМПТ WRITER:**

| Тема | Согласовано? |
|------|----------------|
| ЧТО / не КАК | Да: якорь в delegation, полное тело в `1c-writer-pipeline.mdc`, агент не дублирует yaml оркестратора. |
| Блоки INPUT CONTRACT | Да: pipeline § INPUT CONTRACT отсылает к таблице агента. |
| Project paths **Always** + HALT `MISSING_INPUT:project_paths` | **Расхождение.** Delegation: «в kit-репозитории отсутствует — блок путей опускается». Writer: отсутствие блока = HALT. В проекте 1С с `project.md` ок; в kit-only apply с writer — ловушка. |
| Шаблоны `writer.md` вставляют Project paths + BSL_LSP | Да, кроме kit-omit. |
| Root cause / EXTENSION_GUARD / Resolved Contracts | Согласованы с pipeline и verified-cause. |

Simplifier и QC в глоссарии «Агенты 1С» не названы (см. секцию «Глоссарий»).

---

## Спеки vs реализация

| Спек | Носители | Пробелы |
|------|----------|---------|
| **chat-model-profiles** | `model-adaptation.mdc`, `model-grok4.mdc` / `fable5` / `gpt56` / `opus5`, stub в `AGENTS.md`, carve-out языка в grok4 и бюджете §6 | Существенных нет. Пирамида и MAY/MUST NOT на месте. |
| **chat-surface-clarity** | `chat-output-budget.mdc` (+full), `opsx-output-style.md`, `brief-card.md`, `chat-lexicon.md`, `pause-wait-chat.md` / `pause-wait-file.md`, FAQ Mode Gate | README смешивает форму и макет на new (K8). Apply «Using change» (K7). Эталон FAQ — ок. |
| **sequential-gate-questions** | `openspec-new-change/SKILL.md` §1.5 / 1.55 (один вопрос за ход, Mode на design, kit-only → `n/a`), apply при непустом `marker_scope` | Носитель есть, ADR-0007 отражён. Сценарий «в карточке ЗНИ сразу стоит, что маркеры не применяются» закрыт записью `n/a` в proposal, не отдельной чат-карточкой — допустимо. |
| **session-api-mode** | `model-selection.mdc` § режим сессии, `session-discipline.mdc` cue, бюджет §5 канон, FAQ, строки `-noapi` в дорогих командах | Archive зовёт дорогой verify, подсказки в команде нет. Спека перечисляет набор без archive — дыра с обеих сторон. |
| **subagent-model-mapping** | `model-selection.mdc`, `tool-name-guard.mdc`, `1c-agent-patterns/SKILL.md` (ссылка на SSOT) | K2/K3: new и patterns всё ещё «Retry once» / «упрощённый вариант сам». Frontmatter `inherit` и таблица ролей — ок. |
| **delegation-safeguards** | `tool-name-guard`, `1c-agent-delegation` (запрет explore/GP, два отказа, якорь), `1c-agent-patterns` intent-бриф, coverage-first reviewer | Имя trace-агента в always-apply таблице неверно (K1). |
| **always-apply-context-budget** | `gate-dispatcher.mdc`, якоря в delegation, пометка kit/`project.md` в AGENTS | Бюджет 34 КБ в этом проходе не замерялся. |
| **rules-hygiene** | шапки «Когда загружать» у halt-triggers / task-triage / tool-name-guard и др. | Индекс команд в AGENTS.md **не** актуален (нет explain/overview). |
| **review-quality-disposition** | `onec-code-reviewer.md` § DESIGN AUTHORITY, `review/SKILL.md` шаг 4.5, ADR-0003, `review-guide.md`, якорь apply-reviewer в delegation | Существенных пробелов нет. |
| **hardcode-justification-gate** | `bsl-antipatterns.mdc` AP-055, architect/writer/reviewer контуры | Носитель реестра есть. |
| **split-form-layout-modes** | `forms-mxl-mode-gate.mdc`, new шаг 1.55, apply Forms mode / mxl permission, FAQ | README (K8). |
| **explain-post-implementation-scope** | `review/SKILL.md` § Explain scope, apply `code-map.md` + handoff, `openspec-explain/SKILL.md` prefill, ADR-0002 | Команда explain есть, в AGENTS/README её нет — пользовательский вход слабее носителя. |

Свежие пять спек в правилах/скиллах **в целом посажены**; самые опасные разрывы — индекс команд, опечатка агента трассы, retry без второго шага цепочки.

---

## ADR

Индекс `openspec/adrs/README.md` **актуален**: ADR-0001…0007, статусы и даты совпадают с файлами. Пропущенных файлов в таблице нет.

| ADR | Правила | Вердикт |
|-----|---------|---------|
| **0001** Load-Bearing, chat-facing vs agent-facing | бюджет §7, lexicon, brief-card, Mode Gate FAQ | Держится. Утечки: K7 (английский announce), K8 (README). |
| **0002** explain scope | review + apply + explain skill | Держится в протоколе; дыра в индексе команд. |
| **0003** QualityFlag / Disposition | reviewer + review skill + apply carve-out | Держится. |
| **0004** Load-Bearing, режим API | `model-selection` + FAQ + строки в командах | Держится. Archive без подсказки — мелочь. |
| **0005** канон в том же ходе | бюджет stub §5 дословно; verify исключение из «одно сообщение» | Согласовано с ADR, не противоречит. |
| **0006** русский progress, профиль не сильнее бюджета | бюджет §6 + §1b п.10, grok4 MUST NOT | Согласовано. K7 — локальное нарушение в apply SKILL. |
| **0007** маркер только если будет BSL | new §1.5 kit-only / сомнение; apply `n/a` не в код | Согласовано со спекой sequential-gate. |

Противоречий «ADR принят, правило делает обратное» по 0005–0007 нет, кроме точечных утечек chat-facing (0001/0006) и отставания индексов.

---

## Глоссарий

`openspec/glossary.md` объявлен SSOT терминов workflow. Расхождения:

**Устарело (есть в глоссарии, в рантайме нет):**
- **ff (fast-forward)** и **new + continue** — команды удалены (`/opsx:new` = единственный вход). Changelog это знает; глоссарий — нет. Строка workflow: «explore → new/**ff** → verify…».
- **slice-gate** как термин для чата — в бюджете имена гейтов в чат запрещены; в глоссарии термин нужен для агент-слоя, но пометки «не в чат» нет.

**Нет в глоссарии, в правилах ключевые:**
- режим сессии «с API / без API», токены `-noapi`/`-api`, канон лимита;
- pause-wait / pause-decision;
- уровни брифа B0–B3 / B-explain;
- kit-only / `developer: n/a` / `marker_scope`;
- QualityFlag / Disposition (as-designed, queue-fix);
- `openspec-quality-controller`, `onec-code-simplifier` (в «Агенты 1С» только пять ролей);
- `/opsx:explain`, `/opsx:overview`, `/opsx:status`.

**Используется консистентно:** ЗНИ, срез, `S<N>.accept`, Repair Loop, оркестратор, cf/cfe, phantom-symbol, маркеры `+++`/`---`.

---

## Рекомендации

**R1.** `.cursor/rules/1c-agent-delegation.mdc` строка таблицы делегирования: заменить `onec-code-trace-analyst` → `onec-trace-analyst`. Прогнать grep по репо на старое имя (сейчас единственное вхождение).

**R2.** `AGENTS.md` (список команд) и `README.md` (таблица «Команды» + сценарии): добавить `/opsx:explain` и `/opsx:overview`. В `sdd-workflow.mdc` — хотя бы строка «дополнительно». Закрывает `rules-hygiene` и дыру explain-spec.

**R3.** `openspec-new-change/SKILL.md` и `1c-agent-patterns/SKILL.md` § ошибка вызова: выровнять с `model-selection.mdc` — шаг 2 = тот же агент **без** `model=`; запрет «сам напишу отчёт / scaffold как замену»; стоп только после исчерпания цепочки.

**R4.** `openspec-new-change/SKILL.md`: путь брифа → `.cursor/docs/templates/brief-card.md`. В `command-skill-gate.mdc` для verify добавить `verdict-card.md` и `chat-summary.md`; hygiene/decision оставить как файл-слой или явно пометить agent-only.

**R5.** Заменить `AskUserQuestion` на `AskQuestion` в apply / status / sync / bulk-archive (скилл + команда status).

**R6.** `openspec-apply-change/SKILL.md`: убрать английский `Always announce: "Using change…"`. Имя change — в финальном русском снимке, не отдельным ping.

**R7.** `README.md` сценарий формы/макета: Mode Gate на new — только управляемая форма; макет — на apply. Скопировать смысл из FAQ.

**R8.** `openspec/glossary.md`: вычеркнуть ff / continue; дописать режим API, pause-wait, B0–B3, kit-only, QC/simplifier, explain/overview. Строка workflow = `explore → new → verify → apply → verify → archive`.

**R9.** `sdd-workflow.mdc`: «6 критериев» QC → актуальный набор (включая 8b).

**R10.** Writer INPUT CONTRACT: для kit без `project.md` — не Always-HALT, а «блок или явная пометка omit», в одну линию с delegation § PROJECT PATHS.

**R11.** `.cursor/commands/opsx-archive.md`: одна строка, что `-noapi`/`-api` пишутся в любом сообщении (внутренний verify дорогой). Либо явно исключить archive из «команд с дорогими вызовами» в спеке — сейчас ни то ни другое.

**R12.** `1c-agent-patterns/writer.md` §7: самопроверку Попытки оставить в системном промпте агента, не собирать оркестратором в Task-промпт (граница ЧТО/КАК).