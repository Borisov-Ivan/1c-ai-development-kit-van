# Срез S1: Канон Mode Gate и зеркала

**Сценарий:** Вопрос режима формы и эталоны «хорошо» читаются на языке Конфигуратор / репозиторий / модуль формы.
**Primary acceptance:** В каноне Mode Gate три варианта без skill/compile/поставки; lexicon и decision-block не учат «через skill»; faq/quick-start на `form_mode`, макет в new не обещают.
**Приёмка:** Primary пройден по grep и выборочному чтению канона.
**Связь со spec:** Mode Gate question is product language; Good examples do not teach jargon; FAQ matches form-only Mode Gate; Mode question has no process preamble
**Зависимости:** —

<!-- slice-gate: канон Mode Gate и эталоны без skill/compile в chat-facing -->

- [x] S1.1 Переписать § «Формулировка вопроса (чат)» в `.cursor/rules/forms-mxl-mode-gate.mdc` на канон вручную/автоматически Form.xml/программно; skill-оговорки оставить agent-only (Behavior Contract Mode Gate)
- [x] S1.2 Обновить эталоны «хорошо»/anti-example в `.cursor/docs/templates/decision-block.md` и замены в `.cursor/docs/chat-lexicon.md` без «через skill» (Scenario: Good examples)
- [x] S1.3 Синхронизировать `.cursor/docs/faq-kit.md` и `.cursor/docs/quick-start.md`: `form_mode`, без макета в new, без skill в user-facing таблице (Scenario: FAQ matches)
- [x] S1.4 Убрать «через skill» из `.cursor/skills/openspec-explore/templates/handoff-block.md` (ярлыки режима формы)
- [x] S1.5 Добавить в `.cursor/skills/openspec-new-change/SKILL.md` шаг 5.d.1 HALT процессных преамбул перед вопросом режима формы (Scenario: Mode question has no process preamble)
- [x] S1.accept Принять срез S1 «Канон Mode Gate и зеркала» — канон и зеркала без жаргона kit:
  - **Primary (обязательно):** открыть канон Mode Gate и эталоны decision-block/lexicon/faq — нет `skill compile`, «через skill», «уже в поставке»; faq на `form_mode`
  - Scenario «Mode question has no process preamble» (опционально): в new SKILL есть явный HALT преамбул

# Срез S2: Copy-paste команд P0

**Сценарий:** AskQuestion и thin-chat new/apply/status/review/verify без имён гейтов, Schema и slug агентов.
**Primary acceptance:** User-facing шаблоны apply/new/review/status/verify не содержат Gate/Schema/onec-code-* в тексте для чата; полный handoff помечен как файл-only.
**Приёмка:** Primary по grep и точечному чтению шаблонов.
**Связь со spec:** Slice acceptance prompt without gate names; Apply pause label is product language; Review fix prompt without agent slugs; Status and handoff separate chat from file
**Зависимости:** S1

<!-- slice-gate: AskQuestion и thin-chat без Gate/Schema/onec-code в тексте для чата -->

- [x] S2.1 В `.cursor/skills/openspec-new-change/SKILL.md` заменить user-facing строки с именем внутреннего гейта архитектуры и «(Recommended)» на русский язык эффекта (Scenario: Status and handoff / AskQuestion hygiene)
- [x] S2.2 В `.cursor/skills/openspec-apply-change/SKILL.md` переписать AskQuestion приёмки среза без имени гейта; колонку «Пошаговая пауза» заменить разрешённой формулировкой на языке эффекта; T-HANDOFF с Schema/таблицами пометить только для `reports/handoff-*.md` (Scenarios: Slice acceptance; Apply pause label; Status and handoff)
- [x] S2.3 В `.cursor/skills/openspec-status/SKILL.md` и T-STATUS §5.4 opsx-output-style — prose-снимок без Schema и таблиц в чат (Scenario: Status and handoff)
- [x] S2.4 В `.cursor/skills/review/SKILL.md` AskQuestion на fix без `onec-code-*` (Scenario: Review fix prompt)
- [x] S2.5 Синхронизировать CTA в `.cursor/skills/openspec-verify-change/templates/card-decision.md` с chat-summary; переписать или deprecated `chat-summary-example-hash-duplicate-check.md` (Scenario: Status and handoff / verify shape)
- [x] S2.accept Принять срез S2 «Copy-paste команд P0» — шаблоны команд без жаргона гейтов в чате:
  - **Primary (обязательно):** grep user-facing блоков apply/new/review/status/verify — нет `Пошаговая пауза`, `Slice Gate`/`Architect Gate` в copy-paste для чата, `**Schema:**` в чат-шаблоне, `onec-code-` в AskQuestion review
  - Scenario «Apply pause label is product language» (опционально): варианты паузы/продолжения на языке эффекта
  - Scenario «Status and handoff» (опционально): T-HANDOFF явно file-only

# Срез S3: SSOT-конфликты и приёмка

**Сценарий:** opsx, brief-card и lexicon согласованы; «спроси пользователя» привязан к канону; grep-приёмка зелёная.
**Primary acceptance:** Нет противоречия KB в брифе и имён агентов; chat-facing grep по списку приёмки пуст.
**Приёмка:** Primary по правкам opsx + финальный grep.
**Связь со spec:** Entry brief excludes KB list; Agent names banned uniformly
**Зависимости:** S2

<!-- slice-gate: opsx согласован с lexicon; grep chat-facing по списку design пуст -->

- [x] S3.1 В `.cursor/docs/opsx-output-style.md` свести §2 и P2/P8 с баном агентов; §7.7 KB — не требовать в entry-брифе (как brief-card) (Scenarios: Entry brief; Agent names)
- [x] S3.2 В `.cursor/skills/openspec-extend-change/SKILL.md`, `.cursor/skills/openspec-explore/SKILL.md`, `.cursor/skills/openspec-verify-change/SKILL.md` (AskQuestion drift / new-req / scope): привязать вопросы к decision-block (A/B) или brief-card B2 (1/2/3) с русскими вариантами (Behavior Contract SSOT)
- [x] S3.3 Обновить `.cursor/docs/casebooks/form-module-notes.md` ярлыками Mode Gate без «через skill»; при устаревании сверить `.cursor/docs/ux-acceptance-isolated-chat.md`
- [x] S3.4 Прогнать grep-приёмку по зонам и токенам из design § «Список grep-приёмки (chat-facing)»; исправить остатки. Правки в файлах S1/S2 — только точечный closure без переоткрытия оси решений и без повторного slice-gate S1/S2
- [x] S3.accept Принять срез S3 «SSOT-конфликты и приёмка» — единый запрет жаргона и чистый grep:
  - **Primary (обязательно):** opsx не требует KB в брифе и не разрешает slug агентов вопреки lexicon; финальный grep chat-facing по списку приёмки из design пуст
  - Scenario «Agent names banned uniformly» (опционально): точечная сверка §2 vs §3.1
