---
name: workflow-orphan-cleanup
overview: Единая итерация улучшения фреймворка opsx — чистка orphan-артефактов вне воркфлоу + UX-санитизация (жаргон в выводе verify, дифференцированная дисциплина правок ЗНИ) + рефакторинг гигантского `1c-agent-patterns/SKILL.md`. Один pull без полу-меры.
todos:
  - id: confirm_choices
    content: "Подтвердить развилки §6: onec-admin, 1c-help-mcp/mcp-tools, opsx-onboard — удалять или оставить"
    status: pending
  - id: delete_dead_docs
    content: Удалить precedent-regression-system-review.md и instruction-system-map.md (§1)
    status: pending
  - id: delete_orphan_agents
    content: Удалить mcp-deploy.md (и onec-admin.md если подтверждено), вычистить ссылки в tool-name-guard.mdc, 1c-utility-agents.mdc, AGENTS.md, openspec/glossary.md (§2)
    status: pending
  - id: delete_onboard
    content: "Если подтверждено: удалить opsx-onboard.md и openspec-onboard/SKILL.md, вычистить AGENTS.md и opsx-output-style.md (§3)"
    status: pending
  - id: delete_phase_gates
    content: Удалить phase-gates.mdc, вычистить vertical-slices.mdc, AGENTS.md, openspec/glossary.md (§4)
    status: pending
  - id: delete_mcp_skills
    content: "Если подтверждено: удалить 1c-help-mcp/SKILL.md и mcp-tools/SKILL.md, вычистить AGENTS.md (§5)"
    status: pending
  - id: ux_glossary
    content: Расширить opsx-output-style §3 — глоссарий перевода технических категорий в человеческий язык (§7)
    status: pending
  - id: ux_verify_templates
    content: Переписать шаблоны Блок 1/2/2b/3/4 в openspec-verify-change/SKILL.md — убрать жаргон из заголовков карточек, перенести технические имена в "Источники" (§8)
    status: pending
  - id: ux_edit_discipline
    content: Закодировать дифференцированную дисциплину — decision-класс через /opsx:extend, hygiene-класс ручная правка разрешена (§9)
    status: pending
  - id: ux_t_codes_cleanup
    content: Вычистить T-* коды в пользовательском выводе скиллов debug, explore, apply, extend, estimate, status (T-* остаются как внутренние шаблоны) (§10)
    status: pending
  - id: refactor_patterns
    content: Разбить 1c-agent-patterns/SKILL.md на ролевые модули + миграция всех входящих ссылок (§11)
    status: pending
  - id: verify_no_broken_links
    content: Grep-проверка всех удалённых имён по .cursor и AGENTS.md — допустимые совпадения только в archive/** (§12)
    status: pending
  - id: verify_no_jargon
    content: Grep по запрещённым жаргон-фразам в шаблонах пользовательского вывода (§12)
    status: pending
  - id: smoke_test_verify
    content: Тестовый прогон /opsx:verify на do2-soglasovanie-povtor-forma-ux-v2 — отчёт читается без словаря терминов (§12)
    status: pending
isProject: false
---

## Метод аудита

Воркфлоу = **21 команда** в [.cursor/commands/](.cursor/commands/) + always-apply правила. Артефакт «в воркфлоу», если на него ссылается транзитивное замыкание команд/скиллов/агентов или always-apply правила. Архивные ЗНИ (`openspec/changes/archive/**`) read-only, не считаются активным потребителем.

UX-санитизация — отдельный пласт: правила коммуникации (`opsx-output-style.md`, `verify-user-communication.mdc`) уже **запрещают** жаргон, но шаблоны в `openspec-verify-change/SKILL.md` сами **зашили** технические имена (`Blast Radius`, `precedent-regression`, `Phase A/B`, `9b`) как заголовки карточек. Чистить — **на слое скилла**, не правил.

---

# Часть 1. Чистка orphan-артефактов

## 1. Точно мёртвые артефакты (0 входящих ссылок)

Удаляются без чистки ссылок (никто на них не ссылается, кроме исходного `framework-ux-cleanup_0fe840c7.plan.md`).

- [.cursor/docs/precedent-regression-system-review.md](.cursor/docs/precedent-regression-system-review.md)
- [.cursor/docs/instruction-system-map.md](.cursor/docs/instruction-system-map.md)

## 2. Агенты, связанные только перечислением

Никакая команда/скилл не вызывает их через `Task(subagent_type="...")`. Следы — только в `tool-name-guard.mdc` enum, `AGENTS.md` справочнике и `openspec/glossary.md`.

- [.cursor/agents/mcp-deploy.md](.cursor/agents/mcp-deploy.md) — деплой MCP-серверов; никем не вызывается.
- [.cursor/agents/onec-admin.md](.cursor/agents/onec-admin.md) — ad-hoc инструмент 1С (PostgreSQL, ibcmd); в opsx не вызывается.

**Чистка ссылок:**
- [.cursor/rules/tool-name-guard.mdc](.cursor/rules/tool-name-guard.mdc) — убрать из enum и описаний.
- [.cursor/rules/1c-utility-agents.mdc](.cursor/rules/1c-utility-agents.mdc) — убрать строку «Управление серверами 1С … → onec-admin».
- [AGENTS.md](AGENTS.md) — снять из «Системные промпты агентов» и таблиц.
- [openspec/glossary.md](openspec/glossary.md) — убрать упоминания.

## 3. Изолированная команда `/opsx:onboard`

На скилл и команду не ссылается ни один другой узел воркфлоу.

- [.cursor/commands/opsx-onboard.md](.cursor/commands/opsx-onboard.md)
- [.cursor/skills/openspec-onboard/SKILL.md](.cursor/skills/openspec-onboard/SKILL.md) (с каталогом)

**Чистка ссылок:**
- [AGENTS.md](AGENTS.md) — убрать `/opsx:onboard` из «Дополнительные» и decision-tree.
- [.cursor/docs/opsx-output-style.md](.cursor/docs/opsx-output-style.md) — снять упоминание T-CONFIRM «используется в /opsx:onboard».

## 4. Legacy-only правило `phase-gates`

Активные ЗНИ не используют (Grep по `openspec/changes/` без `archive/` пуст). Все совпадения — в `archive/**` и `openspec/glossary.md`.

- [.cursor/rules/phase-gates.mdc](.cursor/rules/phase-gates.mdc)

**Чистка ссылок:**
- [.cursor/rules/vertical-slices.mdc](.cursor/rules/vertical-slices.mdc) — убрать секцию-ссылку.
- [AGENTS.md](AGENTS.md) — снять секцию «Phase Gates (DEPRECATED)».
- [openspec/glossary.md](openspec/glossary.md) — снять термин (или пометить как историю без ссылки).

## 5. MCP-навыки вне воркфлоу

Не вызываются ни одной командой/агентом; ссылаются только друг на друга и из навигатора `AGENTS.md`.

- [.cursor/skills/1c-help-mcp/SKILL.md](.cursor/skills/1c-help-mcp/SKILL.md)
- [.cursor/skills/mcp-tools/SKILL.md](.cursor/skills/mcp-tools/SKILL.md)

**Чистка ссылок:**
- [AGENTS.md](AGENTS.md) — убрать «1c-help-mcp, mcp-tools» из «Доменные навыки 1С».

## 6. Развилки, требующие подтверждения

| Артефакт | За удаление | За «оставить» |
|---|---|---|
| `onec-admin.md` | В opsx-воркфлоу не вызывается | Может пригодиться для выгрузки БД через ibcmd, PostgreSQL, перезапуска кластера 1С |
| `1c-help-mcp` + `mcp-tools` | Не вызываются ни одной командой | Поиск по документации платформы через MCP при ручной работе |
| `opsx-onboard` + скилл | Не входит в реальный workflow активных ЗНИ | Если планируется онбординг другого разработчика |

---

# Часть 2. UX-санитизация (жаргон в выводе)

## 7. Глоссарий перевода технических категорий

**Принцип:** Технические имена остаются в **движке** (правила, шаблоны секций design.md, ADR Supersedes, методология `vertical-slices.mdc`). Перевод применяется **только в слое вывода пользователю** — в карточках Блок 2 verify, Executive Summary, follow-up сообщениях.

**«Срез» (vertical slice) — корректный методологический термин**, не переименовывается. Это перевод устоявшегося vertical slice из Agile/SDD: функциональная единица, проходящая через все слои (UI + код + тест) и дающая одну готовую к приёмке возможность. Замена на «Шаг (Step)» сместила бы декомпозицию в горизонтальную (технические подзадачи), что противоречит смыслу `vertical-slices.mdc`. Вместо переименования усиливаем подачу термина пользователю — см. §8 ниже.

**Изменение:** в [.cursor/docs/opsx-output-style.md](.cursor/docs/opsx-output-style.md) расширить **§3 «Запрет внутренних ID в пользовательских полях»** — добавить вторую таблицу «Запрещённые технические категории → как говорим пользователю»:

| Технический термин | Пользовательский язык |
|---|---|
| `Blast Radius` | «Что меняется для пользователя» / «Эффект для конечного пользователя» |
| `precedent-regression` / `9b` | «Отмена ранее принятого решения» |
| `invariant-drift` | «Отклонение от ранее зафиксированного правила» |
| `load-bearing-adr-bypass` | «Обход опорного архитектурного решения» |
| `Phase A` / `Phase B` / `Implementation Impact Gate` / `Card consolidation` | Не показывать вообще; пользователь видит результат («Авто-исправлено» / «Решения» / «Уточнения текста») |
| `decision-класс` / `artifact-hygiene` / `INFO` | Не показывать; разбиение через заголовки секций |
| `slice-pre` | «Проверка до реализации среза» |
| `slice-post` | «Проверка после реализации среза» |
| `slice-transition` | «Переход между срезами» |
| `<!-- slice-gate -->` | Внутренний маркер; в чате не цитируется |
| `accept S<N>` / «срез принят» | «Функция готова: <название среза>» |
| `Promotion Test` / `Determinism Test` | Не показывать; работают внутри verify |
| `CRITICAL` / `WARNING` / `SUGGESTION` | «Блокер» / «Замечание» / «Предложение» (в счётчиках допустимы; в заголовках карточек — нет) |

**Дополнить §3:** правило «Пользовательские поля» — категории ID кодов (`precedent-regression`, `dependency-cycle`, `task-opaque-acceptance` и пр.) допустимы **только** в строке «Источники: …» в самом конце карточки.

## 8. Переписывание шаблонов verify SKILL.md

Корневая причина жалобы пользователя — в [.cursor/skills/openspec-verify-change/SKILL.md](.cursor/skills/openspec-verify-change/SKILL.md) (1162 строки) шаблон карточки на строке ~1268 содержит:

```
### 1. <Заголовок> (<SEVERITY>)
**Blast Radius (обязательно для verify 9b: precedent-regression / invariant-drift / load-bearing-adr-bypass):**
```

После санитизации шаблон становится:

```
### 1. <Заголовок>
**Что не так:** <конкретный дефект, 1 предложение>
**Что меняется для пользователя:**
- <бизнес-эффект; в терминах конечного пользователя>
- <источник: archive change / ADR / KB — с человеческим описанием>
- <альтернативы и обоснование>

**Варианты:**
- 1a — <действие> → <последствие в коде/приёмке>
- 1b — <альтернатива> → <последствие>
- 1c — Принять как есть → <риск>

Источники: precedent-regression-9b ← QC <код> / Architect <критерий>
```

**Изменения:**
- Убрать `(<SEVERITY>)` из заголовка → severity передаётся через визуальную секцию или счётчик в Executive Summary, не в каждой карточке.
- Заменить заголовок поля «Blast Radius» на «Что меняется для пользователя».
- Заменить «Влияние / Код при apply / Поведение системы / Приёмочные шаги / Процесс» на единый человеческий блок «Что меняется для пользователя» с подпунктами без процессного жаргона.
- Технические категории (`precedent-regression`, `dependency-cycle`, `slice-incomplete`, …) только в строке `Источники: …`.

**Также переписать:**
- **Жёсткое правило «Срез всегда с названием»**: в любом пользовательском выводе (Executive Summary, таблицы Slice Acceptance, карточки решений, handoff-сообщения) **запрещено** цитировать голый идентификатор `S<N>`. Только формат `Срез S<N>: «<название из tasks.md>»`. Текущий отчёт `verification-slice-pre-2026-05-09.md` нарушает это в таблице «Slice Acceptance Status» (`S1` без названия). Добавить в self-check verify-вывода (правило 8b в `verify-user-communication.mdc`) пункт: «Каждое упоминание `S<N>` в пользовательском поле сопровождается названием среза». Эталон уже есть в `opsx-output-style.md §10`, но не соблюдается — переводим из «рекомендации» в «обязательное правило» с проверкой в self-check.
- **Краткое определение для пользователя:** в первом сообщении новой сессии apply/verify/extend (один раз на сессию, не дублировать) — справочная строка: «**Срез** — связка UI, кода и тестов, дающая одну готовую к приёмке функцию». Реализуется через шаблон в `opsx-output-style.md` (новый раздел §11 «Глоссарий пользовательских терминов»). При повторных запусках в той же сессии строка опускается.
- **Executive Summary** (шаблон в скилле verify, ~строка 1162-1240): убрать «verdict: FAIL/PASS», «verify_mode: slice-pre/slice-post», «9b», «Phase A/B». Использовать «Готово к реализации / Не готово», «Проверка до реализации среза / После реализации», переход в простой язык.
- **Промежуточные сообщения** «Phase A — Mechanical auto-fix», «Phase B — Show results» (~строка 1242): эти заголовки видны только внутренне в скилле, но по факту попадают в чат через шаги. Переименовать секции вывода: «Авто-исправлено» (уже есть), «Решения» (уже есть), «Уточнения текста» (вместо «Уточнение текста артефактов»), «К сведению» (есть).
- **Self-check 8b** (в `verify-user-communication.mdc`, строки 95-103) — расширить пунктом 7: «Ни одна категория из глоссария §3 opsx-output-style не используется в заголовках, полях, варианте; только в `Источники: …`».

**Что НЕ трогаем (важно):**
- [.cursor/rules/precedent-regression-gate.mdc](.cursor/rules/precedent-regression-gate.mdc) — это **правило движка**. «Blast Radius» — техническое имя секции в `design.md`, на которое ссылаются `architect-gate.mdc`, `verified-cause-gate.mdc`, `adr-format.mdc`, `openspec-ff-change/SKILL.md`, `openspec-extend-change/SKILL.md`. Переименование сломает 5+ файлов и существующие ADR/design.md в архиве.
- [.cursor/rules/verify-user-communication.mdc](.cursor/rules/verify-user-communication.mdc) — оставить как специализацию verify. План правит её точечно (расширить self-check), а не удаляет.
- [.cursor/docs/opsx-output-style.md](.cursor/docs/opsx-output-style.md) — оставить и **расширить** (§3). Этот документ — фундамент для 17 скиллов, удаление = регресс на каждый скилл.

## 9. Дифференцированная дисциплина правок ЗНИ

В соответствии с подтверждённым выбором (`differentiated`):

**Правки класса `decision`** (меняют код / поведение / приёмочные шаги) — **только** через `/opsx:extend <name> --from-verify <report>`. Это включает: пере-нарезку срезов, изменение `Behavior Contract`, добавление/удаление сценариев, переформулировку приёмочных тестов.

**Правки класса `artifact-hygiene`** (текст, формулировка, привязка `Связь со spec`, опечатки) — **разрешены вручную** (StrReplace в файлах ЗНИ). После правки **обязателен** повторный verify (любой правки артефакта ЗНИ).

**Изменения в файлах:**
- [.cursor/skills/openspec-verify-change/SKILL.md](.cursor/skills/openspec-verify-change/SKILL.md), шаг 17 (Phase B): убрать вариант «применить ручную правку для decision-замечаний»; оставить только `1a — /opsx:extend …`, `1b — /opsx:extend …`, `1c — Принять как есть`. Для hygiene-замечаний (Блок 2b) явно разрешить `1a — применить правку` (вручную) с автозапуском повторного verify.
- [.cursor/rules/verify-user-communication.mdc](.cursor/rules/verify-user-communication.mdc), правило 6 «Решения от вас»: добавить ссылку на правило дисциплины — decision = extend, hygiene = ручная.
- [.cursor/skills/openspec-extend-change/SKILL.md](.cursor/skills/openspec-extend-change/SKILL.md): убедиться, что флаг `--from-verify <report>` корректно обрабатывает все decision-категории (precedent-regression, slice-incomplete, suboptimal-architecture).

## 10. Чистка T-* кодов в пользовательском выводе

T-* шаблоны (T-BRIEF, T-HANDOFF, T-REPORT, T-STATUS, T-CONFIRM) — **внутренние имена** макетов, в чате пользователю появляться не должны.

**Проверить и почистить упоминания «Output style: T-…», «по T-REPORT», «T-BRIEF» в**:
- [.cursor/skills/openspec-debug/SKILL.md](.cursor/skills/openspec-debug/SKILL.md)
- [.cursor/skills/openspec-explore/SKILL.md](.cursor/skills/openspec-explore/SKILL.md)
- [.cursor/skills/openspec-apply-change/SKILL.md](.cursor/skills/openspec-apply-change/SKILL.md)
- [.cursor/skills/openspec-extend-change/SKILL.md](.cursor/skills/openspec-extend-change/SKILL.md)
- [.cursor/skills/openspec-estimate/SKILL.md](.cursor/skills/openspec-estimate/SKILL.md)
- [.cursor/skills/openspec-status/SKILL.md](.cursor/skills/openspec-status/SKILL.md)
- [.cursor/rules/verify-user-communication.mdc](.cursor/rules/verify-user-communication.mdc)
- [AGENTS.md](AGENTS.md) — секция «Output style» (опустить ссылку на T-* как видимый код).

T-* остаются **в самом** [.cursor/docs/opsx-output-style.md](.cursor/docs/opsx-output-style.md) как имена шаблонов для авторов скиллов. Но скиллы в **исходящих сообщениях** не цитируют T-коды.

---

# Часть 3. Рефакторинг гигантского `1c-agent-patterns`

## 11. Split на ролевые модули с миграцией ссылок

Файл [.cursor/skills/1c-agent-patterns/SKILL.md](.cursor/skills/1c-agent-patterns/SKILL.md) (1563 строки) ссылается из ~13 точек: `1c-agent-delegation.mdc`, `architect-gate.mdc`, `openspec-debug/SKILL.md`, `openspec-apply-change/SKILL.md`, `openspec-verify-change/SKILL.md`, `openspec-extend-change/SKILL.md`, агентские промпты, `AGENTS.md`. Часто ссылаются на **конкретные секции** («Quality Controller — slice coherence review», «Architect — fix quality review»).

**Структура split:**
- `1c-agent-patterns/SKILL.md` (≤200 строк) — **навигатор**: что где лежит, complexity assessment, общий шаблон INPUT для агентов.
- `1c-agent-patterns/architect.md` — все шаблоны для onec-code-architect (design, plan-review, task-readiness, fix-quality, slice-decomposition, scope-coherence-audit, precedent-coherence-audit, invariant-extraction).
- `1c-agent-patterns/writer.md` — шаблоны для onec-code-writer (light mode, bug fix, contract resolution).
- `1c-agent-patterns/reviewer.md` — шаблоны для onec-code-reviewer (review, prerelease).
- `1c-agent-patterns/explorer.md` — шаблоны для onec-code-explorer.
- `1c-agent-patterns/trace-analyst.md` — шаблоны для onec-trace-analyst.
- `1c-agent-patterns/quality-controller.md` — шаблоны для openspec-quality-controller (slice coherence review).

**Миграция ссылок (обязательная):**
1. Перед split — Grep всех входящих ссылок на «1c-agent-patterns» и подсекций.
2. Каждая ссылка обновляется на новый путь (`1c-agent-patterns/<role>.md#<section>`).
3. После split — повторный Grep по строке `1c-agent-patterns/SKILL.md` без подмодуля; если найдены ссылки на удалённые секции в навигаторе — broken link, чистить.

---

# Часть 4. Контроль и калибровка

## 12. Регресс-проверки после всех правок

**Чистота ссылок (после части 1):**
- Grep по каждому удалённому имени файла (`mcp-deploy`, `onec-admin`, `precedent-regression-system-review`, `instruction-system-map`, `phase-gates`, `openspec-onboard`, `opsx-onboard`, `1c-help-mcp`, `mcp-tools`) с `path=c:\GitHub\PavDO\.cursor` и `path=AGENTS.md`. Допустимое попадание — только `archive/**`. Любое попадание в активные правила/скиллы/команды — провал, дочистить.

**Чистота жаргона (после части 2):**
- Grep по `c:\GitHub\PavDO\.cursor\skills\openspec-*\SKILL.md` фразами: `Blast Radius`, `precedent-regression`, `9b`, `Phase A`, `Phase B`, `Implementation Impact Gate`, `Card consolidation`, `Promotion Test`, `Determinism Test`, `verdict:`, `verify_mode:`, `T-REPORT`, `T-BRIEF`, `T-HANDOFF`. Совпадения допустимы **только** в комментариях для авторов скиллов или в строке `Источники: …`. Любое совпадение в **шаблоне сообщения пользователю** (Executive Summary, заголовки карточек, варианты, тексты) — провал.
- Grep по `c:\GitHub\PavDO\.cursor\rules\verify-user-communication.mdc` и `opsx-output-style.md` — глоссарий §3 присутствует, mapping правильный.
- Регекс `\bS\d+\b(?![\.:])` (голый `S<N>` без точки или двоеточия после) в шаблонах пользовательского вывода скиллов opsx-* — допустим только в формате `Срез S<N>:` или внутри идентификатора задачи `S<N>.<M>` / `S<N>.T<M>`. Любое голое `S1`, `S2` в свободном тексте (таблицы Slice Acceptance, Executive Summary, варианты) — провал; должно быть `Срез S1: «<название>»`.

**Чистота split (после части 3):**
- Grep по `1c-agent-patterns/SKILL.md` (без `/<role>.md`) во всех скиллах/правилах/агентах. Если найдены ссылки на конкретные секции (`#…`), которых больше нет в навигаторе — broken link, обновить.
- Grep по новым модулям (`1c-agent-patterns/architect.md`, …) — каждый должен иметь хотя бы одну входящую ссылку.

**Smoke-test:**
- `/opsx:status do2-soglasovanie-povtor-forma-ux-v2` — убедиться, что нет ошибок file-not-found.
- `/opsx:verify do2-soglasovanie-povtor-forma-ux-v2` — отчёт должен:
  - Не содержать слов `verdict`, `precedent-regression`, `Blast Radius`, `Phase A/B`, `9b`, `verify_mode` в Executive Summary.
  - Содержать в карточке решения по precedent-regression поле «Что меняется для пользователя» (или эквивалент) с описанием в терминах пользователя 1С.
  - Источники алертов остаются (`Источники: precedent-regression-9b`).
  - Hygiene-замечания (Блок 2b) явно предлагают `1a — применить правку` (ручная правка) с пометкой «после правки повторный verify».
- Прочитать сгенерированный `reports/verification-slice-pre-*.md` глазами не-разработчика — должно быть понятно, **что именно** меняется для пользователя без знания терминов opsx.

---

## Что НЕ делаем в этой итерации (явные исключения)

Чтобы план не разрастался — фиксирую границы:

- **НЕ переименовываем** «срез» / `slice` в «Шаг (Step)». Это устоявшийся методологический термин (vertical slice из Agile/SDD), осознанно выбран в `vertical-slices.mdc`. «Шаг» сместил бы декомпозицию в горизонтальную (технические подзадачи), убив смысл модели. Жалоба на «жаргон» решается через §7 (глоссарий перевода slice-режимов) и §8 (правило «Срез всегда с названием»), а не переименованием.
- **НЕ создаём** новый файл `agent-to-user.mdc` (исходный план хотел заменить им `verify-user-communication` + `opsx-output-style`). Анализ показал: `opsx-output-style.md` уже содержит принцип трёх слоёв и запрет ID; добавление третьего файла = новый источник истины + миграция 17 ссылок. Расширяем существующий §3.
- **НЕ переименовываем** «Blast Radius» в правилах движка. Это техническое имя секции в `design.md` и в `architect-gate.mdc`, которое работает как ссылка между `precedent-regression-gate`, `adr-format`, `verified-cause-gate`, ff/extend skills. Переименование = blast radius самого изменения. Перевод — только на слое пользовательского вывода через глоссарий §7.
- **НЕ удаляем** `verify-user-communication.mdc` — там уникальная Phase A/B логика, без которой verify сломается. Точечно правим self-check.
- **НЕ удаляем** `opsx-output-style.md` — на него ссылаются 17 скиллов. Расширяем §3 глоссарием.
- **НЕ удаляем** `onec-code-simplifier` — реально вызывается из `/review` (REFACTOR-замечания, строки 350, 382 в `review/SKILL.md`).
- **НЕ удаляем** `openspec-doc-writer` — вызывается из `/opsx:doc-tz` и `verify` (генерация ТЗ).
