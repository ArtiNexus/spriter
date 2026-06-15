<script lang="ts">
  import { pipeline } from "../stores/pipeline.svelte";
</script>

<div class="actions">
  <h2>动作编辑</h2>
  <p class="hint">编辑每个动作的描述，禁用不需要的动作</p>
  <div class="list">
    {#each pipeline.actions as act, i}
      <div class="card" class:disabled={!act.enabled}>
        <div class="card-header">
          <input type="text" bind:value={act.name} placeholder="动作名" class="name-input" />
          <label><input type="checkbox" checked={act.enabled} onchange={() => pipeline.toggleAction(i)} /> 启用</label>
          <button class="del" onclick={() => pipeline.removeAction(i)}>✕</button>
        </div>
        <textarea bind:value={act.prompt} placeholder="描述这个动作..." rows={2}></textarea>
      </div>
    {/each}
  </div>
  <button onclick={() => pipeline.addAction()}>+ 添加动作</button>
</div>

<style>
  .actions { max-width: 500px; margin: 0 auto; }
  .hint { color: var(--muted); margin: 8px 0 20px; }
  .list { display: flex; flex-direction: column; gap: 12px; margin-bottom: 12px; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; }
  .card.disabled { opacity: 0.5; }
  .card-header { display: flex; gap: 8px; align-items: center; margin-bottom: 8px; }
  .name-input { width: 120px !important; }
  .del { background: transparent; color: var(--danger); font-size: 16px; padding: 2px 8px; }
  label { font-size: 13px; color: var(--muted); white-space: nowrap; display: flex; align-items: center; gap: 4px; }
</style>
