## Context

Chat surface kit уже описан в `chat-output-budget`, `decision-block`, `brief-card`, `opsx-output-style` §2.6. На практике часть канонов (Mode Gate, apply AskQuestion, status, «хорошие» примеры lexicon/decision-block) противоречит Тесту понятности. Карта волн этой ЗНИ — срезы S1→S2→S3 ниже (канон → copy-paste команд → SSOT+grep); внешние черновики аудита не являются источником истины. Это эволюция kit на ветке, без прикладного кода 1С.

## Goals / Non-Goals

**Goals:**

- Единый язык чата: разработчик 1С отвечает из одного сообщения без словаря kit.
- Каноны copy-paste и эталоны «хорошо» не содержат skill/compile/Gate/Schema/onec-code-* в user-facing.
- Иерархия SSOT без третьего формата «спроси как-нибудь»: decision-block (A/B) vs brief-card (1/2/3).

**Non-Goals:**

- Переписывание слоёв verify, GO/NO-GO в отчётах, XML/BSL guards.
- Слияние форматов A/B и 1/2/3 в один.
- Создание `openspec/project.md` / маркеров BSL для этой ЗНИ.

## Decisions

1. **Граница chat-facing vs agent-facing** — правим только тексты, уходящие пользователю или помеченные «копировать в чат»; таблицы режимов `form_mode` / skill в agent-секциях остаются.
   - **Mode Gate (`forms-mxl-mode-gate.mdc`):** единственный copy-paste в чат — секция «Формулировка вопроса (чат)» (три русских варианта). Остальные секции файла (таблицы `form_mode`, HALT, skill compile/edit, инструкции apply) — agent-facing, в чат не копировать.
   - **Аналогично** в dual-language skills: блоки AskQuestion / «в чат» / thin handoff — chat-facing; тела Layer/pipeline/промпты Task — agent-facing.
2. **Канон Mode Gate** — три русских варианта (вручную / автоматически Form.xml в репозитории / программно модуль); условие наличия skill — agent-only после выбора.
3. **Thin chat vs файл** — полный T-HANDOFF с Schema/таблицами только в `reports/handoff-*.md`; в чат — thin по §5.2.
4. **KB в entry-брифе** — запрещён (как brief-card); §7.7 opsx привести к brief-card.
5. **Имена агентов в чате** — бан (lexicon / §3.1); §2 opsx, разрешавший slug в backticks, привести к бану.

## Implementation Options

- **Option A (выбран):** четыре волны правок текстов по карте аудита + grep-приёмка.
- **Option B (отклонён):** только Mode Gate — не закрывает apply/status/review.
- **Option C (отклонён):** новый параллельный гайд стиля — плодит четвёртый SSOT.

## Behavior Contract

- После выбора режима формы / приёмки среза / verify-развилки / review-fix в чате нет jargon kit из списка приёмки ниже.
- Процессные non-events («Маркер записан», «proposal набросаны») перед вопросом режима формы не выводятся.
- Self-check §2.6 п.8 и lexicon согласованы с каноном Mode Gate.
- Финальный grep S3 — **кумулятивная приёмка change**: точечные остатки в файлах S1/S2 допустимы без повторного slice-gate S1/S2; ось решений Mode Gate / thin-chat / бан агентов не переоткрывается.

### Список grep-приёмки (chat-facing)

**Запрещённые подстроки** в текстах, которые оркестратор копирует в чат (AskQuestion, канон вопроса, thin status/handoff, эталоны «хорошо»):

| Токен / паттерн | Где искать |
|-----------------|------------|
| `skill compile`, `skill edit`, «через skill», «уже в поставке» | Mode Gate chat-секция, decision-block, lexicon, faq/quick-start, handoff-block |
| `Пошаговая пауза` | apply AskQuestion / таблицы режимов apply в user-facing |
| `Slice Gate`, `Architect Gate` как заголовки/ярлыки для пользователя | apply/new AskQuestion copy-paste |
| `**Schema:**` / markdown-таблицы срезов в чат-шаблоне | status, T-HANDOFF thin vs file |
| `onec-code-` в тексте вариантов для пользователя | review AskQuestion |

**Зоны grep (S3.4):** `.cursor/docs/templates/decision-block.md`, `.cursor/docs/chat-lexicon.md`, `.cursor/docs/faq-kit.md`, `.cursor/docs/quick-start.md`, `.cursor/docs/opsx-output-style.md` (user-facing §), `.cursor/rules/forms-mxl-mode-gate.mdc` **только** секция «Формулировка вопроса (чат)», chat-facing фрагменты skills `openspec-new-change`, `openspec-apply-change`, `openspec-status`, `openspec-verify-change/templates/*`, `openspec-explore/templates/handoff-block.md`, `review`, `openspec-extend-change` / `openspec-explore` (AskQuestion), `.cursor/docs/casebooks/form-module-notes.md`, при устаревании `ux-acceptance-isolated-chat.md`.

**Исключено из grep:** agent-only таблицы `form_mode`/skill, тела Layer/pipeline verify, промпты Task, XML/BSL guards, technical audit в `reports/`.

## Design Rationale

Точка правки — SSOT-каноны и шаблоны команд, потому что оркестратор обязан копировать их «как есть». Менять только runtime-stub без эталонов недостаточно: lexicon и decision-block сейчас зелёно ссылаются на плохой Mode Gate.

## Slices

| Срез | Имя | Сценарий | Файлы (ядро) | Primary acceptance | Зависимости |
|------|-----|----------|--------------|--------------------|-------------|
| S1 | Канон Mode Gate и зеркала | Вопрос режима формы и эталоны без skill | forms-mxl-mode-gate, decision-block, chat-lexicon, faq-kit, quick-start, handoff-block, openspec-new-change (HALT преамбул) | В чате канон 1/2/3 без skill; faq/quick-start на form_mode | — |
| S2 | Copy-paste команд P0 | new/apply/status/review/verify без жаргона гейтов | openspec-new-change, openspec-apply-change, openspec-status, review, card-decision, chat-summary-example-* | AskQuestion/шаблоны чата без Gate/Schema/onec-code-*; thin handoff | S1 |
| S3 | SSOT-конфликты и приёмка | opsx + gaps AskQuestion + grep | opsx-output-style, extend/explore ask paths, form-module-notes, ux-acceptance (при устаревании) | Grep chat-facing чист; KB не в брифе; агенты забанены единообразно | S2 |

### Матрица приёмки

| Scenario (capability) | S1 | S2 | S3 |
|----------------------|----|----|-----|
| Mode Gate канон понятен | Primary | | |
| Нет skill в эталонах | Primary | | |
| Нет Gate/Schema в chat copy-paste | | Primary | |
| Apply pause label product language | | Primary | |
| Thin handoff / status prose | | Primary | |
| SSOT без противоречий KB/агенты | | | Primary |
| Grep-приёмка chat-facing | | | Primary |

**Primary acceptance:**

- S1: открыть канон Mode Gate — три варианта на языке Конфигуратор/репозиторий/модуль; lexicon и decision-block не содержат «через skill» как эталон.
- S2: в user-facing AskQuestion apply/new/review и status нет имён гейтов, «Пошаговая пауза», Schema:, onec-code-*; T-HANDOFF помечен как файл-only.
- S3: opsx §2/§7.7 согласованы с lexicon/brief-card; grep по списку приёмки из design § «Список grep-приёмки» — пусто в chat-facing зонах.

## Risks / Trade-offs

- [Риск] Модель всё ещё «улучшит» вопрос жаргоном → Mitigation: жёсткий «копировать как есть» + anti-example в decision-block.
- [Риск] Большой diff по skills → Mitigation: только chat-facing абзацы, не переписывать целые SKILL.
- [Риск] Устаревшие test-cases explore ссылаются на старые фразы → Mitigation: править при падении grep или явно в S3.

## Open Questions

- Нет блокирующих. P2 meta-docs (`delivery-integrity`, `kit-template-workflow`) — по желанию в S3, не блокер.
