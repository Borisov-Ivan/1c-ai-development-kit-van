# MXL round-trip (T1, без ИБ)

**Optional smoke** (не обязательная поставка). Фикстура: `temp/fixtures/mxl-roundtrip-sample.json` — создать локально при проверке (каталог `temp/fixtures/` в kit не поставляется).

```powershell
# только при artifact_mode assisted на прикладной ЗНИ
powershell.exe -NoProfile -File .cursor/skills/1c-mxl/compile/scripts/mxl-compile.ps1 `
  -JsonPath temp/fixtures/mxl-roundtrip-sample.json `
  -OutputPath temp/fixtures/mxl-roundtrip-out/Template.xml

powershell.exe -NoProfile -File .cursor/skills/1c-mxl/validate/scripts/mxl-validate.ps1 `
  -Path temp/fixtures/mxl-roundtrip-out/Template.xml
```

Требование: Windows PowerShell **5.1**. Оркестратор не использует сырой Write Template.xml.
