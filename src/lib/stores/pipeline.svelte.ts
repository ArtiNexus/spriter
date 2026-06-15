import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";

export type Step = "upload" | "actions" | "generate" | "timeline" | "export";

export interface ActionItem {
  name: string;
  prompt: string;
  enabled: boolean;
}

export interface PipelineSettings {
  api_provider: string;
  api_key: string;
  api_url?: string;
  fps: number;
  frame_size: number;
}

export interface ProgressPayload {
  step: string;
  percent: number;
  message: string;
}

export interface CompletePayload {
  zip_path: string;
  frame_dir: string;
}

function createPipeline() {
  let imagePath = $state("");
  let imageDataUrl = $state("");
  let actions = $state<ActionItem[]>([
    { name: "idle", prompt: "角色自然站立，轻微呼吸起伏", enabled: true },
    { name: "listening", prompt: "角色微笑眨眼，头微微侧倾", enabled: true },
    { name: "thinking", prompt: "角色快速打字，手指敲击键盘", enabled: true },
    { name: "speaking", prompt: "角色嘴巴开合说话", enabled: true },
    { name: "error", prompt: "角色摇头表达否定", enabled: true },
  ]);
  let settings = $state<PipelineSettings>({
    api_provider: "doubao",
    api_key: "",
    fps: 12,
    frame_size: 256,
  });
  let running = $state(false);
  let percent = $state(0);
  let currentMessage = $state("");
  let error = $state("");
  let zipPath = $state("");
  let frameDir = $state("");

  function setImage(path: string, dataUrl: string) {
    imagePath = path;
    imageDataUrl = dataUrl;
  }

  function toggleAction(i: number) {
    actions[i].enabled = !actions[i].enabled;
  }

  function updateAction(i: number, field: keyof ActionItem, val: string | boolean) {
    (actions[i] as any)[field] = val;
  }

  function addAction() {
    actions.push({ name: "new", prompt: "", enabled: true });
  }

  function removeAction(i: number) {
    actions = actions.filter((_, j) => j !== i);
  }

  async function run() {
    running = true;
    error = "";
    percent = 0;

    try {
      const result = await invoke<string>("run_pipeline", {
        params: {
          image_path: imagePath,
          actions: actions.filter(a => a.enabled),
          settings,
        }
      });

      zipPath = result;
      running = false;
    } catch (e: any) {
      error = e?.toString() || "未知错误";
      running = false;
    }
  }

  // 监听进度事件
  listen<ProgressPayload>("pipeline-progress", (e) => {
    percent = e.payload.percent;
    currentMessage = e.payload.message;
  });

  listen<CompletePayload>("pipeline-complete", (e) => {
    zipPath = e.payload.zip_path;
    frameDir = e.payload.frame_dir;
    running = false;
    percent = 100;
  });

  listen<{message: string}>("pipeline-error", (e) => {
    error = e.payload.message;
    running = false;
  });

  return {
    get imagePath() { return imagePath; },
    get imageDataUrl() { return imageDataUrl; },
    get actions() { return actions; },
    get settings() { return settings; },
    get running() { return running; },
    get percent() { return percent; },
    get currentMessage() { return currentMessage; },
    get error() { return error; },
    get zipPath() { return zipPath; },
    get frameDir() { return frameDir; },
    setImage, toggleAction, updateAction, addAction, removeAction, run,
  };
}

export const pipeline = createPipeline();
