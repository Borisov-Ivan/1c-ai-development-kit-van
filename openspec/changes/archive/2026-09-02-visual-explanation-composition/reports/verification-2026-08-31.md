---
verify_mode: pre-apply
change: visual-explanation-composition
date: 2026-08-31
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: WARNING
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: hint-slots-explain-overview
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - hint-slots-explain-overview
  artifacts_mtime:
    proposal.md: "2026-08-31T01:59:55Z"
    design.md: "2026-08-31T02:08:54Z"
    tasks.md: "2026-08-31T02:15:15Z"
    specs/visual-explanation/spec.md: "2026-08-31T02:08:53Z"
  last_challenge_at: "2026-08-31T02:08:54Z"
---

## Резюме для разработчика

visual-explanation-composition — до старта нужен ваш выбор по логике намёка на схему в разборе и обзоре.

**Что решить: править ли в этой поставке намёк на схему в пошаговом разборе и в обзоре проекта**

Боль постановки — после разбора механизма слоями агент молчит. План уже меняет навык панели и подсказку в исследовании. В пошаговом разборе и в обзоре проекта дословно остаётся старый узкий критерий: схему предлагать, только если путаются ветки, условия или уровни. Разбор слоями туда не попадает. Если эти два места не трогать, молчание останется там, где боль и была.

- **A. Включить в эту поставку** — тот же критерий (путаница частей, слоёв или случаев) попадёт и в разбор, и в обзор; зато объём шире исходного.
- **B. Оставить на потом** — эта поставка закроет свободный чат, исследование, шаблон панели и уточнение опорного решения; после пошагового разбора схема по-прежнему не предложится, пока не допишем отдельно.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify visual-explanation-composition`.

План правит навык `.cursor/skills/visual-explanation/SKILL.md`, шаблон `fixtures/panel-shell.md`, слот «Дальше» в `.cursor/skills/openspec-explore/SKILL.md` и два инварианта в `openspec/adrs/ADR-0010-visual-explanation-panel.md`. Прикладной код 1С не меняется. Независимый разбор подтвердил направление (таблица больше не «безопасное упрощение», граф не возвращается), но Why про молчание после разбора слоями не закрыт, пока копий старого критерия в разборе и обзоре нет в объёме ЗНИ.

## Решения до apply

### 1. Намёк на схему в пошаговом разборе и обзоре проекта

**В чём проблема.** Боль постановки — молчание после разбора механизма слоями. Задачи чинят навык панели и намёк в исследовании; в пошаговом разборе и обзоре остаётся старый перечень «ветки, условия или уровни».

**На что влияет.** После `/opsx:explain` и в `/opsx:overview` схема снова не предложится на разбор слоями — ровно там, где боль наблюдалась.

**Если выбрать A / B.** A — критерий путаницы частей, слоёв или случаев попадёт и туда, объём ЗНИ шире исходного Scope. B — эта поставка закрывает свободный чат, исследование, шаблон и ADR; молчание в разборе/обзоре останется до отдельной дописки.

**Что в коде сейчас.** В `.cursor/skills/openspec-explain/SKILL.md` (предложение панели и строка подтверждения списка), `templates/inventory-card.md` и `.cursor/skills/openspec-overview/SKILL.md` дословно: «без картинки легко перепутать ветки, условия или уровни»; в explain ещё «закрытый перечень авто в скилле визуального объяснения». После apply навыка эта фраза станет ссылкой на снятое правило. В `.cursor/skills/openspec-explore/SKILL.md` тот же перечень — его ЗНИ уже меняет (S1.3).

**Что предлагает план.** S1.1 и S1.3 выравнивают навык и исследование. Explain и overview в `## Scope` / `## Impact` / задачах нет.

**Почему это развилка.** Why требует, чтобы после разбора слоями панель предлагалась или открывалась. Scope явно перечисляет навык, шаблон, исследование, ADR — не разбор и не обзор. Добавить файлы — расширение объёма; оставить — Why не закрыт в команде, где боль возникла.

**Варианты решения.**

- **A. Включить в эту поставку** — те же формулировки, что в навыке, в explain (скилл + карточка списка) и overview; ограничения слотов (панель не публикуется вместе с картой точек / в блоке постановки ЗНИ) сохранить. Для разработчика: три markdown-файла в том же mechanical apply. Для человека: намёк появляется и после пошагового разбора.
- **B. Оставить на потом** — явно записать эти файлы в Out of scope + Follow-up. Для разработчика: объём как в исходном Scope. Для человека: в свободном чате и исследовании схема появится; после `/opsx:explain` — нет.

**Что изменится после выбора.** Фиксация в proposal (Scope/Impact), design (Existing Mechanisms / Behavior 2), tasks (задача или Follow-up). Остальные пробелы постановки (наблюдаемый триггер упрощения, область «одна сцена», `Grid`/`Callout` в допущениях) — repair после ответа, не отдельный вопрос в чат.

**Источники** *(техническое):* `layer_4_independent_challenge: CHALLENGE`; gaps 1–2 `reports/design-challenge-2026-08-31.md`; Пробел 1 `reports/architecture-task-readiness-2026-08-31.md`; alert `why-partial-hint-slots`.

## Что меняется в постановке

**Расширение / конфигурация:** kit (не `src/`). Продуктовый код 1С и XML не меняются.

**Точки изменения (уже в задачах):**

- `.cursor/skills/visual-explanation/SKILL.md` — критерий авто/намёка, рассказ (вопрос, вывод, скелет, одна сцена), носитель главной области.
- `.cursor/skills/visual-explanation/fixtures/panel-shell.md` — шаги истории, скелет с фокусом, пример не таблица.
- `.cursor/skills/openspec-explore/SKILL.md` — приоритет слота «Дальше».
- `openspec/adrs/ADR-0010-visual-explanation-panel.md` — два инварианта in-place, без нового ADR.

**Что НЕ меняется:** запрет графа с координатами; файл панели пишет родитель; отдельной команды схемы нет; авто на `/opsx:verify` и `/review` нет; прямой просьбы «покажи схему» без объекта-схемы 1С достаточно.

**Связанные ADR / архив:** ADR-0010 (Load-Bearing, уточняется); архив `2026-08-31-universal-visual-explanation` (extends, секция эффекта для человека в design заполнена).

### К сведению

- После ответа по развилке verify сам допишет: наблюдаемый триггер упрощения (дробление сцены, не сброс в таблицу из‑за счёта); область требования «одна сцена» только для скелета; в допущениях не опираться на `Grid`/`Callout` (в текущем шаблоне их нет); успех после разбора слоями там, где панель в том же сообщении запрещена — намёк в следующем шаге.
- Стартовый набор форм: скелет со сценами — вид главной области по умолчанию; ветки потока, иерархии и карточки остаются запасом; таблица — только сравнение свойств.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте; `<!-- slice-gate -->` есть; `<!-- phase-gate -->` нет; fences сбалансированы; ID с префиксом среза; `form_mode: n/a`; Form.xml / Template/MXL задач нет.
- **Layer 2 (Internal Coherence):** PASS. QC: `reports/quality-control-2026-08-31-2.md` Verdict OK; CRITICAL/WARNING нет; 19/19 Scenario покрыты; User Task Contract pre-check: none. Code-Truth: kit, `openspec/project.md` отсутствует; `computeDAGLayout` — запрет, не рецепт нового символа. Precedent Layer 2.4: capability `visual-explanation`, архив `2026-08-31-universal-visual-explanation`; пары ADDED→MODIFIED (авто-критерий, форма, упрощение нечитаемости) закрыты `## Blast Radius` → INFO `precedent-documented`. Invariant KB: `_index.yaml` нет. Load-Bearing ADR: in-place уточнение ADR-0010, не Supersedes, Blast Radius в design есть → нет `load-bearing-adr-bypass`.
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` на старте прогона отсутствовал; `S1.accept` = `[ ]`; AcceptLoop=0, PatchRounds=0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт delta-требованиями (с оговоркой Layer 4: покрытие Why в командах explain/overview — decision). Каждый Requirement ≥1 Scenario. 19 Scenario в design `## Slices` и в Primary / optional accept / S1.1–S1.5. implementation-leak в THEN: нет. `comment_suffix` пустой, `marker_style: minimal` → не `process-only-marker-suffix`.
- **Layer 4 (Independent Challenge):** CHALLENGE; отчёт: `reports/design-challenge-2026-08-31.md`; confidence: high. Classifier: gaps 3–6 → `implementation_invariant` (отложены до ответа); gap 1 + Why↔Scope → decision `hint-slots-explain-overview`; альтернатива «указатель вместо копии» не вынесена в чат (ось D1/D6 — копия формулировки; закрывается вместе с A или снимается Follow-up на B).
- **Layer 5 (Implementation Readiness):** WARNING; отчёт: `reports/architecture-task-readiness-2026-08-31.md`; вердикт ГОТОВО С ЗАМЕЧАНИЯМИ. Критерии 1–3, 5–8 OK; критерий 4 GAP = те же три файла explain/overview. User Task Contract OK. Precedent Coherence OK.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

См. «Решения до apply» §1. Agent-key: `open_decision_id: hint-slots-explain-overview`. Repair after answer (не в чат): design-challenge gaps 2–6; task-readiness замечание про `presentation.form`.

## Источники

- `openspec/changes/visual-explanation-composition/reports/quality-control-2026-08-31-2.md`
- `openspec/changes/visual-explanation-composition/reports/design-challenge-2026-08-31.md`
- `openspec/changes/visual-explanation-composition/reports/architecture-task-readiness-2026-08-31.md`
- `openspec/adrs/ADR-0010-visual-explanation-panel.md`
- `openspec/changes/archive/2026-08-31-universal-visual-explanation/`
- алерты: `precedent-documented` (INFO); `why-partial-hint-slots` (decision); Layer 5 coverage GAP (тот же decision)
