# Срез S1: Один вопрос за ход

**Сценарий:** При создании ЗНИ пользователь отвечает на один выбор за сообщение; следующий гейт не смешивается с предыдущим.
**Primary acceptance:** В учебном прогоне `/opsx:new` после ответа на вопрос про маркер (или его пропуск) вопрос про режим формы не появляется в том же сообщении; первый Mode-вопрос — отдельным сообщением на этапе design (между Metadata и Mode допустимы сообщения без выбора).
**Приёмка:** ручная проверка по протоколу SKILL (прогон сценария new) + сверка текста правил
**Связь со spec:** Requirement «One selection question per orchestrator turn»; Scenario «Metadata question without Mode Gate in same message», «Second gate only after answer», «Dual selection questions blocked»
**Зависимости:** нет
**Режим apply:** mechanical

## 1. Протокол new и карточка Metadata

- [x] S1.1 В `.cursor/skills/openspec-new-change/SKILL.md` закрепить END TURN после Metadata Gate и запрет ≥2 вопросов выбора в одном сообщении (в т.ч. не вызывать Mode Gate в том же ходе) — (Decision design: инвариант одного вопроса)
- [x] S1.2 В `.cursor/docs/templates/brief-card.md` (секция Metadata Gate) явно запретить соседние вопросы (Mode Gate / дизайн) в том же сообщении, что и выбор описания маркера
- [x] S1.3 В self-check `/opsx:new` добавить пункт HALT: черновик ответа с двумя карточками/нумерованными выборами не отправлять
- [x] S1.accept Принять срез S1 «Один вопрос за ход» — маркеры и Mode Gate не в одном экране:
  - **Primary (обязательно):** учебный `/opsx:new` — после ответа на маркер (или пропуска) Mode-вопрос не в том же сообщении; первый выбор режима формы — отдельным сообщением на design
  - Scenario «Dual selection questions blocked» (опционально): по тексту SKILL dual AskQuestion запрещён в self-check

<!-- slice-gate: После маркера следующий выбор режима формы только отдельным сообщением -->

# Срез S2: Режимы форм (per-form)

**Сценарий:** У каждой формы в scope свой режим поставки; вопросы — на design по одной форме; макет без Mode-вопроса в new.
**Primary acceptance:** В учебном proposal с двумя формами заданы разные `form_mode`; вопросы на design идут по одной форме с паузой; макет в new не спрашивается; apply к макету по умолчанию вручную.
**Приёмка:** сверка текстов gate/skills + учебный сценарий записи proposal
**Связь со spec:** Requirement «Per-form delivery modes for managed forms»; Scenario «Form Mode question on design…», «Multiple forms…», «No layout Mode question…», «Layout stays manual…», «Legacy…», «Kit evolution…», «Empty form mode…», «Layout non-manual requires recorded apply permission»
**Зависимости:** S1
**Режим apply:** mechanical

## 1. Mode Gate SSOT

- [x] S2.1 В `.cursor/rules/forms-mxl-mode-gate.mdc` заменить склейку «форму/макет» и единый `artifact_mode` на Mode Gate **только формы**: вопрос с указанием конкретной формы; канон записи `## Forms mode` + скаляр/`forms:` map (ключ метаданных); `form_mode` ∈ {manual, assisted, bsl-only, n/a}; вопрос макета в new не задавать; политика макета — manual default, non-manual только по норме разрешения Decision 9 — (Decision design: 1, 2, 6, 9)
- [x] S2.2 В `.cursor/skills/openspec-new-change/SKILL.md` перенести Mode Gate форм на этап design после enumeration scope (Decision 3a): цикл «одна форма → один вопрос → END TURN → запись»; без форм — `form_mode: n/a`; закрыть вопросы режимов до Design Gate AskQuestion; resume: валидные режимы форм не переспрашивать; lone legacy `artifact_mode` → одинаковый режим на весь текущий form-scope; при extend/новой форме в scope — вопрос только для этой формы

## 2. Потребители apply / verify / skills

- [x] S2.3 В `.cursor/skills/openspec-apply-change/SKILL.md` читать per-form `form_mode` / map `forms:` (+ fallback legacy `artifact_mode`); пустой/`n/a` при задаче на форму без режима — STOP/extend; для Template/MXL — manual default; non-manual — только при записанном разрешении (чат/AskQuestion/`[mxl:…]` + `debug.md` § Apply permissions), не Mode-вопрос new
- [x] S2.4 В `.cursor/skills/openspec-verify-change/SKILL.md` согласовать проверки Forms mode: секция `## Forms mode` (+ legacy-заголовок на чтение), per-form/`forms:`, fallback legacy, блокер пустого/`n/a` для формы; отсутствие Mode Gate макета не считается дефектом этой ЗНИ
- [x] S2.5 Обновить ссылки/таблицы режимов на `form_mode` / `forms:` (+ legacy `artifact_mode` где нужен fallback) в `.cursor/skills/1c-forms/SKILL.md`, `.cursor/skills/1c-forms/compile/SKILL.md`, `.cursor/skills/1c-forms/edit/SKILL.md`, `.cursor/rules/1c-xml-write-guard.mdc`, `.cursor/skills/openspec-explore/templates/handoff-block.md`, `.cursor/docs/kit-template-workflow.md`; в `1c-mxl` — не resurrect Mode Gate макета в new, отразить manual default / permission on apply + запись разрешения
- [x] S2.accept Принять срез S2 «Режимы форм (per-form)» — разные режимы разных форм и отсутствие Mode-вопроса макета:
  - **Primary (обязательно):** в учебном proposal с двумя формами заданы разные `form_mode` (map); по тексту new вопросы на design по одной форме; макет в new не спрашивается; apply к макету по умолчанию вручную
  - Scenario «Multiple forms get sequential Mode questions» (опционально): две формы → два хода с END TURN
  - Scenario «Legacy single artifact_mode maps to form_mode» (опционально): lone legacy → одинаковый режим на весь form-scope
  - Scenario «Kit evolution without form modes» (опционально): `form_mode: n/a`, вопрос не задаётся
  - Scenario «Empty form mode blocks apply for in-scope form» (опционально): пустой/`n/a` при задаче на форму → STOP/extend
  - Scenario «Layout stays manual unless apply permission» (опционально): без явного разрешения — только manual для макета
  - Scenario «Layout non-manual requires recorded apply permission» (опционально): non-manual только при записи в debug § Apply permissions или маркере `[mxl:…]`

<!-- slice-gate: Per-form form_mode на design; макет без Mode-вопроса в new -->

## Follow-up

- [ ] F1 Заполнить `developer` в proposal.md / project.md, если появятся маркеры кода (сейчас маркеры не нужны)
- [ ] F2 Рассмотреть маркер задач `[form:…]` симметрично `[mxl:…]` (вне Primary этой ЗНИ)
