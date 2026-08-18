# hardcode-justification-gate

## Purpose

Обязательное обоснование хардкода-фильтра идентичности (allow-list имён форм/метаданных) в цепочке проектирования и ревью kit — зеркало каркаса Попытка.

## Requirements

### Requirement: Identity-filter has a named anti-pattern and remediation

В реестре антипаттернов MUST быть класс Hardcoded Identity Filter (AP-055 или актуальный свободный номер) с детекторами runtime-фильтра по строкам имён форм/метаданных и remediation: делегировать фильтр API/настройке либо заполнить секцию Hardcode Justification в design.

#### Scenario: Registry describes identity-filter class

- **WHEN** ревьюер или архитектор ищет норму для allow-list имён форм в хуке
- **THEN** в реестре есть именованный антипаттерн с признаками `ИмяФормы`/литерал открытия формы/список имён метаданных и путём исправления без «просто помни»

#### Scenario: Protocol literals are out of class by default

- **WHEN** в коде литерал кода отказа или ключа протокола API (не фильтр охвата UI)
- **THEN** норма identity-filter не требует MUST_FIX только из-за наличия строкового литерала

### Requirement: Architect cannot choose allow-list without justification

До выбора варианта со списком имён форм/объектов архитектор MUST пройти Identity Filter Gate (callee уже фильтрует? набор закрыт навсегда? план при N+1?) и зафиксировать ответы в design.

#### Scenario: Thin allow-list is not Chosen without answers

- **WHEN** в design предлагается «тонкий» allow-list имён форм как контроль охвата хука
- **THEN** вариант не становится выбранным, пока нет секции Hardcode Justification с ответами на три вопроса Gate

### Requirement: Writer halts on unjustified identity literals

Перед добавлением identity-filter литералов writer MUST остановиться, если в design нет Hardcode Justification и нет явного запрета списка (всегда звать API).

#### Scenario: Allow-list without design section blocks writer

- **WHEN** задача требует добавить сравнения с полными именами форм, а в design нет Hardcode Justification
- **THEN** реализация не продолжается как обычная правка — требуется устранение конфликта постановки

### Requirement: Reviewer audits identity literals with completeness

Ревьюер MUST иметь выделенный проход Identity / Hardcode Audit: перечисление находок, строка на каждый литерал-фильтр, contradiction с «без хардкода» в Why/Non-Goals — MUST_FIX.

#### Scenario: Completeness matches literal count

- **WHEN** в изменённом модуле три сравнения `ИмяФормы` с полными именами как guard хука
- **THEN** в отчёте ревью по identity-filter ровно три строки таблицы с вердиктом по каждой

#### Scenario: Contradiction with no-hardcode goal is blocking

- **WHEN** в постановке change зафиксировано «без хардкода», а в коде есть allow-list имён форм без обоснования
- **THEN** замечание имеет блокирующий характер по норме identity-filter

### Requirement: Existing Mechanisms covers Scope-as-literals

Документ приоритета существующих механизмов MUST описывать запах сведения охвата к литералам имён вместо критерия класса и отсылать к секции Hardcode Justification.

#### Scenario: Smell is documented next to mechanism hierarchy

- **WHEN** архитектор проходит Existing Mechanisms для хука с узким списком имён
- **THEN** в правилах есть запах Scope-as-literals и указание заполнить обоснование хардкода, а не только Shadow Storage / Parallel Workflow
