# Шаблон файла панели (не живой `.canvas.tsx`)

Родитель заполняет этот каркас манифестом картографа и записывает один `.canvas.tsx` в каталог панелей текущей области. Живой файл в git не класть.

Обязательно:

- импорт только из `cursor/canvas`;
- главный вид — граф: `computeDAGLayout` (узлы, стрелки, полосы уровней). Стена одинаковых карточек и список без рёбер **запрещены**;
- переключатель видов меняет раскладку (направление или группировку), а не только подпись «Вид:»;
- клик узла открывает доказательство через `openFile`;
- выбранный вид хранится в `useCanvasState`;
- `newComposerChat` **не** вызывать;
- в шапку переносить `question`, `insight`, `sources`; у узла — `name`, `state` если есть; у связи — `label` и `relation` (не сырой `id` как единственная подпись).

```tsx
import {
  Button,
  H1,
  Row,
  Stack,
  Text,
  computeDAGLayout,
  useCanvasAction,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type NodeId = string;
type ViewType = "causal-flow" | "layers";

type MapNode = {
  id: NodeId;
  name: string;
  kind: string;
  layer: string;
  effect: string;
  evidence: { path: string; start?: number; end?: number };
  state?: string;
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
  sources: ["<header.sources>"],
  view_primary: "causal-flow" as ViewType,
};

const NODES: MapNode[] = [
  /* манифест.nodes */
];

const EDGES: MapEdge[] = [
  /* манифест.edges */
];

const NODE_W = 180;
const NODE_H = 56;

export default function ScenarioMap() {
  const theme = useHostTheme();
  const dispatch = useCanvasAction();
  const [view, setView] = useCanvasState<ViewType>("view", HEADER.view_primary);
  const [selected, setSelected] = useCanvasState<NodeId | null>("selected", null);

  const selectedNode = NODES.find((node) => node.id === selected);
  const layout = computeDAGLayout({
    nodes: NODES.map((node) => ({ id: node.id })),
    edges: EDGES.map((edge) => ({ from: edge.from, to: edge.to })),
    direction: view === "layers" ? "vertical" : "horizontal",
    nodeWidth: NODE_W,
    nodeHeight: NODE_H,
    rankGap: 64,
    nodeGap: 28,
    padding: 24,
  });

  function openEvidence(node: MapNode) {
    dispatch({
      type: "openFile",
      path: node.evidence.path,
    });
  }

  function rankTitle(rankIndex: number, nodeIds: string[]) {
    const layers = nodeIds
      .map((id) => NODES.find((node) => node.id === id)?.layer)
      .filter((name): name is string => Boolean(name));
    return layers[0] ?? `уровень ${rankIndex}`;
  }

  return (
    <Stack gap={16}>
      <H1>{HEADER.question}</H1>
      <Text tone="secondary">{HEADER.insight}</Text>
      <Text tone="tertiary">{HEADER.sources.join(" · ")}</Text>
      <Row gap={8}>
        <Button
          variant={view === "causal-flow" ? "primary" : "secondary"}
          onClick={() => setView("causal-flow")}
        >
          Связи
        </Button>
        <Button
          variant={view === "layers" ? "primary" : "secondary"}
          onClick={() => setView("layers")}
        >
          Слои
        </Button>
      </Row>
      <svg
        width={layout.width}
        height={layout.height}
        viewBox={`0 0 ${layout.width} ${layout.height}`}
        role="img"
        aria-label={HEADER.question}
        style={{ display: "block", maxWidth: "100%" }}
      >
        {layout.ranks.map((rank) => (
          <g key={`rank-${rank.rank}`}>
            <rect
              x={rank.x}
              y={rank.y}
              width={rank.width}
              height={rank.height}
              rx={8}
              fill={theme.fill.quaternary}
            />
            <text
              x={rank.x + 10}
              y={rank.y + 16}
              fill={theme.text.tertiary}
              fontSize={11}
            >
              {rankTitle(rank.rank, rank.nodeIds)}
            </text>
          </g>
        ))}
        {layout.edges.map((edge) => {
          const meta = EDGES.find(
            (item) => item.from === edge.from && item.to === edge.to,
          );
          const active = edge.from === selected || edge.to === selected;
          const midX = (edge.sourceX + edge.targetX) / 2;
          const midY = (edge.sourceY + edge.targetY) / 2;
          return (
            <g key={`edge-${edge.from}-${edge.to}-${edge.isBackEdge}`}>
              <line
                x1={edge.sourceX}
                y1={edge.sourceY}
                x2={edge.targetX}
                y2={edge.targetY}
                stroke={active ? theme.accent.primary : theme.stroke.secondary}
                strokeWidth={active ? 2.2 : 1.4}
                strokeDasharray={edge.isBackEdge ? "6 4" : undefined}
              />
              {meta ? (
                <text
                  x={midX}
                  y={midY - 6}
                  textAnchor="middle"
                  fill={theme.text.secondary}
                  fontSize={10}
                >
                  {meta.label}
                </text>
              ) : null}
            </g>
          );
        })}
        {layout.nodes.map((placed) => {
          const node = NODES.find((item) => item.id === placed.id);
          if (!node) return null;
          const isSelected = placed.id === selected;
          return (
            <g
              key={`node-${placed.id}`}
              onClick={() => {
                setSelected(node.id);
                openEvidence(node);
              }}
              style={{ cursor: "pointer" }}
            >
              <rect
                x={placed.x}
                y={placed.y}
                width={NODE_W}
                height={NODE_H}
                rx={8}
                fill={isSelected ? theme.fill.secondary : theme.bg.elevated}
                stroke={isSelected ? theme.accent.primary : theme.stroke.secondary}
                strokeWidth={isSelected ? 2.4 : 1}
              />
              <text
                x={placed.x + NODE_W / 2}
                y={placed.y + 22}
                textAnchor="middle"
                fill={theme.text.primary}
                fontSize={12}
              >
                {node.name}
              </text>
              <text
                x={placed.x + NODE_W / 2}
                y={placed.y + 40}
                textAnchor="middle"
                fill={theme.text.tertiary}
                fontSize={10}
              >
                {node.state ?? node.layer}
              </text>
            </g>
          );
        })}
      </svg>
      {selectedNode ? (
        <Stack gap={4}>
          <Text>{selectedNode.effect}</Text>
          <Text tone="tertiary">{selectedNode.evidence.path}</Text>
        </Stack>
      ) : null}
    </Stack>
  );
}
```
