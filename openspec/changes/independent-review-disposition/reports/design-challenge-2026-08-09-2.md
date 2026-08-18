---
report_type: design-challenge
generated_at: 2026-08-09
agent: onec-code-architect
mode: design-challenge
scope:
  change: independent-review-disposition
  design_mtime: "2026-08-09T05:55:21Z"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — independent-review-disposition

## KB references

- Discovery выполнен, совпадений нет — секция Existing Knowledge пуста; конфликтов KB нет.

## Адверсариальная установка

Независимый проход после verify-repair: прочитаны только `proposal.md`, обновлённый `design.md` (D2/D8/D9 + Migration волны), `specs/review-quality-disposition/spec.md`, `tasks.md`, `debug.md` § Verify repair и актуальный код kit (агент/шаблоны/skill/AP). Отчёты `reports/architecture-*.md` и предыдущий design-challenge как источник истины не использовались. Closed axis D1 (ортогональные Compliance / Quality) не оспаривается без нового факта; фокус — закрытие implementation_invariant после repair.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** после `/review` и `/release-review` слабая реализация, уже разрешённая в постановке, уходит как «соответствует design» / silent VERIFIED_OK без явного выбора заказчика as-designed | queue-fix; нужен единый слой независимой оценки качества и disposition для обеих команд.
- **Design адресует:**
  - Why «тихий VERIFIED_OK из-за design» → D1/D2 ортогональный `QualityFlag=weak` + `Disposition=needs-confirm`; agreement-override не финальный PASS; D9 выводит design-связанные Evidence из silent whitelist; D7 меняет framing Architectural Context (сейчас в шаблоне: «Оценивать решения в коде на соответствие контексту» — `.cursor/skills/1c-agent-patterns/reviewer.md`).
  - Why «нет выбора заказчика» → D3 корзины A/B/C между шагами 4 и 5; финальные as-designed / queue-fix / deferred пишет оркестратор (D2 владение); шаг 6 только `queue-fix`.
  - Why «один алгоритм ordinary+prerelease» → один skill, команды только `release_mode`; D4 as-designed ≠ waive Category 12.
  - Why «AP / постановка закрывает hygiene» → D8: AP-042 при подстроке в tasks/design остаётся finding с weak/needs-confirm (verified: сейчас отсутствие подстроки = flag, наличие = молчание — `.cursor/agents/onec-code-reviewer.md` AP-042; каталог AP-042 severity MEDIUM).
- **Покрытие:** полное по оси Why; остаточный риск — неоднозначность D9 по Evidence-типам kit, не перечисленным ни в whitelist, ни в «не whitelist» (см. Gaps). Spec scenarios (design-endorse, design-prescribed, prompt framing, disposition UX, hygiene, apply carve-out, guide) трассируются в D2–D9 / S1.

### Q2 — Optimality

- **Выбранный путь:** ортогональные поля QualityFlag/Disposition + UX-корзина B + bump `prompt_contract_version` 3→4; writer-контракт Action (MUST_FIX/REFACTOR/VERIFIED_OK) сохраняется; silent VERIFIED_OK только по узкому Evidence whitelist (D9); AP-042 — flag+disposition (D8).
- **Альтернативы (включая не упомянутые в design):**
  1. **Только ужесточить Design authority без новых полей** — проводка уже существующего `design-prescribed` / Design authority из `reviewer-checks.md` в агент+шаблоны и AskQuestion оркестратора по tag, без QualityFlag/Disposition и без bump контракта. Плюс: меньше BREAKING. Минус: не покрывает VERIFIED_OK-via-agreement с Action=VERIFIED_OK (шаг 5 skill сейчас пропускает чистые VERIFIED_OK → шаг 7 — `.cursor/skills/review/SKILL.md`); Why требует видимого disposition при agreement-override. Отклонена относительно Chosen.
  2. **Удалить design-связанные Evidence-типы из каталога override** (`spec-explicit-tolerance`, `design-hardcode-justification`) так, что Action остаётся MUST_FIX и уходит в текущий fix AskQuestion без второй оси. Плюс: проще модель полей. Минус: ломает легитимные осознанные исключения (D1 уже отверг «всегда MUST_FIX»); смешивает «надо чинить код» и «заказчик принимает риск». Хуже Chosen по UX.
  3. **Отдельный post-review quality-challenger субагент** (аналог verify Layer 4, но код↔принятое слабое решение). Плюс: сильнее независимость от того же промпта reviewer. Минус: второй полный проход, дублирование Findings, выше стоимость kit; proposal/design явно разделяют роли (Non-Goals: не смешивать с Layer 4). Избыточно при корректном QualityFlag в том же отчёте.
- **Вердикт по Q2:** оптимален для Why при условии доопределения D9 по полному каталогу Evidence kit; равноправной лучшей альтернативы по Blast Radius / числу перехватов нет.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками
- **Причины:**
  - Да: Why ↔ механизм (не silent PASS при design-endorse + явный выбор заказчика) согласованы; D2 порог HIGH+∪agreement-override и владение Disposition закрывают шум и двойную запись; D8 бьёт в verified дыру AP-042 «есть в постановке → нет finding».
  - Оговорка: D9 whitelist неполна относительно Evidence override в `onec-code-reviewer.md` (см. Gaps) — риск разного поведения apply по `closed-vendor-enum` / `spec-explicit-non-identity-filter` / `spec-explicit-timestamp`.
  - Оговорка: Action=VERIFIED_OK при QualityFlag=weak корректен только если skill явно парсит QualityFlag/needs-confirm (tasks S1.5–S1.6 это требуют — допустимо как implementation_invariant, не смена оси).

## Verdict

**CHALLENGE** — ось D1 и repair Chosen D2/D8/D9 решают Why и имплементируемы, но D9 должен явно классифицировать все текущие Evidence-типы silent override из агента, иначе ядро «когда silent VERIFIED_OK законен» остаётся дырявым на apply.

## Gaps for design.md

- **D9 — дописать Evidence-типы из kit, отсутствующие и в whitelist, и в «не whitelist»:**
  - `closed-vendor-enum` — verified: Evidence override Phase 2.6 (`onec-code-reviewer.md`); по смыслу silent OK (не design-endorse weak) → добавить в whitelist silent VERIFIED_OK **или** явно «silent без disposition».
  - `spec-explicit-non-identity-filter` — verified: тот же блок override; классификация «не identity-filter», не agreement на слабость → то же.
  - `spec-explicit-timestamp` — verified: AP-045 override в агенте; вне Why quality/disposition → whitelist silent или «вне корзины B».
- **D2/D8 — одна строка связки:** AP-042 в каталоге MEDIUM; при «подстрока есть в tasks/design» путь = agreement-override (D8), не отсекается порогом HIGH+. Сейчас подразумевается; для apply/writer промпта лучше явная фраза в D2 или D8 (implementation_invariant, не reopen оси).
- **Spec ↔ D9:** requirement «Agreement…» ссылается на «явно перечисленный узкий whitelist» — после дописи типов синхронизировать текст spec/tasks S1.1/S1.11 со списком D9 один-в-один (без смены сценариев).

## Architectural alternatives

Нет равноправной развилки по коду/поведению, требующей выбора пользователя: альтернативы Q2 уступают Chosen или меняют стоимость без выигрыша по Why. Repair Chosen D8/D9 не reopen (`reopen-blocked` не применяется — gaps расширяют D9, не отменяют whitelist-подход).

## Источники

- proposal.md — `## Why`, `## What Changes`, Impact (kit review/release-review)
- design.md — D1–D9, Slices S1, Migration волны, Open questions (repair closed)
- specs/review-quality-disposition/spec.md — Agreement / Architectural Context / Unified disposition / Prerelease hygiene / Apply-reviewer
- tasks.md — S1.1–S1.11, Primary acceptance
- debug.md — Verify repair Chosen defaults
- Код kit — `.cursor/agents/onec-code-reviewer.md` (AP-042; Evidence override B/C; Phase 2.6 types; AP-045 `spec-explicit-timestamp`); `.cursor/skills/1c-agent-patterns/reviewer.md` (Architectural Context framing); `.cursor/skills/review/SKILL.md` шаг 5 (VERIFIED_OK → шаг 7); `.cursor/docs/antipatterns/bsl-antipatterns.md` AP-042 MEDIUM
