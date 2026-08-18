---
report_type: design-challenge
generated_at: 2026-08-18
agent: onec-code-architect
mode: design-challenge
scope:
  change: kit-session-api-mode
  design_mtime: "2026-08-17T23:44:24Z"
verdict: APPROVE
confidence: high
---

# Design Challenge — kit-session-api-mode

## KB references

- Existing Knowledge: not relevant — таксономия отсутствует, discovery совпадений не дал; KB-ID во входе нет.

## Адверсариальная установка

Повторный разбор по живым `proposal.md`, `design.md`, `specs/session-api-mode/spec.md`, `tasks.md`. Прошлый `reports/design-challenge-2026-08-18.md` и любые `reports/architecture-*.md` не использовались как источник истины. Ось «режим сессии vs `project.md`» не переоткрывалась (D1 закрыт пользователем; reopen-blocked id нет).

## Closure of prior implementation_invariant gaps

| # | Инвариант | Закрыт? | Доказательство в живых артефактах |
|---|---|---|---|
| 1 | Токен = целое слово после разбиения по пробелам (`--api-key` не токен) | да | design D2; Behavior Contract; spec Scenario «Ложное слово не включает режим»; tasks S1.1, S1.9 |
| 2 | Дешёвая команда не глотает сигнал: `/opsx:status -noapi` молчит в выводе, но режим переключается | да | design D5 + Behavior Contract; spec «Токен на дешёвой команде» и «Команда без дорогих вызовов молчит»; tasks S1.12, S2.9 |
| 3 | После первой строки про недоступность — без повторной такой строки | да | design D3; Behavior Contract; spec Scenario «Память после лимита»; tasks S1.3, S1.accept |
| 4 | Cue на каждом ходе перед Task с моделью (`session-discipline`), потому что `model-selection` не always-apply | да | design D4 и абзац порядка слоёв; Behavior Contract «Перед каждым вызовом…»; tasks S1.7 |
| 5 | Палитра spec включает explore и extend | да | proposal Impact; design Slices S2 + матрица scenarios; spec Scenario «Подсказка в палитре»; tasks S2.5, S2.6 |
| 6 | Разовый слаг и `-noapi` в одном сообщении: этот вызов со слагом, дальше без API | да | design D7; Behavior Contract; spec Scenario «Разовый слаг и токен в одном сообщении»; tasks S1.4, S1.13 |

Незакрытых implementation_invariant по списку из шести нет. Ось D1–D7 не менялась.

## Three-Question Challenge

### Q1 — Problem-Solution Fit

- **Why говорит:** после исчерпания лимита API каждый следующий дорогой вызов снова бьётся в платную модель и только потом уходит на модель чата; нужны два явных режима в том же чате без настройки репозитория; ключи `-noapi` / `-api` (и с двумя дефисами) в любом сообщении дают однозначный сигнал.
- **Design адресует:** Why «повторный удар после лимита» → D3 + D6 (память только на липкий класс сбоев; шаг 2 текущего вызова обязателен). Why «два режима в том же чате» → D1 + D2. Why «без настройки репозитория» → D1 Non-Goals, Impact не трогает `project.md`. Why «однозначный ключ» → D2 (целое слово) + D5 (дешёвая команда не глотает) + D7 (разовый слаг не сбрасывает режим).
- **Покрытие:** полное. Симптом «шум и зря» закрыт пропуском шага 1 на **новых** вызовах; контракт цепочки на уже ушедшем вызове сохранён.

### Q2 — Optimality

- **Выбранный путь:** один признак сессии у оркестратора; SSOT смысла в `model-selection.mdc`; always-apply cue в уже существующем `session-discipline.mdc`; память только после липкого сбоя.
- **Альтернативы (включая не упомянутые в `## Implementation Options`):**
  1. **Always-apply stub вместо cue в session-discipline** — отдельное always-apply правило «перед Task с моделью прочитай секцию режима». Плюс: не зависит от того, активна ли командная сессия. Минус: ещё один always-apply файл и риск разъехаться с D4 («таблицу токенов не копировать»). Хуже выбранного: `session-discipline` уже always-apply и уже гейтит каждый ход — cue туда дешевле.
  2. **Инвертированный default: все Task без параметра модели, `-api` как opt-in в таблицу ролей** — плюс: после лимита не нужен ни токен, ни память. Минус: ломает контракт `kit-evolution-models-economy-profiles` (таблица ролей по умолчанию) и ADR-слой «дорогая модель → при сбое чат». Хуже выбранного по Blast Radius.
  3. **Пользовательское правило Cursor вне kit-поставки** — плюс: не копируется с `.cursor/**`. Минус: не доезжает до consumer-проекта штатной поставкой kit; Why требует ключ в чате kit-команд. Не решает поставку.
- **Вердикт по Q2:** выбранный путь оптимален. У (1) нет преимущества по числу точек правки; у (2) преимущество «не бить API никогда» ценой отмены таблицы ролей — вне Non-Goals и вне этой оси.

### Q3 — Fresh-Eye Approval

- **Согласовал бы (или нет):** да
- **Причины:**
  - Проблема Why — состояние чата («сегодня нет лимита»), а не репозитория; design это фиксирует без файла между чатами.
  - Наблюдаемое поведение (целый токен, дешёвая команда, одна строка про недоступность, разовый слаг, палитра explore/extend) теперь одно и то же в design, spec и tasks.
  - Двухшаговая цепочка и таблица ролей не переписываются — слой поверх, Blast Radius узкий.

## Verdict

**APPROVE** — шесть implementation_invariant закрыты согласованно в design / spec / tasks; Why закрыт режимом сессии и памятью после лимита; ось «признак в project.md» не переоткрывалась.

## Gaps for design.md

Нет.

## Architectural alternatives

Нет равноправной развилки по коду или наблюдаемому поведению, которая требовала бы смены D1–D7. Альтернативы Q2 хуже по поставке kit или по Blast Radius таблицы ролей.

## Источники

- proposal.md — `## Why`; `## What Changes` п.1–4; `## Impact` (палитра: new, verify, apply, extend, explore, review, release-review)
- design.md — D1–D7; Behavior Contract; `## Implementation Options`; Slices S1/S2
- specs/session-api-mode/spec.md — Scenario «Ложное слово не включает режим», «Токен на дешёвой команде», «Команда без дорогих вызовов молчит», «Память после лимита», «Подсказка в палитре», «Разовый слаг и токен в одном сообщении»
- tasks.md — S1.1, S1.3, S1.4, S1.7, S1.9, S1.12, S1.13; S2.5, S2.6, S2.9
- Код (verified в этом прогоне) — не требовался: kit-метапроект, постановка ещё pre-apply
