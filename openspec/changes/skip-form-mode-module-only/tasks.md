# Срез S1: Пропуск холостого вопроса поставки

**Сценарий:** На постановке «только модуль панели, разметку не трогаем» выбора из трёх нет; в карточке сразу поставка программно.
**Primary acceptance:** создать учебную ЗНИ с постановкой «только модуль панели, разметку не трогаем» → выбора вручную/автоматически/программно нет → в карточке поставка программно
**Приёмка:** учебный прогон `/opsx:new` в чате (только S1.accept) и сверка текстов агентом
**Связь со spec:** Requirement «Per-form delivery modes for managed forms» — Scenario «Form Mode question on design for in-scope form», Scenario «Multiple forms get sequential Mode questions», Scenario «No layout Mode question in new», Scenario «Layout stays manual unless apply permission», Scenario «Legacy single artifact_mode maps to form_mode», Scenario «Kit evolution without form modes», Scenario «Empty form mode blocks apply for in-scope form», Scenario «Layout non-manual requires recorded apply permission»; Requirement «Module-only form records programmatic delivery without a question» — Scenario «Module-only records programmatic without question», Scenario «Mixed forms sequential», Scenario «Resume does not overwrite recorded mode», Scenario «Informing line is not a selection question»
**Зависимости:** нет
**Режим apply:** mechanical

## 1. Классификатор и цикл new

- [ ] S1.1 Добавить в `.cursor/rules/forms-mxl-mode-gate.mdc` классификатор «только модуль / разметка / неясно» перед каноном вопроса, чтобы при доказанном «только модуль» записывать поставку программно без выбора из трёх и не выкидывать форму из списка: нужны признаки модуля и отсутствие токенов разметки (голого отсутствия Form.xml недостаточно; «добавить кнопку» без места поставки — неясно; «в модуле» / программные элементы — только модуль); «автоматически» молча не выбирать; набор значений режима не расширять; валидный записанный режим не переспрашивать и не перезаписывать; пустой/`n/a` при задаче на модуль формы не ставить и дыру режима не ослаблять (Decision 1–3, ADR-0001; Scenario «Module-only records programmatic without question», Scenario «Resume does not overwrite recorded mode», Scenario «Empty form mode blocks apply for in-scope form»)
- [ ] S1.2 Добавить в `.cursor/rules/forms-mxl-mode-gate.mdc` рекомендуемую поясняющую строку «Для формы «<ИмяФормы>» в этой ЗНИ меняется только модуль, разметку не трогаем — записываю поставку программно», чтобы это не считалось вопросом выбора и не требовало ответа для продолжения цикла форм (ADR-0001; Scenario «Informing line is not a selection question»). Зависимости: S1.1
- [ ] S1.3 Заменить в `.cursor/skills/openspec-new-change/SKILL.md` шаг 5.d.1: до канона вопроса прогонять классификатор Mode Gate, чтобы «только модуль» писался как программно без AskQuestion, а разметка или неясность по-прежнему давали один вопрос этой формы за ход с паузой до ответа; «автоматически» только явным ответом; пустой ответ на **заданный** вопрос — вручную; ветку kit без форм → `n/a` без вопроса не менять; вопрос макета в new не возвращать; режим соседней формы не копировать (Scenario «Form Mode question on design for in-scope form», Scenario «Mixed forms sequential», Scenario «Multiple forms get sequential Mode questions», Scenario «Kit evolution without form modes», Scenario «No layout Mode question in new»). Зависимости: S1.1

## 2. Справка kit

- [ ] S1.4 Добавить в `.cursor/docs/faq-kit.md` описание пропуска: если в ЗНИ только модуль формы и разметку не трогают, выбора из трёх нет и в карточке сразу программно; при разметке или неясности вопрос остаётся, пустой ответ — вручную (Goals §4)
- [ ] S1.5 Заменить в `.cursor/docs/quick-start.md` (таблица типовых сценариев и §5) формулировку «new всегда спросит режим формы»: вопрос задаётся не всегда — при «только модуль» его нет, в карточке поставка программно; макет на new по-прежнему не спрашивается

## 3. Регрессии (сверка по тексту)

- [ ] S1.6 Верифицировать по тексту `.cursor/rules/forms-mxl-mode-gate.mdc` § «Политика макетов» и `.cursor/skills/openspec-apply-change/SKILL.md`: без явного разрешения apply идёт ручная поставка макета, без молчаливой правки макета в репозитории (Scenario «Layout stays manual unless apply permission»). Зависимости: S1.1
- [ ] S1.7 Верифицировать по тексту `.cursor/rules/forms-mxl-mode-gate.mdc` § «Политика макетов» и `.cursor/skills/openspec-apply-change/SKILL.md`: non-manual путь макета допускается только при уже записанном разрешении (чат apply / одноразовый вопрос / маркер `[mxl:…]`) и записи в `debug.md` (Scenario «Layout non-manual requires recorded apply permission»). Зависимости: S1.1
- [ ] S1.8 Верифицировать по тексту `.cursor/rules/forms-mxl-mode-gate.mdc`, `.cursor/skills/openspec-apply-change/SKILL.md` и `.cursor/skills/openspec-verify-change/SKILL.md`: lone `artifact_mode` без `form_mode`/`forms:` по-прежнему читается как одинаковый режим всех форм текущего scope без переспроса (Scenario «Legacy single artifact_mode maps to form_mode»). Зависимости: S1.1

## 4. Приёмка

- [ ] S1.accept Принять срез S1 «Пропуск холостого вопроса поставки» — на постановке «только модуль» нет выбора из трёх, в карточке программно:
  - **Primary (обязательно):** создать учебную ЗНИ с постановкой «только модуль панели, разметку не трогаем» → выбора вручную/автоматически/программно нет → в карточке поставка программно
  - Scenario «Informing line is not a selection question» (опционально): если есть строка «записываю поставку программно» — это не выбор из трёх, цикл форм не ждёт ответа
  - Scenario «Form Mode question on design for in-scope form» (опционально): постановка с разметкой или «доработать форму» без ясности → в чате вопрос из трёх; пустой ответ → в карточке вручную
  - Scenario «Mixed forms sequential» (опционально): в одной ЗНИ форма A только модуль и форма B разметка → у A нет выбора и в карточке программно, у B отдельный вопрос; режимы разные
  - Scenario «Multiple forms get sequential Mode questions» (опционально): две или более формы с разметкой или неясностью → вопросы только им, по одной за сообщение; «только модуль» в том же списке уже записан как программно

<!-- slice-gate: на постановке «только модуль панели» выбора из трёх нет, в карточке поставка программно -->
