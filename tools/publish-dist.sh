#!/usr/bin/env bash
# Публикация поставки kit из текущей ветки разработки на ветку поставки.
# Манифест: .cursor/** + AGENTS.md + витринный README.md (из tools/dist-readme.md).
# Ветки не сливаются, push --force не используется.
#
# Использование:
#   tools/publish-dist.sh --dry-run          состав поставки, без изменений
#   tools/publish-dist.sh                    публикация в origin/<ветка поставки>
#   tools/publish-dist.sh --tag v1.2.0       публикация + тег на коммит поставки
#   tools/publish-dist.sh --dist-branch main имя ветки поставки (по умолчанию main)

set -euo pipefail

DRY_RUN=0
TAG=""
DIST_BRANCH="main"
REMOTE="origin"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --tag) TAG="${2:?--tag требует значение}"; shift 2 ;;
    --dist-branch) DIST_BRANCH="${2:?--dist-branch требует значение}"; shift 2 ;;
    --remote) REMOTE="${2:?--remote требует значение}"; shift 2 ;;
    *) echo "Неизвестный ключ: $1" >&2; exit 2 ;;
  esac
done

cd "$(git rev-parse --show-toplevel)"

# --- Kit-only guard -----------------------------------------------------------
[[ -f .cursor/docs/kit-template-workflow.md ]] || { echo "Это не репозиторий kit: нет .cursor/docs/kit-template-workflow.md" >&2; exit 1; }
[[ -f tools/dist-readme.md ]] || { echo "Нет шаблона витрины tools/dist-readme.md" >&2; exit 1; }
[[ -e openspec/project.md ]] && { echo "Похоже на проект 1С (есть openspec/project.md) — публикация отменена" >&2; exit 1; }
if compgen -G "src/*/cf/Configuration.xml" > /dev/null; then
  echo "Похоже на проект 1С (есть выгрузка src/*/cf) — публикация отменена" >&2; exit 1
fi

# --- Состояние ----------------------------------------------------------------
# Публикуем только чистое дерево. В режиме проверки грязное дерево допустимо:
# состав считается по закоммиченному HEAD, ничего не отправляется.
if [[ -n "$(git status --porcelain)" ]]; then
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "Внимание: есть незакоммиченные правки — состав считается по закоммиченному HEAD."
  else
    echo "Дерево не чистое — закоммитьте или спрячьте правки перед публикацией" >&2; exit 1
  fi
fi

SOURCE_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
SOURCE_SHA="$(git rev-parse HEAD)"
SOURCE_SHA7="$(git rev-parse --short=7 HEAD)"
REPO_URL="$(git remote get-url "$REMOTE" 2>/dev/null | sed -E 's#https://[^@]*@#https://#')"
DATE="$(date +%Y-%m-%d)"

# --- Состав поставки ----------------------------------------------------------
mapfile -t DIST_FILES < <(git -c core.quotepath=false ls-tree -r --name-only HEAD -- .cursor AGENTS.md | sort)

# Считаем без конвейеров: под pipefail ранний выход grep гасит printf сигналом
# и превращает исправную проверку в ложную ошибку.
CURSOR_COUNT=0
AGENTS_PRESENT=0
for f in "${DIST_FILES[@]}"; do
  case "$f" in
    .cursor/*) CURSOR_COUNT=$((CURSOR_COUNT + 1)) ;;
    AGENTS.md) AGENTS_PRESENT=1 ;;
  esac
done

echo "Состав поставки с ${SOURCE_BRANCH} (${SOURCE_SHA7}):"
echo "  .cursor/**  — ${CURSOR_COUNT} файлов"
if [[ "$AGENTS_PRESENT" == "1" ]]; then
  echo "  AGENTS.md   — да"
else
  echo "AGENTS.md отсутствует в дереве" >&2; exit 1
fi
echo "  README.md   — из tools/dist-readme.md"
echo "  не входят: openspec/, doc/, tools/, temp/"

if [[ "$DRY_RUN" == "1" ]]; then
  echo "Режим проверки: изменений в удалённом репозитории нет."
  exit 0
fi

# --- Рабочее дерево ветки поставки -------------------------------------------
git fetch "$REMOTE" "$DIST_BRANCH"
WT="$(mktemp -d)"
cleanup() { git worktree remove --force "$WT" >/dev/null 2>&1 || true; rm -rf "$WT"; }
trap cleanup EXIT

git worktree add --detach "$WT" "${REMOTE}/${DIST_BRANCH}" >/dev/null

# Полная замена дерева манифестом: старое содержимое убираем, кроме служебного .git
find "$WT" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

TAR="$(mktemp)"
git archive --format=tar --output="$TAR" HEAD -- .cursor AGENTS.md
tar -xf "$TAR" -C "$WT"
rm -f "$TAR"

sed -e "s|{{DATE}}|${DATE}|g" \
    -e "s|{{SOURCE_SHA}}|${SOURCE_SHA7}|g" \
    -e "s|{{SOURCE_BRANCH}}|${SOURCE_BRANCH}|g" \
    -e "s|{{REPO_URL}}|${REPO_URL}|g" \
    tools/dist-readme.md > "$WT/README.md"

# --- Коммит и отправка --------------------------------------------------------
git -C "$WT" add -A
if git -C "$WT" diff --cached --quiet; then
  echo "Поставка уже совпадает с ${REMOTE}/${DIST_BRANCH} — публиковать нечего."
  exit 0
fi

git -C "$WT" commit -q -m "release: поставка ${DATE} (${SOURCE_BRANCH} ${SOURCE_SHA7})" -m "Source-Commit: ${SOURCE_SHA}"
git -C "$WT" push "$REMOTE" "HEAD:${DIST_BRANCH}"

DIST_SHA7="$(git -C "$WT" rev-parse --short=7 HEAD)"
echo "Опубликовано: ${REMOTE}/${DIST_BRANCH} ${DIST_SHA7} ← ${SOURCE_BRANCH} ${SOURCE_SHA7}"

if [[ -n "$TAG" ]]; then
  git -C "$WT" tag "$TAG"
  git -C "$WT" push "$REMOTE" "$TAG"
  echo "Тег: ${TAG}"
fi

# --- Проверка после публикации ------------------------------------------------
git fetch "$REMOTE" "$DIST_BRANCH" >/dev/null
UNEXPECTED="$(git ls-tree --name-only "${REMOTE}/${DIST_BRANCH}" | grep -vx -e '.cursor' -e 'AGENTS.md' -e 'README.md' || true)"
if [[ -n "$UNEXPECTED" ]]; then
  echo "ВНИМАНИЕ: в ветке поставки лишние пути:" >&2
  echo "$UNEXPECTED" >&2
  exit 1
fi
echo "Проверка состава пройдена."
