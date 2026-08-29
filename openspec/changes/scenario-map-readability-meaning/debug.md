## Verify decision ledger

```yaml
closed_decisions:
  - id: infographic_meaning_carriers
    summary: "Карта — инфографика: смысл с полотна (граф плюс до двух аннотаций с якорем и доказательством); зона ловушки — подсветка якоря; новое relation «ожидалось, но отсутствует» не в этой ЗНИ."
    closed_at: "2026-08-29"
    source: verify-user-answer
  - id: short_map_layout_owner
    summary: "Раскладку считает панель; полосы — дорожки по полю слоя узла, не по рангу; ручные координаты родителя не вводятся. Обратное ребро не пунктиром (пунктир — тип связи). Виды — переключатель раскладки; режимы — подсветка."
    closed_at: "2026-08-29"
    source: verify-user-answer
open_decision_id: null
decision_round: 2
verify_depth: incremental
assumptions_accepted: []
```

## Extend Coherence Audit — 2026-08-29

- Триггер: semantic
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-08-29.md`
- Решение пользователя: accepted recommendations — инфографика внутри S1; `relation` «ожидалось, но отсутствует» вынесен; аннотации якорем, развилка раскладки открыта

## Extend — 2026-08-29

- Источник: user-extend после ответа на проверку постановки (вариант «расширить до инфографики»)
- Что добавлено/изменено: `proposal.md` (Why/What Changes/AC), `design.md` (BC 5–6, D1 якорь, D6, D9, Blast Radius, OQ4–5, Slices), `specs/scenario-map-canvas/spec.md` (полотно, три Scenario), `tasks.md` (S1.16–S1.20, правки S1.5/S1.10/S1.13/S1.15, Primary)
- Disposition: accepted (рекомендации coherence: аннотации ≤2, якорь, не в порог; новое `relation` deferred)
- Architect Gate: `reports/architecture-extend-coherence-2026-08-29.md`
- Связь с открытой развилкой: аннотации задаются якорем, не координатами — выбор, кто считает координаты короткой карты, не предрешён
- Следующий шаг: `/opsx:verify scenario-map-readability-meaning`

## Extend — 2026-08-29 (раскладка панели)

- Источник: user-extend после ответа на проверку постановки (вариант «раскладку оставляет панель, полосы — дорожки по полю слоя»)
- Что добавлено/изменено: `proposal.md` (What Changes п.1); `design.md` (BC 1–2, 7; D1, D5; Risk 4; OQ5 закрыт; «Решения verify»); `specs/scenario-map-canvas/spec.md` (полосы по слою, MAY без подписи на длинных картах); `tasks.md` (S1.1–S1.2, S1.4, S1.7, S1.9–S1.10, S1.14; аннотации S1.15–S1.19 перед сверкой S1.20)
- Disposition: accepted
- Architect Gate: не требовался — закрытие открытой развилки по ответу пользователя; ось «шаблон плюс две проверки» не меняется; инфографика уже согласована
- Следующий шаг: `/opsx:verify scenario-map-readability-meaning`

