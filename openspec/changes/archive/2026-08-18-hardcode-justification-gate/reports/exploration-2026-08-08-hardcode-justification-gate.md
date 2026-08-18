# Exploration: Hardcode Justification Gate (kit)

**Дата:** 2026-08-08  
**Профиль:** explore-question  
**user-goal:** Как встроить в фреймворк обязательное обоснование хардкода для архитектора и ревьювера (аналог Попытка / defensive cake)?  
**Пример-якорь:** `РаботаСБизнесПроцессамиВызовСервера` — whitelist `ИмяФормы = "…"` (3 литерала)

---

## 1. Эталон, который уже сработал

Попытка и defensive cake закрыты **четырёхслойно**, а не одним упоминанием в стандартах:

| Слой | Где | Механика |
|------|-----|----------|
| Реестр | `bsl-antipatterns.mdc` + docs AP-004/006/008/027/029… | Именованный антипаттерн + severity + remediation |
| Writer | G14 (contract), G19 (Попытка justification), G20 (design не освобождает) | HALT до добавления; «виновны, пока не доказаны» |
| Reviewer | Phase 2.5 Попытка & Contract Audit | Отдельный проход + completeness gate (N блоков = N строк таблицы) |
| Architect | Data Contract Gate / Rule 14 | Не предписывать guard/Попытку без контракта |

Ключ успеха: **скептическая стойка + выделенный проход + completeness**, а не «помни про антипаттерн».

---

## 2. Где дыра сейчас (kit)

| Что есть | Что отсутствует для хардкода идентичности |
|----------|-------------------------------------------|
| `existing-mechanism-priority.mdc` — Shadow Storage, Parallel Workflow, Substituted Authority | Нет антипаттерна «Literal Identity Filter / hardcoded allow-list имён форм/метаданных» |
| Architect: секция Existing Mechanisms | Нет HALT: «прежде чем allow-list имён — почему callee/API/настройка не решают?» |
| Reviewer Phase 2.5 | Не перечисляет сравнения `ИмяФормы`/`ТипЗнч` с литералами метаданных как класс находок |
| Writer G14/G19 | Нет G-gate на добавление списка литералов идентичности |
| AP-031/054 allow-list | Про **язык/имена идентификаторов**, не про runtime-фильтр по строкам метаданных |

Итог: хардкод часто маскируется под «узкий охват / thin / меньше шума» и проходит architect+reviewer, пока пользователь не отклонит на приёмке.

---

## 3. История ЗНИ: где протекало (ловил заказчик)

### 3.1. `archive/2026-08-06-ssylka-tablitsa-knopok-dop-funkcii` — **directly-related**

Два user-extend после приёмки:

1. Хардкод вызова `ДобавитьСсылкуНаТаблицуКнопокЗапускаШаблонов` в `ПриСозданииНаСервере` (Option B) — ожидание: строка в макете + автогенерация.
2. Именованный `ОткрытьФорму(...ФормаСписка)` — ожидание: цель из `ЗначениеПоУмолчанию` макета.

В design позже зафиксировано: «Именованный ОткрытьФорму — **Отклонён (хардкод цели)**».  
**Кто поймал:** пользователь на S1.accept, не Phase 2.5 / не architect smell.

### 3.2. `prerelease-fix-knopki-shablonov` (active) — **directly-related**

- Architect предложил **S3-B**: `&После` + allow-list из 3 имён форм как «тонкий» вариант.
- Apply прошёл; код с тремя литералами оказался в модуле.
- User-extend 2026-08-08 (2): «Хардкод трёх имён форм — отклонён»; утверждён **S3-C** (всегда вызов API; охват = условия API; D8/D11).
- В `debug.md`: смена scope после apply; tasks ждут доработки хука.

**Кто поймал:** пользователь после apply. Architect **сам предписал** allow-list; reviewer S3 не трактовал список имён как MUST_FIX (фокус на маркерах и пр.).

### 3.3. Смежные (adjacent) — «без хардкода» в Why, но другой класс

- `nastroechnaya-tablitsa-knopok`: Why = без хардкода **шаблонов/видов** → настроечная таблица (сработало как продуктовое требование).
- `klient-zapusk-knopok-shablonov`: design «не хардкод формы Исполнения» → штатный `ОткрытьФормуВыполненияЗадачи`.
- `podpisanie-cherez-soglasovanie`: условие через УсловияМаршрутизации, не хардкод видов.

Эти кейсы показывают: когда «без хардкода» явно в Why — проходит. Дыра — когда хардкод подан как **контроль охвата / thin hook**, а не как отказ от настройки/API.

### 3.4. Паттерн протекания

```
Architect: «узкий список имён = безопаснее / меньше вызовов»
    → design без секции «почему не делегировать фильтр callee»
    → writer реализует литералы
    → reviewer: нет Phase под identity-literals
    → verify: tasks/spec могут совпасть с allow-list
    → user reject на accept / extend
```

---

## 4. Класс дефекта (для нового AP)

**Имя (рабочее):** Hardcoded Identity Filter (хардкод-фильтр идентичности)

**Детекторы (эвристики):**

- `ИмяФормы = "Мета.Путь.Формы"` / цепочка `Или` по полным именам форм;
- `ТипЗнч(Объект) = Тип("…")` как **закрытый** перечень видов без настроечной/штатной абстракции, когда рядом уже есть API отбора;
- `ОткрытьФорму("…")` с литералом имени, когда цель есть в макете/настройке/штатном API открытия;
- allow-list строк имён метаданных в хуке расширения «чтобы не звать общий метод».

**Не путать с легитимным:**

- литералы **кодов отказа / ключей протокола** (`"НеСтартован"`, `"Дубль"`) — контракт API, не фильтр охвата UI;
- литералы в тестах/миграциях;
- закрытый набор платформенного enum / вендорский фиксированный список — **только** с явным обоснованием в design.

**Скептическая стойка (копия Phase 2.5):** каждый runtime-фильтр по строковым именам метаданных/форм **виновен**, пока в design нет обоснования «почему не callee / не настройка / не штатный API».

---

## 5. Рекомендуемое встраивание в kit (зеркало Попытка)

### 5.1. AP (реестр)

Добавить AP (следующий свободный номер в семействе, ориентир **AP-055** — уточнить по актуальному max):

- Категория: architecture / maintainability (HIGH→CRITICAL при противоречии design «без хардкода» или при наличии callee-фильтра).
- Remediation: делегировать фильтр API/настройке; хук только вызывает; либо design-секция **Hardcode Justification** с ответом на 3 вопроса (см. ниже).
- MUST_FIX если design/spec запрещают хардкод, а код содержит allow-list.

### 5.2. Architect (обязательный HALT)

В `onec-code-architect.md` + триггер в `architect-gate.mdc` / `existing-mechanism-priority.mdc`:

**Identity Filter Gate:** перед предписанием allow-list имён форм/объектов:

1. Есть ли у callee уже отсев (доп. функция, строки настроек, soft-return)?
2. Является ли список **неизбежно** закрытым (платформа/вендор), а не «пока только эти две формы»?
3. Что ломается при появлении 4-й формы того же класса?

Без ответов в design — **не выбирать** вариант «&После + список имён» как Chosen.

**Smell:** «Scope-as-literals» — охват ADR сведён к литералам имён вместо критерия класса (форма задачи / есть якорь / API).

Шаблон в design.md:

```markdown
## Hardcode Justification (если есть identity-filter)
- Литералы: …
- Почему не фильтр callee/API/настройки:
- Почему набор закрыт навсегда (не «на первый релиз»):
- План при появлении N+1:
```

### 5.3. Reviewer (выделенный проход)

**Phase 2.6 Identity / Hardcode Audit** (или секция внутри Contract Map):

A. Enumerate: сравнения с полными именами форм/метаданных; `ОткрытьФорму("…")`; массивы/списки строковых имён как guard хука.  
B. На каждую находку: `design-justified?` | `callee-can-filter?` | Verdict AP-055.  
C. Completeness: N литералов-фильтров = N строк таблицы.  
D. Если в change Why/Non-Goals «без хардкода» — contradiction = CRITICAL.

Stance: как Phase 2.5 — наличие списка в коде ≠ доказательство необходимости.

### 5.4. Writer

**G21 (Identity Filter Justification):** до добавления `ИмяФормы = "…"` / литерала `ОткрытьФорму` / allow-list имён — HALT; требуется ссылка на design Hardcode Justification или запрет (звать API без списка). Design, предписывающий allow-list без секции обоснования — конфликт G20-style → HALT к оркестратору.

### 5.5. Orchestrator / verify (лёгкий)

- В design-challenge / task-readiness: чеклист «есть ли identity-literals без Hardcode Justification».
- Grep-хелпер post-apply (опционально): `ИмяФормы = "` в touched modules → сигнал в verify Layer code-truth / hygiene (не замена Phase 2.6).

---

## 6. Связь с текущей прикладной ЗНИ

`prerelease-fix-knopki-shablonov` уже зафиксировала правильный продуктовый ответ (S3-C / D8).  
Код с тремя литералами — **долг apply** после extend, не тема этого исследования.  
Kit-правка нужна, чтобы следующий architect не предложил S3-B снова «как thin».

---

## 7. Вердикт исследования

| Вопрос | Ответ |
|--------|-------|
| Можно ли закрыть одной фразой в standards? | Нет — нужен тот же каркас, что у Попытка |
| Где главная дыра? | Architect **рекомендует** allow-list; reviewer не имеет Phase |
| Достаточно ли Existing Mechanisms? | Нет — не покрывает Scope-as-literals |
| Следующий продуктный шаг | ЗНИ эволюции kit (ветка) по `kit-template-workflow.md` |

---

## 8. Источники

- `.cursor/agents/onec-code-reviewer.md` — Phase 2.5
- `.cursor/agents/onec-code-writer.md` — G14/G19/G20
- `.cursor/agents/onec-code-architect.md` — Data Contract Gate
- `.cursor/rules/existing-mechanism-priority.mdc`
- `.cursor/rules/bsl-antipatterns.mdc`
- `.cursor/docs/standard/reviewer-checks.md` — Phase 2.5
- `openspec/changes/prerelease-fix-knopki-shablonov/design.md`, `debug.md`
- `openspec/changes/archive/2026-08-06-ssylka-tablitsa-knopok-dop-funkcii/`
- `openspec/changes/archive/2026-08-07-nastroechnaya-tablitsa-knopok/`
- Пример кода: `РаботаСБизнесПроцессамиВызовСервера` pav_ФормаЗадачиПриСозданииНаСервере
