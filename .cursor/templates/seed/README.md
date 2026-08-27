# Заготовки поставки (seed)

Файлы, которые команды копируют в целевой проект при первичной настройке. Живут внутри `.cursor/`, чтобы поставка была самодостаточной: на ветке поставки каталога `openspec/` нет (см. `.cursor/docs/kit-template-workflow.md`).

| Заготовка | Куда попадает в проекте | Кто копирует |
|-----------|-------------------------|--------------|
| `knowledge/_taxonomy.template.yaml` | основа `openspec/knowledge/_taxonomy.yaml` | `/opsx:knowledge-init`, `/init-project` (Phase 5) |
| `changes/_template/` | `openspec/changes/_template/` | `/init-project` (Phase 0) |

Правки заготовок — здесь, в репозитории kit. В целевом проекте копии живут своей жизнью и при обновлении kit не перезаписываются.
