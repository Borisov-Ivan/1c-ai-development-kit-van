# split-form-layout-modes

## Purpose

Per-form режимы поставки управляемой формы; макет вне Mode Gate на new.

## Requirements

### Requirement: Per-form delivery modes for managed forms

Proposal ЗНИ с управляемыми формами SHALL хранить режим поставки формы: `form_mode` со значениями `manual`, `assisted`, `bsl-only` или `n/a` (при нескольких формах — YAML-map `forms:` с каноническим ключом метаданных формы → mode; при одной форме допустим скаляр). Вопрос про режим SHALL задаваться на этапе формирования design после стабилизации списка форм в scope, отдельно для каждой формы, и SHALL NOT задаваться для табличного макета (Template/MXL) в `/opsx:new`. Макет по умолчанию поставляется вручную; иной путь для макета — только по явному разрешению пользователя во время apply (чат apply / одноразовый AskQuestion / маркер `[mxl:…]` в tasks), с фиксацией в `debug.md`.

#### Scenario: Form Mode question on design for in-scope form

- **WHEN** постановка на этапе design затрагивает управляемую форму без записанного режима этой формы
- **THEN** оркестратор задаёт один вопрос про поставку **этой** формы и записывает её `form_mode` до приёмки design

#### Scenario: Multiple forms get sequential Mode questions

- **WHEN** в scope две или более управляемых формы без режимов
- **THEN** оркестратор задаёт вопросы по одной форме за сообщение (с паузой до ответа) и допускает разные `form_mode` у разных форм

#### Scenario: No layout Mode question in new

- **WHEN** постановка затрагивает табличный макет
- **THEN** в `/opsx:new` оркестратор не задаёт Mode Gate вопрос про способ поставки макета

#### Scenario: Layout stays manual unless apply permission

- **WHEN** apply выполняет задачи по Template/MXL и пользователь не дал явного разрешения на non-manual путь
- **THEN** apply следует ручной поставке макета (инструкция / WAIT), без молчаливого `assisted`/`compile`

#### Scenario: Legacy single artifact_mode maps to form_mode

- **WHEN** в proposal есть только устаревшее поле `artifact_mode` с валидным значением и нет скаляра `form_mode` / map `forms:`
- **THEN** apply и verify трактуют это значение как одинаковый `form_mode` для всех форм, уже входящих в scope на момент чтения (включая N>1), без переспроса

#### Scenario: Kit evolution without form modes

- **WHEN** ЗНИ — эволюция kit без правки Form.xml прикладной конфигурации
- **THEN** в proposal `form_mode: n/a` (или эквивалент «без форм»), вопрос Mode Gate формы не задаётся

#### Scenario: Empty form mode blocks apply for in-scope form

- **WHEN** в постановке есть задача на управляемую форму, а режим этой формы пуст либо `n/a` (и нет валидного lone legacy `artifact_mode`)
- **THEN** apply и verify останавливаются с требованием дозаполнить режим формы (STOP/extend или Mode-вопрос), не подставляя режим другой формы и не выбирая default молча

#### Scenario: Layout non-manual requires recorded apply permission

- **WHEN** apply собирается выполнить non-manual путь для Template/MXL
- **THEN** путь допускается только при уже зафиксированном разрешении (ответ в чате apply, одноразовый AskQuestion или маркер `[mxl:…]` / явная запись в tasks) и записи в `debug.md` § Apply permissions; иначе apply остаётся на manual (инструкция / WAIT)
