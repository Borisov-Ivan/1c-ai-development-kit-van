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
  - reports/quality-control-2026-08-09.md
  - reports/architecture-new-2026-08-09.md
confidence: high
open_questions_count: 2
readiness: not-ready
blocking_gaps: [C3-AP-042, C3-whitelist]
superseded_by: null
---

# Task Readiness — independent-review-disposition

## Контекст оценки

Kit meta-change: apply mode mechanical; правки markdown/skill/agent/docs/commands/rules в `.cursor/`. Продуктовый BSL не меняется. Формы/метаданные: `form_mode: n/a`.

Оценено по артефактам: `proposal.md`, `design.md`, `tasks.md`, `specs/review-quality-disposition/spec.md`; учтены QC Layer 2 (`reports/quality-control-2026-08-09.md`, verdict OK + SUGGESTION) и pre-screen Layer 5 (executability issues: none).

## Итоговый вердикт

**readiness: not-ready**

Срез S1 в целом хорошо декомпозирован (пути файлов, корзины A/B/C, bump контракта, accept black-box), покрытие scenarios spec полное, User Task Contract соблюдён. Блокируют as-is apply **два незакрытых решения** из `design.md` § «Открытые вопросы» (п. 2 и п. 3): без Chosen исполнитель вынужден угадывать поведение AP-042 и состав whitelist silent VERIFIED_OK — высок риск возврата на уточнение или переделки контракта ревьюера после первого прогона.

П. 1 (порог severity) и п. 4 (queue из apply) **не** блокируют: п. 1 имеет рекомендацию explore + якорь в spec Scenario; п. 4 явно out of MVP.

---

## Критерии

### 1. Реализуемость задач — GAP (частичный; усиливается C3)

| Задача | Вердикт | Обоснование |
|--------|---------|-------------|
| S1.1 | OK* | Файл `onec-code-reviewer.md`, поля из D2, Design authority, bump 3→4 — ясно. *Содержимое правил weak/whitelist зависит от C3.* |
| S1.2 | OK | «Три шаблона» подтверждены в `1c-agent-patterns/reviewer.md` (обычный / prerelease / bug fix); framing из D7 + D2. |
| S1.3 | OK* | Файл и Phase 2.5/2.6 указаны; алгоритм disposition из D2–D3. *AP-042 fork (C3) влияет на формулировку Design authority vs hygiene.* |
| S1.4 | OK | Статическая сверка `expected_reviewer_prompt_contract_version` ↔ agent — ALLOW-agent, путь известен. |
| S1.5 | OK | Skill, шаг 2.2, корзины A/B/C (D3), фильтр шага 6, общий протокол `release_mode` — достаточно для правки. |
| S1.6 | OK (с SUGGESTION) | Формат и опц. `review-queue-*.md` заданы в D3; путь файла в тексте задачи не назван явно (QC SUGGESTION) — из контекста группы «Оркестратор disposition» + S1.5 очевидно `review/SKILL.md`. Не блокер. |
| S1.7 | OK | Два command-файла; D4 для release-hygiene. |
| S1.8 | OK | `review-guide.md` + сценарий из Goals / Customer-visible guidance. |
| S1.9 | OK | Carve-out в delegation; D5 + spec Apply scenarios. «или» в D5 не вилка для исполнителя: non-weak MUST_FIX → авто-fix; weak → open + след (оба сценария spec). |
| S1.10 | OK | Маппинг D6; файл extend skill указан. |
| S1.11 | GAP | Grep-проверка ясна, но «whitelist VERIFIED_OK без disposition перечислен» требует **состава списка**, который design оставляет открытым (п. 3) — см. C3. |

**Итог C1:** большинство задач исполнимы; S1.11 и содержательная часть S1.1/S1.3 не закрыты без Chosen по whitelist/AP-042 → **GAP**.

### 2. Реализуемость форм и метаданных — OK / n/a

`form_mode: n/a`; маркеров ручной конфигурации нет; продуктовый cf/cfe вне scope. Для kit meta-change критерий не применяется — **OK (n/a)**.

### 3. Разрешённость решений — GAP

**Закрытые оси (OK):** D1–D7 (две оси Compliance/Quality, поля finding, корзины UX, prerelease hygiene, apply без AskQuestion disposition, маппинг extend, wording Architectural Context); bump 3→4; defer опционален в корзине B.

**Открытые вопросы design — оценка для as-is apply:**

| # | Вопрос | Вердикт | Почему |
|---|--------|---------|--------|
| 1 | Порог weak: HIGH+ vs шире | **не GAP** | Рекомендация explore в том же § + Scenario «Design endorses weak pattern» (MUST_FIX/HIGH+). Исполнитель берёт HIGH+ ∪ agreement-override из D2 без возврата к заказчику. |
| 2 | AP-042: flag+disposition **или** hygiene-исключение | **GAP (блокер)** | Две равноправные ветки с разным наблюдаемым поведением. AP-042 — release-hygiene (substring в tasks/design сейчас снимает finding). Chosen не зафиксирован в Decisions; пересекается с D4 (as-designed не снимает Category 12). Без решения S1.1/S1.3 пишут разные правила. |
| 3 | Узкий whitelist VERIFIED_OK без disposition | **GAP (блокер)** | Spec MUST: silent VERIFIED_OK только вне «явно перечисленного» whitelist. OQ3 даёт кандидатов (`documented-protocol-key`, platform-documented, resolved-dynamic), но не Chosen-список. S1.11 требует перечисления — состав не определён → риск расхождения agent vs skill vs checks. |
| 4 | Накопительный queue из apply | **не GAP** | Явно later / out of MVP; S1.6 опциональный queue-файл только для review-контура — достаточно. |

Прочие «или»/«/» в tasks/spec (as-designed / queue-fix; writer или extend; эквивалент weak) — продуктовые корзины UX или маршрутизация по типу finding, не неразрешённые развилки реализации.

### 4. Полнота покрытия — OK

Все 11 Scenario из `specs/review-quality-disposition/spec.md` покрыты Primary / S1.<M> / optional accept (согласовано с QC Layer 2). Requirements → задачи:

| Requirement | Задачи |
|-------------|--------|
| Agreement does not silently close… | S1.1–S1.3, Primary |
| Architectural Context is intent… | S1.2, S1.5 |
| Unified disposition UX… | S1.5–S1.7, Primary |
| Prerelease hygiene not waived… | S1.7 |
| Customer-visible guidance | S1.8 |
| Apply-reviewer does not run disposition AskQuestion | S1.9 |

Пробела «requirement без задачи» нет. (Метаданные «Связь со spec» не перечисляют все имена Scenario — SUGGESTION QC, не дыра покрытия.)

### 5. Согласованность — OK (с замечанием)

- **tasks ↔ design Decisions:** согласованы (поля, корзины, bump, apply carve-out, extend mapping).
- **Migration Plan «S1→S2→S3» vs один срез S1:** терминологический рассинхрон (волны групп 1–3 названы S2/S3). `## Slices` и `tasks.md` — один срез; QC SUGGESTION, не missing slices. `architecture-new-2026-08-09.md` повторяет S1→S2→S3 — не меняет apply-порядок по tasks.
- **Противоречий tasks↔design по поведению нет**, кроме незакрытых OQ (учтены в C3).

**Итог C5: OK** — apply идёт по `tasks.md` (S1.1→S1.11); ложная декомпозиция на отдельные slice-gates S2/S3 не следует из tasks.

### 6. Связность и порядок задач — OK

Порядок: группа 1 (контракт ревьюера) → 2 (skill/commands) → 3 (guide/стыки/verify) логичен; S1.4 после bump в S1.1; S1.11 финальная статическая верификация. Один `S1.accept` + `<!-- slice-gate -->`. Зависимостей между срезами нет. Замечаний Layer 5 pre-screen по executability нет.

### 7. Архитектурная эстетика (процесс kit) — OK

Ортогональный QualityFlag/Disposition без ломки Action writer-контракта; один протокол ordinary/prerelease; apply без AskQuestion disposition; семантики extend разведены маппингом — минимально инвазивно для kit. Breaking bump версии контракта осознан. Избыточных сущностей сверх D1–D7 нет.

### 8. User Task Contract / Precedent Coherence

**User Task Contract — OK:** в S1.1–S1.11 нет user runtime-spike / DENY-маркеров; S1.4/S1.11 — agent verification; runtime black-box приёмка только в `S1.accept` (kit `/review`) — допустимо.

**Precedent Coherence — OK (n/a evidence):** Cross-Archive Context / KB в промпт не передавались; capability новая (`openspec/specs/` пуст для этой области). Конфликта с архивным контрактом по артефактам change не видно. Blast Radius не требуется (нет revoke прецедента).

---

## Сводка OK / GAP

| # | Критерий | Вердикт |
|---|----------|---------|
| 1 | Реализуемость задач | **GAP** |
| 2 | Формы и метаданные | **OK (n/a)** |
| 3 | Разрешённость решений | **GAP** |
| 4 | Полнота покрытия | **OK** |
| 5 | Согласованность | **OK** |
| 6 | Связность и порядок | **OK** |
| 7 | Архитектурная эстетика | **OK** |
| 8 | User Task Contract (+ precedent) | **OK** |

**readiness: not-ready** — блокирующие GAP: C3 (и производный C1 на S1.11 / содержимое S1.1–S1.3).

---

## Gaps (закрыть до apply)

### C3-AP-042 (блокер)

В `design.md` § Decisions (или закрытие OQ2) зафиксировать Chosen:

- **A.** AP-042 при «есть в постановке» → QualityFlag weak / needs-confirm + disposition (с учётом D4: as-designed ≠ waive Category 12), **или**
- **B.** оставить hygiene-исключение (substring в tasks/design снимает finding без disposition).

Без Chosen не править S1.1/S1.3 as-is.

### C3-whitelist (блокер)

В Decisions / D2 явно перечислить whitelist Evidence-типов, для которых silent VERIFIED_OK/OK **без** disposition допустим (кандидаты OQ3 + сверка с `reviewer-checks.md` Evidence override). Тогда S1.11 становится проверяемым критерием, а не invent-list.

### Не блокируют (можно не трогать до apply)

- OQ1 — принять рекомендацию HIGH+ ∪ agreement-override (уже в design/spec).
- OQ4 — out of MVP.
- Migration Plan naming S2/S3 → волны/группы (QC SUGGESTION).
- S1.6: добавить явный путь `review/SKILL.md` (QC SUGGESTION).

---

## Рекомендация оркестратору

До `/opsx:apply`: закрыть OQ2 и OQ3 через `/opsx:extend` (правка design Decisions + при необходимости одна строка в tasks S1.1/S1.3/S1.11) **или** явное подтверждение заказчика Chosen A/B + список whitelist. После закрытия — повторный task-readiness не обязателен, если Chosen вписан в design и не ломает покрытие spec; иначе короткий re-check C1/C3.

---

## Источники

- `openspec/changes/independent-review-disposition/proposal.md`
- `openspec/changes/independent-review-disposition/design.md` (§ Decisions D1–D7, § Открытые вопросы, § Migration Plan, § Slices)
- `openspec/changes/independent-review-disposition/tasks.md` (S1.1–S1.11, S1.accept, slice-gate)
- `openspec/changes/independent-review-disposition/specs/review-quality-disposition/spec.md` (11 Scenario)
- `openspec/changes/independent-review-disposition/reports/quality-control-2026-08-09.md`
- Kit fact-check: `.cursor/skills/1c-agent-patterns/reviewer.md` (3 шаблона), `.cursor/agents/onec-code-reviewer.md` / AP-042, `.cursor/rules/bsl-antipatterns.mdc` (AP-042 release-hygiene)
