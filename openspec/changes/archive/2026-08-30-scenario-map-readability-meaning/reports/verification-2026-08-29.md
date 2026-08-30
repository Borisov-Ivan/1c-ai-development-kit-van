---
verify_mode: pre-apply
change: scenario-map-readability-meaning
date: 2026-08-29
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
  open_decision_id: short_map_layout_owner
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - "Кто судит спорную формулировку вывода в шапке (родитель vs приёмка) — не блокирует старт; при A нужно согласовать точку проверки с секциями self-check скилла"
    - "Полосы в запасной раскладке длинных карт: без подписей (default уже в задачах)"
  artifacts_mtime:
    proposal.md: "2026-08-29T10:46:28"
    design.md: "2026-08-29T11:51:50"
    tasks.md: "2026-08-29T11:54:22"
    specs/scenario-map-canvas/spec.md: "2026-08-29T11:47:02"
  last_challenge_at: "2026-08-29T11:51:50"
---

## Резюме для разработчика

scenario-map-readability-meaning — до старта нужен ваш выбор по логике раскладки короткой карты.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify scenario-map-readability-meaning`.

План правит шаблон панели `.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md`, скилл карты, роль сборщика манифеста и дельту `scenario-map-canvas`. Прикладная конфигурация 1С не меняется. Независимая проверка подтвердила дефекты текущего шаблона (нет маркера направления, подпись полосы врёт слоем, на открытии никто не выбран, клик сразу открывает файл). Ось «шаблон плюс две проверки на существующих шагах» держится. Не закрыто, кто считает координаты узлов на короткой карте: родитель (как в плане) или сама панель.

## Решения до apply

### Рекомендации

- **Раскладка короткой карты:** выбрать A или B ниже. От этого зависят обработчик рёбер, легенда, чек-лист пересечений и судьба существующего переключателя «Связи / Слои».
- После выбора в постановку допишутся хвосты, которые не меняют выбранную ось: правило обратного ребра или группировка полос; согласование судьи смысла с секциями self-check; правка хорошего эталона под лимит подписи; оговорка про полосы без подписей на длинных картах; зачистка старой фразы «клик открывает доказательство».

### Развилки

#### 1. Кто считает координаты узлов на короткой карте

**Цель ЗНИ:** карта по шаблону читается, полоса не врёт слоем, направление связей видно без клика. Обе ветки это закрывают разными средствами.

**Что в коде сейчас.** В `fixtures/canvas-shell.md` координаты считает `computeDAGLayout`: концы рёбер, признак `edge.isBackEdge` (петля на эталоне `cache-visual-copy → overlay`, отношение `reuses`), разведение пересечений. Рёбра — `<line>` без `marker-end`. Подпись полосы берётся как слой первого узла ранга. Переключатель `useCanvasState("view")` меняет направление автоматической раскладки.

**Что предлагает план.** Для карт до двенадцати узлов координаты полос и узлов считает родитель при заполнении шаблона. Пунктир и цвет кодируют тип связи. Режимы — подсветка того же графа.

**Почему это развилка.** Если родитель рисует координаты руками, панель больше не знает, какое ребро обратное, и не разводит пересечения сама. Пунктир уже занят типом связи. На хорошем эталоне именно обратное ребро несёт вывод «копии нет → сборка повторяется со старой картинкой». Независимая проверка предлагает оставить раскладку панели и честно подписывать полосу только когда ряд однороден по слою.

**Варианты решения.**

- **A. Координаты короткой карты считает родитель** — полосы точно по слоям; **компромисс:** в постановке нужно заранее сказать, чем помечается обратное ребро и как ловятся пересечения подписей.
- **B. Раскладку оставляет панель, полосы — группировка узлов ряда по слою** — петли и пересечения считает панель; **компромисс:** смешанный ряд остаётся без подписи полосы.

**Влияет на:** читатель схемы видит (или теряет) петлю механизма и честные имена полос с первого взгляда.

**Что изменится после выбора.** В `design.md` и задачах шаблона зафиксируется выбранный путь; остальные пробелы постановки (судья смысла, эталон «хорошо», каналы цвета, зачистка клика) допишутся тем же проходом.

**Источники** *(техническое):* `design-challenge-2026-08-29.md` Q2 alt.1, Gaps 1; `architecture-task-readiness-2026-08-29.md` G2; `layer_4: CHALLENGE`.

## Что меняется в постановке

**Расширение / конфигурация:** kit (не `src/` конфигурации 1С).

**Точки изменения:**

- `.cursor/skills/scenario-map-canvas/fixtures/canvas-shell.md` — полосы, направление рёбер, легенда, выбор узла, кнопка доказательства.
- `.cursor/skills/scenario-map-canvas/SKILL.md` — проверка смысла до записи, проверка читаемости после записи, контракт клика, поля манифеста.
- `.cursor/agents/onec-scenario-map-designer.md` и `.cursor/skills/1c-agent-patterns/scenario-map-designer.md` — несколько отчётов, расхождения как кандидаты.
- `fixtures/map-bad-no-insight.md` — новый плохой эталон; хороший эталон потребует правки после выбора раскладки.

**Что НЕ меняется:** словарь `kind` / `relation`, порог четырёх публикуемых сущностей, запрет выдуманных рёбер, регистрация файла родителем, успех штатной кнопкой среды. ADR-0008 не заменяется: в защищаемых инвариантах нет «клик = открыть файл».

**Связанные ADR / KB / архив:** ADR-0008; архив `2026-08-28-scenario-map-canvas` (отмена THEN «выбор узла сразу открывает доказательство» записана в `design.md` § Blast Radius). Таксономия KB в kit не заведена.

### К сведению

- Имя поля стартового узла в задачах — `header.focus_node`; в текущем скилле поля ещё нет, это новое поле, не ошибка адреса.
- Приёмка живой панели — на границе среза `S1.accept`, в проекте Документооборота; автотестов панелей в kit нет.

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS. Чекбоксы на месте; `<!-- slice-gate -->` есть; `form_mode: n/a`; `<!-- phase-gate -->` нет; User Task Contract DENY-grep: none.
- **Layer 2 (Internal Coherence):** PASS; QC: `reports/quality-control-2026-08-29-2.md` (verdict OK, alerts: none). Code-Truth pre-apply: WARNING `header.focus_node` отсутствует в текущем SKILL (новое поле). Precedent: INFO `precedent-documented` — ADDED→MODIFIED сценария клика закрыт секцией Blast Radius; ADR-0008 не Supersedes. KB Discovery пропущен (taxonomy отсутствует).
- **Layer 2.5 (Loop Detection):** PASS. `debug.md` срезовых решений не содержал; AcceptLoop/PatchRounds = 0.
- **Layer 3 (Problem-Solution Trace):** PASS. Why покрыт Requirements; каждый Requirement имеет Scenario; все 10 Scenario в `## Slices` и в S1.accept / S1.8 / S1.13–S1.14. `scenario-implementation-leak`: none. `process-only-marker-suffix`: none (`comment_suffix` пуст, `marker_style: minimal`).
- **Layer 4 (Independent Challenge):** CHALLENGE; отчёт: `reports/design-challenge-2026-08-29.md`. Post-challenge classifier: architectural fork «кто раскладывает короткую карту» (verified code: `computeDAGLayout`, `edge.isBackEdge`) → decision, не repair-only. Repair-класс (судья смысла, эталон «хорошо», гранулярность полос, каналы цвета, имя `focus_node`) отложен до ответа пользователя (смешанный отчёт: decision first).
- **Layer 5 (Implementation Readiness):** WARNING; отчёт: `reports/architecture-task-readiness-2026-08-29.md` (ГОТОВО С ЗАМЕЧАНИЯМИ). G2 (переключатель видов vs ручные координаты) связан с той же осью, что Layer 4. G1 (безусловная подпись полос vs запасная раскладка) и G3 (зачистка старого контракта клика) — repair после решения.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

- `short_map_layout_owner` — A parent coords / B host layout + band grouping. Источник: design-challenge Gaps 1, Architectural alternatives «Кто раскладывает короткую карту».

## Источники

- `openspec/changes/scenario-map-readability-meaning/reports/quality-control-2026-08-29-2.md`
- `openspec/changes/scenario-map-readability-meaning/reports/design-challenge-2026-08-29.md`
- `openspec/changes/scenario-map-readability-meaning/reports/architecture-task-readiness-2026-08-29.md`
- алерты: `precedent-documented` (INFO), `phantom-symbol` `header.focus_node` (WARNING pre-apply)
