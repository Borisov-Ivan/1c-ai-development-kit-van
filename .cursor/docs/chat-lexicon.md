# Словарь чата (SSOT: жаргон → человеческая замена)

Единый источник для HALT-проверки сообщений оркестратора пользователю. Три слоя; полный grep-паттерн — в конце.

**Критерий:** поймёт ли заказчик-делопроизводитель, не знающий ни 1С-разработки, ни OpenSpec.

Ссылаются: `chat-output-budget.mdc` §7, `opsx-output-style.md` §3.1, `anti-slop.mdc`, `verify-user-communication.mdc`, `tz-lexicon-dictionary.md` (слой «лексика ТЗ»).

---

## Слой 1 — движок OpenSpec

Запрещены в чате (регистронезависимо, вне `` `имя-файла` `` и вне строки «Источники: …»):

`CRITICAL`, `WARNING`, `SUGGESTION`, `Severity`, `Slice Gate`, `Promotion Test`, `Determinism Test`, `Implementation Impact`, `Card consolidation`, `Code-Truth`, `Architect Gate`, `Precedent Regression`, `Phase A`, `Phase B`, `verify_mode`, `verdict:`, `slice-pre`, `slice-post`, `slice-transition`, `Tier`, `Standard` (как метка объёма), `Lite`, `Full`, `low-confidence`, `capability` (как термин движка), `step-by-step`, `checkpoint`, `artifact-hygiene`, `precedent-regression`, `invariant-drift`, `phantom-symbol`, фраза «По документам ЗНИ».

**Дополнительно для `/opsx:verify`:** `Layer 1`…`Layer 5`, `GAP`, `PASS`, `FAIL`, `APPROVE`, `CHALLENGE`, `REJECT`, `GO`, `NO-GO`, `slice coherence`, `code-truth`, `task-readiness`, `design-challenge`, `quality-controller`, `snapshot`, `last_challenge_at`, `novelty`, `SKIPPED-novelty`, `SKIPPED-override`, `Three-Question Challenge`, `Simplicity Check`, `Acceptance Checklist Coverage`, `Internal Coherence`, `Problem-Solution Trace`, `Independent Challenge`, `Implementation Readiness`, «независимый аудит постановки», «согласованность плана», «реализуемость задач», «когерентность», «слой проверки», «слои verify», «гигиена артефактов» (как имя слоя), `тестовая ИБ`, `эталон до перехвата`, `smoke`, `прогнать ручной тест`, `S<N>.T<M>` без расшифровки, `operational этalон`, `baseline ИБ`.

| Термин | Замена в чате |
|--------|----------------|
| Layer N / слой проверки | «проверка постановки» / «проверка задач» (по смыслу) |
| GO / NO-GO | «можно запускать apply» / «apply пока нельзя» |
| design-challenge | «независимая проверка плана» (или не называть) |
| phantom-symbol | «в постановке указано имя, которого нет в коде» |

---

## Слой 2 — workflow OpenSpec

| Запрещено | Замена |
|-----------|--------|
| срез (как единица плана) | этап работ / часть задачи + расшифровка («этап с формой шаблонов») |
| постановка (без контекста) | «план в tasks.md и design.md» / «описание доработки» |
| pivot | «пересмотрели подход» / «сменили направление этапа» |
| scope | «область задачи» / «что входит в доработку» |
| продуктовый выбор | «нужно ваше решение по поведению для пользователя» |
| as-is | «как сейчас работает» |
| extend (как глагол в чате без команды) | «допишу план» + `/opsx:extend …` |
| голый `S<N>`, `S<N>.T<M>` | «этап «…»» из tasks.md или «задача «…»» |
| Option A/B/C/D | «вариант A (…кратко…)» |
| F<N> (Follow-up) | «дополнительная задача «…»» |

Workflow-подстроки verify (запрещены): `apply сейчас`, `apply на свой риск`, `defer apply`, `workaround сейчас`.

---

## Слой 3 — лексика (англицизмы и кальки)

Полная таблица для ТЗ — `.cursor/docs/tz-lexicon-dictionary.md`. В чате оркестратора те же замены:

| Запрещено | Замена |
|-----------|--------|
| checkbox / чекбокс | флажок |
| scope / скоуп | область задачи |
| feature / фича | функциональность, доработка |
| flow / флоу | порядок действий, процесс |
| impact | последствия, область влияния |
| handler / хэндлер | обработчик |
| callback / коллбэк | обратный вызов |
| deploy / деплой | развёртывание, обновление |
| UI | интерфейс |
| когерентность | согласованность |

---

## Разрешено в чате

- Одна строка **`Источники: …`** с техническими кодами.
- Имена команд `/opsx:*` и путей `reports/…`.
- Backticks для **имени файла** или **команды**, не для severity.

---

## Grep-паттерн (pre-send, выборочно)

Оркестратор прогоняет сообщение по слоям 1–2; слой 3 — по `tz-lexicon-dictionary.md` Grep-паттерну при verify/doc-tz.

**Last updated:** 2026-05-30
