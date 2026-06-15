<script lang="ts">
  let dragOver = $state(false);
  let preview = $state<string | null>(null);
  let fileName = $state("");

  function handleDrop(e: DragEvent) {
    e.preventDefault(); dragOver = false;
    const file = e.dataTransfer?.files?.[0];
    if (file) loadImage(file);
  }
  function handleSelect(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) loadImage(file);
  }
  function loadImage(file: File) {
    if (!file.type.startsWith("image/")) { alert("请上传图片文件"); return; }
    fileName = file.name;
    const reader = new FileReader();
    reader.onload = () => preview = reader.result as string;
    reader.readAsDataURL(file);
  }
</script>

<div class="upload">
  <h2>上传角色形象</h2>
  <p class="hint">拖拽图片到这里，或点击选择文件</p>
  <div
    class="dropzone"
    class:drag-over={dragOver}
    ondragover={(e) => { e.preventDefault(); dragOver = true; }}
    ondragleave={() => dragOver = false}
    ondrop={handleDrop}
    onclick={() => document.getElementById("file-input")?.click()}
  >
    {#if preview}
      <img src={preview} alt={fileName} class="preview" />
      <p>{fileName}</p>
    {:else}
      <span class="icon">📁</span>
      <p>拖拽图片到此处</p>
    {/if}
  </div>
  <input id="file-input" type="file" accept="image/png,image/jpeg,image/webp" onchange={handleSelect} hidden />
</div>

<style>
  .upload { max-width: 400px; margin: 0 auto; text-align: center; }
  .hint { color: var(--muted); margin: 8px 0 24px; }
  .dropzone {
    border: 2px dashed var(--border); border-radius: 12px; padding: 40px;
    cursor: pointer; transition: all 0.2s;
  }
  .dropzone:hover, .drag-over { border-color: var(--accent); background: rgba(88,166,255,0.05); }
  .icon { font-size: 48px; display: block; margin-bottom: 8px; }
  .preview { max-width: 200px; max-height: 200px; border-radius: 8px; }
</style>
