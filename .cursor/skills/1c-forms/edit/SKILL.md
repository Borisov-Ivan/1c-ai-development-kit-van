---
name: 1c-forms-edit
description: "Edit existing Form.xml via JSON patch. Only when artifact_mode is assisted. No form-add/ChildObjects."
---

# 1c-forms/edit

Точечная правка **существующего** `Form.xml` по JSON. Только при `artifact_mode: assisted`.

## Hard rules

- Цель — существующий файл формы; не создавать форму/объект; не трогать ChildObjects метаданных объекта.
- После edit → `1c-forms/validate`.
- PowerShell 5.1 only.

## Command

```powershell
powershell.exe -NoProfile -File .cursor/skills/1c-forms/edit/scripts/form-edit.ps1 -FormPath "<path>/Ext/Form.xml" -JsonPath "<patch>.json"
```

## Workflow

1. Mode Gate = `assisted`.
2. info (опционально) → Write patch JSON → edit → validate.
