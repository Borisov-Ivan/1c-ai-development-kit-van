# Исследование: независимая критическая оценка качества в `/review` и `/release-review`

Дата: 2026-08-09  
Репозиторий: `c:\GitHub\1c-ai-development-kit-van`  
Тип: исследование процесса kit (не BSL продукта)

---

## 1. Свод (для заказчика)

Сейчас `/review` и `/release-review` — **одна команда-скилл** (`.cursor/skills/review/SKILL.md`) с флагом `release_mode`. Ревьюер умеет искать слабую реализацию (Phase 0: сложность/шум поверхности, «design-prescribed» антипаттерн, запрет dismiss «термин из design»), но одновременно есть **каналы «зелёного света» от ЗНИ**: блок `## Architectural Context` сформулирован как «соответствие design», а Evidence-override типа `spec-explicit-tolerance` / заполненная `## Hardcode Justification` переводят default MUST_FIX в OK/VERIFIED_OK **без отдельного подтверждения заказчика**, что «слабо, но так задумано».

Уже есть зачатки нужной механики:

- после отчёта `/review` спрашивает «устранить?» (шаг 5) — но только для MUST_FIX/REFACTOR, не для «слабо принято по design»;
- waive для шума поверхности (DISPROPORTIONATE_SURFACE);
- `Review disposition required` + `/opsx:extend --from-review` с disposition `accepted|rejected|deferred` — когда фикс **противоречит** design, а не когда design **прикрывает** слабый код.

**Пробел:** нет единого слоя «weak → as-designed (подтвердил пользователь) | queue-fix», общего для операционного и предрелизного ревью. Apply-reviewer вообще **авто-чинит** замечания без этой развилки.

Стык с explain — см. соседнее исследование (не раскрывается здесь).

---

## 2. Текущее поведение `/review` vs `/release-review`

### 2.1 Архитектура входа

| Элемент | `/review` | `/release-review` |
|---------|-----------|-------------------|
| Команда | `.cursor/commands/review.md` | `.cursor/commands/release-review.md` |
| Скилл | тот же `.cursor/skills/review/SKILL.md` | тот же |
| Флаг | `release_mode=false` | `release_mode=true` |
| Шаблон промпта | `1c-agent-patterns/reviewer.md` «Reviewer (ревью кода)» | тот же файл «Reviewer (предрелиз)» + `mode=prerelease` |
| Агент | `onec-code-reviewer` (`prompt_contract_version: 3`) | тот же |
| Памятка заказчика | `.cursor/docs/review-guide.md` | та же |

### 2.2 Карта потока (общий скилл)

```
Шаг 0  → release_mode / full_review / review_mode
Шаг 1  → resolve scope (+ 1.3a/1.3c только release)
Шаг 1.4 → light-review triage (ТОЛЬКО /review, не release, не --full)
Шаг 1.5 → Review Boundaries (diff-focused)
Шаг 1.6–1.10 → evidence: whitelist, linter, naming, comment hygiene
Шаг 2   → бриф + Prior Findings + Architectural Context + Resolved Contracts
Шаг 3   → Task onec-code-reviewer (+ Tier 2 explorer только release)
Шаг 3.5 → Investigation Loop (explorer ↔ reviewer, max 3)
Шаг 4   → отчёт main + reasoning appendix
Шаг 5   → AskQuestion: устранить MUST_FIX / упростить REFACTOR?
Шаг 6   → writer / simplifier → повторный reviewer (max 2)
Шаг 7   → итог; ARCH → architect; scope/design conflict → extend --from-review
```

### 2.3 Различия режимов (факты из guide + skill)

Источник: `.cursor/docs/review-guide.md` «Три уровня» / «Отличия»; skill шаг 0 и 1.0.

| Аспект | `/review` | `/release-review` |
|--------|-----------|-------------------|
| Scope default | git diff / файл / change | все `.bsl` cfe **или** change-scoped Tier 1 + Tier 2 на всё расширение |
| Light-review | да (тривиальный diff) | нет |
| `mode=prerelease` | нет | да |
| Эскалация severity (AP-каталог) | нет | да (в т.ч. HIGH→CRITICAL где указано) |
| Category 12 Release Readiness | нет | да (`reviewer-checks.md` §12 — опечатки/encoding в user strings; stub уже always) |
| Tier 2 explorer | нет | да (архитектура всего расширения) |
| Scope Preview | редко | при change-scoped + ambiguous/empty target |
| Follow-up extend | опционально | при ARCH / MUST_FIX scope — рекомендовать `/opsx:extend --from-review` |
| Whitelist / mandatory control | оба + apply-reviewer | оба |

### 2.4 Отличие apply-reviewer vs full `/review` vs prerelease

| Измерение | Apply-reviewer (`/opsx:apply`) | Full `/review` | `/release-review` |
|-----------|--------------------------------|----------------|-------------------|
| Когда | после каждой BSL-задачи writer pipeline | по запросу (diff/модуль/change) | перед выкладкой |
| Scope | файлы текущей задачи | по резолву 1.2 | extension / change+Tier2 |
| `mode=prerelease` | нет | нет | да |
| Авто-fix | **да**: `1c-agent-delegation.mdc` § АВТО-ИСПРАВЛЕНИЕ — все CODE critical/high/medium/low → writer → reviewer, max 2 | **нет**: шаг 5 AskQuestion | как `/review` шаг 5 (тот же скилл) |
| Writer без apply | запрещён (кроме Light/Mechanical) | разрешён после подтверждения пользователя | то же |
| Блокировка закрытия задачи | MUST_FIX блокирует закрытие apply-задачи | отчёт + опциональный fix-loop | отчёт + fix / extend |
| Architectural Context | обычно есть (active change) | если change в scope | часто есть |
| Light-review | нет (полный pipeline) | возможен | нет |

**Вывод для заказчика:** «зелёная галочка apply» ≠ «код хороший для релиза». Apply-reviewer не эскалирует severity, не гоняет Category 12 / Tier 2 и **не спрашивает** «слабо, но так задумано?».

---

## 3. Где договорённости перекрывают качество

Ниже — якоря, где agreement (design/ЗНИ/ТЗ) может **снять или смягчить** finding, либо сформулировать задачу ревьюера как conformance, а не critique. Рядом — уже существующие противовесы.

### 3.1 Каналы перекрытия (agreement → OK / VERIFIED_OK / «соответствует»)

#### A. `## Architectural Context` — формулировка «соответствие»

| Якорь | Формулировка |
|-------|--------------|
| `.cursor/skills/review/SKILL.md` § 2.2 | «прочитать `design.md` и `reports/architecture-*.md`. Передать … `## Architectural Context`» |
| `.cursor/skills/1c-agent-patterns/reviewer.md` (оба шаблона + bug-fix) | «Оценивать решения в коде **на соответствие** контексту» / «на соответствие этому контексту» |

**Эффект:** ревьюер получает design как эталон «правильности решения». Слабая, но согласованная с Chosen реализация легче проходит как «соответствует Architectural Context», чем как независимый QUALITY finding. Противовес в том же чеклисте (design-prescribed) **не** отражён в тексте этой строки шаблона.

#### B. Evidence-override `spec-explicit-tolerance` (design/ТЗ снимает default MUST_FIX)

| Якорь | Формулировка |
|-------|--------------|
| `.cursor/agents/onec-code-reviewer.md` Phase 2.5 Default 1 | Override → VERIFIED_OK/OK: тип `spec-explicit-tolerance` — «ТЗ/design.md явно допускает тихое продолжение» |
| тот же файл, Default 2 (AP-032) | Override → OK: `spec-explicit-tolerance` + механизм восстановления |
| `.cursor/skills/1c-agent-patterns/reviewer.md` HIDDEN_PARTIAL_RESULT_GATE | «Исключение: логика приложения явно предусматривает тихий пропуск (**задокументировано в design/ТЗ**)» |

**Эффект:** слабый/рискованный паттерн (тихий fallback, частичная запись) может стать VERIFIED_OK **без UX-слоя «пользователь подтвердил as-designed»** — достаточно цитаты из design в Evidence. Оркестратор шаг 5 про такие VERIFIED_OK **не спрашивает** (шаг 5: только MUST_FIX|REFACTOR).

#### C. `## Hardcode Justification` в design → AP-055 OK

| Якорь | Формулировка |
|-------|--------------|
| `.cursor/agents/onec-code-reviewer.md` Phase 2.6 | литерал-фильтр + заполненная Hardcode Justification → `OK` или `VERIFIED_OK` |
| Evidence override type | `design-hardcode-justification` |
| `.cursor/rules/bsl-antipatterns.mdc` AP-055 | remediation: делегировать **или** заполнить секцию в design |
| `.cursor/docs/standard/reviewer-checks.md` Phase 2.6 | то же зеркало |

**Эффект:** архитектурно спорный allow-list имён в хуке закрывается **документом ЗНИ**, а не повторной критикой качества на `/review`/`/release-review`. Identity Filter Gate на этапе architect жёстче; на этапе reviewer заполненная секция = зелёный свет.

#### D. AP-042: design/tasks как допуск debug-ЖР

| Якорь | Формулировка |
|-------|--------------|
| `.cursor/agents/onec-code-reviewer.md` RELEASE-HYGIENE AP-042 | читать `tasks.md` и `design.md`; если имя события/процедуры **есть** как подстрока — не flag; иначе flag |

**Эффект:** «договорились в задачах» = разрешить отладочный ЖР в коде. Это осознанный whitelist, но снова agreement перекрывает release-hygiene без confirm as-designed.

#### E. Resolved Contracts из ЗНИ → AP-004 / снятие compensating-try

| Якорь | Формулировка |
|-------|--------------|
| `.cursor/agents/onec-code-reviewer.md` Phase 2.5 C п.6 | `resolved-fixed` + guard → AP-004; `resolved-dynamic` + минимальная проверка → OK |
| skill шаг 3.5 | повторный reviewer с `## Resolved Contracts` |

**Эффект:** корректный для контрактов механизм, но при ошибочном/поверхностном resolved-contract explorer может «закрыть» скепсис Phase 2.5. Не user-confirm.

#### F. Whitelist предрелиза (project.md) — exempt removal

| Якорь | Формулировка |
|-------|--------------|
| agent RELEASE-HYGIENE + skill 1.6 | whitelist exempt AP-040 **removal** (не AP-053/AP-054 на текст) |

**Эффект:** process-маркеры остаются в коде по проектной договорённости — ожидаемо; не путать с quality override, но это ещё один agreement-канал.

### 3.2 Противовесы (agreement НЕ должно зелить) — уже есть, но неполный UX

| Якорь | Что делает |
|-------|------------|
| `reviewer-checks.md` Category 11 + Phase 2 п.4 | «Design authority: design.md decisions do **NOT** exempt code from anti-pattern checks. Tag: `design-prescribed`» |
| `onec-code-reviewer.md` Phase 1c / Export Language | «`design term` / терминология ЗНИ — **INVALID dismiss**» для AP-031 |
| Phase 0 Q1 / Q1b | сложность/шум поверхности → DISPROPORTIONATE_* даже без AP-match |
| skill шаг 7.2b | MUST_FIX, противоречащий design → **не** writer; disposition через extend |
| skill шаг 5 + SURFACE | REFACTOR поверхности не закрыть без simplifier **или явного waive** |
| CRITICAL RULE 10 agent | запрет soft language; OPTIONAL есть в схеме Action, но «если не стоит — не включать» |

**Разрыв:** противовесы либо **жёстко флажат** (design-prescribed → MUST_FIX), либо **молча VERIFIED_OK по Evidence**, либо уводят в **extend disposition** только при *конфликте* с design. Нет среднего состояния: «реализация слабая / спорная, design это покрывает → спросить заказчика: as-designed или queue-fix».

### 3.3 Где ревьюер «зелит» на практике (паттерны отказа)

1. **Conformance-bias:** Architectural Context + Chosen → Status PASS при тяжёлом, но «по design» коде (Q1b не сработал / Elegance Score advisory).
2. **Evidence-shortcut:** одна фраза в design → `spec-explicit-tolerance` → VERIFIED_OK на compensating-try / AP-032 / hidden partial — без шага 5.
3. **Hardcode Justification as absolution:** AP-055 исчезает из MUST_FIX после секции в design, даже если секция формальная («временный список») — при том что architect-gate говорит, что «временный» не закрывает Identity Filter Gate; reviewer default при *заполненной* секции уже OK.
4. **Apply path:** замечание, которое в `/review` пользователь мог бы отвергнуть как «так задумано», в apply уходит в авто-writer и меняет код без развилки.
5. **OPTIONAL почти мёртв:** CRITICAL RULE 10 + «все замечания обязательны» → спорная слабость либо MUST_FIX, либо не попадает в отчёт; нет стабильного «WEAK» статуса.

---

## 4. Предложение: слой «weak / as-designed / queue-fix» (единый для обеих команд)

### 4.1 Принцип

**Один протокол disposition**, живёт в `review/SKILL.md` (шаги 4–5), вызывается и при `release_mode=false`, и при `true`. Команды `review.md` / `release-review.md` не дублируют логику — только выставляют `release_mode`.

Разделить две оси:

| Ось | Вопрос | Кто решает |
|-----|--------|------------|
| **Compliance** | нарушен ли стандарт / AP / контракт? | reviewer (как сейчас) |
| **Quality judgment** | реализация слабая / непропорциональная / agreement прикрывает риск? | reviewer помечает → **пользователь** as-designed \| queue-fix |

Design/ЗНИ остаются **context + Evidence**, но **не финальный verdикт quality** без явного as-designed.

### 4.2 Новое поле finding (или disposition-тег)

Добавить к Action-семантике (не ломая MUST_FIX/REFACTOR):

```
QualityFlag: none | weak
Disposition: open | as-designed | queue-fix   # выставляет оркестратор после AskQuestion
```

Правила эмиссии `QualityFlag: weak` (reviewer, оба режима):

1. Сработал override на agreement (`spec-explicit-tolerance`, `design-hardcode-justification`, HIDDEN_PARTIAL «по design», AP-042 «есть в tasks/design») **и** default без Evidence был бы MUST_FIX / HIGH+ — finding **не** исчезает: остаётся с Action `VERIFIED_OK` **или** отдельный twin-finding `WEAK_AS_DESIGNED_CANDIDATE` с QualityFlag=weak.
2. Phase 0 Q1/Q1b = yes, но пользователь/design утверждает «сложность оправдана доменом» — всё равно weak до confirm.
3. Tag `design-prescribed` — всегда weak + MUST_FIX (или ARCH), disposition не может быть as-designed без явного waive + запись в design/ADR.
4. Elegance Score «нужен рефакторинг» без AP — weak + REFACTOR (уже близко к SURFACE).

**Запрет:** молчаливый VERIFIED_OK только по цитате design без строки Disposition в отчёте оркестратора.

### 4.3 Единый UX после шага 4 (замена/расширение шага 5)

После сохранения отчёта оркестратор строит три корзины (одна карточка AskQuestion, оба режима):

| Корзина | Содержимое | Вопрос пользователю |
|---------|------------|---------------------|
| **A. Обязательный ремонт** | MUST_FIX CODE без QualityFlag / functional CRITICAL | Устранить сейчас? (как сейчас) |
| **B. Слабо / спорно** | QualityFlag=weak, design-prescribed, VERIFIED_OK-via-agreement, SURFACE | По каждому (или пакетом): **«так задумано»** / **«в очередь на исправление»** |
| **C. Упрощение** | REFACTOR без weak-оверрайда | Упростить? (+ waive для SURFACE — уже есть) |

**as-designed:**

- записать в main report секцию `## Disposition` (`finding-id → as-designed`, кто/когда, цитата Evidence);
- **не** передавать writer;
- при `release_mode` — as-designed **не** снимает Category 12 / эскалацию без отдельного waive на release-hygiene (политика: as-designed для functional risk ок с записью; для release-hygiene — только queue или правка).

**queue-fix:**

- единый артефакт очереди (см. §4.4), не два формата для review/release;
- CODE → шаг 6 writer/simplifier;
- ARCH / contradiction design → уже существующий путь `extend --from-review` (disposition accepted в extend = queue на уровень ЗНИ).

### 4.4 Единый артефакт очереди (без дублирования логики команд)

Один файл на прогон:

- с change: `openspec/changes/<id>/reports/review-queue-<scope-slug>-YYYY-MM-DD.md`
- без change: `temp/reports/review-queue-<scope-slug>-YYYY-MM-DD.md`

Формат (минимальный):

```markdown
## Review Queue
Source: /review | /release-review
Report: <path to main review-*.md>

| ID | Flag | Action | Disposition | Target |
|----|------|--------|-------------|--------|
| F1 | weak | MUST_FIX | queue-fix | writer |
| F2 | weak | VERIFIED_OK→was-override | as-designed | — |
| F3 | — | REFACTOR | queue-fix | simplifier |
| F4 | — | MUST_FIX | queue-fix | extend |
```

Шаг 6 читает **только** строки `Disposition=queue-fix`. Шаг 5 пишет Disposition. Команды review/release-review не содержат своей копии алгоритма.

Интеграция с уже существующим extend disposition (`accepted|rejected|deferred` в `openspec-extend-change`):  
- `queue-fix` + Type ARCHITECTURE / contradiction → handoff `--from-review` (accepted ≈ queue на уровень артефактов);  
- `as-designed` ≈ `rejected` рекомендации review **с обязательной записью причины** (не молчаливый dismiss).

### 4.5 Изменение контракта ревьюера (чтобы не «зелил»)

В `onec-code-reviewer.md` + шаблон `reviewer.md`:

1. Переписать Architectural Context:
   - было: «на соответствие контексту»;
   - станет: «контекст ЗНИ — для Intent/Contract Map и поиска **design-prescribed** / contradiction; **соответствие design ≠ PASS по качеству**; agreement-override → QualityFlag=weak + Evidence, не скрытый VERIFIED_OK».
2. Evidence override с типами `spec-explicit-tolerance` | `design-hardcode-justification`:
   - разрешён → Status finding = `WEAK_CANDIDATE` (или VERIFIED_OK + QualityFlag=weak);
   - **запрещён** финальный PASS ревью, пока оркестратор не проставит Disposition (оркестратор: если остались open weak — Status отчёта NEEDS_WORK / «ожидает disposition»).
3. Hardcode Justification: при заполненной секции **всё равно** weak, если ответы Identity Filter Gate формальны («временный список») — зеркало architect-gate.
4. Сохранить INVALID dismiss design term (AP-031) и design-prescribed — не ослаблять.

### 4.6 Apply-reviewer (явное отличие)

Apply **не** использует AskQuestion weak/as-designed (скорость цикла ЗНИ). Политика:

- MUST_FIX functional — авто-fix как сейчас;
- QualityFlag=weak / design-prescribed / SURFACE — **не** авто-waive: либо авто-fix в том же apply, либо оставить open и в handoff apply упомянуть «на `/review` или `/release-review` потребуется disposition» (одна строка в отчёте задачи), без дублирования полного UX.

Так сохраняется различие уровней из `review-guide.md`, не смешивая apply с предрелизом.

### 4.7 Что не делать

- Не плодить второй скилл «critical-review».
- Не дублировать шаг 5 в `release-review.md`.
- Не смешивать с explain/handoff (отдельный трек).

---

## 5. Что менять в каких артефактах kit (список, без правок в этом исследовании)

| Файл | Изменение |
|------|-----------|
| `.cursor/skills/review/SKILL.md` | §2.2 переформулировать Architectural Context; шаг 4 — секция Disposition + Status при open weak; шаг 5 — три корзины A/B/C + запись `review-queue-*.md`; шаг 6 — фильтр по queue-fix; шаг 0 — явное «слой disposition общий, release_mode не отключает» |
| `.cursor/commands/review.md` | 1 строка: после отчёта — disposition weak/as-designed/queue (ссылка на skill) |
| `.cursor/commands/release-review.md` | то же + политика: as-designed не снимает release-hygiene без отдельного waive |
| `.cursor/docs/review-guide.md` | таблица «три уровня» + абзац про weak/disposition; отличие apply (без AskQuestion) |
| `.cursor/skills/1c-agent-patterns/reviewer.md` | все 3 шаблона: текст Architectural Context; инструкция QualityFlag=weak при agreement-override; запрет silent VERIFIED_OK |
| `.cursor/agents/onec-code-reviewer.md` | REPORT FORMAT: QualityFlag; Phase 2.5/2.6 override → weak candidate; CRITICAL RULE про disposition; PRE-RELEASE MODE — weak не эскалируется в CRITICAL молча, но не скрывается |
| `.cursor/docs/standard/reviewer-checks.md` | Category 11 / Design authority: добавить «override → weak + user disposition»; Phase 2.6 — заполненная Hardcode Justification ≠ автоматический PASS качества |
| `.cursor/rules/1c-agent-delegation.mdc` | § АВТО-ИСПРАВЛЕНИЕ: carve-out для QualityFlag=weak / design-prescribed (не авто-waive; опционально не авто-fix без флага apply) |
| `.cursor/skills/openspec-extend-change/SKILL.md` | маппинг `as-designed`↔`rejected(with reason)`, `queue-fix`↔`accepted` для `--from-review` |
| `.cursor/rules/bsl-antipatterns.mdc` (AP-055 card hint) | remediation: Justification закрывает Identity Filter Gate на architect, на review остаётся weak до disposition |
| (опц.) `.cursor/docs/standard/reviewer-checks.md` §12 | при prerelease: open weak = блокер «disposition required» рядом с fix-before-release |

**Не трогать** (в первой итерации): light-review triage, Investigation Loop, Tier 2 explorer, Category 12 детект опечаток.

---

## 6. Риски и открытые вопросы

1. **Шум disposition:** каждый AP-042/whitelist-маркер как weak утомит заказчика → нужен порог: weak только для functional/architecture risk и agreement-override на HIGH+, не для каждого style MEDIUM.
2. **Двойная запись Disposition:** отчёт review + extend accepted/rejected — риск рассинхрона; нужен SSOT (queue-файл или только секция в main report).
3. **Apply vs review расхождение:** код «прошёл apply», на `/release-review` всплывает weak — ожидаемо по guide, но нужен UX «не регрессия процесса».
4. **Формальная Hardcode Justification:** кто проверяет качество ответов Identity Filter Gate на review — reviewer (субъективно) или только architect? Предложение: reviewer флажит weak при «временный список» / пустом плане N+1.
5. **VERIFIED_OK семантика:** ломать ли поле Action (writer не трогает VERIFIED_OK) vs вводить `WEAK_CANDIDATE` — предпочтительно не ломать writer contract: Action остаётся, QualityFlag ортогонален.
6. **PROMPT_CONTRACT_VERSION:** любое breaking поле в отчёте → bump `prompt_contract_version` / `expected_reviewer_prompt_contract_version` (сейчас 3).
7. **Открытый вопрос продукта:** должен ли as-designed на functional CRITICAL (напр. частичная запись) требовать ADR, а не только галочку в disposition?
8. **Открытый вопрос:** включать ли apply-reviewer в тот же queue-файл «накопительно по ЗНИ» для предрелиза?

---

## 7. Для оркестратора — буллеты доказательств с путями

- Единый скилл: `.cursor/commands/review.md` L19 (`release_mode=false`); `.cursor/commands/release-review.md` L10–24 (`release_mode=true`); skill шаг 0 таблица переменных.
- Три уровня контроля: `.cursor/docs/review-guide.md` L7–15, L55–66.
- Light-review только non-release: skill §1.4 L129–134.
- Tier 2 только release: skill §3.2 L402–410.
- Architectural Context = conformance wording: skill §2.2 L366–369; `1c-agent-patterns/reviewer.md` L43–44, L198–199, L238–239.
- Agreement override VERIFIED_OK: `onec-code-reviewer.md` Phase 2.5 L286–306 (`spec-explicit-tolerance`); Phase 2.6 L375–381 (`design-hardcode-justification`); HIDDEN_PARTIAL исключение в `reviewer.md` L122–123.
- Design НЕ exempt AP (противовес): `reviewer-checks.md` L203–205, L580; Phase 1c invalid dismiss design term: agent L238 / reviewer-checks L487–491.
- Phase 0 независимая критика сложности/поверхности: agent L223–224, L545.
- Post-review AskQuestion только MUST_FIX|REFACTOR: skill шаг 5 L485–498; SURFACE waive L492; VERIFIED_OK/OPTIONAL пропускают шаг 5.
- Scope/design conflict → extend disposition: skill §7.2b L569–580; extend skill disposition accepted/rejected/deferred (grep `--from-review` / disposition в `openspec-extend-change/SKILL.md`).
- Apply авто-fix всех CODE severity: `1c-agent-delegation.mdc` § АВТО-ИСПРАВЛЕНИЕ L94–96; `/review` writer только после confirm: тот же файл § APPLY GATE L32.
- Category 12 узкий (prerelease-only typos): `reviewer-checks.md` §12 L207–213; эскалация severity: agent PRE-RELEASE MODE L562–574.
- AP-042 design/tasks как допуск ЖР: agent L136.
- Шаблоны промптов prerelease vs normal: `1c-agent-patterns/reviewer.md` L9–156 vs L160–218 (`mode=prerelease`).

---

*Конец отчёта.*
