import re
import os

from analysis_utils import extract_ascii_strings

class DeepDecoder:
    def __init__(self):
        self.filename = "tanakh_full.bin"
        self.min_str_len = 4

    def run(self):
        if not os.path.exists(self.filename):
            print(f"Error: {self.filename} not found.")
            return

        with open(self.filename, 'rb') as f:
            data = f.read()

        # Single pass: every line goes to stdout AND the report file.
        report = []
        def emit(line):
            print(line)
            report.append(line)

        emit(f"Loaded Grand Artifact: {len(data)} bytes")

        # 1. Regex Hunting
        emit("\n[1] Scanning for Patterns (Regex)...")

        patterns = {
            "IPv4": rb'\b(?:\d{1,3}\.){3}\d{1,3}\b', # e.g. 192.168.1.1
            "IPv6": rb'([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}', # Full IPv6 (simple)
            "Email": rb'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "URL": rb'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
            "Year": rb'\b(19|20)\d{2}\b' # 1900-2099
        }

        for name, pat in patterns.items():
            matches = re.findall(pat, data)
            if matches:
                # Deduplicate and decode
                unique = set(matches)
                emit(f"   [!] Found {len(unique)} {name} candidates:")
                for m in list(unique)[:5]:
                    emit(f"       -> {m.decode('ascii', errors='ignore')}")

        # 2. Keyword Dictionary Scan
        emit("\n[2] Scanning for Modern Keywords...")
        keywords = [
            # Tech
            "HTTP", "HTML", "JSON", "XML", "SSH", "FTP", "ROOT", "ADMIN", "SYSTEM", "KERNEL", "BOOT", "SHELL", "SUDO",
            "LOGIN", "PASSWORD", "USER", "SERVER", "CLIENT", "DATABASE", "SQL", "API", "CLOUD", "AI", "AGI", "NEURAL",
            # Bio / Physics
            "DNA", "RNA", "GENE", "CRISPR", "ATOM", "QUARK", "QUANTUM", "RELATIVITY", "E=MC", "CELL", "VIRUS",
            # Crypto
            "BITCOIN", "BTC", "ETH", "BLOCKCHAIN", "HASH", "CIPHER", "KEY", "WALLET", "SATOSHI",
            # History/Prophecy
            "ISRAEL", "ZION", "JERUSALEM", "TEMPLE", "MESSIAH", "GOG", "MAGOG", "ARMAGEDDON"
        ]

        # Extract all ASCII strings first for speed
        # (min length 3 to allow short words like DNA)
        ascii_strings = extract_ascii_strings(data, min_len=3)

        # Search strings
        found_map = {}
        for s in ascii_strings:
            upper_s = s.upper()
            for k in keywords:
                if k in upper_s:
                    if k not in found_map: found_map[k] = 0
                    found_map[k] += 1
                    # Print context if rare
                    if found_map[k] <= 3:
                        emit(f"   [!] MATCH: '{k}' found in string: '{s}'")

        # 3. File Entropy & Header
        head = data[:8].hex()
        emit(f"\n[3] Header Analysis: {head}")
        if "504b0304" in head: emit("   -> PK Header (ZIP) Detected!")

        # 4. Save Strings
        with open("tanakh_strings.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(ascii_strings))
        print(f"\n[4] All {len(ascii_strings)} extracted strings saved to 'tanakh_strings.txt'.")

        # 5. Save Report to File
        with open("deep_scan_clean.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        print("Report saved to deep_scan_clean.txt")

if __name__ == "__main__":
    dd = DeepDecoder()
    dd.run()
