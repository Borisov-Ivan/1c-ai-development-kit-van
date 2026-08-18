# Architecture review (kit meta) — chat-surface-clarity

**Режим:** self-review fallback (нет кода 1С; эволюция chat surface kit).  
**Дата:** 2026-08-01

## Scope

Правки только chat-facing текстов в `.cursor/**`. Интеграция с конфигурацией 1С отсутствует.

## Findings

1. **SSOT hierarchy** — предложенная цепочка budget → decision-block/brief-card → opsx §2.6 → каноны команд согласована с существующим Chat Surface Contract. Новых параллельных гайдов не вводить.
2. **Mode Gate** — корневой дефект: эталон copy-paste нарушает Тест понятности, на него ссылаются lexicon и decision-block. Волна 1 обязательна первой.
3. **Apply/status** — вторичные утечки (Gate names, Schema, «пошаговая пауза») согласованы с HALT lexicon; правка шаблонов достаточна без изменения vertical-slices логики.
4. **Architect Gate (1С)** — не применим: нет перехватов, метаданных, Form.xml. Триггеры structural сработали из-за числа файлов kit — закрыто этим отчётом.

## Recommendation

Принять design и срезы S1→S2→S3. Блокеров нет.
