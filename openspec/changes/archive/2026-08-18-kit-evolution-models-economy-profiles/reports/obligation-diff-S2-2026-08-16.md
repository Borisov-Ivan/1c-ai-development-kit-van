# Обязательство-diff S2 — Диета always-apply

**Change:** kit-evolution-models-economy-profiles  
**Дата:** 2026-08-16  
**Scenario:** «Обязательство-diff без непокрытых строк»

Каждая строка — обязательство разжалованного или удалённого always-apply файла и его якорь, который остаётся в постоянном контексте.

| Файл (было always-apply) | Обязательство | Якорь always-apply | Cue / on-demand |
|---|---|---|---|
| `command-skill-gate.mdc` | Первый tool call командной сессии — только Read `SKILL.md`; не читать файлы пользователя до Entry Protocol | `session-discipline.mdc` § Command → Skill | `gate-dispatcher.mdc`; файл остаётся on-demand |
| `command-skill-gate.mdc` | Страховка обрезки большого `SKILL.md` — дочитать `templates/*.md` | `session-discipline.mdc` § Command → Skill (страховка) | полный перечень шаблонов — в самом `command-skill-gate.mdc` |
| `command-session-persistence.mdc` | Протокол команды на каждом ходе; свободный режим внутри команды недоступен | `session-discipline.mdc` § Persistence | on-demand файл |
| `command-session-persistence.mdc` | Gate check: активная команда, ограничения скилла, СТОП при нарушении | `session-discipline.mdc` § Persistence (Gate check) | on-demand файл |
| `command-session-persistence.mdc` | TodoWrite checkpoint (`in_progress` закрыть до нового действия) | `session-discipline.mdc` § Persistence (TodoWrite checkpoint) | on-demand файл |
| `command-session-persistence.mdc` | Antipattern: explore «создай ЗНИ» / Grep `.bsl` сам; apply «а может лучше?» | `session-discipline.mdc` § Anti-patterns | расширенная таблица — в on-demand persistence |
| `context-strategy-gate.mdc` | TRIGGER 3+ файлов / XML\|CSV\|JSON / код 500+ / «береги контекст» → Read context-strategy до массового чтения; BYPASS 1–2 файла <150 | `session-discipline.mdc` § Context Strategy | `gate-dispatcher.mdc`; on-demand файл |
| `1c-xml-write-guard.mdc` | Сырой Write/StrReplace/Delete XML метаданных 1С в `src/` запрещён | `1c-agent-delegation.mdc` § XML WRITE GUARD | `gate-dispatcher.mdc`; полный шаблон инструкции — on-demand `1c-xml-write-guard.mdc` (`globs: src/**/*.xml`) |
| `bsl-write-guard.mdc` (удалён) | Оркестратор не пишет `.bsl` напрямую; поток writer → ReadLints → reviewer | `1c-agent-delegation.mdc` § BSL WRITE GUARD | — |
| `bsl-write-guard.mdc` (удалён) | Mechanical Mode: StrReplace оркестратора + обязательный reviewer | `1c-agent-delegation.mdc` § BSL WRITE GUARD | детали Light/Mechanical — `1c-halt-triggers.mdc` |
| `bsl-write-guard.mdc` (удалён) | JSDoc / многострочная шапка метода — нетривиально, только writer | `1c-agent-delegation.mdc` § BSL WRITE GUARD | — |
| `bsl-write-guard.mdc` (удалён) | В apply/review исключения однострочной правки не действуют; post-reviewer fixes только через writer | `1c-agent-delegation.mdc` § BSL WRITE GUARD + § АВТО-ИСПРАВЛЕНИЕ («Без прямого StrReplace») | — |
| `conversational-discipline.mdc` (удалён) | No Acknowledgement, Adaptive Brief, Risk Surfacing, Honest Subagent, Progress Marker | `chat-output-budget.mdc` (intro + Runtime-контракт + секции §4–§6) | полное тело — `chat-output-budget-full.mdc` |
| `orchestrator-as-navigator.mdc` (удалён) | Пользователь — заказчик сценария; тишина без блокера; навигатор не правит BSL сам | `chat-output-budget.mdc` (абзацы навигатора и тишины) | — |

**Вынесенные подробности delegation (не отдельные файлы, тот же D6(в)):**

| Секция | Куда подробности | Якорь always-apply |
|---|---|---|
| KB CONTEXT | `knowledge-format.mdc` § Existing Knowledge в промпте агента | `1c-agent-delegation.mdc` § KB CONTEXT (однострочник) |
| АВТО-ИСПРАВЛЕНИЕ РЕВЬЮ | `review/SKILL.md` § Apply-контур | лимит 2; якорь apply-reviewer; якорь поверхности — в delegation |
| WRITER PIPELINE (таблица шагов) | `1c-writer-pipeline.mdc` (единственный эталон) | `writer → ReadLints → … → reviewer` в delegation |
| ПРОМПТ WRITER (yaml ЧТО/КАК) | `1c-writer-pipeline.mdc` § ПРОМПТ WRITER | однострочник ЧТО/не КАК в delegation |

Непокрытых обязательств нет.
