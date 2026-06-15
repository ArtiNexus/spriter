"""S01: 提取主体 + 缩放"""
from PIL import Image
from pathlib import Path
import subprocess, shutil as _shutil

def preprocess(image_path: str, work_dir: Path, target_size: int) -> str:
    img = Image.open(image_path).convert("RGBA")
    img.thumbnail((target_size * 2, target_size * 2), Image.LANCZOS)

    temp_in = work_dir / "input_temp.png"
    temp_out = work_dir / "subject.png"
    img.save(temp_in)

    rembg_bin = _shutil.which("rembg")
    if rembg_bin:
        try:
            subprocess.run(
                [rembg_bin, "i", "-m", "rmbg2", str(temp_in), str(temp_out)],
                check=True, capture_output=True, text=True, timeout=30
            )
        except Exception as e:
            _shutil.copy(temp_in, temp_out)
    else:
        _shutil.copy(temp_in, temp_out)

    result = Image.open(temp_out).convert("RGBA")
    result.thumbnail((target_size, target_size), Image.LANCZOS)
    final = work_dir / "subject_final.png"
    result.save(final)
    return str(final)
