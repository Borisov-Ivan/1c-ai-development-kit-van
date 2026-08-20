## Срез S2 — передача на приёмку: kit-session-noapi-visibility-and-ru-progress

**Change:** kit-session-noapi-visibility-and-ru-progress
**Прогресс:** 10/10 рабочих задач среза S2 [x]; `S2.accept` — `[ ]`.

### 1. Что реализовано

В бюджете чата progress и вводная речь `/opsx:*` только русские. Профиль Grok не может сменить язык команды и не отменяет канон лимита. Стиль `/opsx:*` отсылает runtime-норму в бюджет чата. В verify английский progress не изобретается.

### Карта правок (перед тестом)

- **S2.1** · бюджет чата · русский progress. [`.cursor/rules/chat-output-budget.mdc`](../../../../.cursor/rules/chat-output-budget.mdc):56-58
- **S2.2** · бюджет чата · пункт «язык». [`.cursor/rules/chat-output-budget.mdc`](../../../../.cursor/rules/chat-output-budget.mdc):66-68
- **S2.5** · профиль Grok · язык команды. [`.cursor/rules/model-grok4.mdc`](../../../../.cursor/rules/model-grok4.mdc):32
- **S2.7** · `/opsx:verify` · без английского progress. [`.cursor/skills/openspec-verify-change/SKILL.md`](../../../../.cursor/skills/openspec-verify-change/SKILL.md):369

Полная карта: `reports/code-map.md`

### 2. Что проверить СЕЙЧАС

**Primary:** в бюджете чата progress и вводная речь `/opsx:*` только русские; в профиле Grok — запрет менять язык команды.

1. Откройте бюджет чата §6 и §1b пункт «язык».
2. Откройте профиль Grok, блок MUST NOT.

### 4. Как вернуться

`/opsx:apply kit-session-noapi-visibility-and-ru-progress`

### 7. Short-cut

«принято» / «срез S2 принят».
