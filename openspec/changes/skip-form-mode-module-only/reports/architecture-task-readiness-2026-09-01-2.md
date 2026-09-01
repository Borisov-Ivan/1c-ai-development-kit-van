---
report_type: task-readiness
generated_at: 2026-09-01
agent: onec-code-architect
mode: task-readiness
scope:
  change: skip-form-mode-module-only
  slices: [S1]
  files:
    - openspec/changes/skip-form-mode-module-only/proposal.md
    - openspec/changes/skip-form-mode-module-only/design.md
    - openspec/changes/skip-form-mode-module-only/tasks.md
    - openspec/changes/skip-form-mode-module-only/specs/split-form-layout-modes/spec.md
    - .cursor/rules/forms-mxl-mode-gate.mdc
    - .cursor/skills/openspec-new-change/SKILL.md
    - .cursor/docs/faq-kit.md
    - .cursor/docs/quick-start.md
    - .cursor/skills/openspec-apply-change/SKILL.md
    - .cursor/skills/openspec-verify-change/SKILL.md
  modules: []
  capabilities:
    - split-form-layout-modes
related_reports:
  - reports/architecture-2026-09-01.md
  - reports/design-challenge-2026-09-01.md
  - reports/architecture-task-readiness-2026-09-01.md
  - reports/quality-control-2026-09-01-2.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Task readiness — skip-form-mode-module-only (повтор после repair)

ЗНИ `skip-form-mode-module-only` готова к реализации as-is: правки markdown правил kit по текущим proposal / design / tasks / spec не требуют возврата на уточнение. Ось Chosen A не пересматривалась.

Повтор относительно `reports/architecture-task-readiness-2026-09-01.md`: закрыты три пункта repair (сужение токенов классификатора; Mixed = запись программно + один вопрос в одном ходе; поясняющая строка MAY). Открытых вопросов в design нет.

## KB references

- совпадений нет — Discovery выполнен, якоря пусты. На оценку готовности не влияет.

## ADR references

- ADR-0001 (Load-Bearing): used — канон трёх русских вариантов только когда вопрос задаётся; поясняющая строка без служебных полей (`form_mode` / `bsl-only` / skill). Задачи S1.1–S1.2 и цитата строки в design это соблюдают.

## Precedent Coherence (доп. к таблице 1–8)

- Архив `2026-08-18-sequential-ui-mode-questions`: MUST-вопрос сужается; в `design.md` есть `## Blast Radius`. Запрет молчаливого «автоматически» и skip макета — extends. Конфликта с ADR-0001 нет. Repair не менял Blast Radius и не открывал ось A. GAP по прецеденту нет.

## Simplicity Check

- **Viable alternatives:** ось A/B/C закрыта (выбран A). Для реализации as-is отдельного пути нет: классификатор в существующем Mode Gate + правка шага 5.d.1 + справка + сверка регресса по тексту.
- **Selected simplest viable design:** A — форма остаётся в списке, вопрос не показывают, пишут программно. Не пересматривается.
- **Why not simpler:** «всегда спрашивать» не закрывает Why; смена default пропуска ломает безопасный пустой ответ для разметки; выкинуть форму из списка даёт дыру режима.
- **Complexity budget:** 5 файлов правки (gate, skill new, FAQ, quick-start; apply/verify только сверка), 0 новых хуков прикладного кода, 0 новых значений режима.

## Вердикт

**ГОТОВО**

Исполнитель (агент, mechanical markdown) может закрыть S1.1–S1.8 по design + spec + тексту задач. Пользователь — только приёмка на границе среза (учебный `/opsx:new` в S1.accept). Исполнимость приёмки «прямо сейчас» вне scope этой оценки.

Repair согласован: токены, Mixed и MAY строки зеркалятся в design § Behavior Contract / Decisions 8–9, spec и S1.1–S1.3 / optional accept. Повтор проверки срезов (`reports/quality-control-2026-09-01-2.md`) — OK; на реализуемость задач не противоречит.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | OK | «Код» = markdown kit. Каждая S1.1–S1.8 указывает путь, действие (добавить / заменить / верифицировать по тексту) и инвариант. Целевые файлы существуют. Точки вставки: `forms-mxl-mode-gate.mdc` — канон вопроса, цикл «форма → вопрос → END TURN», enumeration, запись, § Политика макетов, legacy `artifact_mode`, инвариант «один вопрос выбора за ход»; `openspec-new-change/SKILL.md` шаг 5.d.1 п.3 сейчас спрашивает каждую форму — замена на классификатор до канона, Mixed = запись skip + ровно один вопрос в том же ходе (совместимо с HALT двух выборов: поясняющая строка выбором не считается); `faq-kit.md` § «Режим формы»; `quick-start.md` таблица типовых сценариев и §5 («спросит» / вопрос не всегда); apply/verify skills уже содержат политику макета и lone `artifact_mode` для сверки S1.6–S1.8. Классификатор и «сомнение = вопрос» — в design § Behavior Contract; S1.1 дублирует минимальный набор после repair. |
| 2 | Реализуемость форм и метаданных | OK | Прикладных форм/метаданных нет (`form_mode: n/a`). Классификатор задан и после repair сужен: достаточные признаки работы **в модуле** (модуль формы, тела существующих обработчиков, заголовки существующих колонок **в модуле**, программные элементы, «разметку не трогаем» / «в модуле»); сами «обработчики» и «видимость уже существующих элементов» **без** «в модуле» — не skip (могут быть свойства/привязки в Конфигураторе); токены разметки (Form.xml, реквизиты как метаданные, элементы в Конфигураторе, состав полей/кнопок без «в модуле», привязка нового обработчика, видимость в Конфигураторе); голого отсутствия Form.xml недостаточно; «добавить кнопку» без места поставки — неясно → вопрос. Fallback «сомнение = вопрос» закрывает хвост. Полный онтологический список не нужен. |
| 3 | Разрешённость решений | OK | A/B/C закрыты (выбран A; не пересматривается). Default пустого ответа на **заданный** вопрос остаётся «вручную». «Автоматически» только явным ответом. Kit без форм → `n/a`, не программно. Скаляр vs map при одной форме — существующая гибкость gate. Decision 8: Mixed в одном ходе = запись программно + ровно один канон; строка не второй выбор. Decision 9: поясняющая строка MAY; отсутствие не дефект; критерий skip — запись в карточке. Открытых вопросов в design нет. |
| 4 | Полнота покрытия | OK | Оба requirement spec покрыты. ADDED «Module-only…»: Primary S1.accept + S1.1/S1.3; Mixed — S1.3 + optional accept (один ход); Resume — S1.1; Informing line — S1.2 + optional accept (MAY). MODIFIED «Per-form delivery modes…»: вопрос при разметке/неясности — S1.3 + optional accept; несколько форм — S1.3 + optional accept; kit `n/a` — S1.3; макет в new — S1.3/S1.5; дыра режима — S1.1; регресс макета — S1.6/S1.7; legacy `artifact_mode` — S1.8. Справка kit (proposal What Changes п.3) — S1.4/S1.5. 12/12 Scenario. Согласовано с QC-2. |
| 5 | Согласованность | OK | tasks ↔ design: классификатор перед каноном; суженные токены; форма в списке; запись программно (`bsl-only`); строка чата дословно; Mixed один ход; MAY строки; apply/verify не менять, только сверка. tasks ↔ spec: chat-facing «программно» = `bsl-only`; Mixed THEN и Informing line MAY совпадают. Задачи говорят «Добавить/Заменить/Верифицировать», не «создать файл» — файлы в репо есть. Blast Radius согласован с MODIFIED WHEN вопроса. proposal Decision 4 = design Decision 9. |
| 6 | Связность кода и порядок задач | OK | Явные зависимости: S1.2, S1.3, S1.6–S1.8 → S1.1. S1.4/S1.5 самодостаточны по тексту справки. Ровно один `S1.accept`. Маркер `<!-- slice-gate -->` на месте. Межсрезовых зависимостей нет. Циклов нет. Порядок в файле: классификатор → цикл new → справка → регресс → приёмка. Repair не добавил задач и не размыл границу среза. |
| 7 | Архитектурная эстетика (Design Smells) | OK | Классификатор из трёх классов в существующем цикле 5.d.1 — не новый гейт и не новый enum. «Всегда спрашивать» отвергнут контрактом Why, не вкусом. Не инвазивно (нет BSL/XML). Переиспользуется класс skip (макет / kit `n/a`) с обязательной записью режима. Сужение токенов уменьшает ложноположительный skip — не over-engineering. Mixed в одном ходе не плодит второй выбор. |
| 8 | User Task Contract | OK | В S1.1–S1.8 нет user runtime-spike (ИБ, консоль, отладчик, API, «спайк», «на стенде»). S1.6–S1.8 — «верифицировать по тексту» (агент, static). Подстроки «вручную» / «Конфигуратор» в S1.1 — токены классификатора и названия вариантов чата, не ручная конфигурация этой ЗНИ. Учебный `/opsx:new` только в S1.accept — допустимая приёмка на границе среза. Structural spike в `S<N>.<M>` отсутствует. Repair не добавлял spike. |

## Пробелы

Нет (GAP / SUBOPTIMAL не зафиксированы).

## Источники

- `proposal.md` — Why, What Changes, Acceptance, Decisions (строка рекомендуется)
- `design.md` — Behavior Contract п.1–8, Decisions 1–9, Blast Radius, Slices, Решения verify
- `tasks.md` — S1.1–S1.8, S1.accept, slice-gate
- `specs/split-form-layout-modes/spec.md` — MODIFIED + ADDED, 12 Scenario
- `debug.md` — repair-from-verify (токены, Mixed, MAY)
- Целевые файлы kit (проверено наличие и точка вставки)
- ADR-0001
- `reports/quality-control-2026-09-01-2.md` — Verdict OK
- `reports/architecture-task-readiness-2026-09-01.md` — оценка до repair (открытый вопрос строки; более широкие токены в критерии 2)
