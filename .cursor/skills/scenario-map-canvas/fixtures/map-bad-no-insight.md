# Эталон «плохо»: полотно есть — смысла нет

Так **не** публиковать. Манифест структурно полон (узлы, подписанные связи), но проверка смысла на шаге макета его отсекает — в том числе предикат скрытой шапки (`6a`).

Показаны **оба** провала: вывод живёт только в тексте шапки; вторая аннотация приведена без доказательства. Находка, которая меняет действие читателя (картинка штампа живёт отдельно; смена макета копию не сбрасывает), на полотне **отсутствует**.

Отсекается пунктами self-check манифеста:

- `6a` — ответ на вопрос шапки не складывается с полотна **при скрытой шапке** (до записи смотрят поля манифеста: связи, строки, аннотации, стартовый узел — не раскладку панели);
- `6b` — находка, меняющая действие, на полотне нет;
- `6d` — вторая аннотация без доказательства; первая пересказывает шаг открытия, не ответ шапки.

```yaml
header:
  question: "Почему после смены формата штампа недостаточно удалить только готовую визуализацию?"
  insight: "Смена макета копию не сбрасывает: картинка штампа живёт отдельно и снова попадает в новую копию."
  sources:
    - "temp/reports/exploration-example-vizualizaciya-shtampa.md"
    - "temp/reports/review-example-shtamp-ep.md"
  medium: "graph"
  view_primary: "causal-flow"
  focus_node: "overlay"

nodes:
  - id: "signed-original"
    name: "Подписанный оригинал файла"
    kind: "protected-original"
    layer: "Оригинал"
    effect: "Исходный файл с электронной подписью. Штамп в него не пишется."
    evidence:
      path: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl"
      start: 3848
      end: 3864

  - id: "overlay"
    name: "Наложение по формату"
    kind: "transform"
    layer: "Слой 2 — копия"
    effect: "Картинка накладывается на копию исходного файла. Форматы идут разными путями."
    evidence:
      path: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl"
      start: 3831
      end: 3936

  - id: "cache-visual-copy"
    name: "Копия со штампом"
    kind: "cache"
    layer: "Слой 2 — копия"
    effect: "Служебная копия документа со штампом. Именно её отдают при открытии."
    evidence:
      path: "src/Example/cf/InformationRegisters/СлужебныеФайлыДокументов/Ext/ManagerModule.bsl"
      start: 43
      end: 73

  - id: "user-sees"
    name: "Пользователь открывает файл со штампом"
    kind: "user-result"
    layer: "Результат"
    effect: "При открытии подменяются двоичные данные: пользователь видит копию."
    evidence:
      path: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl"
      start: 3437
      end: 3441

edges:
  - from: "signed-original"
    to: "overlay"
    relation: "reads"
    label: "копия из оригинала"
    evidence_ref: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl:3831-3936"
  - from: "overlay"
    to: "cache-visual-copy"
    relation: "writes"
    label: "пишется служебный файл"
    evidence_ref: "src/Example/cf/InformationRegisters/СлужебныеФайлыДокументов/Ext/ManagerModule.bsl:43-73"
  - from: "cache-visual-copy"
    to: "user-sees"
    relation: "feeds"
    label: "подмена при открытии"
    evidence_ref: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl:3437-3441"
  - from: "signed-original"
    to: "user-sees"
    relation: "protects"
    label: "оригинал не трогать"
    evidence_ref: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl:3848-3864"

views:
  - type: "causal-flow"
    focus: "Как собирается копия со штампом"

annotations:
  - text: "Копию отдают при открытии"
    evidence_ref: "src/Example/cf/CommonModules/РаботаСФайламиВызовСервера/Ext/Module.bsl:3437-3441"
    anchor:
      node: "user-sees"
  - text: "Это важно запомнить"
    anchor:
      node: "overlay"

# у второй аннотации нет evidence_ref — провал 6d
```

## Почему не публиковать

- Скрыть шапку: вопрос («почему недостаточно удалить визуализацию») с полотна не читается — нет узла картинки штампа, нет события сброса, нет ловушки «смена макета не сбрасывает». Вывод живёт только в `header.insight` (`6a`).
- Находка, меняющая действие (отдельный кэш картинки; смена макета не сбрасывает копию), на полотне отсутствует (`6b`).
- Первая аннотация с доказательством пересказывает шаг открытия, не ответ шапки. Вторая аннотация без доказательства (`6d`).
- Набор после отсева по правилам графа ≥4 связанных узлов — структурный порог выполнен; провал смысла порог не лечит и в текстовый резерв не уходит.
