# Ревью: хардкод-списки и антипаттерны во фреймворке kit

Ось: не «мало правил», а **расползание перечислений**. Kit уже формулирует правильный механизм (тест читателя / allow-list по построению / «не добавлять слова в §7»), но **продолжает копировать блок-листы** в always-apply, скиллы, шаблоны и профили моделей. В результате один смысл живёт в 3–8 редакциях разного состава.

---

## Инвентарь списков

Колонка **размер** — число пунктов/токенов (оценка по текущему тексту, не байты). **SSOT объявлен?** — что файл сам про себя говорит. **Дубли** — где тот же смысл повторён.

| файл:строки | назначение | размер | SSOT объявлен? | дубли |
|---|---|---|---|---|
| `.cursor/rules/chat-output-budget.mdc:60-64` | HALT-жаргон «§7 top-20» (always-apply, greppable) | ~23 группы + 4 regex (`OQ`/`D`/`S`/`interim`) | Да: «Лимиты / HALT → этот stub»; полнота — «тест §1c, не длина списка» | full §7; lexicon Слой 1; verify SKILL:450; opsx §3.1b |
| `.cursor/rules/chat-output-budget.mdc:44-46` | Non-events (сжатый) | 5 примеров | Нет (отсылает к full) | full §3a таблица; apply SKILL; lexicon строка non-event |
| `.cursor/rules/chat-output-budget.mdc:48-50` | No Acknowledgement | 2–3 фразы | Нет | full §4; opsx §7 п.14; review SKILL |
| `.cursor/rules/chat-output-budget.mdc:52-54` | Состояния Task (`completed` / `interrupted-by-user` / `failed`) | 3 | Нет | full §5 |
| `.cursor/rules/chat-output-budget.mdc:56-58` | Англ. каркасы progress | 5 (`I'll`/`Let's`/`Starting`/`Switched to`/`chat model`) | Нет; «примеры, не HALT» | full §6; spec chat-surface-clarity:109; verify SKILL:369 |
| `.cursor/rules/chat-output-budget.mdc:66-68` | Pre-send self-check | 10 пунктов | Да как runtime | full §1b (развёрнутый); opsx §2.6 (8); opsx §7 (21); verify-user-communication (10) |
| `.cursor/rules/chat-output-budget.mdc:20-36` | Таблица лимитов строк | 13 сценариев | Да (stub) | full §1 (другая детализация; pause-wait вынесен в §1d) |
| `.cursor/rules/chat-output-budget-full.mdc:125-144` | Non-events по командам | ~25 примеров в таблице | Да: определение + таблица примеров | stub §3a; apply/new/verify skills |
| `.cursor/rules/chat-output-budget-full.mdc:179-189` | HALT top-20 + голые коды | top-20 + 7 кодов (`interim`, `default для apply`, `decision_round`, `open_decision_id`, …) | Да: «запреты → этот документ §7 + lexicon» — **конфликт со stub** | stub короче; lexicon длиннее |
| `.cursor/rules/chat-output-budget-full.mdc:173-177` | Progress RU + англ. примеры | те же 5 + принцип | Да для языка `/opsx:*` | spec + `I'll rerun` в verify |
| `.cursor/rules/chat-output-budget-full.mdc:49-56` | Запреты в «Карте правок» | ~8 токенов поверх §7 | Нет | apply SKILL:355 |
| `.cursor/rules/chat-output-budget-full.mdc:58-65` | Запреты pause-wait в чате | ~6 | Нет; чат-SSOT — `pause-wait-chat.md` | pause-wait-chat; ux-acceptance E4; spec |
| `.cursor/rules/chat-output-budget-full.mdc:165-169` | Запреты финала verify | 4 класса (цитаты агентов, имена, внутренние тесты, несколько вердиктов) | Нет | verify SKILL; verify-user-communication |
| `.cursor/docs/chat-lexicon.md:29-52` | Слой 1: бан кодов движка + таблица замен | **~80+ токенов** в одном абзаце + ~12 строк замен | **Да: «единый источник для HALT-проверки»** | stub/full §7 — подмножество; opsx §3.1 — другое подмножество |
| `.cursor/docs/chat-lexicon.md:61-71` | Слой 2: разрешённые workflow-слова + запрет «ложной безопасности apply» | 4 запрета (`apply сейчас`, `apply на свой риск`, `defer apply`, `workaround сейчас`) | Частично | architect.md HARD-список **шире** |
| `.cursor/docs/chat-lexicon.md:75-84` | Слой 3: англицизмы (мягко) | 4 пары | Да для заказчика | overlap со stop-slop и overview |
| `.cursor/docs/opsx-output-style.md:216-242` | §3.1 таблица «техтермин → человеческий язык» | ~25 строк | Да: «расширенная карта, при расхождении приоритет lexicon» | lexicon; §9 |
| `.cursor/docs/opsx-output-style.md:240-241` | Имена агентов и гейтов (явный перечень) | 7 агентов + 8 гейтов/проверок | Нет (якорь — lexicon) | stub: glob `onec-code-*`; full: 3 имени гейтов |
| `.cursor/docs/opsx-output-style.md:180` | Agent-only keys | 7 ключей | Нет | verify-user-communication:8 (другой набор); lexicon |
| `.cursor/docs/opsx-output-style.md:198` | Anti-patterns isolated chat | 8 | Нет; зеркало `ux-acceptance-isolated-chat.md` | ux-acceptance:43-55 **длиннее** |
| `.cursor/docs/opsx-output-style.md:316-320` | Запрещённые подписи брифа + HALT-строки | 4 + 4 | Нет; «см. brief-card» | brief-card **шире** (7 подписей) |
| `.cursor/docs/opsx-output-style.md:668-681` | §9 «Что НЕ цитируется в чате» | 8 категорий | Вспомогательная сводка | §3.1 + lexicon + budget |
| `.cursor/docs/opsx-output-style.md:624-650` | Self-check-5 (де-факто 21 пункт) | 21 | Для авторов скиллов | конкурирует с budget §1b |
| `.cursor/docs/templates/brief-card.md:26-32` | Запрещённые подписи + HALT-строки брифа | 7 подписей + внутреннее + 4 HALT-строки | **Да: SSOT формы брифа** | opsx §5.1; full таблица лимитов |
| `.cursor/docs/templates/decision-block.md:55-80` | Англ-метки + «запрещено в чате» (робот-стек, таблицы, Цена/Плюс) | ~6 запретов + 5 меток | Да: формат развилки | card-decision.md:78-85 **почти дословно** |
| `.cursor/skills/stop-slop/SKILL.md:31-40` | Core Rules AI-tells | 8 принципов | Да для слопа; «не дублирует §7 / lexicon §3» | ai-tells-ru.md; budget §1b.7 |
| `.cursor/skills/stop-slop/references/ai-tells-ru.md` | Каталог фраз до/после + grep | 8 секций, ~40 фраз + regex | Да: полный каталог | SKILL кратко; decision-block §7 ссылается сюда |
| `.cursor/rules/bsl-antipatterns.mdc:14-73` | Writer bulletin (AP без примеров) | **55 AP** | Да для writer-сжатия | каталог в том же файле; карточки docs |
| `.cursor/rules/bsl-antipatterns.mdc:100-158` | Каталог AP (таблица Severity/Kind/детект) | 55 строк | Да для reviewer severity | bulletin + docs/antipatterns |
| `.cursor/docs/antipatterns/bsl-antipatterns.md` | Полные карточки AP | **50 заголовков `## AP-`** (~3000 строк) | Да: «проектный реестр» | **нет карточек AP-034…038** |
| `.cursor/rules/1c-writer-pipeline.mdc:113` | orchestration-blocklist (опционально) | 9+ токенов | Явно «не основа», «отказались от blocklist» | writer.md:85; AP-031 карточка; bulletin AP-031 |
| `.cursor/rules/1c-writer-pipeline.mdc:115-124` vs `:175-184` | Allow-list AP-031 vs AP-054 | 5 классов; protocol-список | Baseline — `marker-canon.md` | marker-canon:152-162; **HTTPS есть не везде** |
| `.cursor/docs/marker-canon.md:124-134` | Baseline-запреты `domain_label` (AP-053) | 5 классов примеров | **Да: LIST kit** | AP-053 карточка |
| `.cursor/docs/marker-canon.md:152-162` | Allow-list AP-054 | 5 классов, ~14 аббревиатур | Да: baseline LIST | writer-pipeline; AP-054 |
| `.cursor/rules/1c-halt-triggers.mdc:30-49` | HALT CONDITIONS (действия, не жаргон) | 12 триггеров | Да при правке `.bsl` | 1c-agent-delegation:9-16 **сжат до 2 строк** |
| `.cursor/rules/1c-halt-triggers.mdc:20-28` | Promotion triggers Light→full | 5 | Да | task-triage:23-33 **+ wired metadata / Mode Gate / RCA** |
| `.cursor/rules/1c-agent-delegation.mdc:9-22` | HALT cue + explore/Task запреты | 2+2 | Cue; тело — halt-triggers | tool-name-guard NEGATIVE |
| `.cursor/rules/1c-agent-delegation.mdc:65-70` | XML WRITE GUARD (типы файлов) | 4 | Cue | 1c-xml-write-guard (полное тело) |
| `.cursor/rules/1c-agent-delegation.mdc:76-88` | Таблица делегирования ролей | ~8 | Да для «кого звать» | tool-name-guard enum |
| `.cursor/rules/gate-dispatcher.mdc:13-29` | Карта on-demand гейтов | 13 | Да: индекс, не блок-лист | — |
| `.cursor/rules/tool-name-guard.mdc:29-57` | Допустимые `subagent_type` + NEGATIVE | 7 1С + 4 generic | Да для Task | delegation; model-selection |
| `.cursor/rules/model-selection.mdc:150-185` | Запреты `Task.model` + ANTI-PATTERNS | 4 + 10 | **Да: SSOT моделей** | tool-name-guard частично |
| `.cursor/rules/model-adaptation.mdc:44` + `model-{grok4,fable5,gpt56,opus5}.mdc` MUST NOT | Что профиль не снимает | **4 почти идентичных списка по ~8 пунктов** | Роутер: MUST NOT выигрывает | 4 профиля копируют тело |
| `.cursor/rules/verify-user-communication.mdc:66-77` | Pre-send verify + Agent-keys HALT | 10 + **10 ключей** | Нет; HALT §7 — budget | opsx:180 (7 ключей); lexicon |
| `.cursor/rules/session-discipline.mdc:47-53` | Anti-patterns команд | 3 строки | Нет | протокол explore/apply, не словарь |
| `.cursor/rules/verified-cause-gate.mdc:59-61` | Анти-паттерны заплаток | отсылка + 4 примера | Нет; карточки — AP | AP-016 |
| `.cursor/rules/architect-gate.mdc:13-50` | Триггеры Architect Gate | ~25 | Да для «нужен архитектор» | verify SKILL Layer 4 grep-фразы |
| `.cursor/agents/onec-code-architect.md:133-134` | Запрещённые формулировки развилок | **9 подстрок** | Нет | lexicon Слой 2: **4** |
| `.cursor/skills/openspec-verify-change/SKILL.md:450` | «Запрещено в чат» (урезанный HALT) | 9 токенов вкл. `SUGGESTION` | Нет; «полный список — budget §7» | **SUGGESTION нет в stub §7** |
| `.cursor/skills/openspec-verify-change/templates/chat-summary.md:68,118` | Запреты чата verify | ~8 | Нет | verify-user-communication; ux-acceptance |
| `.cursor/skills/openspec-apply-change/SKILL.md:256,445` | Meta-статус pipeline / non-events apply | 4 фразы | Нет; §3a budget | lexicon; ux-acceptance |
| `.cursor/skills/openspec-apply-change/templates/pause-wait-chat.md:15-21` | Запрещено в pause-wait | 5 | **Да: SSOT карточки** | full §1d; spec; ux E4 |
| `.cursor/docs/ux-acceptance-isolated-chat.md:43-55` | Anti-patterns (fail) регрессии UX | 12 | Для gate перед merge | opsx §2.6 короче |
| `.cursor/skills/openspec-overview/templates/style-checklist.md:12-92` | Англицизмы + маркеры механизма + anti-tutor | ~15 англ. + 8 HALT-механизмов + 8 форм | Да для overview/заказчика | **не связан с lexicon Слой 1** |
| `.cursor/skills/openspec-explain/templates/entry-brief.md:24-34` | HALT слотов explain | 7 | Да для B-explain | brief-card + full таблица |
| `.cursor/skills/openspec-explore/profiles/bug.md:59-71` | HALT слота «Дальше» | 3 запрета / 3 разрешено | Да для bug-профиля | opsx Symptom Lock |
| `.cursor/rules/forms-mxl-mode-gate.mdc` | Enum `form_mode` + ярлыки чата | 3 режима | Да | lexicon замены manual/assisted |
| `openspec/specs/chat-surface-clarity/spec.md:107-119` | Норма языка + англ. каркасы | 6 примеров (+ `next-best model`) | Поведенческая спека | budget §6 **без** `next-best model` |
| `AGENTS.md:18-48` | Карта SSOT | индекс | Навигация | указывает lexicon + stop-slop + halt-triggers + bsl-antipatterns |

Не блок-листы (оставлять как enum/диспетчер): `form_mode`, `Task.model` / `subagent_type`, состояния Task, таблица гейтов, таблица делегирования, бинарные вердикты verify («можно apply» / «нужен выбор»).

---

## Дрейф и противоречия

### F1 — major. Три «SSOT» на один HALT-список, составы разные

Always-apply stub пишет: «Лимиты / HALT / принципы → **этот stub**». Full пишет: запреты → **этот документ §7 и lexicon**. Lexicon пишет: «**Единый источник** для HALT-проверки». Gate-dispatcher и AGENTS.md указывают на lexicon. Оркестратор на каждом ходе видит stub и **не обязан** читать full/lexicon.

Доказательства состава:

Stub (§7) **не содержит**: `SUGGESTION`, `Ваш шаг (`, `diff не обязателен`, именованные гейты, `default для apply`, `decision_round`, `open_decision_id`, `APPROVE`/`REJECT`, agent-keys.

Full добавляет: `Ваш шаг (`, три имени гейтов (`Architect Gate`, `Code-Truth Gate`, `Slice Gate`), коды `default для apply` / `decision_round` / `open_decision_id`.

Lexicon добавляет ещё десятки: `SUGGESTION`, `Severity`, `SKIPPED-*`, `Three-Question Challenge`, `Blast Radius`, `mount_context`, `Precedent Regression Gate`, `diff не обязателен`, …

Verify SKILL при этом говорит «полный список — budget §7», но сам банит `SUGGESTION`, которого в stub §7 нет.

```62:64:.cursor/rules/chat-output-budget.mdc
Вне backticks запрещены: `CRITICAL`, `WARNING`, `GO`/`NO-GO`, `PASS`/`FAIL`, `GAP`, `CHALLENGE`, `Layer 1`…`Layer 5`, `verify_mode`, `verdict:`, `snapshot`, `phantom-symbol`, `design-challenge`, `task-readiness`, `quality-controller`, `code-truth`, имена `onec-code-*` / `openspec-*`, имена гейтов, `пошаговая пауза`, `автопроверки пройдены` / `reviewer PASS` / `линтер чист`, `apply на свой риск` / `defer apply`.
```

```450:450:.cursor/skills/openspec-verify-change/SKILL.md
Запрещено в чат: «PASS / FAIL / verdict: GO / Layer N / design-challenge / task-readiness / phantom-symbol / CRITICAL / WARNING / SUGGESTION». Эти технические коды — только в YAML отчёта и в строке `Источники: …` файла. Полный список запрещённых подстрок — `.cursor/rules/chat-output-budget.mdc` §7.
```

### F2 — major. «Top-20» — ложное имя; механизм объявлен, практика — наращивать списки

В stub/full заголовок «top-20», пунктов уже больше 20. Lexicon Слой 0 и full §7 прямо запрещают лечить понятность удлинением списка — и в том же ходе ADR-0006 снова обсуждает «не класть английские глаголы в HALT», потому что соблазн добавить слово остаётся основным способом «закрыть дыру».

```189:189:.cursor/rules/chat-output-budget-full.mdc
> **Список §7 — быстрый детектор примеров, не механизм.** … Не добавлять новые подстроки в §7 как основной способ борьбы — применять §1c.
```

```23:24:openspec/adrs/ADR-0006-opsx-progress-russian.md
| Расширить HALT top-20 английскими глаголами | Постановка запрещает как основную защиту |
```

### F3 — major. Имена гейтов и агентов: glob vs перечень vs «имена гейтов»

| Место | Агенты | Гейты |
|---|---|---|
| stub | glob `onec-code-*` / `openspec-*` | «имена гейтов» (без списка) |
| full | тот же glob | 3: Architect, Code-Truth, Slice |
| lexicon | glob | 4: + Precedent Regression |
| opsx §3.1 | **7 явных slugs** | **8** (+ Implementation Impact, Symptom Relevance, Cross-Archive, KB Discovery) |

Новый гейт или агент гарантированно попадёт не во все четыре места.

### F4 — major. Английские progress-фразы: «не HALT», но уже 3 разных набора примеров

| Источник | Состав |
|---|---|
| stub + full §6 | `I'll` / `Let's` / `Starting` / `Switched to` / `chat model` |
| spec `chat-surface-clarity` | то же + **`next-best model`**; сценарий: «I'll start» / «Switched to chat model» |
| verify SKILL | **`I'll rerun`** (этого нет ни в budget, ни в spec) |

Защита объявлена принципом («русский + не новые пункты HALT»), но поддерживается как мини-блок-лист, который уже разъехался.

### F5 — major. Каталог BSL-антипаттернов — тройная копия, карточки отстали от индекса

- Writer bulletin: 55 AP (строки 19–73).
- Таблица каталога в том же `.mdc`: 55 строк.
- «Полные карточки» `.cursor/docs/antipatterns/bsl-antipatterns.md`: **50** заголовков `## AP-`.
- **AP-034, AP-035, AP-036, AP-037, AP-038** есть в индексе/bulletin и **отсутствуют в файле карточек** (после AP-033 сразу AP-039). Поиск `AP-034` в карточках — 0 совпадений.

Файл карточек объявлен полным реестром; reviewer, который Read карточки, не увидит пять AP, которые writer bulletin уже запрещает.

Порядок в bulletin: AP-051, **AP-053, AP-052**, AP-054 — инверсия относительно номеров; в карточках тоже каша (AP-052 перед AP-051).

### F6 — major. «Отказались от blocklist» — и тут же держат orchestration-blocklist в трёх местах

`1c-writer-pipeline.mdc` явно: конечный список запретов пропускает новое слово (`PreMatrix`); основа — детектор латиницы + allow-list. Сразу ниже — «необязательное усиление» со списком `Fallback`, `PostWrite`, `PreWrite`, `Guard`, … Тот же список в `onec-code-writer.md` (NEVER) и в карточке AP-031. Это ровно тот класс, от которого документ отрёкся.

```81:83:.cursor/rules/1c-writer-pipeline.mdc
**Принцип — детектор латиницы в идентификаторе, НЕ словарь стоп-слов.** … Любое будущее английское слово (`PreMatrix`, `PostMatrix`, …) закрывается автоматически, без правки списка.
> **Зачем отказались от blocklist.** Конечный список запрещённых токенов (`PreWrite`, `Guard`, …) пропускает всё, чего в нём нет — `PreMatrix` так и проскочил.
```

```113:113:.cursor/rules/1c-writer-pipeline.mdc
3. **Необязательное усиление (опционально):** если имя содержит токен из orchestration-blocklist (`Fallback`, `PostWrite`, `PreWrite`, `Guard`, `Mechanics`/`Механика`, `Gate`/`Гейт`, `Temp`/`Tmp`, `Wrapper`, `Orchestrat`)
```

### F7 — major. Четыре конкурирующих pre-send чеклиста

| Чеклист | Пунктов | Когда |
|---|---|---|
| budget stub/full §1b | 10 | каждое сообщение |
| opsx §2.6 | 8 | финал `/opsx:*` |
| opsx §7 «self-check-5» | **21** (имя лжёт) | бриф/отчёт/handoff |
| verify-user-communication | 10 (другие) | только verify |

Пункт «HALT» в каждом свой: §1b → stub top-20; verify → §7 **плюс** отдельный Agent-keys; opsx → §3.1 + §7. Агент не может «пройти один список».

### F8 — major. «Ложный apply» — два состава

Lexicon Слой 2: `apply сейчас`, `apply на свой риск`, `defer apply`, `workaround сейчас`.

Architect HARD:

```133:134:.cursor/agents/onec-code-architect.md
- Если описание «варианта» содержит подстроки `apply сейчас`, `apply now`, `apply на свой риск`, `apply на глаз`, `отложить apply`, `defer apply`, `принять архитектурный долг`, `workaround сейчас`, `пройти гейт и доделать` — это **не альтернатива**.
```

Чат-оркестратор по lexicon пропустит `apply now` / `apply на глаз` / `пройти гейт и доделать`. Архитектор по своему списку — нет. Это не «два слоя», а дрейф одного запрета.

### F9 — minor. Agent-keys: три подмножества

- opsx §2.6: `closed_decisions`, `decision_id`, `decision_round`, `verify_depth`, `reopen-blocked`, `supersedes`, `CHALLENGE-saturated`
- verify-user-communication: то же + `D0`–`Dn`, `GO-with-assumptions`, `SKIPPED-lite`; **нет** `open_decision_id`
- lexicon Слой 1: шире (`SKIPPED-novelty`, `mount_context`, `open_decision_id`, …)
- full §7 голые коды: `decision_round`, `open_decision_id` — **нет** большинства agent-keys

Always-apply не ловит `GO-with-assumptions`; verify-правило не ловит `open_decision_id`, который full уже объявил HALT.

### F10 — minor. Non-events смешаны с HALT-жаргоном

`автопроверки пройдены` / `reviewer PASS` / `линтер чист` стоят в §7 (бан подстроки) **и** в §3a (не выводить, потому что не событие) **и** в apply SKILL **и** в lexicon **и** в ux-acceptance. `diff не обязателен` — в lexicon/apply/ux, **не** в stub §7. Класс один, дома разные.

### F11 — minor. Подписи брифа: brief-card шире, чем зеркало в opsx

brief-card: `Что понял`, `Моё понимание`, `Как я понял`, `Что сделаю`, `Что получите`, `Как буду искать`, `Бриф для исследования`.

opsx §5.1 копирует только 4 из 7. Full таблица лимитов — ещё короче (`Что понял`, `Бриф для исследования`).

### F12 — minor. MUST NOT профилей: четыре копии одного абзаца

`model-grok4/fable5/gpt56/opus5.mdc` секция MUST NOT — почти дословно одна. Grok4 дополнительно держит язык `/opsx:*` и канон лимита; остальные — нет (это вынесено в роутер, но не во все профили). Правка «что профиль не снимает» = 4 diff.

### F13 — minor. Allow-list протокола: `HTTPS` то есть, то нет

- `marker-canon.md` и COMMENT HYGIENE: `HTTP`, **`HTTPS`**, `JSON`, …
- IDENTIFIER HYGIENE (тот же pipeline, шаг 4): `HTTP`, `JSON`, … — **без HTTPS**

Имя `HTTPS` в идентификаторе формально кандидат AP-031, в комментарии — allow-list. Файл сам ссылается на marker-canon как baseline.

### F14 — minor. Promotion-триггеры Light→full разъехались

`1c-halt-triggers.mdc`: транзакции, экспортный контракт, RLS, заимствования, подписки/регламент.

`task-triage.mdc` плюс: wired metadata, Mode Gate форма/макет, неочевидный root cause.

Cue в halt-triggers говорит «запрет ок → meta/form-add» через triage, но сами promotion-списки не совпадают.

### F15 — minor. Decision «запрещено в чате» скопировано в card-decision

`decision-block.md:73-80` и `card-decision.md:78-85` — один список (робот-стек, таблицы, Цена/Плюс, третий вариант-документирование, псевдокод, подзаголовки файла). Правка одного не чинит другое.

### F16 — minor. Isolated-chat anti-patterns: opsx короче регрессионного чеклиста

opsx §2.6: 8 fail. `ux-acceptance-isolated-chat.md`: 12, включая `пошаговая пауза` / `Ваш шаг (` и meta pipeline. Регрессионный gate строже, чем «SSOT контракта».

### F17 — minor. Overview — третий словарь запретов для другой аудитории, без якоря

`style-checklist.md` банит `runtime`, `UX`, `kill-switch`, `хардкод`, `Behavior Contract`, коды `S1`/`D7`/`Layer`. Это разумный жанр (ФА/заказчик), но OpenSpec-коды дублируют lexicon Слой 1, а `UX`/`UI` **противоречат** lexicon Слой 3 («в workflow-чате UI допустим»). Нет ссылки «для чата разработчику — lexicon; здесь — overview».

### F18 — minor. Lexicon `Last updated: 2026-08-02` при живом контенте 2026-08-20

В Слое 1 уже pause-wait, Mode Gate, `diff не обязателен`. Дата обмана: ревьюер думает, что словарь не трогали с начала августа.

### F19 — minor. HALT-триггеры 1С: cue 2 строки vs 12 строк тела

Это **не** дрейф состава запрещённых слов, а риск «оркестратор решит по cue». Cue слишком сжат (`apply gate / explore без change / metadata / трасса`); полный ряд `-FromObject`, Task explore, Light/Mechanical живёт только в on-demand файле. Для оси «списки» это приемлемый stub, если не начать копировать 12 строк обратно в always-apply.

### F20 — minor. Stop-slop vs No Acknowledgement vs «вводные»

Budget §4: `Понял` / `Сейчас сделаю`. Stop-slop: `Конечно!` / `Давайте разберёмся`. Full §1b.7 копирует 2 примера из stop-slop. Три списка вводных с пересечением, без единого grep. `ai-tells-ru.md` grep **не** включает `Понял`/`Сейчас сделаю`.

---

## Оценка поддерживаемости

**Не масштабируются (слово за словом):**

1. HALT-жаргон в stub/full/lexicon/скиллах — любой новый внутренний термин (гейт, agent-key, метка verify) требует N правок. Kit это уже понял (§1c) и **не остановился**.
2. Английские каркасы progress — бесконечный хвост (`I'll rerun`, `next-best`, `Working on`, `Hang tight`…).
3. AI-tells фразы в таблицах «Плохо/Замена» — полезны как примеры, вредны как закрытый бан.
4. Orchestration-blocklist идентификаторов — опровергнут собственным текстом (`PreMatrix`).
5. Overview-англицизмы и «маркеры механизма» (`автомат`, `ядро`, `триггер`) — бесконечны; уже есть тест «сказать вслух аналитику».
6. Запрещённые подписи брифа — конечны сегодня, но opsx уже отстал от brief-card.

**Заменить принципом / тестом (не enum):**

| Тема | Принцип уже есть | Список оставить как? |
|---|---|---|
| Понятность развилки/pause-wait | §1c reader test + allow-list токенов | 0–12 **примеров** в одном файле |
| Язык `/opsx:*` | «русский; Communication не сильнее» (ADR-0006) | 0 английских глаголов в HALT |
| Non-events | 3 вопроса: получил / нужно / куда | 1 таблица примеров только в full |
| Слоп | 8 Core Rules stop-slop | каталог on-demand, не always-apply |
| Export Language (AP-031/054) | детектор латиницы + allow-list по построению | calibration-примеры в **одной** карточке |
| Ложный apply | «вариант = разница в коде/поведении, не обход гейта» | 2–3 примера, не 9 подстрок |
| Имена агентов/гейтов | glob + «в чат только роли» | не перечислять slugs в opsx |

**Реально нужны как закрытый enum / каталог с ID:**

- `form_mode` ∈ {manual, assisted, bsl-only}
- `Task.subagent_type` и таблица Primary `Task.model` (сверка с enum инструмента)
- Состояния Task: completed / interrupted / failed
- HALT **действий** (не писать BSL самому, не создавать метаданные) — таблица триггер→действие
- Каталог AP-NNN как **продукт ревью** (карточка = принцип + детект + BAD/GOOD), не как блок-лист чата
- Allow-list AP-054 baseline (протоколы) — короткий закрытый LIST, overlay в project.md
- Бинарные формулировки вердикта verify (3 строки карточки)

**Особый случай AP:** каталог **должен** расти (новые дефекты 1С), но рост = **одна карточка + одна строка индекса**, не bulletin+таблица+карточка+writer NEVER+pipeline blocklist. Сейчас рост умножается на 4–5 поверхностей.

---

## Рекомендации по консолидации

### R1. Один HALT-детектор: lexicon Слой 1; stub — только отсылка + тест

**Файлы:** `chat-output-budget.mdc`, `chat-output-budget-full.mdc`, `chat-lexicon.md`, `AGENTS.md` (уже почти так).

**Сделать:** в stub §7 заменить перечисление на 3 строки: (1) вне backticks не цитировать коды/имена движка; (2) greppable детектор — Read lexicon Слой 1 при сомнении / при правке шаблонов; (3) полнота — §1c. Убрать претензию stub «HALT SSOT = этот файл». Full §7 оставить **либо** 8–10 самых частых токенов как cheat-sheet, **либо** удалить top-20 и оставить цитату «список в lexicon». Дата lexicon — обновлять при каждом изменении Слоя 1.

### R2. Заморозить §7: запретить новые подстроки процессом, не советом

**Файлы:** `chat-output-budget-full.mdc:189`, `opsx-output-style.md:158` (уже «не раздувать»), новый пункт в `openspec/adrs/README.md` или расширение ADR-0006.

**Сделать:** правило для авторов kit: новый жаргон → строка в lexicon **или** тест §1c; **запрещено** добавлять токен одновременно в stub, skill и ux-acceptance. Verify SKILL:450 удалить свой мини-список, оставить «lexicon + §1c».

### R3. Progress: принцип, выкинуть расходящиеся примеры из runtime

**Файлы:** stub §6, full §6, `openspec/specs/chat-surface-clarity/spec.md:107-119`, `openspec-verify-change/SKILL.md:369`.

**Сделать:** одна нормативная фраза: «в `/opsx:*` вводная речь и progress — русский; английский каркас предложения — провал; не пополнять HALT». Примеры (`I'll`, `Let's`, …) — **только** в spec/ADR как иллюстрация теста, не в always-apply. Удалить `I'll rerun` из verify SKILL (покрывается принципом). Не тащить `next-best model` в stub.

### R4. Non-events: определение в stub, примеры только в full

**Файлы:** stub §3a; full §3a; `openspec-apply-change/SKILL.md:256,445`; lexicon строка замен.

**Сделать:** stub оставить 3 вопроса self-check. Таблицу примеров — единственную в full. В apply SKILL заменить перечень фраз на «non-events §3a». Убрать `автопроверки пройдены` из HALT §7 (это non-event, не жаргон движка) — **или** оставить в lexicon Слой 1 как пример non-event, не как отдельный HALT-класс.

### R5. Слоп: принципы always-apply, каталог — on-demand

**Файлы:** stub §1b.7 (уже ссылается на skill); `stop-slop/SKILL.md`; `ai-tells-ru.md`.

**Сделать:** не копировать «Конечно! / Давайте…» в budget. Объединить No Acknowledgement (`Понял`) в grep `ai-tells-ru.md`. SKILL остаётся SSOT правил; references — примеры. Не тащить §7 жаргона в stop-slop (уже разведены — сохранить).

### R6. Один pre-send: budget §1b

**Файлы:** `opsx-output-style.md` §2.6 и §7; `verify-user-communication.mdc`.

**Сделать:** §2.6 self-check → «плюс пункты 1–10 budget §1b; ниже только verify-специфика (isolated chat, GO next step)». §7 «self-check-5» превратить в чеклист **автора скилла/шаблона** (явно: не runtime оркестратора) или сократить до «прогнать §1b + §3.1 для файла отчёта». Verify: пункт «HALT §7» заменить на «lexicon Слой 1»; Agent-keys — ссылка на lexicon, не третий список.

### R7. MUST NOT профилей — только в роутере

**Файлы:** `model-adaptation.mdc`; четыре `model-*.mdc`.

**Сделать:** в профилях секция MUST NOT = одна строка «не ослабляет список в `model-adaptation.mdc` § Precedence». Язык `/opsx:*` и канон лимита — в роутере (уже есть), не копировать в grok4 отдельно как уникальный MUST NOT, если это общее.

### R8. BSL AP: индекс + карточки; bulletin без детекта

**Файлы:** `bsl-antipatterns.mdc`; `docs/antipatterns/bsl-antipatterns.md`; `onec-code-writer.md`; `1c-writer-pipeline.mdc`.

**Сделать:**
1. Дописать карточки **AP-034…038** или вычеркнуть их из индекса — сейчас индекс врёт.
2. Writer bulletin: только `AP-NNN — одно предложение запрета`, без jargon-скобок и allow-list.
3. Таблица каталога в `.mdc` — единственный машинный индекс (Severity/Kind); карточки — единственное тело.
4. Orchestration-blocklist: удалить из pipeline/writer **или** явно пометить «калибровка ревьювера, не детектор»; не дублировать в NEVER writer.
5. Починить порядок AP-052/053.

### R9. Allow-list латиницы — один LIST

**Файлы:** `marker-canon.md` (оставить SSOT); `1c-writer-pipeline.mdc` шаги 4; карточки AP-031/054.

**Сделать:** pipeline не перечислять аббревиатуры, а «классы как в marker-canon». Добавить HTTPS в identifier-таблицу **или** убрать из comment-таблицы — выровнять. Префиксы `pav_`/`lvv_`/`пр_` — overlay project.md, не kit-хардкод в трёх файлах (kit может держать «префикс расширения из project»).

### R10. «Ложный apply» — принцип в lexicon Слой 2, architect ссылается

**Файлы:** `chat-lexicon.md` Слой 2; `onec-code-architect.md:133-134`.

**Сделать:** в lexicon принцип + 3 примера. В architect: «см. lexicon Слой 2; вариант без разницы в поведении → Gaps». Удалить 9-подстрочный HARD.

### R11. Бриф / decision / pause-wait: один файл запретов на шаблон

**Файлы:** `brief-card.md` (подписи); `decision-block.md` (робот-стек); `pause-wait-chat.md`.

**Сделать:** из opsx §5.1 убрать повтор подписей («см. brief-card»). Из `card-decision.md` убрать блок «Запрещено» → ссылка на decision-block. Apply SKILL не копировать pause-wait запреты. ux-acceptance ссылается на эти три файла, не растит свой 12-й список — **или** ux остаётся регрессионным зеркалом и генерируется из них (в markdown — хотя бы явная таблица «источник → ID сценария» без новых фраз).

### R12. Имена агентов/гейтов в opsx §3.1 — glob, не перечень

**Файлы:** `opsx-output-style.md:240-241`.

**Сделать:** как в stub: `onec-code-*` / `openspec-*`; гейты — «любое `* Gate` / имя проверки из rules». Перечень из 7+8 удалить (он гарантированно протухнет).

### R13. Overview оставить отдельным жанром, отрезать от lexicon чата

**Файлы:** `openspec-overview/templates/style-checklist.md`; `chat-lexicon.md` (уже упоминает overview).

**Сделать:** в чеклисте шапка: «это не HALT чата разработчику; UI в `/opsx:*` допустим». Коды `S1`/`Layer` не копировать — «см. lexicon Слой 1». Растить только маркеры **механизма** (`автомат`, `ядро`) — они уникальны для ФА.

### R14. Что не трогать (не списки-антипаттерны)

Не сливать и не «принципизировать»:

- `1c-halt-triggers.mdc` таблица действий (это диспетчер безопасности);
- `tool-name-guard` + `model-selection` enum;
- `forms-mxl-mode-gate` режимы;
- session-discipline таблица 3 анти-паттерна команд (протокол, не словарь);
- каталог AP как таковой — чинить структуру (R8), не заменять «общим принципом пиши хорошо».

---

**Итог владельцу:** жалоба точная. Расползание не в HALT-триггерах 1С и не в AP-ID как продукте, а в **копиях блок-листов чата** (жаргон, non-events, англ. progress, AI-tells, agent-keys, подписи брифа) и в **четвёртой копии AP** (bulletin / таблица / карточки / writer NEVER). Kit уже написал лекарство (тест понятности, отказ от blocklist, ADR-0006) — его нужно сделать **единственным** путём добавления нормы, иначе следующий change снова допишет слово в три файла из четырёх.