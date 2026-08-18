## Срез S3 — передача на приёмку: chat-surface-clarity

**Change:** chat-surface-clarity  
**Прогресс:** S1+S2 приняты; S3 рабочие 4/4 [x]; `S3.accept` — `[ ]`

### 1. Что реализовано

Согласованы SSOT чата: opsx не требует KB в брифе и не разрешает slug агентов вопреки lexicon; вопросы extend/explore/verify — decision-block или нумерованные варианты; кейсбук форм без «через skill»; финальный grep chat-facing по списку из design — пуст в зонах копирования в чат.

### Карта правок

См. `reports/code-map.md` секции S2 и S3.

### 2. Что проверить СЕЙЧАС

1. opsx §2 / §7.7 — бан агентов и «KB не в entry-брифе»
2. Финальный grep по зонам design § «Список grep-приёмки» — нет запрещённых токенов в текстах для чата

### 3. Как вернуться

`/opsx:apply chat-surface-clarity` — вердикт по S3; после принятия всех срезов — `/opsx:archive chat-surface-clarity`.

### 7. Short-cut

«принято» / «срез S3 принят» — отмечу приёмку.
