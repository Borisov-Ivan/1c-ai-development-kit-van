# Шаблон файла панели (не живой `.canvas.tsx`)

Родитель подставляет константу `DATA` из текущего ответа и записывает один `.canvas.tsx` в каталог панелей текущей области. Живой файл в git не класть.

Обязательно:

- импорт только из `cursor/canvas`;
- рендер читает `presentation.form`: `flow` | `table` | `hierarchy` | `card`;
- иерархия — вложенный `Stack`, не граф с абсолютной раскладкой;
- имена на полотне — полные фразы, не многоточие вместо шага;
- стартово выбран `focus_item` (исход или виновник);
- выбор элемента показывает `explanation` в деталях и **не** открывает файл;
- путь из ответа — кнопкой в деталях через `openFile`; `newComposerChat` **не** вызывать;
- `key` только на нативных элементах (`span`), не на `Button` / `Row` / `Text`;
- цвета из `useHostTheme()`; без градиентов, теней и эмодзи;
- **запрещено:** граф с абсолютной раскладкой, снятие подписи с полотна, фиксированная ширина коробки как носитель смысла.

Родитель **до записи** выбирает форму: больше 6 элементов или больше 5 связей → `table` или `card`, не `flow` и не `hierarchy`.

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

type PanelData = {
  question: string;
  takeaway: string;
  items: Item[];
  relations?: Relation[];
  focus_item: ItemId;
  presentation: { form: Form };
};

/* Родитель заменяет объект целиком данными текущего ответа. */
const DATA: PanelData = {
  question: "Когда документ проводится, а когда нет",
  takeaway: "Проведение идёт только если заполнен договор; иначе запись остаётся черновиком",
  items: [
    {
      id: "contract",
      label: "Договор заполнен",
      explanation: "Без договора проведение не стартует",
      confidence: "fact",
    },
    {
      id: "post",
      label: "Документ проводится",
      explanation: "Движения пишутся, если договор на месте",
      confidence: "fact",
    },
    {
      id: "draft",
      label: "Документ остаётся черновиком",
      explanation: "Договор пуст — проведение не вызывается",
      confidence: "fact",
    },
  ],
  relations: [
    { from: "contract", to: "post", label: "если заполнен", confidence: "fact" },
    { from: "contract", to: "draft", label: "если пуст", confidence: "fact" },
  ],
  focus_item: "post",
  presentation: { form: "table" },
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
  const selected = itemById(selectedId) ?? itemById(initial);
  const relations = DATA.relations ?? [];
  const form = DATA.presentation.form;

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

  function ItemButton({ item }: { item: Item }) {
    const active = item.id === selected?.id;
    return (
      <Stack gap={6}>
        <Button
          variant={active ? "primary" : "secondary"}
          onClick={() => selectItem(item.id)}
        >
          {item.label}
        </Button>
        {confidenceLabel(item.confidence) ? (
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

  function Main() {
    if (form === "table") return <TableView />;
    if (form === "hierarchy") return <HierarchyView />;
    if (form === "card") return <CardView />;
    return <FlowView />;
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
