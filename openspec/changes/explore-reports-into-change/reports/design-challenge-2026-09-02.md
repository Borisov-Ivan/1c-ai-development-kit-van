---
report_type: design-challenge
generated_at: 2026-09-02
agent: onec-code-architect
mode: design-challenge
scope:
  change: explore-reports-into-change
  design_mtime: "2026-09-02T02:51:24Z"
verdict: CHALLENGE
confidence: high
---

# Design Challenge — explore-reports-into-change

## Адверсариальная установка

Разбор независим от `reports/architecture-*.md` этой ЗНИ: прочитаны `proposal.md`, `design.md`, оба delta-spec, ADR-0001, архивы `chat-surface-clarity` / `kit-evolution-models-economy-profiles` / `explain-after-review-apply-scope`, плюс живые правила kit (`preserve-subagent-reports.mdc`, `openspec-new-change/SKILL.md`, `openspec-explore/SKILL.md`, `.gitignore`, шаблон `handoff-block.md`, каркас журнала explain). Ledger пуст (`closed_decisions: []`) — ось не закрыта, reopen не требуется.

Позиция: выбранный путь закрывает обе боли из Why и не отменяет ADR-0001, но контракт отбора/шапки в текущей редакции недостаточно жёсткий, чтобы приёмка не разъехалась с kit as-is.

## KB references

- Discovery пропущен, таксономия отсутствует — фактов KB нет; секция конфликтов не требуется.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** исследование кладёт полный отчёт в `temp`, а после `/opsx:new` файл остаётся снаружи каталога задачи — `temp` в `.gitignore` (подтверждено `.gitignore`: `temp/`). Открыв отчёт позже, нельзя вспомнить объект проблемы: в файле есть разбор кода, нет исходных вводных (`proposal.md` § Why).
- **Design адресует:**
  - Почему файл не в каталоге ЗНИ → переезд (не копия) типов exploration / trace-analysis / architecture / explain (+ опциональный handoff) в `openspec/changes/<name>/reports/` сразу после появления каталога, до записи proposal/design и до проверки постановки на design (`design.md` Behavior 1, 5, 6).
  - Почему в отчёте нет вводных → шапка `## Вводные` с понятной формулировкой запроса, областью, путями из постановки, симптомом и вопросом (`design.md` Behavior 11–13; spec `explore-report-intake`).
- **Покрытие:** полное по двум болям Why.
  - Why говорит «файл не в каталоге ЗНИ» → design переносит файл в `reports/` ЗНИ и убирает его из `temp` (spec `Reports of this topic move into the change catalog`).
  - Why говорит «открыв отчёт, нет объекта / исходного запроса» → шапка в самом файле отчёта, не в чат-блоке (spec `Intake header names the object` + `Original request is a clear restatement`).
  - Why не требует хранить исследование без последующего `/opsx:new` — это согласовано с Non-Goals (нет каталога сессий, нет обязательного handoff).
  - Сопутствующий разрыв «продолжи вчерашний» после переезда — следствие решения, не подмена Why; без него переезд ломает уже описанный поиск в `openspec-explore/SKILL.md` (Continuity сейчас для неназванной ЗНИ смотрит только `temp/reports/*.md`).

Частичных «Why говорит X → design адресует Z» по самим болям нет. Есть **сужение, которое ещё не зафиксировано в spec/design** (см. Gaps): формулировка «архитектурного разбора» шире, чем отчёт исследования.

### Q2 — Optimality

- **Выбранный путь:** дописать недостающий переход к уже существующему правилу двух корней (`temp/reports/` без ЗНИ, `openspec/changes/<id>/reports/` при ЗНИ — `preserve-subagent-reports.mdc` § ДЕЙСТВИЕ) плюс короткая шапка в файле; чат без перечня путей (ADR-0001 extends).

- **Альтернативы, уже названные в `## Implementation Options` (для полноты атаки, не как «неупомянутые»):** копия вместо переезда; обязательный файл передачи; возврат `openspec/sessions/`; слив всего `temp` без фильтра темы; только правка пути архитектурного отчёта; шапка только оркестратором; дубль всего брифа; слияние с «Для заказчика»; обязательное поле списка отчётов в чат-блоке. Все отвергнуты постановкой / ADR-0001 — повторно не предлагаются.

- **Альтернативы, не упомянутые в `## Implementation Options`:**

  1. **Снять `temp/` из `.gitignore` (или исключение для `temp/reports/`).** Файлы переживают clone/commit без переезда. Плюс: нулевой алгоритм отбора. Минус: Why требует именно каталог **задачи**, а не «файл где-то в git»; в репозиторий попадут брошенные исследования без ЗНИ; соседний архив `kit-evolution-models-economy-profiles` как раз иллюстрирует Why с путями `temp/reports/…` — легализация temp как SSOT эту дыру маскирует, а не закрывает. **Хуже выбранного.**

  2. **Создавать каталог ЗНИ уже в финале `/opsx:explore` (слияние explore→new) и писать отчёты сразу туда.** Плюс: нет окна «файл в temp, каталога ещё нет». Минус: ломает инвариант explore «не создаёт `openspec/changes/` целиком» (`openspec-explore/SKILL.md` § Не делает) и критерий «new без отчётов проходит»; вопрос-профиль остаётся без ЗНИ. **Инвазивнее, не лучше.**

  3. **Отдельный sidecar `reports/intake.md` (или копировать вводные только в `proposal.md` § Context), шапку в теле exploration/trace/architecture не ставить.** Плюс: один файл, меньше правок шаблонов агентов. Минус: Why буквально «открыв **отчёт**» — sidecar и proposal не видны, пока не откроешь второй файл. **Не закрывает Q1.**

  4. **Поля вводных только в YAML front-matter** (у архитектурного отчёта YAML уже есть). Плюс: машиночитаемость. Минус: разработчик 1С, открывая markdown, читает H1 и тело; YAML часто пропускают. Выбранная `## Вводные` после заголовка лучше для человеческой приёмки S2.

  5. **Только цитаты сессии, без запасного glob 48 ч ∩ тема.** Плюс: проще, меньше риска смешать параллельные темы. Минус: в одном ходе explore часто два файла (обследование + архитектурный разбор), а в чат-превью по бюджету уходит путь последнего; `handoff-block.md` цитирует только `report:` архитектурного файла. Без glob соседний `exploration-*.md` того же разбора легко не переедет — это прямо ломает AC «файл из превью / этой темы». Запасной glob оправдан; приоритет цитат над glob уже в design.

- **Вердикт по Q2:** выбранный путь оптимален относительно неупомянутых альтернатив: минимальная инвазивность (расширение save/ingest, не новый контур), попадание в git внутри каталога ЗНИ, шапка в том файле, который открывают, чат без служебного списка (ADR-0001 не отменяется). Ни одна неупомянутая альтернатива не превосходит по Blast Radius / обратимости / попаданию в Why.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** с оговорками.
- **Причины «да»:**
  - Обе боли Why закрываются существующими механизмами kit, а не параллельным хранилищем.
  - Граница чат/файл явно extends ADR-0001 (`design.md` § Blast Radius); обязательный список файлов в `## Постановка ЗНИ` не добавляется — это совпадает с `openspec/specs/chat-surface-clarity/spec.md` (thin chat vs файл) и с архивом `2026-08-01-chat-surface-clarity`.
  - Архив `kit-evolution-models-economy-profiles` оставлен adjacent (Why той ЗНИ с `temp/reports/…` не переписывается) — отмены прецедента нет.
- **Причины оговорок (не «нет» решению, а «ещё не apply-ready»):**
  - Отбор описан как glob «тех же типов» в `temp`, тогда как живой kit кладёт опциональный файл передачи в `temp/explore-handoff-*.md`, не в `temp/reports/` (`openspec-new-change/SKILL.md` шаг 1.b, `opsx-output-style.md`).
  - Префикс `architecture-*.md` в Continuity и в проверке постановки на design уже означает слишком широкий класс файлов (`architecture-new-*`, `architecture-task-readiness-*`, `architecture-extend-coherence-*` — `architect-gate.mdc`, `openspec-new-change/SKILL.md` шаг Design Gate).
  - Страховка шапки «вставить из слотов промпта» может скопировать сырой текст чата и нарушить spec «не дословная цитата».

## Verdict

**CHALLENGE** — направление (переезд в каталог ЗНИ + шапка вводных в файле, чат без перечня путей) решает Why и оптимально, но в `design.md` / specs не зафиксированы три уточнения контракта, без которых приёмка разъедется с kit as-is.

## Gaps for design.md

Уточнения оси (не смена выбранного пути). Закрыть в design/spec до apply.

1. **Путь опционального файла передачи.** В Behavior Contract явно: кандидат `temp/explore-handoff-*.md` (корень `temp/`, не `temp/reports/`). Иначе сценарий spec `Handoff file moves only if it exists` выполняется только если путь случайно процитирован в чате. После переезда — `openspec/changes/<name>/reports/<basename>`; ingest `/opsx:new` / `/opsx:extend` должен искать уже новый путь, а не только `temp/explore-handoff-*`.

2. **Положительный allowlist имён, не префикс `architecture-*`.** Для переезда и для поиска «продолжи вчерашний» (glob 7 дней по `openspec/changes/*/reports/`):
   - брать: `exploration-*`, `trace-analysis-*`, `explain-*`, `explore-handoff-*`, и архитектурный отчёт исследования вида `architecture-YYYY-MM-DD.md` / `architecture-YYYY-MM-DD-<тема>.md`;
   - не брать (даже если лежат в `temp` или в чужой ЗНИ за 7 дней): `architecture-new-*`, `architecture-new-selfreview-*`, `architecture-task-readiness-*`, `architecture-extend-coherence-*`, `architecture-precedent-coherence-*`, `architecture-review-*`, `design-challenge-*`, `quality-control-*`, `verification-*`, `resolved-contract-*`, `handoff-*`, `code-map*`, `slice-acceptance-*`.
   - Обоснование kit: Continuity без имени ЗНИ сегодня — `Glob temp/reports/*.md`; после переезда design расширяет поиск на все каталоги ЗНИ. Без allowlist «вчерашний разбор» начнёт предлагать отчёты приёмки/проверки постановки соседних задач. Для переезда из `temp` риск ниже (эти файлы обычно пишутся уже внутри ЗНИ), для Continuity — высокий.

3. **Источник поля «Исходный запрос» при дописывании шапки оркестратором.** Spec `Original request is a clear restatement` запрещает дословную цитату. `design.md` Behavior 15 говорит «вставить блок из слотов промпта» — слоты сейчас несут сырой якорь / текст пользователя (`user-goal` / первое сообщение), не гарантированную переформулировку. Зафиксировать: SSOT формулировки = подтверждённый слот «Вопрос» брифа (уже сжатый смысл); если есть только сырая реплика чата — оркестратор MUST сжать в 1–2 предложения и MUST NOT вставлять реплику целиком. Поле «Объекты / пути» по-прежнему только из названного пользователем (пусто → «не указаны»), без вывода из кода.

4. **Граница шапки vs отчёты приёмки.** Spec `Intake header names the object` формулирует «архитектурного разбора» без ограничения mode. Why — про отчёт исследования, который открывают после постановки. Зафиксировать: `## Вводные` обязательна для exploration / trace-analysis и для архитектурного отчёта **исследования** (тот, на который ссылается `report:` в постановке / mode записи в каталог без ЗНИ). Не требовать ту же пятипольную шапку у `architecture-new-*`, task-readiness, design-challenge и прочих отчётов проверки постановки — это не боль Why и размывает «названное пользователем». Журнал explain по-прежнему без второй шапки при заполненной «Мета» (уже в spec).

5. **Порядок относительно Design Gate — оставить как MUST (сейчас есть, не ослаблять).** `openspec-new-change/SKILL.md` шаг Design Gate ищет `architecture-*.md` **в `reports/` ЗНИ** и `report: <path>` только если path существует. Переезд **до** записи proposal/design закрывает дыру «в постановке `report: temp/reports/…`, файла на диске уже нет / каталог ЗНИ пуст». Перепись `report:` → `reports/<basename>` обязательна, иначе проверка постановки смотрит в gitignore-путь. Это не развилка, а инвариант реализации; в design он есть (Behavior 1, 6) — в задачах apply не переставлять.

6. **Ссылки журнала explain.** Архив `2026-08-09-explain-after-review-apply-scope` и шаблон `.cursor/skills/openspec-explain/templates/explain-report.md` уже задают разную глубину href к `src/` (`temp/reports/` → `../../src/`, change/reports → `../../../../src/`). Behavior 6 это упоминает; в spec promote нет отдельного scenario «относительные ссылки журнала живы после переезда». Добавить scenario или явно включить в `Extend from temp` / `Reports of this topic move`: после переезда nav-link в `explain-*` указывает на `src/` с глубины каталога ЗНИ, не остаётся `../../src/` от temp.

Не gaps (атаковал, отверг):

- Отмена ADR-0001 / поле «Отчёты исследования» в чат-блоке — это revoke архива `chat-surface-clarity`, не улучшение Why. В постановке и Blast Radius уже extends.
- Переписать Why архива `kit-evolution-models-economy-profiles` — adjacent, вне scope.
- Копия вместо переезда — пользователь и proposal требуют переезд; два источника хуже для Continuity и gitignore.
- Обязательный handoff / возврат sessions — Non-Goals, больше контуров.

## Architectural alternatives

Нет двух равноправных путей по наблюдаемому поведению, которые стоило бы развиливать. Неупомянутые варианты в Q2 либо не закрывают Why, либо заметно инвазивнее. Уточнения выше — сужение контракта выбранного пути.

## Источники

- proposal.md — § Why (temp / gitignore / нет вводных в отчёте); § What Changes п.1–5; § Decisions п.1 (extends ADR-0001, adjacent kit-evolution); § Acceptance Criteria.
- design.md — § Goals / Non-Goals; § Existing Mechanisms п.1–6; § Behavior Contract п.1–20; § Implementation Options; § Blast Radius; § Decisions п.1–10; mtime `2026-09-02T02:51:24Z`.
- specs/explore-report-promote/spec.md — переезд, new без отчётов, параллельные темы, extend из temp, Continuity, confirm без списка путей, handoff только если есть.
- specs/explore-report-intake/spec.md — шапка объекта, понятная формулировка (не цитата), страховка при записи, «Для заказчика» отдельно, Мета explain, бриф не файл, чат без списка отчётов.
- ADR-0001 — Load-Bearing: thin chat vs полный материал в reports; не предлагается отмена.
- archive/2026-08-01-chat-surface-clarity/ — capability `chat-surface-clarity`; thin chat без Schema/служебных перечней.
- archive/2026-08-18-kit-evolution-models-economy-profiles/proposal.md § Why — источники `temp/reports/exploration-2026-08-16-*.md` (adjacent, не переписывать).
- archive/2026-08-09-explain-after-review-apply-scope/ + `openspec-explain/templates/explain-report.md` — журнал explain, относительные href `src/` зависят от корня отчёта.
- Kit as-is (verified): `.gitignore` (`temp/`); `preserve-subagent-reports.mdc` (два корня, переезда нет); `openspec-explore/SKILL.md` Continuity (`temp/reports/*.md` за 7 дней; каталог ЗНИ — только если пользователь назвал имя); `openspec-new-change/SKILL.md` ingest `temp/explore-handoff-*.md` и Design Gate `reports/architecture-*.md`; `templates/handoff-block.md` поле `report: temp/reports/architecture-YYYY-MM-DD-<slug>.md`; `architect-gate.mdc` закрытие по `architecture-*.md` в change **или** `temp/reports/`.
