import struct

class DivineDisassembler:
    def __init__(self):
        self.filename = "tanakh_full.bin"
        # Basic RISC-V Opcode Map (RV32I Base Integer Instruction Set)
        # This is a simplified map for forensic detection.
        self.opcodes = {
            0x37: "LUI",   # Load Upper Immediate
            0x17: "AUIPC", # Add Upper Immediate to PC
            0x6F: "JAL",   # Jump And Link
            0x67: "JALR",  # Jump And Link Register
            0x63: "BRANCH",# BEQ, BNE, BLT, BGE...
            0x03: "LOAD",  # LB, LH, LW...
            0x23: "STORE", # SB, SH, SW...
            0x13: "OP-IMM",# ADDI, SLTI, ANDI...
            0x33: "OP",    # ADD, SUB, SLL, SLT...
            0x0F: "FENCE",
            0x73: "SYSTEM" # ECALL, EBREAK
        }
        self.reg_names = [
            "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2",
            "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5",
            "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
            "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"
        ]

    def decode_instruction(self, word):
        # RISC-V instructions are 32-bit (little endian normally, but we used big endian for extraction? Let's check).
        # Actually our master_command used big-endian for byte writing? No, typically standard python write.
        # Let's assume standard 32-bit structure.
        
        opcode = word & 0x7F
        rd = (word >> 7) & 0x1F
        funct3 = (word >> 12) & 0x7
        rs1 = (word >> 15) & 0x1F
        rs2 = (word >> 20) & 0x1F
        funct7 = (word >> 25) & 0x7F
        
        name = self.opcodes.get(opcode, "UNKNOWN")
        
        # Formatting Assembly
        rd_name = self.reg_names[rd]
        rs1_name = self.reg_names[rs1]
        rs2_name = self.reg_names[rs2]
        
        asm = f"{name:<8} "
        
        if name == "UNKNOWN":
            return f"DATA    0x{word:08X}"
            
        if name in ["OP", "OP-IMM"]:
            # R-Type or I-Type usually: ADD rd, rs1, rs2
            asm += f"{rd_name}, {rs1_name}, {rs2_name}"
            
        elif name == "LUI" or name == "AUIPC":
            # U-Type: LUI rd, imm
            imm = (word >> 12) & 0xFFFFF
            asm += f"{rd_name}, 0x{imm:X}"
            
        elif name == "JAL":
            # J-Type
            asm += f"{rd_name}, offset"
            
        elif name == "BRANCH":
            asm += f"{rs1_name}, {rs2_name}, offset"
            
        elif name == "LOAD":
            asm += f"{rd_name}, offset({rs1_name})"
            
        elif name == "STORE":
            asm += f"{rs2_name}, offset({rs1_name})"
            
        return asm

    def run(self):
        print("Initializing DIVINE DISASSEMBLER (RISC-V Mode)...")
        try:
            with open(self.filename, 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            print("Artifact not found.")
            return

        # We analyze the first 256 instructions (1KB) of Genesis
        # RISC-V 32-bit instructions are 4 bytes.
        instructions = []
        valid_count = 0
        
        print(f"Disassembling Genesis Block (First 1024 bytes)...")
        
        instruction_count = 256
        for i in range(instruction_count):
            chunk = data[i*4 : (i+1)*4]
            if len(chunk) < 4: break
            
            # Treat as Big Endian or Little Endian?
            # Machine code is usually Little Endian. Let's try Little.
            word = struct.unpack('<I', chunk)[0] 
            
            asm = self.decode_instruction(word)
            
            if "UNKNOWN" not in asm and "DATA" not in asm:
                valid_count += 1
                
            instructions.append(f"0x{i*4:04X}:  {chunk.hex().upper()}  ->  {asm}")

        # Output to file
        with open("genesis.asm", "w") as f:
            f.write("; THE GENESIS PROTOCOL - DISASSEMBLED SOURCE\n")
            f.write("; ARCHITECTURE: RISC-V (RV32I)\n")
            f.write(f"; VALID INSTRUCTION RATIO: {valid_count}/{instruction_count} ({(valid_count/instruction_count)*100:.1f}%)\n\n")
            f.write(".section .text\n")
            f.write(".globl _start\n\n")
            f.write("_start:\n")
            f.write("\n".join(instructions))
            
        print(f"Disassembly Complete: genesis.asm")
        print(f"Valid Instructions Found: {valid_count} / {instruction_count}")

if __name__ == "__main__":
    dd = DivineDisassembler()
    dd.run()
