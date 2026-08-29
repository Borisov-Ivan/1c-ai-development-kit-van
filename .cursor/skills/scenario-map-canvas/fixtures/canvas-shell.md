# Шаблон файла панели (не живой `.canvas.tsx`)

Родитель заполняет этот каркас манифестом картографа и записывает один `.canvas.tsx` в каталог панелей текущей области. Живой файл в git не класть.

Обязательно:

- импорт только из `cursor/canvas`;
- главный вид — граф: `computeDAGLayout` (узлы, стрелки, полосы по слою узлов). Стена одинаковых карточек и список без рёбер **запрещены**;
- координаты всех карт считает панель; прямоугольник полосы — объемлющая рамка посчитанных координат узлов этого слоя (с отступом); список слоёв — по первому появлению в узлах манифеста только для порядка отрисовки и подписей;
- если полоса подписана, подпись — имя слоя её узлов; подпись рангом и подпись слоем первого узла ранга **запрещены**; смешанный ряд без однородного слоя не подписывать;
- для карт длиннее двенадцати узлов та же раскладка работает как запасная и отличается только тем, что полосы остаются без подписей;
- если рамки двух полос пересекаются — заливку полос не рисовать, оставить имя слоя рядом со своими узлами;
- переключатель видов меняет раскладку (направление или группировку), а не только подпись «Вид:»;
- если в манифесте есть `modes` — второй ряд кнопок: режим меняет подсветку того же набора узлов и рёбер и один короткий ответ, состав рёбер не трогает и рёбра не скрывает;
- у режима обязательны `id`, человекочитаемый `label`, `highlight_nodes`, `highlight_edges` (пары `from`/`to` уже опубликованных связей) и `answer` не длиннее двенадцати слов;
- выбор узла показывает эффект и доказательство в панели деталей; файл открывается **кнопкой** этой панели через `openFile`; `newComposerChat` **не** вызывать;
- стартово выбирать `header.focus_node` (если такого id нет — первый узел);
- заголовок (`header.question`) не длиннее двенадцати слов; подпись ребра не длиннее четырёх слов (длинное — в панели деталей); литеральные кавычки кода в текстах панели запрещены;
- у каждой связи — маркер направления; цвет и пунктир по `relation`; легенда только фактически использованных типов **под** графом; обратное ребро раскладки — изгибом или маркером, **не** пунктиром (пунктир занят типом связи);
- аннотации рисовать у якорного узла или ребра с видимым доказательством и подсветкой зоны якоря; не перекрывать граф стеной карточек; координаты аннотации из манифеста **не** читать; якорь: `{ node: id }` либо `{ edge: { from, to } }`;
- в шапку переносить `question`, `insight`, `sources`, `focus_node`; у узла — `name`, `state` если есть; у связи — `label` и `relation` (не сырой `id` как единственная подпись);
- файл панели должен проходить проверку типов носителя: `key` ставить только на нативные элементы (`span`, `g`), не на `Button` / `Row` / `Text`; якорь аннотации сначала копировать в локальную переменную, затем читать поля — иначе проверка записи нечистая и среда не показывает кнопку.

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
type CategoryKey =
  | "gray"
  | "purple"
  | "green"
  | "yellow"
  | "cyan"
  | "pink"
  | "blue"
  | "orange"
  | "red";

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

type MapMode = {
  id: string;
  label: string;
  highlight_nodes: NodeId[];
  highlight_edges: { from: NodeId; to: NodeId }[];
  answer: string;
};

type MapAnnotation = {
  text: string;
  evidence_ref: string;
  anchor: { node: NodeId } | { edge: { from: NodeId; to: NodeId } };
};

const HEADER = {
  question: "<header.question>",
  insight: "<header.insight>",
  sources: ["<header.sources>"],
  view_primary: "causal-flow" as ViewType,
  focus_node: "<header.focus_node>" as NodeId,
};

const NODES: MapNode[] = [
  /* манифест.nodes */
];

const EDGES: MapEdge[] = [
  /* манифест.edges */
];

const MODES: MapMode[] = [
  /* манифест.modes */
];

const ANNOTATIONS: MapAnnotation[] = [
  /* манифест.annotations */
];

const NODE_W = 180;
const NODE_H = 56;
const BAND_PAD = 12;
const ANNO_GUTTER = 220;

const RELATION_META: Record<
  string,
  { category: CategoryKey; dash?: string; title: string }
> = {
  follows: { category: "gray", dash: "4 3", title: "следование" },
  calls: { category: "blue", title: "вызов" },
  reads: { category: "cyan", title: "чтение" },
  writes: { category: "green", title: "запись" },
  feeds: { category: "purple", title: "питает" },
  transforms: { category: "yellow", title: "преобразует" },
  reuses: { category: "orange", dash: "6 4", title: "повтор" },
  invalidates: { category: "red", dash: "6 4", title: "сброс" },
  protects: { category: "pink", title: "защита" },
  "branches-to": { category: "blue", dash: "2 3", title: "ветка" },
  "converges-to": { category: "green", dash: "8 3", title: "схождение" },
};

type Placed = { id: string; x: number; y: number };
type Band = {
  layer: string;
  x: number;
  y: number;
  width: number;
  height: number;
  nodeIds: string[];
};

function boxesOverlap(
  a: { x: number; y: number; width: number; height: number },
  b: { x: number; y: number; width: number; height: number },
) {
  return (
    a.x < b.x + b.width &&
    a.x + a.width > b.x &&
    a.y < b.y + b.height &&
    a.y + a.height > b.y
  );
}

function layerOrder(nodes: MapNode[]) {
  const seen: string[] = [];
  for (const node of nodes) {
    if (!seen.includes(node.layer)) seen.push(node.layer);
  }
  return seen;
}

function computeLayerBands(placed: Placed[], nodes: MapNode[]): Band[] {
  const byLayer = new Map<string, Placed[]>();
  for (const layer of layerOrder(nodes)) byLayer.set(layer, []);
  for (const item of placed) {
    const meta = nodes.find((node) => node.id === item.id);
    if (!meta) continue;
    const bucket = byLayer.get(meta.layer);
    if (bucket) bucket.push(item);
    else byLayer.set(meta.layer, [item]);
  }
  const bands: Band[] = [];
  for (const layer of layerOrder(nodes)) {
    const items = byLayer.get(layer) ?? [];
    if (items.length === 0) continue;
    const minX = Math.min(...items.map((item) => item.x)) - BAND_PAD;
    const minY = Math.min(...items.map((item) => item.y)) - BAND_PAD;
    const maxX = Math.max(...items.map((item) => item.x + NODE_W)) + BAND_PAD;
    const maxY = Math.max(...items.map((item) => item.y + NODE_H)) + BAND_PAD;
    bands.push({
      layer,
      x: minX,
      y: minY,
      width: maxX - minX,
      height: maxY - minY,
      nodeIds: items.map((item) => item.id),
    });
  }
  return bands;
}

function bandsOverlap(bands: Band[]) {
  for (let i = 0; i < bands.length; i++) {
    for (let j = i + 1; j < bands.length; j++) {
      if (boxesOverlap(bands[i], bands[j])) return true;
    }
  }
  return false;
}

function curveBackEdge(
  sx: number,
  sy: number,
  tx: number,
  ty: number,
) {
  const dx = tx - sx;
  const dy = ty - sy;
  const len = Math.hypot(dx, dy) || 1;
  const ox = (-dy / len) * 36;
  const oy = (dx / len) * 36;
  const cx = (sx + tx) / 2 + ox;
  const cy = (sy + ty) / 2 + oy;
  return `M ${sx} ${sy} Q ${cx} ${cy} ${tx} ${ty}`;
}

function resolveFocus(): NodeId | null {
  if (HEADER.focus_node && NODES.some((node) => node.id === HEADER.focus_node)) {
    return HEADER.focus_node;
  }
  return NODES[0]?.id ?? null;
}

function edgeHighlighted(
  mode: MapMode | undefined,
  from: NodeId,
  to: NodeId,
) {
  if (!mode) return true;
  return mode.highlight_edges.some(
    (item) => item.from === from && item.to === to,
  );
}

export default function ScenarioMap() {
  const theme = useHostTheme();
  const dispatch = useCanvasAction();
  const [view, setView] = useCanvasState<ViewType>("view", HEADER.view_primary);
  const [selected, setSelected] = useCanvasState<NodeId | null>(
    "selected",
    resolveFocus(),
  );
  const [modeId, setModeId] = useCanvasState<string | null>("mode", null);

  const selectedNode = NODES.find((node) => node.id === selected);
  const activeMode = MODES.find((mode) => mode.id === modeId);
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
  const bands = computeLayerBands(layout.nodes, NODES);
  const overlap = bandsOverlap(bands);
  const labelBands = NODES.length <= 12;
  const usedRelations = Array.from(new Set(EDGES.map((edge) => edge.relation)));
  const svgWidth = layout.width + (ANNOTATIONS.length > 0 ? ANNO_GUTTER : 0);
  const incident = EDGES.filter(
    (edge) => edge.from === selected || edge.to === selected,
  );

  function paint(relation: string) {
    const meta = RELATION_META[relation] ?? {
      category: "gray" as CategoryKey,
      title: relation,
    };
    return {
      stroke: theme.category[meta.category],
      dash: meta.dash,
      title: meta.title,
    };
  }

  function openEvidence(node: MapNode) {
    dispatch({
      type: "openFile",
      path: node.evidence.path,
    });
  }

  function nodeHot(id: NodeId) {
    if (!activeMode) return true;
    return activeMode.highlight_nodes.includes(id);
  }

  function anchorPoint(annotation: MapAnnotation) {
    const anchor = annotation.anchor;
    if ("node" in anchor) {
      const nodeId = anchor.node;
      const placed = layout.nodes.find((item) => item.id === nodeId);
      if (!placed) return null;
      return {
        x: placed.x + NODE_W / 2,
        y: placed.y + NODE_H / 2,
        kind: "node" as const,
        id: placed.id,
      };
    }
    const fromId = anchor.edge.from;
    const toId = anchor.edge.to;
    const edge = layout.edges.find(
      (item) => item.from === fromId && item.to === toId,
    );
    if (!edge) return null;
    return {
      x: (edge.sourceX + edge.targetX) / 2,
      y: (edge.sourceY + edge.targetY) / 2,
      kind: "edge" as const,
      from: edge.from,
      to: edge.to,
    };
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
      {MODES.length > 0 ? (
        <Row gap={8}>
          {MODES.map((mode) => (
            <span key={mode.id}>
              <Button
                variant={modeId === mode.id ? "primary" : "secondary"}
                onClick={() =>
                  setModeId((current) => (current === mode.id ? null : mode.id))
                }
              >
                {mode.label}
              </Button>
            </span>
          ))}
        </Row>
      ) : null}
      {activeMode ? <Text>{activeMode.answer}</Text> : null}
      <svg
        width={svgWidth}
        height={layout.height}
        viewBox={`0 0 ${svgWidth} ${layout.height}`}
        role="img"
        aria-label={HEADER.question}
        style={{ display: "block", maxWidth: "100%" }}
      >
        <defs>
          {usedRelations.map((relation) => {
            const { stroke } = paint(relation);
            const id = `arrow-${relation}`;
            return (
              <marker
                key={id}
                id={id}
                markerWidth={8}
                markerHeight={8}
                refX={7}
                refY={4}
                orient="auto"
                markerUnits="strokeWidth"
              >
                <polygon points="0 0, 8 4, 0 8" fill={stroke} />
              </marker>
            );
          })}
        </defs>
        {bands.map((band) => (
          <g key={`band-${band.layer}`}>
            {overlap ? null : (
              <rect
                x={band.x}
                y={band.y}
                width={band.width}
                height={band.height}
                rx={8}
                fill={theme.fill.quaternary}
              />
            )}
            {labelBands ? (
              <text
                x={
                  overlap
                    ? (layout.nodes.find((item) => item.id === band.nodeIds[0])
                        ?.x ?? band.x)
                    : band.x + 10
                }
                y={
                  overlap
                    ? (layout.nodes.find((item) => item.id === band.nodeIds[0])
                        ?.y ?? band.y) - 4
                    : band.y + 16
                }
                fill={theme.text.tertiary}
                fontSize={11}
              >
                {band.layer}
              </text>
            ) : null}
          </g>
        ))}
        {layout.edges.map((edge) => {
          const meta = EDGES.find(
            (item) => item.from === edge.from && item.to === edge.to,
          );
          const relation = meta?.relation ?? "follows";
          const { stroke, dash } = paint(relation);
          const hot = edgeHighlighted(activeMode, edge.from, edge.to);
          const selectedHere =
            edge.from === selected || edge.to === selected;
          const trap = ANNOTATIONS.some((annotation) => {
            const anchor = annotation.anchor;
            if (!("edge" in anchor)) return false;
            return (
              anchor.edge.from === edge.from && anchor.edge.to === edge.to
            );
          });
          const d = edge.isBackEdge
            ? curveBackEdge(
                edge.sourceX,
                edge.sourceY,
                edge.targetX,
                edge.targetY,
              )
            : `M ${edge.sourceX} ${edge.sourceY} L ${edge.targetX} ${edge.targetY}`;
          const midX = (edge.sourceX + edge.targetX) / 2;
          const midY = (edge.sourceY + edge.targetY) / 2;
          return (
            <g key={`edge-${edge.from}-${edge.to}-${edge.isBackEdge}`}>
              <path
                d={d}
                fill="none"
                stroke={trap ? theme.accent.primary : stroke}
                strokeWidth={selectedHere || trap ? 2.4 : 1.6}
                strokeDasharray={dash}
                markerEnd={`url(#arrow-${relation})`}
                opacity={hot ? 1 : 0.35}
              />
              {meta ? (
                <text
                  x={midX}
                  y={midY - 8}
                  textAnchor="middle"
                  fill={theme.text.secondary}
                  fontSize={10}
                  opacity={hot ? 1 : 0.35}
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
          const hot = nodeHot(placed.id);
          const trap = ANNOTATIONS.some((annotation) => {
            const anchor = annotation.anchor;
            return "node" in anchor && anchor.node === placed.id;
          });
          return (
            <g
              key={`node-${placed.id}`}
              onClick={() => setSelected(node.id)}
              style={{ cursor: "pointer" }}
              opacity={hot ? 1 : 0.35}
            >
              {trap ? (
                <rect
                  x={placed.x - 6}
                  y={placed.y - 6}
                  width={NODE_W + 12}
                  height={NODE_H + 12}
                  rx={10}
                  fill="none"
                  stroke={theme.accent.primary}
                  strokeWidth={2}
                />
              ) : null}
              <rect
                x={placed.x}
                y={placed.y}
                width={NODE_W}
                height={NODE_H}
                rx={8}
                fill={isSelected ? theme.fill.secondary : theme.bg.elevated}
                stroke={
                  isSelected ? theme.accent.primary : theme.stroke.secondary
                }
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
        {ANNOTATIONS.map((annotation, index) => {
          const point = anchorPoint(annotation);
          if (!point) return null;
          const boxX = layout.width + 12;
          const boxY = Math.max(8, point.y - 18 + index * 4);
          return (
            <g key={`anno-${index}`}>
              <line
                x1={point.x}
                y1={point.y}
                x2={boxX}
                y2={boxY + 10}
                stroke={theme.accent.primary}
                strokeWidth={1.2}
              />
              <rect
                x={boxX}
                y={boxY}
                width={ANNO_GUTTER - 24}
                height={44}
                rx={6}
                fill={theme.bg.elevated}
                stroke={theme.accent.primary}
              />
              <text
                x={boxX + 8}
                y={boxY + 16}
                fill={theme.text.primary}
                fontSize={11}
              >
                {annotation.text}
              </text>
              <text
                x={boxX + 8}
                y={boxY + 34}
                fill={theme.text.tertiary}
                fontSize={9}
              >
                {annotation.evidence_ref}
              </text>
            </g>
          );
        })}
      </svg>
      {usedRelations.length > 0 ? (
        <Row gap={16}>
          {usedRelations.map((relation) => {
            const { stroke, dash, title } = paint(relation);
            return (
              <span key={relation}>
                <Row gap={6}>
                  <svg width={28} height={10} aria-hidden="true">
                    <line
                      x1={2}
                      y1={5}
                      x2={20}
                      y2={5}
                      stroke={stroke}
                      strokeWidth={2}
                      strokeDasharray={dash}
                    />
                  </svg>
                  <Text tone="tertiary">{title}</Text>
                </Row>
              </span>
            );
          })}
        </Row>
      ) : null}
      {selectedNode ? (
        <Stack gap={8}>
          <Text>{selectedNode.effect}</Text>
          {incident.map((edge) => (
            <span key={`${edge.from}-${edge.to}`}>
              <Text tone="secondary">
                {edge.label} · {paint(edge.relation).title} · {edge.evidence_ref}
              </Text>
            </span>
          ))}
          <Button onClick={() => openEvidence(selectedNode)}>
            Открыть доказательство
          </Button>
        </Stack>
      ) : null}
    </Stack>
  );
}
```
