"""S06: 生成 config.json"""
import json
from pathlib import Path

def generate_config(actions: list, total_frames: int, output_dir: Path) -> str:
    frames_per_action = max(4, total_frames // max(1, len(actions)))
    config = {"name": "character", "size": 256, "actions": {}}
    cursor = 0
    for act in actions:
        if not act.get("enabled", True):
            continue
        end = min(cursor + frames_per_action - 1, total_frames - 1)
        config["actions"][act["name"]] = {
            "start": cursor, "end": end,
            "fps": 12 if act["name"] in ("idle", "listening") else 8
        }
        cursor = end + 1

    out_path = output_dir / "config.json"
    out_path.write_text(json.dumps(config, ensure_ascii=False, indent=2))
    return str(out_path)
