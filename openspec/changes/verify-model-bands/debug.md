# debug — verify-model-bands

## Verify decision ledger

```yaml
closed_decisions:
  - id: readiness-unknown-signature
    summary: "Неизвестная сигнатура или контракт данных при сверке задач идёт на тяжёлую модель, вместе с неизвестным перехватом и неподтверждённым вызовом платформы. Ручная настройка и новая связь модулей остаются на модели чата."
    closed_at: "2026-10-14"
    source: verify-user-answer
    confirmed_by: user
    premise: none
  - id: multi-slice-counter
    summary: "Модель семейства GPT берётся, если в заявке больше одного среза, даже когда в этот запуск сверки попал один срез. Заявка из одного среза остаётся на модели чата."
    closed_at: "2026-10-14"
    source: verify-user-answer
    confirmed_by: user
    premise: none
open_decision_id: null
decision_round: 1
verify_depth: full
assumptions_accepted: []
refuted_premises: []
```

## Extend Coherence Audit — 2026-10-14

- Триггер: semantic
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-10-14.md`
- Решение пользователя: accepted recommendations — пять пунктов остаются в срезе S1, новую заявку не открывать

## Extend — 2026-10-14

- источник: `--from-verify` `reports/verification-2026-10-14.md`, ответ заказчика 1A и 2B, подтверждение варианта 1 брифа
- что изменено: неизвестная сигнатура или контракт данных положена на тяжёлую модель; счётчик модели GPT — число срезов заявки; признаки сильнейшей модели названы словами строки глубокого разбора и триггера повторного разбора, «фильтр по имени объекта» приравнен к Identity Filter; пункт 2 ADR-0011 сужен теми же тремя поводами; абзац обоснования места GPT опёрт на решение заявки и запрет чужого семейства
- disposition: G1 accepted, G2 accepted, G3 accepted, G4 accepted, G5 accepted
- Темы: G1, G2, G3, G4, G5
- Architect Gate: `reports/architecture-extend-coherence-2026-10-14.md`
- следующий шаг: `/opsx:verify verify-model-bands`

## Extend — 2026-10-14 repair

- источник: repair-from-verify, `reports/design-challenge-2026-10-14-2.md`
- что изменено: в D5 и в задаче S1.2 пункт 3 ADR-0011 оставляет сверку с прошлым договором на лестнице самой сильной модели и отдельно говорит, что независимый разбор берёт эту лестницу только при тяжёлом признаке; последствия перестают утверждать прежнюю модель ревью и согласованности срезов. WHEN сценария «Вызов архитектора без ошибки enum» оставлен на обычной строке и на независимом разборе без тяжёлого признака; ветки самой сильной модели в этот WHEN не входят
- disposition: G9 accepted, G10 accepted
- Темы: G9, G10
- Architect Gate: `reports/design-challenge-2026-10-14-2.md`
- следующий шаг: внутренний повтор проверки
