# Срез S1: Реестр и запах

**Сценарий:** ревьюер или архитектор находит норму Hardcoded Identity Filter и запах Scope-as-literals рядом с Existing Mechanisms, с отсылкой к секции Hardcode Justification.
**Primary acceptance:** открыть `.cursor/rules/bsl-antipatterns.mdc` (индекс + Writer bulletin) и `.cursor/docs/antipatterns/bsl-antipatterns.md` — есть AP-055 (Hardcoded Identity Filter) с детекторами и remediation; открыть `.cursor/rules/existing-mechanism-priority.mdc` — есть запах Scope-as-literals и SSOT шаблона Hardcode Justification.
**Приёмка:** Primary по чтению/grep канона rules/docs (без ИБ).
**Связь со spec:** Requirement «Identity-filter has a named anti-pattern and remediation» — Scenario «Registry describes identity-filter class», Scenario «Protocol literals are out of class by default»; Requirement «Existing Mechanisms covers Scope-as-literals» — Scenario «Smell is documented next to mechanism hierarchy».
**Зависимости:** нет.

## 1. Реестр антипаттернов

- [x] S1.1 В `.cursor/rules/bsl-antipatterns.mdc`: добавить AP-055 Hardcoded Identity Filter в краткий индекс Writer bulletin и строку таблицы с детекторами runtime-фильтра по `ИмяФормы` / литералу `ОткрытьФорму` / allow-list имён метаданных в хуке и remediation «делегировать фильтр API/настройке или секция Hardcode Justification», чтобы норма была именуемой, а не «просто помни» (design Decision 2, Behavior Contract, детекторы)
- [x] S1.1b В `.cursor/docs/antipatterns/bsl-antipatterns.md`: добавить полную карточку AP-055 Hardcoded Identity Filter (детекторы из design § «Детекторы identity-filter»; remediation API/настройка или `## Hardcode Justification`; граница «не путать» с литералами протокола/enum), синхронно с индексом/таблицей в `bsl-antipatterns.mdc` (SSOT карточек — шапка `.mdc`)
- [x] S1.2 В `.cursor/docs/antipatterns/bsl-antipatterns.md` и однострочнике Writer bulletin в `.cursor/rules/bsl-antipatterns.mdc`: явно отделить легитимные литералы кодов отказа / ключей протокола / закрытых enum от класса identity-filter, чтобы Scenario «Protocol literals are out of class by default» не требовал MUST_FIX только из-за строкового литерала (Non-Goals)

## 2. Existing Mechanisms

- [x] S1.3 В `.cursor/rules/existing-mechanism-priority.mdc`: добавить запах Scope-as-literals (охват ADR/хука сведён к литералам имён вместо критерия класса) рядом с Shadow Storage / Parallel Workflow / Substituted Authority и отсылку заполнить `## Hardcode Justification`, чтобы Existing Mechanisms ловил этот класс до выбора «тонкого» списка (Requirement Scope-as-literals)
- [x] S1.4 В `.cursor/rules/existing-mechanism-priority.mdc`: вставить шаблон секции `## Hardcode Justification` из design.md Behavior Contract (литералы / почему не callee-API / набор закрыт навсегда / план N+1) как **SSOT пути** для копирования в design прикладных ЗНИ (не оставлять шаблон только в design этой ЗНИ)

## 3. Приёмка

- [x] S1.accept Принять срез S1 «Реестр и запах» — AP-055 и Scope-as-literals доступны в каноне kit:
  - **Primary (обязательно):** открыть `bsl-antipatterns.mdc` (индекс + Writer bulletin) и `docs/antipatterns/bsl-antipatterns.md` — AP-055 описывает Hardcoded Identity Filter, детекторы и remediation; открыть `existing-mechanism-priority.mdc` — есть Scope-as-literals и SSOT шаблона Hardcode Justification
  - Scenario «Protocol literals are out of class by default» (опционально): в карточке AP-055 и bulletin граница «не путать с литералами протокола/enum» читается без MUST_FIX на любой строковый литерал
  - Scenario «Smell is documented next to mechanism hierarchy» (опционально): запах Scope-as-literals стоит в блоке анти-паттернов Existing Mechanisms, а не только в отдельном standards-файле

<!-- slice-gate: в реестре (mdc+docs) есть AP-055; в Existing Mechanisms — Scope-as-literals и SSOT Hardcode Justification -->

# Срез S2: Architect HALT

**Сценарий:** архитектор не выбирает Chosen «&После + список имён форм», пока не ответит на три вопроса Identity Filter Gate и не зафиксирует Hardcode Justification.
**Primary acceptance:** в `.cursor/agents/onec-code-architect.md` и `.cursor/rules/architect-gate.mdc` есть Identity Filter Gate (три вопроса); вариант allow-list без ответов / без секции Hardcode Justification не становится Chosen.
**Приёмка:** Primary по чтению agent/rules (grep HALT / Identity Filter Gate).
**Связь со spec:** Requirement «Architect cannot choose allow-list without justification» — Scenario «Thin allow-list is not Chosen without answers».
**Зависимости:** S1.

## 1. Agent и gate

- [x] S2.1 В `.cursor/agents/onec-code-architect.md`: добавить Identity Filter Gate (зеркало Data Contract Gate) — HALT до Chosen allow-list имён форм/метаданных; три вопроса: callee уже фильтрует? набор закрыт навсегда? план при N+1?; без ответов в design секции Hardcode Justification вариант «список имён» не Chosen (Behavior Contract architect)
- [x] S2.2 В `.cursor/rules/architect-gate.mdc`: добавить триггер/правило Identity Filter Gate со ссылкой на AP-055 и шаблон Hardcode Justification (S1), чтобы оркестратор подгружал HALT при проектировании allow-list в хуке расширения (design Decision 1)
- [x] S2.3 В `.cursor/agents/onec-code-architect.md` и/или `.cursor/rules/architect-gate.mdc`: запретить обход формулировкой «временный список на первый релиз» — вопрос «закрыт навсегда» и план N+1 обязательны (Risks / Trade-offs design)

## 2. Приёмка

- [x] S2.accept Принять срез S2 «Architect HALT» — allow-list без Gate не Chosen:
  - **Primary (обязательно):** открыть `onec-code-architect.md` / `architect-gate.mdc` — есть Identity Filter Gate из трёх вопросов; без ответов / без Hardcode Justification вариант «тонкий список имён» не описывается как Chosen
  - Scenario «Thin allow-list is not Chosen without answers» (опционально): точечно сверить, что HALT ссылается на AP-055 и секцию Hardcode Justification из S1

<!-- slice-gate: Identity Filter Gate (3 вопроса) в architect agent/rules; allow-list без секции не Chosen -->

# Срез S3: Writer + Reviewer

**Сценарий:** writer останавливается на identity-literals без Hardcode Justification; reviewer проходит Phase 2.6 с completeness-таблицей и MUST_FIX при contradiction «без хардкода».
**Primary acceptance:** в writer есть G21; в `onec-code-reviewer.md`, `reviewer-checks.md` и `review/SKILL.md` — Phase 2.6 Identity / Hardcode Audit с completeness N=N; contradiction с Why/Non-Goals «без хардкода» → MUST_FIX AP-055.
**Приёмка:** Primary по чтению agent/docs/skills (grep G21 / Phase 2.6 / completeness).
**Связь со spec:** Requirement «Writer halts on unjustified identity literals» — Scenario «Allow-list without design section blocks writer»; Requirement «Reviewer audits identity literals with completeness» — Scenario «Completeness matches literal count», Scenario «Contradiction with no-hardcode goal is blocking».
**Зависимости:** S2.

## 1. Writer

- [x] S3.1 В `.cursor/agents/onec-code-writer.md`: добавить gate G21 (Identity / Hardcode justification) — HALT до добавления `ИмяФормы = "…"`, литерала `ОткрытьФорму("…")`, allow-list имён метаданных в хуке без ссылки на Hardcode Justification в design или явного запрета списка (всегда звать API); design с allow-list без секции = конфликт G20-style → HALT к оркестратору (design Decision 4)
- [x] S3.2 В `.cursor/agents/onec-code-writer.md` и `.cursor/skills/1c-agent-patterns/writer.md` (чеклист/сводка gates рядом с G14/G19/G20): включить G21 в перечень обязательных gates и self-check / Gate Results отчёта writer, чтобы проход не терялся на apply

## 2. Reviewer

- [x] S3.3 В `.cursor/agents/onec-code-reviewer.md`: добавить выделенный проход **Phase 2.6 Identity / Hardcode Audit** (не растворять только в Contract Map) — перечисление находок по детекторам design, строка таблицы на каждый литерал-фильтр, Evidence-override для легитимных литералов протокола/enum; contradiction с «без хардкода» в Why/Non-Goals → CRITICAL / MUST_FIX AP-055 (design Decision 3, Behavior Contract reviewer)
- [x] S3.4 В `.cursor/docs/standard/reviewer-checks.md`: описать Phase 2.6 Identity / Hardcode Audit с completeness-gate (число строк таблицы = число литералов-фильтров) и правилом MUST_FIX при contradiction, синхронно с agent reviewer (канон имени фазы: Phase 2.6 Identity / Hardcode Audit)
- [x] S3.5 В `.cursor/agents/onec-code-reviewer.md` и `.cursor/docs/standard/reviewer-checks.md`: вставить Phase 2.6 в порядок фаз (после 2.5, до Phase 3) и в checklist/summary отчёта, чтобы проход был обязательным, а не опциональной заметкой
- [x] S3.6 В `.cursor/skills/review/SKILL.md`: в местах, где сейчас упоминается / пропускается Phase 2.5 (trivial-skip, порядок фаз, appendix), добавить зеркало Phase 2.6 Identity / Hardcode Audit, чтобы выделенный проход не остался только в теле agent reviewer

## 3. Приёмка

- [x] S3.accept Принять срез S3 «Writer + Reviewer» — G21 и Phase 2.6 закрывают протекание на apply:
  - **Primary (обязательно):** открыть writer — есть G21; открыть reviewer + `reviewer-checks.md` + `review/SKILL.md` — есть Phase 2.6 с completeness N=N; contradiction с «без хардкода» → MUST_FIX AP-055
  - Scenario «Completeness matches literal count» (опционально): в тексте Phase 2.6 явно: N литералов-фильтров → N строк таблицы
  - Scenario «Contradiction with no-hardcode goal is blocking» (опционально): contradiction Why/Non-Goals помечен как блокирующий MUST_FIX по AP-055

<!-- slice-gate: G21 в writer; Phase 2.6 с completeness и MUST_FIX contradiction в reviewer + reviewer-checks + review/SKILL -->

## Follow-up

- [ ] Follow-up: опциональный grep post-apply (`ИмяФормы = "`) в verify как сигнал hygiene — отдельный extend; не блокер первой поставки (design Open Questions)
