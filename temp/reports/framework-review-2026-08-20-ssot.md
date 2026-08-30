# Ревью SSOT: расползание норм kit

Проверены `AGENTS.md`, все 42 `.cursor/rules/*.mdc`, якоря в `.cursor/docs/`, шаблоны, frontmatter `.cursor/agents/*.md` и пять свежих спек. Ничего не менялось.

**Короткий диагноз:** карта SSOT в `AGENTS.md` в целом верная, но after нескольких доработок always-apply стабы перестали быть стабами, одни и те же числа живут в 3–6 файлах, а три документа одновременно называют себя источником истины для чата.

---

## Дубли норм

| Норма | SSOT по AGENTS.md | Где продублирована | Расходятся ли значения |
|---|---|---|---|
| Лимиты строк чата (таблица сценариев) | `chat-output-budget.mdc` (полное тело — `chat-output-budget-full.mdc`) | Полное тело §1; `opsx-output-style.md` §5.1/§5.2 (8–15, ≤6 слотов, 4–8 handoff, карта 5, pause-wait 7); шаблоны `brief-card.md`, `decision-block.md`, `openspec-*/templates/*`, скиллы explore/explain/apply/verify | **Да.** Развилка: стаб «≤8 (verify ≤12)»; полное тело в таблице «8», в примечании «≤12», в §2 «~12». Карта правок / AskQuestion на entry — только в полном теле. |
| HALT-жаргон (top-20) | `chat-output-budget.mdc` | `chat-output-budget-full.mdc` §7 (длиннее: `Ваш шаг (`, имена гейтов, `decision_round`…); `chat-lexicon.md` (ещё длиннее + `SUGGESTION`/`APPROVE`/`Blast Radius`); `gate-dispatcher.mdc` объявляет жаргон → lexicon | **Да, как списки.** Стаб — урезанный детектор; полное тело и lexicon шире. При этом стаб и lexicon оба претендуют на SSOT. |
| Тест понятности (3 части) | не назван отдельно; детали в полном теле §1c | `opsx-output-style.md` §2.6; `chat-lexicon.md` «Слой 0» — почти дословный повтор | Нет по смыслу; **три полных копии** механизма. |
| Pre-send self-check | бюджет чата §1b | Стаб: 10 пунктов; полное тело: 10 пунктов (развёрнутые); `opsx-output-style.md` §2.6: **другой** список из 8 пунктов | **Да (состав).** Общий дух один, чеклисты разные. |
| Канон лимита «дорогие модели недоступны — дальше на модели чата» | бюджет чата (фраза+триггер); `model-selection.mdc` (когда сказать) | Стаб §5 и §1b.9; полное тело §1/§5/§5a/§1b.9; `model-selection.mdc` строки 28 и 73 (фраза **снова**); `session-discipline.mdc` 27; FAQ; verify SKILL; `verdict-card`/`chat-summary` | Фраза одна. **«Не повторять строку»** есть только в `model-selection.mdc`, не в always-apply. |
| Таблица ролей `Task.model` | `model-selection.mdc` | Спека `subagent-model-mapping`; примеры слагов в `model-adaptation.mdc`; перечень ролей без слагов в `tool-name-guard.mdc`; **ошибочная** фраза в `AGENTS.md` | **Да vs AGENTS.md.** Таблица и 7× `model: inherit` согласованы. `AGENTS.md` называет Fable/GPT Primary. |
| Порядок «токен → память → таблица» | `model-selection.mdc` | `session-discipline.mdc` 27; `tool-name-guard.mdc` 24 | Нет (cue без таблицы). |
| writer↔reviewer = 2 | `1c-agent-delegation.mdc` § АВТО-ИСПРАВЛЕНИЕ | Таблица в том же файле § WRITER PIPELINE; `review/SKILL.md` (шаги 4.5 и 6); `1c-agent-patterns/SKILL.md` 289 | Число **2** совпадает. Patterns **без** carve-out weak / design-prescribed. Таблица ошибочно ссылается на writer Phase 7. |
| Investigation loop = 3 | таблица delegation → `review/SKILL.md` 3.5 | `1c-writer-pipeline.mdc` 270 («Лимит — 3»); `review/SKILL.md` `max_iterations = 3`; `1c-agent-patterns` | Число совпадает; **три места с числом**. |
| Self-review writer = 2 | таблица delegation → `onec-code-writer.md` | `onec-code-writer.md` Phase 7: «Max 2 iterations of self-review» | Совпадает. Но таблица путает это с циклом writer↔reviewer. |
| Repair Loop verify = 2 | не в карте AGENTS; живёт в verify | `verify-user-communication.mdc`; `openspec-verify-change/SKILL.md`; шаблоны `verdict-card` / `chat-summary` / `executive-summary` | Совпадает. Риск путаницы с «2 итерации» writer↔reviewer. |
| DELEGATION GATE: ≤3 чтения `.bsl`; обследование = 0 | `1c-agent-delegation.mdc` | `1c-agent-patterns/SKILL.md` 296–300 (только ≤3, **без порога 0**) | **Частично.** Patterns не копирует «обследование → 0». |
| Explorer при 3+ модулях | delegation, таблица делегирования | halt-triggers; `tool-name-guard`; `1c-agent-patterns` EXPLORE MODE | **Да.** Delegation: «Рекомендуется». Halt-triggers / patterns: звучит как MUST. |
| Light Mode: 1 файл, 2–10 строк | `1c-halt-triggers.mdc` | `task-triage.mdc`; `sdd-workflow.mdc`; `openspec-explore/SKILL.md`; `architect-gate.mdc` (исключение) | Порог совпадает. Promotion-список в triage **шире**, чем safety floor в halt-triggers. |
| Mechanical Mode чеклист | `1c-halt-triggers.mdc` | Кратко в `1c-agent-delegation.mdc` § BSL WRITE GUARD; `architect-gate` исключение | Нет. |
| XML: Form/Template/Rights | `1c-xml-write-guard.mdc` | Компакт-таблица в `1c-agent-delegation.mdc`; `forms-mxl-mode-gate.mdc`; apply SKILL; `1c-no-metadata-creation.mdc` | **Да.** `1c-no-metadata-creation.mdc:44` всё ещё `artifact_mode: assisted`. Компакт Template.xml не требует разрешения apply. |
| pause-wait: до 7 пунктов, вне 4–8 | бюджет чата; шаблон `pause-wait-chat.md` | Полное тело §1d; `opsx-output-style.md` §5.2; apply SKILL | Совпадает. |
| Карта правок: 5 пунктов вне 4–8 | полное тело §1c (apply) | Стаб **не содержит** числа 5; `opsx-output-style.md`; apply SKILL | Стаб молчит о «5» — риск потерять норму, если читать только always-apply. |
| Один вопрос выбора за ход | не в карте AGENTS (спека sequential-gate) | `openspec-new-change/SKILL.md`; `brief-card.md`; `forms-mxl-mode-gate.mdc:124`; verify SKILL | Совпадает в new. В extend — слабо. В §1b бюджета — нет. |
| Бюджет always-apply ≤ 34 КБ | спека `always-apply-context-budget`; `delivery-integrity.md` | — | **Да vs факт:** сейчас **37,2 КБ** (38 062 байт) при лимите 34 816. |
| FIRST AND ONLY Read SKILL.md | `session-discipline.mdc` → `command-skill-gate.mdc` | Почти дословно в обоих | Нет. |
| Context-strategy триггер 3+ / XML / 500+ | `session-discipline.mdc` → `context-strategy-gate.mdc` | Почти дословно | Нет. BYPASS одинаковый. |
| Free-text → explore SKILL | только `session-discipline.mdc` | нет в трёх on-demand гейтах | Не дубль; **уникально для стаба**. |

---

## Противоречия

**C1 — blocker.** Бюджет постоянного контекста нарушен.  
Файлы: `openspec/specs/always-apply-context-budget/spec.md` (лимит ≤34 КБ); факт замера always-apply + `AGENTS.md` = **38 062 байт (37,2 КБ)**. Состав: `1c-agent-delegation.mdc` 14,0 КБ, `chat-output-budget.mdc` 8,6 КБ, `AGENTS.md` 6,6 КБ, `session-discipline.mdc` 5,6 КБ, `gate-dispatcher.mdc` 3,2 КБ.  
Цитата спеки: «суммарный размер … SHALL не превышать 34 КБ».  
Следствие: каждая новая норма в стабе (канон, режим сессии, JSDoc carve-out) бьёт по тому же бюджету, который спека диеты как раз защищала.

**C2 — major.** Лимит развилки 8 vs 12 vs ~12.  
- Стаб `.cursor/rules/chat-output-budget.mdc:36`: «Компактная карточка ≤8 (verify decision ≤12)».  
- Полное тело `:37`: «в пределах 8 строк»; `:39`: «Развилка/decision в чате — ≤12 строк»; `:112`: «в пределах ~12 строк на решение».  
- `.cursor/docs/templates/decision-block.md:50`: «≤12 строк (`chat-output-budget.mdc` §1)».  
Агент, читающий только таблицу полного тела, урежет карточку до 8; читающий примечание или decision-block — до 12. Стаб пытается склеить оба числа в одной ячейке и тем самым закрепляет двусмысленность.

**C3 — major.** Три «SSOT для чата».  
- `AGENTS.md:22`: лимиты/HALT/принципы → `chat-output-budget.mdc`.  
- Стаб `:70–72`: «Лимиты / HALT / принципы → **этот stub**; детали → full».  
- Полное тело `:69`: «Лимиты строк в чате → **этот документ**, §1».  
- `opsx-output-style.md:86`: «**SSOT для чата.** Все skill-ы … обязаны следовать этому контракту».  
- `chat-lexicon.md:3`: «Единый источник для HALT-проверки».  
- `gate-dispatcher.mdc:44`: жаргон → lexicon.  
Невозможно сказать, какой файл править при изменении одной нормы.

**C4 — major.** `AGENTS.md` врёт про Primary субагентов.  
`AGENTS.md:5`: «Fable / GPT-5.6 / Opus 5 — **Primary** субагентов».  
`model-selection.mdc:81–91` и спека `subagent-model-mapping`: Primary архитектора — Opus 5; reviewer — Gemini; simplifier — Composer; Fable **не** Primary ни одной роли; GPT-5.6 в таблице ролей нет.  
Это прямо противоречит свежей спеке и таблице, которую карта SSOT сама же назначает источником.

**C5 — major.** `artifact_mode` vs `form_mode` в живом запрете метаданных.  
`.cursor/rules/1c-no-metadata-creation.mdc:44`: «только при `artifact_mode: assisted`».  
Актуальный SSOT: `forms-mxl-mode-gate.mdc` / `1c-xml-write-guard.mdc` — `form_mode` / map `forms:`, `artifact_mode` только как legacy fallback. Оркестратор по этому файлу может отказать в assisted-форме с корректным `form_mode`.

**C6 — major.** Explorer: «рекомендуется» vs обязательно.  
`1c-agent-delegation.mdc:83`: исследование 3+ модулей — «**Рекомендуется**».  
Тот же файл `:116`: обследование → порог **0** обращений, «Делегировать сразу».  
`1c-halt-triggers.mdc:48`: «Исследование 3+ модулей | **onec-code-explorer**».  
`1c-agent-patterns/SKILL.md` EXPLORE MODE: «Код 3+ модулей → explorer» без hedging.  
Спека `delegation-safeguards` запрещает самостоятельное обследование 1С. Слово «Рекомендуется» в always-apply таблице ослабляет MUST.

**C7 — major.** Таблица лимитов итераций ссылается не туда.  
`1c-agent-delegation.mdc:139`: цикл writer↔reviewer = 2, «этот файл § АВТО-ИСПРАВЛЕНИЕ РЕВЬЮ; **writer Phase 7**».  
`onec-code-writer.md:413–419` Phase 7 — это **внутренний self-review** («Max 2 iterations of self-review after initial write»), не цикл с reviewer. Writer↔reviewer живёт в `review/SKILL.md`. Сама «сводная» таблица, задуманная чтобы «не путать три цикла», путает два из них.

**C8 — major.** Авто-fix в patterns без carve-out apply-reviewer.  
`1c-agent-patterns/SKILL.md:289`: «Все кодовые замечания (critical, high, medium, low) → автоматически writer … Максимум 2 итерации».  
`1c-agent-delegation.mdc:102`: авто-fix только functional MUST_FIX **без** `QualityFlag=weak` / `design-prescribed` / agreement-override; в apply — не AskQuestion.  
Кто идёт по patterns в apply — починит weak сам, вопреки якорю D6.

**C9 — major.** Risk Surfacing в стабе ≠ в полном теле.  
Стаб `:18`: «после handoff/verify/explore **поднять 1–3 границы** на UX-языке».  
Полное тело `:76`: Risk Surfacing = «блокеры/развилки всегда в чат §2 Исключение 1».  
Протокола «1–3 границы» в полном теле нет. Либо стаб изобрёл обязанность, либо full её потерял.

**C10 — minor→major в runtime.** Компакт XML в delegation теряет разрешение макета.  
`1c-agent-delegation.mdc:68`: «Template.xml | `assisted`: `1c-mxl/compile`; иначе pause-wait / WAIT».  
`1c-xml-write-guard.mdc:24` / Mode Gate: default **manual**; non-manual только при записанном разрешении apply. Компакт читается как «видишь assisted — компилируй».

**C11 — minor.** Light Mode: указатель в architect-gate устарел.  
`architect-gate.mdc:139`: «Light Mode (см. **1c-agent-delegation.mdc**)».  
Детали Light — в `1c-halt-triggers.mdc`; в delegation только отсылка «Read halt-triggers».

**C12 — minor.** Promotion-триггеры: два списка.  
`1c-halt-triggers.mdc:22–28`: транзакции, контракт `Экспорт`, RLS, adopted, подписки/регламенты.  
`task-triage.mdc:23–33`: то же **плюс** wired metadata, Mode Gate форма/макет, неочевидный root cause, «новый или меняющийся экспортный API».  
Спека `rules-hygiene` фиксирует список в halt-triggers. Triage расширяет молча.

**C13 — minor.** HALT-списки разной полноты при претензии на SSOT.  
Стаб §7 без `Ваш шаг (`, без `decision_round` / `open_decision_id`. Полное тело их даёт. Lexicon даёт ещё `SUGGESTION`, `Blast Radius`, `diff не обязателен`. Если агент grepaет только always-apply top-20, часть запретов не сработает — это задумано как детектор, но стаб `:70` говорит «HALT → этот stub».

**C14 — minor.** Канон лимита всё ещё живёт в on-demand, хотя спека это запретила как *единственное* место — и всё равно продублировала текст.  
`session-api-mode`: «on-demand правило выбора моделей MUST NOT быть единственным местом текста канона» + «Дословная фраза … always-apply».  
`model-selection.mdc:28` и `:73` всё равно содержат ту же фразу целиком, хотя `:28` пишет «Дословная фраза и триггер — always-apply бюджет чата §5».

**C15 — minor.** `forms-mxl-mode-gate.mdc:15` в таблице режимов: «XML только **через skill**».  
Спека `chat-surface-clarity`: эталон для `assisted` не должен учить jargon «через skill». Чат-канон вопроса в том же файле уже чистый; таблица режимов и кейсбук `metadata-xml-workarounds.md` — нет.

---

## Стаб vs полное тело

### 1) `chat-output-budget.mdc` ↔ `chat-output-budget-full.mdc`

Стаб **перестал быть стабом**. ~50 строк runtime-контракта: полная таблица лимитов, HALT, §1b из 10 пунктов, канон, язык progress, non-events, subagent protocol. Это 8,6 КБ из 34 КБ бюджета.

**Только в стабе (нет в full или определено иначе):**
- «Тишина: нет решения и нет блокера → одна строка; не дублировать reports/; `Task` / writer-pipeline не отменяются».
- Risk Surfacing как «1–3 границы» (см. C9).
- Претензия «лимиты/HALT → этот stub» (full считает SSOT себя).
- Сжатая строка verify без разбора quiet 1a/1b / Repair Loop.

**Только в полном теле:**
- §1c Тест понятности (стаб ссылается «§1c full», но агент без Read full его не видит).
- §1d инвентарь pause-wait.
- Карта правок: 5 пунктов.
- Раздельные строки entry-брифа new vs extend; AskQuestion-исключения.
- Skip-on-empty §3; таблица non-events по командам.
- §5a протокол verify (имена агентов, запрет цитирования QC).
- Interrupted-by-user: обязательный вопрос «Прервали — продолжить…».
- Двухшаговая цепочка `failed` → `model-selection.mdc`.

**Противоречия пары:** C2 (8 vs 12), C3 (кто SSOT), C9 (Risk Surfacing), C13 (HALT).  
Иерархия «лимит > шаблон > пример» есть в обоих; исключение pause-wait/понятность — тоже. Это согласовано.

Профиль GPT явно carve-out’ит «стаб → полное тело», то есть авторы знают: стаб *недостаточен*. Тогда держать в стабе полную таблицу лимитов — против собственной модели «cue + Read».

### 2) `session-discipline.mdc` ↔ `command-skill-gate` + `command-session-persistence` + `context-strategy-gate`

Вход SKILL.md и context-strategy — честные сжатия, значения совпадают.

**Стаб содержит нормы, которых нет в «полных» телах:**
- **Free-text entry** → Read `openspec-explore/SKILL.md` (критичный маршрутизатор без команды).
- **Режим сессии** (токены `-noapi`/`-api`, память после лимита, канон) — в persistence **намеренно нет** (задача архива: «`command-session-persistence.mdc` не трогать»).
- Ultra-Lite explore: якорь «Вопрос» / `user-goal`.
- Ссылка на несуществующий принцип **Compact Brief** (есть ещё в `command-skill-gate.mdc:33`; в бюджете чата термина нет).

Persistence **богаче** стаба по anti-patterns (new Design Gate, handoff, follow-up `openspec status`). Стаб — не супермножество.

Итог: session-discipline — третий always-apply протокол, а не оглавление трёх гейтов.

### 3) `1c-agent-delegation.mdc` ↔ `1c-halt-triggers.mdc` + `1c-writer-pipeline.mdc`

Якорь потока `writer → ReadLints → … → reviewer` и отсылка «эталон в writer-pipeline» согласованы. Writer-pipeline честно говорит «сводная таблица лимитов — delegation».

**Стаб delegation раздут содержанием, которое должно быть on-demand:**
- JSDoc / шапка метода (carve-out) — продублирован смысл halt-triggers «не JSDoc шапки».
- Mechanical Mode: StrReplace + reviewer.
- APPLY GATE целиком (повтор первой строки halt-triggers).
- XML-таблица (см. C10).
- Якоря apply-reviewer и поверхности (это как раз требование спеки диеты — оставить дословно).
- Полная таблица трёх циклов итераций (и она же с ошибкой Phase 7 — C7).

Halt-triggers **не** содержит APPLY GATE prose и XML-таблицу — хорошо. Но Light/Mechanical/исключения в delegation всё равно пересказаны, не только «Read halt-triggers».

---

## Терминология

| Понятие | Основное имя | Варианты | Оценка |
|---|---|---|---|
| Пауза apply «нужен Конфигуратор» | **pause-wait** (шаблоны, бюджет, спека chat-surface) | пауза-ожидание; `WAIT`; `pause`; в apply ещё `pause-decision` | Имена **pause-wait** / **pause-decision** стабильны. **WAIT** живёт в XML-guard / Mode Gate / no-metadata как отдельный halt без отсылки к карточке. Агент может сделать WAIT без инвентаря в чате. |
| Light / Mechanical | Light Mode, Mechanical Mode | LIGHT MODE / MECHANICAL MODE (заголовки); quick-fix ≈ Light | Согласовано. architect-gate смотрит не в тот файл. |
| Канон | перегружен | (1) канон лимита; (2) канон «Модель архитектора: Opus 5»; (3) канон вопроса Mode Gate; (4) `marker-canon.md`; (5) «Каноны вопросов» в lexicon | Спека и ADR-0005/0007 различают (1) и (2). В бюджете чата слово «канон» без уточнения = (1). Путаница с Mode Gate реальна. |
| Липкий сбой | липкий сбой / липкая память | память после лимита; режим «без API» | В `model-selection.mdc` различение липких vs таймаут ясное. В стабе бюджета «липкий сбой» = три причины, без «не повторять». |
| Карточка вердикта verify | **verdict-card** (имя файла) | бинарный вердикт; карточка вердикта; в стабе жаргон `verdict-card` как имя шаблона | В чат шаблон не должен утекать; в правилах имя файла уместно. Стаб `:24` пишет «Вердикт verdict-card» — агент может скопировать англ. ярлык. |
| Compact Brief | — | ссылки в session-discipline и command-skill-gate | **Сирота.** В бюджете чата нет определения. Бывший `conversational-discipline.mdc`. |
| Режим формы | `form_mode` + русские ярлыки | `artifact_mode` (legacy); `assisted`/`manual`/`bsl-only` | Чат-канон и FAQ согласованы. Живой `1c-no-metadata-creation.mdc` на legacy-имени (C5). |
| Режим сессии | «с API» / «без API» | `-noapi` (токен человека, не сигнал) | Согласовано с FAQ и спекой. |

«Пошаговая пауза» везде в HALT как запрет — хорошо, совпадает со спекой chat-surface.

---

## Спеки vs правила

### `chat-model-profiles`

Покрытие в целом есть: строка в `AGENTS.md` → `model-adaptation.mdc` → четыре профиля; MAY/MUST NOT; precedence; carve-out GPT «стаб → полное тело»; язык `/opsx:*` и канон в роутере и в `model-grok4.mdc`.

Пробелы:
- `AGENTS.md` (C4) ломает пирамиду «чат Grok / Primary по таблице».
- Профили fable/gpt/opus **не** повторяют MUST NOT про английский progress и канон; это есть в роутере и только в grok4. Спека формулирует требование к «профилю», не только к роутеру.
- Сценарий «бриф субагента учитывает MAY opus5» нигде не превращён в обязательный пункт `1c-agent-patterns` (MAY, не дыра).

### `chat-surface-clarity`

Покрытие сильное: pause-wait шаблоны, decision-block «не через skill», FAQ/quick-start на `form_mode`, русский progress в бюджете, HALT «пошаговая пауза».

Пробелы:
- Таблица режимов Mode Gate и кейсбук всё ещё «через skill» (C15).
- Тест понятности скопирован в style-guide и lexicon вместо ссылки на §1c.
- `opsx-output-style.md` §2.6 объявляет себя SSOT чата — против спеки, которая требует *согласованности* docs, не третьего владельца.

### `sequential-gate-questions`

`/opsx:new` закрыт хорошо (Metadata Gate, END TURN, dual-selection HALT, kit-only `n/a`, apply и `n/a` в маркере). `brief-card.md` согласован.

Пробелы:
- Инвариант «один вопрос выбора» **не** в always-apply §1b (спека: self-check перед отправкой). Сейчас это локальный HALT скилла new.
- `/opsx:extend` не имеет dual-selection HALT (спека: «создание **или уточнение** ЗНИ»).
- Деловая постановка без `.bsl` → спросить: есть в new SKILL и brief-card; в always-apply нет (приемлемо, если new всегда читают).

### `session-api-mode`

Реализовано: токены, память vs таймаут, не путать с `--skip-architect`, подсказка в семи командах, FAQ, канон в always-apply §5, «Модель архитектора: Opus 5», не печатать `-noapi`.

Пробелы / трение:
- Текст канона всё ещё в `model-selection.mdc` (C14), вопреки разделению «фраза в бюджете / когда — в model-selection».
- «Не повторять строку» только on-demand: агент на одном always-apply может повторять канон каждый ход.
- Раздувание стаба каноном прямо ударило по 34 КБ (C1). Спека visibility и спека диеты **конфликтуют**, пока канон живёт в always-apply вместе с полной таблицей лимитов.

### `subagent-model-mapping`

Таблица ролей, inherit во всех 7 агентах, двухшаговая цепочка, Fable как закрытая эскалация, самосверка enum, запрет family guessing — согласованы с `model-selection.mdc` и `tool-name-guard.mdc`.

Пробел: только `AGENTS.md` (C4). Anti-example `composer-2` в tool-name-guard допустим спекой.

### Другие спеки kit (коротко)

| Спека | Статус |
|---|---|
| `always-apply-context-budget` | **Не выполняется** (C1). Якоря apply-reviewer/поверхности в delegation — выполнены. |
| `rules-hygiene` | Крупные on-demand без шапки «Когда загружать»: `knowledge-format.mdc`, `vertical-slices.mdc`, `model-selection.mdc`, `chat-output-budget-full.mdc`, `existing-mechanism-priority.mdc`, `adr-format.mdc`. Safety floor в halt-triggers есть. |
| `delegation-safeguards` | Запрет built-in explore — в delegation и tool-name-guard. «Две неудачи» — в delegation. Patterns авто-fix расходится (C8). |

---

## Рекомендации

**R1.** Вернуть always-apply ≤34 КБ. Файлы: `chat-output-budget.mdc`, `1c-agent-delegation.mdc`, `session-discipline.mdc`. Действие: в стабах оставить cue + 1–2 обязательные фразы (канон лимита, FIRST AND ONLY, порог 0 для обследования); таблицы лимитов, HALT, XML, JSDoc, APPLY GATE — только в full/halt-triggers/xml-guard. Иначе C1 не закрыть.

**R2.** Один владелец лимитов строк. Файл-SSOT: `chat-output-budget-full.mdc` §1. Стаб: «Read full при любом сообщении в чат / при сомнении» **без** своей таблицы. `AGENTS.md` и `opsx-output-style.md:86` переписать: style-guide — контракт авторов скиллов, не runtime-SSOT. Снять «лимиты → этот stub» из стаба `:70`.

**R3.** Зафиксировать одно число развилки. Предложение: **≤12** (как decision-block и примечание full), в таблице full заменить «8» на «≤12»; стаб не держать вторую цифру. Проверить `opsx-output-style.md` эталон ~25 строк информативного блокера — он уже согласован с 25–30.

**R4.** Исправить `AGENTS.md:5`: «чат оркестратора — Grok 4; модели субагентов — только таблица `model-selection.mdc` (архитектор Opus 5, ревьюер Gemini, упрощение Composer; Fable не Primary)».

**R5.** `1c-no-metadata-creation.mdc:44`: заменить `artifact_mode: assisted` на `form_mode: assisted` (или map `forms:`) + legacy-оговорка в одну фразу.

**R6.** В таблице делегирования сменить «Рекомендуется» на «Да» для обследования 3+ модулей / любого обследования кода; оставить «рекомендуется» нельзя при пороге 0. Файл: `1c-agent-delegation.mdc:83` + сверка halt-triggers.

**R7.** Строка таблицы итераций: writer↔reviewer → только § АВТО-ИСПРАВЛЕНИЕ + `review/SKILL.md` 4.5; Phase 7 writer — только self-review. Файл: `1c-agent-delegation.mdc:135–141`. В `1c-writer-pipeline.mdc:270` убрать число «3», оставить ссылку на таблицу.

**R8.** `1c-agent-patterns/SKILL.md` § АВТО-ИСПРАВЛЕНИЕ: заменить пересказ на ссылку «якорь в delegation; процедура в review/SKILL.md 4.5». То же для DELEGATION GATE: не копировать «≤3», добавить «обследование = 0».

**R9.** Либо определить Compact Brief одной фразой в бюджете чата, либо заменить ссылки в `session-discipline.mdc:19` и `command-skill-gate.mdc:33` на «лимиты `chat-output-budget.mdc`».

**R10.** Risk Surfacing: либо вписать «1–3 границы» в full §2, либо вычеркнуть из стаба и оставить только «блокеры/развилки всегда в чат».

**R11.** HALT: в стабе и `gate-dispatcher.mdc` явно «детектор top-20; SSOT словаря — `chat-lexicon.md`; механизм — §1c full». Убрать претензию стаба на владение HALT.

**R12.** `model-selection.mdc`: не цитировать канон в кавычках повторно; «когда сказать / не повторять / не печатать `-noapi`» без дословной фразы. Фраза — только бюджет §5 (требование спеки).

**R13.** Один вопрос за ход: пункт в §1b бюджета (ссылка на спеку) + HALT dual-selection в `openspec-extend-change/SKILL.md`.

**R14.** `architect-gate.mdc:139`: Light Mode → `1c-halt-triggers.mdc`. Promotion: triage ссылается на список halt-triggers и добавляет только свои пункты с пометкой «сверх safety floor».

**R15.** Словарь: в `chat-lexicon.md` или Mode Gate одна строка «WAIT (внутренний halt) = тот же случай, что pause-wait в чате apply». В XML-таблице delegation писать `pause-wait`, не `WAIT` в одиночку.

**R16.** Шапки «Когда загружать» в крупных on-demand: как минимум `model-selection.mdc`, `chat-output-budget-full.mdc`, `vertical-slices.mdc`, `knowledge-format.mdc` (спека `rules-hygiene`).

**R17.** После R1–R2 — повторный замер байт always-apply; критерий `delivery-integrity.md` сейчас красный.

Приоритет: **C1+R1** (бюджет), **C4+R4** (ложный Primary), **C2+R2+R3** (лимиты чата), **C5+R5** (битый `artifact_mode`), **C6–C8** (делегирование/итерации). Остальное — гигиена, без неё расползание повторится на следующей ЗНИ kit.