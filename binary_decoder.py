import os
import binascii
from text_processor import TextProcessor

class BinaryExtractor:
    def __init__(self):
        self.tp = TextProcessor()
        # Mapping Aleph(0) to Tav(21)
        self.alphabet = "אבגדהוזחטיכלמנסעפצקרשת"
        self.char_map = {char: i for i, char in enumerate(self.alphabet)}

    def text_to_bits(self, text):
        """
        Converts Hebrew text to a bitstream.
        Hypothesis: Each letter is a Base-22 digit.
        We convert the massive Base-22 number into binary.
        """
        # Optimized approach: Large integer math in Python is automatic
        print("Converting text to massive integer (Base-22)...")
        big_int = 0
        for char in text:
            if char in self.char_map:
                val = self.char_map[char]
                big_int = big_int * 22 + val
        
        # Convert to bytes
        print("Transforming to bytes...")
        try:
            # bit_length() gives bits, divide by 8 for bytes
            num_bytes = (big_int.bit_length() + 7) // 8
            byte_data = big_int.to_bytes(num_bytes, byteorder='big')
            return byte_data
        except OverflowError:
            print("Integer too large to convert immediately.")
            return b""

    def analyze_entropy(self, data):
        """Check if the extracted binary looks like code or noise."""
        if not data: return 0
        import math
        from collections import Counter
        counts = Counter(data)
        entropy = 0
        total = len(data)
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def run(self):
        print("Initiating MASTER COMMAND Protocol: Binary Extraction...")
        
        # Load Genesis 1
        raw = self.tp.load_file("data/torah_text.txt")
        flat = self.tp.normalize(raw)
        print(f"Input Stream: {len(flat)} Hebrew instruction codes (letters).")
        
        # Decode
        binary_data = self.text_to_bits(flat)
        print(f"Extracted payload size: {len(binary_data)} bytes.")
        
        # Analysis
        entropy = self.analyze_entropy(binary_data)
        print(f"Data Entropy: {entropy:.4f} bits/byte (Max 8.0)")
        
        # Heuristic: High entropy (>7.5) often means Compressed Data or Encrypted Code.
        # Low entropy (<5) means Text or Sparse Data.
        
        if entropy > 7.5:
            print("[!] ALERT: High Entropy Detected. This resembles COMPRESSED DATA.")
        else:
            print("[i] Status: Moderate Entropy. Likely raw structured data.")
            
        # Search for file headers?
        # Check for PDF ("%PDF"), ZIP ("PK"), PNG, Executable signatures?
        hex_head = binascii.hexlify(binary_data[:8]).decode()
        print(f"File Header (HEX): {hex_head}")
        
        # Save output
        with open("genesis_1.bin", "wb") as f:
            f.write(binary_data)
        print("Payload saved to 'genesis_1.bin'.")
        print("Use a Hex Editor to inspect the MASTER COMMAND payload.")

if __name__ == "__main__":
    extractor = BinaryExtractor()
    extractor.run()
