## REMOVED Requirements

### Requirement: Map designer does not full-read the canvas skill

**Reason:** Роль сборщика манифеста карты удаляется вместе с картой сценария. Оркестратор сам заполняет тонкий шаблон панели.
**Migration:** `visual-explanation` — данные панели собирает родитель сессии; отдельный агент-картограф не вызывается.
