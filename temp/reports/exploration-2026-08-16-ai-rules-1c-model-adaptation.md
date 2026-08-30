# Исследование ai_rules_1c: адаптация моделей и смежные механики

**Дата:** 2026-08-16
**Источник:** `C:\GitHub\ai_rules_1c\` (референс-репозиторий, только чтение)
**Цель:** конспект механик свежего обновления ai_rules_1c с оценкой применимости к нашему Cursor-kit (субагенты через Task(model=slug), frontmatter агентов, `.cursor/rules/*.mdc` с alwaysApply/globs, скиллы `.cursor/skills/`).

**Легенда вердиктов:** ✅ прямой перенос · 🔧 адаптация · ❌ не применимо.

---

## 1. Роутер профилей моделей — `content/rules/model-adaptation.md`

### 1.1 Суть

Базовый свод правил написан **модель-нейтрально**: «it states what must be verified, which tools are mandatory, and what the delivery report must contain — none of which depends on which LLM is executing it». Поверх него лежит тонкий слой — **model profile**:

> «A **model profile** is a thin delta that tunes those documented behaviours to the running model. It exists so the same ruleset produces the same outcome on Claude Opus 5, Claude Sonnet 5, Claude Fable 5 and GPT-5.6 without the base rules being rewritten for a particular vendor's quirks.» (§1)

Источники дельт — только вендорская документация (Anthropic prompting best-practices per-model, OpenAI latest-model guide). Правило фильтрации: **«Only the model-specific parts of those guides are allowed into profiles; everything a guide states for all models belongs to §5 below and is always in force.»**

**Выбор профиля (§2):** ключ `AGENT_MODEL` в `.dev.env` → слаг (`opus5` | `sonnet5` | `fable5` | `gpt56`) → файл `content/rules/model-<slug>.md`. Пустое / неизвестное значение = «no model layer», базовый свод полный сам по себе:

> «missing file, missing key, empty or unrecognised value means "no model layer". Never ask for it at task time, never guess it, never treat its absence as a defect — the base ruleset is complete without it.»

Ключевые правила выбора:

- **Load once per session** — профиль ≈1–2k токенов, грузится один раз до первой нетривиальной задачи; не перечитывать per task, не грузить больше одного.
- **Self-knowledge wins over a stale value:** «`AGENT_MODEL` is a project setting and may have been written for a different client. If you know you are running a model that has a profile, apply **that** profile, state the mismatch in one line, and recommend `/rulesmodel` — do not silently rewrite `.dev.env` mid-task. If the value names a model that has a profile and you cannot tell what you are running, trust the value.»
- **No family guessing:** «Applying a neighbouring profile "because it is close" is wrong — profiles encode deltas that are only correct for the named model.» Модель без профиля (Opus 4.8, Sonnet 4.6, GPT-5.5, любые не-Anthropic/не-OpenAI) работает на базовом своде. Пользователь может явно включить чужой профиль через `/rulesmodel <slug>` — тогда исполнить и назвать активный профиль.
- **`AGENT_MODEL` ≠ `SUBAGENT_MODEL_*`:** первый описывает модель самого оркестратора и тюнит его поведение; вторые — конкретные модели субагентов по тирам (`CODING`/`ANALYSIS`/`LIGHT`), их правит `/economymode models`. «Changing one never changes the other. A subagent running a different model applies its own profile only if its client resolves one; the parent does not translate profiles for it.»

### 1.2 Нормализация имён (§3)

Резолв свободного ввода в слаг — «by **family + major version**, case-insensitive, ignoring spaces, dashes, dots, underscores, vendor prefixes and language». Таблица алиасов включает русские написания («клод опус 5», «фейбл 5», «гпт 5.6»). Правила:

- **Запрет молчаливой коэрции:** «**Ambiguous or unsupported input is never silently coerced.** `gpt-5.5`, `opus 4.8`, `sonnet 4.6`, `haiku`, `gemini`, `glm`, `qwen`, a bare `claude` or a bare `5` resolve to **nothing**: report the supported set and leave / clear the value (base ruleset). Offer the nearest same-family profile only as an explicit choice the user confirms.»
- **Суффиксы усилия — не часть слага:** «Client-side variants and effort suffixes (`-thinking`, `-high`, `#xhigh`, `-max`, `-fast`, provider prefixes such as `anthropic/`, `openai/`) are stripped before matching: `anthropic/claude-opus-5#xhigh` → `opus5`.»
- Канонический слаг всегда без точек (`gpt56`, не `gpt5.6`) — под именование файлов правил.

### 1.3 Precedence — что профиль может и не может (§4)

Ключевой принцип: **«A profile tunes how much the agent does on its own initiative and how it communicates. It never lowers the floor.»**

**Профиль МОЖЕТ (MAY):**
- форму ответа: длину, каденс нарратива, формулировку (не наличие!) delivery-отчёта;
- пропорцию upfront-исследования и планирования перед действием;
- eagerness делегирования — но в границах `subagents.md` (и `orchestrator-economy.md` при включённом режиме);
- **запрещать самопридуманную лишнюю верификацию** — «additional self-review passes, a verifier subagent, or repeated re-reading of your own diff that no rule asked for»;
- рекомендовать клиентские настройки (effort / reasoning effort / verbosity / thinking on-off) + промпт-эквивалент, где настройки не доступны агенту;
- рекомендовать уровень существующего презентационного переключателя (уровень скилла `caveman`) с однострочной причиной;
- подчёркивать механизм, которым уже владеют базовые правила (memory, `recall`/`remember`, handoff), если модель документированно от него выигрывает.

**Профиль НЕ МОЖЕТ (MUST NOT) — и «any reading of a profile that seems to do so is a misreading»:**
- хард-гейты: скилл мутаций метаданных, MCP-first search, platform-capability check, обязательства `templatesearch`/`recall`, memory-гейты;
- цепочку валидаторов и её бюджет; гейты verification-gates. Ключевая формула: **«Mandated validator calls are tool evidence, not self-verification — a profile that damps "over-verification" damps only the extra passes the agent invents for itself»**;
- triage, обязательство `CONFUSION` на материальных развилках, принцип полноты/no-placeholders, языковую политику, evidence-однострочники;
- требование подтверждать деструктивные / трудно-обратимые действия.

**Цепочка precedence при конфликте:**

> «`USER-RULES.md` and `memory.md` → `LLM-RULES.md` → the active model profile → `AGENTS.md` and the other on-demand rules, for the behaviours the profile explicitly covers. Everything in the MUST NOT list is outside what a profile can cover, so it wins regardless of the order.»

И протокол разрешения коллизии: если профиль и базовое правило реально столкнулись на поведении **вне** MUST NOT — следовать профилю и отметить одной строкой; если коллизия касается MUST NOT — следовать базовому правилу «and report the profile text as a defect worth fixing upstream».

### 1.4 Модель-агностическая база промптинга (§5)

Части вендорских гайдов, общие для всех моделей — «not repeated in profiles, are never overridden by a profile»:

1. Be explicit and specific; sequence steps when order matters.
2. **Give the reason with the instruction** — «A rule that carries its "why" is followed more accurately — this is why rules in this set state the consequence of violation, and why task briefs to subagents must carry intent, not only steps».
3. Structure mixed content with tags; примеры релевантные, разнообразные, немного (3–5).
4. **Long context: data first, question last** — длинные входы (листинги модулей, XML, логи) выше инструкции; ответы заземлять цитатами.
5. Say what to do, not what not to do.
6. Parallel independent tool calls; never guess parameters.
7. Investigate before answering — не спекулировать о коде, который не открывал.
8. Define success criteria and verify against them.
9. **Keep instructions non-contradictory** — «Conflicting instructions degrade every model; resolve a conflict explicitly … instead of averaging the two readings».

### 1.5 Зачем

Решает три проблемы: (а) один свод правил ведёт себя по-разному на разных LLM (Opus многословен и перепроверяет, Sonnet буквален, Fable переплановывает и рапортует без evidence, GPT-5.6 деградирует от повторов); (б) соблазн «подкрутить правила под модель» ломает переносимость — слой дельт изолирует вендорские причуды; (в) без жёсткой границы MAY/MUST NOT адаптация под модель незаметно ослабляет гейты качества.

### 1.6 Применимость к Cursor-kit: 🔧 адаптация (высокий приоритет)

- **Хранение `AGENT_MODEL`:** у нас нет `.dev.env`. Варианты: (а) секция-overlay в `openspec/project.md` (у нас уже есть паттерн overlay + `capture-to-project.mdc`); (б) полагаться только на self-knowledge — в Cursor оркестратор знает свою модель из системного промпта («powered by …»), и правило «self-knowledge wins» делает записанное значение почти лишним. Рекомендация: **self-knowledge как primary, запись в project.md как опциональный override для команды** — это упрощение схемы ai_rules_1c, оправданное тем, что Cursor всегда сообщает агенту его модель.
- **Файлы профилей:** прямой аналог — `.cursor/rules/model-profile-<slug>.mdc` c `alwaysApply: false`, подгрузка через always-on стаб (как наши `gate-dispatcher.mdc` / `chat-output-budget.mdc` stub→full). Стаб — 5–8 строк: таблица «модель → файл профиля», принцип «профиль не ослабляет гейты», запрет соседних профилей.
- **MAY/MUST NOT-граница — переносится дословно (✅ внутри 🔧):** наши хард-гейты уже поимённо известны (BSL/XML write guard, APPLY GATE, LINT GATE, writer pipeline, verified-cause, delegation gate, chat-output-budget HALT). Формулу «Mandated validator calls are tool evidence, not self-verification» стоит взять как есть — она закрывает реальный риск: профиль для Opus «не перепроверяй себя» не должен отменить ReadLints/reviewer.
- **Precedence-цепочка:** адаптировать под наши слои: user rules → память проекта (project.md overlay) → активный профиль модели → workspace rules (.mdc) — только для поведений, которые профиль явно покрывает; MUST NOT вне охвата профиля всегда.
- **§5 (базовые принципы промптинга):** ✅ прямой перенос как короткое on-demand правило или секция в 1c-agent-patterns — особенно «reason with the instruction», «data first, question last», «never average conflicting readings». Половина уже де-факто у нас есть (интент вместо микрошагов в промпте writer), но не оформлена как единый список.

---

## 2. Профиль Claude Fable 5 — `content/rules/model-fable5.md` (полный список дельт)

**Baseline:** «Fable 5 sustains long, autonomous, multi-step work and follows instructions strongly enough that short instructions beat enumerated checklists. Individual turns run longer than on prior models — that is expected, not a hang.»

Все 10 секций:

1. **Act when you have enough to act.** Fable может переплановывать амбигуозную задачу и «survey options it will not pursue». План остаётся, но короткий: «files / procedures to touch, risks, verification points. Not an options catalogue». «Do not re-derive facts already established in this session, re-litigate a decision the user already made, or narrate alternatives you will not take. When weighing two approaches, give a recommendation, not an exhaustive comparison. (This applies to user-facing text, not to your thinking.)» CONFUSION на материальной развилке остаётся; низкорисковая амбигуозность — однострочное допущение; убирается «третий путь — long meditation on options».
2. **Effort and over-tidying.** `high` — дефолт; `xhigh` — архитектура, кросс-подсистемный рефакторинг, тяжёлый дебаг; `medium`/`low` — рутина («lower effort on Fable 5 still performs strongly»). На высоком effort модель «gathers context and tidies beyond the task» — противоядие: no unrequested refactors, no abstractions for one-time operations, no error handling for impossible scenarios, no compatibility shims. «A bug fix does not need the surrounding code cleaned up.» Снижать effort, когда задача решается, но занимает дольше, чем заслуживает.
3. **Short instructions, literal gates.** Ключевая дельта: «prescriptive scaffolding written for weaker models can *degrade* output here». Процессные правила — применять по духу («apply the spirit of triage, planning and reporting without mechanically expanding every checklist into extra work or extra prose»); **гейты — буквально** («These are not stylistic scaffolding — they encode consequences the model cannot infer from the code in front of it»). Брифы субагентам: «intent plus constraints plus scope, and skip the micro-steps».
4. **Ground every progress claim in evidence.** «On long autonomous runs, unaudited status reports are the main failure mode this model has to be steered away from.» Перед отчётом о прогрессе — «audit each claim against an actual tool result from this session»: «Проверено», «тесты прошли», «синтаксис чистый» требуют соответствующего вывода инструмента. «Unverified is a status you report, not a gap you paper over.»
5. **Boundaries and checkpoints.** Fable «can occasionally take an action nobody asked for (a defensive git branch, a drafted document, a "while I'm here" fix)». Правила: когда пользователь описывает проблему / думает вслух — «the deliverable is your assessment. Report findings and stop; do not apply a fix until asked»; никаких новых файлов/веток/бэкапов, которые задача не просила; временные артефакты чистятся до сдачи; перед state-changing действием — проверить, что evidence поддерживает **именно это** действие («a symptom that pattern-matches a known failure may have a different cause»); паузы только на деструктив / смену скоупа / input, который может дать только пользователь. «When you do stop, ask and end the turn — do not end on a promise.»
6. **Do not end a turn on an intention.** «Deep into a long session this model can end a turn with a statement of intent ("сейчас запущу проверку") without issuing the call.» Перед завершением хода прочитать последний абзац: если это план / анализ остатка / вопрос, на который можешь ответить сам / обещание — сделать сейчас. **«Context budget is not a reason to stop.»** — не предлагать новую сессию, не сокращать работу из-за «тесного окна»; для настоящего handoff — скилл handoff / remember.
7. **Parallel subagents.** «Fable 5 dispatches and sustains parallel subagents more dependably than prior models.» В рамках критериев делегирования — предпочитать «parallel independent tracks … and keep working while they run instead of blocking on each return». «A long-lived subagent that keeps its context across subtasks beats re-briefing a fresh one.» Вмешиваться, когда субагент дрейфует.
8. **Never echo your own reasoning.** «Instructions that ask the model to reproduce, transcribe or explain its internal reasoning as response text can trigger a refusal (`reasoning_extraction`) on this model.» Не добавлять «покажи ход рассуждений» и т. п. в промпты/брифы/скиллы; если такое есть в legacy-брифе — выкинуть строку и сказать об этом одной строкой. Не ограничивает work product: план, допущения, список источников, CONFUSION-опции, delivery-отчёт — «describe decisions and evidence, not the internal reasoning trace that produced them». Бонус-факт: `refusal` stop reason — документированный исход, не баг; на легитимной работе — доложить и продолжить на другой модели, не перефразировать вокруг классификатора.
9. **Memory pays off here.** «This model benefits more than most from a written memory layer.» recall до проектирования, remember в том же ходе, что и коррекция; «Record confirmed approaches as well as corrections — a note that says "this pattern worked and why" is as valuable as one that says "do not do this".»
10. **Readable final answers.** «In long agentic runs this model's prose can drift into dense working shorthand — arrow chains, hyphen-stacked compounds, invented labels, references to work the user never saw.» Шортхенд между тул-коллами — ок; «The final answer is for a reader who saw none of it»: аутком первым предложением, полные предложения, термины расшифрованы. «If you have to choose between short and clear, choose clear.» Взаимодействие с caveman: на длинных прогонах предпочитать уровень `lite`.

### Применимость: 🔧 адаптация (приоритет №1 среди профилей)

Fable 5 — актуальная модель нашего оркестратора. Дельты №1, 4, 5, 6, 10 частично совпадают с системным промптом Cursor (autonomy_guidance, communication_style) — их дублировать не надо; ценность — в **специфике для kit**: (№3) наши скиллы местами написаны как prescriptive scaffolding («механическое разворачивание чеклистов») — профиль легитимизирует «apply the spirit» для процессов при буквальных гейтах; (№4) evidence-audit прогресс-клеймов усиливает наш LINT GATE / evidence-блоки reviewer; (№7) поощрение параллельных треков субагентов — прямо ложится на наши Task-вызовы; (№8) **проверить наши шаблоны промптов** (1c-agent-patterns, sidecar) на формулировки типа «объясни ход рассуждений» — риск reasoning_extraction-отказа; (№9) у нас нет remember/recall-MCP, но есть KB (openspec/knowledge) — дельта «записывать подтверждённые подходы, не только запреты» применима к knowledge-format.

---

## 3. Профиль GPT-5.6 — `content/rules/model-gpt56.md` (полный список дельт)

**Baseline:** «GPT-5.6 is more concise, more proactive and better at inferring intent than GPT-5.5, and it responds measurably better to **lean** context than to repeated emphasis.»

Все 6 секций:

1. **Lean context — each instruction once.** «Removing repeated instructions and examples and simplifying tool descriptions improves both task performance and token efficiency on this model (vendor testing: ~10–15% higher scores at 41–66% fewer tokens).» Правила: грузить минимальный набор правил по triage («docs-fix loads nothing beyond the always-on layer; quick-fix loads the one relevant rule»); не перечитывать перекрывающиеся файлы в одной задаче (индекс → детальный файл, не оба); **«Treat a rule as stated once. This ruleset repeats emphasis … so that a rule survives being read in isolation. Repetition marks importance, not additional work: one obligation = one action. A gate mentioned three times is still one gate»**; узкая поверхность инструментов; «Leanness never means skipping a mandated call».
2. **Reasoning effort and verbosity.** `reasoning_effort`: `low`/`none` — docs-fix и lookups; `medium` — quick-fix; `high` — full-cycle; `xhigh`/`max` — архитектура и тяжёлый дебаг. **«When porting a setting from GPT-5.5 / 5.4, keep the old level as the baseline and try one level lower — this model usually holds quality there.»** `text.verbosity`: модель и так лаконичнее — «blanket brevity instructions carried over from older prompts are redundant — drop them instead of stacking them». Форма отчёта: «lead with the conclusion, then the evidence that supports it, then any material caveat, then the next action». Где параметры недоступны — промпт-эквивалент: заявить глубину один раз в начале плана.
3. **Autonomy boundaries.** «It needs the boundary drawn, not the initiative suppressed.» **Proceed without asking:** безопасная локальная обратимая работа (чтение/поиск, правки файлов проекта, валидаторы, метаданные-скилл, OpenSpec-артефакты, заметки в память). **Ask first:** всё, что меняет состояние вне собственных правок или трудно обратимо (операции с ИБ, удаления, `git push`/force-push/history rewrite, внешние системы, «any **material expansion of scope** beyond what was requested»). Формат эскалации настоящей развилки — CONFUSION; подтверждение деструктива — «a plain one-line question, not a CONFUSION block». «Do not use a destructive shortcut to get past an obstacle.»
4. **Intent-level briefs, not micro-steps.** «GPT-5.6 infers the user's underlying goal and the intended level of work from context better than earlier models, so prescriptive step-by-step guidance buys little and costs tokens.» Бриф субагенту: «state the goal, the constraints, the scope, and the definition of done. Skip the mechanical step list unless the order genuinely matters (it does for the gates — say "validators per `B.1`", not the three call names spelled out with parameters)». Недоспецифицированный низкорисковый запрос — «infer the most useful reading, state the assumption in one line, and proceed». Однострочная преамбула перед пачкой тул-коллов; «No narration per call».
5. **No contradictory instructions.** «Conflicting instructions are expensive on reasoning models: the model spends effort reconciling them instead of solving the task.» Конфликт — разрешать явно (precedence-цепочка или CONFUSION); «Never average the two readings into a compromise implementation». Конфликт внутри свода — фиксировать как friction-сигнал (`rule-friction:`-заметка) и рекомендовать `/evolve`, «Do not patch the rule inline». Длинные брифы структурировать тегами `<task>`, `<constraints>`, `<scope>`, `<done_when>`.
6. **Levers worth knowing.** Pro mode — для hard quality-critical задач; programmatic tool calling — для bounded workflow с пакетной постобработкой результатов инструментов. «Both are configuration choices for the user; state the recommendation in one line when a task would clearly benefit.»

### Применимость: 🔧 адаптация

GPT-5.6 доступен у нас как `gpt-5.6-sol-medium` в enum Task — профиль актуален и для оркестратора (если пользователь выберет GPT), и особенно как **инструкция для брифов субагентам на GPT-тирах**: intent-level брифы (№4) и структура `<task>/<constraints>/<scope>/<done_when>` прямо совместимы с нашим INPUT CONTRACT writer'а. Дельта №1 (lean context) — аргумент против дублирования правил в нашем kit: наши always-apply стабы + on-demand полные тела — уже правильная архитектура; принцип «a gate mentioned three times is still one gate» стоит записать явно, потому что у нас правила намеренно повторяются (stub + full + SKILL). №5 — «never average conflicting readings» — универсален, перенести в базовый слой, не в профиль.

---

## 4. Профиль Claude Opus 5 — `content/rules/model-opus5.md` (кратко, полный список)

**Baseline:** «runs this ruleset well without tuning». Дельты: (1) **Verbosity** — ответы длиннее прежних Opus; отчёт tight, «lead with the outcome»; «Written artefacts follow the same calibration … Length is not evidence of thoroughness» (авторские файлы — proposal/design/tasks/handoff — тоже склонны раздуваться). (2) **Narration** — одно предложение перед первым тул-коллом; дальше апдейт только на material finding / смену направления. (3) **No self-invented verification** — «Do not add verification the ruleset did not ask for … and **never** a subagent spawned to check your own work»; мандатная цепочка — не self-verification; scope discipline против самовольного расширения задачи. (4) **Delegation damping** — «Opus 5 delegates more readily than prior models, and delegation multiplies cost when the task is small»; лин к прямому исполнению, low spawn counts, «prefer a single wide brief over fan-out». (5) **Correction narration** — исправлять прежние заявления только когда ошибка меняет код/выводы/решения; «No tally of your own mistakes, no apology paragraph». (6) **Review tasks** — «a brief that says "only critical issues" produces fewer findings, not a better filter»: просить **coverage** (все находки с severity и confidence), фильтровать после. (7) **Effort/thinking** — `high` дефолт, `xhigh` для сложного; **«Keep thinking enabled»** — с выключенным thinking модель «can emit a tool call as plain text» и течёт XML-тегами; «If cost is the concern, lower effort — do not disable thinking»; никогда не писать «do not think» в промпты; 1M-контекст — не лицензия на bulk-read.

### Применимость: 🔧 адаптация

Opus 5 в нашем enum (`claude-opus-5-thinking-high`). Самое переносимое — №6 (**coverage-first брифы для reviewer**): наш onec-code-reviewer может получать «only critical» — антипаттерн задокументировать в 1c-agent-patterns; №3/№4 — готовые дельты профиля оркестратора; №7 — предупреждение «не писать "do not think" в брифы» стоит добавить в наши шаблоны промптов независимо от профиля.

## 5. Профиль Claude Sonnet 5 — `content/rules/model-sonnet5.md` (кратко, полный список)

Дельты: (1) **Literal instruction following** — «does **not** silently generalise one item to another»; в брифах перечислять scope для **каждого** объекта («перепроверь все три модуля из списка, не только первый»); «A brief that names one example and expects the pattern to spread will get exactly the one example»; явно указывать out of scope. (2) **Effort** — respects effort **strictly**; на `low` для сложной задачи — under-thinking; «the fix is **raising effort**, not padding the prompt»; кросс-модельная шкала: Sonnet 5 `medium` ≈ Sonnet 4.6 `high`. (3) **Adaptive thinking on** — «With thinking disabled the model reaches for tools noticeably less» → ломает tool-first дисциплину; `budget_tokens` удалён, `temperature`/`top_p`/`top_k` отклоняются. (4) **Progress updates** — уже откалиброваны, не добавлять скаффолдинг принудительных промежуточных итогов. (5) **Review — coverage** — «"only high-severity" makes it investigate just as deeply and then **withhold** the lower-severity findings»; если нужен самофильтр — определить планку конкретно, не качественным словом. (6) **Token budget** — модель отслеживает остаток окна; «Do not wrap up work early because context feels tight»; токенизатор ≈+30% к Sonnet 4.6.

### Применимость: 🔧 адаптация (низкий приоритет)

Sonnet 5 не в нашем enum моделей Task — профиль оркестратора не нужен. Ценность общая: №1 (перечислять scope поимённо в брифах субагентам) и №5 (coverage-first) — это правила **написания брифов**, полезные для любой модели-исполнителя; кандидаты в 1c-agent-patterns как model-agnostic советы.

---

## 6. Команда `/rulesmodel` — `content/commands/rulesmodel.md`

### Суть

Канонический редактор ключа `AGENT_MODEL`; «The command edits **only** the `AGENT_MODEL` line in `.dev.env` — never other keys, never other files». Механика:

- **Нормализация — работа агента, не скрипта:** «Resolve free-form input to a canonical slug **yourself** — no script has to be fed an exact string» (lowercase, срезать разделители, вендор-префиксы, суффиксы усилия, дата-штампы; принимать русские написания; «use judgement for spellings it does not list»).
- **Аргументы:** пусто/`auto` — определить модель по self-knowledge; не из четырёх — трактовать как `off` и назвать, кого опознал. `status` — отчёт без правок (что записано, совпадает ли с running model, рекомендованные effort/verbosity, 2–3 главных дельты в силе, для ориентира — модели тиров субагентов с указателем на `/economymode models`). `off`/`none`/`generic`/`сброс` — очистить значение.
- **Запрет коэрции** повторён и в команде: «report the four supported slugs, explain that the base ruleset applies unchanged for other models, and ask which the user wants … never map one family onto another».
- **Requested slug ≠ running model — легально** («the user may be configuring the project for a teammate or for another client»): записать запрошенное, применять сейчас профиль своей identity, о расхождении — одной строкой.
- **Хрупкий инсталлятор учтён:** если `.dev.env` нет — «do **not** create a partial file (a stub would permanently block it)»; применить профиль только на сессию. «No re-render needed» — значение читается at task time, профили уже установлены как on-demand.
- **Подтверждение пользователю** — 3–5 строк по-русски: что записано; 2–3 главных изменения поведения; **что НЕ меняется** (хард-гейты поимённо); рекомендуемые клиентские настройки; как переключить/выключить.
- **Constraints:** «The profile layer never weakens a hard gate» (полный список повторён); «General prompting principles are not part of the profile»; «never rewrite a rule file to "bake in" a profile — the layer is selected by the `.dev.env` value, not by editing rules».

### Зачем

Убирает трение конфигурации (пользователь пишет имя модели как угодно) без риска: невозможно молча получить чужой профиль, невозможно через смену профиля ослабить гейты, состояние прозрачно (`status`).

### Применимость: 🔧 адаптация

Прямой аналог — команда `.cursor/commands/` (напр. `/rulesmodel` или `/model-profile`) с той же логикой auto/status/off, но записью в `openspec/project.md` overlay вместо `.dev.env` (или вообще без персистентности — только session-scope, т. к. self-knowledge в Cursor всегда доступен). Ценные заимствования независимо от команды: (а) нормализация как обязанность агента с таблицей алиасов + русские написания; (б) шаблон подтверждения «что изменилось / что НЕ изменилось / как выключить»; (в) паттерн «команда правит ровно один ключ». Наш существующий guard в описании Task («If the user requests a model that is NOT in the list above, do NOT substitute a different model or guess») — тот же принцип no-silent-coercion, но для субагентов; правило ai_rules_1c закрывает второй фронт — профиль самого оркестратора.

---

## 7. Субагенты — `content/rules/subagents.md`

### 7.1 Учёт профиля модели в делегировании

> «The active-model profile … may tune **how eagerly** you delegate within these criteria: some models delegate too readily and their profile biases toward direct execution and low spawn counts, others sustain parallel subagents well and their profile encourages independent parallel tracks. The criteria above, the per-subagent "when NOT to call" column, the built-in-explorer ban, and every common obligation stay unchanged — a profile never adds a subagent the rules forbid, and never removes one they require. In particular, no profile authorises a subagent spawned to double-check your own work.»

То есть spawn eagerness — единственная степень свободы профиля в делегировании; каталог, запреты и обязательства — инвариант.

**Применимость: ✅ прямой перенос принципа.** У нас делегирование жёстче (BSL write guard делает writer обязательным независимо от модели) — тем важнее зафиксировать: профиль модели может смещать eagerness только там, где у оркестратора есть выбор (explorer vs прямое чтение в рамках DELEGATION GATE, параллельность треков), и никогда — обязательность writer/reviewer.

### 7.2 Host-tool built-in explorers (hard ban)

> «Cursor (and some other hosts) ship a **built-in** Explore helper — e.g. Cursor Task `subagent_type: "explore"` — with a fixed, non-overridable system prompt. That helper is **not** this project's explorer. It does not run the MCP-first fallback chain, does not prefer 1C graph / code-metadata tools, and does not return the structured report from `content/agents/explorer.md`.»

Четыре пункта hard rule: (1) делегированное read-only исследование → только проектный `1c-explorer`; (2) не запускать built-in Explore для этой работы; (3) **«If the session's Task / subagent API only exposes built-in types and cannot start the installed `1c-explorer` — do not silently substitute built-in Explore»** — либо исследовать на родителе, либо сказать пользователю; «Falling back to built-in Explore is a defect»; (4) «project rules steer the **parent**; they do not rewrite the built-in Explore prompt — so "putting explore instructions in rules" is not a substitute for calling `1c-explorer`». Бан «Cursor-shaped … but applies to any host-native generic explorer».

**Применимость: 🔧 адаптация с оговоркой.** У нас есть и built-in `explore`, и кастомный `onec-code-explorer`. Наша таблица делегирования уже направляет «Исследование 3+ модулей» на onec-code-explorer, но **явного запрета** подменять его built-in explore нет — это реальная дыра: модель ради скорости может дернуть explore для 1С-кода. Стоит добавить в `1c-agent-delegation.mdc` строку-запрет по образцу пункта 3 (включая «не подменять молча»). Оговорка: полный бан нам не нужен — built-in explore легитимен для **не-1С** задач (навигация по .cursor/rules, openspec-артефактам); граница — «исследование 1С-кодобазы → только onec-code-explorer». Аргумент №4 (правила не переписывают промпт built-in агента) — важное обоснование, которое стоит процитировать в правиле.

### 7.3 Критерии каталога и model-tier routing

- Каталог — 13 агентов, формат «When to call / When NOT to call» двумя колонками; выделяются жёсткие ограничители: «1c-code-reviewer — **Only when the user explicitly asks for a code review**; Auto-triggering after edits is forbidden»; 1c-tester гейтится env-параметром.
- **Model-tier routing:** «Subagent source files do **not** hard-code model names. Each agent declares an abstract tier in its frontmatter — `modelTier: coding` | `analysis` | `light` — and the installer resolves the tier into a concrete model from `.dev.env` … Model names live only in project settings, never in rules or agent prompts.» Три тира: `coding` (мутирует код — сильнейшая модель), `analysis` (ревью/планы/доки), `light` (скаутинг, impact-списки, механические проверки — дешёвая модель).
- Правила роутинга: light-кандидаты перечислены (скаутинг, навигация, impact-списки, механическая пост-проверка, мелкие bounded-правки); **«Never use the `light` tier as the final authority»** для архитектуры/транзакций/безопасности — «Output of a light-tier run is working material, not a source of truth»; «Do not delegate trivial single-step tasks at all — the launch overhead exceeds the saving»; тир не меняет обязательств валидации.
- **Bounded sidecar task templates:** каждый промпт делегирования обязан содержать bounded responsibility (одна верифицируемая цель), allowed/forbidden sources, read/write scope, expected output format, и напоминание «the subagent **is not alone in the codebase**: it must not revert or overwrite changes outside its scope». Шесть готовых шаблонов: explorer-impact, explorer-patterns, metadata-scout, worker-bounded-edit, reviewer-risk, smoke-check.

**Применимость: 🔧 адаптация.** У нас модели субагентов — SSOT `model-selection.mdc` + Task(model=slug); идея **абстрактных тиров во frontmatter** (`modelTier` вместо слага) элегантнее нашей таблицы: агент объявляет класс задачи, маппинг «тир → слаг» живёт в одном месте. Стоит рассмотреть при следующей ревизии model-selection.mdc. «Light output = working material, not source of truth» — стоит записать явно (у нас explorer-отчёты иногда становятся основой решений без spot-check). Шаблон «not alone in the codebase» — прямой кандидат в наши sidecar-шаблоны 1c-agent-patterns. Формат каталога «When NOT to call» — у нас частично есть; докрутить.

---

## 8. Экономия оркестратора — `content/rules/orchestrator-economy.md`

### Суть

Opt-in режим `ORCHESTRATION=economy` (команда `/economymode`; фраза в чате переключает на сессию без правки файла). Принцип:

> «Parent-agent (orchestrator) tokens are the most expensive resource of the session — typically several times the price of a subagent on the `analysis` / `light` tier. While the mode is on, the parent **does not do anything itself that a subagent of an appropriate tier can do**: the parent thinks, decides, writes specs, and verifies; subagents do the reading and the writing.»

Разделение труда — родитель оставляет себе: triage/декомпозицию, архитектурные решения («decision forks go to the **user** via the CONFUSION format, never to a subagent»), спеки для субагентов «with all accepted decisions inside», выборочный spot-check отчётов против первоисточников, интеграцию/гейты/финальный отчёт. Делегируется: exploration/inventory/bulk reading (только `1c-explorer`, не built-in), имплементация по готовому плану, планирование/анализ/доки, механические мультифайловые правки, quick error fixes.

Ключевые ограничители: «The mode changes **who executes**, never **which gates apply**. On any conflict, the stricter existing rule wins»; тривиальные правки не делегируются (overhead > экономия); reviewer не автотриггерится. Mode discipline: «A spec for a subagent contains ready decisions: the subagent executes, it does not invent»; «Scouting reports are spot-checked against primary sources … light models hallucinate; verification is mandatory»; «Review of delegated results is selective … a full re-read eats the savings»; **эскалация: «if a subagent failed twice on a clear spec, the parent does the work itself — a third iteration costs more than direct execution»**; факт режима и исполнители — в delivery summary.

### Зачем

Экономика токенов: дорогой родитель как чистый «мозг», дешёвые тиры — «руки», без ослабления гейтов.

### Применимость: 🔧 адаптация (частично уже есть)

Наш kit уже несёт ту же философию распределённо: DELEGATION GATE (порог обращений к .bsl), orchestrator-as-navigator, context-strategy, BSL write guard. Чего у нас **нет** и стоит взять: (а) **правило эскалации «две неудачи субагента на ясной спеке → родитель делает сам»** — у нас лимит итераций writer↔reviewer есть, а критерия выхода из бесплодного делегирования нет; (б) «spot-check отчётов скаутов против первоисточников перед решением» — явно записать (перекликается с нашим preserve-subagent-reports, но там про сохранение, не про проверку); (в) «selective review, a full re-read eats the savings». Сам toggle-режим нам не нужен — у нас делегирование не opt-in, а конституция.

---

## 9. UI-тестирование — `content/rules/ui-testing-tools.md`

### Суть

Жёсткий порядок предпочтений драйверов веб-тестов 1С: (1) **agent-browser** (vercel-labs) — «default for 1C web client tests. Use accessibility-tree snapshots … Screenshots only for evidence in the test report, not as the primary observe loop»; (2) built-in browser MCP клиента — только fallback после гейта; (3) Windows-MCP — «last resort», только настоящий desktop-сценарий. «Never invent a parallel stack (PowerShell screenshot loops, custom OCR, ad-hoc vision pipelines).»

**Механика preflight (hard gate):** перед первым браузерным действием — каждый раз: (1) детект agent-browser (CLI на PATH или MCP-тулы в сессии); (2) есть → работать без вопросов; (3) нет → **«stop before any browser action»** и спросить пользователя одним сообщением на русском (готовый текст с вариантами да/нет в правиле); (4) «да» → выполнить `/install-agent-browser` полностью, продолжить (с паузой на рестарт клиента при необходимости); (5) «нет» → продолжить на built-in, отметить одной строкой стоимость, «Do not ask again in the same session»; (6) **автономный прогон без оператора → не автоинсталлировать**, залогировать одну строку и продолжить на built-in. «Skipping this check and silently using cursor-ide-browser / Playwright / vision is a **defect**.» Token discipline: структурные снапшоты вместо картинок, re-snapshot после навигации, узкий профиль MCP-тулов.

### Зачем

Vision-петля на скриншотах — самый дорогой путь; правило гарантирует, что дешёвый драйвер будет предложен до дорогого прогона, но без блокировки автономных прогонов и без самодельных OCR-стеков.

### Применимость: ❌ не применимо сейчас / 🔧 паттерн — да

В нашем kit нет инфраструктуры UI-тестов 1С (нет публикации ИБ, нет tester-агента) — прямо переносить нечего. Ценен **обобщаемый паттерн preflight**: «перед дорогой операцией — детект дешёвого инструмента → предложение установки с явным выбором → однократный отказ на сессию → в автономии не автоинсталлировать, а деградировать с логом». Применим у нас к любым опциональным тулчейнам (например, линтеры/валидаторы BSL, MCP-серверы 1С), если такие появятся. Также перенос-кандидат: «структурные снапшоты > скриншоты» как принцип для будущих browser-задач.

---

## 10. Верификация — `content/rules/verification-policy.md`

### Суть

Параметр `VERIFICATION_DEPTH` (Defaulted; канонический редактор — `/litemode`) тюнит глубину гейтов 1–3 **только для низкорисковых правок**. Три уровня: `full` (три валидатора, до 3 вызовов на валидатор после блокирующего фикса), `standard` (три валидатора, ровно одно подтверждение после фикса — 2 вызова, «no open-ended retry loop»), `lite` (**`syntaxcheck` обязателен всегда**; `check_1c_code`/`review_1c_code` пропускаются, кроме явной просьбы).

**Safety floor — never crossed by any level:** Gate 1 никогда не пропускается; **«Promotion-trigger changes … always run the full chain … regardless of `VERIFICATION_DEPTH`. `lite`/`standard` lighten only the checks that were already being applied to low-risk, quick-fix-eligible edits — they do not weaken the control of dangerous paths.»** Promotion triggers (детально): wired metadata (переименование/удаление объекта, изменение posting/write path, RLS, индексация, fill-checks, подписки), транзакционные пути, **contract change публичного `Экспорт`** (чисто внутренний фикс с сохранением контракта остаётся quick-fix), adopted-объекты расширений, подписки/регламентные задания/RLS. «When in doubt — full-cycle wins.» Критерии isolated metadata addition для quick-fix — исчерпывающий список из 4 условий (новый несвязанный объект, ничего существующего не трогается, никакого проведения/прав, не требует БСП-регистрации); «wiring is a separate change». Quick-fix gate: «Quick-fix reduces planning and delegation overhead, **not** verification depth».

### Зачем

Даёт проекту явную ручку «скорость vs глубина» с гарантией, что ослабляется только проверка заведомо низкорисковых правок, а опасные пути защищены конституционно (триггеры промоушена сильнее любой настройки).

### Применимость: 🔧 адаптация

У нас аналоги распределены: Light/Mechanical Mode (1c-halt-triggers), task-triage, verify_mode. Чего не хватает и стоит взять: (а) **явный «safety floor» как отдельная секция** — список того, что не ослабляет ни один режим (у нас: reviewer обязателен даже в исключениях, ReadLints после каждой правки) — сейчас это разбросано; (б) **формализованные promotion triggers** — наш Light Mode описывает, что можно, а список «что всегда эскалирует» (транзакционные пути, контракт Экспорт-процедуры, RLS, adopted-объекты) — готовый чеклист для 1c-halt-triggers; (в) принцип «quick-fix reduces overhead, not verification depth» — точная формула для нашего Light Mode.

---

## 11. Структура AGENTS.md (~58 КБ always-on) — приёмы сжатия

Файл 58 748 байт, организован в 5 макро-разделов: `# Process` (Persona, Core Principles, Active model adaptation, Development Procedure — triage + 5 шагов, Project info) → `# Tooling & Standards` (MCP Tool Calling A/B/C, Coding Standards, Skills and Subagents) → `# Discipline` (Project memory, Rules self-improvement, Editing discipline) → `# Additional rules (load on demand)` (аннотированный индекс ~40 правил по 8 категориям) → `# Spec-driven development workspace`.

Приёмы сжатия и организации (без пересказа содержимого):

1. **Секция «Active model adaptation» в always-on — 10 строк.** Только selection/loading/boundary/не-путать-с-SUBAGENT_MODEL; всё остальное — «Routing, the alias table, precedence, and the model-agnostic prompting baseline no profile may override — `content/rules/model-adaptation.md`». То есть трёхуровневая пирамида: always-on стаб → router-файл → 4 файла профилей.
2. **«When to load this file» — первая строка каждого on-demand правила.** Само правило несёт свой триггер загрузки; always-on индекс дублирует его одной строкой-cue. Явно оговорено: «Each entry below is a routing cue only; the authoritative scope description is the frontmatter `description` inside the file itself» — SSOT триггера в frontmatter, индекс не авторитетен.
3. **Compat-роутеры вместо удаления:** `dev-standards-core`, `verification-checklist` помечены «compatibility router …; load only when following a legacy reference» — старые ссылки не ломаются, новые читатели идут к focused-файлам.
4. **Decision shortcut перед справочником:** triage начинается с 4-строчного классификатора («classifies most tasks in seconds; the bullets below are the reference for contested cases») — быстрый путь отделён от полного.
5. **Классификация параметров Advisory / Highly desirable / Defaulted** с общим принципом «No field is globally mandatory … do not gather empties up front» — снимает целый класс вопросов агента одним правилом; каждый Defaulted-параметр обязан иметь документированный дефолт.
6. **Path convention** — один абзац легализует двойную адресацию (source-repo путь vs установленная копия, `.md`→`.mdc`), «This convention applies globally — individual rule and subagent files do not repeat the disclaimer».
7. **Evidence-однострочники как контракт** (`Template:`, `Memory:`, `Metadata tooling:`, `IB tooling:`) — вместо длинных отчётных форм каждая дисциплина сворачивается в строку финального ответа; гейты проверяемы по наличию строки.
8. **Осознанное повторение с декларацией:** свод повторяет акценты («hard gate», «defect»), чтобы правило переживало изолированное чтение, и одновременно профиль GPT-5.6 декларативно снимает риск: «Repetition marks importance, not additional work». Повторы — только для floor-обязательств, детали не дублируются («The full catalog of detail files is owned by `coding-standards.md`; this document does not duplicate or partially mirror it»).
9. **Каждое правило несёт «why» и цену нарушения** («…is a defect, not a stylistic choice», «same standing as a skipped validator») — санкция вместо императива, следуя собственному §5 «Give the reason with the instruction».

**Применимость: 🔧 адаптация.** Наш kit уже реализует №1 (stub→full), №3 (redirect-стабы), частично №7 (Linter/Naming Signals). Стоит взять: №2 — унифицированная шапка «When to load this file» в on-demand `.mdc` + принцип «индекс = routing cue, SSOT в frontmatter description» (у нас триггеры местами дублируются между dispatcher и файлами с риском рассинхрона); №4 — decision shortcut в начало task-triage; №5 — классификация параметров (у нас project.md overlay-поля можно так же градуировать); №9 — аудит наших правил на «императив без why».

---

## 12. Сводная таблица применимости

| # | Механика | Вердикт | Приоритет | Куда в нашем kit |
|---|---|---|---|---|
| 1 | Слой model-профилей (роутер + 4 профиля) | 🔧 адаптация | Высокий | `.cursor/rules/model-profile-*.mdc` + стаб; self-knowledge как primary селектор |
| 2 | MAY/MUST NOT граница + «validator calls are tool evidence, not self-verification» | ✅ прямой перенос формулы | Высокий | стаб профилей; связать с BSL write guard, LINT GATE, reviewer |
| 3 | Precedence-цепочка user→memory→profile→base | 🔧 адаптация под наши слои | Средний | стаб профилей |
| 4 | Запрет молчаливой коэрции + no family guessing | ✅ (для субагентов уже есть) | Средний | распространить с Task-enum на профиль оркестратора |
| 5 | §5 model-agnostic baseline промптинга | ✅ прямой перенос | Средний | 1c-agent-patterns или новое короткое правило |
| 6 | Дельты Fable 5 (10 шт., особенно evidence-audit, reasoning_extraction, spirit-vs-literal) | 🔧 адаптация | Высокий | профиль + аудит шаблонов промптов на «покажи рассуждения» |
| 7 | Дельты GPT-5.6 (lean context, one instruction once, intent-briefs, no averaging) | 🔧 адаптация | Высокий | профиль + INPUT CONTRACT writer; принцип «gate ×3 = один gate» |
| 8 | Дельты Opus 5 (coverage-first review, no self-verification, damped delegation, keep thinking) | 🔧 адаптация | Средний | профиль + антипаттерн «only critical» в брифах reviewer |
| 9 | Дельты Sonnet 5 (literal scope, coverage) | 🔧 частично, model-agnostic советы | Низкий | 1c-agent-patterns (правила брифов) |
| 10 | `/rulesmodel` (auto/status/off, нормализация, шаблон подтверждения) | 🔧 адаптация | Средний | `.cursor/commands/`; запись в project.md overlay или session-only |
| 11 | Spawn eagerness — единственная степень свободы профиля в делегировании | ✅ прямой перенос принципа | Высокий | 1c-agent-delegation.mdc |
| 12 | Запрет built-in Explore для проектного исследования | 🔧 адаптация (бан только для 1С-кода) | Высокий | 1c-agent-delegation.mdc + session-discipline |
| 13 | Model-tier routing (абстрактный modelTier во frontmatter) | 🔧 рассмотреть | Средний | model-selection.mdc при ревизии |
| 14 | «Light output = working material, not source of truth» + spot-check скаутов | ✅ прямой перенос | Средний | preserve-subagent-reports / delegation |
| 15 | Sidecar-шаблоны («not alone in the codebase», bounded responsibility) | 🔧 дополнение | Средний | 1c-agent-patterns/sidecar.md |
| 16 | Economy mode как режим | ❌ (философия уже конституция kit) | — | — |
| 17 | Эскалация «2 неудачи субагента → родитель сам» | ✅ прямой перенос | Средний | 1c-agent-delegation (лимиты итераций) |
| 18 | UI-testing preflight (agent-browser) | ❌ сейчас; 🔧 паттерн preflight | Низкий | запас: паттерн для опциональных тулчейнов |
| 19 | VERIFICATION_DEPTH: safety floor + promotion triggers | 🔧 адаптация | Средний | 1c-halt-triggers (Light Mode), формула «overhead, not depth» |
| 20 | Приёмы AGENTS.md: «When to load» шапки, routing-cue индекс, decision shortcut, параметры Advisory/Defaulted | 🔧 адаптация | Средний | gate-dispatcher, task-triage, project.md |

---

## 13. Рекомендуемый порядок внедрения (эскиз, 3 волны)

1. **ЗНИ «model-profiles»:** стаб `model-adaptation.mdc` (селектор по self-knowledge, MAY/MUST NOT со списком наших хард-гейтов, precedence) + `model-fable5.mdc` и `model-gpt56.mdc` (актуальные модели); Opus 5 — вторым эшелоном.
2. **Точечные правки существующих правил:** запрет built-in explore для 1С-исследований (1c-agent-delegation); spawn-eagerness клауза; эскалация «2 неудачи → сам»; coverage-first в шаблоны брифов reviewer; аудит шаблонов на reasoning-extraction-фразы и «do not think».
3. **Гигиена свода:** шапки «When to load», decision shortcut в triage, секция safety floor + promotion triggers в halt-triggers.

Каждый пункт — отдельный change по нашему workflow (`/opsx:new`); этот отчёт — source context для постановок.
