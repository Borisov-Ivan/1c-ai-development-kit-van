---
verify_mode: pre-apply
change: sequential-ui-mode-questions
date: 2026-08-01
verdict: NO-GO
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: acceptance-loop-detected
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: CHALLENGE
  layer_5_implementation_readiness: WARNING
snapshot:
  acceptance_loop_max: 3
  repair_attempt: 0
  accepted_tasks: []
  closed_decisions: []
  open_decision_id: acceptance-loop-s2
  decision_round: 0
  decision_round_max: 2
  verify_depth: full
  assumptions_accepted: []
  open_known_questions:
    - template-fill-only-successor-after-layout-no-bsl-only
    - s2-5-operational-readers-xml-guard-forms-compile-edit
  artifacts_mtime:
    proposal.md: "2026-07-31T22:50:02Z"
    design.md: "2026-07-31T22:51:49Z"
    tasks.md: "2026-07-31T22:51:54Z"
    specs/sequential-gate-questions/spec.md: "2026-07-31T14:17:32Z"
    specs/split-form-layout-modes/spec.md: "2026-07-31T22:50:22Z"
  last_challenge_at: "2026-07-31T22:51:49Z"
---

## Резюме для разработчика

sequential-ui-mode-questions — до старта нужен ваш выбор по логике среза раздельных режимов формы и макета.

**Что решить: постановку второго среза уже трижды уточняли до реализации — что делать дальше**

Срез про раздельные режимы формы и макета правили три раза подряд (два авто-дополнения и одно ваше уточнение про асимметрию каналов), а приёмку ещё не начинали. Независимый аудит снова нашёл край той же модели: куда девается сценарий «только код заполнения макета, XML не трогаем» после запрета программного режима для макета. Ещё один точечный патч рискует продолжить кружение.

- **A. Один раз дописать постановку** — матрица состояний режимов и явный наследник сценария заполнения без правки макета плюс полный список читателей полей; зато ещё один проход перед реализацией. Рекомендуется.
- **B. Заморозить как есть** — идти к правкам skills/rules; но путь «только код заполнения макета» останется недописанным до сюрприза на apply.

**Следующий шаг:** ответьте в чате (A или B). После фиксации в постановке — снова `/opsx:verify sequential-ui-mode-questions`.

План — эволюция Cursor-kit: один вопрос выбора за ход в `/opsx:new` и раздельные `form_mode` / `layout_mode` вместо склейки `artifact_mode`. Прикладной BSL и Form.xml/Template.xml не трогаются; правки только в `.cursor/**`.

## Решения до apply

### 1. Петля уточнений среза раздельных режимов (до apply)

**В чём проблема.** Срез S2 трижды правили через Extend при `S2.accept` ещё не подписанном; порог PatchRounds достигнут. Одновременно независимый аудит снова нашёл незакрытый край той же модели режимов (наследник Template-`bsl-only`).

**На что влияет.** Автор прикладной ЗНИ и apply могут по-разному понять, куда направлять «заполнение макета без правки Template.xml» после запрета `layout_mode: bsl-only`.

**Если выбрать A / B.** A — один consolidation-pass (матрица + наследник + readers), затем повторный verify. B — заморозка as-is с остаточным риском на apply.

**Что в коде сейчас.** Mode Gate и consumers всё ещё на едином `artifact_mode`; план Option B (`form_mode`/`layout_mode`, асимметрия layout) уже в proposal/design/specs/tasks после extend 2026-08-01.

**Что предлагает план.** Mechanical apply по `.cursor/skills` / `.cursor/rules` / docs; учебная приёмка протоколов `/opsx:new`.

**Почему это развилка.** Детектор петли (AcceptLoop=0, PatchRounds=3) + рекомендация редизайна vs новый gap независимого аудита на том же state space.

**Варианты решения.**

- **A. Consolidation** — Mode State Matrix в design + явный наследник fill-only Template + расширение S2.5 readers (`1c-xml-write-guard`, `1c-forms/compile|edit`); ledger Decisions 6/7/9. Рекомендуется (upgrade minimal→consolidation из-за свежего gap).
- **B. Minimal freeze** — не трогать S2 tasks точечно; принять остаточный риск Template fill-only до apply; закрыть петлю осознанно.

**Что изменится после выбора.** A → user-extend от отчёта редизайна + gaps challenge/task-readiness. B → запись решения в debug Loop Detection + assumptions; повторный verify без thin-repair.

**Источники** *(техническое):* `acceptance-loop-detected`; `reports/architecture-loop-redesign-2026-08-01.md`; `reports/design-challenge-2026-08-01.md` (implementation_invariant); `reports/architecture-task-readiness-2026-08-01.md` gaps 1–2.

## Что меняется в постановке

**Расширение / конфигурация:** метапроект kit — `.cursor/**` (не `src/` прикладной конфигурации).

**Точки изменения:**

- `.cursor/skills/openspec-new-change/SKILL.md` — END TURN / HALT одного вопроса; Mode Gate на этапе design.
- `.cursor/docs/templates/brief-card.md` — Metadata без соседних вопросов.
- `.cursor/rules/forms-mxl-mode-gate.mdc` — `form_mode` / `layout_mode`, асимметрия layout, legacy Decision 7.
- `.cursor/skills/openspec-apply-change/SKILL.md`, `openspec-verify-change/SKILL.md` — чтение пары + fallback.
- Skills `1c-forms` / `1c-mxl`, handoff explore, `kit-template-workflow.md` — термины режимов.

**Что НЕ меняется:** прикладной BSL, Form.xml, Template.xml consumer-проектов; обязательный `[form:…]` (Follow-up F2).

**Связанные ADR / KB / архив:** нет (capabilities ADDED; архивных MODIFIED/REMOVED нет).

### К сведению

- QC: optional bullets S2.accept с paraphrase имён Scenario («Form-only / Layout-only», «Kit evolution») — покрытие есть, выравнивание литералов опционально.
- Metadata: `marker_style: minimal`, пустой `comment_suffix` — допустимо; process-only suffix не сработал.
- Layer 5 SUBOPTIMAL (наследник Template-bsl-only, S2.5 readers) — не CRITICAL; при выборе A войдут в consolidation; при B остаются остаточным риском.
- Repair-класс gaps от Layer 4 отложены: приоритет у decision по петле (смешанный отчёт).

## Технический аудит (для движка OpenSpec)

### Слои проверки

- **Layer 1 (Гигиена артефактов):** PASS — checkboxes, slice-gate, Forms & layouts mode (`form_mode`/`layout_mode: n/a`) OK; autofix не применялся.
- **Layer 2 (Internal Coherence):** PASS — QC `OK` (12/12 scenarios; 8b/11 Pass); User Task Contract pre-check none; Code-Truth N/A (kit docs, не phantom BSL); Precedent 2.4 — только ADDED, архивов/KB/ADR нет.
- **Layer 2.5 (Loop Detection):** acceptance-loop-detected — S2 AcceptLoop=0, PatchRounds=3 ≥ acceptance_loop_max=3; отчёт `reports/architecture-loop-redesign-2026-08-01.md` (рекомендация исходная: minimal; оркестратор upgrade→consolidation из-за Layer 4 gap на том же state space).
- **Layer 3 (Problem-Solution Trace):** PASS — Why↔Req↔Scenario↔Slices↔Tasks; scenario-implementation-leak не найден; process-only-marker-suffix N/A (minimal).
- **Layer 4 (Independent Challenge):** CHALLENGE — `reports/design-challenge-2026-08-01.md`; classifier: implementation_invariant (наследник Template-bsl-only; S1 Primary timing; readers table) — deferred Repair Loop из-за decision priority Layer 2.5.
- **Layer 5 (Implementation Readiness):** WARNING — `reports/architecture-task-readiness-2026-08-01.md` вердикт ГОТОВО С ЗАМЕЧАНИЯМИ; manual-config markers none; User Task Contract OK.

### Авто-исправлено (Layer 1)

не применялось

### Развёрнутые карточки развилок

- `acceptance-loop-detected` / open_decision_id: `acceptance-loop-s2`
- Layer 4 gaps (repair after decision): template-fill-only-successor; S2.5 operational readers; optional S1.accept timing prose

## Источники

- `reports/quality-control-2026-08-01.md`
- `reports/design-challenge-2026-08-01.md`
- `reports/architecture-task-readiness-2026-08-01.md`
- `reports/architecture-loop-redesign-2026-08-01.md`
- `reports/architecture-extend-coherence-2026-08-01.md`
- Алерты: `acceptance-loop-detected`; Layer 4 `CHALLENGE` / implementation_invariant; Layer 5 SUBOPTIMAL gaps; QC SUGGESTION `accept-scenario-name-paraphrase`
