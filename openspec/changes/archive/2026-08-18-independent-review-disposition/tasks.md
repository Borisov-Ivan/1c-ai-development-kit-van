# Срез S1: Disposition качества в review

**Сценарий:** После `/review` или `/release-review` спорное качество при endorse design не зелится молча — заказчик подтверждает «так задумано» или ставит в очередь на исправление.
**Primary acceptance:** Given активный change с design, допускающим слабый паттерн; When выполнен `/review` по scope этого change; Then в отчёте/чате есть finding weak (или эквивалент) с ожиданием disposition, предложен выбор as-designed / queue-fix, и при as-designed writer не вызывается для этого finding.
**Приёмка:** ручная проверка протокола review на kit (без обязательной ИБ продукта); сверка отчёта и поведения оркестратора.
**Связь со spec:** Requirement «Agreement does not silently close quality findings», Scenario «Design endorses weak pattern», «Design-prescribed anti-pattern»; Requirement «Unified disposition UX for ordinary and prerelease review», Scenario «Ordinary review disposition», «As-designed recorded», «Queue-fix routed», «Prerelease same protocol»; Requirement «Architectural Context is intent, not PASS criterion»; Requirement «Prerelease hygiene not waived by as-designed alone»; Requirement «Customer-visible guidance»; Requirement «Apply-reviewer does not run disposition AskQuestion».
**Зависимости:** нет
**Режим apply:** mechanical

## 1. Контракт ревьюера

- [ ] S1.1 В `onec-code-reviewer.md` добавить QualityFlag / Disposition (needs-confirm…), Design authority, порог weak HIGH+∪agreement-override (D2), правило AP-042 (D8), whitelist silent VERIFIED_OK (D9) и запрет silent VERIFIED_OK «только цитата design»; bump `prompt_contract_version` 3→4
- [ ] S1.2 В трёх шаблонах `1c-agent-patterns/reviewer.md` заменить framing «на соответствие» на контекст намерения + skeptic stance к Architectural Context; инструкцию эмитить weak при agreement-override
- [ ] S1.3 В `reviewer-checks.md` связать Design authority / `design-prescribed` с алгоритмом disposition (D8); уточнить Phase 2.5/2.6: заполненная Justification ≠ авто-PASS качества; whitelist Evidence — D9
- [ ] S1.4 Верифицировать по коду kit согласованность `expected_reviewer_prompt_contract_version` в `review/SKILL.md` с версией агента

## 2. Оркестратор disposition

- [ ] S1.5 В `review/SKILL.md` переформулировать подачу Architectural Context (шаг 2.2); между шагами 4 и 5 — корзины A/B/C и запись Disposition; шаг 6 фильтрует queue-fix; явно: слой общий для `release_mode` true/false
- [ ] S1.6 В `review/SKILL.md` описать формат секции Disposition в main report и опциональный `review-queue-*.md` (с change / в `temp/reports/`); владение полями — D2 (агент needs-confirm, оркестратор — финальный disposition)
- [ ] S1.7 В `review.md` и `release-review.md` одна строка-указатель на disposition; для release — as-designed не снимает release-hygiene без отдельного waive

## 3. Памятка и стыки

- [ ] S1.8 Обновить `review-guide.md`: сценарий «как в постановке, но спорно», две кнопки, отличие apply (без AskQuestion disposition)
- [ ] S1.9 Точечно в `1c-agent-delegation.mdc` (авто-исправление): carve-out для QualityFlag weak / design-prescribed — не авто-waive; след для disposition на `/review`
- [ ] S1.10 В `openspec-extend-change/SKILL.md` маппинг as-designed ↔ rejected(with reason), queue-fix ↔ accepted для `--from-review` без смешения семантик
- [ ] S1.11 Верифицировать по коду kit покрытие scenarios spec (grep Disposition/QualityFlag/design-prescribed в изменённых файлах; whitelist silent VERIFIED_OK из D9 перечислен в skill или agent)

- [x] S1.accept Принять срез S1 «Disposition качества в review» — независимый флаг качества и выбор as-designed / queue-fix на `/review`:
  - **Primary (обязательно):** на change с design-endorse слабого паттерна выполнить `/review` → увидеть weak/needs-confirm и выбор as-designed / queue-fix; при as-designed writer для этого finding не запускается; запись disposition есть в отчёте
  - Scenario «Prerelease same protocol» (опционально): убедиться по skill, что `/release-review` ссылается на тот же протокол (отдельный прогон не обязателен)
  - Scenario «Guide updated» (опционально): в `review-guide.md` читается смысл двух кнопок без имён агентов
  - Scenario «Apply speed / weak not waived» (опционально): по delegation — apply без AskQuestion disposition, weak не авто-as-designed

<!-- slice-gate: Primary — /review показывает disposition и as-designed не уходит в writer -->
