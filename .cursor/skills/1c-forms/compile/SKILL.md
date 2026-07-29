---
name: 1c-forms-compile
description: "Compile Form.xml from JSON DSL. Only when proposal artifact_mode is assisted. No -FromObject, no form-add/ChildObjects."
---

# 1c-forms/compile

Сборка **существующего** пути `Form.xml` из JSON DSL. Только при `artifact_mode: assisted`.

## Hard rules (kit-van v1)

- **Разрешено:** `-JsonPath` + `-OutputPath` → запись `.../Forms/<Имя>/Ext/Form.xml` для **уже существующей** формы в метаданных.
- **Запрещено:** `-FromObject`, borrow, form-add, правка `ChildObjects` объекта, создание нового объекта метаданных.
- Сырой Write Form.xml оркестратором **вне** этого скрипта — запрещён.
- После compile → `1c-forms/validate`.
- PowerShell **5.1** only (Windows встроенный).

## Command

```powershell
powershell.exe -NoProfile -File .cursor/skills/1c-forms/compile/scripts/form-compile.ps1 -JsonPath "<dsl>.json" -OutputPath "<path>/Ext/Form.xml"
```

Опционально: `-Preset erp-standard` (см. `presets/`).

## Workflow

1. Проверить Mode Gate = `assisted`.
2. Убедиться, что форма уже есть в объекте (Конфигуратор) — иначе HALT → manual / человек.
3. Write JSON DSL → run compile → validate.
4. Не вызывать `-FromObject`.
