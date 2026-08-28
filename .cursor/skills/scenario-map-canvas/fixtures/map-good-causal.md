# Эталон «хорошо»: слои и подписанные связи

Предметный сюжет в эталоне допустим. В предикатах скилла и шаблонах предложения таких имён нет.

Сверка живой панели — по схеме ниже, не по списку шагов.

```yaml
header:
  question: "Почему после смены формата штампа недостаточно удалить только готовую визуализацию документа?"
  insight: "Кэш картинки живёт отдельно от кэша копии: пока PNG не снят, новая копия снова получает старый формат."
  sources:
    - "temp/reports/exploration-example-vizualizaciya-shtampa.md"
  view_primary: "causal-flow"

nodes:
  - id: "signed-original"
    name: "Подписанный оригинал файла"
    kind: "protected-original"
    layer: "Оригинал"
    state: "valid"
    effect: "Исходный файл с электронной подписью. Штамп в него никогда не пишется — визуализация всегда отдельная копия."
    evidence:
      path: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl"
      start: 3848
      end: 3864

  - id: "cache-stamp-png"
    name: "Картинка штампа"
    kind: "cache"
    layer: "Слой 1 — картинка"
    state: "stale"
    effect: "PNG штампа, нарисованная из макета. Пока файл существует, картинка считается актуальной — признака версии формата в коде нет."
    evidence:
      path: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl"
      start: 9540
      end: 9565

  - id: "overlay"
    name: "Наложение по формату"
    kind: "transform"
    layer: "Слой 2 — копия"
    effect: "Картинка накладывается на копию исходного файла. Разные форматы идут разными техническими путями, но оба читают ту же PNG."
    evidence:
      path: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl"
      start: 3831
      end: 3936

  - id: "cache-visual-copy"
    name: "Копия со штампом"
    kind: "cache"
    layer: "Слой 2 — копия"
    state: "cleared"
    effect: "Служебная копия документа со штампом. Именно её отдают при открытии. Удалили только её — механизм соберёт копию заново."
    evidence:
      path: "src/Example/cf/InformationRegisters/СлужебныеФайлыДокументов/Ext/ManagerModule.bsl"
      start: 43
      end: 73

  - id: "user-sees"
    name: "Пользователь открывает файл со штампом"
    kind: "user-result"
    layer: "Результат"
    effect: "При открытии подменяются двоичные данные: пользователь видит копию со штампом, оригинал остаётся нетронутым."
    evidence:
      path: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl"
      start: 3437
      end: 3441

  - id: "invalidate-on-sign"
    name: "Запись подписей сбрасывает копию"
    kind: "invalidation"
    layer: "События"
    effect: "При изменении состава подписей копия удаляется всегда. Смена макета таким событием не является."
    evidence:
      path: "src/Example/cf/CommonModules/РаботаСЭП/Ext/Module.bsl"
      start: 1445
      end: 1476

edges:
  - from: "signed-original"
    to: "overlay"
    relation: "reads"
    label: "копия делается из оригинала, подпись не портится"
    evidence_ref: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl:3831-3936"
  - from: "cache-stamp-png"
    to: "overlay"
    relation: "feeds"
    label: "берётся уже готовая PNG"
    evidence_ref: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl:9540-9565"
  - from: "overlay"
    to: "cache-visual-copy"
    relation: "writes"
    label: "результат сохраняется как служебный файл"
    evidence_ref: "src/Example/cf/InformationRegisters/СлужебныеФайлыДокументов/Ext/ManagerModule.bsl:43-73"
  - from: "cache-visual-copy"
    to: "user-sees"
    relation: "feeds"
    label: "подмена данных при открытии"
    evidence_ref: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl:3437-3441"
  - from: "cache-visual-copy"
    to: "overlay"
    relation: "reuses"
    label: "копии нет → сборка повторяется со старой картинкой"
    evidence_ref: "temp/reports/exploration-example-vizualizaciya-shtampa.md"
  - from: "invalidate-on-sign"
    to: "cache-visual-copy"
    relation: "invalidates"
    label: "смена состава подписей сносит копию"
    evidence_ref: "src/Example/cf/CommonModules/РаботаСЭП/Ext/Module.bsl:1445-1476"
  - from: "signed-original"
    to: "user-sees"
    relation: "protects"
    label: "оригинал удалять нельзя"
    evidence_ref: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl:3848-3864"

views:
  - type: "causal-flow"
    focus: "Почему удаления только копии недостаточно при смене формата"
  - type: "layers"
    focus: "Оригинал, картинка, копия, результат"
```
