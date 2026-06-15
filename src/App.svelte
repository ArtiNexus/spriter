<script lang="ts">
  import Upload from "./lib/components/Upload.svelte";
  import Actions from "./lib/components/Actions.svelte";
  import Generate from "./lib/components/Generate.svelte";
  import Timeline from "./lib/components/Timeline.svelte";
  import Export from "./lib/components/Export.svelte";

  const steps = ["上传", "动作", "生成", "时间轴", "导出"];
  let current = $state(0);

  function next() { if (current < steps.length - 1) current++; }
  function prev() { if (current > 0) current--; }
</script>

<div class="app">
  <nav class="stepper">
    {#each steps as step, i}
      <button class="step" class:active={i === current} class:done={i < current}
              onclick={() => current = i} disabled={i > current && i > 0}>
        {i + 1}. {step}
      </button>
    {/each}
  </nav>

  <main class="content">
    {#if current === 0}<Upload />
    {:else if current === 1}<Actions />
    {:else if current === 2}<Generate />
    {:else if current === 3}<Timeline />
    {:else if current === 4}<Export />
    {/if}
  </main>

  <footer class="footer">
    <button onclick={prev} disabled={current === 0}>上一步</button>
    <span class="step-indicator">{current + 1} / {steps.length}</span>
    <button onclick={next} disabled={current === steps.length - 1}>下一步</button>
  </footer>
</div>

<style>
  .app { display: flex; flex-direction: column; height: 100vh; }
  .stepper { display: flex; gap: 4px; padding: 12px; background: var(--surface); border-bottom: 1px solid var(--border); }
  .step { flex:1; background: transparent; color: var(--muted); border: 1px solid var(--border); }
  .step.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  .step.done { color: var(--success); border-color: var(--success); }
  .content { flex:1; overflow: auto; padding: 24px; }
  .footer { display: flex; justify-content: space-between; align-items: center; padding: 12px 24px; background: var(--surface); border-top: 1px solid var(--border); }
  .step-indicator { color: var(--muted); font-size: 13px; }
</style>
