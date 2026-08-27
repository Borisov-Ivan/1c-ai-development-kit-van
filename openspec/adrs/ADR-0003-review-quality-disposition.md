# ADR-0003: Ортогональный QualityFlag / Disposition в code-review

**Статус:** Accepted  
**Дата:** 2026-08-10  
**Область:** kit / code-review (`/review`, `/release-review`)  
**Источник:** openspec/changes/archive/2026-08-10-independent-review-disposition/reports/architecture-new-2026-08-09.md  
**Load-bearing:** yes  
**Protects-invariants:**
  - "Соответствие design не закрывает спорное качество без явного disposition заказчика"
  - "as-designed не снимает Category 12 / release-hygiene без отдельного waive"
  - "apply-reviewer не блокирует цикл AskQuestion disposition и не авто-waive weak"

## Контекст

Agreement-override и цитата design переводили слабую реализацию в VERIFIED_OK без подтверждения заказчика. Нужен слой независимой оценки качества поверх Action writer-контракта.

## Решение

Ортогональные поля `QualityFlag` / `Disposition` (контракт ревьюера v4). Корзина disposition = agreement-override ∪ design-prescribed ∪ design-endorsed weak. Финальные as-designed / queue-fix пишет оркестратор skill review; silent VERIFIED_OK — только whitelist Evidence (= design D9). Один протокол для ordinary и prerelease.

## Альтернативы

| Вариант | Плюсы | Минусы | Почему отклонён |
|---------|-------|--------|-----------------|
| Всегда MUST_FIX без disposition | Простота | Ломает легитимные исключения | Отклонён |
| Только ужесточить Design authority без UX | Меньше UI | Шум без выбора заказчика | Отклонён |
| AskQuestion disposition в apply | Единый UX | Тормозит цикл apply | Out of scope (D5) |

## Последствия

- Положительные: осознанные исключения фиксируются; quality не зелится молча
- Отрицательные: breaking bump `prompt_contract_version` 3→4; возможный шум disposition (режется предикатом корзины B)
- Нейтральные: writer-контракт Action MUST_FIX/REFACTOR сохраняется

## Связи

- **Specs:** openspec/specs/review-quality-disposition/spec.md
- **Changes:** archive/2026-08-10-independent-review-disposition/
- **Связанные ADR:** —
