import math
import os
import random

from analysis_utils import shannon_entropy
from hebrew import ALPHABET
from torah_loader import TorahLoader

class EntropyLab:
    def __init__(self):
        self.loader = TorahLoader()

    def generate_control_text(self, length, rng=None):
        """Generates a random string of Hebrew letters of given length."""
        rng = rng or random
        return "".join(rng.choice(ALPHABET) for _ in range(length))

    def run_experiment(self):
        # 1. Letter-level entropy of the full canon
        torah_text = self.loader.load_full_torah()
        if not torah_text:
            print("Error: corpus not found. Run download_data.py first.")
            return

        torah_entropy = shannon_entropy(torah_text)
        print(f"\nTorah Text Length: {len(torah_text)} letters")
        print(f"Torah Letter Entropy: {torah_entropy:.4f} bits/symbol")

        # 2. Control Group (Random Noise), seeded for reproducibility
        control_text = self.generate_control_text(len(torah_text), random.Random(22))
        control_entropy = shannon_entropy(control_text)
        print(f"Random Control Entropy: {control_entropy:.4f} bits/symbol")

        # Max entropy for 22 symbols = log2(22) ≈ 4.459
        max_entropy = math.log2(len(ALPHABET))
        print(f"Theoretical Max Entropy ({len(ALPHABET)} symbols): {max_entropy:.4f}")

        diff = control_entropy - torah_entropy
        print(f"\nNote: Torah letters carry {diff:.4f} bits less than pure noise -")
        print("the redundancy ('grammar') expected of any natural language.")

        # 3. Byte-level entropy of the packed artifact, if present
        if os.path.exists("tanakh_full.bin"):
            with open("tanakh_full.bin", 'rb') as f:
                data = f.read()
            print(f"\nPacked Artifact Entropy: {shannon_entropy(data):.4f} bits/byte")
            print("(See null_hypothesis.py: this value is a property of the Base-22")
            print(" packing - shuffled text packs to the same entropy.)")

if __name__ == "__main__":
    lab = EntropyLab()
    lab.run_experiment()
