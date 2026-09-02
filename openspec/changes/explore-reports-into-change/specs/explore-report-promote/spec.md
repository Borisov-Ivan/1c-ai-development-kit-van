## ADDED Requirements

### Requirement: Reports of this topic move into the change catalog

После `/opsx:explore` с сохранённым отчётом и последующего `/opsx:new` по той же теме система MUST перенести отчёты этой темы (обследование, разбор трассы, архитектурный разбор, журнал пошагового разбора) в каталог ЗНИ. После успешного переезда тех же файлов в `temp` MUST NOT оставаться.

#### Scenario: Reports of this topic move into the change catalog

- **WHEN** в чате есть превью отчёта обследования и создают ЗНИ по этой теме
- **THEN** файл с тем же именем лежит в `reports/` каталога ЗНИ, а в `temp/reports/` этого файла нет

#### Scenario: Confirm message has no file list

- **WHEN** создание ЗНИ завершилось и отчёты темы были перенесены
- **THEN** в чате есть эффект «материалы разбора в задаче» и нет перечня перенесённых путей

#### Scenario: Handoff file moves only if it exists

- **WHEN** пользователь словами просил сохранить постановку в файл и затем создают ЗНИ по этой теме
- **THEN** этот файл тоже лежит в `reports/` каталога ЗНИ
- **AND** если пользователь не просил сохранить — ЗНИ создаётся без этого файла, отчёты обследования всё равно переезжают

### Requirement: New without research reports succeeds

Если исследования с отчётом не было, создание ЗНИ MUST пройти без ошибки и без требования приложить отчёт.

#### Scenario: New without research reports succeeds

- **WHEN** создают ЗНИ только по блоку постановки в чате, отчётов обследования не было
- **THEN** ЗНИ создана, нет сообщения «приложите отчёт» и нет остановки из‑за пустого `temp`

### Requirement: Parallel topics do not mix

При нескольких отчётах разных тем в `temp` система MUST переносить в новую ЗНИ только файлы этой темы.

#### Scenario: Parallel topics do not mix

- **WHEN** в `temp` лежат отчёты двух разных тем и создают ЗНИ по второй теме
- **THEN** в каталоге новой ЗНИ только файлы второй темы; файлы первой остаются в `temp`

### Requirement: Extend from temp moves the file

Если ЗНИ уже есть и дополнение идёт из отчёта, который ещё в `temp`, система MUST перенести файл в каталог этой ЗНИ и дальше ссылаться на новый путь.

#### Scenario: Extend from temp moves the file

- **WHEN** дополняют существующую ЗНИ из `temp/reports/exploration-….md`
- **THEN** файл лежит в `reports/` этой ЗНИ, а новые ссылки в постановке не указывают на `temp/reports/` для этого файла

### Requirement: Continuity finds reports after move

Поиск «продолжи вчерашний разбор» MUST находить отчёты темы в каталогах ЗНИ за последние 7 дней, не требуя живой копии в `temp`.

#### Scenario: Continuity finds reports after move

- **WHEN** в новом чате просят продолжить разбор темы уже созданной ЗНИ (с именем или без)
- **THEN** находятся следы в `openspec/changes/<name>/reports/` за 7 дней, без требования, чтобы тот же файл ещё лежал в `temp`
