# Sprite Maker 🎨

> 一张角色图 → 多个动作 → 桌宠精灵素材包

## 这是什么

Sprite Maker 是一个桌面工具，帮你把一张角色图片变成可动的精灵图（Sprite Sheet），直接给 [Mascot](https://github.com/ArtiNexus/mascot) 桌宠使用。

## 怎么用

1. 打开 App
2. 拖一张角色图到上传区
3. 编辑动作描述（或直接用预设的5个动作）
4. 点"开始生成"
5. 在时间轴上拖拽红线切分帧段，给每段命名
6. 导出 ZIP

## 开发

```bash
pnpm install
pnpm tauri:dev
```

## 架构

```
桌面层: Tauri 2 + Svelte 5
调度层: Rust (std::process::Command → Python)
执行层: Python + rembg + FFmpeg + Pillow
交付层: ZIP (sprite.png + config.json + preview.gif)
```

## 输出格式

```json
{
  "name": "character",
  "size": 256,
  "actions": {
    "idle": {"start": 0, "end": 23, "fps": 12},
    "listening": {"start": 24, "end": 47, "fps": 12}
  }
}
```

MIT
