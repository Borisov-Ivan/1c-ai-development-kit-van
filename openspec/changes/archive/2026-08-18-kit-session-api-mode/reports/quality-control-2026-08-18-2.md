# Quality Controller — Slice Coherence

- Change: `kit-session-api-mode`
- Date: 2026-08-18 (прогон 2, после repair постановки)
- Mode: slice (`# Срез S1`, `# Срез S2` в `tasks.md`)
- Domain: kit-метапроект (правила / команды / FAQ; информационной базы 1С нет). Наблюдаемость Primary — сессия Cursor, не отладчик 1С.
- Scope: `proposal.md`, `design.md`, `tasks.md`, `specs/session-api-mode/spec.md`. Критерии 1–6, 8, 8b, 9–11 + читаемость задач.
- Prior: `reports/quality-control-2026-08-18.md` (13/13 Scenario). Repair: Scenario «Токен на дешёвой команде» (S1.12), «Разовый слаг и токен в одном сообщении» (S1.13); палитра spec включает explore/extend. Объединение срезов не требуется и не рекомендуется.
- Constraints: не оценивать исполнимость приёмки «прямо сейчас»; structural user-spike в `S<N>.<M>` — in scope.

## Verdict

`OK`

Два среза с самостоятельными исходами: S1 — режим сессии по ключу в чате; S2 — обнаруживаемость в FAQ и палитре. Primary каждого среза один, наблюдаемый, достижим своими задачами. 15/15 Scenario покрыты. Foundation-среза нет. User-spike в `S<N>.<M>` нет.

## Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1 Режим сессии | В чате `-noapi` / `-api` и память после лимита управляют дорогими вызовами; таблица ролей не ломается | S1.1–S1.13 (13) | `S1.accept` (7/12; 5 в S1.8–S1.10, S1.12, S1.13) | нет | да `<!-- slice-gate -->` |
| S2 Подсказка в палитре | Пользователь видит, что ключ можно написать в чате, не ища его у каждой команды | S2.1–S2.9 (9); `Режим apply: mechanical` | `S2.accept` (2/3; 1 в S2.9) | S1 | да `<!-- slice-gate -->` |

Notes:

- `form_mode: n/a`. Слои метаданных / форм / BSL для completeness не требуются.
- Размер: 22 рабочих задачи + 2 accept (≥16, Full). Второй срез оправдан отдельным пользовательским исходом (справка), не числом задач.
- Primary S1 и S2 в `tasks.md` совпадают с колонкой `design.md` § Slices.
- Имя Scenario «Ключ без API» в теле `S1.accept` не дублируется отдельным буллетом: это и есть mandatory Primary (канон формата). «FAQ включает и выключает» — то же для S2 Primary.
- Палитра: spec и optional `S2.accept` перечисляют `/opsx:new`, `/opsx:verify`, `/opsx:apply`, `/opsx:explore`, `/opsx:extend`, `/review`, `/release-review`; задачи S2.2–S2.8 покрывают тот же набор.

## Scenario Coverage

Правило: `#### Scenario:` покрыт Primary, optional-буллетом `S<N>.accept` или агентской `S<N>.<M>` (static). User IB/runtime — только через accept.

### session-api-mode → S1 (поведение сессии)

| Scenario | Covered by | Status |
|---|---|---|
| Ключ без API | S1 Primary / `S1.accept` **Primary (обязательно)** | OK |
| Ключ с API | `S1.accept` optional | OK |
| Оба токена в одном сообщении | S1.8 (верифицировать по тексту) | OK |
| Ложное слово не включает режим | S1.9 (верифицировать по тексту) | OK |
| Токен на дешёвой команде | S1.12 (верифицировать по тексту) | OK |
| Новый чат сбрасывает | `S1.accept` optional | OK |
| Память после лимита | `S1.accept` optional | OK |
| Таймаут не липнет | `S1.accept` optional | OK |
| Целостность первого сбоя | S1.10 (верифицировать по тексту) | OK |
| Не путать с пропуском архитектора | `S1.accept` optional; слой S1.5 | OK |
| Эскалация в режиме без API | `S1.accept` optional; слой S1.4 | OK |
| Разовый слаг и токен в одном сообщении | S1.13 (верифицировать по тексту); слой S1.4 | OK |

### session-api-mode → S2 (обнаруживаемость)

| Scenario | Covered by | Status |
|---|---|---|
| FAQ включает и выключает | S2 Primary / `S2.accept` **Primary (обязательно)**; слой S2.1 | OK |
| Подсказка в палитре | `S2.accept` optional; слои S2.2–S2.8 | OK |
| Команда без дорогих вызовов молчит | S2.9 (верифицировать по тексту `opsx-status.md`) | OK |

**Orphans:** нет (15/15). `accept-bullets-missing-scenario` не эмитирован: пять S1-сценариев и один S2 покрыты только `S<N>.<M>` — это допустимо (критерий 5b).

Implementation-only (агент static, не user-spike): «Оба токена в одном сообщении», «Ложное слово не включает режим», «Токен на дешёвой команде», «Целостность первого сбоя», «Разовый слаг и токен в одном сообщении», «Команда без дорогих вызовов молчит».

Смежные, но не дубли: «Токен на дешёвой команде» (S1 — режим всё равно переключается) vs «Команда без дорогих вызовов молчит» (S2 — вывод status без ошибки/справки). Разные `#### Scenario:` spec.

## Dependency Graph

```mermaid
flowchart TD
  S1[S1 Режим сессии]
  S2[S2 Подсказка в палитре]
  S1 --> S2
```

- Cycles: нет.
- Forward acceptance (приёмка S1 требует S2): нет. Primary S1 не ссылается на FAQ/палитру.
- Объявленная дуга: S2 `**Зависимости:** S1`; родитель существует.
- Незаявленных рёбер нет. S1 принимаем без S2 (режим работает без справки). S2 — документационная зависимость, не runtime-фундамент.
- Внутрисрезовые рёбра: S1.8–S1.13 после правок S1.1–S1.7; S2.9 после палитры. Циклов задач нет.

## Criteria

1. **Scenario Coverage** — 15/15. S1: 12 поведения (Primary + 6 optional + 5 static). S2: 3 подсказки (Primary + 1 optional + 1 static). Поимённые `**Связь со spec:**` в `tasks.md` совпадают с `#### Scenario:` spec и со списками `design.md` § Slices.

2. **Slice Independence** — S1 без зависимостей вперёд. S2 зависит только назад (S1). Принятие S1 не требует S2. Исходы различны: поведение оркестратора vs текст FAQ/палитры.

3. **Slice Completeness** — для kit: файлы S1 (`model-selection.mdc`, `tool-name-guard.mdc`, `session-discipline.mdc`) достаточны для Primary «написал `-noapi`». Файлы S2 (`faq-kit.md` + команды с дорогими вызовами) достаточны для Primary «FAQ включает и выключает». `opsx-status.md` — задача S2.9 static, не blocking Primary. Метаданные 1С / формы / BSL не нужны (`form_mode: n/a`).

4. **Slice Dependency Graph** — см. выше. Объявления совпадают с `design.md` («S1 независим. S2 после S1»).

5. **Slice Gate Integrity** — ровно один `S1.accept` и один `S2.accept`; по одному `<!-- slice-gate -->` на срез; дублей и legacy `S<N>.T<M>` нет. Текст маркера совпадает с Primary.

5b. **Acceptance Checklist Coverage** — у обоих срезов есть `**Primary acceptance:**` в metadata и `**Primary (обязательно):**` в accept. Пустого accept нет. Чужих Scenario в чеклистах нет (S1 не содержит FAQ/палитру; S2 не содержит токены/память как Scenario).

6. **Rework Risk** — низкий. S2 не стартует без объявленной зависимости от S1. Одинаковых `#### Scenario:` на двух срезах нет. Факт «не пропуск архитектора» живёт в S1 как поведение (Scenario «Не путать…») и в S2 как текст FAQ (Scenario «FAQ включает и выключает») — разные сценарии spec, ожидаемая связка docs-follows-behavior.

8. **Verticality** — mandatory Primary S1: пользователь пишет ключ в чате → следующий дорогой вызов на модели чата (чёрный ящик сессии Cursor, не вызов функции в отладчике). Mandatory Primary S2: в FAQ видно включение / выключение / отличие от пропуска архитектора (чтение пользовательской справки). `slice-not-vertical` не срабатывает. Поле `**Приёмка:**` S1 допускает чтение правил плюс контрольный ход — supporting method, не замена Primary.

8b. **Self-achievable** — S1 Primary достижим правилами S1.1–S1.7 без файлов S2. S2 Primary достижим S2.1 без повторной смены семантики цепочки. Дубля user-journey S1↔S2 нет. Слоя, нужного Primary S1, в S2 нет (и наоборот). Новые S1.12 / S1.13 — static coverage внутри S1, не выносят приёмку S1 в S2. `slice-accept-not-self-achievable` не срабатывает. Исполнимость «прямо сейчас» в текущем чате / без перечитывания правил — transient, вне scope. Объединение срезов не показано.

9. **Foundation + gate** — условие «S1.accept programmatic-only, а S2 — единственный UX» ложно: у S1 свой наблюдаемый исход. `slice-foundation-with-gate` не срабатывает (нужны все три условия сразу; третье не выполнено).

10. **Acceptance simplicity** — в каждом `S<N>.accept` ровно один mandatory black-box journey. Optional-буллеты помечены «(опционально)». Перегруз 2026-08-17 в текущих `design.md` и `tasks.md` снят.

11. **User Task Contract** — mechanical pre-check: строки `S1.1–S1.13`, `S2.1–S2.9`; DENY-подстрок нет; repair-grep нет. Семантика: S1.8–S1.13 и S2.9 — агент «верифицировать по тексту» (ALLOW-agent static, аналог «по коду» для markdown-правил). Runtime-ход «написать `-noapi`» — только в `S1.accept` / metadata приёмки (граница среза, разрешено). Условных цепочек «после verify S / после стенда» нет. `user-task-contract-violation` не срабатывает.

## Task readability

Паттерн «глагол + файл + результат + (D/ADR)» выдержан на рабочих задачах. Опорные ссылки D1–D7 / ADR-0001 на месте, кроме регресса таблицы ролей S1.11 (цель ясна без голого идентификатора).

- `task-opaque-title` — не эмитирован.
- `task-too-short` — не эмитирован (все `S<N>.<M>` длиннее 8 слов, с путём файла).
- Заголовки `S1.accept` / `S2.accept` содержат бизнес-результат среза, не голое «проверить».
- Имена Scenario в optional-буллетах буквально совпадают с `#### Scenario:` spec (включая explore/extend в палитре).
- `Верифицировать по тексту` — агентский static-путь, не opaque-title. S1.12 и S1.13 следуют тому же шаблону, что S1.8–S1.10.

## Alerts

Нет CRITICAL / WARNING / SUGGESTION.

## Recommendations

### Automatic fix

Нет.

### Decision required

Нет. Срезы не объединять: у каждого свой наблюдаемый исход и свой достижимый Primary.

## Remediation (auto-repair)

Нет алертов — блок не применяется.
