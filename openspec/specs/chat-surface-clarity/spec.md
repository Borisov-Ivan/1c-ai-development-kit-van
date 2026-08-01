# chat-surface-clarity

## Purpose

Требования к текстам оркестратора в чат: Тест понятности, запрет жаргона kit в copy-paste канонах, разделение thin-chat и файла отчёта.

## Requirements

### Requirement: Chat-facing canons pass the readability test

Оркестратор MUST копировать в чат только формулировки, по которым разработчик 1С выбирает вариант, не зная внутренних имён kit (skill, compile/edit, имена гейтов, Schema, имена субагентов).

#### Scenario: Mode Gate question is product language

- **WHEN** на этапе design `/opsx:new` задаётся вопрос режима управляемой формы
- **THEN** в чате три варианта: вручную в Конфигураторе; автоматически — правки Form.xml в репозитории; программно — только модуль формы; и нет упоминаний skill, compile/edit или «уже в поставке»

#### Scenario: Good examples do not teach jargon

- **WHEN** оркестратор сверяется с decision-block или chat-lexicon для ярлыков режима формы
- **THEN** эталон «хорошо» / замена для `assisted` не содержит «через skill» как обязательную формулировку для чата

### Requirement: Process noise is not shown before a choice

Перед вопросом выбора режима формы оркестратор MUST NOT выводить процессные статусы артефактов (запись маркера, «proposal/design набросаны» и аналогичные non-events).

#### Scenario: Mode question has no process preamble

- **WHEN** оркестратор задаёт вопрос режима формы
- **THEN** сообщение содержит канон вопроса (и при необходимости одну строку зачем нужен выбор) без лога внутренних шагов new

### Requirement: Command AskQuestion and handoff stay user-facing

Шаблоны AskQuestion и thin-chat в new, apply, status, review и verify MUST использовать русские ярлыки ролей и решений; имена гейтов, Schema и `onec-code-*` MUST оставаться в debug/reports или agent-контексте.

#### Scenario: Slice acceptance prompt without gate names

- **WHEN** apply спрашивает вердикт по приёмке среза
- **THEN** текст для пользователя сформулирован как «Что решить» / приёмка среза без заголовка с именем внутреннего гейта и без голого кода задачи как единственного заголовка

#### Scenario: Apply pause label is product language

- **WHEN** apply показывает варианты продолжения работы после среза или паузы
- **THEN** в тексте для пользователя нет ярлыка «Пошаговая пауза»; варианты сформулированы на языке эффекта (продолжить / остановиться / принять срез)

#### Scenario: Review fix prompt without agent slugs

- **WHEN** review предлагает устранить замечания
- **THEN** варианты говорят «агент» / «упростить код», а не имена субагентов kit

#### Scenario: Status and handoff separate chat from file

- **WHEN** выводится статус change или handoff apply
- **THEN** в чате нет блока Schema и markdown-таблиц срезов; полный структурированный handoff при необходимости лежит в отчёте

### Requirement: SSOT documents do not contradict each other on chat bans

Документы opsx-output-style, brief-card и chat-lexicon MUST одинаково запрещать имена агентов в чате и MUST NOT требовать секцию KB в entry-брифе.

#### Scenario: Entry brief excludes KB list

- **WHEN** оркестратор показывает entry-бриф explore или extend
- **THEN** в брифе нет обязательного слота со списком KB-фактов; discovery остаётся во внутреннем контексте агентов

#### Scenario: Agent names banned uniformly

- **WHEN** self-check перед сообщением в чат ссылается на opsx-output-style и lexicon
- **THEN** оба источника запрещают slug субагентов в user-facing тексте (допустимы «агент», «ревьюер», «архитектор»)

### Requirement: Docs for humans match the Mode Gate canon

faq-kit и quick-start MUST описывать вопрос режима формы через `form_mode` и русские ярлыки; MUST NOT утверждать, что Mode Gate в new спрашивает способ поставки макета.

#### Scenario: FAQ matches form-only Mode Gate

- **WHEN** разработчик читает faq-kit про вопрос режима формы
- **THEN** таблица использует `form_mode` и не обещает вопрос про макет на `/opsx:new`
