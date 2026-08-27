# Установка kit в проект 1С

Как поставить и обновлять kit в проекте. Документ для того, кто **пользуется** kit. Как публиковать поставку — [kit-template-workflow.md](./kit-template-workflow.md).

## Зачем модуль

При ручном копировании папок в git проекта остаётся снимок файлов, но нет записи, **какая версия** kit стоит. На нескольких проектах версии расходятся молча. Модуль git фиксирует точный коммит поставки в истории проекта: обновление становится осознанным шагом, а не «кажется, я копировал в прошлом месяце».

## Раскладка

```text
проект/
  vendor/kit-van/        модуль git на ветку main (поставка)
  .cursor/               копия vendor/kit-van/.cursor — делает скрипт
  AGENTS.md              копия vendor/kit-van/AGENTS.md
  kit-local/             необязательно: ваши локальные файлы поверх копии
  tools/sync-kit.cmd     скрипт синхронизации (живёт в проекте)
  openspec/              своё: project.md, ЗНИ, база знаний
  src/                   своя выгрузка 1С
```

Модуль лежит в `vendor/kit-van`, а не в `.cursor`: `.cursor` — рабочий каталог Cursor, туда попадает **копия**. Так локальные файлы и настройки не превращают модуль в «грязный», а сам `.cursor` остаётся обычной папкой проекта.

## Установка (один раз в проекте)

Windows, из корня проекта. Если `.cursor` уже лежал копией в git — сначала снять его с учёта.

```bat
git rm -r --cached .cursor
git submodule add -b main https://github.com/Borisov-Ivan/1c-ai-development-kit-van.git vendor/kit-van
tools\sync-kit.cmd
git add .gitmodules vendor/kit-van AGENTS.md
git commit -m "chore: подключить kit-van модулем"
```

После — **Reload Window** в Cursor. Команды `/opsx:*` должны появиться.

## Скрипт синхронизации

Положите в проект `tools\sync-kit.cmd`. Он не тянет обновление сам: сначала вы решаете, какую версию брать.

```bat
@echo off
setlocal
cd /d "%~dp0.."

git submodule update --init vendor/kit-van || goto :err

robocopy "vendor\kit-van\.cursor" ".cursor" /MIR /NFL /NDL /NJH /NJS /XF KIT_VERSION
if errorlevel 8 goto :err

if exist "kit-local" robocopy "kit-local" ".cursor" /E /NFL /NDL /NJH /NJS

copy /Y "vendor\kit-van\AGENTS.md" "AGENTS.md" >nul

for /f %%i in ('git -C vendor\kit-van rev-parse HEAD') do set KITSHA=%%i
> ".cursor\KIT_VERSION" echo %KITSHA% %DATE%

echo kit синхронизирован: %KITSHA%
exit /b 0

:err
echo ОШИБКА синхронизации kit
exit /b 1
```

Что делает: обновляет рабочую копию модуля, зеркалит `.cursor` из поставки, накладывает `kit-local\`, обновляет `AGENTS.md`, записывает версию в `.cursor\KIT_VERSION`.

`robocopy /MIR` **удаляет** в `.cursor` то, чего нет в поставке. Поэтому свои файлы держите в `kit-local\`, а не внутри `.cursor`.

## Обновление kit

После того как в репозитории kit опубликована новая поставка:

```bat
git submodule update --remote vendor/kit-van
tools\sync-kit.cmd
git add vendor/kit-van AGENTS.md
git commit -m "chore: обновить kit-van"
```

Reload Window. Какая версия стоит сейчас — `git submodule status` или `.cursor\KIT_VERSION`.

Для нескольких проектов удобно пройти списком:

```powershell
$repos = @('C:\GitHub\ПроектА', 'C:\GitHub\ПроектБ')
foreach ($r in $repos) {
  Set-Location $r
  git submodule update --remote vendor/kit-van
  & "$r\tools\sync-kit.cmd"
  git add vendor/kit-van AGENTS.md
  if (git diff --cached --quiet) { Write-Host "без изменений: $r" }
  else { git commit -m "chore: обновить kit-van"; git push }
}
```

## Клон проекта на другой машине

```bat
git clone --recurse-submodules <url-проекта>
cd <проект>
tools\sync-kit.cmd
```

Если клонировали без модулей — `git submodule update --init --recursive`, затем `tools\sync-kit.cmd`.

## Два решения по умолчанию

**`.cursor/` не коммитим.** Это генерируемая копия; версия закреплена ссылкой на коммит модуля и продублирована в `KIT_VERSION`. В `.gitignore` проекта:

```gitignore
/.cursor/
```

Альтернатива — коммитить `.cursor`: после клона правила на месте без запуска скрипта, зато каждое обновление даёт крупный diff. Выбирайте одно и держитесь его в рамках проекта.

**Локальные правила — только в `kit-local/`.** Структура повторяет `.cursor`: например `kit-local\rules\project-local.mdc` окажется в `.cursor\rules\project-local.mdc`. Прямые правки внутри `.cursor` затрёт следующая синхронизация.

## Запасной путь: без модуля

Если модули в проекте нежелательны — один клон ветки поставки и ручное копирование:

```bat
git clone -b main --depth 1 https://github.com/Borisov-Ivan/1c-ai-development-kit-van.git C:\GitHub\_kit-dist
robocopy C:\GitHub\_kit-dist\.cursor <проект>\.cursor /MIR
copy /Y C:\GitHub\_kit-dist\AGENTS.md <проект>\AGENTS.md
```

Обновление — `git pull` в `_kit-dist` и повтор копирования. Минус: версия kit в проекте нигде не зафиксирована.

## Что ломается и почему

| Симптом | Причина | Что сделать |
|---------|---------|-------------|
| В Cursor нет `/opsx:*` | `.cursor` пуст: не запускали синхронизацию | `tools\sync-kit.cmd`, затем Reload Window |
| Правки правил исчезли | правили внутри `.cursor`, прошла синхронизация | перенести в `kit-local\` |
| «Грязный» модуль в `git status` | правили файлы внутри `vendor\kit-van` | `git -C vendor\kit-van checkout -- .` |
| У коллеги пустой `vendor\kit-van` | клон без модулей | `git submodule update --init --recursive` |
| Нет доступа к модулю | приватный репозиторий kit | выдать права на чтение репозитория kit |
| `openspec/project.md` пропал | попал под зеркалирование | `project.md` живёт в `openspec/`, синхронизация его не трогает; восстановить из git проекта |

## Связь

- Первый сценарий после установки: [quick-start.md](./quick-start.md)
- Частые вопросы: [faq-kit.md](./faq-kit.md)
- Первичная настройка проекта: `/init-project` (протокол — [init-project-protocol.md](./init-project-protocol.md))
