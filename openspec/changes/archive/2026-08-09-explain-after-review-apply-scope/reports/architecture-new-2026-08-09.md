# Architecture: explain-after-review-apply-scope (kit process)

**Дата:** 2026-08-09  
**Тип:** процесс kit (не BSL продукта)  
**Основание:** `temp/reports/exploration-2026-08-09-explain-after-review-scope.md`; Architect / verify: not-required для 1C-architect.

## Решение

1. Handoff-секция `## Explain scope` внутри review/apply артефактов.
2. Propose explain в финалах review/apply ниже fix/extend.
3. Prefill B-explain (Охват XOR Варианты + Контекст) из handoff; карта только после «да».

## Границы

Не пересекать с `independent-review-disposition` (QualityFlag/Disposition). Не создавать `temp/explain-handoff-*.md`.

## Chosen

Один срез S1; Decisions D1–D5 в `design.md`.
