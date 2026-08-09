# Срез S1: Explain scope после review/apply

**Сценарий:** После ревью или внедрения кода kit предлагает `/opsx:explain` и в первом брифе показывает охват обработанного кода на подтверждение.
**Primary acceptance:** Given отчёт review или code-map/handoff с секцией `## Explain scope`; When вызван `/opsx:explain` на этот артефакт; Then в чате B-explain со слотом Охват (или Варианты для огромного release), путями в Контекст, и карта точек не начинается до «да».
**Приёмка:** ручная проверка протокола kit (explain + наличие секции/propose в skill); без обязательной ИБ продукта.
**Связь со spec:** Requirement «Explain scope section…», Scenario «Review report has Explain scope», «Apply artifacts have Explain scope»; Requirement «Propose explain after review and apply»; Requirement «B-explain prefill from handoff»; Requirement «Brief HALT allows compact…»; Requirement «Explore propose remains intact».
**Зависимости:** нет
**Режим apply:** mechanical

## 1. Handoff-секция

- [x] S1.1 В `review/SKILL.md` обязать писать `## Explain scope` в main report (формат из design D1); self-check
- [x] S1.2 В `openspec-apply-change/SKILL.md` при BSL: писать `## Explain scope` в `code-map.md` (SSOT); в `handoff-acceptance-*` — копия секции среза или ссылка на code-map + `focus: slice-S<N>` (design D1); запрет отдельного explain-handoff файла

## 2. Propose explain

- [x] S1.3 В `review/SKILL.md` / финале release-review (слот «Куда дальше» / шаг 7): propose `/opsx:explain` по D2+D2a — не занимает слот при открытом MUST_FIX/extend; skip trivial light-review
- [x] S1.4 В `opsx-output-style` §5.2 и next-step T-HANDOFF `openspec-apply-change/SKILL.md`: опциональный `/opsx:explain` после BSL acceptance/final (приоритет ниже verify/extend)
- [x] S1.5 Одна строка в `review.md`, `release-review.md` и обновление `review-guide.md`: когда звать explain после ревью

## 3. Prefill B-explain

- [x] S1.6 В `openspec-explain/SKILL.md` ветка source=review|apply: Read ≤3 артефактов, извлечь Explain scope, собрать B-explain (Охват / Варианты), карта только в утверждённой рамке
- [x] S1.7 В `entry-brief.md` эталон C post-review/apply; уточнить HALT модулей (сырой dump запрещён; компактный охват разрешён); опц. fixture в `voice-good-brief.md`
- [x] S1.8 Обновить `brief-card.md` § B-explain (ссылка на эталон) и примеры в `opsx-explain.md` (`@review-*.md`, `@code-map.md`)
- [x] S1.9 Верифицировать по коду kit: explore-propose explain не удалён; grep `Explain scope` / post-review в изменённых skills; as-designed disposition не затронут

- [x] S1.accept Принять срез S1 «Explain scope после review/apply» — бриф explain с охватом обработанного кода:
  - **Primary (обязательно):** открыть/смоделировать `/opsx:explain` на артефакте с `## Explain scope` → в брифе Охват (или Варианты) и Контекст со списком path; до «да» карта не стартует
  - Scenario «Review/Apply offer explain» (опционально): по skill финал review или apply может предложить explain при подходящем scope
  - Scenario «Explore still suggests explain» (опционально): в explore skill строка propose explain на месте
  - Scenario «Trivial skip» (опционально): light-review без findings не обязан propose

<!-- slice-gate: Primary — B-explain с Охватом из Explain scope до карты точек -->
