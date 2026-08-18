# Architecture: independent-review-disposition (kit process)

**Дата:** 2026-08-09  
**Тип:** процесс kit (не архитектура BSL продукта)  
**Основание:** explore-отчёты `temp/reports/exploration-2026-08-09-critical-review-quality.md`, `exploration-2026-08-09-review-critical-quality-layer.md`; в постановке Architect / verify: `not-required` (1C-architect не вызывался — смена контракта ревью, не конфигурации).

## Решение

Ввести ортогональный слой **QualityFlag + Disposition** поверх существующих Action (MUST_FIX/REFACTOR/VERIFIED_OK):

1. Reviewer — владелец QualityFlag / needs-confirm при agreement-override.
2. Orchestrator (review skill) — владелец AskQuestion disposition и записи в report/queue.
3. Один протокол для `/review` и `/release-review` (`release_mode` не отключает слой).

## Границы

| Внутри | Снаружи |
|--------|---------|
| Code-review контур kit | `/opsx:explain` handoff |
| Памятка review-guide | Verify Layer 4 design-challenge |
| Стык маппинга extend disposition | Авто-AskQuestion в apply |

## Риски процесса

- Шум disposition → пакетный confirm + порог severity.
- Breaking `prompt_contract_version` 3→4.
- Семантика as-designed ≠ extend rejected без явного маппинга.

## Chosen

Реализация по `design.md` Decisions D1–D7; срезы S1→S2→S3.
