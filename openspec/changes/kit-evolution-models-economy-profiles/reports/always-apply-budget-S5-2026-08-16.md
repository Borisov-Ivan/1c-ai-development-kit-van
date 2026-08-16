# Замер бюджета always-apply — после S5 (контрольный, S5.8)

**Change:** kit-evolution-models-economy-profiles  
**Дата:** 2026-08-16  
**Методика (D6):** факт = сумма байт файлов `.cursor/rules/*.mdc` с `alwaysApply: true` плюс `AGENTS.md`. Заявленные дельты не суммировались. Измерение: `Get-Item.Length` (байты на диске).

**Порог:** ≤ 34 КБ (34816 байт)

## Состав набора

| Файл | Байты |
|------|------:|
| `.cursor/rules/1c-agent-delegation.mdc` | 13967 |
| `.cursor/rules/chat-output-budget.mdc` | 6202 |
| `AGENTS.md` | 6492 |
| `.cursor/rules/session-discipline.mdc` | 4774 |
| `.cursor/rules/gate-dispatcher.mdc` | 3227 |
| **Итого** | **34662** |

4 правила always-apply + `AGENTS.md`.

**Сравнение с S2:** после S2 было 33965 байт. Дописывание S5 в диспетчер 1С и правки индекса уложились за счёт сжатия формулировок (якоря D6(в) не удалялись).

**Итог:** 34662 байт ≈ **33,85 КБ** — ниже порога 34 КБ (запас 154 байта).
