"""M: ZIP 打包"""
import zipfile
from pathlib import Path

def create_zip(output_dir: Path, name: str) -> str:
    zip_path = output_dir / f"{name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in output_dir.glob("*"):
            if f.name.endswith(".zip"):
                continue
            zf.write(f, f.name)
    return str(zip_path)
