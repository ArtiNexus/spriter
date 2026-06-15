"""S04: 逐帧透明化"""
import subprocess, shutil, time
from pathlib import Path

def refine_frames(frame_dir: Path) -> int:
    rembg = shutil.which("rembg")
    if not rembg:
        return 0
    # Quick test: can rembg actually run?
    try:
        r = subprocess.run([rembg, "--help"], capture_output=True, timeout=3)
        if r.returncode != 0:
            return 0
    except Exception:
        return 0

    frames = sorted(frame_dir.glob("frame_*.png"))
    count = 0
    deadline = time.time() + 30  # max 30s total
    for f in frames:
        if time.time() > deadline:
            break
        try:
            subprocess.run(
                [rembg, "i", "-m", "rmbg2", str(f), str(f)],
                check=True, capture_output=True, timeout=10
            )
            count += 1
        except Exception:
            pass
    return count
