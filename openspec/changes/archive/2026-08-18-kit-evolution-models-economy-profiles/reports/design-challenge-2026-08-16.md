---
report_type: design-challenge
generated_at: 2026-08-16
agent: onec-code-architect
mode: design-challenge
scope:
  change: kit-evolution-models-economy-profiles
  design_mtime: "2026-08-16T11:48:05+09:00"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — kit-evolution-models-economy-profiles

## KB references

- Discovery выполнен, совпадений нет (taxonomy `openspec/knowledge/_taxonomy.yaml` отсутствует, есть только `_taxonomy.template.yaml`). Секция зафиксирована; на выводы challenge KB-факты не влияли.

## Адверсариальная установка

Разбор независим от сессии постановки: прочитаны `proposal.md`, `design.md`, пять delta specs, ADR-0001, ADR-0003, основной spec `review-quality-disposition`, текущие `model-selection.mdc` / `1c-agent-delegation.mdc` / `review/SKILL.md` / always-apply frontmatter. Не использовались `reports/architecture-new-2026-08-16.md` и `reports/architecture-task-readiness-2026-08-16.md` как источник истины. Закрытых решений verify нет.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** (1) таблица ролей ссылается на слаги вне живого enum `Task.model` (`claude-opus-4-8-thinking-high` и др.) — вызов архитектора падает и молча деградирует на запасную модель; новые модели (Opus 5, Fable 5, GPT-5.6) не задействованы; (2) always-apply ~54 КБ с ~20 КБ дублей; (3) поведение оркестратора не адаптируется под модель чата. Источник: `proposal.md` § Why.
- **Design адресует:** D1/D2/D3 — живой мэппинг + самосверка + двухшаговая цепочка; D1a — Fable как закрытая эскалация; D6/D7 — упаковка always-apply и диета reviewer; D4/D5 — профили; D8–D10 — делегирование и гигиена.
- **Покрытие:** частичное.

Почему не полное:

1. **Why говорит о X (мёртвые слаги в таблице → ошибка enum)** → design адресует X для *обычного* архитектора через `claude-opus-5-thinking-high` (слаг **есть** в живом enum этой сборки) и D3 (не подставлять «похожую» модель). Это закрывает ежедневный сбой, который сейчас кодируется в `model-selection.mdc:19` и `architect-gate.mdc:97–98` (`claude-opus-4-8-thinking-high`).
2. **Why говорит о X (задействовать Fable 5 как доступную новую модель)** → design адресует Z: хардкод `claude-fable-5-thinking-high` как MUST для независимого разбора постановки (`design.md` D1a п.1; `specs/subagent-model-mapping/spec.md` Requirement «Fable только как закрытая эскалация», сценарий «Независимый разбор постановки идёт на Fable»).
3. **X не покрыт, Z ломает X:** verified runtime fact этой сессии (2026-08-16): enum `Task.model` = `inherit`, `claude-opus-5-thinking-high`, `composer-2.5-fast`, `cursor-grok-4.5-high`, `cursor-grok-4.6-xhigh`, `gemini-3.1-pro`, `gpt-5.6-sol-medium`. **В enum нет** `claude-fable-5-thinking-high` (и нет `claude-opus-4-8-thinking-high`). `design.md` § Context строка 7 утверждает обратное: evidence-enum *включает* `claude-fable-5-thinking-high`. Это ложный факт постановки, не закрытое решение.
4. Следствие: D1a «всегда Fable» и D3 «слаг вне enum не подставлять» несовместимы на этой сборке. Спека усиливает конфликт: сценарий «Рантайм свободен от мёртвых слагов» запрещает слаги вне enum в runtime-файлах, а Requirement про Fable требует писать `claude-fable-5-thinking-high` в таблицу/гейты. Приёмка среза S1 («независимый разбор идёт на Fable») на этой сборке либо нарушит D3, либо не выполнится.
5. **Why говорит о Y (диета без потери обязательств)** → design адресует Y упаковкой D6, но адресаты выноса (§ АВТО-ИСПРАВЛЕНИЕ → `review/SKILL.md`; § KB CONTEXT → `knowledge-format.mdc`) противоречат D6 (в): обязательство с диалоговым триггером остаётся в always-apply якоре. Без остатка в always-apply apply-контур потеряет carve-out ADR-0003 (см. ниже) — это не «та же упаковка», а смена наблюдаемого поведения.
6. **Why говорит о Z (адаптация под модель чата без ослабления гейтов)** → D4/D5 покрывают. Внутренний зазор spec: `chat-model-profiles` Requirement «Граница MAY / MUST NOT» говорит «профиль … не транслируется в брифы субагентов», а Requirement «Трёхуровневая пирамида» и сценарий «Бриф субагента учитывает профиль его модели» требуют MAY в intent-брифе. Design D5 различает «профиль чата не копировать» vs «MAY профиля *модели субагента* учесть» — spec этого различия не фиксирует.

### Q2 — Optimality

- **Выбранный путь:** живой мэппинг ролей + самосверка enum + Fable как закрытая эскалация по точному слагу; диета always-apply разжалованием/слиянием с переносом SSOT; пирамида профилей; точечные усиления делегирования.
- **Альтернативы (включая не упомянутые в design):**
  1. **Эскалация, разрешённая живым enum (не упомянута).** Закрытый список режимов D1a сохраняется. Перед вызовом оркестратор читает enum `Task` этой сборки. Если слаг Fable **есть** — передаёт его. Если **нет** — Primary обычного архитектора (`claude-opus-5-thinking-high`) + одна строка, что дорогая эскалация недоступна в этой сборке; family guessing запрещён (D3). Плюс: не воссоздаёт Why. Минус: независимый разбор и обычная постановка временно на одной модели. Почему лучше выбранного: выбранный путь на этой сборке *гарантирует* `Invalid model selection` на самом ответственном вызове — ровно тот дефект, который ЗНИ лечит.
  2. **Независимый разбор на `gpt-5.6-sol-medium`, пока Fable нет в enum (не упомянута).** Слаг **есть** в живом enum. Плюс: другой Primary, чем у обычного `design` (Opus 5) — сохраняется смысл «не тот же вызов, что постановка». Минус: это не «самая дорогая» модель из D1a; при появлении Fable в enum политику придётся сменить. Design отклонил reviewer→GPT-5.6, но не рассматривал GPT-5.6 как *носитель закрытой эскалации архитектора*.
  3. **Остаток carve-out apply-reviewer в always-apply delegation (не упомянута как Chosen).** Детали протокола `/review` остаются в `review/SKILL.md`; в `1c-agent-delegation.mdc` остаётся дословный абзац: авто-fix только functional MUST_FIX без `QualityFlag=weak` / `design-prescribed` / agreement-override; weak не авто-waive и не авто-fix; disposition — на `/review`. Плюс: сохраняет `openspec/specs/review-quality-disposition/spec.md` Requirement «Apply-reviewer does not run disposition AskQuestion» и инвариант ADR-0003 «apply-reviewer не … авто-waive weak». Минус: ~0,5–1 КБ в бюджете 34 КБ. Выбранный адресат D6 («вынести § АВТО-ИСПРАВЛЕНИЕ целиком в `review/SKILL.md`») этот остаток не требует — при apply скилл `/review` не является входным протоколом, значит carve-out не загрузится.
  4. **Не разжаловать полный `1c-xml-write-guard.mdc` (не упомянута).** Compact уже в `1c-agent-delegation.mdc` § XML WRITE GUARD; полный файл имеет `alwaysApply: true` **и** `globs: "src/**/*.xml"` — globs не сработают, пока XML нет в контексте, а запрос «поправь Form.xml» приходит текстом. Chosen (разжаловать полный файл, опереться на compact + cue) здесь разумен. Альтернатива «оставить always-apply» безопаснее по ложным срабатываниям globs, но хуже по бюджету; не превосходит Chosen, если compact+D6(в) сохранены. Упомянута для полноты атаки: не лучше.
  5. **Один файл `model-adaptation.mdc` со всеми MAY/MUST NOT вместо четырёх профилей (не упомянута).** Поведение то же, меньше файлов. Минус: толстый роутер, хуже точечный Read профиля субагента. Не лучше пирамиды D4 при конституции D5.
- **Вердикт по Q2:** есть лучшая альтернатива — (1) обязательна, чтобы D1a не отрицал D3 и Why; (3) обязательна, чтобы упаковка не отменила ADR-0003. (2) равноправна (1) по оси «другая модель для независимого разбора», если заказчик хочет развести независимый разбор и обычный design без Fable.

Отклонённые в design варианты (оркестратор = Opus/Fable в чате; Fable на любой Architect Gate; трёхступенчатые цепочки; файл-состояние профиля) остаются хуже Chosen по цене и инвазивности. Атака не про них.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками.
- **Причины:**
  - Да: ядро Why (мёртвый `claude-opus-4-8-thinking-high`, трёхступенчатый fallback, ложный «inherit нет в enum») лечится D1+D2+D3; Opus 5 / Grok 4 / Gemini reviewer / composer simplifier согласованы с живым enum; конституция профилей (MAY внутри лимитов, MUST NOT гейтов, misread, stub→full carve-out для GPT) здравая; запрет built-in Explore только для 1С-путей точнее тотального бана референса.
  - Нет: нельзя согласовать постановку, которая в § Context печатает неверный enum и затем требует слаг, которого нет — это повтор исходного дефекта на новой роли.
  - Нет: нельзя согласовать вынос apply-carve-out в скилл, который apply не читает, при пустом `### Modified Capabilities` в proposal и отсутствии `## Blast Radius` — молчаливая отмена load-bearing ADR-0003.
  - Нет (слабее): spec профилей противоречит сама себе по трансляции MAY в бриф; переносимый минимум D6 для трёх session-правил не включает TRIGGER context-strategy (3+ файлов / XML|CSV|JSON), хотя smoke S2 его требует. `session-discipline.mdc` сейчас содержит TRIGGER; если разжалование скопирует только перечисленный минимум — сценарий «3+ файлов → strategy» пропадёт.

## Verdict

**CHALLENGE** — выбранный каркас (живой мэппинг + самосверка + упаковка без ослабления гейтов + тонкие профили) решает Why, но постановка не готова к реализации: хардкод Fable конфликтует с живым enum и с D3, а адресат выноса carve-out ревью молча угрожает ADR-0003.

Это не отказ от направления. Нет равноправной замены «профили vs не профили» или «упаковка vs оставить 54 КБ». Блокируют конкретные дыры в design/spec, без которых apply воспроизведёт исходный сбой и/или снимет disposition-пол.

## Gaps for design.md

1. **Исправить evidence-enum в `design.md` § Context.** Заменить список с `claude-fable-5-thinking-high` на фактический enum сборки (без Fable). Пометить, что Fable — *желаемый* слаг эскалации, а не подтверждённый член enum.
2. **implementation_invariant D1a ∩ D3 (предпочтительно перед развилкой).** В D1a и в `specs/subagent-model-mapping/spec.md`: передавать `claude-fable-5-thinking-high` **только если** слаг есть в описании `Task` этой сборки; иначе Primary обычного архитектора (`claude-opus-5-thinking-high`) + предупреждение; **не** family guessing; **не** Fable-as-fallback после сбоя Opus (ось D1a сохраняется). Сценарий «Рантайм свободен от мёртвых слагов» и сценарий «независимый разбор идёт на Fable» привести к одному контракту (условный, не безусловный MUST). Приёмка S1 — то же.
3. **Остаток ADR-0003 в always-apply.** D6 адресат «§ АВТО-ИСПРАВЛЕНИЕ → `review/SKILL.md`» сузить: skill — SSOT протокола `/review` / `/release-review`; always-apply `1c-agent-delegation.mdc` **сохраняет дословный** carve-out apply-reviewer (weak / design-prescribed / agreement-override → open + след, не авто-waive, не авто-fix). Это D6 (в), не опция. Добавить `## Blast Radius` (контракт apply-reviewer ↔ архив `review-quality-disposition` / ADR-0003). Proposal: либо явный MODIFIED `review-quality-disposition` с формулировкой «семантика не меняется, меняется только носитель», либо доказательство остатка — и тогда Modified по-прежнему пуст.
4. **Остаток KB CONTEXT.** Вынос в on-demand `knowledge-format.mdc` не детектирует диалоговый триггер «делегирование explorer/architect/trace». В always-apply delegation оставить однострочный якорь: при делегировании этих ролей — блок `## Existing Knowledge` по правилу в `knowledge-format.mdc` (cue + обязательство, не только cue).
5. **Переносимый минимум session-правил.** В список «дословно» D6 добавить TRIGGER/ACTION/BYPASS context-strategy (как в текущем `session-discipline.mdc` § Context Strategy) и persistence «протокол на каждом ходе». Иначе smoke S2 (3+ файлов) не из чего восстановить после разжалования `context-strategy-gate.mdc` (сейчас `alwaysApply: true`, без globs).
6. **Согласовать spec профилей.** В `chat-model-profiles`: профиль *чата* не копируется в бриф; MAY профиля *модели Primary субагента* может учитываться в intent-брифе без ослабления MUST NOT. Убрать прямое противоречие «не транслируется» vs сценарий opus5-брифа.
7. **ADR-0001.** Профили MUST NOT явно включить инварианты chat-facing: в чат не копировать имена субагентов, skill/compile, Schema, имена гейтов (`openspec/adrs/ADR-0001-chat-facing-vs-agent-facing.md`, `openspec/specs/chat-surface-clarity/spec.md`). Сейчас D5 перечисляет HALT `chat-output-budget`, но не границу chat-facing vs agent-facing. Строка D1a «разбор на самой дорогой модели» (без слага и без имени агента) этой границе соответствует — закрепить как эталон, не «идёт на Fable».
8. **Не объявлять Fable членом enum в tasks/приёмке**, пока сборка его не отдаёт. Исторические анти-примеры в `tool-name-guard.mdc` — единственное место мёртвых слагов (уже в spec).

## Architectural alternatives

Равноправная развилка **только** по носителю независимого разбора, *пока* Fable нет в enum. Ось «Fable не роль по умолчанию и не запас после сбоя Opus» не переоткрывается.

### Носитель независимого разбора постановки при отсутствии слага Fable в enum

**A. Тот же Primary, что у обычного архитектора (`claude-opus-5-thinking-high`):** независимый разбор и обычный design временно на одной модели; D3 соблюдён; дешевле. Trade-off: теряется разведение «постановка vs атака постановки» по модели.

**B. Primary `gpt-5.6-sol-medium` (есть в живом enum):** независимый разбор на другой модели, чем design/Opus 5; D3 соблюдён. Trade-off: это не «самая дорогая» модель из текста D1a; при появлении Fable в enum D1a п.1 снова включает Fable без смены оси.

Оба пути требуют gap 2 (не передавать отсутствующий слаг). Выбор A vs B — продуктовый, не workflow.

Упаковка carve-out: путь «целиком в `review/SKILL.md`» **не** равноправен пути «остаток в always-apply» — первый отменяет ADR-0003 в apply. Это gap 3, не развилка.

## Precedent / Blast Radius (аудит молчаливой отмены)

Change не содержит `Supersedes` и не содержит `## Blast Radius`. Архивных delta specs с теми же capability нет.

| Контракт | Архивный источник | Бизнес-эффект | Альтернативы | Обоснование |
|---|---|---|---|---|
| Apply-reviewer не авто-waive weak / design-prescribed; disposition только на `/review` | ADR-0003; `openspec/specs/review-quality-disposition/spec.md` Requirement «Apply-reviewer does not run disposition AskQuestion»; currently `1c-agent-delegation.mdc` § АВТО-ИСПРАВЛЕНИЕ (always-apply) | При реализации ЗНИ спорное качество кода могло бы тихо закрыться «как задумано» или авто-фикситься, без вопроса заказчику | Остаток carve-out в always-apply (gap 3) vs полный вынос в skill | D6 адресат без D6 (в) = молчаливая отмена. `review/SKILL.md` уже содержит disposition для `/review`, но **не** заменяет always-apply правило apply-контура |
| В чат — только продуктовые формулировки; slug агентов / skill / гейты — agent-facing | ADR-0001; `openspec/specs/chat-surface-clarity/spec.md` | Разработчик 1С снова видит внутренние имена в командах | Явный MUST NOT в профилях (gap 7); строка «самая дорогая модель» без слага | Слияние `conversational-discipline` + `orchestrator-as-navigator` в `chat-output-budget` само по себе не отменяет контракт, **если** HALT и thin-chat переезжают. Профили MAY «нарратив» без отсылки к ADR-0001 могут размыть границу. Не доказанная отмена, недозакрытый риск |
| Always-apply XML/BSL write guard, LINT, reviewer | текущие always-apply `1c-agent-delegation.mdc`, `bsl-write-guard.mdc`, compact XML | Оркестратор мог бы править XML/` .bsl` сам | Compact XML уже в delegation; D5 MUST NOT | Разжалование полного `1c-xml-write-guard.mdc` допустимо **при** сохранении compact. Слияние `bsl-write-guard` в delegation (включая JSDoc/шапка, apply/review, Mechanical) — не отмена, если три carve-out переезжают дословно (D6 это требует) |

Профили сами по себе аддитивны и не отменяют ADR, пока MUST NOT включает write-guard / reviewer / HALT. Угроза — не профили, а **упаковка носителя** apply-carve-out.

## Источники

- proposal.md — § Why (мёртвые слаги, 54 КБ, нет профилей); § What Changes (Fable как закрытая эскалация, D3, диета, профили); § Capabilities (Modified пуст); § Impact (риск consumer: «только упаковка»).
- design.md — § Context (ложный evidence-enum с Fable); D1, D1a, D3, D4, D5, D6 (в) vs адресаты выноса, D7–D10; Behavior Contract; Slices S1 приёмка Fable; Open Questions.
- specs/subagent-model-mapping/spec.md — мэппинг; самосверка; «нет мёртвых слагов»; безусловный Fable на независимом разборе; сбой Opus ≠ Fable.
- specs/always-apply-context-budget/spec.md — ≤ 34 КБ; разжалование (а)(б)(в); передача SSOT pipeline; диета reviewer.
- specs/chat-model-profiles/spec.md — пирамида vs «не транслируется в брифы».
- specs/delegation-safeguards/spec.md — Explore только для 1С; эскалация после двух неудач «в пределах guard».
- specs/rules-hygiene/spec.md — не источник конфликта Q1–Q3.
- ADR-0001 — `openspec/adrs/ADR-0001-chat-facing-vs-agent-facing.md`.
- ADR-0003 — `openspec/adrs/ADR-0003-review-quality-disposition.md`.
- `openspec/specs/review-quality-disposition/spec.md` — apply-reviewer scenarios.
- `openspec/specs/chat-surface-clarity/spec.md` — chat-facing canons.
- Код kit: `.cursor/rules/model-selection.mdc:19,31–33,43–47,63`; `.cursor/rules/architect-gate.mdc:97–98`; `.cursor/rules/1c-agent-delegation.mdc` § XML WRITE GUARD, § KB CONTEXT, § АВТО-ИСПРАВЛЕНИЕ; `.cursor/skills/review/SKILL.md` (disposition `/review`); frontmatter `alwaysApply: true` у `1c-xml-write-guard.mdc` (с globs), `command-skill-gate.mdc`, `command-session-persistence.mdc`, `context-strategy-gate.mdc`; `session-discipline.mdc` § Context Strategy; `knowledge-format.mdc` `alwaysApply: false`.
- Verified runtime fact (эта сессия): enum `Task.model` без `claude-fable-5-thinking-high` и без `claude-opus-4-8-thinking-high`.
