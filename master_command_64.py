import argparse
import struct

from analysis_utils import shannon_entropy
from hebrew import build_char_map
from torah_loader import TorahLoader

class MasterCommand64:
    def __init__(self):
        self.loader = TorahLoader()
        self.char_map = build_char_map()

    def process_block(self, chunk):
        """
        Processes a block of up to 13 Hebrew letters.
        13 letters * log2(22) = 58 bits. Fits safely in 64-bit Int.
        """
        val = 0
        for char in chunk:
            if char in self.char_map:
                val = val * 22 + self.char_map[char]
        return val

    def run(self, out_file="tanakh_full.bin", torah_only=False):
        print("SYSTEM ONLINE: 64-BIT OPTIMIZATION ENABLED")

        # Load Data
        if torah_only:
            # First five books only — this is how the_hidden_book.bin is built
            self.loader.books = self.loader.books[:5]
        text = self.loader.load_full_torah()
        if not text:
            print("Error: No data.")
            return

        total_len = len(text)
        block_size = 13 # 13 chars fits within 64 bits (22^13 < 2^64)

        binary_stream = bytearray()

        print(f"Processing {total_len} characters in {block_size}-char blocks...")

        for i in range(0, total_len, block_size):
            chunk = text[i : i + block_size]

            # Convert chunk to 64-bit Integer
            block_val = self.process_block(chunk)

            # Pack as 8 bytes (64-bit unsigned long long)
            # Big Endian to preserve flow order
            packed = struct.pack('>Q', block_val)
            binary_stream.extend(packed)

        # Output
        with open(out_file, "wb") as f:
            f.write(binary_stream)

        print(f"\n[SUCCESS] Extraction Complete.")
        print(f"Payload Size: {len(binary_stream)} bytes ({len(binary_stream)/1024:.2f} KB)")
        print(f"Artifact Saved: {out_file}")
        print(f"Global Entropy: {shannon_entropy(binary_stream):.4f} bits/byte")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Base-22 binary extraction")
    parser.add_argument("-o", "--output", default="tanakh_full.bin",
                        help="output file (default tanakh_full.bin)")
    parser.add_argument("--torah-only", action="store_true",
                        help="extract only the Five Books (the_hidden_book.bin)")
    args = parser.parse_args()
    MasterCommand64().run(out_file=args.output, torah_only=args.torah_only)
