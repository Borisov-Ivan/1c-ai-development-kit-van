# Acceptance: isolated chat (регрессия UX)

**Gate перед merge** правил Chat Surface Contract и verify Repair Loop.

## Зачем изолированный чат

Оркестратор не должен опираться на prior turns («да», контекст extend, якорь брифа). Проверка UX — **только** по первому ответу в **новом** чате без истории.

SSOT контракта: `.cursor/docs/opsx-output-style.md` §2.6.

## Протокол

1. **Подготовка:** change в известном состоянии (fixture или git tag «до repair»).
2. **Новый чат (Composer/Agent):** единственное сообщение — команда under test.
3. **Pass/fail** — только по **первому** ответу оркестратора.

## Сценарии A–F

| ID | Команда | Fixture | Pass |
|----|---------|---------|------|
| **A** | `/opsx:verify <name>` | ZNI с repair-only (текстовые пробелы, нет decision) | **1** сообщение; GO; нет «Подтвердить?», `/opsx:extend`, списка файлов |
| **B** | `/opsx:verify <name>` | ZNI с CHALLENGE / A-B | **1** блок вопроса (проблема→последствия→варианты); END TURN |
| **C** | `/opsx:verify <name>` | post-GO, артефакты не менялись | 3–5 строк; «статус прежний: можно apply» |
| **D** | `/opsx:ff <name>` | новый change | T-CONFIRM; **одна** команда next: verify; без перечня файлов |
| **E** | `/opsx:apply <name>` | завершённый срез | handoff на языке эффекта; user-action next step |
| **F** | `/opsx:explore` | симптом | бриф по Правилу 4; финал — блок `## Для /opsx:ff` или один вопрос |

## Anti-patterns (fail)

- «Как в прошлой сессии» / «вы уже подтвердили»
- Internal-команды с путями (`/opsx:extend --from-verify …`)
- Перечень изменённых файлов как handoff
- Explore-бриф на internal repair
- «Ничего не требуется» + «Подтвердить?»
- Перегруз bold/backticks; решение требует открыть файл

## Fixtures (рекомендуемые)

| Сценарий | Change / примечание |
|----------|---------------------|
| A, C | `do2-pavlik-predzapolnenie-viz-shablony` — после repair или tag «до repair» |
| B | тот же change с открытым CHALLENGE (контракт схемы КП) |
| D | любой новый ff из explore-блока |
| E | любой change с готовым срезом к приёмке |
| F | произвольный симптом ДО2 |

Опционально: `temp/ux-fixtures/README.md` с git tag на commit «до repair».

## Чеклист регрессии (gate)

- [ ] A — repair-only verify в новом чате
- [ ] B — decision verify в новом чате
- [ ] C — silent_ok в новом чате
- [ ] D — ff hint verify в новом чате
- [ ] E — apply handoff
- [ ] F — explore бриф/финал

Все six — **pass** перед merge изменений правил.
