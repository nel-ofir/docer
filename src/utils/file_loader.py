import os

def load_file(path: str, max_chars: int = 20000) -> str:
    """
    Read a file’s text content, truncating if it exceeds max_chars.
    Returns an empty string on any read error.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        # Truncate to avoid exceeding model token limits
        return text if len(text) <= max_chars else text[:max_chars]
    except Exception:
        return ""