# Замер бюджета always-apply — после S2

**Change:** kit-evolution-models-economy-profiles  
**Дата:** 2026-08-16  
**Методика (D6):** факт = сумма байт файлов `.cursor/rules/*.mdc` с `alwaysApply: true` плюс `AGENTS.md`, измеренная после всех правок среза. Заявленные дельты мер не суммировались.

**Порог:** ≤ 34 КБ (34816 байт)

## Состав набора

| Файл | Байты |
|------|------:|
| `.cursor/rules/1c-agent-delegation.mdc` | 13133 |
| `.cursor/rules/chat-output-budget.mdc` | 6202 |
| `.cursor/rules/AGENTS.md` → `AGENTS.md` (корень) | 6622 |
| `.cursor/rules/session-discipline.mdc` | 4803 |
| `.cursor/rules/gate-dispatcher.mdc` | 3205 |
| **Итого** | **33965** |

4 правила always-apply + `AGENTS.md`.

**Итог:** 33965 байт ≈ **33,17 КБ** — ниже порога 34 КБ (запас 851 байт).

Разжалованные (не входят в сумму): `1c-xml-write-guard.mdc`, `command-skill-gate.mdc`, `command-session-persistence.mdc`, `context-strategy-gate.mdc`.  
Удалённые: `bsl-write-guard.mdc`, `conversational-discipline.mdc`, `orchestrator-as-navigator.mdc`.
