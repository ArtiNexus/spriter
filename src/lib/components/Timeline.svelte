<script lang="ts">
  import { pipeline } from "../stores/pipeline.svelte";
  import { onMount } from "svelte";

  let canvas: HTMLCanvasElement;
  let container: HTMLDivElement;
  let scrollX = $state(0);
  let dragging = $state<number | null>(null);  // 正在拖动的切割线 index
  let cuts = $state<number[]>([24, 48, 72, 96]);  // 默认4个切割点(5段)
  let labels = $state(["idle", "listening", "thinking", "speaking", "error"]);
  let deleted = $state(new Set<number>());
  let totalFrames = $state(120);
  let hoverFrame = $state<number | null>(null);

  const CELL = 60, GAP = 2, HEADER_H = 24;

  function frameCount(): number {
    return totalFrames - deleted.size;
  }

  function effectiveIndex(raw: number): number {
    let skip = 0;
    for (let i = 0; i <= raw; i++) if (deleted.has(i)) skip++;
    return raw - skip;
  }

  function draw() {
    const ctx = canvas.getContext("2d")!;
    const w = totalFrames * (CELL + GAP);
    canvas.width = w;
    canvas.height = CELL + HEADER_H + 30;

    ctx.clearRect(0, 0, w, canvas.height);

    // 段标签
    const segs = [-1, ...cuts, totalFrames - 1];
    for (let s = 0; s < segs.length - 1; s++) {
      const start = segs[s] + 1;
      const end = segs[s + 1];
      const cx = start * (CELL + GAP) + (end - start + 1) * (CELL + GAP) / 2;
      ctx.fillStyle = "#8b949e";
      ctx.font = "11px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(labels[s] || `段${s+1}`, cx, 14);
    }

    // 帧块
    for (let i = 0; i < totalFrames; i++) {
      if (deleted.has(i)) continue;
      const x = i * (CELL + GAP);
      const y = HEADER_H;

      if (hoverFrame === i) {
        ctx.strokeStyle = "#58a6ff";
        ctx.lineWidth = 2;
        ctx.strokeRect(x - 1, y - 1, CELL + 2, CELL + 2);
      }

      ctx.fillStyle = `hsl(${(i * 7) % 360}, 40%, 25%)`;
      ctx.fillRect(x, y, CELL, CELL);
      ctx.fillStyle = "#e6edf3";
      ctx.font = "10px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(`${i}`, x + CELL / 2, y + CELL / 2 + 4);

      ctx.strokeStyle = i % 12 === 0 ? "#58a6ff" : "#30363d";
      ctx.lineWidth = 1;
      ctx.strokeRect(x, y, CELL, CELL);
    }

    // 切割线
    for (let c = 0; c < cuts.length; c++) {
      const x = (cuts[c] + 1) * (CELL + GAP) - GAP / 2;
      ctx.strokeStyle = "#f85149";
      ctx.lineWidth = dragging === c ? 4 : 3;
      ctx.beginPath();
      ctx.moveTo(x, HEADER_H);
      ctx.lineTo(x, HEADER_H + CELL);
      ctx.stroke();

      // 拖拽手柄
      ctx.fillStyle = "#f85149";
      ctx.beginPath();
      ctx.arc(x, HEADER_H + CELL / 2, 6, 0, Math.PI * 2);
      ctx.fill();
    }

    // 滚动同步
    container.scrollLeft = scrollX;
  }

  function handleMouseDown(e: MouseEvent) {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left + scrollX;

    // 检测是否点在切割线上
    for (let c = 0; c < cuts.length; c++) {
      const cx = (cuts[c] + 1) * (CELL + GAP) - GAP / 2;
      if (Math.abs(mx - cx) < 10) {
        dragging = c;
        e.preventDefault();
        return;
      }
    }

    // 检测是否点在帧上（删除废帧）
    const fi = Math.floor(mx / (CELL + GAP));
    if (fi >= 0 && fi < totalFrames) {
      if (e.shiftKey) {
        if (deleted.has(fi)) {
          deleted.delete(fi);
        } else {
          deleted.add(fi);
        }
        deleted = new Set(deleted); // 触发响应式
        draw();
      }
    }
  }

  function handleMouseMove(e: MouseEvent) {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left + scrollX;

    if (dragging !== null) {
      const fi = Math.round(mx / (CELL + GAP));
      const clamped = Math.max(1, Math.min(totalFrames - 2, fi));
      // 不能越过相邻切割线
      const prev = dragging > 0 ? cuts[dragging - 1] + 1 : 1;
      const next = dragging < cuts.length - 1 ? cuts[dragging + 1] - 1 : totalFrames - 2;
      cuts[dragging] = Math.max(prev, Math.min(next, clamped));
      cuts = [...cuts];  // 触发响应式
      draw();
    }

    hoverFrame = Math.floor(mx / (CELL + GAP));
  }

  function handleMouseUp() {
    dragging = null;
    updateConfig();
  }

  function addCut() {
    // 在最长的段中间加切割
    const segs = [-1, ...cuts, totalFrames - 1];
    let maxLen = 0, maxIdx = 0;
    for (let i = 0; i < segs.length - 1; i++) {
      const len = segs[i+1] - segs[i];
      if (len > maxLen) { maxLen = len; maxIdx = i; }
    }
    const mid = Math.floor((segs[maxIdx] + segs[maxIdx+1]) / 2);
    cuts = [...cuts.slice(0, maxIdx), mid, ...cuts.slice(maxIdx)].sort((a,b) => a-b);
    labels = [...labels.slice(0, maxIdx+1), `段${maxIdx+2}`, ...labels.slice(maxIdx+1)];
    draw();
    updateConfig();
  }

  function updateConfig() {
    const segs = [-1, ...cuts, totalFrames - 1];
    const config: any = { name: "character", size: 256, actions: {} };
    for (let s = 0; s < segs.length - 1; s++) {
      config.actions[labels[s] || `segment_${s}`] = {
        start: segs[s] + 1,
        end: segs[s + 1],
        fps: 12,
      };
    }
    // 存到 window 供导出页读取
    (window as any).__spriteConfig = config;
  }

  function handleScroll() {
    scrollX = container.scrollLeft;
  }

  $effect(() => {
    if (canvas) draw();
  });

  onMount(() => {
    draw();
    updateConfig();
  });
</script>

<div class="timeline">
  <div class="toolbar">
    <h2>时间轴编辑器</h2>
    <span class="info">
      {totalFrames} 帧 | {deleted.size} 已删 | {cuts.length + 1} 段
      <span class="tip">(Shift+点击删除/恢复帧 | 拖拽红线切分)</span>
    </span>
    <button onclick={addCut}>+ 添加切割</button>
    <button class="reset" onclick={() => { cuts = []; labels = ["全部"]; deleted = new Set(); draw(); updateConfig(); }}>重置</button>
  </div>

  <div class="labels-row">
    {#each labels as lbl, i}
      <input
        type="text"
        value={lbl}
        oninput={(e) => { labels[i] = (e.target as HTMLInputElement).value; labels = [...labels]; updateConfig(); }}
        class="seg-label"
      />
    {/each}
  </div>

  <div class="scroll" bind:this={container} onscroll={handleScroll}>
    <canvas
      bind:this={canvas}
      onmousedown={handleMouseDown}
      onmousemove={handleMouseMove}
      onmouseup={handleMouseUp}
      onmouseleave={() => { dragging = null; hoverFrame = null; draw(); }}
      style="cursor: crosshair"
    ></canvas>
  </div>
</div>

<style>
  .timeline { display: flex; flex-direction: column; height: 100%; }
  .toolbar { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; flex-wrap: wrap; }
  .toolbar h2 { margin: 0; font-size: 16px; }
  .info { color: var(--muted); font-size: 12px; flex: 1; }
  .tip { opacity: 0.6; margin-left: 8px; }
  .reset { background: transparent; border: 1px solid var(--border); color: var(--muted); }
  .labels-row { display: flex; gap: 4px; margin-bottom: 8px; flex-wrap: wrap; }
  .seg-label { width: 100px !important; font-size: 12px; padding: 4px 8px !important; }
  .scroll { flex: 1; overflow-x: auto; overflow-y: hidden; border: 1px solid var(--border); border-radius: 8px; background: #0d1117; }
  canvas { display: block; }
</style>
