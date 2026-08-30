# Заготовки поставки (seed)

Файлы, которые команды копируют в целевой проект при первичной настройке. Живут внутри `.cursor/`, чтобы копирования `.cursor/` + `AGENTS.md` хватало для `/init-project`. Каталог `openspec/` репозитория kit (specs/ADR эволюции шаблона) в проект не копируют.

| Заготовка | Куда попадает в проекте | Кто копирует |
|-----------|-------------------------|--------------|
| `knowledge/_taxonomy.template.yaml` | основа `openspec/knowledge/_taxonomy.yaml` | `/opsx:knowledge-init`, `/init-project` (Phase 5) |
| `changes/_template/` | `openspec/changes/_template/` | `/init-project` (Phase 0) |

Правки заготовок — здесь, в репозитории kit. В целевом проекте копии живут своей жизнью и при обновлении kit не перезаписываются.
