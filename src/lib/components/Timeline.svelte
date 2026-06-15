<script lang="ts">
  let placeholder = $state(true);
</script>

<div class="timeline">
  <h2>时间轴编辑器</h2>
  {#if placeholder}
    <div class="placeholder">
      <p>🎞️ 生成完成后，在这里拖拽切割标记来切分动作段</p>
      <p class="sub">上传图片 → 编辑动作 → 点"开始生成" → 回到这里</p>
    </div>
  {:else}
    <!-- Canvas 时间轴将在 Phase 3 实现 -->
  {/if}
</div>

<style>
  .timeline { max-width: 100%; }
  .placeholder { text-align: center; padding: 60px 20px; color: var(--muted); }
  .sub { font-size: 13px; margin-top: 8px; }
</style>
