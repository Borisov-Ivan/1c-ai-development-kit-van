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

### Requirement: Apply pause-wait is a navigator card

Когда `/opsx:apply` останавливается, потому что следующий шаг человека — создать или поправить объекты в Конфигураторе, выгрузить расширение или завести доп.реквизиты в ИБ, оркестратор MUST показать в чате карточку-навигатор: где мы; нумерованный список того, что создать; якорь файла **и имя раздела** с рецептом; как вернуться. Оркестратор MUST NOT заменять этот список одной ссылкой на `handoff-pause-*.md` и MUST NOT выдавать прогресс «0 из N» или перечень отсутствующих XML как тело сообщения.

#### Scenario: Apply pause-wait lists objects in chat

- **WHEN** apply останавливается: в выгрузке расширения нет объектов, без которых нельзя писать код модулей
- **THEN** в чате первая строка говорит, где мы (код пока не пишу, сначала объекты); есть нумерованный список того, что создать; указан файл паузы **и** раздел «Что создать в Конфигураторе»; нет «0/N задач» и списка отсутствующих XML как тела сообщения

#### Scenario: Pause-wait is not a decision fork

- **WHEN** единственный путь вперёд — создать объекты по рецепту (имена в живой базе могут отличаться)
- **THEN** в чате нет заголовка выбора «сделать чеклист или имена другие»; расхождение имён — одна фраза в конце («напишите фактические»), не развилка A/B

#### Scenario: Isolated chat E4 rejects a file-only pause

- **WHEN** в новом чате вызывают `/opsx:apply` на ЗНИ без объектов в выгрузке
- **THEN** первое сообщение не состоит из заголовка «Сессия приостановлена» плюс ссылки на `handoff-pause-*.md` без списка «что создать»

### Requirement: Pause-wait file leads with the recipe

Файл `reports/handoff-pause-*.md` при pause-wait MUST начинать человеческую часть с раздела «Что создать в Конфигураторе». Перечень отсутствующих путей XML MUST быть приложением, не шапкой. Секция «Что проверить СЕЙЧАС» MUST говорить, что сценарий на ИБ не гонять, пока нет объектов.

#### Scenario: Первый раздел файла — что создать

- **WHEN** разработчик открывает файл паузы по ссылке из чата
- **THEN** первым содержательным разделом идёт «Что создать в Конфигураторе» с именами, типами и шагами; не список «ничего в коде» из идентификаторов выгрузки

### Requirement: Command AskQuestion and handoff stay user-facing

Шаблоны AskQuestion и thin-chat в new, apply, status, review и verify MUST использовать русские ярлыки ролей и решений; имена гейтов, Schema и `onec-code-*` MUST оставаться в debug/reports или agent-контексте. Thin-chat apply MUST NOT вырезать инвентарь pause-wait: список «что создать» остаётся в чате, таблицы прогресса — в файле.

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
- **THEN** в чате нет блока Schema и markdown-таблиц срезов; полный структурированный handoff при необходимости лежит в отчёте; при pause-wait в чате есть список объектов, а не только ссылка на отчёт

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
