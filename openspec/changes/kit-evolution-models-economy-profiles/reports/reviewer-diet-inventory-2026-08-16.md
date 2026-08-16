# Инвентарь чек-листов reviewer — до и после диеты (S3.2 / S3.7)

**Change:** kit-evolution-models-economy-profiles  
**Дата:** 2026-08-16  
**Эталон до диеты:** `.cursor/agents/onec-code-reviewer.md` v4.0 (662 строки, 67 119 байт)

## До диеты (S3.2)

Секции промпта и характер пунктов:

| Секция агента | Характер | Пункты / содержание |
|---|---|---|
| ROLE | ядро | роль, скепсис |
| REVIEW PHILOSOPHY | ядро | 6 принципов |
| PROMPT CONTRACT VERSION | ядро | v4 |
| DESIGN AUTHORITY & QUALITY DISPOSITION | ядро (не выносить) | design-prescribed, agreement-override, whitelist silent Evidence |
| INPUT CONTRACT | ядро | таблица evidence-блоков |
| PATHS | ядро | project.md |
| REFERENCE: AP REGISTRY | ядро/указатель | 4 обязанности |
| RISK MODEL | ядро | оси, формула, эвристики recurrent / subjective / frequency |
| REVIEW BOUNDARIES | ядро | diff-focused / full / BOUNDARY_EXCEPTION |
| RELEASE-HYGIENE RULES | чек-лист | AP-040..045, 051, 053, 054; whitelist vs язык |
| AVAILABLE TOOLS | справочник | LSP, skills, RLM |
| Phase 0.1–0.4 | чек-лист | Intent/Contract/Knowledge; Evaluation Checklist Q1–Q6 |
| Phase 1 / 1b / 1c / 1d | чек-лист | Linter / Naming / Comment Hygiene gates |
| Phase 2 | чек-лист | AP-pass, vendor, &ИзменениеИКонтроль |
| Phase 2.5 A–D | чек-лист | Попытка audit, default verdicts, Defensive Checks, Investigation Request |
| Phase 2.6 A–C | чек-лист | identity-filter AP-055 |
| Phase 3 / 3.5 | чек-лист | context; self-review yaml |
| Phase 4 + REPORT FORMAT | ядро | Summary, Findings, QualityFlag, appendix |
| PRE-RELEASE MODE | ядро/указатель | §12 + эскалация |
| ERROR HANDLING | ядро | сбой инструментов, self-review |
| METRICS TRACKING | справочник | RLM |
| CRITICAL RULES | ядро | 11 пунктов |
| INVOCATION | ядро | apply / review |

Категории 1–15 и детальный workflow уже жили в `.cursor/docs/standard/reviewer-checks.md` (дубль со справочником в агенте).

## После диеты (S3.7)

Промпт: `.cursor/agents/onec-code-reviewer.md` v4.1 (~15 КБ). Чек-листы — `.cursor/docs/standard/reviewer-checks.md` (+ шапка «агент читает разделы по типу задачи»).

| Пункт до | Куда переехал | Исчез? |
|---|---|---|
| ROLE, PHILOSOPHY, CONTRACT, DESIGN AUTHORITY, INPUT, PATHS, AP pointer | агент (ядро) | нет |
| RISK MODEL, REVIEW BOUNDARIES, REPORT FORMAT, CRITICAL RULES, INVOCATION | агент (ядро) | нет |
| RELEASE-HYGIENE AP-040..054 | `reviewer-checks.md` §9 + Phase 2 | нет |
| AVAILABLE TOOLS / RLM | `reviewer-checks.md` § AVAILABLE TOOLS | нет |
| Phase 0.1–0.4, Q1–Q6 | `reviewer-checks.md` Phase 0 | нет |
| Phase 1b/1c/1d | `reviewer-checks.md` Phase 1b–1d | нет |
| Phase 2 AP-pass / vendor / &ИзменениеИКонтроль | `reviewer-checks.md` Phase 2 | нет |
| Phase 2.5 A–D | `reviewer-checks.md` Phase 2.5 | нет |
| Phase 2.6 A–C | `reviewer-checks.md` Phase 2.6 | нет |
| Phase 3 / 3.5 детали | `reviewer-checks.md` Phase 3; 3.5 сжато в агенте | нет |
| Categories 1–15 | `reviewer-checks.md` §1–15 | нет |
| PRE-RELEASE / §12 | агент (указатель) + `reviewer-checks.md` §12 | нет |
| Строка `Checklists read:` | агент REPORT FORMAT + `review/SKILL.md` граничные случаи | добавлено |

**Итог:** ни один пункт исходного промпта не удалён без адресата. Справочник переехал; DESIGN AUTHORITY остался в агенте.
