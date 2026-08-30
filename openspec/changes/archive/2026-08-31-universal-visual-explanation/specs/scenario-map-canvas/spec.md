## REMOVED Requirements

### Requirement: Silence unless asked or hinted

**Reason:** Молчание не давало схему, когда ответ без картинки хуже. Заменено появлением панели по просьбе и когда структура ответа этого требует.
**Migration:** `visual-explanation` — «Direct request opens a visual explanation», «Panel appears when a picture makes the answer easier».

### Requirement: Direct request draws the scenario map

**Reason:** Порог четырёх сущностей, обязательный журнал и закрытый граф давали отказ или нечитаемый DAG.
**Migration:** `visual-explanation` — «Direct request opens a visual explanation».

### Requirement: Show-scheme phrase is a direct request

**Reason:** Узнавание фразы нужно, но оно было привязано к старому порогу и источнику-отчёту.
**Migration:** `visual-explanation` — «Platform schema object is not a kit panel», «Direct request opens a visual explanation».

### Requirement: Technical fallback is not a map

**Reason:** «Текстовый резерв карты» путал журнал с панелью. При отсутствии среды остаётся обычный ответ в чате.
**Migration:** `visual-explanation` — «Unreadable panel is simplified, not refused».

### Requirement: Node contract forbids empty or code-primary nodes

**Reason:** Контракт узла карты сценария снимается вместе с жанром. Запрет выдумывать факты сохраняется в новом capability.
**Migration:** `visual-explanation` — «Panel explains the same question as the chat».

### Requirement: Causal map has layers or branches

**Reason:** Обязательные слои/ветки, скрытая шапка и два средства вида не дали ясности.
**Migration:** `visual-explanation` — «Form follows the content», «Panel explains the same question as the chat».

### Requirement: Offer by topology not by topic

**Reason:** Экзамен топологии предлагал схему не тогда, когда она помогает ответу.
**Migration:** `visual-explanation` — «Panel appears when a picture makes the answer easier».

### Requirement: No dedicated map command

**Reason:** Смысл сохраняется в новом capability, старое требование удаляется вместе с картой.
**Migration:** `visual-explanation` — «No dedicated visualization command».

### Requirement: Two map names stay distinct

**Reason:** Различие «карта точек» / «карта сценария» / «текстовый резерв» больше не нужно: остаётся список точек разбора в чате и панель объяснения.
**Migration:** Карта точек разбора — скилл пошагового разбора. Панель — `visual-explanation`.

### Requirement: Hint only on an existing decision line

**Reason:** Намёк «карта сценария» как отдельный жанр снимается. Предложение панели — только если картинка упрощает этот ответ.
**Migration:** `visual-explanation` — «Panel appears when a picture makes the answer easier».

### Requirement: Map outside walkthrough uses named source

**Reason:** Запрет собирать схему из текущего ответа в чате мешал ясности.
**Migration:** `visual-explanation` — «Direct request opens a visual explanation».
