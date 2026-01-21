import math
import collections
import random
import os
from text_processor import TextProcessor

class EntropyLab:
    def __init__(self):
        self.tp = TextProcessor()
        self.hebrew_alphabet = "אבגדהוזחטיכלמנסעפצקרשת"

    def calculate_shannon_entropy(self, text):
        """Calculates Shannon Entropy in bits per symbol."""
        if not text:
            return 0
        freqs = collections.Counter(text)
        total_len = len(text)
        entropy = 0
        for count in freqs.values():
            p = count / total_len
            entropy -= p * math.log2(p)
        return entropy

    def generate_control_text(self, length):
        """Generates a random string of Hebrew letters of given length."""
        return "".join(random.choice(self.hebrew_alphabet) for _ in range(length))

    def run_experiment(self):
        # Load Genesis
        path = os.path.join("data", "torah_text.txt")
        if not os.path.exists(path):
            print("Error: content file needed.")
            return

        raw_text = self.tp.load_file(path)
        torah_text = self.tp.normalize(raw_text)
        
        # 1. Shannon Entropy
        torah_entropy = self.calculate_shannon_entropy(torah_text)
        print(f"Torah Text Length: {len(torah_text)} letters")
        print(f"Torah Shannon Entropy: {torah_entropy:.4f} bits/symbol")
        
        # 2. Control Group (Random Noise)
        control_text = self.generate_control_text(len(torah_text))
        control_entropy = self.calculate_shannon_entropy(control_text)
        print(f"Random Control Entropy: {control_entropy:.4f} bits/symbol")
        
        # Analysis
        # Max entropy for 22 chars = log2(22) ≈ 4.459
        max_entropy = math.log2(22)
        print(f"Theoretical Max Entropy (22 chars): {max_entropy:.4f}")
        
        diff = control_entropy - torah_entropy
        print(f"\nDiscovery Note: Torah is {diff:.4f} bits 'less random' than pure noise.")
        print("Interpretation: This indicates structural 'redundancy' or 'grammar', which is expected in language.")
        # But maybe we can frame it as "Compression Potential".

if __name__ == "__main__":
    lab = EntropyLab()
    lab.run_experiment()
