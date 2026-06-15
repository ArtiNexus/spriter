<script lang="ts">
  let actions = $state([
    { name: "idle", prompt: "角色自然站立，轻微呼吸起伏，身体不移动", enabled: true },
    { name: "listening", prompt: "角色微笑眨眼，头微微侧倾，表示在听", enabled: true },
    { name: "thinking", prompt: "角色坐在电脑前快速打字，手指敲击键盘", enabled: true },
    { name: "speaking", prompt: "角色嘴巴开合说话，头部轻微晃动", enabled: true },
    { name: "error", prompt: "角色摇头，表达否定或出错了", enabled: true },
  ]);
  function add() { actions = [...actions, { name: "new", prompt: "", enabled: true }]; }
  function remove(i: number) { actions = actions.filter((_, j) => j !== i); }
</script>

<div class="actions">
  <h2>动作编辑</h2>
  <p class="hint">编辑每个动作的描述，禁用不需要的动作</p>
  <div class="list">
    {#each actions as act, i}
      <div class="card" class:disabled={!act.enabled}>
        <div class="card-header">
          <input type="text" bind:value={act.name} placeholder="动作名" class="name-input" />
          <label><input type="checkbox" bind:checked={act.enabled} /> 启用</label>
          <button class="del" onclick={() => remove(i)}>✕</button>
        </div>
        <textarea bind:value={act.prompt} placeholder="描述这个动作..." rows={2}></textarea>
      </div>
    {/each}
  </div>
  <button onclick={add}>+ 添加动作</button>
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
