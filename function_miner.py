import struct

class FunctionMiner:
    def __init__(self):
        self.filename = "tanakh_full.bin"
        self.opcodes = {
            0x37: "LUI", 0x17: "AUIPC", 0x6F: "JAL", 0x67: "JALR",
            0x63: "BRANCH", 0x03: "LOAD", 0x23: "STORE", 0x13: "OP-IMM",
            0x33: "OP", 0x0F: "FENCE", 0x73: "SYSTEM"
        }

    def run(self):
        print("Mining for Logic Blocks (Contiguous Instructions)...")
        try:
            with open(self.filename, 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            return

        longest_chain = []
        current_chain = []
        chains = []

        # Scan the first 100KB for speed (it's huge)
        limit = 100000 
        print(f"Scanning first {limit} bytes...")
        
        for i in range(0, min(len(data), limit), 4):
            chunk = data[i:i+4]
            if len(chunk) < 4: break
            
            word = struct.unpack('<I', chunk)[0] # Little Endian for RISC-V
            opcode = word & 0x7F
            
            if opcode in self.opcodes:
                # It's a valid instruction opcode
                name = self.opcodes[opcode]
                current_chain.append( (i, name, chunk.hex()) )
            else:
                # Chain broken
                if len(current_chain) > 2: # Keep chains longer than 2
                    chains.append(current_chain)
                    if len(current_chain) > len(longest_chain):
                        longest_chain = current_chain
                current_chain = []

        print(f"\nFound {len(chains)} potential Logic Blocks.")
        
        if longest_chain:
            print(f"\n[!] Longest Function Discovered: {len(longest_chain)} Instructions")
            print(f"    Offset: 0x{longest_chain[0][0]:X}")
            print("    Code:")
            for offset, name, hexval in longest_chain:
                print(f"      0x{offset:X}: {name:<8} ({hexval})")
                
            # Save to file for the Runner
            with open("genesis_function.txt", "w") as f:
                for offset, name, hexval in longest_chain:
                    f.write(f"{offset},{hexval}\n")
            print("    -> Saved to 'genesis_function.txt'")
        else:
            print("No significant logic blocks found.")

if __name__ == "__main__":
    fm = FunctionMiner()
    fm.run()
