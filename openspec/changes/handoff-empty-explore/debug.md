# debug — handoff-empty-explore

## Verify decision ledger

```yaml
closed_decisions:
  - id: explore_create_only_with_block
    summary: "В исследовании, которое идёт понять и исправить, команда создать новую заявку стоит только в том же сообщении, где уже есть блок постановки. Создание сразу без исследования по-прежнему считает постановкой короткий ответ. Продолжение уже начатой заявки без требований идёт коротким ответом по записанному описанию и блока не требует."
    closed_at: "2026-10-23"
    source: verify-user-answer
    confirmed_by: user
    premise:
      claim: "Слот следующего шага в финале исследования может назвать создание заявки без блока постановки."
      anchor: ".cursor/skills/openspec-explore/SKILL.md:218"
open_decision_id: null
decision_round: 1
verify_depth: incremental
assumptions_accepted: []
refuted_premises: []
```

## Extend Coherence Audit — 2026-10-23

- Триггер: semantic
- Drift-check из брифа: scope-violation
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-10-23.md`
- Решение пользователя: accepted recommendations — вариант 1 записан вместе с отменой архивного правила для заявки без требований и задачей на показ команды только рядом с блоком

## Extend — 2026-10-23

- источник: `--from-verify` `reports/verification-2026-10-23.md`, ответ B, затем вариант 1 брифа
- что изменено: из исследования с шагами команда новой заявки только в сообщении с блоком постановки; создание сразу и продолжение уже начатой заявки без требований коротким ответом сохранены; в design добавлен Blast Radius на узкую отмену «всегда дописать»
- disposition: accepted
- Темы: explore_create_only_with_block
- Architect Gate: `reports/architecture-extend-coherence-2026-10-23.md`
- следующий шаг: `/opsx:verify handoff-empty-explore`

## Extend — 2026-10-23

- источник: repair-from-verify, `reports/design-challenge-2026-10-23.md`
- что изменено: путь без имени не выравнивается с созданием с именем; ветка остановки «нет постановки» снимается, тексты оставшихся остановок без пустого разбора; явная просьба создать заявку подчинена тому же правилу, продолжение без блока только при видимом каталоге; источник «код» и собственное решение хода названы проверяемо; неизменённые сценарии названы в матрице как сверка
- disposition: accepted
- Темы: G1, G2, G3, G4, G5
- Architect Gate: не требовался
- следующий шаг: итог той же проверки
