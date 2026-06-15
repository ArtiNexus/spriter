<script lang="ts">
  import { pipeline } from "../stores/pipeline.svelte";
</script>

<div class="generate">
  <h2>生成精灵图</h2>

  {#if pipeline.error}
    <div class="error-msg">
      <span>{pipeline.error}</span>
      <button onclick={() => pipeline.run()}>重试</button>
    </div>
  {/if}

  <div class="summary">
    <p>图片: {pipeline.imagePath || "未上传"}</p>
    <p>动作: {pipeline.actions.filter(a => a.enabled).length} 个</p>
  </div>

  <div class="progress-section">
    <div class="progress-bar">
      <div class="progress-fill" style="width:{pipeline.percent}%"></div>
    </div>
    <p class="percent">
      {pipeline.running ? `${pipeline.percent}% — ${pipeline.currentMessage}` : pipeline.percent === 100 ? "✅ 完成" : "等待开始"}
    </p>
  </div>

  <button onclick={() => pipeline.run()} disabled={pipeline.running || !pipeline.imagePath}>
    {pipeline.running ? "生成中..." : "🚀 开始生成"}
  </button>
</div>

<style>
  .generate { max-width: 400px; margin: 0 auto; }
  .error-msg { background: rgba(248,81,73,0.1); border: 1px solid var(--danger); border-radius: 8px; padding: 12px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
  .summary { display: flex; gap: 24px; margin-bottom: 24px; color: var(--muted); font-size: 14px; }
  .progress-section { margin-bottom: 24px; }
  .progress-bar { height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
  .progress-fill { height: 100%; background: var(--accent); transition: width 0.3s; border-radius: 4px; }
  .percent { text-align: center; color: var(--muted); margin-top: 8px; font-size: 13px; }
</style>
