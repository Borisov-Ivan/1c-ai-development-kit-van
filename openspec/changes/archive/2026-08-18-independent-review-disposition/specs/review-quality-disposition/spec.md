# Capability: review-quality-disposition

Независимая оценка качества в `/review` и `/release-review` и disposition заказчика (as-designed / queue-fix).

## ADDED Requirements

### Requirement: Agreement does not silently close quality findings

Ревьюер MUST сохранять finding по качеству, когда код слаб или рискован, даже если design/ТЗ/ADR явно допускает такое поведение. Тихий перевод в VERIFIED_OK/OK **только** из-за цитаты design MUST NOT применяться вне явно перечисленного узкого whitelist Evidence-типов (не «просто есть фраза в design»).

#### Scenario: Design endorses weak pattern

- **WHEN** в коде паттерн, который без Evidence был бы MUST_FIX/HIGH+, и в design есть явное допущение (spec-explicit-tolerance / Hardcode Justification / «по design»)
- **THEN** отчёт содержит finding с QualityFlag weak (или эквивалент) и Disposition needs-confirm (или ожидает disposition оркестратора), а не единственный VERIFIED_OK без видимости заказчику

#### Scenario: Design-prescribed anti-pattern

- **WHEN** код реализует антипаттерн, предписанный design
- **THEN** finding помечен tag `design-prescribed` (или эквивалент) и не считается закрытым согласием постановки до disposition

### Requirement: Architectural Context is intent, not PASS criterion

Промпт ревьюера MUST трактовать Architectural Context как факты намерения и источник поиска contradiction / design-prescribed. Соответствие design MUST NOT быть единственным критерием PASS по качеству.

#### Scenario: Prompt framing

- **WHEN** оркестратор передаёт Architectural Context из design/architecture report
- **THEN** инструкции ревьюеру не сводятся к «оценивать решения на соответствие контексту» как к финальному verdикту качества

### Requirement: Unified disposition UX for ordinary and prerelease review

После main report оркестратор MUST предложить заказчику disposition для weak / design-prescribed findings: as-designed, queue-fix (и опционально defer). Один и тот же протокол MUST действовать при `release_mode=false` и `release_mode=true` без дублирования логики в отдельных командах.

#### Scenario: Ordinary review disposition

- **WHEN** завершён `/review` с хотя бы одним finding, требующим disposition
- **THEN** в чате предлагается выбор as-designed / queue-fix до того, как замечание считается «закрытым согласием постановки»

#### Scenario: Prerelease same protocol

- **WHEN** завершён `/release-review` с finding, требующим disposition
- **THEN** используется тот же алгоритм disposition, что и для `/review`

#### Scenario: As-designed recorded

- **WHEN** заказчик выбирает as-designed
- **THEN** disposition записывается в main report (finding-id, Design ref, кто/когда) и finding НЕ передаётся writer

#### Scenario: Queue-fix routed

- **WHEN** заказчик выбирает queue-fix для CODE
- **THEN** finding попадает в существующий fix-loop (writer/simplifier) или в extend при ARCHITECTURE / contradiction design

### Requirement: Prerelease hygiene not waived by as-designed alone

Выбор as-designed для functional/quality weak MUST NOT снимать требования Category 12 / release-hygiene без отдельного явного waive на эту категорию.

#### Scenario: Release-hygiene remains

- **WHEN** prerelease finding относится к release-hygiene (Category 12 / эскалация hygiene) и заказчик выбрал as-designed для связанного quality weak
- **THEN** hygiene-требование остаётся открытым, пока не исправлено или не выписан отдельный waive

### Requirement: Customer-visible guidance

Памятка заказчика MUST описывать сценарий «совпадает с постановкой, но спорно по качеству» и смысл выбора as-designed vs исправить — без внутренних имён агентов.

#### Scenario: Guide updated

- **WHEN** заказчик читает review-guide после внедрения
- **THEN** он понимает, что «так в design» не означает автоматический ок и какие два действия доступны после флага

### Requirement: Apply-reviewer does not run disposition AskQuestion

Контур apply-reviewer MUST NOT блокировать цикл AskQuestion as-designed/queue-fix. Weak / design-prescribed MUST NOT авто-waive без следа; допускается авто-fix functional MUST_FIX или open-пометка для последующего `/review`.

#### Scenario: Apply speed preserved

- **WHEN** apply-reviewer находит CODE MUST_FIX без QualityFlag weak
- **THEN** авто-fix работает как прежде

#### Scenario: Weak not silently waived in apply

- **WHEN** apply-reviewer видит QualityFlag weak / design-prescribed
- **THEN** замечание не считается авто-принятым as-designed; в отчёте задачи остаётся след для disposition на `/review` или `/release-review`
