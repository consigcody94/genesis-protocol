"""
NULL HYPOTHESIS LAB
===================
Answers the "Open Questions" in the README with measured controls instead of
speculation. Every headline finding is re-tested against control corpora that
share the artifact's *encoding* but not its *content*:

  Control A — SHUFFLED TORAH: the real Hebrew letter stream, randomly
              permuted, then packed with the exact same Base-22 encoder.
              Destroys all linguistic structure, keeps letter frequencies.
  Control B — UNIFORM RANDOM: uniform random Base-22 digits of the same
              length, same packing. No structure at all.
  Control C — PURE RANDOM BYTES: os.urandom-style random bytes of the same
              size (seeded PRNG for reproducibility). No packing.

Experiments:
  1. Shannon entropy of the real artifact vs Controls A/B/C.
  2. Monte Carlo count of ASCII keyword hits ("DNA", "CODE", ...) in control
     binaries vs the real artifact.
  3. RISC-V "valid instruction" ratio of the real artifact vs controls.

Everything is stdlib-only and seeded, so results are reproducible:
    python null_hypothesis.py [--trials N]
"""

import argparse
import collections
import math
import random
import struct
import os

from torah_loader import TorahLoader

ALPHABET = "אבגדהוזחטיכלמנסעפצקרשת"
SOFIT_MAP = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}
BLOCK_SIZE = 13  # 22^13 < 2^64
SEED = 22

KEYWORDS = ["DNA", "RNA", "CODE", "NETWORK", "IPV6", "AI", "KEY", "ROOT",
            "HASH", "USER", "SSH", "GENE"]

# Same RV32I opcode set used by function_miner / divine_disassembler
RISCV_OPCODES = {0x37, 0x17, 0x6F, 0x67, 0x63, 0x03, 0x23, 0x13, 0x33, 0x0F, 0x73}


def shannon_entropy(data):
    """Shannon entropy in bits per byte."""
    if not data:
        return 0.0
    counts = collections.Counter(data)
    total = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


def letters_to_digits(text):
    """Map a Hebrew letter stream to Base-22 digits (finals folded)."""
    char_map = {char: i for i, char in enumerate(ALPHABET)}
    for sofit, base in SOFIT_MAP.items():
        char_map[sofit] = char_map[base]
    return [char_map[c] for c in text if c in char_map]


def pack_base22(digits):
    """Identical packing to master_command_64.py: 13 digits per 64-bit word."""
    out = bytearray()
    for i in range(0, len(digits), BLOCK_SIZE):
        val = 0
        for d in digits[i:i + BLOCK_SIZE]:
            val = val * 22 + d
        out.extend(struct.pack('>Q', val))
    return bytes(out)


def extract_ascii_strings(data, min_len=3):
    """Same extraction rule as deep_decoder.py."""
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


def keyword_hits(data):
    """Count substring hits of each keyword in the extracted ASCII strings."""
    strings = extract_ascii_strings(data)
    hits = {k: 0 for k in KEYWORDS}
    for s in strings:
        upper = s.upper()
        for k in KEYWORDS:
            if k in upper:
                hits[k] += 1
    return hits


def riscv_valid_ratio(data, max_words=None):
    """Fraction of 32-bit little-endian words whose low 7 bits are a valid
    RV32I opcode."""
    n_words = len(data) // 4
    if max_words is not None:
        n_words = min(n_words, max_words)
    if n_words == 0:
        return 0.0
    valid = 0
    for i in range(n_words):
        word = struct.unpack_from('<I', data, i * 4)[0]
        if word & 0x7F in RISCV_OPCODES:
            valid += 1
    return valid / n_words


class NullHypothesisLab:
    def __init__(self, trials=5):
        self.trials = trials
        self.rng = random.Random(SEED)
        self.report = []

    def emit(self, line=""):
        print(line)
        self.report.append(line)

    def run(self):
        self.emit("NULL HYPOTHESIS LAB")
        self.emit("=" * 60)

        # --- Load the real artifact and letter stream ---
        if not os.path.exists("tanakh_full.bin"):
            print("Error: tanakh_full.bin not found. Run master_command_64.py first.")
            return
        with open("tanakh_full.bin", 'rb') as f:
            real = f.read()

        text = TorahLoader().load_full_torah()
        digits = letters_to_digits(text)
        self.emit(f"\nReal artifact: {len(real)} bytes from {len(digits)} letters")
        self.emit(f"Monte Carlo trials per control: {self.trials} (seed={SEED})")

        # --- Experiment 1: Entropy ---
        self.emit("\n[1] SHANNON ENTROPY (bits/byte)")
        self.emit(f"    Real Tanakh artifact:        {shannon_entropy(real):.4f}")

        shuffled_bins, uniform_bins, random_bins = [], [], []
        for _ in range(self.trials):
            d = digits[:]
            self.rng.shuffle(d)
            shuffled_bins.append(pack_base22(d))
            uniform_bins.append(pack_base22(
                [self.rng.randrange(22) for _ in range(len(digits))]))
            random_bins.append(self.rng.randbytes(len(real)))

        def mean(vals):
            return sum(vals) / len(vals)

        e_shuf = [shannon_entropy(b) for b in shuffled_bins]
        e_unif = [shannon_entropy(b) for b in uniform_bins]
        e_rand = [shannon_entropy(b) for b in random_bins]
        self.emit(f"    Control A (shuffled Torah):  {mean(e_shuf):.4f}  "
                  f"(min {min(e_shuf):.4f} / max {max(e_shuf):.4f})")
        self.emit(f"    Control B (uniform Base-22): {mean(e_unif):.4f}  "
                  f"(min {min(e_unif):.4f} / max {max(e_unif):.4f})")
        self.emit(f"    Control C (random bytes):    {mean(e_rand):.4f}  "
                  f"(min {min(e_rand):.4f} / max {max(e_rand):.4f})")
        self.emit("    Note: 13 Base-22 digits occupy ~58.1 of each word's 64 bits,")
        self.emit("    so the first byte of every 8-byte block only takes values 0-4.")
        self.emit("    That alone caps the entropy of ANY Base-22-packed text below 8.0.")

        # --- Experiment 2: ASCII keyword Monte Carlo ---
        self.emit("\n[2] ASCII KEYWORD HITS (real vs shuffled-Torah controls)")
        real_hits = keyword_hits(real)
        control_hits = [keyword_hits(b) for b in shuffled_bins]
        self.emit(f"    {'Keyword':<10} {'Real':>6} {'Control mean':>14} {'Control range':>16}")
        for k in KEYWORDS:
            cvals = [c[k] for c in control_hits]
            self.emit(f"    {k:<10} {real_hits[k]:>6} {mean(cvals):>14.1f} "
                      f"{f'{min(cvals)}-{max(cvals)}':>16}")

        # --- Experiment 3: RISC-V valid-instruction ratio ---
        self.emit("\n[3] RISC-V VALID-OPCODE RATIO (32-bit LE words, low 7 bits)")
        expected = len(RISCV_OPCODES) / 128
        self.emit(f"    Chance expectation (11 opcodes / 128): {expected:.4f}")
        self.emit(f"    Real Tanakh artifact:                  "
                  f"{riscv_valid_ratio(real):.4f}")
        r_shuf = [riscv_valid_ratio(b) for b in shuffled_bins]
        r_rand = [riscv_valid_ratio(b) for b in random_bins]
        self.emit(f"    Control A (shuffled Torah):            {mean(r_shuf):.4f}")
        self.emit(f"    Control C (random bytes):              {mean(r_rand):.4f}")

        # --- Verdict ---
        self.emit("\n[VERDICT]")
        self.emit("    Any signal unique to the Tanakh should separate 'Real' from")
        self.emit("    Control A (same letters, no meaning). Metrics that match the")
        self.emit("    controls are properties of the Base-22 ENCODING, not the text.")

        with open("null_hypothesis_report.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(self.report))
        print("\nReport saved to null_hypothesis_report.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Null-hypothesis control experiments")
    parser.add_argument("--trials", type=int, default=5,
                        help="Monte Carlo trials per control (default 5)")
    args = parser.parse_args()
    NullHypothesisLab(trials=args.trials).run()
