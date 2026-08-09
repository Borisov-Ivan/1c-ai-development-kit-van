---
report_type: task-readiness
generated_at: 2026-08-09
agent: onec-code-architect
mode: task-readiness
scope:
  change: independent-review-disposition
  slices: [S1]
  files:
    - .cursor/agents/onec-code-reviewer.md
    - .cursor/skills/1c-agent-patterns/reviewer.md
    - .cursor/docs/standard/reviewer-checks.md
    - .cursor/skills/review/SKILL.md
    - .cursor/commands/review.md
    - .cursor/commands/release-review.md
    - .cursor/docs/review-guide.md
    - .cursor/rules/1c-agent-delegation.mdc
    - .cursor/skills/openspec-extend-change/SKILL.md
  modules: []
  capabilities: [review-quality-disposition]
related_reports:
  - reports/architecture-task-readiness-2026-08-09.md
  - reports/quality-control-2026-08-09.md
  - reports/architecture-new-2026-08-09.md
confidence: high
open_questions_count: 2
readiness: not-ready
blocking_gaps: [C3-AP-042, C3-whitelist]
superseded_by: null
---

# Task Readiness — independent-review-disposition (re-check)

## Контекст оценки

Kit meta-change: apply mode mechanical; правки markdown/skill/agent/docs/commands/rules в `.cursor/`. Продуктовый BSL не меняется. `form_mode: n/a`. Маркеров ручной конфигурации нет.

Оценено as-is по: `proposal.md`, `design.md`, `tasks.md`, `specs/review-quality-disposition/spec.md`. Учтены замечания mechanical pre-screen (покрытие scenario anti-pattern, Migration S2/S3 vs один срез, открытые вопросы 1–4, отсутствие `openspec/project.md`). Executability: целевые kit-файлы существуют. Это независимый повторный прогон; предыдущий отчёт `architecture-task-readiness-2026-08-09.md` не использовался как источник истины.

### Вердикт

**НЕ ГОТОВО**

Срез единственный, задачи S1.1–S1.11 и приёмка S1.accept в целом исполнимы по путям и порядку. Блокируют as-is реализацию **два незакрытых решения** в `design.md` § «Открытые вопросы» (п. 2 AP-042 и п. 3 whitelist silent VERIFIED_OK): без Chosen исполнитель угадывает наблюдаемое поведение контракта ревьюера → риск возврата на уточнение или переделки после первого прогона.

П. 1 (порог severity) и п. 4 (queue из apply) **не** блокируют S1.1–S1.11.

---

## Оценка по критериям

| # | Критерий | Вердикт | Обоснование |
|---|----------|---------|-------------|
| 1 | Реализуемость кодовых задач (kit) | **GAP** | Пути и объём S1.1–S1.10 ясны; содержательные правила weak/whitelist в S1.1/S1.3/S1.11 зависят от незакрытых п. 2–3 (см. критерий 3). |
| 2 | Реализуемость форм и метаданных | **OK** | `form_mode: n/a`; cf/cfe вне scope; маркеров ручной конфигурации нет. |
| 3 | Разрешённость решений | **GAP** | D1–D7 закрыты; OQ2 и OQ3 — две равноправные ветки / не Chosen-список → блокер apply. |
| 4 | Полнота покрытия | **OK** | Все requirements и 11 scenarios покрыты задачами / Primary / optional accept; anti-pattern — через S1.1/S1.3. |
| 5 | Согласованность | **OK** | tasks↔Decisions согласованы; Migration «S1→S2→S3» = волны групп внутри одного среза, не missing slices. |
| 6 | Связность кода и порядок задач | **OK** | S1.1→S1.11 логичен; ровно один S1.accept; один slice-gate; зависимости между срезами нет. |
| 7 | Архитектурная эстетика | **OK** | Ортогональный QualityFlag/Disposition, один протокол ordinary/prerelease, apply без AskQuestion disposition — без лишних сущностей. |
| 8 | User Task Contract (+ precedent) | **OK** | Runtime-spike в S1.1–S1.11 нет; black-box приёмка только в S1.accept. Precedent: новая capability, revoke/Blast Radius не требуются. |

---

## Детали по критериям

### 1. Реализуемость кодовых задач — GAP

| Задача | Вердикт | Обоснование |
|--------|---------|-------------|
| S1.1 | OK* | Файл агента, поля D2, Design authority, bump 3→4. *Текст правил AP-042 и whitelist зависит от C3.* |
| S1.2 | OK | Три шаблона в `1c-agent-patterns/reviewer.md` (обычный / предрелиз / bug fix); framing D7 + эмит weak при agreement-override (D2). |
| S1.3 | OK* | `reviewer-checks.md`, Phase 2.5/2.6, связка Design authority / `design-prescribed`. *Формулировка AP-042 vs hygiene — C3.* |
| S1.4 | OK | Статическая сверка `expected_reviewer_prompt_contract_version` ↔ агент; сейчас оба = 3 — цель bump ясна. |
| S1.5 | OK | Skill: шаг 2.2, корзины A/B/C (D3), фильтр шага 6, общий протокол `release_mode`. |
| S1.6 | OK | Формат секции Disposition + опц. `review-queue-*.md` в D3; целевой файл из группы «Оркестратор disposition» — `review/SKILL.md` (путь в тексте задачи не назван — не блокер). |
| S1.7 | OK | `review.md` + `release-review.md`; D4 для release-hygiene. |
| S1.8 | OK | `review-guide.md` + Customer-visible guidance. |
| S1.9 | OK | Carve-out в `1c-agent-delegation.mdc`; D5: non-weak MUST_FIX → авто-fix; weak → open + след (оба сценария spec). |
| S1.10 | OK | Маппинг D6 в `openspec-extend-change/SKILL.md`. |
| S1.11 | GAP | Grep-проверка ясна, но «whitelist VERIFIED_OK без disposition перечислен» требует **состава списка**, который design оставляет открытым (п. 3). |

**Итог:** большинство задач исполнимы по файлам; S1.11 и содержательная часть S1.1/S1.3 не закрыты без Chosen → **GAP**.

### 2. Формы и метаданные — OK (n/a)

Явно n/a для kit meta-change. Отсутствие `openspec/project.md` не блокирует: нет делегирования BSL writer и нет путей cf/cfe в scope.

### 3. Разрешённость решений — GAP

**Закрытые оси (OK):** D1–D7; bump 3→4; defer опционален в корзине B; «или» в UX (as-designed / queue-fix) и маршрутизация writer|extend — продуктовые корзины, не вилки реализации.

| # | Вопрос design | Вердикт для as-is | Почему |
|---|---------------|-------------------|--------|
| 1 | Порог weak: HIGH+ vs шире | не GAP | В том же § есть рекомендация explore + Scenario «Design endorses weak pattern» (MUST_FIX/HIGH+). Исполнитель берёт HIGH+ ∪ agreement-override из D2. |
| 2 | AP-042: flag+disposition **или** hygiene-исключение | **GAP** | Две равноправные ветки. Сейчас агент: substring в tasks/design снимает AP-042. D4: as-designed ≠ waive Category 12. Chosen не в Decisions → S1.1/S1.3 пишут разные правила. |
| 3 | Узкий whitelist VERIFIED_OK без disposition | **GAP** | Spec MUST: silent VERIFIED_OK только для явно перечисленного whitelist. OQ3 даёт кандидатов (`documented-protocol-key`, platform-documented, resolved-dynamic), но не Chosen. S1.11 требует перечисления. D2 закрывает agreement-override → weak, но не состав «тихих» Evidence-типов. |
| 4 | Накопительный queue из apply | не GAP | Явно later / out of MVP; S1.6 опционален для review-контура. |

### 4. Полнота покрытия — OK

| Requirement | Задачи / приёмка |
|-------------|------------------|
| Agreement does not silently close… | S1.1–S1.3, Primary; Scenario «Design-prescribed anti-pattern» — S1.1 (tag) + S1.3 (Design authority), даже если имя scenario не в «Связь со spec» |
| Architectural Context is intent… | S1.2, S1.5 |
| Unified disposition UX… | S1.5–S1.7, Primary |
| Prerelease hygiene not waived… | S1.7 (+ D4) |
| Customer-visible guidance | S1.8 |
| Apply-reviewer does not run disposition AskQuestion | S1.9 |

Дыры «requirement без задачи» нет. Неполное перечисление имён scenario в metadata tasks — замечание гигиены, не gap покрытия.

### 5. Согласованность — OK (с замечанием)

- tasks ↔ design Decisions: согласованы (поля, корзины, bump, apply carve-out, extend mapping).
- Migration Plan «S1→S2→S3» vs `## Slices` только S1: волны = группы задач 1→2→3 внутри одного среза; отдельного slice-gate для «S2/S3» в tasks нет. Apply-порядок = S1.1→S1.11. Не GAP.
- Противоречий поведения tasks↔design нет, кроме незакрытых OQ (критерий 3).

### 6. Связность и порядок — OK

Группа 1 (контракт) → 2 (skill/commands) → 3 (guide/стыки/verify); S1.4 после bump; S1.11 финальная статика. Один `S1.accept`, один `<!-- slice-gate -->`. Executability issues по путям: none.

### 7. Архитектурная эстетика — OK

Минимальная инвазия в kit: две оси без ломки Action writer; один skill-протокол; breaking bump осознан. Избыточных сущностей сверх D1–D7 нет. Design smells, блокирующие apply, не найдены.

### 8. User Task Contract / Precedent Coherence — OK

- **UTC:** S1.1–S1.11 — agent/mechanical правки kit; нет user runtime-spike / DENY в номерах задач. Runtime black-box только в `S1.accept` (kit `/review`) — допустимо.
- **Precedent:** Cross-Archive / KB в промпт не передавались; capability новая. Конфликта revoke с архивным контрактом по артефактам change не видно; Blast Radius не требуется.

---

## Пробелы (блокирующие)

### C3-AP-042

- **Артефакт:** `design.md` § «Открытые вопросы» п. 2 (и отсутствие Chosen в § Decisions).
- **Что отсутствует:** одно выбранное поведение для AP-042 при «есть в постановке».
- **Рекомендация:** закрыть до apply (правка design + при необходимости одна строка в S1.1/S1.3).

**Сниппет для `design.md` § Decisions (выбрать одну ветку и вставить):**

```markdown
### D8. AP-042 и disposition (закрытие OQ2)

**Chosen:** при наличии подстроки события/процедуры в tasks/design активного change AP-042 **не** silent-закрывается как «просто есть в постановке».
Finding остаётся (QualityFlag=weak / needs-confirm или отдельный release-hygiene finding); as-designed по D4 **не** снимает Category 12 / release-hygiene без отдельного waive.

*(Альтернатива, если заказчик явно выберет B: оставить текущее hygiene-исключение substring→без finding; тогда D8 = «AP-042 вне disposition UX, только substring-gate как сейчас» — записать Chosen B одной фразой.)*
```

### C3-whitelist

- **Артефакт:** `design.md` § «Открытые вопросы» п. 3; зависит S1.11 / текст S1.1.
- **Что отсутствует:** Chosen-список Evidence-типов, для которых silent VERIFIED_OK/OK **без** disposition допустим.
- **Рекомендация:** зафиксировать список в D2/D9; тогда S1.11 проверяем grep’ом, а не invent-list.

**Сниппет (кандидаты из OQ3 + согласование с текущими Evidence-типами агента):**

```markdown
### D9. Whitelist silent VERIFIED_OK без disposition (закрытие OQ3)

Silent VERIFIED_OK/OK **без** QualityFlag weak / needs-confirm допускается **только** для Evidence-типов:
- `documented-optional-contract` / `documented-protocol-key` (явный опциональный контракт API/протокола)
- `platform-documented-behavior`
- `resolved-contract:dynamic` (Resolved Contracts, Contract:dynamic, без жизнеспособных альтернатив)
- `historical-verified` (если уже в контракте агента)

**Не** в whitelist (→ weak / needs-confirm): `spec-explicit-tolerance`, `design-hardcode-justification`, HIDDEN_PARTIAL «по design», формальная Hardcode Justification без иных Evidence.
```

---

## Не блокируют (можно не править до apply)

- OQ1 — принять HIGH+ ∪ agreement-override.
- OQ4 — out of MVP.
- Migration naming S2/S3 → волны/группы (гигиена формулировок).
- S1.6: явный путь `review/SKILL.md` в тексте задачи (SUGGESTION).
- Metadata «Связь со spec»: дописать имя Scenario «Design-prescribed anti-pattern» (SUGGESTION; покрытие уже есть).

---

## Рекомендация оркестратору

До `/opsx:apply`: закрыть OQ2 и OQ3 (Chosen в design Decisions; при необходимости одна строка в S1.1/S1.3/S1.11) через подтверждение заказчика или `/opsx:extend`. После вписывания Chosen повторный полный task-readiness не обязателен, если покрытие spec не ломается; иначе короткий re-check критериев 1 и 3.

---

## Источники

- `openspec/changes/independent-review-disposition/proposal.md`
- `openspec/changes/independent-review-disposition/design.md` (§ Decisions D1–D7, § Открытые вопросы, § Migration Plan, § Slices)
- `openspec/changes/independent-review-disposition/tasks.md` (S1.1–S1.11, S1.accept, slice-gate)
- `openspec/changes/independent-review-disposition/specs/review-quality-disposition/spec.md` (11 Scenario)
- Kit fact-check: существование целевых файлов; `prompt_contract_version: 3` / `expected_reviewer_prompt_contract_version: 3`; три шаблона в `reviewer.md`; текущее правило AP-042 substring в `onec-code-reviewer.md` / `bsl-antipatterns.mdc`
