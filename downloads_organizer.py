#!/usr/bin/env python3
"""
Downloads Auto Organizer
"I hate cleaning my Downloads folder, so I automated it."

This script:
- Scans your Downloads folder
- Detects file types by extension
- Creates category folders (Images, PDFs, Docs, etc.)
- Moves files into the right folder
- Avoids name conflicts by renaming safely
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# ---- 1. BASIC CONFIG ----

# By default, use the current user's Downloads folder
DEFAULT_DOWNLOADS_DIR = Path.home() / "Downloads"

# Map extensions to folder names
EXTENSION_MAP = {
    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",
    ".svg": "Images",
    ".heic": "Images",

    # Documents
    ".txt": "Documents",
    ".md": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".rtf": "Documents",

    # PDFs
    ".pdf": "PDFs",

    # Spreadsheets
    ".xls": "Spreadsheets",
    ".xlsx": "Spreadsheets",
    ".csv": "Spreadsheets",

    # Presentations
    ".ppt": "Presentations",
    ".pptx": "Presentations",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".m4a": "Audio",
    ".flac": "Audio",

    # Video
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".webm": "Videos",

    # Code files
    ".py": "Code",
    ".c": "Code",
    ".cpp": "Code",
    ".java": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".html": "Code",
    ".css": "Code",
    ".json": "Code",
}


def get_category_for_extension(ext: str) -> str:
    """
    Return folder category based on file extension.
    Unknown extensions go to 'Others'.
    """
    ext = ext.lower()
    return EXTENSION_MAP.get(ext, "Others")


def safe_move(src: Path, dst: Path) -> Path:
    """
    Move file from src to dst.
    If a file with the same name exists at dst, append a counter.
    Returns the final destination path.
    """
    dst_parent = dst.parent
    dst_parent.mkdir(parents=True, exist_ok=True)

    if not dst.exists():
        shutil.move(str(src), str(dst))
        return dst

    # Name conflict: add (1), (2), etc.
    stem = dst.stem
    suffix = dst.suffix
    counter = 1

    while True:
        new_name = f"{stem} ({counter}){suffix}"
        new_dst = dst_parent / new_name
        if not new_dst.exists():
            shutil.move(str(src), str(new_dst))
            return new_dst
        counter += 1


def organize_downloads(downloads_dir: Path = DEFAULT_DOWNLOADS_DIR) -> None:
    """
    Main function: organize files inside the given downloads_dir.
    """
    if not downloads_dir.exists():
        print(f"❌ Downloads folder not found: {downloads_dir}")
        return

    # Path of this script (so we don't move it accidentally)
    script_path = Path(__file__).resolve()

    print("📂 Downloads Organizer")
    print(f"🔎 Scanning: {downloads_dir}\n")

    moved_files_count = 0

    for item in downloads_dir.iterdir():
        # Skip directories
        if item.is_dir():
            continue

        # Skip hidden files like .DS_Store
        if item.name.startswith("."):
            continue

        # Skip the script itself, in case it's inside Downloads
        if item.resolve() == script_path:
            continue

        ext = item.suffix
        category = get_category_for_extension(ext)

        target_folder = downloads_dir / category
        target_path = target_folder / item.name

        final_path = safe_move(item, target_path)
        moved_files_count += 1

        print(f"➡️  {item.name}  →  {category}/ (saved as: {final_path.name})")

    if moved_files_count == 0:
        print("\n✨ Nothing to organize. Your Downloads is already clean!")
    else:
        print(f"\n✅ Done! Organized {moved_files_count} file(s).")
        print(f"📁 Check inside: {downloads_dir}")


if __name__ == "__main__":
    print("🧹 Starting Downloads Auto Organizer...\n")
    print(f"🕒 Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📍 Using Downloads folder: {DEFAULT_DOWNLOADS_DIR}\n")
    organize_downloads()
    print("\n🎉 Finished!")
