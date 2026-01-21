import struct

class GenesisRunner:
    def __init__(self):
        # 32 General Purpose Registers (x0 is always 0)
        self.regs = [0] * 32
        self.pc = 0
        self.memory = {}
        
        # Opcodes map to implementation (simplified)
        self.opcodes = {
            "LUI": self.exec_lui, "AUIPC": self.exec_auipc,
            "JAL": self.exec_jal, "JALR": self.exec_jalr,
            "BRANCH": self.exec_branch,
            "LOAD": self.exec_load, "STORE": self.exec_store,
            "OP-IMM": self.exec_op_imm, "OP": self.exec_op
        }

    def load_program(self, filename="genesis_function.txt"):
        self.instructions = []
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        offset, hexval = parts
                        # Little endian parse
                        val = int(hexval, 16)
                        # Re-pack to bytes to unpack correctly (lazy way to get int)
                        b = bytes.fromhex(hexval)
                        val = struct.unpack('<I', b)[0]
                        self.instructions.append(val)
            print(f"Loaded {len(self.instructions)} instructions into memory.")
        except:
            print("Failed to load program.")

    def run(self):
        print("\n=== EXECUTING GENESIS PROTOCOL ===")
        print("CPU State: Validating Logic...")
        
        steps = 0
        limit = 100 # Safety halt
        
        while self.pc < len(self.instructions) and steps < limit:
            word = self.instructions[self.pc]
            self.execute(word)
            self.pc += 1
            steps += 1
            
        print(f"\nExecution Halted after {steps} cycles.")
        self.dump_registers()

    def execute(self, word):
        opcode = word & 0x7F
        rd = (word >> 7) & 0x1F
        funct3 = (word >> 12) & 0x7
        rs1 = (word >> 15) & 0x1F
        rs2 = (word >> 20) & 0x1F
        imm_i = (word >> 20)
        
        # Opcode Dispatch
        handler = list(self.opcodes.values())[list(self.opcodes.keys()).index(self.get_opcode_name(opcode))]
        if handler:
            handler(word, rd, rs1, rs2, imm_i, funct3)
        else:
            print(f"PC:{self.pc:02X} | [UNKNOWN] Opcode 0x{opcode:X}")

    def get_opcode_name(self, op):
        # Reverse lookup for dispatch
        if op == 0x37: return "LUI"
        if op == 0x17: return "AUIPC"
        if op == 0x13: return "OP-IMM"
        if op == 0x33: return "OP"
        if op == 0x6F: return "JAL"
        if op == 0x67: return "JALR"
        if op == 0x63: return "BRANCH"
        if op == 0x03: return "LOAD"
        if op == 0x23: return "STORE"
        return "UNKNOWN"

    # --- INSTRUCTION IMPLEMENTATIONS ---
    def exec_lui(self, word, rd, rs1, rs2, imm, funct3):
        val = (word & 0xFFFFF000)
        if rd != 0: self.regs[rd] = val
        print(f"PC:{self.pc:02X} | LUI x{rd} <- 0x{val:X}")

    def exec_auipc(self, word, rd, rs1, rs2, imm, funct3):
        val = (word & 0xFFFFF000) + (self.pc * 4)
        if rd != 0: self.regs[rd] = val
        print(f"PC:{self.pc:02X} | AUIPC x{rd} <- PC + 0x{(word & 0xFFFFF000):X}")

    def exec_op_imm(self, word, rd, rs1, rs2, imm, funct3):
        # Handle sign extension
        if imm & 0x800: imm -= 0x1000
        val = (self.regs[rs1] + imm) & 0xFFFFFFFF
        if rd != 0: self.regs[rd] = val
        print(f"PC:{self.pc:02X} | ADDI/OP x{rd} <- x{rs1} + {imm}")

    def exec_op(self, word, rd, rs1, rs2, imm, funct3):
        val = (self.regs[rs1] + self.regs[rs2]) & 0xFFFFFFFF
        if rd != 0: self.regs[rd] = val
        print(f"PC:{self.pc:02X} | ADD x{rd} <- x{rs1} + x{rs2} = 0x{val:X}")

    def exec_jal(self, word, rd, rs1, rs2, imm, funct3):
        # Decode J-Type Immediate
        imm_20 = (word >> 31) & 0x1
        imm_10_1 = (word >> 21) & 0x3FF
        imm_11 = (word >> 20) & 0x1
        imm_19_12 = (word >> 12) & 0xFF
        offset = (imm_20 << 20) | (imm_19_12 << 12) | (imm_11 << 11) | (imm_10_1 << 1)
        if offset & 0x100000: offset -= 0x200000
        
        print(f"PC:{self.pc:02X} | JAL offset {offset}")
        # Not actually jumping in this simple test, just logging

    def exec_jalr(self, word, rd, rs1, rs2, imm, funct3):
        print(f"PC:{self.pc:02X} | JALR (Jump Register)")

    def exec_branch(self, word, rd, rs1, rs2, imm, funct3):
        print(f"PC:{self.pc:02X} | BRANCH (Conditional)")

    def exec_load(self, word, rd, rs1, rs2, imm, funct3):
        print(f"PC:{self.pc:02X} | LOAD x{rd} from MEM")

    def exec_store(self, word, rd, rs1, rs2, imm, funct3):
        print(f"PC:{self.pc:02X} | STORE x{rs2} to MEM")


    def dump_registers(self):
        print("\n--- FINAL REGISTER STATE ---")
        for i in range(0, 32, 4):
            regs = ""
            for j in range(4):
                if i+j < 32:
                    regs += f"x{i+j:<2}: 0x{self.regs[i+j]:08X}  "
            print(regs)
            
        # Check for interesting values
        # e.g. 42, 613, or ascii
        print("\n[ANALYSIS]")
        found = False
        for i, val in enumerate(self.regs):
            if val != 0:
                print(f"Register x{i} holds value: {val}")
                found = True
        if not found:
            print("System State: NULL (The Void)")

if __name__ == "__main__":
    runner = GenesisRunner()
    runner.load_program()
    runner.run()
