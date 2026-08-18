## Context

Эволюция Cursor-kit (метапроект): UX гейтов `/opsx:new` при создании прикладной ЗНИ. Источник: `temp/reports/exploration-2026-07-31-sequential-ui-mode-questions.md`, бриф подтверждён; сужение 2026-08-01 — формы only, per-form Mode Gate. Ветка `kit-evolution-sequential-ui-mode-questions`; в `main` — только `.cursor/**`, папка change не мержится.

Сейчас: Metadata Gate и Forms/MXL Mode Gate формально «отдельные», но нет жёсткого END TURN; один `artifact_mode` и склейка «форму/макет» не покрывают разные режимы **разных форм**. Apply уже различает Form vs Template.

## Goals / Non-Goals

**Goals:**

- Один вопрос выбора за ход чата; следующий гейт — только после ответа.
- Режим поставки управляемой формы (`form_mode`) на этапе design: **одна форма в scope → один вопрос**; несколько форм → последовательные вопросы с END TURN; разные формы могут иметь разные режимы.
- Mode Gate формы — не в одном сообщении с Metadata и не с Design Gate selection.
- Legacy `artifact_mode` читается как fallback для `form_mode`.

**Non-Goals:**

- Изменение прикладного BSL / Form.xml / Template.xml в consumer-проектах.
- Mode Gate / выбор режима поставки для Template/MXL в `/opsx:new` (макеты вне этой ЗНИ как предмет выбора).
- Введение новых значений режимов формы сверх `manual` | `assisted` | `bsl-only` | `n/a`.
- Отдельный AskQuestion «MXL или СКД».
- Обязательный `[form:…]` в tasks (Follow-up).
- Поле `layout_mode` как предмет выбора в новых proposal (не пишем; политика макета — apply-инвариант).

## Decisions

1. **Имя поля режима формы:** `form_mode` (`manual` | `assisted` | `bsl-only` | `n/a`). Отклонено: длинные `form_artifact_mode`. Поле `layout_mode` **не** вводим как Mode Gate / выбор в new (сужение 2026-08-01).
2. **Секция proposal:** целевое имя `## Forms mode`. Readers также принимают legacy-заголовок `## Forms & layouts mode` (только чтение). Внутри:
   - нет форм / kit → `form_mode: n/a`;
   - одна форма → допустим скаляр `form_mode: <mode>` **или** map из одного ключа;
   - несколько форм → **только** YAML-map `forms:` с каноническим ключом метаданных формы → mode.
   **Канон ключа:** полное имя объекта формы в терминах метаданных (`Документ.<Имя>.Форма.<ИмяФормы>` / `Document.<Name>.Form.<FormName>` — как принято в proposal проекта; один стиль на change). Не использовать путь выгрузки `src/.../Form.xml` как ключ SSOT.
   **Канонический пример (N форм):**
   ```yaml
   ## Forms mode
   forms:
     "Document.ЗаказКлиента.Form.ФормаДокумента": manual
     "Document.ЗаказКлиента.Form.ФормаСписка": bsl-only
   ```
   Единый `artifact_mode` в **новых** change не писать как SSOT. Пустой/`n/a` режим при задаче на конкретную форму без записи режима этой формы — блокер apply/verify.
3. **Последовательность new:** Metadata (STOP) → scaffold/артефакты → на этапе design: для **каждой** формы в scope по очереди вопрос Mode → END TURN → запись режима этой формы → … → все формы закрыты **до** AskQuestion приёмки design/срезов. Mode Gate **никогда** не в одном сообщении с Design Gate selection. Между ответом Metadata и первым Mode-вопросом допустимы сообщения **без** выбора (scaffold, правки текста). Frontload 1.56 = «собрать до apply», не «два AskQuestion в одном ходе».
3a. **Enumeration «формы в scope»:** список для цикла Mode строится на этапе design, когда scope форм стабилизирован (после scaffold / уточнения What Changes), из объединения: (1) формы, явно названные в proposal/design/handoff; (2) задачи/сценарии, затрагивающие управляемую Form.xml / модуль формы. Не включать Template/MXL. Пока список не стабилен — Mode-вопросы не начинать. Новая форма, появившаяся позже (extend) — отдельный вопрос только для неё (Decision 8).
4. **Инвариант ≥2 AskQuestion:** HALT в self-check new + явная строка в Mode Gate / Metadata «не смешивать в одном сообщении»; после любого выбора — END TURN.
5. **`[form:…]`:** не обязателен в этой ЗНИ; Follow-up.
6. **Формулировка вопроса (SSOT):** в `forms-mxl-mode-gate.mdc` — только текст про **форму** (вручную / автоматически через skill / программно → `manual` | `assisted` | `bsl-only`), с указанием **какой** формы касается вопрос. Склейку «форму/макет» убрать. Вопрос макета в new **не** задавать.
7. **Запись proposal / readers:** источник истины для форм — `form_mode` / map `forms:`. Fallback lone `artifact_mode` **только** если нет ни скаляра `form_mode`, ни map `forms:`: одно значение → одинаковый валидный `form_mode` **для всех** форм, уже входящих в scope на момент чтения (N≥1), без переспроса и без копирования режима «с соседней формы при пустой записи». При N>1 lone legacy **достаточен** как гомогенный режим; если позже добавляется форма без записи — Mode-вопрос только для новой (Decision 8), legacy на неё не молчит. Макет не получает Mode-вопрос из legacy.
8. **Extend / поздний Form-scope:** если scope впервые получил форму без режима — задать Mode-вопрос **этой** формы (по одной, END TURN); не наследовать режим соседней формы.
9. **Политика макетов (вне Mode Gate):** по умолчанию Template/MXL — только вручную (Конфигуратор + выгрузка). Non-manual путь (`1c-mxl/compile`, assisted и т.п.) — **только** после явного разрешения в ходе `/opsx:apply`. **Форма разрешения (норма):** (a) одноразовый AskQuestion или однозначный утвердительный ответ пользователя в чате apply **или** (b) маркер задачи `[mxl:assisted]` / явная запись non-manual в tasks до apply. Факт разрешения зафиксировать в `debug.md` § `## Apply permissions` (что разрешено, кем/когда). Это **не** Mode Gate в `/opsx:new` и не поле `layout_mode` в proposal. Отдельный AskQuestion «MXL или СКД» не вводить.

## Behavior Contract

- Пользователь видит не больше одного нумерованного/карточкой выбора за сообщение оркестратора, пока не ответил.
- Mode Gate в new спрашивает только про управляемую форму; при N формах в scope — N последовательных вопросов (каждый про конкретную форму), с END TURN между ними; первый Mode — на этапе design после стабилизации списка форм (Decision 3a), не в том же сообщении, что Metadata.
- Разные формы одной ЗНИ могут иметь разные `form_mode` (map `forms:`); apply следует режиму **этой** формы по каноническому ключу.
- Вопросы режимов форм закрыты записью в proposal до выбора приёмки design/срезов; не смешивать с Design Gate AskQuestion.
- Resume: валидные режимы уже записанных форм не переспрашивать; для новой формы в scope без режима — вопрос.
- Пустой/`n/a` при задаче на форму без валидного режима этой формы (и без lone legacy `artifact_mode`) — блокер apply/verify / Mode-вопрос; не молчаливый default и не копирование режима другой формы.
- Lone legacy `artifact_mode` без `form_mode`/`forms:` → один режим на весь текущий form-scope (Decision 7).
- Макет: Mode-вопрос в new не задаётся; default — manual; non-manual на apply — только по норме разрешения Decision 9 (`debug.md` § Apply permissions или маркер `[mxl:…]`).

## Implementation Options

| Option | Суть | Выбор |
|--------|------|--------|
| A | Один `artifact_mode` + текст в design | Отклонено — нет per-form |
| B | `form_mode` + `layout_mode` + dual Mode Gate | Отклонено сужением 2026-08-01 (макеты вне Mode Gate) |
| D | Per-form `form_mode` на design + sequential questions; макеты — apply-политика | **Выбрано** |
| C | Всегда вопросы даже без UI | Отклонено — шум |

## Design Rationale

Точки правки — протоколы оркестратора и Mode Gate (SSOT `forms-mxl-mode-gate.mdc`). Apply уже ветвит Form vs Template; выравниваем UX вопросов на **формы** и убираем шум Mode Gate макета. Сужение: `reports/architecture-extend-coherence-2026-08-01-2.md`.

## Slices

| ID | Имя | Сценарии | Файлы (ориентир) | Primary acceptance | Зависимости |
|----|-----|----------|------------------|--------------------|-------------|
| S1 | Один вопрос за ход | Metadata alone; no dual AskQuestion | `openspec-new-change/SKILL.md`, `brief-card.md` | В учебном `/opsx:new` после ответа на маркер следующий вопрос (режим формы) приходит отдельным сообщением, не вместе с маркером | нет |
| S2 | Режимы форм (per-form) | form Mode on design; multi-form sequential; legacy→form_mode; empty form mode blocks; kit n/a; layout no Mode question; layout permission recorded | `forms-mxl-mode-gate.mdc`, new design-stage, apply, verify, 1c-forms, handoff | В proposal с двумя формами можно задать разные `form_mode`; вопросы на design по одной форме; макет без Mode-вопроса | S1 |

### Матрица приёмки

| Scenario | S1 | S2 |
|----------|----|----|
| Один вопрос Metadata без Mode Gate в том же сообщении | Primary | — |
| Вопрос формы на design при scope Form | — | Primary |
| Несколько форм — последовательные вопросы | — | multi-form |
| Legacy `artifact_mode` → form_mode | — | legacy |
| Пустой/`n/a` режим при задаче на форму | — | empty form mode |
| Kit / без форм — `form_mode: n/a`, вопрос не задаётся | — | kit |
| Макет без Mode-вопроса в new | — | layout policy |
| Non-manual макет только с записанным разрешением apply | — | layout permission |

## Risks / Trade-offs

- [Риск] Оркестратор снова сбатчит два AskQuestion → Mitigation: END TURN + self-check HALT.
- [Риск] N форм → N ходов на design → Trade-off: осознанно ради разных режимов.
- [Риск] Старые change с одним `artifact_mode` → Mitigation: fallback → `form_mode`.
- [Риск] Apply всё же спросит Mode Gate макета по старым правилам → Mitigation: явная политика Decision 9 в gate/apply.
- **Architect / verify:** `reports/architecture-new-selfreview-2026-07-31.md`; extend: `reports/architecture-extend-coherence-2026-08-01-2.md`.

## Assumptions

- `project.md` в этом репозитории kit может отсутствовать; Metadata для эволюции kit допустим с `marker_style: minimal`.
- Skill `1c-forms/compile|edit` обязателен для Form+`assisted`.

## Решения verify (зафиксировано)

- После verify 2026-08-01: не замораживать dual-channel постановку — сузить ЗНИ до форм; макеты вне Mode Gate (default manual, programmatic только с явного разрешения на apply).
- Режим формы задаётся на design **по каждой форме** в scope (не один режим на всю ЗНИ).

## Open Questions

- (снято) Dual-channel `layout_mode` / Mode Gate макета — вне ЗНИ.
- (снято) Один режим на всю ЗНИ vs per-form → per-form.
- Follow-up: `[form:…]` в tasks — вне Primary.
