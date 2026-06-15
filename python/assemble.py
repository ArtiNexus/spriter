"""S05: 拼接水平 Sprite Sheet"""
from PIL import Image
from pathlib import Path

def assemble_sheet(frame_dir: Path, output_dir: Path, cell_size: int) -> str:
    frames = sorted(frame_dir.glob("frame_*.png"))
    if not frames:
        raise ValueError("没有帧可拼接")

    total_width = len(frames) * cell_size
    sheet = Image.new("RGBA", (total_width, cell_size), (0, 0, 0, 0))

    for i, f in enumerate(frames):
        img = Image.open(f).convert("RGBA")
        img = img.resize((cell_size, cell_size), Image.LANCZOS)
        sheet.paste(img, (i * cell_size, 0))

    out_path = output_dir / "sprite.png"
    sheet.save(out_path)
    return str(out_path)
