"""
MabrAIn — File System Tools (Conscience Agent)
All operations run through core.safety.check_path before touching disk.
"""

import os
import shutil
from pathlib import Path
from core.safety import check_path, SafetyError

# --- Tool definitions (Anthropic tool-use format) ---
FILE_TOOLS = [
    {
        "name": "list_files",
        "description": "List files and folders in a directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory path to list."},
                "pattern": {"type": "string", "description": "Optional glob pattern, e.g. '*.pdf'"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "rename_file",
        "description": "Rename or move a file within the same allowed directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Current file path."},
                "destination": {"type": "string", "description": "New file path or name."},
            },
            "required": ["source", "destination"],
        },
    },
    {
        "name": "move_file",
        "description": "Move a file to a different allowed directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source file path."},
                "destination": {"type": "string", "description": "Destination directory or full path."},
            },
            "required": ["source", "destination"],
        },
    },
    {
        "name": "create_folder",
        "description": "Create a new folder (including parent folders).",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path of the folder to create."},
            },
            "required": ["path"],
        },
    },
    {
        "name": "search_files",
        "description": "Search for files matching a name pattern in a directory tree.",
        "input_schema": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "description": "Root directory to search in."},
                "pattern": {"type": "string", "description": "Glob pattern, e.g. '*.docx' or '*rapor*'"},
            },
            "required": ["root", "pattern"],
        },
    },
]


# --- Implementations ---

def list_files(path: str, pattern: str = "*") -> str:
    safe = check_path(path)
    if not safe.is_dir():
        return f"Hata: '{safe}' bir klasör değil."
    items = sorted(safe.glob(pattern))
    if not items:
        return "Klasör boş veya eşleşen dosya yok."
    lines = []
    for item in items:
        prefix = "📁" if item.is_dir() else "📄"
        size = f"  ({item.stat().st_size:,} bytes)" if item.is_file() else ""
        lines.append(f"{prefix} {item.name}{size}")
    return f"{safe}:\n" + "\n".join(lines)


def rename_file(source: str, destination: str) -> str:
    src = check_path(source)
    dst = check_path(destination) if Path(destination).is_absolute() else src.parent / destination
    if not src.exists():
        return f"Hata: '{src}' bulunamadı."
    src.rename(dst)
    return f"✅ '{src.name}' → '{dst.name}' olarak yeniden adlandırıldı."


def move_file(source: str, destination: str) -> str:
    src = check_path(source)
    dst_path = check_path(destination)
    if not src.exists():
        return f"Hata: '{src}' bulunamadı."
    if dst_path.is_dir():
        dst_path = dst_path / src.name
    shutil.move(str(src), str(dst_path))
    return f"✅ '{src.name}' → '{dst_path}' konumuna taşındı."


def create_folder(path: str) -> str:
    safe = check_path(path)
    safe.mkdir(parents=True, exist_ok=True)
    return f"✅ Klasör oluşturuldu: '{safe}'"


def search_files(root: str, pattern: str) -> str:
    safe_root = check_path(root)
    matches = sorted(safe_root.rglob(pattern))
    if not matches:
        return f"'{pattern}' ile eşleşen dosya bulunamadı."
    return "\n".join(str(m) for m in matches[:50])  # cap at 50


def execute_file_tool(name: str, params: dict) -> str:
    dispatch = {
        "list_files": list_files,
        "rename_file": rename_file,
        "move_file": move_file,
        "create_folder": create_folder,
        "search_files": search_files,
    }
    if name not in dispatch:
        return f"Bilinmeyen tool: {name}"
    return dispatch[name](**params)
