"""Sprite Maker Pipeline — 主入口"""
import sys, json, os, tempfile, shutil
from pathlib import Path
from preprocess import preprocess
from extract import extract_frames
from refine import refine_frames
from assemble import assemble_sheet
from config_gen import generate_config
from package import create_zip

def progress(percent, msg):
    print(f"PROGRESS:{percent}:{msg}", flush=True)

def main():
    params = json.loads(sys.argv[sys.argv.index("--params") + 1])
    image_path = params["image_path"]
    actions = params["actions"]
    settings = params.get("settings", {})
    fps = settings.get("fps", 12)
    frame_size = settings.get("frame_size", 256)

    work_dir = Path(tempfile.mkdtemp(prefix="spriter_"))
    frame_dir = work_dir / "frames"
    output_dir = work_dir / "output"
    frame_dir.mkdir(); output_dir.mkdir()

    try:
        # S01: 预处理
        progress(10, "提取主体...")
        subject_path = preprocess(image_path, work_dir, frame_size)
        progress(25, "预处理完成")

        # S02: 动作生成（占位，后续接入豆包API）
        total_actions = len([a for a in actions if a.get("enabled", True)])
        progress(30, f"准备生成 {total_actions} 个动作视频")

        # S03: 拆帧（从已有视频或占位帧）
        progress(60, "拆帧...")
        frame_count = extract_frames(None, frame_dir)
        progress(65, f"拆帧完成 ({frame_count} 帧)")

        # S04: 精修
        progress(70, "透明背景抠图...")
        refine_frames(frame_dir)
        progress(80, "抠图完成")

        # S05: 拼接
        progress(85, "拼接精灵图...")
        sprite_path = assemble_sheet(frame_dir, output_dir, frame_size)
        progress(90, "拼接完成")

        # S06: 配置生成
        progress(93, "生成配置...")
        config_path = generate_config(actions, frame_count, output_dir)
        progress(96, "配置生成完成")

        # 打包
        progress(98, "打包ZIP...")
        zip_path = create_zip(output_dir, f"spriter_output_{os.path.basename(image_path).split('.')[0]}")
        progress(100, "打包完成")

        print(f"COMPLETE:{zip_path}", flush=True)

    except Exception as e:
        print(f"ERROR:{str(e)}", flush=True)
    finally:
        pass  # 保留临时文件供调试

if __name__ == "__main__":
    main()
