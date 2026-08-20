---
report_type: design-challenge
generated_at: 2026-08-19
agent: onec-code-architect
mode: design-challenge
scope:
  change: kit-session-noapi-visibility-and-ru-progress
  design_mtime: "2026-08-19T15:48:37+09:00"
  files:
    - openspec/changes/kit-session-noapi-visibility-and-ru-progress/proposal.md
    - openspec/changes/kit-session-noapi-visibility-and-ru-progress/design.md
    - openspec/changes/kit-session-noapi-visibility-and-ru-progress/tasks.md
    - openspec/changes/kit-session-noapi-visibility-and-ru-progress/specs/session-api-mode/spec.md
    - openspec/changes/kit-session-noapi-visibility-and-ru-progress/specs/chat-surface-clarity/spec.md
    - openspec/changes/kit-session-noapi-visibility-and-ru-progress/specs/chat-model-profiles/spec.md
    - openspec/changes/kit-session-noapi-visibility-and-ru-progress/specs/sequential-gate-questions/spec.md
    - openspec/changes/kit-session-noapi-visibility-and-ru-progress/specs/subagent-model-mapping/spec.md
verdict: APPROVE
confidence: high
open_questions_count: 0
---

## KB references

- Existing Knowledge: not relevant — таксономия отсутствует; discovery без совпадений, фактов KB нет, конфликтов нет.
- ADR-0004 (Load-Bearing): used — ось «не печатать токен, не плодить режим, in-flight не отменять» сохранена; design extends наблюдаемость, не revoke.
- ADR-0001 (Load-Bearing): used — канон одной русской строки без слага/имён агентов; язык `/opsx:*` в бюджете чата, не новый слой стиля.

## Адверсариальная установка

Повторный разбор как чужой работы: прочитаны `proposal.md` (`## Why`, `## What Changes`), `design.md` (Context / Decisions / Behavior Contract / Options / Slices), пять дельт `specs/**/spec.md`, `tasks.md`. Текущие точки вставки сверены с kit-файлами (бюджет чата §5/§6, `opsx-output-style.md` §2, Metadata Gate 1.5, apply Metadata Prep). Отчёты `reports/architecture-*.md` и предыдущий design-challenge **не** использовались как источник истины. Ось «дописать существующие правила, ноль новых механизмов» не открывается. `closed_decisions: []`.

## Сверка пробелов (по текущим файлам)

| Проверяемый пробел | Где закрыт | Статус |
|---|---|---|
| Диагноз Why: канон уже есть; сбой = on-demand vs момент после сбоя; триггер в always-apply бюджете §5 (S1.14) | proposal `## Why`; design Context + D2; spec `session-api-mode` Requirement «Видимость…» (обязанность из always-apply разбора сбоя, не только on-demand); tasks S1.14 + S1.8 | закрыт |
| Приоритет языка `/opsx:*` в бюджете §6; `opsx-output-style` §2 — отсылка | design D6; spec `chat-surface-clarity` (язык задаёт runtime-бюджет); tasks S2.1 + S2.4 | закрыт |
| Дельта `chat-surface-clarity`: английские каркасы как примеры, не MUST NOT-список | spec: «примеры провала, не нормативный запретный список»; design D5; tasks S2.1 | закрыт |
| Поздний BSL: `n/a` = плейсхолдер на apply (S3.6); Scenario «Поздний BSL — вопрос на apply» | design D8; spec `sequential-gate-questions` Scenario; tasks S3.6 + S3.5 + optional в S3.accept | закрыт |
| D8 эвристика по постановке / «Постановка ЗНИ» на 1.5, не по Impact; пропуск `n/a` закрывает гейт | proposal What Changes п.6; design D8; spec Requirement; tasks S3.1 | закрыт |
| Приёмка S1 — чтение §5, не смоделированный лимит | tasks: «Приёмка: чтение правил kit и FAQ»; S1.accept Primary = наличие триггера в §5; S1.8 — сверка по тексту | закрыт |

Текущий kit подтверждает адреса: stub `chat-output-budget.mdc` уже имеет **Subagent (§5)** и **Progress marker (§6)**; полное тело — «### 5. Subagent result protocol» и «### 6. Progress marker»; `opsx-output-style.md` §2 — «Типографика и языки»; `/opsx:new` шаг 1.5 — Metadata Gate; apply Metadata Prep пока ловит `<developer>` / `<ФИО>`, не `n/a` — это как раз работа S3.6, не дыра постановки.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** канон в правиле уже есть, в чате его нет, потому что текст лежит в on-demand правиле (читают **до** вызова), а обязанность наступает **после** сбоя; токен `-noapi` оркестратор не печатает, платформа пишет про смену модели; progress `/opsx:*` уходит по-английски; на `/opsx:new` лишний вопрос маркера, если BSL не предполагается.
- **Design адресует:**
  - Why «канон есть / в чате нет / момент после сбоя» → D1+D2: тот же текст канона; триггер в always-apply §5 разбора сбоя субагента; не новый текст и не печать токена.
  - Why «платформа пишет fallback» → D2: текст платформы не протокол и не замена канона; spec MUST NOT цитировать.
  - Why «английский progress» → D5+D6: MUST русский в §6; приоритет языка команды над Communication; гайд стиля — отсылка.
  - Why «лишний маркер на kit-ЗНИ» → D8: вопрос только по постановке на шаге 1.5; без BSL сразу `n/a` и гейт закрыт; поздний BSL — apply / `marker_scope`.
- **Покрытие:** полное. Симптом «человек не увидел режим» не подменяется «добавить ещё один канон»; симптом «английский progress» не подменяется HALT-списком глаголов; симптом «лишний вопрос» не подменяется новым гейтом.

### Q2 — Optimality

- **Выбранный путь:** дописать существующие правила (видимость в §5, язык в §6, условие маркера на 1.5 + перехват `n/a` на apply); 0 новых механизмов.
- **Альтернативы (не из `## Implementation Options`):**
  1. **Отдельный always-apply файл «сигнал лимита»** — тот же канон, но новый SSOT рядом с бюджетом. Плюс: явный дом обязанности. Минус: лишний файл, разъезд со §5 (оркестратор уже классифицирует `Task failed` там). Хуже по числу точек правки; ось «ноль новых механизмов» не улучшает.
  2. **Канон только в timeline / status line IDE, без первой строки чата** — меньше строк в чат. Минус: Why — человек смотрит в чат и первым видит английский абзац платформы; без чатовой строки инцидент повторяется.
  3. **Триггер канона скопировать в каждый `SKILL.md` `/opsx:*`** — ближе к команде. Минус: N копий, сбой `Task` бывает вне одной команды, разъезд. Хуже Blast Radius.
  4. **Язык progress только узким MUST NOT в профиле/роутере, без §6** — один файл профиля. Минус: профиль не читается на каждую progress-строку; runtime-дом — бюджет §6 (это already always-apply). Не закрывает Communication надёжно.
  5. **Поздний BSL спрашивать на extend, не на apply** — отдельный ритуал. Минус: запись маркера происходит на apply при непустом `marker_scope`; extend не обязан случиться. Существующий Metadata Prep — правильный перехват.
- **Вердикт по Q2:** оптимален. Перечисленные пути либо не закрывают Why (status line; только профиль), либо добавляют механизм/копии без выигрыша наблюдаемости. Печать `-noapi` / файл-состояние / третий режим / HALT-глаголы / FAQ-only / всегда спрашивать маркер уже отвергнуты в design и здесь не переоткрываются: они хуже по ADR-0004 или по постановке.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** да
- **Причины:**
  - Диагноз совпадает с реальной дыркой времени: канон уже нормативен, читают правило до вызова, а сказать надо после сбоя — и §5 бюджета уже есть как разбор `failed`.
  - Наблюдаемость не ломает ADR-0004 (токен остаётся словом пользователя; in-flight не отменяется; таблицы ролей нет в scope) и ADR-0001 (одна русская строка без слага).
  - Двойной смысл `n/a` (на new закрывает гейт; на apply при BSL — плейсхолдер автора) записан в D8, spec и S3.1/S3.6 явно, без третьего гейта.
  - Приёмка S1 завязана на чтение §5, а не на инсценировку лимита — для kit-метапроекта это единственный честный критерий.

Нит, недостаточный для challenge: формулировка S1.accept Primary ещё содержит «оркестратор не печатает `-noapi`» без слов «по тексту правил»; метод приёмки среза и S1.9 это закрывают.

## Verdict

**APPROVE** — шесть проверяемых пробелов закрыты согласованно в proposal / design / specs / tasks; оставшиеся альтернативы хуже по Why или по Blast Radius; ось «дописать правила» не требует смены.

## Gaps for design.md

Нет. Implementation_invariant gaps, которые блокировали бы apply, в текущих артефактах не найдены.

## Architectural alternatives

Нет равноправной развилки по коду или наблюдаемому поведению. Различия рассмотренных путей — дом обязанности (новый файл / каждый SKILL / только профиль / только timeline), а не другой видимый контракт для человека. Новую ось не открывать.

## Источники

- proposal.md — `## Why` (канон есть, момент после сбоя; английский progress; лишний маркер); `## What Changes` п.1, 4–6; `## Impact` (§5/§6, отсылка §2, Metadata Gate по постановке, `n/a` на apply).
- design.md — Context; D2, D5, D6, D8; Existing Mechanisms 1/4/6; Behavior Contract; Implementation Options 1; Slices S1–S3 (Primary S1 = триггер в §5; сценарий «Поздний BSL — вопрос на apply»).
- specs/session-api-mode/spec.md — обязанность из always-apply разбора сбоя; MUST NOT печати токена и цитаты платформы.
- specs/chat-surface-clarity/spec.md — русский progress; каркасы как примеры провала, не запретный список.
- specs/chat-model-profiles/spec.md — MAY профиля не меняет язык и не отменяет канон.
- specs/sequential-gate-questions/spec.md — эвристика по постановке; пропуск закрывает гейт; Scenario «Поздний BSL — вопрос на apply».
- specs/subagent-model-mapping/spec.md — отдельный канон «Модель архитектора: Opus 5».
- tasks.md — S1.14, S1.8, S1.accept (чтение правил); S2.1, S2.4; S3.1, S3.6, S3.5.
- Код/правила kit (verified insertion, не реализация среза) — `.cursor/rules/chat-output-budget.mdc` §5 Subagent / §6 Progress marker; `chat-output-budget-full.mdc` §5–§6; `.cursor/docs/opsx-output-style.md` §2; `.cursor/skills/openspec-new-change/SKILL.md` шаг 1.5; `.cursor/skills/openspec-apply-change/SKILL.md` Metadata Prep + `marker_scope`.
- ADR-0004, ADR-0001 — Load-Bearing инварианты, не отменяются.
