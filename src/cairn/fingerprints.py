from __future__ import annotations

import hashlib
import re


_WORD = re.compile(r"\w+", re.UNICODE)
_BITS = 64


def _normalized_text(text: str) -> str:
    return " ".join(token.casefold() for token in _WORD.findall(text))


def _features(text: str) -> list[str]:
    normalized = _normalized_text(text)
    if not normalized:
        return []
    padded = f"  {normalized}  "
    width = 4
    if len(padded) <= width:
        return [padded]
    return [padded[index : index + width] for index in range(len(padded) - width + 1)]


def simhash(text: str) -> int:
    vector = [0] * _BITS
    for feature in _features(text):
        digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        for bit in range(_BITS):
            vector[bit] += 1 if value & (1 << bit) else -1
    out = 0
    for bit, weight in enumerate(vector):
        if weight > 0:
            out |= 1 << bit
    return out


def fingerprint_similarity(left: str, right: str) -> float:
    if not _features(left) or not _features(right):
        return 0.0
    distance = (simhash(left) ^ simhash(right)).bit_count()
    return round(1 - (distance / _BITS), 4)
