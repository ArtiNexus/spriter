<script lang="ts">
  let ready = $state(false);
</script>

<div class="export">
  <h2>预览与导出</h2>
  {#if !ready}
    <div class="placeholder">
      <p>📦 完成时间轴编辑后，这里显示 GIF 预览和下载</p>
    </div>
  {:else}
    <!-- GIF 预览 + 下载按钮 Phase 4 实现 -->
  {/if}
</div>

<style>
  .export { max-width: 400px; margin: 0 auto; }
  .placeholder { text-align: center; padding: 60px 20px; color: var(--muted); }
</style>
