---
name: 1c-bsp-patterns
description: "SSL/БСП subsystems guidance. Use when working with standard library subsystems."
---

# 1C SSL/БСП Subsystems Reference

This skill provides guidance for using SSL subsystems via `ssl_search` MCP tool.

For basic SSL usage (attribute access, user messages) — see `1c-coding-standards.mdc`.

## When to Use

Invoke this skill when:
- Working with users and access rights
- Working with files and attachments
- Implementing print forms
- Managing background jobs
- Working with object versioning
- Sending emails
- Need common utility functions (arrays, structures, strings)

## Core Principle

**ALWAYS check if SSL has a solution before writing custom code.**

## SSL Search Workflow

When implementing new functionality:

1. **First, search SSL** — use `ssl_search` MCP tool with keywords describing your need
   - Example: `ssl_search("фоновое задание прогресс")`
   - Example: `ssl_search("копирование структуры")`

2. **Check existing patterns** — use `codesearch` to find how similar tasks are solved in the codebase

3. **Use SSL if available** — it's tested, optimized, and maintained

4. **Only then write custom code** — and document why SSL wasn't suitable

## Key SSL Modules

- **Пользователи** — users, roles, access rights
- **РаботаСФайлами** — file storage and attachments
- **УправлениеПечатью** — print forms
- **ДлительныеОперации** — background jobs with progress
- **ВерсионированиеОбъектов** — object history
- **РаботаСПочтовымиСообщениями** — email sending
- **ОбщегоНазначения** / **ОбщегоНазначенияКлиентСервер** — common utilities
- **Проверка наличия реквизита**: см. `.cursor/rules/1c-coding-standards.mdc` (правила проверки заполнения и доступа к реквизитам)
- **СтроковыеФункцииКлиентСервер** — string functions

---

**Remember**: SSL is your first stop for common functionality. Writing custom code when SSL has a solution is technical debt.

Для стандартов вендора по разработке библиотек и переопределению модулей: чеклист — `.cursor/skills/1c-vendor-standards/SKILL.md` (раздел 10); детали — Read `.cursor/docs/standard/std-10-bsp-libraries.md`. Навигатор: `.cursor/docs/standard/1c-standards-navigator.md`.
