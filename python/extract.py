"""S03: FFmpeg 拆帧"""
import subprocess
from pathlib import Path

def extract_frames(video_path: str | None, output_dir: Path) -> int:
    if video_path:
        subprocess.run([
            "ffmpeg", "-i", video_path, "-vf", "fps=12",
            str(output_dir / "frame_%04d.png"), "-y"
        ], check=True, capture_output=True)
    else:
        # 占位：生成测试帧
        from PIL import Image
        for i in range(24):
            img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
            img.save(output_dir / f"frame_{i+1:04d}.png")

    frames = sorted(output_dir.glob("frame_*.png"))
    return len(frames)
