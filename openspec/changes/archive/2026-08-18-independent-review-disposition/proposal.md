## Why

После `/review` и `/release-review` слабая реализация, уже разрешённая в постановке ЗНИ, часто уходит как «соответствует design» или VERIFIED_OK без явного выбора заказчика «оставляем как задумано» или «чиним». Нужен единый слой независимой оценки качества и disposition для обеих команд.

## What Changes

- Ревьюер помечает спорное качество даже при endorse design (`design-prescribed` / QualityFlag weak), а не снимает finding тихим VERIFIED_OK «только потому что design».
- Оркестратор `/review` и `/release-review` после отчёта спрашивает disposition: as-designed | queue-fix (| defer); один алгоритм для `release_mode` false/true.
- Architectural Context в промпте — контекст намерения, не эталон «соответствия = PASS».
- Памятка заказчика описывает сценарий простым языком.
- **BREAKING** для контракта отчёта ревьюера: новые поля Disposition / QualityFlag → bump `prompt_contract_version`.

## Capabilities

### New Capabilities

- `review-quality-disposition`: независимая оценка качества в code-review контуре и UX disposition (as-designed / queue-fix) для `/review` и `/release-review`.

### Modified Capabilities

- (нет существующих specs в `openspec/specs/`)

## Impact

- Kit: skill review, агент `onec-code-reviewer`, шаблоны `1c-agent-patterns/reviewer.md`, `reviewer-checks.md`, `review-guide.md`, команды review/release-review; опционально стык extend disposition и carve-out apply-reviewer.
- Продуктовый BSL не меняется.
- Вне scope: explain handoff / охват в брифе (отдельная ЗНИ); Layer 4 verify design-challenge.

## Metadata (comment markers)

developer: N/A
comment_suffix:
marker_style: minimal

<!-- Kit meta-change: BSL comment markers не применяются; ФИО не требуется. -->

## Forms mode

form_mode: n/a

## Scope

- In scope: `.cursor/skills/review/SKILL.md`, `.cursor/agents/onec-code-reviewer.md`, `.cursor/skills/1c-agent-patterns/reviewer.md`, `.cursor/docs/standard/reviewer-checks.md`, `.cursor/docs/review-guide.md`, `.cursor/commands/review.md`, `.cursor/commands/release-review.md`; при необходимости точечно `openspec-extend-change`, `1c-agent-delegation.mdc`, AP-карточки.
- Out of scope: `/opsx:explain`, apply авто-fix UX (кроме пометки «потребуется disposition на review»), изменения cf/cfe продукта.
