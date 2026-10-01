# Adversarial-аудит `kit-contract-provenance-gate` перед переносом

## Вводные
- Исходный запрос: критически перепроверить целостность внешней ЗНИ перед переносом
- Область: OpenSpec change и контракты verify/new/extend
- Объекты / пути из постановки: C:\GitHub\PavDO\openspec\changes\kit-contract-provenance-gate\
- Симптом: пакет может быть внутренне связным, но избыточным, недоказанным или конфликтующим с текущими изменениями
- Вопрос: какая минимальная доказанная постановка действительно нужна текущему киту?

## Общий вердикт

**CRITICAL — пакет нельзя переносить как ЗНИ целиком.**

Внешний change содержит доказанное ядро проблемы, но не готов к переносу в текущий kit:

1. В пакете нет `tasks.md`; заявленные четыре среза существуют только как проект в `design.md`, без исполнимых задач, `S<N>.accept` и `slice-gate`.
2. Все четыре Primary acceptance завязаны на задачу `do2-template-forbid-add-approvers`, которой в целевом репозитории нет. Она есть только в соседнем репозитории `C:\GitHub\PavDO`, поэтому приёмка после переноса не является самодостаточной.
3. В текущем kit уже реализованы активные изменения `value-efficient-verify` и `verify-stop-repeat`. Они ввели `External Contract Ledger`, авторитет источников, пакет продуктовых развилок, проверку внешней валидности, точечную инвалидацию и повторное открытие темы. Внешний пакет проектировался без согласования с этими действующими контрактами.
4. Решение D5 о закрытии замечания качества общим ответом «принято» противоречит main spec `review-quality-disposition`, Load-Bearing ADR-0003 и always-apply якорю: weak/design-prescribed в apply остаётся открытым до явного disposition в `/review` или `/release-review`.
5. D6 «накопительный рост от первого verify» и D7 «не извлекать `[исполнитель]` в инвариант» — второй ряд. Они не нужны для закрытия исходного симптома, а предложенный расчёт D6 не восстанавливает историческую базу достоверно.
6. Три ADDED capability искусственно дробят одну причинную цепочку и одновременно прячут в `kit-optimality-signal-routing` четыре разных контракта: предупреждение простоты, маршрутизацию review, метрику роста и архивное извлечение.

**Минимальное доказанное ядро:** требования решения должны ссылаться на уже существующий внешний контракт или на явно сохраняемое проверенное поведение; предложенный исполнителем новый пользовательский исход не становится обязательным без решения заказчика; decision-critical утверждение в развилке должно иметь доказательство, иначе задаётся вопрос о факте. Это можно оформить одним будущим срезом после согласования с двумя активными changes.

## Проверенная область

Прочитаны все 10 файлов внешнего change:

- `.openspec.yaml`;
- `proposal.md`;
- `design.md`;
- три `specs/**/spec.md`;
- `reports/architecture-new-2026-10-01.md`;
- три `reports/exploration-2026-10-01-*.md`.

В целевом репозитории проверены:

- proposal/design/spec/tasks активных `value-efficient-verify` и `verify-stop-repeat`;
- их последние verification/debug-артефакты;
- фактические контракты `.cursor/**` по new/verify/extend/apply/archive, decision cards, architect/reviewer;
- main specs `review-quality-disposition`, `always-apply-context-budget`;
- архивные precedents по review/disposition и last-slice review;
- ADR, включая Load-Bearing ADR-0003;
- наличие KB index и переносимой фикстуры.

Ветка целевого репозитория подтверждена как `develop`. До создания этого отчёта рабочее дерево было чистым.

## Requirement / report traceability

### Что доказано первичной фактурой

| Источник | Подтверждённый факт | Какие решения действительно следуют |
|---|---|---|
| `exploration-2026-10-01-customer-rework-diff.md` | Заказчик сократил основной фасад со 124 до 72 строк, убрал предикат карточки этапа, ветку родителя не-КП, серверный барьер и перенёс проверку до адресной книги | Нужен контроль появления непрошенных поведенческих веток; отклонение более простого пути должно ссылаться на обязательное требование |
| `exploration-2026-10-01-zni-trail-optimality.md` | Простой вариант был отвергнут по ложному утверждению о данных; readiness-сигнал об избыточной проверке потерян; reviewer-trace об избыточности появился, но `/review` не запускался | Нужна доказательность decision-critical утверждений; readiness-замечание должно стать открытой темой постановки |
| `exploration-2026-10-01-kit-optimality-criterion.md` | Критерий простоты объявлен, `architect-simplicity-missing` не реализован; reviewer-вопрос «проще на другом уровне?» не имеет собственного типа результата | Нужна исполнимая проверка ссылок на требования и определённый исход замечания об избыточности |
| `architecture-new-2026-10-01.md` | Первоначальная постановка была шире фактов; отчёт сузил ядро до provenance, запрета непрошенного требования, evidence в развилке и адресата сигнала | Полезен как challenge, но не является независимой первичной фактурой для D6/D7 и не заменяет сверку с текущим kit |

### Трассировка требований внешнего пакета

| Требование / решение | Опора в фактуре | Оценка |
|---|---|---|
| D1: происхождение каждого нормативного пункта поведения | Прямо следует из четырёх удалённых заказчиком веток и ложного расширения Behavior Contract | **Доказано как потребность**, но не доказано, что inline-метки с дословной цитатой — лучший механизм |
| D2: `[исполнитель]` не остаётся требованием и не получает код | Инцидент подтверждает вред нескольких непрошенных защит | **Частично доказано**: универсальный запрет блокируется открытым вопросом о правах, целостности и транзакциях |
| D2/D3: простой вариант отклоняется только по обязательному требованию | Прямо следует из ложной формулы «проще, но хуже по поведению» | **Доказано** |
| D4: факт в развилке проверен либо вопрос задаётся о факте | Прямо следует из развилки 29.09 на ложной посылке | **Доказано**; это наиболее сильный отдельный контракт пакета |
| D3: `architect-simplicity-missing` через метки | Предупреждение действительно не реализовано | **Механизм не доказан**: на инциденте Simplicity Check был содержательным; недостающая метка уже планируется как блокер, второе предупреждение дублирует исход |
| D5: readiness-сигнал идёт в Open Questions | Readiness-замечание было потеряно | **Доказано** |
| D5: reviewer-trace получает disposition в acceptance handoff; «принято» = as-designed | Reviewer-trace был виден в handoff, но `/review` не запускался | **Не следует из факта и конфликтует с precedent**: факт доказывает отсутствие явного disposition, а не право заменить его общей приёмкой |
| D6: рост сложности восстанавливается от первого verify | Был ложный «нетто ноль» при большом итоговом фасаде | **Симптом доказан, алгоритм нет**: current-minus-additions не восстанавливает состояние при удалениях, заменах и неполных Extend-записях |
| D7: `[исполнитель]` не становится invariant KB / Load-Bearing ADR | В инциденте такого архивного превращения не было | **Гипотетическая профилактика**, не часть минимального исправления |

### Proposal ↔ symptom

`proposal.md#Why` в целом соответствует симптому: результат принят функционально, но оказался сложнее пользовательского запроса, а процесс этого не остановил. Подмена начинается в `## What Changes`:

- пункты 1–4 закрывают причинную цепочку;
- пункт 5 повторяет контроль пункта 1 другим уровнем severity;
- пункт 6 смешивает readiness и post-code review, хотя у них разные владельцы и precedents;
- пункт 7 добавляет две профилактики, которых исходный инцидент не проверял.

Таким образом, proposal уже зафиксировал конкретную трёхметочную схему, новый канал handoff и историческую метрику до сравнения с текущими механизмами target kit. Для текущего репозитория это solution-first постановка.

## Coherence gaps

### 1. Внутренние противоречия design

1. **D2 уже принято как правило, но его граница остаётся Open Question.** Design запрещает любой код под `[исполнитель]`, одновременно спрашивая владельца, какие защиты нельзя снимать без вопроса. Пока не определены права доступа, целостность данных и транзакции, универсальная норма не готова.
2. **`[типовое: path:line]` смешивает факт и обязанность.** Существование поведения в базе не доказывает, что новый change обязан его сохранять. Design проговаривает это словами, но механический verify проверяет только существование пути, а не обязательность сохранения.
3. **Дословная цитата дублирует текущий `External Contract Ledger`.** В target kit источник, authority, axis и решение уже имеют устойчивый `EC-*`. Inline-копия цитаты создаёт второй SSOT и ложные отказы на допустимом пересказе.
4. **D3 даёт WARNING на условии, которое D1/D2 уже превращают в отказ.** Пункт без метки одновременно блокирует проверку и поднимает `architect-simplicity-missing`; это дублирование, а не дополнительное покрытие.
5. **D5 объединяет разные события.** Readiness работает до реализации и должен править постановку. Reviewer finding возникает после кода и регулируется отдельным disposition-контрактом. Один «обязательный адресат» не делает их одной capability.
6. **D6 не имеет воспроизводимого source of truth для базы.** Дата первого verification-файла не содержит исторический текст design/tasks. Текущие хэши показывают изменение, но не позволяют вычислить количество старых задач/решений.
7. **D7 частично недостижим по собственному D2.** Если `[исполнитель]` не может остаться в нормативном контракте и не получает код, его последующее превращение в устойчивый пользовательский инвариант уже должно быть исключено раньше.
8. **Общий образец создаёт скрытую связь срезов.** Design заявляет независимость, но S1, S3 и S4 меняют одну песочницу; без обязательного reset результат последующего среза зависит от предыдущего.

### 2. Delta specs

#### Искусственное дробление capabilities

| Capability | Фактическое содержание | Оценка |
|---|---|---|
| `kit-contract-provenance` | provenance нормативных требований, запрет непрошенного поведения, основание отклонения альтернатив, исключение quick-fix | Когерентное ядро, но в target это должно расширять внешний контракт, а не быть полностью новой независимой capability |
| `kit-decision-card-evidence` | доказательность утверждений в карточке выбора | Самостоятельно наблюдаемо, но причинно и процессно это тот же provenance/evidence-контур и расширение активного пакетирования решений |
| `kit-optimality-signal-routing` | warning простоты + readiness routing + review disposition + cumulative complexity + archive invariant | **Некогерентный контейнер** из четырёх разных жизненных циклов |

Минимальная будущая постановка не требует трёх ADDED capabilities. Нужны точечные MODIFIED-контракты к активным `value-efficient-verify` / `verify-stop-repeat`; `review-quality-disposition` не менять без отдельного решения и Blast Radius.

#### Проблемы Scenario

1. Scenario «Защита от несуществующего пути выдана за существующее поведение» требует доказать всех вызывающих и семантику обхода. Это не механический Layer 2 check по метке/пути; нужен semantic/code evidence.
2. «Цитата дословно не встречается» делает форму текста частью контракта. Текущий kit уже использует stable source и authority; точная подстрока не равна смысловой трассируемости.
3. «Требование переведено в допущение, но код остался» смешивает pre-apply design и post-apply код. Нужно явно определить, проверяется ли решение/tasks или фактическая реализация.
4. В `kit-decision-card-evidence` два уровня не разведены: несущественное непроверенное утверждение можно показать с пометкой, но утверждение, от которого зависит сравнение вариантов, должно превратиться в вопрос. Термин `decision-critical` отсутствует.
5. В `kit-optimality-signal-routing` отсутствие provenance одновременно описано как блокирующее нарушение и как warning простоты.
6. Requirement роста говорит о любом накопленном росте, Scenario — о росте более чем вдвое, а design — о предупреждении, только если весь рост состоит из `[исполнитель]`. Единого trigger нет.
7. Scenario «Требование заказчика становится инвариантом» сформулирован слишком широко. Прямое требование заказчика может быть transient и всё равно обязано пройти Reuse Value Test и invariant-extraction.

### 3. Срезы и исполнимость

`tasks.md` отсутствует. Формально это не slice-mode implementation plan, а черновая декомпозиция в design.

#### Slice Summary

| Срез | Scenario | Tasks | Acceptance | Dependencies | Gate |
|---|---:|---|---|---|---|
| S1 Provenance и verify | 13 | отсутствуют | только draft Primary в design | заявлено: нет; скрыто: внешний incident fixture | отсутствует |
| S2 Evidence в decision card | 5 | отсутствуют | только draft Primary в design | заявлено: нет; скрыто: внешний report 29.09 | отсутствует |
| S3 Маршрутизация сигнала | 3 | отсутствуют | только draft Primary в design | заявлено: нет; скрыто: ADR/main spec review | отсутствует |
| S4 Рост + archive invariant | 4 | отсутствуют | Primary покрывает только рост; archive optional | S1 + внешний incident fixture | отсутствует |

#### Scenario Coverage

| Группа сценариев | Покрытие в design | Покрытие задачами / accept |
|---|---|---|
| Provenance и альтернативы — 11 | заявлено S1 | отсутствует |
| Simplicity warning — 2 | заявлено S1 | отсутствует |
| Decision evidence — 5 | заявлено S2 | отсутствует |
| Signal routing — 3 | заявлено S3 | отсутствует |
| Complexity / archive — 4 | заявлено S4 | отсутствует |

На уровне design заявлено 25/25. На уровне исполнимого OpenSpec-плана — 0/25, потому что нет задач и acceptance checklist.

#### Dependency Graph

```text
S1 ───────► S4
│           │
│           └──► внешний do2 fixture + первый verification snapshot
├──► общий mutable sandbox (скрытая связь с S3)
S2 ────────────► внешний verification-2026-09-29.md
S3 ────────────► review-quality-disposition / ADR-0003

Все S1–S4 ─────► отсутствующие в target артефакты C:\GitHub\PavDO
```

Цикла между заявленными срезами нет. Есть незаявленные внешние зависимости и общий изменяемый fixture.

### Alerts

#### 1. `no-slices`

- Область: весь change.
- Severity: **CRITICAL**.
- Evidence: среди 10 файлов нет `tasks.md`; отсутствуют `# Срез S<N>`, задачи, `S<N>.accept` и `<!-- slice-gate -->`.
- Рекомендация: не генерировать tasks до закрытия блокирующих решений и перепривязки к текущим contracts.

### Remediation (decision-required)
- alert: no-slices
- target: `kit-contract-provenance-gate/tasks.md`
- action: после выбора SSOT provenance и политики review создать один минимальный срез с реальными задачами, одним `S1.accept` и marker; не переносить черновые четыре среза автоматически

#### 2. `slice-accept-not-self-achievable`

- Область: S1–S4.
- Severity: **CRITICAL**.
- Evidence: target repo не содержит `do2-template-forbid-add-approvers`, его report 29.09, исходные `src/ДО2/**` и `sample-kit-provenance-do2`; все Primary acceptance ссылаются на них.
- Рекомендация: переносимая synthetic fixture или Primary, работающий на артефактах самого change.

### Remediation (decision-required)
- alert: slice-accept-not-self-achievable
- target: `design.md` Slices S1–S4
- action: по умолчанию заменить incident-copy на компактную нейтральную fixture, включённую в scope будущей ЗНИ; альтернативно переписать Primary на статически наблюдаемый результат без зависимости от `C:\GitHub\PavDO`

#### 3. `slice-scenario-overload`

- Область: S1 (13), S2 (5), S4 (4).
- Severity: **WARNING**.
- Evidence: канон допускает 1–3 связанных пользовательских сценария на срез; validator branches превращены в самостоятельные spec Scenario.
- Рекомендация: оставить один black-box Primary и 1–2 варианта; проверки строк, путей и режима quick-fix сделать agent/static задачами.

### Remediation (auto-repair)
- alert: slice-scenario-overload
- target: `specs/**/spec.md` + `design.md` Slices
- action: объединить технические ветви одного validator outcome в scenario matrix внутри задачи; сохранить отдельными Scenario только различимые пользовательские исходы

#### 4. `slice-hidden-fixture-coupling`

- Область: S1, S3, S4.
- Severity: **WARNING**.
- Evidence: общий sandbox объявлен не создающим зависимости, но срезы читают и меняют одно состояние; reset contract отсутствует.
- Рекомендация: immutable fixture per scenario либо явный reset в каждой agent-задаче.

### Remediation (auto-repair)
- alert: slice-hidden-fixture-coupling
- target: `design.md` § Slices / fixture contract
- action: определить immutable input и отдельную рабочую копию на каждый acceptance run; запретить использовать состояние предыдущего среза

#### 5. `slice-mixed-outcomes`

- Область: S4.
- Severity: **WARNING**.
- Evidence: Primary проверяет drift growth, а archive invariant является другим lifecycle outcome и только optional; общей пользовательской приёмки у них нет.
- Рекомендация: удалить оба из минимальной ЗНИ; если позднее докажется необходимость — оформить отдельными изменениями.

### Remediation (decision-required)
- alert: slice-mixed-outcomes
- target: `design.md` S4 + `kit-optimality-signal-routing/spec.md`
- action: по умолчанию исключить D6/D7; включение любого пункта требует отдельного Why, собственного acceptance и решения владельца

#### 6. `requirement-severity-contradiction`

- Область: provenance / simplicity.
- Severity: **WARNING**.
- Evidence: пункт без метки даёт hard failure D1/D2 и одновременно warning D3.
- Рекомендация: один owner и один исход; warning оставить только для качественной недостаточности alternatives, не для отсутствующей provenance.

### Remediation (auto-repair)
- alert: requirement-severity-contradiction
- target: `design.md` D3 + `kit-optimality-signal-routing/spec.md`
- action: удалить provenance из условия `architect-simplicity-missing`; проверять warning только на отсутствие жизнеспособных alternatives или source-backed основания отклонения

#### 7. `task-readability-not-assessable`

- Область: весь change.
- Severity: **WARNING**.
- Evidence: `tasks.md` отсутствует.
- Рекомендация: task readability проверять только после минимизации scope и генерации задач.

### Remediation (decision-required)
- alert: task-readability-not-assessable
- target: будущий `tasks.md`
- action: каждая non-accept задача должна содержать глагол, конкретный файл/секцию, изменение и бизнес-результат; не создавать задачи вида «реализовать D1»

## Overlap / precedent map

### Активные changes

| Текущий change | Отношение | Пересечение | Конфликт / условие совместимости |
|---|---|---|---|
| `value-efficient-verify` | **overlaps**; может стать `extends` после перепроектирования | `External Contract Ledger`, authority/source, external validity, re-open по новому сигналу, delta/cache, передача `EC-*` в review | Inline `[заказчик: цитата]` создаёт второй SSOT. Совместимо только как ссылка на `EC-*`/source anchor, а не копия authority в design |
| `verify-stop-repeat` | **overlaps**; evidence-rule может `extend` | пакет продуктовых развилок, запрет авторского ответа агента, все темы одной карточкой, точечный прогон после ответа | Новая отдельная handoff-корзина и implicit «принято = as-designed» обходят пакет явных решений и журнал |

Ни один из двух активных changes не independent. Перенос нового change без dependency/merge создаст конкурирующие правила в тех же файлах:

- `openspec-new-change/SKILL.md`;
- `openspec-verify-change/SKILL.md`;
- `openspec-extend-change/SKILL.md`;
- `openspec-apply-change/SKILL.md`;
- `decision-block.md`;
- `onec-code-architect.md`;
- reviewer contracts.

Оба активных change реализованы, но не полностью приняты:

- `value-efficient-verify`: S1 принят, S2 ждёт acceptance;
- `verify-stop-repeat`: рабочие задачи выполнены, acceptance нескольких срезов открыт.

Следовательно, новый пакет нельзя считать основанным на стабильном main contract до завершения этих changes либо явного решения о консолидации.

### Архивные contracts и ADR

| Precedent | Отношение | Вывод |
|---|---|---|
| Main spec `review-quality-disposition` | **conflicts** с D5 | apply weak не считается as-designed; явный disposition выполняется в `/review`/`/release-review` |
| Load-Bearing ADR-0003 | **conflicts** с D5 | «принято» не является явным disposition; финальный выбор принадлежит review skill |
| Archive `2026-08-18-independent-review-disposition` | **conflicts** с D5 | AskQuestion disposition внутри apply был сознательно исключён; open trace оставляется для review |
| Archive `2026-08-18-kit-evolution-models-economy-profiles` + main `always-apply-context-budget` | **conflicts** с implicit closure | always-apply якорь запрещает auto-waive weak и сохраняет след |
| Archive `2026-08-30-last-slice-review-or-archive` | **overlaps** | после последнего среза уже существует явный путь в `/release-review`; внешняя ЗНИ не анализирует этот механизм |
| Archive contracts по exact capabilities | **independent / отсутствуют** | одноимённых `kit-contract-*` capability нет, но semantic precedent выше обязателен |
| Invariant KB | отсутствует | `_index.yaml` отсутствует; KB Discovery пуст, конфликтов KB не найдено |

Другие Load-Bearing ADR целевой области не затрагивают. Новый ADR с `Supersedes` пакет не предлагает.

### Precedent alert

#### `precedent-regression`

- Область: D5, S3, `kit-optimality-signal-routing`.
- Severity: **CRITICAL**.
- Evidence: D5 считает общий ответ «принято» выбором «оставить как задумано», тогда как main spec и ADR-0003 требуют явного disposition и сохраняют weak open после apply.
- Рекомендация: в минимальном варианте удалить implicit closure и не менять owner disposition.

### Remediation (decision-required)
- alert: precedent-regression
- target: `design.md` D5 / S3 и delta spec
- action: по умолчанию оставить reviewer-trace открытым до `/review` или `/release-review`; если владелец хочет закрывать его на acceptance, оформить `MODIFIED review-quality-disposition`, заполнить `## Blast Radius`, определить явную запись who/when и отдельно согласовать изменение ADR-0003

## Blast Radius и решения пользователя

### Обязательно до любой будущей ЗНИ

1. **Единственный источник provenance.** Рекомендация: `External Contract Ledger` и stable `EC-*`; в design — ссылки, не дубли цитат/authority.
2. **Политика `[исполнитель]` для защит.** Нужно решить, какие классы нельзя молча исключить: права, целостность, транзакции, безопасность, восстановление после ошибок. Без этого D2 небезопасен.
3. **Disposition reviewer-trace.** Рекомендация: не менять ADR-0003; generic acceptance не закрывает quality finding.
4. **Переносимая приёмка.** Рекомендация: нейтральная fixture внутри будущего scope, без абсолютных путей и зависимостей от PavDO.
5. **Sequencing с активными changes.** Рекомендация: сначала принять/архивировать `value-efficient-verify` и `verify-stop-repeat`, затем писать delta к их итоговым capabilities.

### Требует `## Blast Radius`

Blast Radius обязателен, если выбирается любой из вариантов:

- «принято» закрывает weak/design-prescribed как as-designed;
- disposition переносится из `/review`/`/release-review` в acceptance handoff;
- apply перестаёт оставлять open trace для последующего review;
- новый provenance-формат отменяет authority/source semantics `External Contract Ledger`, а не расширяет их.

Минимальные поля Blast Radius:

| Контракт | Источник | Бизнес-эффект | Альтернатива без отмены | Обоснование |
|---|---|---|---|---|
| Explicit disposition before quality finding is closed | ADR-0003 + `review-quality-disposition` | Пользователь может принять функциональность, не подтвердив спорное качество | Показывать trace и направлять в review | Почему generic acceptance достаточно как quality decision |
| Apply weak remains open, no auto-waive | main spec + always-apply anchor | Не теряется независимое замечание | Не закрывать finding на handoff | Почему новый owner безопаснее review |
| Authority/source lives in EC ledger | active `value-efficient-verify` | Один проверяемый источник требований | Design ссылается на `EC-*` | Почему нужен второй inline SSOT |

## Минимальный вариант

### Минимальный Why

В текущем kit уже есть внешний контракт и пакет продуктовых развилок, но design не обязан связать каждый добавленный нормативный пользовательский исход с конкретным `EC-*`/проверенным baseline, а decision card не обязана отделять проверенный факт от предположения, которое определяет выбор. Поэтому непрошенная защита или ложное утверждение могут стать основанием более сложного решения.

### Минимальные требования

1. **Source-backed normative behavior.** Каждый новый нормативный пункт Behavior Contract / behavior-changing Decision ссылается на:
   - `EC-*` с `customer-direct` или `accepted-reference`; либо
   - verified baseline anchor, который design явно решил сохранять.
2. **Proposal is not authority.** Пункт без такого основания помечается как предложение исполнителя и не становится нормативным требованием до существующего пакетного решения пользователя. Для safety-классов применяется согласованная отдельная политика.
3. **Source-backed alternative rejection.** Отклонение более простого варианта называет конкретный requirement/contract ID и объясняет нарушаемый наблюдаемый исход.
4. **Decision-critical evidence.** Утверждение о системе, от которого зависит преимущество варианта, имеет verified evidence. Если evidence нет, карточка задаёт вопрос о факте и не предлагает выбор на этой посылке.
5. **Readiness routing only.** Замечание task-readiness об избыточности становится открытой темой design и попадает в уже существующий пакет verify. Post-code reviewer disposition остаётся без изменений.

### Capabilities

Рекомендованная модель после завершения активных changes:

- `MODIFIED value-efficient-verify`: requirement-level ссылки на `EC-*`/baseline;
- `MODIFIED verify-stop-repeat`: evidence contract для decision-critical утверждений и попадание readiness-темы в общий пакет;
- `review-quality-disposition`: **без изменений**.

Новая capability нужна только если после архивирования этих changes main specs не дают корректной точки расширения. Даже тогда достаточно одной capability, а не трёх.

### Один вертикальный срез

По канону 6–15 задач здесь достаточно одного среза:

**Сценарий:** разработчик создаёт/проверяет ЗНИ; непрошенный новый исход не становится требованием, а выбор не строится на непроверенном факте.

**Primary acceptance:** на нейтральной fixture с одним `EC-*`, одним предложенным guard и одной decision-critical неподтверждённой посылкой запустить verify → guard не проходит как нормативный пункт, а карточка вариантов заменяется вопросом о факте; после явного ответа пользователя и записи в ledger повторный verify проходит эти два контроля.

Остальные проверки — agent/static tasks:

- baseline anchor существует;
- rejection ссылается на contract ID;
- quick-fix без design не затронут;
- readiness finding присутствует среди открытых тем;
- review/apply contracts не изменены.

### Почему этот минимум закрывает симптом

- Четыре непрошенных ветки инцидента не получают authority.
- Ложная посылка развилки не приводит к выбору сложного варианта.
- Более простой вариант нельзя отклонить словами «хуже по поведению» без требования.
- Потерянный pre-implementation сигнал readiness доходит до существующей карточки.
- Не добавляются новая историческая метрика, новый archive policy и второй disposition UX.

## Что отбросить

1. Перенос внешней ЗНИ один-в-один.
2. Inline-дословную цитату как второй источник authority; использовать `EC-*`/source anchor.
3. Автоматическое признание `[типовое: path]` обязательным к сохранению без design-решения.
4. Универсальный запрет любых `[исполнитель]` до определения safety policy.
5. Дублирующий warning provenance в D3.
6. S3 в текущем виде: handoff disposition и implicit «принято = as-designed».
7. D6 и связанные Scenario/Primary накопительного роста.
8. D7 archive invariant из первой поставки.
9. Capability `kit-optimality-signal-routing` как сборный контейнер.
10. Копию реальной customer change как переносимую fixture.
11. Утверждение «четыре самостоятельных результата»: D6/D7 не доказаны самостоятельной ценностью, а D1–D4 образуют один end-to-end процесс.
12. 25 Scenario: оставить различимые пользовательские исходы, технические ветви перенести в static verification tasks.

## Блокирующие решения

1. **Источник требований:** `EC-*`/ledger или inline-теги с цитатой? Рекомендация — ledger.
2. **Safety policy:** какие предложенные исполнителем защиты всегда требуют вопроса, а какие могут быть Non-Goal по умолчанию?
3. **Review disposition:** сохранять явный `/review`/`/release-review` или сознательно менять ADR-0003? Рекомендация — сохранять.
4. **Fixture:** включить нейтральный переносимый образец или отказаться от runtime acceptance? Рекомендация — включить минимальный образец.
5. **Sequencing:** дождаться закрытия двух активных changes или расширять их сейчас? Рекомендация — сначала завершить acceptance, чтобы не проектировать против подвижного контракта.
6. **Второй ряд:** нужен ли отдельный последующий change на complexity history/archive extraction? Рекомендация — нет, пока нет второго подтверждённого инцидента.

## Рекомендации для будущей ЗНИ

1. Не переносить каталог `kit-contract-provenance-gate`.
2. После acceptance активных changes создать новую минимальную постановку по Why выше.
3. В proposal объявить не три ADDED capability, а изменения существующих process contracts.
4. В design сначала зафиксировать source model: `EC-*`, baseline anchor, proposal; затем проектировать checks.
5. Развести deterministic checks и semantic checks:
   - existence/schema/source link — deterministic;
   - следует ли требование из источника и действительно ли baseline надо сохранять — semantic design challenge.
6. Не обещать механически доказать «пути обхода нет» одним grep пути.
7. Сохранить owner review disposition и last-slice путь в `/release-review`.
8. Сделать один срез с одной portable fixture и одним mandatory Primary.
9. Сгенерировать `tasks.md` только после решений 1–5 из блока выше.
10. На pre-apply verify отдельно проверить:
    - нет второго SSOT authority;
    - нет изменения ADR-0003 без Blast Radius;
    - Scenario coverage обеспечено задачами/accept;
    - fixture находится в target repo;
    - все ссылки на capabilities соответствуют состоянию после архивирования активных changes.

## Итог

Внешний пакет полезен как исследовательский материал, но не как переносимая ЗНИ. Доказан один компактный процессный дефект: authority нового поведения и evidence выбора не связаны до конца. Текущий пакет добавляет поверх него недоказанные метрики, архивную профилактику и конфликтующий disposition. Правильный следующий артефакт — новая минимальная ЗНИ после стабилизации `value-efficient-verify` и `verify-stop-repeat`, с одним срезом и без изменения review precedent.
