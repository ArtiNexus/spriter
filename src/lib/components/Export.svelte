<script lang="ts">
  import { pipeline } from "../stores/pipeline.svelte";
  import { save } from "@tauri-apps/plugin-dialog";
  import { writeFile } from "@tauri-apps/plugin-fs";

  let config = $state("");
  let saving = $state(false);

  function loadConfig() {
    const cfg = (window as any).__spriteConfig;
    if (cfg) config = JSON.stringify(cfg, null, 2);
  }

  async function download() {
    if (!pipeline.zipPath) return;
    saving = true;
    try {
      const path = await save({
        defaultPath: "spriter_output.zip",
        filters: [{ name: "ZIP", extensions: ["zip"] }]
      });
      if (path) {
        // 读取ZIP内容并写入选择的位置
        const resp = await fetch(`file://${pipeline.zipPath}`);
        const buf = await resp.arrayBuffer();
        await writeFile(path, new Uint8Array(buf));
      }
    } catch (e) {
      console.error(e);
    }
    saving = false;
  }
</script>

<div class="export">
  <h2>预览与导出</h2>

  {#if pipeline.zipPath}
    <div class="done-box">
      <p>✅ 精灵图生成完成</p>
      <button onclick={download} disabled={saving}>
        {saving ? "保存中..." : "💾 保存 ZIP"}
      </button>
    </div>
  {:else}
    <p class="hint">完成时间轴编辑后回到"生成"页点"开始生成"</p>
  {/if}

  <button onclick={loadConfig} class="secondary">📋 查看 config.json</button>

  {#if config}
    <pre class="config-preview">{config}</pre>
  {/if}
</div>

<style>
  .export { max-width: 500px; margin: 0 auto; }
  .done-box { background: rgba(63,185,80,0.1); border: 1px solid var(--success); border-radius: 8px; padding: 16px; margin: 16px 0; display: flex; justify-content: space-between; align-items: center; }
  .hint { color: var(--muted); }
  .secondary { background: transparent; border: 1px solid var(--border); color: var(--text); margin-top: 12px; display: block; }
  .config-preview { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; margin-top: 12px; font-size: 12px; overflow: auto; max-height: 300px; white-space: pre-wrap; }
</style>
