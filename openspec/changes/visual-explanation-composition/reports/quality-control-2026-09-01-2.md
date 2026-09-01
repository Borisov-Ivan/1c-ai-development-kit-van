# Quality Control — visual-explanation-composition

- date: 2026-09-01
- file: `reports/quality-control-2026-09-01-2.md`
- mode: slice (`# Срез S1`, `# Срез S2`)
- sources: `tasks.md`, `design.md`, `proposal.md`, `specs/visual-explanation/spec.md`
- closed decision (не развилка QC): две отдельные приёмки; срезы не сливать, пока 8b/9 не сработали
- пересчёт: критерии 5b, 8, 8b, 10 заново по текущему `tasks.md` (прошлый отчёт не копировался)

Mechanical pre-checks (verify 7A–7E, 7.5, 2.1a) приняты как вход: чекбоксы на месте; по одному `S<N>.accept` и `<!-- slice-gate -->`; `form_mode: n/a`; DENY-маркеров User Task Contract в `S<N>.<M>` нет; S2.4 — ALLOW-agent «верифицировать по файлам kit»; маркеров ручной конфигурации 1С в `S<N>.<M>` нет.

## Verdict

`OK`

## Slice Summary

| Slice | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---|---|---|---|---|
| S1 Читаемое объяснение механизма слоями | После ответа про механизм из нескольких слоёв панель предлагается или открывается по просьбе; на полотне вопрос, вывод, скелет и одна сцена | S1.1–S1.5 `[x]`; S1.accept `[ ]` | S1.accept (16/16 Scenario из Связь + 1 mandatory Primary) | нет | `<!-- slice-gate -->` есть |
| S2 Полотно как спутник сопоставления | По просьбе отметить отличия уже сказанного сопоставления полотно показывает классы сразу, без конвейера и без пачки кнопок | S2.1–S2.4 `[ ]`; S2.accept `[ ]` | S2.accept (6/6 Scenario из Связь + 1 mandatory Primary) | нет | `<!-- slice-gate -->` есть |

Размер ЗНИ: 11 чекбокс-задач (Standard). Второй срез допустим: у каждого среза свой наблюдаемый исход (скелет+сцена vs классы сразу). Follow-up вне срезов — не в подсчёте приёмки.

## Scenario Coverage

Spec: 7 требований, 22 `#### Scenario:` в `specs/visual-explanation/spec.md`. Покрытие = Primary, optional-буллет accept **или** `S<N>.<M>` (покрытие только задачей агента — допустимо).

| Scenario | Covered by | Status |
|---|---|---|
| Разбор механизма слоями — панель или намёк | S1 Primary; S1.accept optional; S1.1, S1.3, S1.5 | covered |
| Ветвление в ответе | S1.accept optional; S1.1, S1.5 | covered |
| Простой факт без панели | S1.accept optional; S1.1, S1.5 | covered |
| Три буллета без связей | S1.accept optional; S1.1, S1.5 | covered |
| Проверка постановки без автопанели | S1.accept optional; S1.1, S1.5 | covered |
| Просьба на проверке постановки | S1.accept optional; S1.1, S1.5 | covered |
| Отказ «без схемы» в сессии | S1.accept optional; S1.1, S1.5 | covered |
| Правило о условиях — не всегда таблица | S1.accept optional; S1.1, S1.5 | covered |
| Сравнение свойств — таблица допустима | S2.accept optional; S1.2, S1.5, S2.2 | covered (срез-хозяин S2) |
| Таблица свойств без обязательных кнопок | S2.accept optional; S2.2, S2.4 | covered |
| Неизвестный жанр не даёт отказ | S2.accept optional; S2.1, S2.4 (упоминание в S1.5 — сверка старого правила S1, не хозяин сценария) | covered (срез-хозяин S2) |
| Сложная схема упрощается | S1.accept optional; S1.1, S1.2, S1.5 | covered |
| Много частей — скелет, не сетка | S1.accept optional; S1.2, S1.5 | covered |
| Нет среды панели | S1.accept optional; S1.5 | covered |
| Одна сцена на скелете | S1 Primary; S1.accept optional; S1.1 | covered |
| Почему одного наивного шага мало | S1.accept optional; S1.1 | covered |
| Плакат всех случаев не публикуется | S2.accept optional; S1.2, S1.5, S2.2 | covered (срез-хозяин S2) |
| Сопоставление уже сказанных классов | S2 Primary; S2.accept optional; S2.1, S2.4 | covered |
| Смешанный источник не даёт конвейер | S2.accept optional; S2.1 | covered |
| Полотно без водяного текста | S1.accept optional; S1.1, S1.5 | covered |
| Координатный граф не публикуется | S1.accept optional; S1.1, S1.5 | covered |
| Нет метатекста про панель | S1.accept optional; S1.1, S1.5 | covered |

Имена в ёлочках `S<N>.accept` совпадают с заголовками `#### Scenario:` буквально. Чужих Scenario в чеклистах accept нет: S1.accept держит только 16 из своей Связь; S2.accept — только 6 из своей Связь. Сценарии S2, упомянутые в телах S1.2/S1.5, в `S1.accept` не входят — `accept-bullet-foreign-scenario` не срабатывает.

## Dependency Graph

```mermaid
graph TD
  S1["S1 механизм слоями"]
  S2["S2 спутник сопоставления"]
  S1_1[S1.1 SKILL]
  S1_2[S1.2 panel-shell]
  S1_3[S1.3 explore]
  S1_4[S1.4 ADR авто]
  S1_5[S1.5 сверка kit]
  S1a[S1.accept]
  S2_1[S2.1 SKILL]
  S2_2[S2.2 библиотека рецептов]
  S2_3[S2.3 ADR форма]
  S2_4[S2.4 сверка kit]
  S2a[S2.accept]
  S1_1 --> S1_5
  S1_2 --> S1_5
  S1_3 --> S1_5
  S1_4 --> S1_5
  S1_5 --> S1a
  S2_1 --> S2_4
  S2_2 --> S2_4
  S2_3 --> S2_4
  S2_4 --> S2a
```

- Циклов нет.
- Forward-зависимости приёмки нет: `**Зависимости:**` у обоих срезов — `нет`.
- Объявленных мёртвых зависимостей нет.
- Общие файлы (навык, шаблон, ADR-0010): S2 переписывает те же пути после `[x]` на S1.1–S1.5. Это порядок работ на пересекающихся markdown, не «приёмка S1 требует S2» и не незадекларированная зависимость *приёмки*. Граф design: «S2 → нет». Слияние по этому факту не предлагается (closed decision; 8b/9 не сработали).

## Criteria evaluation (пересчёт)

### 1. Scenario Coverage

Все 22 Scenario покрыты. Implementation-only нет: все сценарии — наблюдаемое поведение панели; агентский путь S1.5 / S2.4 — static «по файлам kit» (ALLOW-agent), не user-spike.

### 2. Slice Independence

Каждый срез принимаем без следующего. Primary различны (скелет+одна сцена ≠ классы сразу). Циклов нет. Forward acceptance dependency нет → критерий 8b не дублирует здесь падение.

### 3. Slice Completeness

Kit-поставка, `form_mode: n/a`, слоёв 1С (метаданные / форма / BSL) нет. Для S1 Primary достаточны навык, шаблон-скелет, слот исследования, ADR-авто, сверка. Для S2 Primary достаточны навык (работа/язык), библиотека рецептов, ADR-форма, сверка. Пропусков слоя, нужного для приёмки, нет. Фикстура слепого прогона S2 — Open Question design, вне scope QC (тестовые данные).

### 4. Slice Dependency Graph

Совпадает с метаданными. См. граф выше.

### 5. Slice Gate Integrity

Ровно один `S1.accept`, ровно один `S2.accept`, по одному `<!-- slice-gate -->`. Legacy `T<M>` нет.

### 5b. Acceptance Checklist Coverage (пересчёт)

| Проверка | S1 | S2 |
|---|---|---|
| `**Primary acceptance:**` в metadata | есть (GWT: слои → просьба/путаница → вопрос, вывод, скелет, текущий шаг; не сетка-сток; не каталог шагов процесса; нет пути в чате) | есть (GWT: уже сказанные классы + просьба об отличиях → одно полотно сопоставления; не ветка процесса; без пачки кнопок; нет пути в чате) |
| `**Primary (обязательно):**` в accept | есть, текст совпадает с metadata | есть, текст совпадает с metadata |
| mandatory sub-bullet пуст | нет | нет |
| Scenario из spec нигде | нет | нет |
| Scenario чужого среза в accept | нет (16 optional = Связь S1) | нет (6 optional = Связь S2) |

Семь буллетов с пометкой «(опционально, покрыто S1.1)» **не** blocking: по правилу среза 6 `[x]` на accept = только Primary. Дубль «optional + S1.1» допустим. `primary-acceptance-missing` / `accept-checklist-empty` / `accept-bullets-missing-scenario` / `accept-bullet-foreign-scenario` — не эмитируются.

### 6. Rework Risk

Пересечение файлов S1/S2 осознано extend (E-D1, design Slices). S2.1 явно сохраняет рецепт скелета для разбора механизма; S2.2 оставляет рецепт скелета. Повтор Primary нет. Алерт не эмитируется: риск повторного осмотра S1 после правки тех же файлов — операционный порядок apply, не дефект нарезки. Слияние не рекомендуется.

### 8. Slice Verticality (пересчёт)

Семантика, не grep.

- S1 mandatory Primary: человек просит схему или дочитывает ответ про слои → рядом с чатом панель с вопросом, выводом, скелетом и текущим шагом. Это black-box (кнопка среды, вид полотна, отсутствие пути в чате), не вызов функции / тип возврата / код-ревью API.
- S2 mandatory Primary: человек открывает панель по просьбе к уже сказанному сопоставлению → видит классы сразу, не конвейер и не пачку кнопок. Тоже black-box.

`slice-not-vertical` не срабатывает: у обоих срезов mandatory Primary наблюдаем.

### 8b. Self-Achievable Acceptance (пересчёт)

Пара S1 / S2:

- Механически GWT: user-journey не совпадают (скелет+шаг истории vs классы сопоставления; разные Then, разный экран).
- Слой S1 Primary (навык авто/рассказ, шаблон скелета со сценами) есть в S1.1 и S1.2, не только в S2.
- Слой S2 Primary (работа над текстом до виджетов, рецепт классификации без обязательных кнопок) есть в S2.1 и S2.2; `**Зависимости:**` у S2 не `S1`.
- Семантика: S1 Primary достижим задачами S1 без S2; S2 Primary достижим задачами S2 (рецепт скелета S2 сохраняет, не заимствует как единственный путь приёмки S1).

`slice-accept-not-self-achievable` не срабатывает. Remediation «объединить срезы» **не** предлагается (8b не сработал; closed decision).

### 9. Foundation slice with gate

Условия критерия — **все** сразу. S1 имеет accept и gate. S2 **не** объявляет `Зависимости: S1`. S1.accept — user-journey, не programmatic-only. Условие «S1 programmatic / S2 UX» ложно.

`slice-foundation-with-gate` не срабатывает. Слияние не предлагается.

### 10. Acceptance Simplicity (пересчёт)

Mandatory (без «опционально») black-box journey в теле accept:

- S1: один — `**Primary (обязательно):**`. Остальные 16 помечены «(опционально)» (включая семь «покрыто S1.1»). When Primary содержит «попросить схему **либо** дочитать ответ» — два входа в **тот же** Then, не два mandatory journey.
- S2: один — `**Primary (обязательно):**`. Шесть Scenario — «(опционально)».

`acceptance-simplicity-overload` не срабатывает.

### 11. User Task Contract

Строки `^- \[[ x]\] S\d+\.\d+`: DENY-маркеров нет (вход verify 2.1a). Семантика: S1.1–S1.4 / S2.1–S2.3 — правки файлов kit агентом; S1.5 / S2.4 — «верифицировать по файлам kit» (ALLOW-agent). Ручной осмотр панели — только `S<N>.accept` и поле `**Приёмка:**`. Условных цепочек «после verify/стенда» нет. `user-task-contract-violation` не срабатывает.

### Task readability

Не-accept задачи: глагол + путь файла + изменение + зачем + опорные D/Scenario. Исключения: `S<N>.accept` (бизнес-результат в заголовке есть); Follow-up с префиксом. `task-opaque-title` / `task-too-short` / `task-opaque-acceptance` не эмитируются. Тела accept: по одной строке на каждый Scenario из Связь данного среза.

## Alerts

Нет.

## Recommendations

### Automatic fix

Нет.

### Decision required

Нет. Две отдельные приёмки остаются; 8b и 9 не сработали — слияние срезов не предлагается.
