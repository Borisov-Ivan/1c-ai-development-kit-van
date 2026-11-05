## Slice Gate Decisions

### Slice S1 — Маршрут починки с прежним результатом (2026-10-16)
Срез: S1 — Маршрут починки с прежним результатом
Решение: awaiting-acceptance
Обоснование: все рабочие задачи реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: нет (S1.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S1-2026-10-16.md

### Slice S1 — Маршрут починки с прежним результатом (2026-11-05)
Срез: S1 — Маршрут починки с прежним результатом
Решение: awaiting-acceptance
Обоснование: рабочие задачи S1.6–S1.10 реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: нет (S1.accept остаётся [ ])
Связанный отчёт: reports/handoff-acceptance-S1-2026-11-05.md

### Slice S1 — Маршрут починки с прежним результатом (2026-11-05)
Срез: S1 — Маршрут починки с прежним результатом
Решение: принят
Обоснование: без замечаний
Изменения tasks: S1.accept отмечен [x]
Связанный отчёт: reports/slice-acceptance-S1-2026-11-05.md

## Extend — 2026-10-16

- источник: repair-from-verify, `reports/design-challenge-2026-10-16.md`
- что изменено: общее правило размещения без слов инцидента; срез по полю зависимостей, иначе наименьший номер; снятие уже открытой приёмки из текста ошибки до таблицы глубины; вопрос остаётся при двух разных результатах; приоритет строки глубины; ответ внутри выбранного подхода остаётся короткой сверкой
- disposition: G1 accepted, G2 accepted, G3 accepted, G4 accepted, G5 accepted, G6 accepted, G7 accepted (уже закрыт текстом, отдельной правки нет), G8 accepted
- Темы: G1, G2, G3, G4, G5, G6, G7, G8
- Architect Gate: не требовался
- следующий шаг: повторная сверка постановки в том же прогоне проверки

## Extend Coherence Audit — 2026-11-05

- Триггер: semantic
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-11-05.md`
- Решение пользователя: accepted recommendations — три двери в этот срез, остальные процессы не копировать

## Extend — 2026-11-05

- Источник: подтверждённый бриф после разбора ложной пары; отчёты `reports/exploration-2026-11-05-effect-verify.md`, `reports/exploration-2026-11-05-effect-extend.md`, `reports/exploration-2026-11-05-effect-other.md`, `reports/architecture-extend-coherence-2026-11-05.md`.
- Что изменено: в Why, контракт и приёмку S1 дописана граница живой ветви. Карточка проверки не ставит ветвь, которая не выполняет уже записанную приёмку. Карточка дополнения не предлагает не делать уже названное правило. Вход проверки не прячет фразу, уже сказанную в той же команде. Следующий шаг после ответа берётся из таблицы глубины. Задачи S1.6–S1.9 стоят перед приёмкой S1. Разбор, создание, пошаговый разбор, реализация и архив не входят.
- Темы: G9
- Disposition: accepted
- Architect Gate: `reports/architecture-extend-coherence-2026-11-05.md`
- Следующий шаг: проверка постановки. Правило само изменилось, поэтому это полный проход, не короткая сверка.

## Verify decision ledger

```yaml
closed_decisions:
  - id: card_rule_binding
    summary: "Правило карточки обязательно. Починка с прежней суммой и справкой остаётся в открытой приёмке, без вопроса о срезе и без отдельного шага проведения. Вариант, который проведение не выполняет, в карточку не ставится. Убрать это правило из текста можно только новым ответом."
    closed_at: "2026-11-05T14:12:00+09:00"
    source: verify-user-answer
    confirmed_by: user
    authority: customer-direct
    external_contract_id: EC-1
    premise:
      claim: "Правило уже стоит в тексте заявки; ответ делает его обязательным, чтобы снять его можно было только новым ответом."
      anchor: "openspec/changes/fix-route-from-analysis/debug.md#Extend — 2026-11-05"
  - id: card_rule_binding
    summary: "Запрет вычёркивать правило без нового ответа снят. Само правило остаётся: проверка не предлагает путь, который не снимает названную проблему. Текст правил этим ответом не переписан."
    closed_at: "2026-11-05T17:14:00+09:00"
    source: verify-user-answer
    confirmed_by: user
    authority: customer-direct
    external_contract_id: EC-1
    premise:
      claim: "Заказчик поручил выбрать вариант, который не меняет выполнение заявки и не добавляет остановку без разницы для запуска реализации. Запрет снят, текст правила остаётся."
      anchor: "openspec/changes/fix-route-from-analysis/debug.md#Extend — 2026-11-05 снятие запрета"
open_decision_id: null
decision_round: 2
verify_depth: full
assumptions_accepted: []
refuted_premises:
  - decision_id: card_rule_binding
    refuting_anchor: "openspec/changes/fix-route-from-analysis/debug.md:27"
    report: "openspec/changes/fix-route-from-analysis/reports/design-challenge-2026-11-05.md"
    detected_at: "2026-11-05T15:45:04+09:00"
    fingerprint: "f4628a6134ec0a040c684c985e197a09c6b5a0a0ff727e92cc0455c67d0be39a"
```

## External Contract Ledger

```yaml
external_contract:
  - id: EC-1
    topic:
      capability: pipeline-light-route
      anchor: "правило карточки"
      axis: visible-result
      reference: "проверка не предлагает путь, который не снимает названную проблему; запрет вычёркивать правило без нового ответа снят; текст правила остаётся"
    axis: visible-result
    source: "debug.md#Extend — 2026-11-05"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-11-05T17:14:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec1
        kind: customer-return
        primary_event_id: verify-answer-2026-11-05T14:12:00+09:00
        primary_event_at: "2026-11-05T14:12:00+09:00"
        source_fingerprint: "51e8ccdb5560fd8ee64ad358e7049248e6c9d8001ca027d313cf9d159f9c7025"
      - id: sig-ec1-2
        kind: customer-correction
        primary_event_id: verify-answer-2026-11-05T17:13:00+09:00
        primary_event_at: "2026-11-05T17:13:00+09:00"
        source_fingerprint: "a6d12d8b6052c061e1fc642213a186fef0b28eee7585ac021ceb5193b0330cde"
  - id: EC-2
    topic:
      capability: pipeline-light-route
      anchor: "слова вопроса"
      axis: visible-result
      reference: "перед показом вопрос переписывается словами уже записанного результата; путь к заметке остаётся в отчёте; вопрос не пропускается"
    axis: visible-result
    source: "debug.md#Extend — 2026-11-05 вопрос словами задачи"
    authority: customer-direct
    decision:
      parity: matches
    confirmation: confirmed
    confirmed_at: "2026-11-05T16:33:00+09:00"
    confirmed_by: user
    signals:
      - id: sig-ec2
        kind: customer-correction
        primary_event_id: extend-answer-2026-11-05T16:33:00+09:00
        primary_event_at: "2026-11-05T16:33:00+09:00"
        source_fingerprint: "1a6764da3ff3b7a9cbb1626cae35ba362af27d393574c3a6380422edd3291a9e"
```

## Extend Coherence Audit — 2026-11-05-2

- Триггер: semantic
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-11-05-2.md`
- Решение пользователя: accepted recommendations — переписать вопрос словами уже записанного результата и показать его; путь оставить в отчёте

## Extend — 2026-11-05 вопрос словами задачи

- Источник: подтверждённый бриф, вариант 1. Постановка из чата исследования: вопрос показывается словами уже записанного результата, путь к заметке остаётся в отчёте, вопрос не пропускается.
- Что изменено: в Why, контракт и приёмку S1 дописана проверка текста вопроса перед показом. Задача S1.10 стоит перед приёмкой S1. Список служебных кодов не расширяется. Новая строка таблицы глубины не добавляется.
- Темы: EC-2
- Disposition: accepted
- Architect Gate: `reports/architecture-extend-coherence-2026-11-05-2.md`
- Следующий шаг: проверка постановки. Добавлен сценарий, поэтому это полный проход.

## Extend — 2026-11-05 снятие запрета

- Источник: ответ на проверку. Заказчик поручил выбрать вариант, который не меняет выполнение заявки и не добавляет остановку без разницы для запуска реализации.
- Что изменено: запрет вычёркивать правило без нового ответа снят. Текст правила, задачи и требования не переписаны.
- Темы: EC-1
- Disposition: accepted
- Architect Gate: не требовался
- Следующий шаг: проверка постановки продолжается в том же запуске

## Verify repair — 2026-11-05

- Источник: разбор постановки `reports/design-challenge-2026-11-05-2.md`. Все замечания уточняют уже названное правило и не меняют обещанный результат.
- Что дописано: вход передаёт текст в дополнение без лишнего вопроса; после ответа не зовётся первая проверка; граница пары только в карточке проверки; подтверждение без номера принимает «да»; две ветви называются каждая своим результатом; путь не заменяет слова выбора.
- Журнал решений не менялся.
