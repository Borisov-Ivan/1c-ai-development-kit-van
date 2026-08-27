# Публикация поставки kit из текущей ветки разработки на ветку поставки.
# Манифест: .cursor/** + AGENTS.md + витринный README.md (из tools/dist-readme.md).
# Ветки не сливаются, push --force не используется.
#
# Использование:
#   powershell -File tools\publish-dist.ps1 -DryRun
#   powershell -File tools\publish-dist.ps1
#   powershell -File tools\publish-dist.ps1 -Tag v1.2.0
#
# Требования: git в PATH, tar (входит в Windows 10 и выше). PowerShell 5.1.

[CmdletBinding()]
param(
  [switch]$DryRun,
  [string]$Tag = "",
  [string]$DistBranch = "main",
  [string]$Remote = "origin"
)

$ErrorActionPreference = 'Stop'

function Fail($message) { Write-Error $message; exit 1 }
function Git { & git @args; if ($LASTEXITCODE -ne 0) { Fail "git $($args -join ' ') завершился с кодом $LASTEXITCODE" } }

Set-Location (& git rev-parse --show-toplevel)

# --- Kit-only guard -----------------------------------------------------------
if (-not (Test-Path '.cursor/docs/kit-template-workflow.md')) { Fail 'Это не репозиторий kit: нет .cursor/docs/kit-template-workflow.md' }
if (-not (Test-Path 'tools/dist-readme.md')) { Fail 'Нет шаблона витрины tools/dist-readme.md' }
if (Test-Path 'openspec/project.md') { Fail 'Похоже на проект 1С (есть openspec/project.md) — публикация отменена' }
if (Get-ChildItem -Path 'src' -Filter 'Configuration.xml' -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match '[\\/]cf[\\/]' }) {
  Fail 'Похоже на проект 1С (есть выгрузка src/*/cf) — публикация отменена'
}

# --- Состояние ----------------------------------------------------------------
# Публикуем только чистое дерево. В режиме проверки грязное дерево допустимо:
# состав считается по закоммиченному HEAD, ничего не отправляется.
if (& git status --porcelain) {
  if ($DryRun) { Write-Host 'Внимание: есть незакоммиченные правки — состав считается по закоммиченному HEAD.' }
  else { Fail 'Дерево не чистое — закоммитьте или спрячьте правки перед публикацией' }
}

$sourceBranch = (& git rev-parse --abbrev-ref HEAD).Trim()
$sourceSha    = (& git rev-parse HEAD).Trim()
$sourceSha7   = (& git rev-parse --short=7 HEAD).Trim()
$repoUrl      = ((& git remote get-url $Remote) -replace 'https://[^@]*@', 'https://').Trim()
$date         = Get-Date -Format 'yyyy-MM-dd'

# --- Состав поставки ----------------------------------------------------------
$distFiles   = & git -c core.quotepath=false ls-tree -r --name-only HEAD -- .cursor AGENTS.md
$cursorCount = ($distFiles | Where-Object { $_ -like '.cursor/*' }).Count
if ($distFiles -notcontains 'AGENTS.md') { Fail 'AGENTS.md отсутствует в дереве' }

Write-Host "Состав поставки с $sourceBranch ($sourceSha7):"
Write-Host "  .cursor/**  — $cursorCount файлов"
Write-Host "  AGENTS.md   — да"
Write-Host "  README.md   — из tools/dist-readme.md"
Write-Host "  не входят: openspec/, doc/, tools/, temp/"

if ($DryRun) {
  Write-Host 'Режим проверки: изменений в удалённом репозитории нет.'
  exit 0
}

# --- Рабочее дерево ветки поставки -------------------------------------------
Git fetch $Remote $DistBranch

$wt = Join-Path ([System.IO.Path]::GetTempPath()) ("kit-dist-" + [System.Guid]::NewGuid().ToString('N').Substring(0, 8))
try {
  Git worktree add --detach $wt "$Remote/$DistBranch"

  # Полная замена дерева манифестом: старое содержимое убираем, кроме служебного .git
  Get-ChildItem -LiteralPath $wt -Force | Where-Object { $_.Name -ne '.git' } | Remove-Item -Recurse -Force

  $tar = Join-Path ([System.IO.Path]::GetTempPath()) ("kit-dist-" + [System.Guid]::NewGuid().ToString('N').Substring(0, 8) + '.tar')
  Git archive --format=tar --output=$tar HEAD -- .cursor AGENTS.md
  & tar -xf $tar -C $wt
  if ($LASTEXITCODE -ne 0) { Fail 'Не удалось распаковать архив поставки (нужен tar)' }
  Remove-Item -LiteralPath $tar -Force

  (Get-Content -LiteralPath 'tools/dist-readme.md' -Raw).
    Replace('{{DATE}}', $date).
    Replace('{{SOURCE_SHA}}', $sourceSha7).
    Replace('{{SOURCE_BRANCH}}', $sourceBranch).
    Replace('{{REPO_URL}}', $repoUrl) |
    Set-Content -LiteralPath (Join-Path $wt 'README.md') -Encoding UTF8

  # --- Коммит и отправка ------------------------------------------------------
  Git -C $wt add -A
  & git -C $wt diff --cached --quiet
  if ($LASTEXITCODE -eq 0) {
    Write-Host "Поставка уже совпадает с $Remote/$DistBranch — публиковать нечего."
    exit 0
  }

  Git -C $wt commit -q -m "release: поставка $date ($sourceBranch $sourceSha7)" -m "Source-Commit: $sourceSha"
  Git -C $wt push $Remote "HEAD:$DistBranch"

  $distSha7 = (& git -C $wt rev-parse --short=7 HEAD).Trim()
  Write-Host "Опубликовано: $Remote/$DistBranch $distSha7 <- $sourceBranch $sourceSha7"

  if ($Tag) {
    Git -C $wt tag $Tag
    Git -C $wt push $Remote $Tag
    Write-Host "Тег: $Tag"
  }
}
finally {
  & git worktree remove --force $wt 2>$null | Out-Null
  if (Test-Path -LiteralPath $wt) { Remove-Item -LiteralPath $wt -Recurse -Force -ErrorAction SilentlyContinue }
}

# --- Проверка после публикации ------------------------------------------------
Git fetch $Remote $DistBranch
$unexpected = & git ls-tree --name-only "$Remote/$DistBranch" | Where-Object { $_ -notin @('.cursor', 'AGENTS.md', 'README.md') }
if ($unexpected) {
  Write-Host 'ВНИМАНИЕ: в ветке поставки лишние пути:'
  $unexpected | ForEach-Object { Write-Host "  $_" }
  exit 1
}
Write-Host 'Проверка состава пройдена.'
