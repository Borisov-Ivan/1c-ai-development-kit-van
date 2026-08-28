## Debug

<!-- Создаётся/дополняется на /opsx:verify и /opsx:apply. Стартер Symptom/Evidence — опционален. -->

### Symptom
- Панель рядом с чатом рисуется вне правил кита: пустая или как навигатор по модулю.

### Evidence
- Постановка ЗНИ 2026-08-27; в `.cursor/` кита до ЗНИ упоминаний панели нет.

### Root Cause
- Нет контракта карты сценария и нет always-apply запрета рисовать панель «по системному канвасу».

### Fix plan
- Скилл карты + строка диспетчера (просьба и подавление) + намёк в существующей строке выхода разбора.

## Verify decision ledger

```yaml
closed_decisions:
  - id: direct_request_linear_publish
    summary: "Прямая просьба сильнее предложения: при ≥4 публикуемых сущностях панель всегда; линейная цепочка с подписанными связями допустима; предлагать схему по-прежнему только при топологии."
    closed_at: "2026-08-28"
    source: verify-user-answer
  - id: edges_evidenced_or_investigate
    summary: "Подписи на связях только из уже видимых фактов (отчёт, журнал, порядок прохода); выдумывать рёбра запрещено; если связей не хватает — панель не публиковать, можно продолжить разбор или исследование."
    closed_at: "2026-08-28"
    source: verify-user-answer
  - id: parent_side_registration
    summary: "Файл панели регистрирует родитель собственной записью и чистой проверкой панели; картограф отдаёт манифест и файл не пишет; ссылка в чате не критерий успеха; успех — штатная кнопка среды. Слияние S2+S2b оставлено в силе: регистрация панели не даёт собственного UX-результата."
    closed_at: "2026-08-28"
    source: user-extend
open_decision_id: null
decision_round: 2
decision_round_max: 2
verify_depth: incremental
assumptions_accepted: []
repair_attempt: 2
last_challenge_at: "2026-08-28T12:10:00Z"
```

## Verify repair — 2026-08-27

Источник: internal repair-from-verify по `reports/design-challenge-2026-08-27.md` (три уточнения инвариантов) и `reports/architecture-task-readiness-2026-08-27.md` (два пробела формулировок).

Что изменено:

- `design.md` D1: порог намёка (≥5 точек) согласован с порогом карты (≥4 узлов) через контракт карточки точки.
- `design.md` D3: источник узлов вне разбора — только существующий журнал/указанный отчёт.
- `design.md` D5: правило молчания в always-apply строке диспетчера, не только в скилле по просьбе.
- `design.md` D7: доступность панели = уже открыта или пользователь назвал файл; без панели — только `explain-*.md` (создать по шаблону, если нет); третьего адресата нет.
- `tasks.md`: S1.1a порядок действий по просьбе; S1.5 источник вне разбора; S1.6 без «чат-файла разбора»; S1.8 диспетчер несёт и подавление, и просьбу.

`Architect Gate:` не требовался (уточнение инвариантов внутри выбранной оси; отчёт независимого разбора уже есть).

## Verify repair — 2026-08-27 (attempt 2)

Источник: residual из `reports/design-challenge-2026-08-27-2.md` и `reports/architecture-task-readiness-2026-08-27-2.md` — журнал по просьбе в середине прохода затирался бы на выходе.

Что изменено:

- `design.md` D7 и пункт 8 Behavior Contract: секция «Карта сценария» в журнале; штатный `Write` на выходе её сохраняет.
- `tasks.md` S1.6: та же формулировка; S1.10a — каркас `explain-report.md` плюс оговорка в скилле разбора и `exit-card.md`.
- таблица срезов: в файлы добавлен шаблон журнала разбора.

`Architect Gate:` не требовался.

## Extend — 2026-08-27

- источник: `--from-verify` (repair-from-verify, без смены scope)
- что добавлено/изменено: см. `## Verify repair — 2026-08-27`
- disposition: accepted (все findings — уточнения формулировок, не новая функциональность)
- **Architect Gate:** не требовался
- следующий шаг: повторный прогон слоёв verify

## Slice Gate Decisions

<!-- Решения по slice-gate маркерам (wait / continue / defer). -->

### Apply — S1.13 verification — 2026-08-27

- Отдельной команды карты в `.cursor/commands/` и `AGENTS.md` — нет.
- `/opsx:explain` в слоте «Дальше» explore — без изменений.
- `opsx-output-style.md`, `brief-card.md`, `inventory-card.md` — не затронуты.

### Slice S1 — Карта сценария по просьбе и намёк на выходе разбора (2026-08-27)

Срез: S1 — Карта сценария по просьбе и намёк на выходе разбора
Решение: awaiting-acceptance
Обоснование: все рабочие задачи S1.1–S1.13 реализованы; приёмочная задача передана на ручной прогон Primary.
Изменения tasks: S1.1–S1.13 отмечены [x]
Связанный отчёт: reports/handoff-acceptance-S1-2026-08-27.md

## Extend Coherence Audit — 2026-08-28

- Триггер: both (semantic drift-warning + counter M≥3)
- Drift-check из брифа: drift-warning
- Вердикт архитектора: drift-warning
- Отчёт: `reports/architecture-extend-coherence-2026-08-28.md`
- Решение пользователя: accepted recommendations — вариант 1 (исследование и разбор); принцип предложения универсален, от темы не зависит

## Extend — 2026-08-28

- источник: user-extend; постановка из чата `/opsx:explore`; `reports/architecture-2026-08-28-scenario-map-redesign.md`; подтверждение варианта 1 + «принцип универсальный, от конкретной темы не зависит»
- что добавлено/изменено: `proposal.md` (Why, оба контура, универсальность); `design.md` (D1/D3/D5–D9, Blast Radius, срезы S2/S2b/S3); `specs/scenario-map-canvas/spec.md` (причинный контракт, предложение по топологии, технический резерв); `tasks.md` (сужен S1.accept; срезы S2, S2b, S3)
- disposition: accepted
- **Architect Gate:** `reports/architecture-extend-coherence-2026-08-28.md`; также `reports/architecture-2026-08-28-scenario-map-redesign.md`
- следующий шаг: `/opsx:verify scenario-map-canvas`

## Extend — 2026-08-28 (from-verify, decision B)

- источник: `--from-verify` после выбора пользователя (вариант B, `reports/verification-2026-08-28.md`)
- что добавлено/изменено: прямая просьба сильнее предложения (spec Direct request + Causal map; design D3, Behavior Contract 6/12/13, § Решения verify); согласие на предложение = та же постройка; порог по публикуемым сущностям; финал исследования без «Дальше» — без предложения; срез картографа влит в S2 (S2.8–S2.12, grep без отдельной приёмки); S2 зависит от S1, S3 от S2; Primary картографа в таблице — без параметра модели
- disposition: accepted (выбор B); repair findings QC (вертикальность / foundation-gate, сценарий порога) — accepted
- **Architect Gate:** не требовался (фиксация выбора из `reports/design-challenge-2026-08-28.md`; ось не менялась)
- следующий шаг: `/opsx:verify scenario-map-canvas`

## Verify repair — 2026-08-28 (consent / threshold)

Источник: internal repair-from-verify по `reports/design-challenge-2026-08-28-2.md` (Gaps 1–6) и `reports/architecture-task-readiness-2026-08-28-2.md` (G1, G2).

Что изменено:

- `design.md` D1/D3, Behavior Contract 9/13, § Решения verify, открытый вопрос 5 закрыт (отложенная постройка).
- `specs/scenario-map-canvas/spec.md`: Direct request, Causal map, Offer, Hint, Map outside walkthrough; сценарий «Согласие до первой карточки разбора запоминает фокус».
- `tasks.md`: S2.1a, S3.1, S3.2, S3.4, S3.5, Follow-up, Связь и чеклист третьего среза.

`Architect Gate:` не требовался (уточнение инвариантов внутри выбранной оси).

## Verify repair — 2026-08-28 (attempt 2, hint vs draw)

Источник: internal repair-from-verify, второй круг, по `reports/design-challenge-2026-08-28-3.md` (Gaps 1–5).

Что изменено:

- Намёк печатает вариант и не собирает панель (D5, spec Silence, Behavior 1).
- Просьба в активном исследовании берёт текущий отчёт (D7, spec Map outside).
- Предложение на подтверждении списка — MAY по предсказанной топологии; публикация — из карточек прохода.
- Сценарии «Намёк не рисует панель», «Просьба в исследовании берёт текущий отчёт», «Отложенное согласие публикует карту без повторного вопроса».

`Architect Gate:` не требовался.

## Verify repair — slice merge — 2026-08-28

- было: S2 + S2b → стало: S2 (задачи S2.8–S2.12 до S2.accept)
- alerts: slice-not-vertical, slice-foundation-with-gate
- files: `tasks.md`, `design.md` (таблица срезов и граф)

## Verify repair — 2026-08-28 (from-verify, edge origin)

Источник: ответ пользователя на остаток проверки постановки (`reports/design-challenge-2026-08-28-4.md`, происхождение ребра): при недостатке информации можно продолжить разбор или исследование; выдумывать связи запрещено.

Что изменено:

- `design.md` D3 (происхождение связи), D8, Behavior Contract 2/3/7, § Решения verify, Assumptions, Risks, таблица срезов.
- `specs/scenario-map-canvas/spec.md`: Node contract + Scenario «Связь без видимого отношения не выдумывается»; линейная цепочка — подписи из порядка прохода.
- `tasks.md`: S2.1, S2.1a, S2.8, Связь и чеклист второго среза.

Без третьей секции `## Extend —` на незапущенные срезы (порог петли приёмки).

`Architect Gate:` не требовался (уточнение инварианта внутри выбранной оси; ось просьбы не переоткрывалась).

## Verify repair — 2026-08-28 (from-verify, deferred publish / offer split)

Источник: internal repair-from-verify по `reports/design-challenge-2026-08-28-5.md` (G1–G4) и `reports/architecture-task-readiness-2026-08-28-5.md` (передача макета на пути просьбы).

Что изменено:

- `design.md` D1 (ход публикации, исход к выходу без порога, согласие наследует раскладку), D3, Behavior 7/13, § Решения verify, таблица срезов, Risks.
- `specs/scenario-map-canvas/spec.md`: Direct request (раскладка согласия); сценарии «Отложенное согласие» уточнён; добавлены «Согласие было, порог до выхода не набрался», «Согласие при неподтвердившейся топологии даёт цепочку»; сценарий предложения разбора разведён на список и выход.
- `tasks.md`: S2.4a, S2.12; S3.2, S3.4; Связь и чеклист третьего среза.

Без секции `## Extend —` на незапущенные срезы (порог петли приёмки).

`Architect Gate:` не требовался (уточнение инвариантов внутри выбранной оси).

## Apply — 2026-08-28 (S2 + S3, приёмка отложена)

Пользователь на resume: «приму всё в конце, продолжай». Пауза приёмки S1 пропущена без отметки `[x]`. Рабочие задачи S2 и S3 закрыты в той же сессии.

### Slice S1 — Карта сценария по просьбе (2026-08-28, resume)

Срез: S1 — Карта сценария по просьбе
Решение: awaiting-acceptance (пропуск паузы по просьбе пользователя)
Обоснование: рабочие задачи S1 закрыты ранее; чекбокс S1.accept остаётся [ ].
Изменения tasks: нет
Связанный отчёт: reports/handoff-acceptance-S1-2026-08-27.md

### Slice S2 — Карта показывает причинность (2026-08-28)

Срез: S2 — Карта показывает причинность
Решение: awaiting-acceptance
Обоснование: рабочие задачи S2.1–S2.12 реализованы; приёмку пользователь отложил на конец.
Изменения tasks: S2.1–S2.12 отмечены [x]
Связанный отчёт: reports/handoff-acceptance-S2-2026-08-28.md

### Slice S3 — Команды предлагают схему по топологии (2026-08-28)

Срез: S3 — Команды предлагают схему по топологии
Решение: awaiting-acceptance
Обоснование: рабочие задачи S3.1–S3.7 реализованы; приёмку пользователь отложил на конец.
Изменения tasks: S3.1–S3.7 отмечены [x]
Связанный отчёт: reports/handoff-acceptance-S3-2026-08-28.md

### Kit verification

- Отдельной команды карты в `.cursor/commands/` и списке команд `AGENTS.md` нет.
- Frontmatter картографа: `model: inherit`; отдельного слага модели нет.
- Роль есть в `model-selection.mdc` (без `model=`), `tool-name-guard.mdc` (Generic/OpenSpec), `1c-agent-delegation.mdc` (вне таблицы 1С-ролей), `1c-agent-patterns/SKILL.md`, `AGENTS.md`.
- `opsx-output-style.md` и `brief-card.md` не менялись; термин «карта точек» сохранён.
- Порог и отказ ниже четырёх, просьба после выхода, отказ вне источника, просьба в исследовании → текущий отчёт — в скилле карты.

## Extend — 2026-08-28 (user-extend, канал публикации)

- источник: план финальной шлифовки, подтверждённый пользователем; живой опыт «нативная кнопка появилась, ссылка не работает»
- **Architect Gate:** `reports/architecture-extend-coherence-2026-08-28-2.md` — drift-warning, правки внутрь S2 (accept ещё открыт)
- что изменено: Why провал №3, D7/D8/D10, Behavior Contract 3/6/13, Blast Radius (снятие ссылки, parent Write), spec Direct request + три сценария, S2.1b/S2.4b/S2.8a/S2.13, упрощение Primary S1/S2/S3, Follow-up без checkbox
- ledger: `parent_side_registration`
- слияние S2+S2b оставлено в силе (нет собственного UX-результата) — тот же критерий для регистрации панели
- repair-from-verify (2026-08-28): шаблон панели рисует граф (`computeDAGLayout`); insight при только `follows` не причинный; аварийная строка пути если схемы не видно; self-check разделён на манифест (1–6) и регистрацию (7–8)
- следующий шаг: archive

## Slice Gate Decisions — приёмка 2026-08-28

### Slice S1 — Карта сценария по просьбе

Срез: S1 — Карта сценария по просьбе
Решение: accepted
Обоснование: без просьбы панель не создаётся; отдельной команды нет; песочница `temp/sandbox-scenario-map-2026-08-28`.
Изменения tasks: S1.accept [x]
Связанный отчёт: reports/slice-acceptance-S1-2026-08-28.md

### Slice S2 — Карта показывает причинность

Срез: S2 — Карта показывает причинность
Решение: accepted
Обоснование: родитель зарегистрировал файл; проверка панели чистая; штатная кнопка среды; ремонт ошибки типов пройден.
Изменения tasks: S2.accept [x]
Связанный отчёт: reports/slice-acceptance-S2-2026-08-28.md

### Slice S3 — Команды предлагают схему по топологии

Срез: S3 — Команды предлагают схему по топологии
Решение: accepted
Обоснование: на топологии одно предложение схемы; линейный случай молчит; предикаты без темы.
Изменения tasks: S3.accept [x]
Связанный отчёт: reports/slice-acceptance-S3-2026-08-28.md

