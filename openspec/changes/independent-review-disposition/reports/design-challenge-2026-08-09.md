---
report_type: design-challenge
generated_at: 2026-08-09
agent: onec-code-architect
mode: design-challenge
scope:
  change: independent-review-disposition
  design_mtime: "2026-08-09T11:14:00+09:00"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — independent-review-disposition

## KB references

- Discovery выполнен, совпадений нет — not relevant: база знаний в репозитории отсутствует; на выводы challenge не влияет.

## Адверсариальная установка

Независимый разбор: прочитаны только `proposal.md`, `design.md`, `specs/review-quality-disposition/spec.md` и текущие файлы kit (`.cursor/skills/review/SKILL.md`, `.cursor/agents/onec-code-reviewer.md`, `.cursor/skills/1c-agent-patterns/reviewer.md`, `.cursor/docs/standard/reviewer-checks.md`). Собственные прошлые `reports/architecture-*.md` / QC как источник истины не использовались. Цель — отвергнуть решение, если оно не закрывает Why или уступает более простому пути в коде/контракте отчёта.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** после `/review` и `/release-review` слабая реализация, уже разрешённая в постановке, уходит как «соответствует design» / VERIFIED_OK без явного выбора заказчика «оставляем как задумано» или «чиним»; нужен единый слой независимой оценки качества и disposition для обеих команд (`proposal.md` ## Why, ## What Changes).
- **Design адресует:**
  - Why «тихий VERIFIED_OK из agreement» → D2: agreement-override оставляет finding с `QualityFlag=weak` / `needs-confirm`, не silent VERIFIED_OK; spec «Agreement does not silently close quality findings».
  - Why «нет выбора заказчика» → D3 корзина B + AskQuestion as-designed | queue-fix | defer; spec «Unified disposition UX».
  - Why «Architectural Context как эталон PASS» → D7 переписывает framing; подтверждено в коде kit: шаблон `reviewer.md` сейчас буквально требует «Оценивать решения в коде на соответствие контексту» (`.cursor/skills/1c-agent-patterns/reviewer.md`).
  - Why «один алгоритм ordinary/prerelease» → один протокол в skill, команды только выставляют `release_mode` (D3/D4 + spec scenarios).
  - Why «apply не должен тормозить» → D5 без AskQuestion disposition в apply-reviewer (spec «Apply-reviewer does not run disposition AskQuestion»).
- **Покрытие:** частичное. Ось Compliance vs Quality и UX disposition закрывают симптом из Why. Но в `design.md` ## Открытые вопросы остаются нерешёнными порог severity (Q1), судьба AP-042 (Q2) и узкий whitelist Evidence без disposition (Q3) — без них сценарий «WHEN паттерн был бы MUST_FIX/HIGH+» из spec неоднозначен: оркестратор/агент могут по-разному решать, что попадает в корзину B vs остаётся silent VERIFIED_OK. Пока эти политики не зафиксированы как решения (не «рекомендация explore»), Why закрыт на уровне модели, но не на уровне исполняемого контракта.

### Q2 — Optimality

- **Выбранный путь:** ортогональные поля `QualityFlag` / `Disposition` на finding + корзины A/B/C в skill после шага 4; writer-контракт Action (MUST_FIX/REFACTOR) сохраняется; bump `prompt_contract_version` 3→4.
- **Альтернативы (включая не упомянутые в design; секции `## Implementation Options` нет — сравнение с D1 и с путями ниже):**

  1. **Пост-фильтр оркестратора без новых полей finding** — после отчёта skill сканирует Evidence-типы (`spec-explicit-tolerance`, `design-hardcode-justification`, …) и поднимает AskQuestion disposition, не меняя схему Action/QualityFlag. Плюсы: меньший breaking surface (возможен bump только skill, не prompt contract агента). Минусы: `VERIFIED_OK` остаётся «закрытым» в теле отчёта до пост-обработки; агент и guide расходятся; `design-prescribed` из `reviewer-checks.md` уже существует, но не доведён до промпта — фильтр не чинит framing Architectural Context и не даёт стабильного сигнала writer/extend. Хуже выбранного: нет явной оси качества в SSOT отчёта.

  2. **Новое значение Action (`CONFIRM` / `QUALITY_REVIEW`) вместо ортогонального QualityFlag** — слабые design-endorsed findings меняют Action, а не добавляют поле. Плюсы: одно поле для шага 5. Минусы: ломает writer-пайплайн и исторические отчёты сильнее (writer сегодня ключует MUST_FIX/REFACTOR); смешивает compliance-дефект и quality-judgment. Хуже выбранного: D1 явно сохраняет writer-контракт — это правильный инвариант для kit.

  3. **Только ужесточить Design authority / запрет agreement→VERIFIED_OK, без UX disposition** — уже отвергнуто в D1 как «шум без выбора». Подтверждение из кода: шаг 5 skill спрашивает только про MUST_FIX/REFACTOR; путь «только VERIFIED_OK → шаг 7» (`.cursor/skills/review/SKILL.md`) — без disposition заказчик снова не выбирает as-designed vs queue-fix. Не закрывает Why про явный выбор.

  4. **Всегда MUST_FIX без disposition** — отвергнуто в D1; ломает легитимные исключения (Hardcode Justification, documented tolerance). Для kit meta-change это регресс осознанных постановки-исключений.

  5. **Отдельный adversarial-субагент на `/review` (аналог verify challenge code↔design)** — независимая проверка качества вторым агентом. Плюсы: сильнее независимость. Минусы: стоимость/латентность каждого review, дублирование Phase 0/AP, не нужен для UX disposition. Избыточен относительно Why (нужен флаг + выбор, не второй полный audit).

- **Вердикт по Q2:** выбранный путь оптимален среди жизнеспособных для Why: минимально инвазивен к writer (ортогональные поля), чинит framing и agreement-override в источнике (агент+шаблоны), даёт единый UX. Альтернатива «пост-фильтр» проще по схеме полей, но слабее по наблюдаемости и стыку с extend/guide. Лучшей альтернативы по коду/поведению нет.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками (не чистое «да»).
- **Причины:**
  - Да: Why воспроизводится в kit (`reviewer.md` framing «на соответствие»; Evidence-override → VERIFIED_OK в `onec-code-reviewer.md`; шаг 5 skill игнорирует quality-hidden VERIFIED_OK) — направление решения правильное.
  - Да: разделение корзин A/B/C и запрет as-designed снимать Category 12 (D4 + spec) — здравые границы prerelease.
  - Нет / оговорка: до apply нельзя оставлять открытыми порог weak, AP-042 и whitelist Evidence (## Открытые вопросы 1–3) — это не косметика, а границы, когда finding обязан попасть в disposition; иначе spec Scenario «Design endorses weak pattern» недетерминирован.
  - Оговорка: Migration Plan описывает S1→S2→S3, а таблица Slices — один срез S1 на все файлы; риск рассинхрона приёмки/tasks, не альтернатива по поведению, но gap постановки.

## Verdict

**CHALLENGE** — модель Compliance/Quality + disposition UX решает Why и оптимальнее рассмотренных альтернатив, но исполняемый контракт не готов, пока не закрыты политики порога/whitelist/AP-042 и не выровнены фазы миграции со срезом.

## Gaps for design.md

1. **implementation_invariant — порог weak:** зафиксировать решение (не «рекомендация explore»): weak/disposition только для HIGH+ и agreement-override **или** явная более широкая матрица severity×kind; отразить в D2/D3 и в scenarios spec при необходимости.
2. **implementation_invariant — whitelist Evidence без disposition:** явно перечислить типы, которым разрешён VERIFIED_OK без корзины B (`documented-protocol-key` / `platform-documented` / `resolved-dynamic` и т.д. — как в открытом вопросе 3); всё остальное agreement → weak/needs-confirm.
3. **implementation_invariant — AP-042:** выбрать flag+disposition **или** оставить hygiene-исключение; убрать развилку из ## Открытые вопросы.
4. **implementation_invariant — владение Disposition:** кто выставляет `open` vs `needs-confirm` (агент в отчёте vs оркестратор после парсинга); как шаг 5 отличает «VERIFIED_OK-via-agreement» от настоящего VERIFIED_OK при парсинге (обязательность `QualityFlag=weak` даже если Action остаётся VERIFIED_OK — зафиксировать одной фразой в D2/D3).
5. **постановка — Migration vs Slices:** либо одна фаза внутри S1 с внутренним порядком агент→skill→docs, либо явные подсрезы; убрать противоречие «S2/S3» без строк в таблице Slices.
6. **spec (minor):** Scenario «Prompt framing» — добавить позитивный критерий (какие формулировки MUST присутствовать: intent / design-prescribed / «соответствие ≠ PASS»), не только негативный «не сводятся к…».

## Architectural alternatives

Равноправной развилки по коду/поведению, требующей выбора заказчика до apply, **нет**. Закрытые вопросы выше — уточнения инварианта реализации, не смена оси D1.

Рассмотренные и отклонённые пути (для трассировки, не развилки):

### Пост-фильтр skill vs поля на finding
**A. Ортогональный QualityFlag/Disposition (выбранный):** сигнал в SSOT отчёта агента; skill читает поля. Trade-off: breaking prompt_contract_version.
**B. Только пост-фильтр Evidence в skill:** без новых полей. Trade-off: отчёт агента врёт «OK» до фильтра; хуже для guide/extend/записи disposition.

## Источники

- proposal.md — `## Why`, `## What Changes`, Impact/Scope (kit review contour; out of scope explain / verify challenge)
- design.md — Context; Goals; D1–D7; Slices vs Migration Plan; ## Открытые вопросы 1–3; Risks
- specs/review-quality-disposition/spec.md — Agreement does not silently close; Architectural Context; Unified disposition UX; Prerelease hygiene; Apply-reviewer
- Код kit — `.cursor/skills/1c-agent-patterns/reviewer.md` (Architectural Context: «Оценивать решения… на соответствие»); `.cursor/agents/onec-code-reviewer.md` (`prompt_contract_version: 3`, Evidence-override → VERIFIED_OK / `spec-explicit-tolerance`); `.cursor/skills/review/SKILL.md` (шаг 2.2 Architectural Context; шаг 5 AskQuestion только MUST_FIX|REFACTOR; только VERIFIED_OK → шаг 7); `.cursor/docs/standard/reviewer-checks.md` (Design authority / `design-prescribed` без проводки в системный промпт агента — по утверждению design Context, согласуется с разрывом checks vs agent frontmatter)
