## Why

При создании ЗНИ оркестратор может выдать два выбора в одном сообщении (маркер автора и способ поставки формы), а единый `artifact_mode` не даёт задать разные режимы для **разных форм** в одной ЗНИ. Заказчик не понимает, как отвечать, и не может выбрать, например, одну форму вручную, а другую программно.

## Metadata (comment markers)

developer: <ФИО>
comment_suffix:
marker_style: minimal

## Forms mode

form_mode: n/a

## What Changes

- Жёсткий инвариант: в одном ходе чата — не больше одного вопроса выбора; после вопроса — пауза до ответа; Metadata Gate и Mode Gate не смешиваются.
- Mode Gate касается только **управляемых форм**: режим `form_mode` (`manual` | `assisted` | `bsl-only` | `n/a`). Вопрос — на этапе design, **по одной форме** на каждую форму в scope (разные формы могут иметь разные режимы); END TURN между вопросами.
- **Макеты (Template/MXL) вне Mode Gate этой ЗНИ:** вопрос про поставку макета не задаётся. По умолчанию макеты правятся только вручную; программная правка макета — только по явному разрешению пользователя во время `/opsx:apply`.
- Новые proposal не пишут единый `artifact_mode` как единственный источник истины для форм; пишут `form_mode` / список режимов по формам. Legacy `artifact_mode` читается как fallback для `form_mode`.
- Опционально: маркер задач `[form:…]` — Follow-up.

## Capabilities

### New Capabilities

- `sequential-gate-questions`: один вопрос выбора за ход в `/opsx:new` (и связанных карточках); запрет параллельных выборов Metadata и Mode Gate.
- `split-form-layout-modes`: режимы поставки **управляемой формы** (per-form `form_mode`) в proposal и на apply/verify; макеты — политика default manual без Mode-вопроса в new.

### Modified Capabilities

- (нет существующих specs в `openspec/specs/` — capability вводятся как New)

## Impact

- `.cursor/skills/openspec-new-change/SKILL.md` — порядок гейтов, END TURN, Mode Gate форм на design (цикл по формам).
- `.cursor/rules/forms-mxl-mode-gate.mdc` — вопрос только про форму; политика макета (manual default / permission on apply).
- `.cursor/docs/templates/brief-card.md` — Metadata Gate без соседних вопросов.
- `.cursor/skills/openspec-apply-change/SKILL.md`, `openspec-verify-change/SKILL.md` — чтение `form_mode` (per-form) + fallback `artifact_mode`; макет без Mode-вопроса.
- Ссылки в `1c-forms`, handoff explore, `kit-template-workflow.md` — согласовать термины; `1c-mxl` — политика manual default без resurrect Mode Gate макета.
- Ветка `kit-evolution-sequential-ui-mode-questions`; в `main` мержится только итог `.cursor/**` (папка change не поставляется).

## Open follow-ups

- [ ] F1 Заполнить `developer` в proposal.md (и при необходимости project.md), если появятся маркеры в коде — сейчас маркеры не нужны (эволюция kit).
