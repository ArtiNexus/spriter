<script lang="ts">
  import { pipeline } from "../stores/pipeline.svelte";
  let dragOver = $state(false);

  function handleDrop(e: DragEvent) {
    e.preventDefault(); dragOver = false;
    const file = e.dataTransfer?.files?.[0];
    if (file) load(file);
  }
  function handleSelect(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) load(file);
  }
  function load(file: File) {
    if (!file.type.startsWith("image/")) { alert("请上传图片"); return; }
    const reader = new FileReader();
    reader.onload = () => {
      pipeline.setImage(file.name, reader.result as string);
    };
    reader.readAsDataURL(file);
  }
</script>

<div class="upload">
  <h2>上传角色形象</h2>
  <p class="hint">拖拽图片到这里，或点击选择</p>
  <div
    class="dropzone"
    class:drag-over={dragOver}
    ondragover={(e) => { e.preventDefault(); dragOver = true; }}
    ondragleave={() => dragOver = false}
    ondrop={handleDrop}
    onclick={() => document.getElementById("fi")?.click()}
  >
    {#if pipeline.imageDataUrl}
      <img src={pipeline.imageDataUrl} alt="" class="preview" />
      <p>{pipeline.imagePath}</p>
    {:else}
      <span class="icon">📁</span><p>拖拽图片到此处</p>
    {/if}
  </div>
  <input id="fi" type="file" accept="image/png,image/jpeg,image/webp" onchange={handleSelect} hidden />
</div>

<style>
  .upload { max-width: 400px; margin: 0 auto; text-align: center; }
  .hint { color: var(--muted); margin: 8px 0 24px; }
  .dropzone { border: 2px dashed var(--border); border-radius: 12px; padding: 40px; cursor: pointer; transition: all 0.2s; }
  .dropzone:hover, .drag-over { border-color: var(--accent); background: rgba(88,166,255,0.05); }
  .icon { font-size: 48px; display: block; margin-bottom: 8px; }
  .preview { max-width: 200px; max-height: 200px; border-radius: 8px; }
</style>
