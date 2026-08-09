# Capability: explain-post-implementation-scope

Handoff охвата обработанного кода из review/apply в `/opsx:explain` и подтверждение рамки в B-explain.

## ADDED Requirements

### Requirement: Explain scope section in review and apply artifacts

После `/review` / `/release-review` main report MUST содержать секцию `## Explain scope` со списком обработанных `.bsl` (и желательно процедур). После apply с изменением BSL секция MUST появляться в `code-map.md` (SSOT охвата); в `handoff-acceptance-*` — копия секции текущего среза или ссылка на code-map (не отдельный `temp/explain-handoff-*.md`).

#### Scenario: Review report has Explain scope

- **WHEN** оркестратор сохраняет main review report
- **THEN** в конце отчёта есть `## Explain scope` с `source: review`, списком `files` и ссылкой на отчёт

#### Scenario: Apply artifacts have Explain scope

- **WHEN** завершён срез apply с правками BSL (acceptance) или final change с BSL
- **THEN** в `code-map.md` есть `## Explain scope` с `source: apply` и файлами среза/change; handoff-acceptance при наличии содержит ту же секцию или ссылку на code-map

### Requirement: Propose explain after review and apply

Финалы `/review`, `/release-review` и apply (acceptance/final при BSL) MAY предлагать `/opsx:explain` по охвату, когда scope подходит; блокеры fix/extend MUST иметь более высокий приоритет. Trivial light-review без findings MUST NOT требовать propose как default.

#### Scenario: Review offers explain

- **WHEN** `/review` завершён с подходящим scope (несколько файлов/точек или после fix-цикла) и нет нерешённого MUST_FIX ask
- **THEN** в «Куда дальше» / финале может появиться предложение `/opsx:explain` по охвату ревью

#### Scenario: Apply offers explain

- **WHEN** apply acceptance или final после BSL-правок
- **THEN** T-HANDOFF или short-cut может предложить `/opsx:explain` по карте правок

#### Scenario: Trivial review skips default propose

- **WHEN** light-review одного файла без findings
- **THEN** обязательный propose explain не требуется

### Requirement: B-explain prefill from handoff

При входе `/opsx:explain` с `@` на review-report / code-map / handoff-acceptance (или эквивалент «по ревью» / «по срезу» в сессии) оркестратор MUST построить B-explain со слотом **Охват** (или **Варианты** для огромного release scope), отражающим обработанный код, и путями в **Контекст**; карта точек MUST NOT начинаться до подтверждения брифа.

#### Scenario: Prefill Охват from review

- **WHEN** пользователь вызывает `/opsx:explain` на review report с `## Explain scope`
- **THEN** бриф содержит Сценарий post-review, Вопрос, Охват (UX) и Контекст со списком path; Подтвердить? до карты

#### Scenario: Huge release uses Варианты

- **WHEN** источник — `/release-review` full-extension с очень широким scope
- **THEN** бриф использует **Варианты** рамки (например Tier1 / файлы с замечаниями / весь scope), а не обязательный полный Охват всего cfe

#### Scenario: No mass Read before confirm

- **WHEN** бриф ещё не подтверждён
- **THEN** нет массового обхода `.bsl` / Task inventory вне чтения ≤3 указанных артефактов для сборки брифа

### Requirement: Brief HALT allows compact post-implementation scope

Правила B-explain MUST запрещать сырой inventory / коды точек как замену Сценарию. При source=review|apply MUST разрешать в слоте **Охват** только UX-абзац (без полного списка path), а маркированный список `path` и опциональные имена процедур из `## Explain scope` — только в слоте **Контекст**.

#### Scenario: Compact paths allowed

- **WHEN** source=review или apply и в handoff есть files/procedures
- **THEN** бриф может включать краткий UX-охват в Охват и маркированный список path в Контекст без нарушения бюджета ≤6 слотов; полный список path не размещается в слоте Охват

### Requirement: Explore propose remains intact

Предложение `/opsx:explain` из explore при цепочке точек MUST продолжать работать; эта ЗНИ MUST NOT ломать explore shortcut.

#### Scenario: Explore still suggests explain

- **WHEN** explore-синтез находит цепочку точек
- **THEN** «Дальше» по-прежнему может предложить `/opsx:explain`
