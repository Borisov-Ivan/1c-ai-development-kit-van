---
name: openspec-knowledge-audit
description: Audit OpenSpec Knowledge Base facts, TTL, anchors, indexes, metrics, and taxonomy sync.
---

# Skill: openspec-knowledge-audit

## Описание
Скилл для проведения аудита базы знаний (Knowledge Base) OpenSpec. Реализует команду `/opsx:knowledge-audit`.
Аудит проверяет актуальность фактов, сверяет якоря с кодом (read-repair), обновляет индекс, собирает метрики и проверяет синхронизацию таксономии с кодовой базой.

## Когда использовать
- Когда пользователь вызывает команду `/opsx:knowledge-audit`.
- Для ручной ревизии фактов, у которых истёк TTL или обнаружен drift (например, после `/opsx:explore`).
- Для пересборки индекса базы знаний (`--reindex`).
- Для анализа метрик использования базы знаний (`--metrics`).
- Для проверки синхронизации таксономии с диском (`--taxonomy-sync`).

## Флаги команды `/opsx:knowledge-audit`
По умолчанию (без флагов) команда выполняет full-revisit: проверяет anchors и заново оценивает Reuse Value Test для всех фактов в scope. Быстрая проверка только устаревших фактов доступна через явный `--overdue`.

*   `--domain <name>` — ограничить аудит конкретным доменом или субдоменом.
*   `--overdue` — проверять только факты с истёкшим TTL или со статусом `stale`.
*   `--status <s>` — фильтр фактов по конкретному статусу (`active`, `stale`, `deprecated`, `superseded`).
*   `--ids KB-NNNN,KB-MMMM` — ревизия конкретных фактов (например, из explore drift-accumulator).
*   `--action <action>` — прямое действие над фактами, указанными в `--ids` (`update`, `deprecate`, `supersede`, `delete --force-delete`).
*   `--no-reuse-test` — выполнить только verify/TTL без Reuse Value Test (для технической проверки anchors).
*   `--reindex` — пересобрать `openspec/knowledge/_index.yaml` на основе `.md` файлов (файлы — источник истины).
*   `--metrics` — показать отчёт по счётчикам (used-count, drift-history).
*   `--taxonomy-sync` — только отчёт: поиск несоответствий между `openspec/knowledge/_taxonomy.yaml` и структурой каталогов `src/*/cfe/*`.
*   `--from-archive <name>` — легализованный ретро-пилот: повторно применить протокол `openspec-archive-change` шаг 5.5 к уже **архивированной** ЗНИ (`openspec/changes/archive/<YYYY-MM-DD-name>/`). См. алгоритм 5. Не путать с `--reindex` (тот пересобирает индекс из существующих `.md`-файлов, а `--from-archive` создаёт новые KB из аналитических reports архивной ЗНИ).
*   `--structure-check` — отдельный режим: проверка whitelist содержимого `openspec/knowledge/` без верификации фактов. Структурная проверка также автоматически выполняется в начале основного аудита и в `--reindex` (см. шаг 0 алгоритма 1).

## Алгоритмы работы

### 1. Основной алгоритм аудита (без флагов или с фильтрами)
0.  **Structure check (perform always before main audit):** Прочитать содержимое `openspec/knowledge/` и сверить с whitelist из `knowledge-format.mdc` (раздел РАСПОЛОЖЕНИЕ).
    *   Разрешённые подкаталоги: `<domain>/` (по `_taxonomy.yaml`), `_archive/`.
    *   Разрешённые файлы в корне: `_index.yaml`, `_taxonomy.yaml`, `_taxonomy.template.yaml`, `README.md`.
    *   Любой иной файл/каталог → строка в Warnings отчёта: `Structure: <path> вне формата. Перенести в temp/reports/ или openspec/changes/<name>/reports/`.
    *   Не блокировать audit; продолжить шаги 1–7.
1.  **Чтение индекса:** Прочитать `openspec/knowledge/_index.yaml`.
2.  **Фильтрация:** Отфильтровать факты согласно переданным флагам (`--domain`, `--status`, `--overdue`, `--ids`).
    *   Без флагов scope = все факты из индекса (full-revisit).
    *   Если без флагов в KB > 50 фактов суммарно и не задан `--domain`, задать AskQuestion: `full` / `overdue-only` / `by-domain`. `full` продолжает полный аудит; `overdue-only` применяет фильтр `--overdue`; `by-domain` просит пользователя указать домен и завершает текущий ход без записи.
3.  **Верификация:** Для каждого отфильтрованного KB-файла выполнить алгоритм Verify (описан в `.cursor/rules/knowledge-format.mdc`).
3.5. **Reuse Value Re-evaluation:** Если не указан `--no-reuse-test`, для каждого отфильтрованного KB-файла применить `Reuse Value Test` из `.cursor/rules/knowledge-format.mdc`.
    *   Все 5 критериев = `да` → факт остаётся в рабочем состоянии.
    *   Любой критерий = `нет` или `не уверен` → добавить факт в секцию отчёта `## Reuse Value Warnings` с проваленными критериями (`RVT-1`..`RVT-5`), кратким обоснованием и рекомендацией `deprecate` / `merge` / `keep with justification`.
    *   Reuse-failed **не переводится автоматически** в `deprecated` и не удаляется. Это read-only оценка ценности; решение требует ручного действия или явного `--action`.
4.  **Auto-actions (без вопросов к пользователю):**
    *   Если статус верификации `verified` → выполнить silent auto-refresh поля `verified-at` в KB-файле и индексе (батчем, без AskQuestion).
    *   Если обнаружен drift (`signature-drift`, `path-drift`, `anchor-missing`, `count-drift`) → изменить статус KB на `stale`, добавить факт в секцию Warnings отчёта.
5.  **Единый AskQuestion по итогам:**
    *   Если хотя бы один KB перешёл в статус `stale` или попал в `Reuse Value Warnings`, задать **один вопрос на всю сессию**: «Открыть отчёт для ручной ревизии stale + reuse-failed? [yes | no]».
    *   `yes` → открыть сгенерированный отчёт `openspec/reports/knowledge-audit-<date>.md` с построчным списком `stale` фактов, `Reuse Value Warnings` и рекомендациями (`update` / `deprecate` / `supersede` / `delete --force-delete` / `keep with justification`).
    *   `no` → оставить KB в текущем состоянии; `stale` остаются stale, reuse-failed остаются active/stale до явного решения пользователя.
6.  **Прямые действия:** Сам audit-скилл **без явного флага `--action` ничего деструктивного не пишет**. Прямые действия над KB пользователь делает вручную (правкой KB-файла) или запуском `/opsx:knowledge-audit --ids KB-NNNN --action <action>`.
7.  **Отчёт:** Сгенерировать `openspec/reports/knowledge-audit-<date>.md` (статистика verified/refreshed/stale + `Reuse Value Warnings` + рекомендации).

### 2. Алгоритм `--reindex`
1.  Найти все `.md` файлы фактов в `openspec/knowledge/` (исключая `_archive/`).
2.  Считать метаданные из каждого файла.
3.  Сформировать новый `openspec/knowledge/_index.yaml`.
4.  Атомарно перезаписать индексный файл.
5.  Вывести сообщение об успешной пересборке индекса и количестве проиндексированных фактов.

### 3. Алгоритм `--metrics`
1.  Считать `openspec/knowledge/_index.yaml` и все KB-файлы (для полных данных).
2.  Сформировать и вывести отчёт:
    *   **Топ-10 used facts:** Факты с наибольшим `used-count` (кандидаты на повышение TTL до 180 дней).
    *   **Мёртвые факты:** Факты с `used-count: 0` за последние 180 дней (кандидаты на перевод в `deprecated`).
    *   **Кандидаты на немедленный deprecate:** Пересечение «мёртвых» фактов с Reuse Value-failed. Эти факты сначала показывать в отчёте, потому что они одновременно не используются и не проходят текущий критерий ценности.
    *   **Перенаселённые домены:** Домены, в которых > 50 фактов (вывести warning по бюджету, порекомендовать консолидацию или перевод в `_archive/`).
    *   **Калибровка TTL:** Сравнение среднего TTL с `drift-detected-count` (если drift часто происходит при TTL 90, порекомендовать уменьшить до 60).

### 4. Алгоритм `--taxonomy-sync`
1.  Считать `openspec/knowledge/_taxonomy.yaml`.
2.  Просканировать структуру каталогов `src/*/cfe/*`.
3.  Найти несоответствия:
    *   **orphan directory:** Каталог расширения есть на диске, но записи домена в YAML нет.
    *   **orphan domain:** В YAML объявлен `source`, но соответствующего каталога не существует.
4.  **Режим report only:** Автоматически YAML не править!
5.  Вывести отчёт о найденных несоответствиях. Если найдены расхождения, **обязательно порекомендовать** запуск `/opsx:knowledge-init` для согласованного diff и записи.

### 5. Алгоритм `--from-archive <name>` (ретро-пилот)

Цель: легализованно применить протокол archive шаг 5.5 к **уже архивированной** ЗНИ. Повторно использует тот же extraction pipeline и единый AskQuestion с per-candidate карточками.

1.  **Resolve archive path:**
    *   Если `<name>` уже содержит дату (`YYYY-MM-DD-<slug>`), искать `openspec/changes/archive/<name>/`.
    *   Иначе — найти каталог с суффиксом `-<name>` среди `openspec/changes/archive/*/`. При нескольких совпадениях — взять самый свежий (по дате в префиксе) и сообщить выбор.
    *   Если не найден — вернуть ошибку: «Archive `<name>` не найден в `openspec/changes/archive/`».
2.  **Preflight (taxonomy):** если `openspec/knowledge/_taxonomy.yaml` отсутствует — STOP, сообщить пользователю команду `/opsx:knowledge-init`. Это не auto-yes контекст, аудит подразумевает наличие таксономии.
3.  **Inputs:** искать в `<archive-path>/reports/` файлы по маскам `exploration-*.md`, `trace-analysis-*.md`, `resolved-contract-*.md`. Если ни один не найден — вернуть отчёт `No analytical reports in archive <name>` и завершить.
4.  **Apply archive шаг 5.5 Path C** дословно (см. `openspec-archive-change/SKILL.md`):
    *   Подготовить ≤5 KB-кандидатов с полностью готовыми полями (domain, subdomain, anchors, tentative TTL).
    *   Для каждого: автоподбор domain/subdomain по `_taxonomy.yaml`, извлечение anchors, verify по текущему `src/`, dedup относительно `_index.yaml`, Reuse Value Test, `reuse-scenario`, `why-knowledge`, `source.report:lines`.
    *   `source.report` указывает на путь внутри архива (`openspec/changes/archive/<YYYY-MM-DD-name>/reports/...`).
5.  **Если кандидатов нет** — вернуть отчёт с указанием причины (taxonomy mismatch / verify drift / dedup / deferred reuse value) для каждого отбракованного кандидата, без AskQuestion. State = `No candidates after filters` или `Deferred N — reuse value not justified`, если все кандидаты отброшены только Reuse Value Test.
6.  **Если есть кандидаты** — вывести их per-candidate карточками (формат идентичен archive 5.5 Path C) и **один AskQuestion** на весь батч: «Сохранить N извлечённых KB-фактов из архива `<name>`? [yes | no]».
7.  **Save:**
    *   `yes` → сгенерировать `KB-NNNN-slug.md` в соответствующих доменах + атомарно перезаписать `_index.yaml`. State = `Saved N`.
    *   `no` → ничего не пишется. State = `Declined by user`.
8.  **Отчёт:** `openspec/reports/knowledge-audit-from-archive-<archive-slug>-<date>.md` с полным списком кандидатов, причинами отбраковки, итоговым state, structure check warnings (из шага 0 алгоритма 1).
9.  **Ограничение:** одна `--from-archive` сессия = одна ЗНИ. Массовая ретро-миграция запрещена политикой `knowledge-format.mdc` («Ретроактивная миграция НЕ делается»).

## Правила и ограничения
- **Writer contract:** Скилл аудита имеет право обновлять KB-файлы и `_index.yaml`.
- **Удаление:** Запрещено удалять факты без явного флага `--force-delete` (вместе с `--action delete`). Рекомендуется переводить устаревшие факты в статус `deprecated`, после чего (если возраст > 6 мес) они будут автоматически перенесены в `_archive/` при следующем аудите.
- **Деструктивные действия:** Любые действия, изменяющие суть факта или удаляющие его, требуют либо ручной правки пользователем, либо явного указания `--action`. Auto-actions применяются только для обновления `verified-at` и перевода в `stale`.
- **Reuse Value Test:** Это read-only оценка ценности факта. Audit может рекомендовать `deprecate`, `merge` или `keep with justification`, но не переводит reuse-failed факты в `deprecated` автоматически.
