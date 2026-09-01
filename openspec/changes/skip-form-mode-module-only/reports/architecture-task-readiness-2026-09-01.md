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
  - reports/quality-control-2026-09-01.md
confidence: high
open_questions_count: 0
superseded_by: null
---

# Task readiness — skip-form-mode-module-only

ЗНИ `skip-form-mode-module-only` готова к реализации as-is: правки markdown правил kit по текущим proposal / design / tasks / spec не требуют возврата на уточнение.

## KB references

- совпадений нет — таксономия отсутствует, Discovery выполнен, якоря пусты. На оценку готовности не влияет.

## ADR references

- ADR-0001 (Load-Bearing): used — канон трёх русских вариантов только когда вопрос задаётся; поясняющая строка без служебных полей (`form_mode` / `bsl-only` / skill). Задачи S1.1–S1.2 и цитата строки в design это соблюдают.

## Precedent Coherence (доп. к таблице 1–8)

- Архив `2026-08-18-sequential-ui-mode-questions`: MUST-вопрос сужается; в `design.md` есть `## Blast Radius`. Запрет молчаливого «автоматически» и skip макета — extends. Конфликта с ADR-0001 нет. GAP по прецеденту нет.

## Вердикт

**ГОТОВО**

Исполнитель (агент, mechanical markdown) может закрыть S1.1–S1.8 по design + spec + тексту задач. Пользователь — только приёмка на границе среза (учебный `/opsx:new` в S1.accept). Открытый вопрос design про поясняющую строку не блокирует: S1.2 требует рекомендуемую, не обязательную строку.

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач | OK | «Код» = markdown kit. Каждая S1.1–S1.8 указывает путь, действие (добавить / заменить / верифицировать по тексту) и инвариант. Целевые файлы существуют: `forms-mxl-mode-gate.mdc` (канон вопроса, enumeration, запись, § Политика макетов, legacy `artifact_mode`); `openspec-new-change/SKILL.md` шаг 5.d.1 п.3 сейчас спрашивает каждую форму — точка замены; `faq-kit.md` § «Режим формы»; `quick-start.md` таблица §3 и §5; apply/verify skills для регресса S1.6–S1.8 уже содержат политику макета и lone `artifact_mode`. Классификатор, токены и «сомнение = вопрос» есть в design § Behavior Contract; задача S1.1 дублирует минимальный набор примеров. |
| 2 | Реализуемость форм и метаданных | OK | Прикладных форм/метаданных нет (`form_mode: n/a`). Классификатор «только модуль / разметка / неясно» задан: положительные признаки модуля (модуль формы, заголовки существующих колонок, обработчики, видимость существующих элементов, «разметку не трогаем» / «в модуле» / программные элементы); токены разметки (Form.xml, реквизиты как метаданные, элементы в Конфигураторе, состав полей/кнопок без «в модуле»); голого отсутствия Form.xml недостаточно; «добавить кнопку» без места поставки — неясно → вопрос. Исполнителю не нужен полный онтологический список: fallback «сомнение = вопрос» закрывает хвост. |
| 3 | Разрешённость решений | OK | A/B/C в design закрыты (выбран A). Default пустого ответа на **заданный** вопрос остаётся «вручную». «Автоматически» только явным ответом. Kit без форм → `n/a`, не программно. Скаляр vs map при одной форме — уже существующая гибкость gate, не новая развилка. Открытый вопрос «поясняющая строка рекомендуется, не обязательно» **не GAP**: S1.2 добавляет **рекомендуемую** строку и запрет считать её выбором; spec — MAY; обязательности без выбора нет. |
| 4 | Полнота покрытия | OK | Оба requirement spec покрыты задачами. ADDED «Module-only…»: Primary S1.accept + S1.1/S1.3; Mixed — S1.3 + optional accept; Resume — S1.1; Informing line — S1.2 + optional accept. MODIFIED «Per-form delivery modes…»: вопрос при разметке/неясности — S1.3 + optional accept; несколько форм — S1.3 + optional accept; kit `n/a` — S1.3; макет в new — S1.3/S1.5; дыра режима — S1.1; регресс макета — S1.6/S1.7; legacy `artifact_mode` — S1.8. Справка kit (proposal What Changes п.3) — S1.4/S1.5. 12/12 Scenario. |
| 5 | Согласованность | OK | tasks ↔ design: классификатор перед каноном; форма остаётся в списке; запись программно (`bsl-only`); строка чата дословно совпадает; apply/verify не менять, только сверка текста. tasks ↔ spec: chat-facing «программно» в задачах = `bsl-only` в spec (таблица gate). Задачи говорят «Добавить/Заменить/Верифицировать», не «создать файл» — файлы в репо есть. Blast Radius в design согласован с MODIFIED WHEN вопроса. |
| 6 | Связность кода и порядок задач | OK | Явные зависимости: S1.2, S1.3, S1.6–S1.8 → S1.1. S1.4/S1.5 самодостаточны по тексту (FAQ/quick-start) и не ломают порядок. Ровно один `S1.accept`. Маркер `<!-- slice-gate -->` на месте. Межсрезовых зависимостей нет (`**Зависимости:** нет` у среза). Циклов нет. Порядок в файле: классификатор → цикл new → справка → регресс → приёмка. |
| 7 | Архитектурная эстетика (Design Smells) | OK | Классификатор из трёх классов в существующем цикле 5.d.1 — не новый гейт и не новый enum. «Всегда спрашивать» отвергнут контрактом Why (холостой вопрос + вредный default «вручную»), не вкусом. Не инвазивно (нет BSL/XML). Переиспользуется класс skip (макет / kit `n/a`) с обязательной записью режима, чтобы не открыть дыру. Over-engineering нет. |
| 8 | User Task Contract | OK | В S1.1–S1.8 нет user runtime-spike (ИБ, консоль, отладчик, API). S1.6–S1.8 — «верифицировать по тексту» (агент, static). Подстроки «вручную» / «Конфигуратор» в S1.1 — токены классификатора и названия вариантов чата, не ручная конфигурация этой ЗНИ. Учебный `/opsx:new` только в S1.accept — допустимая приёмка на границе среза. Structural spike в `S<N>.<M>` отсутствует. |

## Пробелы

Нет (GAP / SUBOPTIMAL не зафиксированы).

## Источники

- `proposal.md` — Why, What Changes, Acceptance, Decisions (строка рекомендуется)
- `design.md` — Behavior Contract, Decisions 1–3, Blast Radius, Slices, открытый вопрос про строку
- `tasks.md` — S1.1–S1.8, S1.accept, slice-gate
- `specs/split-form-layout-modes/spec.md` — MODIFIED + ADDED, 12 Scenario
- Целевые файлы kit (проверено наличие и точка вставки)
- ADR-0001
