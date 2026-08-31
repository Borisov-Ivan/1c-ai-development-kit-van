# Шаблон файла панели (не живой `.canvas.tsx`)

Родитель подставляет константу `DATA` из текущего ответа и записывает один `.canvas.tsx` в каталог панелей текущей области. Живой файл в git не класть.

Обязательно:

- импорт только из `cursor/canvas`; не добавлять `Grid` и `Callout`;
- рендер читает `presentation.form`: `flow` | `table` | `hierarchy` | `card` (четыре значения; скелет со сценами — вид главной области для `flow` и `hierarchy`, не новое значение формы);
- в модель входят шаги истории `scenes[]`: текст шага и какие части в фокусе;
- главная область по умолчанию — скелет слоёв и текущий шаг; «Назад / Дальше» — общая обёртка для `flow` и `hierarchy`, не копия внутри каждой ветки;
- ветки `table` и `card` сохраняют свой вид без обязательного степпера;
- иерархия — вложенный `Stack`, не граф с абсолютной раскладкой;
- имена на полотне — полные фразы, не многоточие вместо шага;
- стартово выбран `focus_item` (исход или виновник);
- выбор элемента показывает `explanation` (роль) и текст текущей сцены («в этом шаге»); отдельного поля на пару «часть × шаг» нет; выбор **не** открывает файл;
- путь из ответа — кнопкой в деталях через `openFile`; `newComposerChat` **не** вызывать;
- `key` только на нативных элементах (`span`), не на `Button` / `Row` / `Text`;
- цвета из `useHostTheme()`; без градиентов, теней и эмодзи;
- выбранная часть — основной вариант кнопки независимо от фокуса сцены; вне фокуса приглушается пояснение вторичным или третичным тоном текста, не прозрачностью, не своим цветом и не наложением; подпись части остаётся читаемой;
- **запрещено:** граф с абсолютной раскладкой, снятие подписи с полотна, фиксированная ширина коробки как носитель смысла, самодельный HTML-плакат, водяной текст, сюжет штампа электронной подписи как эталон.

Родитель **до записи:** таблица — только если вопрос сам есть сравнение одних и тех же свойств; число частей само не переводит в таблицу. Пока главная область — скелет со сценами: если в одной сцене больше шести именованных частей — дробить на сцены или сворачивать уровень, не сбрасывать в таблицу. Пример в этом файле не ставит `form: "table"`.

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
  presentation: { form: Form };
  scenes?: Scene[];
};

/* Родитель заменяет объект целиком данными текущего ответа. */
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
  const form = DATA.presentation.form;
  const skeletonScenes = form === "flow" || form === "hierarchy";

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
        {DATA.items.map((item, index) => {
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
              {rels.length === 0 && index < DATA.items.length - 1 ? (
                <Text size="small" tone="tertiary">
                  ↓
                </Text>
              ) : null}
            </span>
          );
        })}
      </Stack>
    );
  }

  function TableView() {
    const headers = ["Элемент", "Пояснение", "Связь"];
    const rows = DATA.items.map((item) => {
      const rels = outgoing(item.id);
      const relText =
        rels.length === 0
          ? "—"
          : rels
              .map((r) => {
                const target = itemById(r.to)?.label ?? r.to;
                const guess = confidenceLabel(r.confidence);
                return `${r.label} → ${target}${guess ? ` (${guess})` : ""}`;
              })
              .join("; ");
      return [
        <Button
          variant={item.id === selected?.id ? "primary" : "secondary"}
          onClick={() => selectItem(item.id)}
        >
          {item.label}
        </Button>,
        item.explanation,
        relText,
      ];
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
    if (form === "table") return <TableView />;
    if (form === "card") return <CardView />;
    if (form === "hierarchy") {
      return <SkeletonChrome body={<HierarchyView />} />;
    }
    return <SkeletonChrome body={<FlowView />} />;
  }

  return (
    <Stack gap={16} style={{ padding: 16 }}>
      <Stack gap={8}>
        <H1>{DATA.question}</H1>
        <Text weight="semibold">{DATA.takeaway}</Text>
      </Stack>
      <Divider />
      <Row gap={24} align="start" wrap>
        <Stack gap={12} style={{ flex: 2, minWidth: 280 }}>
          <H2>Как устроено</H2>
          <Main />
        </Stack>
        {selected ? (
          <Card style={{ flex: 1, minWidth: 240 }}>
            <CardHeader>{selected.label}</CardHeader>
            <CardBody>
              <Stack gap={10}>
                <Text>{selected.explanation}</Text>
                {currentScene && skeletonScenes ? (
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
