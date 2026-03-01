# AGENTS.md — BSL Code Gate

**Главный диспетчер:** `.cursor/rules/1c-dispatch-gate.mdc` — таблица HALT-условий и делегирования агентам.

---

## OpenSpec Workflow (единственный)

**Терминология:** *change* (изменение, заявка на изменение) в OpenSpec допустимо называть кратко **ЗНИ** (заявка на изменение). В артефактах и диалоге можно использовать «ЗНИ», «change», «изменение» как синонимы.

```
explore → new/ff → apply → verify → archive
```

Команды: `/opsx:explore`, `/opsx:new`, `/opsx:ff`, `/opsx:apply`, `/opsx:verify`, `/opsx:archive`.
Паттерны делегирования агентам: `.cursor/skills/1c-agent-patterns/SKILL.md`.
Описание flow: `.cursor/rules/sdd-workflow.mdc`.

---

## BSL write guard и делегирование

**Запрет прямого редактирования .bsl:** architect → writer → reviewer, DELEGATION GATE, ограничения агентов — `.cursor/rules/1c-agent-delegation.mdc`.

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

## Предрелизное ревью расширения 1С

Команда `/prerelease-review` или скилл `.cursor/skills/prerelease-review/SKILL.md`.

---

## Стандарты вендора 1С (architect / reviewer)

Чеклисты: `.cursor/skills/1c-vendor-standards/SKILL.md`. Доменные файлы: `.cursor/docs/standard/std-NN-*.md`.

---

## Полнота артефакта specs (Delta Specs Gate)

`.cursor/rules/openspec-specs-gate.mdc`.
