## Context

`/review` и `/release-review` делят один skill (`.cursor/skills/review/SKILL.md`) и агента `onec-code-reviewer`. Design ЗНИ попадает в промпт как `## Architectural Context` с framing «оценивать на соответствие». Evidence-override (`spec-explicit-tolerance`, `design-hardcode-justification`, AP-042 «есть в постановке») переводят default MUST_FIX в VERIFIED_OK/OK без подтверждения заказчика. В `reviewer-checks.md` есть Design authority / tag `design-prescribed`, но в системном промпте агента и шаблонах `reviewer.md` это не проведено. Шаг 5 оркестратора спрашивает только про устранение MUST_FIX/REFACTOR.

Источники: `temp/reports/exploration-2026-08-09-critical-review-quality.md`, `temp/reports/exploration-2026-08-09-review-critical-quality-layer.md`.

## Goals / Non-Goals

**Goals:**

1. Независимое качество: слабая реализация флажится даже при endorse design.
2. UX disposition: as-designed | queue-fix (| defer) — единый для ordinary и prerelease.
3. Запись disposition в main report (+ опционально `review-queue-*.md`).
4. Памятка заказчика без жаргона движка.

**Non-Goals:**

- Handoff в `/opsx:explain` и охват в B-explain (отдельная ЗНИ).
- Полный adversarial audit постановки (это `/opsx:verify` Layer 4).
- AskQuestion weak/as-designed внутри apply-reviewer (скорость цикла apply).

## Existing Mechanisms

- Skill review шаги 4–7: отчёт → AskQuestion fix → writer/simplifier → extend `--from-review`.
- Extend disposition `accepted|rejected|deferred` при конфликте с design (другая семантика: смена постановки).
- Tag `design-prescribed` и Design authority в `reviewer-checks.md`.
- Phase 0 Q1/Q1b (сложность/шум поверхности), SURFACE waive.
- `prompt_contract_version: 3` у ревьюера.

## Design Rationale

Выбран **ортогональный QualityFlag / Disposition**, а не замена Action: writer-контракт (MUST_FIX/REFACTOR) сохраняется; agreement-override больше не даёт финальный PASS без disposition оркестратора. Один протокол в skill — команды review/release-review только выставляют `release_mode`.

Аналог роли challenge — verify Layer 4, но там proposal↔design; здесь код↔принятое слабое решение. Не смешивать.

## Decisions

### D1. Две оси: Compliance vs Quality judgment

- **Compliance** — AP/контракт/стандарт (как сейчас).
- **Quality judgment** — weak / design-prescribed → пользователь as-designed | queue-fix.
- Альтернатива «всегда MUST_FIX без disposition» отвергнута: ломает легитимные осознанные исключения.
- Альтернатива «только ужесточить Design authority без UX» отвергнута: шум без выбора заказчика.

### D2. Поля finding

```
QualityFlag: none | weak
Disposition: open | needs-confirm | as-designed | queue-fix | deferred
Design ref: …
design-endorsed: true|false
```

Agreement-override (`spec-explicit-tolerance`, `design-hardcode-justification`, HIDDEN_PARTIAL «по design», формальная Hardcode Justification) → finding остаётся с QualityFlag=weak / needs-confirm, не silent VERIFIED_OK.

**Порог weak:** `QualityFlag=weak` / корзина disposition — для findings severity HIGH+ **или** agreement-override (независимо от снижения Action). Ниже HIGH+ без agreement-override — по умолчанию без disposition UX (не раздувать шум).

**Владение Disposition:** агент в отчёте выставляет `QualityFlag=weak` и `Disposition=needs-confirm` (или `open` до парсинга оркестратором); финальные `as-designed` / `queue-fix` / `deferred` пишет **только** оркестратор после ответа заказчика. Шаг 5 skill отличает «VERIFIED_OK-via-agreement» от настоящего VERIFIED_OK по обязательности `QualityFlag=weak` (Action может остаться VERIFIED_OK — сигнал в QualityFlag, не только в Action).

**BREAKING:** bump `prompt_contract_version` (3 → 4) и `expected_reviewer_prompt_contract_version` в skill.

### D3. UX корзины после шага 4

| Корзина | Содержимое | Вопрос |
|---------|------------|--------|
| A | MUST_FIX CODE без weak | Устранить? (как сейчас) |
| B | weak / design-prescribed / VERIFIED_OK-via-agreement | as-designed / queue-fix / defer (пакетно + точечно) |
| C | REFACTOR / SURFACE | Упростить? / waive (как сейчас) |

Артефакт очереди (опц. SSOT): `openspec/changes/<id>/reports/review-queue-<slug>-YYYY-MM-DD.md` или `temp/reports/…` без change. Шаг 6 читает только `Disposition=queue-fix`.

### D4. Политика prerelease

`as-designed` не снимает Category 12 / release-hygiene без отдельного waive. Functional weak — as-designed с записью допустим.

### D5. Apply-reviewer

Без AskQuestion disposition. QualityFlag=weak / design-prescribed не авто-waive: авто-fix functional MUST_FIX как сейчас **или** оставить open + одна строка в отчёте задачи «на `/review` потребуется disposition».

### D6. Стык с extend

- `queue-fix` + ARCH / contradiction design → `--from-review` (accepted ≈ очередь на артефакты).
- `as-designed` ≈ rejected рекомендации **с записью причины**, не silent dismiss.
- Не смешивать семантики в одном поле без маппинга в extend skill.

### D7. Architectural Context wording

Было: «оценивать на соответствие контексту».  
Станет: контекст для Intent/Contract Map и поиска design-prescribed / contradiction; **соответствие design ≠ PASS по качеству**.

### D8. AP-042 и disposition

При наличии подстроки события/процедуры в tasks/design активного change AP-042 **не** silent-закрывается как «просто есть в постановке». Finding остаётся (`QualityFlag=weak` / `needs-confirm` или отдельный release-hygiene finding). Выбор as-designed по D4 **не** снимает Category 12 / release-hygiene без отдельного waive.

### D9. Whitelist silent VERIFIED_OK без disposition

Silent VERIFIED_OK/OK **без** `QualityFlag=weak` / `needs-confirm` допускается **только** для Evidence-типов:

- `documented-optional-contract` / `documented-protocol-key`
- `platform-documented-behavior`
- `resolved-contract:dynamic` (Resolved Contracts, Contract:dynamic, без жизнеспособных альтернатив)
- `historical-verified` (если уже в контракте агента)

**Не** в whitelist (→ weak / needs-confirm): `spec-explicit-tolerance`, `design-hardcode-justification`, HIDDEN_PARTIAL «по design», формальная Hardcode Justification без иных Evidence из whitelist.

## Slices

| Срез | Сценарии | Файлы | Primary acceptance | Зависимости |
|------|----------|-------|--------------------|-------------|
| S1 Disposition качества в review | Все scenarios capability `review-quality-disposition` | агент/шаблоны/checks + `review/SKILL.md` + команды + `review-guide.md` + стыки apply/extend | После внедрения: на change с design-endorse слабого паттерна `/review` (и зеркально понимание для `/release-review`) даёт weak/needs-confirm и предлагает as-designed / queue-fix; as-designed не уходит в writer | — |

### Матрица приёмки

| Сценарий (spec) | S1 |
|-----------------|----|
| Weak finding при design-endorse | Primary |
| Disposition UX ordinary+prerelease | Primary (тот же протокол) |
| as-designed не в writer | Primary |
| Prompt framing / Design authority | S1.<M> static |
| Prerelease hygiene / guide / apply | S1.<M> + optional accept |

**Primary acceptance:**

- S1: заказчик на подходящем change видит флаг «совпадает с постановкой, но спорно» и выбирает as-designed или queue-fix; выбор отражён в отчёте; as-designed не запускает writer.

## Открытые вопросы

1. Накопительный queue-файл из apply для предрелиза — later / out of MVP (не блокирует S1).

Закрыто verify-repair (2026-08-09): порог weak HIGH+∪agreement-override → D2; AP-042 → D8; whitelist Evidence → D9; владение Disposition → D2.

## Risks / Trade-offs

- [Шум disposition] → пакетный AskQuestion + порог severity.
- [Рассинхрон Disposition в report vs extend] → SSOT секция в main report; queue-файл опционален.
- [Breaking prompt contract] → bump version; оркестратор ждёт v4.
- [Apply «зелёный», release «weak»] → ожидаемо по уровням guide; UX-строка в apply-отчёте.

## Migration Plan

1. Один срез S1; внутри — волны применения: группа 1 (агент+шаблоны+checks) → группа 2 (skill/команды) → группа 3 (guide/стыки). Отдельных срезов S2/S3 нет.
2. Rollback: откат файлов kit; старые отчёты без Disposition читаются как open/none.
