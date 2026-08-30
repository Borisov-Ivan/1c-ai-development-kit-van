# Шаблон файла панели (не живой `.canvas.tsx`)

Родитель заполняет этот каркас манифестом картографа и записывает один `.canvas.tsx` в каталог панелей текущей области. Живой файл в git не класть.

Обязательно:

- импорт только из `cursor/canvas`;
- клик узла открывает доказательство через `openFile` (путь + `selection`);
- выбранный вид хранится в `useCanvasState`;
- `newComposerChat` **не** вызывать.

```tsx
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  H1,
  Pill,
  Row,
  Stack,
  Text,
  useCanvasAction,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type NodeId = string;
type ViewType = "causal-flow" | "layers" | "flow";

type MapNode = {
  id: NodeId;
  name: string;
  kind: string;
  layer: string;
  effect: string;
  evidence: { path: string; start?: number; end?: number };
};

type MapEdge = {
  from: NodeId;
  to: NodeId;
  relation: string;
  label: string;
  evidence_ref: string;
};

const HEADER = {
  question: "<header.question>",
  insight: "<header.insight>",
  view_primary: "causal-flow" as ViewType,
};

const NODES: MapNode[] = [
  /* манифест.nodes */
];

const EDGES: MapEdge[] = [
  /* манифест.edges */
];

export default function ScenarioMap() {
  const theme = useHostTheme();
  const dispatch = useCanvasAction();
  const [view, setView] = useCanvasState<ViewType>("view", HEADER.view_primary);
  const [selected, setSelected] = useCanvasState<NodeId | null>("selected", null);

  const selectedNode = NODES.find((node) => node.id === selected);

  function openEvidence(node: MapNode) {
    dispatch({
      type: "openFile",
      path: node.evidence.path,
      selection:
        node.evidence.start && node.evidence.end
          ? {
              start: { line: node.evidence.start, character: 0 },
              end: { line: node.evidence.end, character: 0 },
            }
          : undefined,
    });
  }

  return (
    <Stack gap={16}>
      <H1>{HEADER.question}</H1>
      <Text tone="secondary">{HEADER.insight}</Text>
      <Row gap={8}>
        <Button onClick={() => setView("causal-flow")}>Связи</Button>
        <Button onClick={() => setView("layers")}>Слои</Button>
      </Row>
      <Text style={{ color: theme.text.secondary }}>Вид: {view}</Text>
      <Stack gap={8}>
        {NODES.map((node) => (
          <div key={node.id}>
            <Card>
              <CardHeader trailing={<Pill size="sm">{node.layer}</Pill>}>
                {node.name}
              </CardHeader>
              <CardBody>
                <Text>{node.effect}</Text>
                <Button
                  onClick={() => {
                    setSelected(node.id);
                    openEvidence(node);
                  }}
                >
                  Доказательство
                </Button>
              </CardBody>
            </Card>
          </div>
        ))}
      </Stack>
      <Stack gap={4}>
        {EDGES.map((edge) => (
          <div key={`${edge.from}-${edge.to}-${edge.relation}`}>
            <Text>
              {edge.from} → {edge.to}: {edge.label} ({edge.relation}; {edge.evidence_ref})
            </Text>
          </div>
        ))}
      </Stack>
      {selectedNode ? (
        <Text tone="secondary">Выбран: {selectedNode.name}</Text>
      ) : null}
    </Stack>
  );
}
```

Раскладка слоёв и цепочки MAY опираться на `computeDAGLayout` носителя, без предметных имён. Главный вид — не список без рёбер.
