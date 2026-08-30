# Шаблон файла панели (не живой `.canvas.tsx`)

Родитель заполняет этот каркас манифестом картографа и записывает один `.canvas.tsx` в каталог панелей текущей области. Живой файл в git не класть.

Обязательно:

- импорт только из `cursor/canvas`;
- главное средство читает `header.medium`: `graph` (умолчание, топология и смешанное содержание) или `table` (правило о условиях). Главный вид отвечает на вопрос шапки (ADR-0009). Стена одинаковых карточек, список и аккордеон без связей и без вывода **запрещены**; таблица со смысловыми колонками и выводом **разрешена**;
- для `medium: table`: строка = узел; колонки фиксированы (`name`, `layer`, `effect`, кнопка `evidence`); связи не рисуются; выбор строки = выбор узла; переключатель видов не рисуется; `header.view_primary` и `views` не заполняются;
- для `medium: graph`: `computeDAGLayout` (узлы, стрелки). Полосы — дорожки по полю `layer` узлов: узлы одного слоя в одной полосе независимо от уровня раскладки. Координаты считает панель. Прямоугольник полосы — объемлющая рамка координат узлов этого слоя (с отступом). Порядок слоёв — по первому появлению в списке узлов. Рамки рангов раскладки (`layout.ranks`) подписями полос **не** являются;
- если полоса подписана, подпись — имя слоя её узлов; подпись рангом и подпись слоем первого узла ранга **запрещены**; смешанный ряд без однородного слоя не подписывать;
- для карт длиннее двенадцати узлов та же раскладка работает как запасная и отличается только тем, что полосы остаются без подписей; запасная раскладка **не** бюджет разборчивости и **не** выдаётся за читаемость в ширине панели;
- если рамки двух полос пересекаются — заливку полос не рисовать, оставить имя слоя рядом со своими узлами;
- переключатель видов меняет раскладку графа (направление или группировку), не состав рёбер; поле режимов подсветки в шаблоне **нет**;
- выбор узла или строки показывает эффект и доказательство в панели деталей; файл открывается **кнопкой** этой панели через `openFile`; `newComposerChat` **не** вызывать;
- стартово выбирать `header.focus_node` — носителя исхода или виновника (если такого id нет — первый узел);
- заголовок (`header.question`) не длиннее двенадцати слов; подпись ребра не длиннее четырёх слов (длинное — в панели деталей); литеральные кавычки кода в текстах панели запрещены;
- живой переключатель «скрыть шапку»: заголовок и абзац вывода скрываются, полотно и детали узла остаются;
- у каждой связи графа — маркер направления; цвет и пунктир по `relation`; легенда только фактически использованных типов **под** графом; обратное ребро раскладки — изгибом или маркером, **не** пунктиром (пунктир занят типом связи);
- аннотации рисовать у якорного узла или ребра с видимым доказательством и подсветкой зоны якоря; не в правой полосе за пределами графа и не колонкой карточек; координаты аннотации из манифеста **не** читать; якорь: `{ node: id }` либо `{ edge: { from, to } }`;
- полотно графа **не** масштабировать целиком под ширину панели (`maxWidth: 100%` на широком DAG запрещён); рисовать в натуральных размерах внутри контейнера с горизонтальной прокруткой; цепочку длиннее пяти узлов в одном ряду переносить на следующий ряд той же раскладки;
- в шапку переносить `question`, `insight`, `sources`, `medium`, `focus_node`; для графа — `view_primary`; у узла — `name`, `state` если есть; у связи — `label` и `relation` (не сырой `id` как единственная подпись);
- файл панели должен проходить проверку типов носителя: `key` ставить только на нативные элементы (`span`, `g`), не на `Button` / `Row` / `Text`; якорь аннотации сначала копировать в локальную переменную, затем читать поля — иначе проверка записи нечистая и среда не показывает кнопку.

```tsx
import {
  Button,
  H1,
  Row,
  Stack,
  Table,
  Text,
  Toggle,
  computeDAGLayout,
  useCanvasAction,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type NodeId = string;
type ViewType = "causal-flow" | "layers";
type Medium = "graph" | "table";
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

type MapAnnotation = {
  text: string;
  evidence_ref: string;
  anchor: { node: NodeId } | { edge: { from: NodeId; to: NodeId } };
};

type Placed = { id: string; x: number; y: number };

const HEADER = {
  question: "<header.question>",
  insight: "<header.insight>",
  sources: ["<header.sources>"],
  medium: "graph" as Medium,
  view_primary: "causal-flow" as ViewType,
  focus_node: "<header.focus_node>" as NodeId,
};

const NODES: MapNode[] = [
  /* манифест.nodes */
];

const EDGES: MapEdge[] = [
  /* манифест.edges */
];

const ANNOTATIONS: MapAnnotation[] = [
  /* манифест.annotations */
];

const NODE_W = 180;
const NODE_H = 56;
const BAND_PAD = 12;
const MAX_ROW = 5;
const ROW_GAP = 28;
const PAD = 24;

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

type Band = {
  layer: string;
  x: number;
  y: number;
  width: number;
  height: number;
  nodeIds: string[];
  homogeneous: boolean;
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

function rowLayers(placed: Placed[], nodes: MapNode[], y: number) {
  const layers = new Set<string>();
  for (const item of placed) {
    if (item.y !== y) continue;
    const meta = nodes.find((node) => node.id === item.id);
    if (meta) layers.add(meta.layer);
  }
  return layers;
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
    const mixedRow = items.some(
      (item) => rowLayers(placed, nodes, item.y).size > 1,
    );
    bands.push({
      layer,
      x: minX,
      y: minY,
      width: maxX - minX,
      height: maxY - minY,
      nodeIds: items.map((item) => item.id),
      homogeneous: !mixedRow,
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

function wrapLayout(
  raw: ReturnType<typeof computeDAGLayout>,
) {
  const nodes = raw.nodes.map((node) => ({ ...node }));
  const ranks = Array.from(new Set(nodes.map((node) => node.rank))).sort(
    (a, b) => a - b,
  );
  let extra = 0;
  for (const rank of ranks) {
    const group = nodes
      .filter((node) => node.rank === rank)
      .sort((a, b) => a.order - b.order);
    if (group.length === 0) continue;
    if (group.length <= MAX_ROW) {
      for (const node of group) node.y += extra;
      continue;
    }
    const originY = group[0].y + extra;
    const rows = Math.ceil(group.length / MAX_ROW);
    for (let i = 0; i < group.length; i++) {
      const row = Math.floor(i / MAX_ROW);
      const col = i % MAX_ROW;
      group[i].x = PAD + col * (NODE_W + ROW_GAP);
      group[i].y = originY + row * (NODE_H + ROW_GAP);
    }
    extra += (rows - 1) * (NODE_H + ROW_GAP);
  }
  const byId = new Map(nodes.map((node) => [node.id, node]));
  const horizontal = raw.direction === "horizontal";
  const edges = raw.edges.map((edge) => {
    const from = byId.get(edge.from);
    const to = byId.get(edge.to);
    if (!from || !to) return edge;
    const sourceX = horizontal ? from.x + NODE_W : from.x + NODE_W / 2;
    const sourceY = horizontal ? from.y + NODE_H / 2 : from.y + NODE_H;
    const targetX = horizontal ? to.x : to.x + NODE_W / 2;
    const targetY = horizontal ? to.y + NODE_H / 2 : to.y;
    const isBackEdge = horizontal
      ? to.x + NODE_W / 2 < from.x
      : to.y + NODE_H / 2 < from.y;
    return { ...edge, sourceX, sourceY, targetX, targetY, isBackEdge };
  });
  const width =
    Math.max(PAD * 2, ...nodes.map((node) => node.x + NODE_W + PAD));
  const height =
    Math.max(PAD * 2, ...nodes.map((node) => node.y + NODE_H + PAD));
  return { nodes, edges, width, height };
}

function annotationBox(
  point: { x: number; y: number },
  index: number,
) {
  const w = 168;
  const h = 42;
  let x = point.x + 16;
  let y = point.y - h - 10 + index * 2;
  if (y < 4) y = point.y + 18;
  return { x, y, w, h };
}

export default function ScenarioMap() {
  const theme = useHostTheme();
  const dispatch = useCanvasAction();
  const medium: Medium = HEADER.medium === "table" ? "table" : "graph";
  const [view, setView] = useCanvasState<ViewType>("view", HEADER.view_primary);
  const [selected, setSelected] = useCanvasState<NodeId | null>(
    "selected",
    resolveFocus(),
  );
  const [hideHeader, setHideHeader] = useCanvasState<boolean>(
    "hideHeader",
    false,
  );

  const selectedNode = NODES.find((node) => node.id === selected);
  const raw =
    medium === "graph"
      ? computeDAGLayout({
          nodes: NODES.map((node) => ({ id: node.id })),
          edges: EDGES.map((edge) => ({ from: edge.from, to: edge.to })),
          direction: view === "layers" ? "vertical" : "horizontal",
          nodeWidth: NODE_W,
          nodeHeight: NODE_H,
          rankGap: 64,
          nodeGap: 28,
          padding: PAD,
        })
      : null;
  const layout = raw ? wrapLayout(raw) : null;
  const bands = layout ? computeLayerBands(layout.nodes, NODES) : [];
  const overlap = bandsOverlap(bands);
  const labelBands = NODES.length <= 12;
  const usedRelations = Array.from(new Set(EDGES.map((edge) => edge.relation)));
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

  function anchorPoint(annotation: MapAnnotation) {
    const anchor = annotation.anchor;
    if (!layout) return null;
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

  let svgWidth = layout?.width ?? 0;
  let svgHeight = layout?.height ?? 0;
  if (layout) {
    ANNOTATIONS.forEach((annotation, index) => {
      const point = anchorPoint(annotation);
      if (!point) return;
      const box = annotationBox(point, index);
      svgWidth = Math.max(svgWidth, box.x + box.w + 8);
      svgHeight = Math.max(svgHeight, box.y + box.h + 8);
    });
  }

  const tableRows = NODES.map((node) => {
    const trap = ANNOTATIONS.some((annotation) => {
      const anchor = annotation.anchor;
      return "node" in anchor && anchor.node === node.id;
    });
    const nameCell = (
      <span>
        <Button
          variant={selected === node.id ? "primary" : "secondary"}
          onClick={() => setSelected(node.id)}
        >
          {node.name}
        </Button>
      </span>
    );
    const evidenceCell = (
      <span>
        <Button onClick={() => openEvidence(node)}>Доказательство</Button>
      </span>
    );
    return {
      cells: [nameCell, node.layer, node.effect, evidenceCell],
      tone: trap
        ? ("warning" as const)
        : selected === node.id
          ? ("info" as const)
          : undefined,
    };
  });

  return (
    <Stack gap={16}>
      <Row gap={8}>
        <Text>Скрыть шапку</Text>
        <Toggle checked={hideHeader} onChange={setHideHeader} />
      </Row>
      {hideHeader ? null : (
        <Stack gap={8}>
          <H1>{HEADER.question}</H1>
          <Text tone="secondary">{HEADER.insight}</Text>
          <Text tone="tertiary">{HEADER.sources.join(" · ")}</Text>
        </Stack>
      )}
      {medium === "graph" ? (
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
      ) : null}
      {medium === "table" ? (
        <Table
          headers={["Сущность", "Условие или слой", "Что происходит", "Доказательство"]}
          rows={tableRows.map((row) => row.cells)}
          rowTone={tableRows.map((row) => row.tone)}
          framed
          striped
        />
      ) : null}
      {medium === "graph" && layout ? (
        <div style={{ overflowX: "auto", width: "100%" }}>
          <svg
            width={svgWidth}
            height={svgHeight}
            viewBox={`0 0 ${svgWidth} ${svgHeight}`}
            role="img"
            aria-label={HEADER.question}
            style={{ display: "block" }}
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
                {labelBands && band.homogeneous ? (
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
                  />
                  {meta ? (
                    <text
                      x={midX}
                      y={midY - 8}
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
              const trap = ANNOTATIONS.some((annotation) => {
                const anchor = annotation.anchor;
                return "node" in anchor && anchor.node === placed.id;
              });
              return (
                <g
                  key={`node-${placed.id}`}
                  onClick={() => setSelected(node.id)}
                  style={{ cursor: "pointer" }}
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
              const box = annotationBox(point, index);
              return (
                <g key={`anno-${index}`}>
                  <line
                    x1={point.x}
                    y1={point.y}
                    x2={box.x}
                    y2={box.y + box.h / 2}
                    stroke={theme.accent.primary}
                    strokeWidth={1.2}
                  />
                  <rect
                    x={box.x}
                    y={box.y}
                    width={box.w}
                    height={box.h}
                    rx={6}
                    fill={theme.bg.elevated}
                    stroke={theme.accent.primary}
                  />
                  <text
                    x={box.x + 8}
                    y={box.y + 16}
                    fill={theme.text.primary}
                    fontSize={11}
                  >
                    {annotation.text}
                  </text>
                  <text
                    x={box.x + 8}
                    y={box.y + 32}
                    fill={theme.text.tertiary}
                    fontSize={9}
                  >
                    {annotation.evidence_ref}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>
      ) : null}
      {medium === "graph" && usedRelations.length > 0 ? (
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
      {medium === "table"
        ? ANNOTATIONS.filter((annotation) => {
            const anchor = annotation.anchor;
            return "node" in anchor && anchor.node === selected;
          }).map((annotation, index) => (
            <span key={`table-anno-${index}`}>
              <Text>
                {annotation.text} · {annotation.evidence_ref}
              </Text>
            </span>
          ))
        : null}
      {selectedNode ? (
        <Stack gap={8}>
          <Text>{selectedNode.effect}</Text>
          {medium === "graph"
            ? incident.map((edge) => (
                <span key={`${edge.from}-${edge.to}`}>
                  <Text tone="secondary">
                    {edge.label} · {paint(edge.relation).title} ·{" "}
                    {edge.evidence_ref}
                  </Text>
                </span>
              ))
            : null}
          <Button onClick={() => openEvidence(selectedNode)}>
            Открыть доказательство
          </Button>
        </Stack>
      ) : null}
    </Stack>
  );
}
```
