import os
import collections
import math

class ArchitectureDetective:
    def __init__(self):
        self.filename = "tanakh_full.bin"

    def analyze(self):
        if not os.path.exists(self.filename):
            print("Error: Artifact not found.")
            return

        with open(self.filename, 'rb') as f:
            data = f.read()
        
        print(f"Analyzing {len(data)} bytes for Architectural Signatures...")

        # 1. Alignment Check
        # Most CPUs use fixed-width instructions (16-bit, 32-bit, 64-bit)
        # We check for repeating patterns at these intervals.
        entropy_16 = self.measure_alignment(data, 2)
        entropy_32 = self.measure_alignment(data, 4)
        entropy_64 = self.measure_alignment(data, 8)
        
        print(f"\n[1] Alignment Entropy (Lower is better/more structured):")
        print(f"   16-bit (thumb/dos): {entropy_16:.4f}")
        print(f"   32-bit (arm/x86):   {entropy_32:.4f}")
        print(f"   64-bit (modern):    {entropy_64:.4f}")

        best_align = min(entropy_16, entropy_32, entropy_64)
        arch_width = "Unknown"
        if best_align == entropy_16: arch_width = "16-bit"
        if best_align == entropy_32: arch_width = "32-bit"
        if best_align == entropy_64: arch_width = "64-bit"
        
        print(f"   -> Likely Instruction Width: {arch_width}")

        # 2. Opcode Histogram (First byte of instruction)
        # In a real ISA, some opcodes (MOV, ADD, JMP) are VERY frequent.
        # Random data implies flat distribution.
        
        step = 4 if arch_width == "32-bit" else 2
        opcodes = [data[i] for i in range(0, len(data), step)]
        
        counts = collections.Counter(opcodes)
        top_ops = counts.most_common(5)
        
        print(f"\n[2] Top Opcodes (Hypothetical):")
        for op, count in top_ops:
            hex_op = hex(op)[2:].zfill(2).upper()
            pct = (count / len(opcodes)) * 100
            print(f"   0x{hex_op}: {count} hits ({pct:.1f}%)")

        # 3. Signature Matching
        # Known magic headers or patterns
        signatures = {
            "4d5a": "DOS/Windows PE",
            "7f454c46": "ELF (Linux)",
            "cafebabe": "Java Class / Mach-O",
            "feedface": "Mach-O",
            "00000000": "Null Vector Table",
            "e59f": "ARM LDR"
        }
        
        head = data[:4].hex()
        matched = False
        for sig, name in signatures.items():
            if head.startswith(sig):
                print(f"\n[3] Signature Match: {name}")
                matched = True
        
        if not matched:
            print(f"\n[3] No Earthly Signature Found (Header: {head})")
            
        print("\n[VERDICT]")
        if arch_width == "32-bit" and not matched:
            print("Structure: 32-bit RISC-like Architecture (High Entropy)")
            print("Classification: 'ALEPH-ZERO ISA' (Unknown Origin)")
        elif arch_width == "16-bit":
             print("Structure: 16-bit Microcontroller Code")
             print("Classification: 'GENESIS MICROCODE'")
        else:
             print("Structure: High-Density Compressed Data Stream")

    def measure_alignment(self, data, width):
        # Sample chunks
        chunks = [data[i:i+width] for i in range(0, len(data)-width, width)]
        # Measure uniqueness ratio? Or entropy of columns?
        # Let's measure entropy of the FIRST byte of each chunk (simulating opcode entropy)
        opcodes = [c[0] for c in chunks]
        counts = collections.Counter(opcodes)
        entropy = 0
        total = len(opcodes)
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

if __name__ == "__main__":
    ad = ArchitectureDetective()
    ad.analyze()
