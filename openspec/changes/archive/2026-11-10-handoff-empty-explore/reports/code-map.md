# Срез S1 — Постановка не теряется (2026-11-10)

- **S1.1** · создание заявки · шаг 1 (modified) — короткое подтверждение до записи описания, если имя есть, а блока постановки нет. [`.cursor/skills/openspec-new-change/SKILL.md`](../../../../.cursor/skills/openspec-new-change/SKILL.md):29-33
- **S1.2** · создание заявки · шаг 1 (modified) — согласие на этом пути считается постановкой; поле архитектора этот источник не заполняет. [`.cursor/skills/openspec-new-change/SKILL.md`](../../../../.cursor/skills/openspec-new-change/SKILL.md):32-32
- **S1.3** · создание заявки · сводка подтверждений (modified) — подтверждение названо и для имени без блока; готовый блок остаётся без паузы. [`.cursor/skills/openspec-new-change/SKILL.md`](../../../../.cursor/skills/openspec-new-change/SKILL.md):18-18
- **S1.4** · создание заявки · продолжение каталога (modified) — подтверждение из записанного описания, второй каталог не создаётся. [`.cursor/skills/openspec-new-change/SKILL.md`](../../../../.cursor/skills/openspec-new-change/SKILL.md):161-168
- **S1.5** · создание заявки · разбор решения (modified) — остановка «нет постановки» на пути с именем недостижима, сложное изменение идёт в уже существующий запуск анализа. [`.cursor/skills/openspec-new-change/SKILL.md`](../../../../.cursor/skills/openspec-new-change/SKILL.md):342-347
- **S1.6** · создание заявки · тексты остановок (modified) — отказ и прерванный ход дают одну команду с именем; пропуск разбора решения вынесен отдельной строкой. [`.cursor/skills/openspec-new-change/SKILL.md`](../../../../.cursor/skills/openspec-new-change/SKILL.md):33-33
- **S1.7** · финал разбора · один следующий шаг (modified) — без требований продолжение тем же именем, с требованиями и задачами — дописывание. [`.cursor/skills/openspec-explore/SKILL.md`](../../../../.cursor/skills/openspec-explore/SKILL.md):252-252
- **S1.8** · финал разбора · строка бага и дефект в открытой заявке (modified) — то же различие требований. [`.cursor/skills/openspec-explore/SKILL.md`](../../../../.cursor/skills/openspec-explore/SKILL.md):60-60
- **S1.9** · пустой разбор · первый ход (modified) — новый чат без текста ждёт описание и не подставляет прошлую тему. [`.cursor/skills/openspec-explore/SKILL.md`](../../../../.cursor/skills/openspec-explore/SKILL.md):29-29
- **S1.11** · слот «Дальше» (modified) — команда новой заявки только в сообщении с блоком постановки. [`.cursor/skills/openspec-explore/SKILL.md`](../../../../.cursor/skills/openspec-explore/SKILL.md):220-220
- **S1.12** · явная просьба создать заявку (modified) — без блока команды новой заявки нет; каталог без требований продолжается тем же именем. [`.cursor/skills/openspec-explore/SKILL.md`](../../../../.cursor/skills/openspec-explore/SKILL.md):295-301
- **S1.10** · сверка шагов 1–2, остановок, финала и слота «Дальше» (modified) — расхождения закрыты в текстах правил; поле архитектора, порядок артефактов и нарезка после списка задач не переписывались.

Полная карта этого среза — этот файл. Кода модулей в срезе нет.

# Срез S2 — Признаки только модуля (2026-11-10)

- **S2.1** · правило режима формы · абзац признаков (modified) — признаки «только модуль» берутся из слов заказчика, блока постановки или кода. [`.cursor/rules/forms-mxl-mode-gate.mdc`](../../../../.cursor/rules/forms-mxl-mode-gate.mdc):47-47
- **S2.2** · правило режима формы · строка «Не skip» (modified) — «всё в модуле» только из решения того же хода оставляет вопрос, программная поставка до ответа не записывается. [`.cursor/rules/forms-mxl-mode-gate.mdc`](../../../../.cursor/rules/forms-mxl-mode-gate.mdc):53-53
- **S2.3** · создание заявки · цикл форм (modified) — ветка «только модуль» ссылается на абзац признаков и не копирует список. [`.cursor/skills/openspec-new-change/SKILL.md`](../../../../.cursor/skills/openspec-new-change/SKILL.md):310-310
- **S2.4** · сверка правила и цикла форм (modified) — расхождение закрыто в правиле; запись программно без вопроса при доказанном «только модуль» сохранена. Смесь форм и поясняющая строка не переписывались.

Кода модулей в срезе нет.

# Срез S3 — Хвост одной строки (2026-11-10)

- **S3.1** · грамматика пометок · исключение одной строки (modified) — одна оставшаяся строка кода несёт хвост открывающей пометки. [`.cursor/docs/marker-canon.md`](../../../../.cursor/docs/marker-canon.md):113-124
- **S3.2** · оформление при разработке (modified) — то же размещение для одной строки, нескольких строк, константы, вставки, удаления и строки со своим комментарием. [`.cursor/agents/onec-code-writer.md`](../../../../.cursor/agents/onec-code-writer.md):113-122
- **S3.3** · сборка пометки (modified) — размещение передаётся вместе с пометкой, текст открывающей пометки не меняется. [`.cursor/skills/openspec-apply-change/SKILL.md`](../../../../.cursor/skills/openspec-apply-change/SKILL.md):130-130
- **S3.4** · проверка комментариев (modified) — одиночный хвост признаётся законченной пометкой, соседние хвосты одного изменения сжимаются в пару. [`.cursor/docs/antipatterns/bsl-antipatterns.md`](../../../../.cursor/docs/antipatterns/bsl-antipatterns.md):2795-2795
- **S3.5** · обзор слоёв и заготовка оформления (modified) — отсылка к тому же критерию одной строки. [`.cursor/docs/marker-layers-guide.md`](../../../../.cursor/docs/marker-layers-guide.md):58-58
- **S3.6** · сверка грамматики, оформления, сборки и проверки (modified) — расхождения закрыты в текстах правил. Требование не переписывалось.

Кода модулей в срезе нет.
