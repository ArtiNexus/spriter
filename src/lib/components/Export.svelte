<script lang="ts">
  import { pipeline } from "../stores/pipeline.svelte";
  let config = $state("");

  function loadConfig() {
    const cfg = (window as any).__spriteConfig;
    if (cfg) config = JSON.stringify(cfg, null, 2);
  }
</script>

<div class="export">
  <h2>预览与导出</h2>

  {#if pipeline.zipPath}
    <div class="done-box">
      <p>✅ 精灵图生成完成</p>
      <p class="path">{pipeline.zipPath}</p>
    </div>
  {:else}
    <p class="hint">完成时间轴编辑后点"生成"</p>
  {/if}

  <button onclick={loadConfig} class="secondary">📋 查看 config.json</button>

  {#if config}
    <pre class="config-preview">{config}</pre>
  {/if}
</div>

<style>
  .export { max-width: 500px; margin: 0 auto; }
  .done-box { background: rgba(63,185,80,0.1); border: 1px solid var(--success); border-radius: 8px; padding: 16px; margin: 16px 0; }
  .path { font-size: 12px; color: var(--muted); word-break: break-all; margin-top: 4px; }
  .hint { color: var(--muted); }
  .secondary { background: transparent; border: 1px solid var(--border); color: var(--text); margin-top: 12px; }
  .config-preview { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; margin-top: 12px; font-size: 12px; overflow: auto; max-height: 300px; white-space: pre-wrap; }
</style>
