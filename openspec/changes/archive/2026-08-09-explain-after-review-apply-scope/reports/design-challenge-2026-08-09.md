---
report_type: design-challenge
generated_at: 2026-08-09
agent: onec-code-architect
mode: design-challenge
scope:
  change: explain-after-review-apply-scope
  design_mtime: "2026-08-09T11:23:42.8157748+09:00"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — explain-after-review-apply-scope

## Адверсариальная установка

Независимый разбор kit meta-change: прочитаны только `proposal.md`, `design.md`, `specs/explain-post-implementation-scope/spec.md` и актуальные файлы kit (`openspec-explain` entry-brief/SKILL, `review/SKILL` §4.4–5, `openspec-apply-change` code-map/T-HANDOFF, `opsx-output-style` B-explain / next-step). Собственные прошлые `reports/architecture-*.md` и exploration-отчёты **не** использовались как источник истины. Closed decisions: пусто.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** после `/review`, `/release-review` и `/opsx:apply` нет перехода в `/opsx:explain` с уже известным списком обработанного кода; бриф explain приходится заполнять вручную, хотя охват уже есть в отчёте ревью или `code-map`; нужны handoff и автозаполнение **Охвата** в entry-брифе для подтверждения.
- **Design адресует:**
  - Why «нет перехода» → propose `/opsx:explain` из финалов review/release-review/apply (D2, Goals 1).
  - Why «охват уже лежит в артефакте, но не machine-readable / не в брифе» → секция `## Explain scope` внутри существующих отчётов (D1, Goals 2) + prefill слотов B-explain (D3, Goals 3).
  - Why «подтверждение рамки» → карта только после «да» (D3, spec «No mass Read before confirm»).
  - Конфликт текущего HALT «список модулей не в бриф» с целью показать охват → точечная правка HALT (D4), не снятие бюджета ≤6 слотов.
- **Покрытие:** полное по сути Why. Вне Why и явно out of scope: disposition as-designed/queue-fix; отдельный `temp/explain-handoff-*.md`; автостарт без брифа — согласовано с Non-Goals. Частичный риск исполнения (не дыра Why): сосуществование propose с «одна команда» в финале review и канон apply-артефакта не зафиксированы как решение — см. Gaps.

### Q2 — Optimality

- **Выбранный путь:** handoff-секция внутри `review-*.md` / `code-map` / handoff-acceptance + propose с приоритетом ниже fix/extend + prefill B-explain (Охват XOR Варианты) без отдельного файла и без автопрогона карты.
- **Альтернативы (включая не упомянутые в design):**
  1. **Парсинг уже существующих карт без новой секции** — explain читает строки `code-map.md` (формат `- **S<N>.<M>** · … [`path`](…):lines`) и/или блок «Что отрецензировано» / findings paths из review-отчёта. Плюсы: меньше писателей секций, zero-churn формата для apply. Минусы: review-отчёты сегодня не гарантируют единый machine-readable список файлов+процедур; эвристика хрупка; Why требует явного handoff на подтверждение. Отклонена как MVP: хуже контракт «откуда брать охват», чем явная секция (D1/D5).
  2. **Shortcut как у explore (без второго брифа)** — при `@review-*.md` / `@code-map.md` сразу карта точек в рамке артефакта. Плюсы: меньше трения, зеркало explore («Дальше» → explain без второго брифа). Минусы: для huge release и широкого review рамка неочевидна; Why явно хочет подтверждение Охвата; Non-Goal «автопрогон без да» делает shortcut хуже выбранного пути. Отклонена для post-review/apply; explore shortcut сохраняется отдельно (spec «Explore propose remains intact»).
  3. **Липкий scope только в текущем чате** — после review/apply оркестратор держит список файлов в контексте сессии и подставляет в explain без записи в отчёт. Плюсы: ноль правок формата артефактов. Минусы: ломается `/opsx:explain @review-*.md` в новом чате; нет audit trail; противоречит Impact «секция в артефактах». Отклонена.
  4. *(упомянута в Non-Goals, для полноты атаки)* **Отдельный `temp/explain-handoff-*.md`** — дублирует охват вне review/code-map. Хуже выбранного: orphan-файлы, расхождение с отчётом-источником. Правильно отклонена.
- **Вердикт по Q2:** выбранный путь оптимален среди жизнеспособных для Why (durable handoff + подтверждение рамки + бюджет брифа). Лучшей альтернативы по коду/поведению kit нет; остаются пробелы спецификации поведения propose и канона apply-артефакта (не смена оси решения).

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками
- **Причины:**
  - Да: боль подтверждается текущим kit — `review/SKILL.md` §4.4 «Куда дальше — одна команда (устранение / extend / archive)» без explain; apply строит `code-map` и T-HANDOFF, но не предлагает explain; B-explain HALT запрещает «Список модулей (`pav…`, M01…)» в брифе, что реально конфликтует с post-implementation охватом.
  - Да: форма решения минимальна для meta-kit (одна секция + ветка entry + propose), сохраняет explore и не тащит disposition.
  - Оговорка: до apply нужно закрыть Gaps ниже — иначе writer/оркестратор получит конфликт «одна команда» vs вторичный hint, и неоднозначность `code-map` **и/или** handoff-acceptance как входа для `@`.

## Verdict

**CHALLENGE** — Why закрыт выбранным механизмом handoff+prefill, путь оптимален, но в `design.md`/`spec` остаются незакрытые правила UX propose и канона apply-артефакта; это `implementation_invariant` gaps, не смена архитектуры.

## Gaps for design.md

1. **Сосуществование с «одна команда» / MUST_FIX ask (открытый вопрос design №1 → Decision).** Зафиксировать: когда primary next step = устранение / extend — explain **не** занимает слот «Куда дальше»; допускается одна вторичная строка «также можно `/opsx:explain @…`» **только** если primary уже выбран/отказан, либо explain становится primary лишь при отсутствии MUST_FIX ask и next ∈ {только отчёт, archive}. Иначе правка review финала конфликтует с `review/SKILL.md` §4.4 и правилом одного user-action next step в `opsx-output-style`.
2. **Канон apply-источника для `@`.** Убрать мягкое «и/или»: SSOT охвата apply = `reports/code-map.md` (уже содержит path+процедуры по срезам); в `handoff-acceptance-*` — либо полная копия секции текущего среза, либо одна ссылка на code-map + `focus: slice-S<N>`. Spec Scenario «Apply artifacts…» согласовать с этим каноном.
3. **Черновик формулировки HALT (D4) в design.** Явно: в **Охват** — UX-абзац (≤~5 строк смысла, без inventory/`pav`/`Mxx`); полный маркированный список `path` (+ опц. процедуры) — только в **Контекст**; эталон C в `entry-brief.md` обязан демонстрировать XOR Охват/Варианты без путей в Охвате.
4. **Закрыть MVP по fallback (открытый вопрос №2).** В Decisions: первая итерация = только артефакты с `## Explain scope`; без эвристики старых отчётов; propose-автозаполнение при отсутствии секции — не делать (мягкий hint «добавьте секцию / перезапустите review» допустим в skill, не в prefill).
5. **Порог «≤~12 .bsl».** Либо вынести в design как guidance (не MUST в spec), либо заменить качественным критерием уже из таблицы D2 («несколько логических точек / после fix») без числа, чтобы не плодить ложные HALT на границе 12.

## Architectural alternatives

Равноправной развилки по наблюдаемому поведению kit **нет**: отдельный handoff-файл и chat-only scope хуже; parse-without-section и explore-shortcut уступают по контракту подтверждения рамки / устойчивости между чатами. После закрытия Gaps ось решения (секция внутри отчёта + prefill брифа) остаётся Chosen.

## Источники

- proposal.md — `## Why`, `## What Changes`, `## Impact`, `## Scope` (out: disposition, отдельный handoff, автостарт).
- design.md — Context; Goals/Non-Goals; Decisions D1–D5; открытые вопросы 1–3; Risks; Slices.
- specs/explain-post-implementation-scope/spec.md — requirements Explain scope section; Propose explain; B-explain prefill; Brief HALT; Explore intact; scenarios Prefill / Huge release / No mass Read / Trivial skip.
- Kit: `.cursor/skills/openspec-explain/templates/entry-brief.md` (слоты, HALT «Список модулей»); `.cursor/skills/openspec-explain/SKILL.md` §1 бриф; `.cursor/skills/review/SKILL.md` §4.4 «Куда дальше — одна команда», шаг 5 MUST_FIX ask; `.cursor/skills/openspec-apply-change/SKILL.md` (code-map формат, T-HANDOFF acceptance); `.cursor/docs/opsx-output-style.md` (B-explain, user-action next step); `.cursor/skills/openspec-explore/SKILL.md` (propose explain без второго брифа).
