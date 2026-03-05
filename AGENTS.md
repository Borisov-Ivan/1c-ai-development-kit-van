# AGENTS.md — BSL Code Gate

**Главный диспетчер:** `.cursor/rules/1c-dispatch-gate.mdc` — таблица HALT-условий и делегирования агентам.

---

## OpenSpec Workflow (единственный)

**Терминология:** *change* (изменение, заявка на изменение) в OpenSpec допустимо называть кратко **ЗНИ** (заявка на изменение). В артефактах и диалоге можно использовать «ЗНИ», «change», «изменение» как синонимы.

```
explore → new/ff → apply → verify → archive
```

Команды: `/opsx:explore`, `/opsx:new`, `/opsx:ff`, `/opsx:apply`, `/opsx:verify`, `/opsx:archive`, `/opsx:debug` (алиас `/debug`), `/opsx:prerelease-review` (алиас `/prerelease-review`).
Дополнительные действия: continue (продолжить артефакт), sync (синхронизация спеков), bulk-archive (пакетная архивация).
Паттерны делегирования агентам: `.cursor/skills/1c-agent-patterns/SKILL.md`.
Описание flow: `.cursor/rules/sdd-workflow.mdc`.

Генерация проектных документов из OpenSpec: `/docs:functional`, `/docs:architecture`, `/docs:technical` — `.cursor/skills/openspec-docs/SKILL.md`.

---

## BSL write guard и делегирование

**Запрет прямого редактирования .bsl:** architect → writer → reviewer, DELEGATION GATE, ограничения агентов — `.cursor/rules/1c-agent-delegation.mdc`.

**Apply Gate:** реализация ЗНИ (writer/reviewer) — только через `/opsx:apply`. Без apply — только артефакты. `.cursor/rules/1c-agent-delegation.mdc` (APPLY GATE).

---

## Запрет создания объектов метаданных

**Никогда** не создавать XML-файлы метаданных, директории объектов или новые .bsl в несуществующих директориях. При отсутствии объекта — СТОП, блокер пользователю. `.cursor/rules/1c-no-metadata-creation.mdc`.

---

## Анализ ошибок 1С (трассы и стеки)

Делегирование onec-trace-analyst, затем explorer/architect — `.cursor/rules/1c-error-analysis.mdc`.

---

## Запрет заплаточных фиксов

Root cause (verified, не hypothesis) + architectural impact перед фиксом; при системном масштабе — onec-code-architect. `.cursor/rules/verified-cause-gate.mdc`.

---

## Сохранение отчётов субагентов

Полные отчёты architect/explorer/trace-analyst → `openspec/changes/<id>/reports/`. `.cursor/rules/preserve-subagent-reports.mdc`.

---

## Администрирование баз и серверов 1С

Управление серверами 1С, базами данных, PostgreSQL, ibcmd, выгрузка/загрузка XML — делегировать **onec-admin**. `.cursor/agents/onec-admin.md`.

---

## Предрелизное ревью расширения 1С

Команда `/opsx:prerelease-review` (алиас `/prerelease-review`) или скилл `.cursor/skills/prerelease-review/SKILL.md`.

---

## Стандарты вендора 1С (architect / reviewer)

Чеклисты: `.cursor/skills/1c-vendor-standards/SKILL.md`. Доменные файлы: `.cursor/docs/standard/std-NN-*.md`.

---

## Полнота артефакта specs (Delta Specs Gate)

`.cursor/rules/openspec-specs-gate.mdc`.

---

## Барьер чтения скилла из команд (Command → Skill Read Gate)

Когда команда-обёртка (`.cursor/commands/*.md`) делегирует в скилл — единственное действие в первом tool call batch — Read скилла. Не батчить с чтением трасс, модулей и других файлов. `.cursor/rules/command-skill-gate.mdc`.
