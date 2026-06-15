<script lang="ts">
  let running = $state(false);
  let percent = $state(0);
  let currentStep = $state("");
  let steps = $state([
    { id: "preprocess", label: "提取主体", done: false },
    { id: "generate", label: "生成动作视频", done: false },
    { id: "extract", label: "拆帧", done: false },
    { id: "refine", label: "透明背景抠图", done: false },
    { id: "assemble", label: "拼接精灵图", done: false },
    { id: "package", label: "打包", done: false },
  ]);
  let error = $state("");

  async function start() {
    running = true; error = ""; percent = 0;
    // 模拟流程（后续接入真实 Pipeline）
    for (let i = 0; i < steps.length; i++) {
      currentStep = steps[i].id;
      for (let p = 0; p <= 100; p += 5) {
        percent = Math.round((i * 100 + p) / steps.length);
        await new Promise(r => setTimeout(r, 100));
      }
      steps[i].done = true;
    }
    running = false;
  }
</script>

<div class="generate">
  <h2>生成精灵图</h2>
  {#if error}
    <div class="error">{error}<button onclick={() => error = ""}>重试</button></div>
  {/if}

  <div class="progress-section">
    <div class="progress-bar">
      <div class="progress-fill" style="width:{percent}%"></div>
    </div>
    <p class="percent">{percent}% — {currentStep || "等待开始"}</p>
  </div>

  <div class="step-list">
    {#each steps as s}
      <div class="step-item" class:done={s.done} class:active={currentStep === s.id}>
        {s.done ? "✅" : currentStep === s.id ? "⏳" : "⬜"} {s.label}
      </div>
    {/each}
  </div>

  <button onclick={start} disabled={running}>
    {running ? "生成中..." : "🚀 开始生成"}
  </button>
</div>

<style>
  .generate { max-width: 400px; margin: 0 auto; }
  .error { background: rgba(248,81,73,0.1); border: 1px solid var(--danger); border-radius: 8px; padding: 12px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
  .progress-section { margin: 24px 0 16px; }
  .progress-bar { height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
  .progress-fill { height: 100%; background: var(--accent); transition: width 0.3s; border-radius: 4px; }
  .percent { text-align: center; color: var(--muted); margin-top: 8px; font-size: 13px; }
  .step-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 24px; }
  .step-item { padding: 8px 12px; border-radius: 6px; font-size: 14px; color: var(--muted); }
  .step-item.active { color: var(--accent); background: rgba(88,166,255,0.05); }
  .step-item.done { color: var(--success); }
</style>
