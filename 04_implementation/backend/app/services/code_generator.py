from __future__ import annotations

import re
import unicodedata


STOP_WORDS = {"DE", "DEL", "LA", "EL", "LOS", "LAS", "Y", "EN", "PARA"}


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", ascii_text.upper()).strip()


def generate_material_code(description: str, max_length: int = 24) -> str:
    text = normalize_text(description)
    tokens = [token for token in re.split(r"[^A-Z0-9/]+", text) if token]
    meaningful = [token for token in tokens if token not in STOP_WORDS]

    code_parts: list[str] = []
    for token in meaningful:
        if re.search(r"\d", token) or "/" in token:
            code_parts.append(token)
        else:
            code_parts.append(token[:4] if len(token) > 4 else token)

    code = "-".join(code_parts) or "ITEM"
    return code[:max_length].strip("-")
