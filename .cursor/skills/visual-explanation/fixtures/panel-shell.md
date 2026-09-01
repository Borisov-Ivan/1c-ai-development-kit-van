# Шаблон файла панели (не живой `.canvas.tsx`)

Библиотека **необязательных рецептов**. Родитель подставляет константу `DATA` из текущего ответа и записывает один `.canvas.tsx` в каталог панелей текущей области. Живой файл в git не класть. Регистрация с чистого листа из тех же примитивов среды — штатная.

Обязательно:

- импорт только из `cursor/canvas`;
- вопрос и короткий вывод на полотне;
- имена на полотне — полные фразы, не многоточие вместо шага;
- `key` только на нативных элементах (`span`), не на `Button` / `Row` / `Text`;
- цвета из `useHostTheme()`; без градиентов, теней и эмодзи;
- выбор элемента **не** открывает файл; `newComposerChat` **не** вызывать;
- **запрещено:** граф с абсолютной раскладкой, снятие подписи с полотна, фиксированная ширина коробки как носитель смысла, самодельный HTML-плакат, водяной текст, сюжет штампа электронной подписи как эталон.

Рецепты (копировать нужный; не новое значение `presentation.form`):

- **Скелет со сценами** — работа = слои или последовательность механизма. `scenes[]`, «Назад / Дальше», части вне фокуса тускнеют вторичным тоном текста (не прозрачность). Пример `DATA` ниже — этот рецепт, не умолчание библиотеки.
- **Классификация** — копировать тело `ClassificationView` **в `Main`**, только если работа = одноимённые эффекты одного ранга **и** картина даёт то, чего нет в чате (например, рядом в отчёте цепочки, и их легко принять за шаги). Колонка = именованный класс (`group` или один элемент-класс), не пункт списка. Ряд стопок — не умолчание для любого списка.
- **Таблица свойств** — сравнение одних и тех же свойств. Имя не обязано быть кнопкой. Колонки «Элемент / Пояснение / Связь» — не единственная таблица.

`ItemButton`, степпер и карточка деталей — опции рецепта скелета, не обязательный хром. `Grid` и `Callout` в рецепты не добавлять; продукт их не запрещает на сборке с чистого листа.

Родитель **до записи:** назвать отношение и **какое восприятие дают те же части на полотне**. Нет восприятия — файл не писать. Поле формы — подсказка, его можно опустить. Готовая копия `Main` при опущенной `form` ничего не раскладывает — это незавершённая заготовка, не публикация. Классы: вставить тело `ClassificationView` в `Main`, `form` и `relations`-стрелки не копировать, `scenes` не копировать. Слои: скелет, не стопки. `Table` не подставлять, чтобы «было видно». Пустой список связей не рисует стрелки следования. Число пунктов само не выбирает раскладку. Каталог приёмов навыка на полотно не класть. Таблица — только если вопрос сам есть сравнение свойств. Пока рецепт — скелет со сценами: если в одной сцене больше шести именованных частей — дробить на сцены или сворачивать уровень, не сбрасывать в таблицу.

```tsx
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Divider,
  H1,
  H2,
  Pill,
  Row,
  Stack,
  Table,
  Text,
  useCanvasAction,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type ItemId = string;
type Confidence = "fact" | "inference" | "hypothesis";
type Form = "flow" | "table" | "hierarchy" | "card";

type Item = {
  id: ItemId;
  label: string;
  explanation: string;
  group?: string;
  confidence?: Confidence;
  evidence?: { path: string; start?: number; end?: number };
};

type Relation = {
  from: ItemId;
  to: ItemId;
  label: string;
  confidence?: Confidence;
};

type Scene = {
  text: string;
  focus: ItemId[];
};

type PanelData = {
  question: string;
  takeaway: string;
  items: Item[];
  relations?: Relation[];
  focus_item: ItemId;
  presentation?: { form?: Form };
  scenes?: Scene[];
};

const STARTER_FORMS: Form[] = ["flow", "table", "hierarchy", "card"];

/* Пример рецепта скелета (разбор механизма), не умолчание библиотеки.
   Другая работа заменяет тело Main: классы → ClassificationView(); сравнение свойств → TableView(); иначе свой Stack.
   Не крутить form. Не публиковать копию, у которой Main вернул null. */
const DATA: PanelData = {
  question: "Когда документ проводится, а когда нет",
  takeaway:
    "Проведение идёт только если заполнен договор; иначе запись остаётся черновиком",
  items: [
    {
      id: "contract",
      label: "Договор в шапке",
      explanation: "Источник: без договора проведение не стартует",
      confidence: "fact",
    },
    {
      id: "post",
      label: "Документ проводится",
      explanation: "Обработка пишет движения, если договор на месте",
      confidence: "fact",
    },
    {
      id: "draft",
      label: "Документ остаётся черновиком",
      explanation: "Исход без договора: проведение не вызывается",
      confidence: "fact",
    },
  ],
  relations: [
    { from: "contract", to: "post", label: "если заполнен", confidence: "fact" },
    { from: "contract", to: "draft", label: "если пуст", confidence: "fact" },
  ],
  focus_item: "post",
  presentation: { form: "flow" },
  scenes: [
    {
      text: "Сначала смотрят договор в шапке: без него проведение не стартует.",
      focus: ["contract"],
    },
    {
      text: "Если договор заполнен, документ проводится и пишутся движения.",
      focus: ["contract", "post"],
    },
    {
      text: "Если договор пуст, документ остаётся черновиком.",
      focus: ["contract", "draft"],
    },
  ],
};

function confidenceLabel(c: Confidence | undefined): string | null {
  if (c === "inference") return "вывод";
  if (c === "hypothesis") return "догадка";
  return null;
}

function itemById(id: ItemId): Item | undefined {
  return DATA.items.find((it) => it.id === id);
}

export default function VisualExplanationPanel() {
  const theme = useHostTheme();
  const dispatch = useCanvasAction();
  const initial =
    itemById(DATA.focus_item)?.id ?? DATA.items[0]?.id ?? "";
  const [selectedId, setSelectedId] = useCanvasState<string>(
    "focus-item",
    initial,
  );
  const scenes = DATA.scenes ?? [];
  const [sceneIndex, setSceneIndex] = useCanvasState<number>("scene-index", 0);
  const safeSceneIndex =
    scenes.length === 0 ? 0 : Math.min(Math.max(sceneIndex, 0), scenes.length - 1);
  const currentScene = scenes[safeSceneIndex];
  const focusSet = currentScene
    ? new Set(currentScene.focus)
    : new Set(DATA.items.map((it) => it.id));
  const selected = itemById(selectedId) ?? itemById(initial);
  const relations = DATA.relations ?? [];
  const form = DATA.presentation?.form;
  const formIsStarter = form !== undefined && STARTER_FORMS.includes(form);
  const skeletonRecipe =
    (form === "flow" || form === "hierarchy") && scenes.length > 0;

  function selectItem(id: ItemId) {
    setSelectedId(id);
  }

  function openEvidence(item: Item) {
    if (!item.evidence?.path) return;
    dispatch({
      type: "openFile",
      path: item.evidence.path,
    });
  }

  const evidenceItems = DATA.items.filter((it) => it.evidence?.path);
  const singleEvidence = evidenceItems.length === 1 ? evidenceItems[0] : null;

  function goBack() {
    setSceneIndex(Math.max(0, safeSceneIndex - 1));
  }

  function goNext() {
    setSceneIndex(Math.min(scenes.length - 1, safeSceneIndex + 1));
  }

  function ItemButton({ item }: { item: Item }) {
    const active = item.id === selected?.id;
    const inSceneFocus = focusSet.has(item.id);
    return (
      <Stack gap={6}>
        <Button
          variant={active ? "primary" : "secondary"}
          onClick={() => selectItem(item.id)}
        >
          {item.label}
        </Button>
        {!inSceneFocus ? (
          <Text size="small" tone="tertiary">
            {item.explanation}
          </Text>
        ) : confidenceLabel(item.confidence) ? (
          <Text size="small" tone="secondary">
            {confidenceLabel(item.confidence)}
          </Text>
        ) : null}
      </Stack>
    );
  }

  function outgoing(from: ItemId): Relation[] {
    return relations.filter((r) => r.from === from);
  }

  function incomingIds(): Set<ItemId> {
    const set = new Set<ItemId>();
    for (const r of relations) set.add(r.to);
    return set;
  }

  function HierarchyBranch({ id, depth }: { id: ItemId; depth: number }) {
    const item = itemById(id);
    if (!item) return null;
    const kids = outgoing(id);
    return (
      <Stack
        gap={8}
        style={{
          marginLeft: depth === 0 ? 0 : 16,
          paddingLeft: depth === 0 ? 0 : 12,
          borderLeft:
            depth === 0 ? undefined : `1px solid ${theme.stroke.secondary}`,
        }}
      >
        <ItemButton item={item} />
        {kids.map((rel) => (
          <span key={`${rel.from}-${rel.to}`}>
            <Text size="small" tone="secondary">
              {rel.label}
              {confidenceLabel(rel.confidence)
                ? ` · ${confidenceLabel(rel.confidence)}`
                : ""}
            </Text>
            <HierarchyBranch id={rel.to} depth={depth + 1} />
          </span>
        ))}
      </Stack>
    );
  }

  function FlowView() {
    return (
      <Stack gap={12}>
        {DATA.items.map((item) => {
          const rels = outgoing(item.id);
          return (
            <span key={item.id}>
              <ItemButton item={item} />
              {rels.map((rel) => (
                <span key={`${rel.from}-${rel.to}`}>
                  <Text size="small" tone="secondary">
                    ↓ {rel.label}
                    {confidenceLabel(rel.confidence)
                      ? ` · ${confidenceLabel(rel.confidence)}`
                      : ""}
                  </Text>
                </span>
              ))}
            </span>
          );
        })}
      </Stack>
    );
  }

  function ClassificationView() {
    const grouped = new Map<string, Item[]>();
    for (const item of DATA.items) {
      const key = item.group?.trim() || item.id;
      const list = grouped.get(key) ?? [];
      list.push(item);
      grouped.set(key, list);
    }
    return (
      <Row gap={16} align="start" wrap>
        {[...grouped.entries()].map(([key, members]) => {
          const title = members[0]?.group?.trim() || members[0]?.label || key;
          return (
            <span key={key}>
              <Stack gap={6} style={{ flex: 1, minWidth: 140 }}>
                <Text weight="semibold">{title}</Text>
                {members.map((item) => (
                  <span key={item.id}>
                    {item.label !== title ? <Text>{item.label}</Text> : null}
                    <Text tone="secondary">{item.explanation}</Text>
                    {confidenceLabel(item.confidence) ? (
                      <Text size="small" tone="secondary">
                        {confidenceLabel(item.confidence)}
                      </Text>
                    ) : null}
                  </span>
                ))}
              </Stack>
            </span>
          );
        })}
      </Row>
    );
  }

  function TableView() {
    const headers =
      relations.length > 0 ? ["Имя", "Пояснение", "Отношение"] : ["Имя", "Пояснение"];
    const rows = DATA.items.map((item) => {
      const cells: Array<string> = [item.label, item.explanation];
      if (relations.length > 0) {
        const rels = outgoing(item.id);
        cells.push(
          rels.length === 0
            ? "—"
            : rels
                .map((r) => {
                  const target = itemById(r.to)?.label ?? r.to;
                  const guess = confidenceLabel(r.confidence);
                  return `${r.label} → ${target}${guess ? ` (${guess})` : ""}`;
                })
                .join("; "),
        );
      }
      return cells;
    });
    return <Table headers={headers} rows={rows} striped stickyHeader />;
  }

  function HierarchyView() {
    const incoming = incomingIds();
    const roots = DATA.items.filter((it) => !incoming.has(it.id));
    const start =
      roots.find((r) => r.id === DATA.focus_item) ??
      roots[0] ??
      DATA.items[0];
    if (!start) return null;
    const extraRoots = roots.filter((r) => r.id !== start.id);
    return (
      <Stack gap={16}>
        <HierarchyBranch id={start.id} depth={0} />
        {extraRoots.map((r) => (
          <span key={r.id}>
            <HierarchyBranch id={r.id} depth={0} />
          </span>
        ))}
      </Stack>
    );
  }

  function CardView() {
    const focus = itemById(DATA.focus_item) ?? DATA.items[0];
    if (!focus) return null;
    return (
      <Card>
        <CardHeader>{focus.label}</CardHeader>
        <CardBody>
          <Stack gap={8}>
            <Text>{DATA.takeaway}</Text>
            <Text tone="secondary">{focus.explanation}</Text>
          </Stack>
        </CardBody>
      </Card>
    );
  }

  function SkeletonChrome({ body }: { body: ReturnType<typeof FlowView> }) {
    return (
      <Stack gap={12}>
        {currentScene ? <Text>{currentScene.text}</Text> : null}
        {body}
        {scenes.length > 1 ? (
          <Row gap={8}>
            <Button variant="secondary" onClick={goBack}>
              Назад
            </Button>
            <Button variant="secondary" onClick={goNext}>
              Дальше
            </Button>
          </Row>
        ) : null}
      </Stack>
    );
  }

  function Main() {
    // !formIsStarter → null: незавершёнка, не публиковать. Сюда нельзя писать ClassificationView «потому что формы нет». Классы: заменить всё тело Main на <ClassificationView />. Слои: скелет (form flow|hierarchy + scenes). Иначе свой Stack в теле Main. Table не подставлять «чтобы было видно».
    if (!formIsStarter) return null;
    if (form === "table") return <TableView />;
    if (form === "card") return <CardView />;
    if (form === "hierarchy") {
      return skeletonRecipe ? (
        <SkeletonChrome body={<HierarchyView />} />
      ) : (
        <HierarchyView />
      );
    }
    return skeletonRecipe ? <SkeletonChrome body={<FlowView />} /> : <FlowView />;
  }

  return (
    <Stack gap={16} style={{ padding: 16 }}>
      <Stack gap={8}>
        <H1>{DATA.question}</H1>
        <Text weight="semibold">{DATA.takeaway}</Text>
        {singleEvidence && !skeletonRecipe ? (
          <Button
            variant="secondary"
            onClick={() => openEvidence(singleEvidence)}
          >
            Открыть файл
          </Button>
        ) : null}
      </Stack>
      <Divider />
      <Row gap={24} align="start" wrap>
        <Stack gap={12} style={{ flex: 2, minWidth: 280 }}>
          {formIsStarter ? <H2>Как устроено</H2> : null}
          <Main />
        </Stack>
        {skeletonRecipe && selected ? (
          <Card style={{ flex: 1, minWidth: 240 }}>
            <CardHeader>{selected.label}</CardHeader>
            <CardBody>
              <Stack gap={10}>
                <Text>{selected.explanation}</Text>
                {currentScene ? (
                  <Text tone="secondary">{currentScene.text}</Text>
                ) : null}
                {confidenceLabel(selected.confidence) ? (
                  <Pill size="sm">
                    {confidenceLabel(selected.confidence) ?? ""}
                  </Pill>
                ) : null}
                {selected.evidence?.path ? (
                  <Button
                    variant="secondary"
                    onClick={() => openEvidence(selected)}
                  >
                    Открыть файл
                  </Button>
                ) : null}
              </Stack>
            </CardBody>
          </Card>
        ) : null}
      </Row>
    </Stack>
  );
}
```
