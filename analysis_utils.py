"""
Shared analysis helpers.

Shannon entropy and ASCII string extraction were re-implemented in five
different scripts with subtle variations; this module is the single
canonical version used everywhere.
"""

import collections
import math
import sys


def ensure_utf8_stdout():
    """Make Hebrew output safe on non-UTF-8 consoles (Windows cp1252)."""
    enc = getattr(sys.stdout, "encoding", None)
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if enc and reconfigure and enc.lower().replace("-", "") != "utf8":
        reconfigure(encoding="utf-8", errors="replace")


def shannon_entropy(data):
    """Shannon entropy in bits per symbol (bits/byte for byte input)."""
    if not data:
        return 0.0
    counts = collections.Counter(data)
    total = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


def extract_ascii_strings(data, min_len=3):
    """Runs of printable ASCII (0x20-0x7E) at least min_len long."""
    strings = []
    cur = []
    for byte in data:
        if 32 <= byte <= 126:
            cur.append(chr(byte))
        else:
            if len(cur) >= min_len:
                strings.append("".join(cur))
            cur = []
    if len(cur) >= min_len:
        strings.append("".join(cur))
    return strings
