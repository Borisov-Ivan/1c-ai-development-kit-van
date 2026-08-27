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
closed_decisions: []
open_decision_id: null
decision_round: 0
decision_round_max: 2
verify_depth: full
assumptions_accepted: []
repair_attempt: 0
last_challenge_at: "2026-08-27T05:06:41Z"
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
