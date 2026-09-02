## Extend — 2026-09-02

- источник: `--from-verify` (internal repair-from-verify), `reports/design-challenge-2026-09-02.md`
- что добавлено/изменено:
  - design/tasks/specs: путь опционального файла передачи `temp/explore-handoff-*.md` (корень `temp/`, не `temp/reports/`);
  - положительный allowlist имён вместо префикса `architecture-*` (переезд и поиск продолжения);
  - источник поля «Исходный запрос» при дописывании шапки — слот «Вопрос» или сжатие 1–2 предложения, не полная реплика чата;
  - граница шапки: обязательна у отчётов исследования, не у служебных отчётов проверки постановки;
  - после переезда журнала разбора — href на `src/` с глубины каталога ЗНИ.
- disposition: accepted (уточнение контракта выбранного пути, ось переезда + шапка не меняется)
- Architect Gate: не требовался — ось не пересматривается; независимый разбор постановки уже выполнен (`reports/design-challenge-2026-09-02.md`)
- следующий шаг: повтор слоёв проверки постановки (internal Repair Loop, `repair_attempt: 1`)

## Verify decision ledger

```yaml
closed_decisions: []
open_decision_id: null
decision_round: 0
verify_depth: full
assumptions_accepted: []
repair_attempt: 1
last_challenge_at: "2026-09-02T12:20:20+09:00"
```
