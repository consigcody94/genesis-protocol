import struct
from torah_loader import TorahLoader

class MasterCommand64:
    def __init__(self):
        self.loader = TorahLoader()
        self.alphabet = "אבגדהוזחטיכלמנסעפצקרשת"
        self.char_map = {char: i for i, char in enumerate(self.alphabet)}

    def process_block(self, chunk):
        """
        Processes a block of 13-14 Hebrew letters.
        13 letters * log2(22) = 58 bits. Fits safely in 64-bit Int.
        """
        val = 0
        for char in chunk:
            if char in self.char_map:
                val = val * 22 + self.char_map[char]
        return val

    def run(self):
        print("SYSTEM ONLINE: 64-BIT OPTIMIZATION ENABLED")
        
        # Load Data
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
            # We use 'Q' for unsigned long long (8 bytes)
            # Big Endian to preserve flow order
            packed = struct.pack('>Q', block_val)
            
            # Trim leading null bytes? 
            # If we treat it as a stream, we might want fixed width, 
            # strictly packing 8 bytes effectively "pads" it. 
            # But true compression would remove zeros.
            # Let's keep it fixed width for "aligned" data (like RAM).
            binary_stream.extend(packed)

        # Output
        out_file = "tanakh_full.bin"
        with open(out_file, "wb") as f:
            f.write(binary_stream)
            
        print(f"\n[SUCCESS] Extraction Complete.")
        print(f"Payload Size: {len(binary_stream)} bytes ({len(binary_stream)/1024:.2f} KB)")
        print(f"Artifact Saved: {out_file}")
        
        # Entropy Check
        import math
        from collections import Counter
        counts = Counter(binary_stream)
        entropy = 0
        total = len(binary_stream)
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        print(f"Global Entropy: {entropy:.4f} bits/byte")

if __name__ == "__main__":
    mc = MasterCommand64()
    mc.run()
