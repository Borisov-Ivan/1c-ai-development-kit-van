## Context

`/opsx:explain` зрелый (B-explain → карта → карточки), но канонический propose идёт почти только из explore. Финалы `/review`, `/release-review`, apply T-HANDOFF explain не предлагают. Артефакты охвата (`review-*.md`, `code-map.md`, handoff-acceptance) не содержат machine-readable handoff и не автозаполняют слот **Охват**. HALT entry-brief запрещает «список модулей в бриф», что конфликтует с целью показать обработанный код на подтверждение.

Источник: `temp/reports/exploration-2026-08-09-explain-after-review-scope.md` (и `explain-scope-after-review.md`).

Параллельная ЗНИ `independent-review-disposition` не пересекается: Explain scope не кодирует accepted/rejected findings.

## Goals / Non-Goals

**Goals:**

1. Propose `/opsx:explain` после review/apply при подходящем scope.
2. Секция `## Explain scope` в артефактах-источниках.
3. Prefill B-explain (Охват / Варианты + Контекст) из handoff; подтверждение до карты.
4. Сохранить explore-propose и бюджет B-explain ≤6 слотов.

**Non-Goals:**

- Disposition as-designed / queue-fix.
- Отдельный handoff-файл explain.
- Автопрогон explain без «да» на брифе.
- Propose на trivial light-review (1 файл, 0 findings) как default.

## Existing Mechanisms

- Explore: «Дальше» → `/opsx:explain` при цепочке точек (без второго брифа в shortcut — здесь бриф нужен).
- Review: карточка 4 слотов, «Куда дальше» — fix / extend / archive.
- Apply: code-map, handoff-acceptance, T-HANDOFF → verify/apply/archive/extend.
- B-explain: Сценарий / Вопрос / Варианты XOR Охват / Контекст / Подтвердить?

## Design Rationale

Handoff живёт **внутри** существующих отчётов (`## Explain scope`), не отдельным файлом. Охват в брифе — UX-рамка (человеческий язык + пути в Контекст); карта точек — эффекты внутри утверждённой рамки. Для release full-extension — Варианты (Tier1 / findings / all), не весь cfe по умолчанию.

## Decisions

### D1. Формат `## Explain scope`

```markdown
## Explain scope (handoff)

- source: review | apply
- change: <name|none>
- focus: diff-focused | full | slice-S<N>
- files:
  - path: src/.../Module.bsl
    procedures: [Имя1, Имя2]   # опц.
- report: <path>
```

MVP: `files[]` + путь к отчёту. Процедуры — желательно.

**Канон apply-источника для `@`:** SSOT охвата = `reports/code-map.md` (path + процедуры по срезам). В `handoff-acceptance-*` — либо полная копия секции текущего среза, либо одна ссылка на code-map + `focus: slice-S<N>`. Не оставлять «и/или» без канона: при создании обоих артефактов секция обязательна в code-map; handoff — копия или ссылка.

### D2. Когда предлагать

| Триггер | Условие | Приоритет |
|---------|---------|-----------|
| `/review` | несколько `.bsl` / ≥2 логических точки / после fix | ниже MUST_FIX ask / extend |
| `/release-review` | всегда с намёком на Варианты рамки | то же |
| apply acceptance/final | менялся BSL | то же |
| trivial light-review 0 findings | не предлагать (мягкий hint допустим) | — |
| apply pause / только ARCH | не default | — |

Числовой порог «≤12 файлов» — только guidance для оркестратора, не MUST в spec.

### D2a. Propose vs «одна команда» / MUST_FIX

Когда primary next step = устранение MUST_FIX или `/opsx:extend` — `/opsx:explain` **не** занимает слот «Куда дальше».
Вторичная строка «также можно `/opsx:explain @…`» допускается **только** после выбора/отказа от primary.
Explain становится primary next step лишь при отсутствии открытого MUST_FIX ask и когда next ∈ {только отчёт, archive}.

### D3. Prefill B-explain

| Слот | Заполнение |
|------|------------|
| Сценарий | «После ревью…» / «После реализации среза…» |
| Вопрос | default: как устроены затронутые места |
| Охват | UX-абзац; ≥4 файлов — «список в Контекст» + якоря |
| Варианты | XOR с Охват; для huge release |
| Контекст | пути отчёта + полный список path |

После «да» — inventory только в утверждённом охвате.

### D4. HALT модулей

Запрещён сырой inventory / коды точек (`Mxx`, `pav…`) как замена Сценарию.  
В слоте **Охват** — только UX-абзац (≤~5 строк смысла, без полного списка path).  
Полный маркированный список `path` (+ опц. процедуры) — только в **Контекст**.  
Эталон C в `entry-brief.md` обязан демонстрировать XOR Охват/Варианты без путей в Охвате.  
Норматив spec Requirement «Brief HALT…» MUST совпадать с этим разделением слотов (не «path в Охват и Контекст»).

### D5. Fallback без секции

Первая итерация (MVP): автозаполнение Охвата **только** из артефактов с `## Explain scope`. Эвристика старых отчётов без секции — out of MVP (later). При отсутствии секции propose-автозаполнение не делать; в skill допустим мягкий hint «добавьте секцию / перезапустите review», не prefill.

## Slices

| Срез | Сценарии | Файлы | Primary acceptance | Зависимости |
|------|----------|-------|--------------------|-------------|
| S1 Explain scope handoff | Все scenarios capability | explain + review + apply + guide/commands | `/opsx:explain @review-или-code-map` показывает в брифе Охват обработанного кода; после review/apply может появиться propose explain | — |

### Матрица приёмки

Все scenarios spec → Primary или S1.<M> / optional accept внутри S1.

**Primary acceptance:** вызов explain по артефакту с `## Explain scope` → B-explain с Охватом; пользователь подтверждает до карты; propose доступен из финала review или apply.

## Открытые вопросы

1. ~~Сосуществование fix ask и explain~~ — закрыто в D2a.
2. ~~Fallback старых отчётов~~ — закрыто в D5 (MVP = только новый формат).
3. Обогащение procedures из Code-Truth — later.

## Risks / Trade-offs

- [Огромный release scope] → обязательные Варианты рамки.
- [Конфликт HALT] → точечная правка формулировки, не снятие бюджета.
- [Дублирование next steps] → explain ниже блокеров.

## Migration Plan

1. Секция Explain scope + propose в review/apply.
2. Ветка entry explain + эталон брифа.
3. Guide/commands/examples.
