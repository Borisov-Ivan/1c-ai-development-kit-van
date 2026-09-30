# Приёмка S1 — прогон фикстуры (2026-09-21)

**Change:** value-efficient-verify  
**Срез:** S1 «Внешний контракт и ранняя остановка повторной темы»  
**Фикстура:** `openspec/changes/fixture-ec-unclassified-axis/`

## Сценарий

Принятый референс `accepted-ref-demo` по двум осям: `visible-result` (уже подтверждена) и `error-recovery` (сначала не классифицирована).

## Прогон 1

Файл: `openspec/changes/fixture-ec-unclassified-axis/reports/verification-2026-09-21.md`

- Продолжение заблокировано.
- Названы тема «Восстановление после ошибки», ось восстановления после ошибки, источник `design.md#Behavior-Contract`.
- Контроль срезов и независимый разбор постановки не запускались.

## Подтверждение

В фикстуре записано решение заказчика: ось `error-recovery` совпадает с референсом; парная запись журнала `EC-010` / `verify-user-answer` / `confirmed_by: user` с временем позже сигнала.

## Прогон 2

Файл: `openspec/changes/fixture-ec-unclassified-axis/reports/verification-2026-09-21-2.md`

- Тот же блокер снят.
- `open_decision_id: null`.

## Итог

Обязательный сценарий приёмки среза S1 воспроизведён на универсальной тестовой ЗНИ.
