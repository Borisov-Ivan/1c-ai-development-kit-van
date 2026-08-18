## Why

Architect предлагает allow-list имён форм как «тонкий» охват хука, writer вливает литералы, reviewer не имеет выделенного прохода — отклоняет заказчик на приёмке. В kit нет зеркала каркаса Попытка (реестр + HALT + выделенный проход + completeness) для runtime-фильтра по строкам метаданных/форм.

## What Changes

- Добавить антипаттерн Hardcoded Identity Filter (ориентир AP-055) в реестр и remediation «делегировать фильтр API/настройке или секция Hardcode Justification».
- Ввести Identity Filter Gate у architect и шаблон секции Hardcode Justification в design.
- Добавить writer G21 (HALT до литералов identity-filter без обоснования в design).
- Добавить у reviewer выделенный проход Identity / Hardcode Audit с completeness-таблицей.
- Расширить Existing Mechanisms / Preference Hierarchy запахом Scope-as-literals.
- **Не** менять прикладной код ЗНИ `prerelease-fix-knopki-shablonov` и не трогать легитимные литералы протокола/enum без смены контракта.

## Capabilities

### New Capabilities

- `hardcode-justification-gate`: обязательное обоснование хардкода-фильтра идентичности (allow-list имён форм/метаданных) в цепочке architect → writer → reviewer.

### Modified Capabilities

- (нет — capability в `openspec/specs/` ещё не существует)

## Impact

- Файлы: `.cursor/rules/bsl-antipatterns.mdc`, `.cursor/docs/antipatterns/bsl-antipatterns.md`, `.cursor/rules/existing-mechanism-priority.mdc`, `.cursor/rules/architect-gate.mdc`, `.cursor/agents/onec-code-architect.md`, `.cursor/agents/onec-code-writer.md`, `.cursor/agents/onec-code-reviewer.md`, `.cursor/docs/standard/reviewer-checks.md`, `.cursor/skills/review/SKILL.md`, `.cursor/skills/1c-agent-patterns/writer.md` (список Gate Results +G21).
- Потребители kit: после поставки `.cursor` architect не выбирает «&После + список имён» без обоснования; reviewer ловит identity-literals до приёмки заказчиком.
- Метапроект: ветка `kit-hardcode-justification-gate`; папку change в main не мержить (`kit-template-workflow.md`).

## Scope

- In scope: четыре слоя kit (реестр AP, architect HALT + design-секция, writer G21, reviewer Phase Identity Audit) и смежные docs/rules.
- Out of scope: прикладной долг allow-list в consumer-ЗНИ; опциональный grep post-apply в verify (открытый вопрос); литералы кодов отказа/ключей протокола как класс (не identity-filter).

## Metadata (comment markers)

developer:
comment_suffix:
marker_style: minimal

## Forms mode

form_mode: n/a

## Decisions

1. **Precedent:** новый change эволюции kit; паттерн протекания directly-related к archive `ssylka-tablitsa-knopok-dop-funkcii` и reject S3-B в `prerelease-fix-knopki-shablonov` (прикладной fix вне scope).
2. **Маркеры BSL:** не используются (`marker_style: minimal`) — правятся только тексты kit.
