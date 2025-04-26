from pathlib import Path
from typing import List, Tuple

from src.utils.file_loader import load_file

def scan_repo(
        repo_path: str,
        include_exts: List[str] = None,
        exclude_dirs: List[str] = None
) -> List[Tuple[str, str]]:
    """
    Walks repo_path recursively, reads each file via load_file,
    and returns a list of (relative_path, content) tuples.

    - include_exts: list of file extensions to include (e.g. ['.py', '.js']); None = all.
    - exclude_dirs: list of directory names to skip (e.g. ['.git', '__pycache__']).
    """
    include_exts = [e.lower() for e in include_exts] if include_exts else None
    exclude_dirs = set(exclude_dirs or [])

    results = []
    base = Path(repo_path)

    for filepath in base.rglob("*"):
        # Skip directories
        if filepath.is_dir():
            continue

        # Skip by extension
        if include_exts and filepath.suffix.lower() not in include_exts:
            continue

        # Skip files in excluded directories
        if any(part in exclude_dirs for part in filepath.parts):
            continue

        rel_path = str(filepath.relative_to(base))
        content = load_file(str(filepath))
        if content:
            results.append((rel_path, content))

    return results
