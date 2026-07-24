#!/usr/bin/env python3
from pathlib import Path
import runpy
import sys

script_path = Path(__file__).resolve().parent / "web-tool" / "web_click_tool.py"
if not script_path.exists():
    raise SystemExit(f"找不到脚本文件: {script_path}")

sys.path.insert(0, str(script_path.parent))
runpy.run_path(str(script_path), run_name="__main__")

