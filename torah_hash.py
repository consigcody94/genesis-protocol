import zlib
from gematria import GematriaEngine

class TorahHashLab:
    def __init__(self):
        self.ge = GematriaEngine()
        # A small dictionary of words to test collisions
        self.test_words = [
            "apple", "banana", "cherry", "date", "elderberry", 
            "fig", "grape", "honeydew", "kiwi", "lemon",
            "torah", "bible", "code", "python", "algorithm",
            "gematria", "hebrew", "cipher", "atbash", "mystery"
        ]

    def torah_hash(self, text):
        """
        A novel hashing utility inspired by Gematria.
        Concept:
        - Map each char to an index (1-26 for English).
        - Use weights based on 'Potency' (similar to 10^n in decimal, but maybe prime based?).
        - Add a 'skip' factor (ELS influence).
        """
        hash_val = 0
        skip = 0
        # English Gematria mapping (a=1, b=2... z=26)
        # But heavily weighted by position (like base-27)
        
        for i, char in enumerate(text):
            ascii_val = ord(char)
            # 1-26 mapping roughly
            val = (ascii_val - 96) if 'a' <= char <= 'z' else ascii_val
            
            # The "Torah" twist: 
            # 1. Use the Gematria 'Triangular' property? (Traffic = 1+2+3..n) - No, too slow.
            # 2. Weight by position (i+1) * Value.
            # 3. Add a specialized "salt" based on text length (Kabbalistic significance of numbers?).
            
            weight = (i + 1) * 7 # 7 is a significant number in Torah
            hash_val += (val * weight)
            
            # ELS-inspired: Add value of character 'skip' steps away? 
            # Too complex for simple checksum.
            
        # Modulo to keep it within standard integer range (32-bitish)
        return hash_val % 4294967296

    def simple_hash(self, text):
        """Standard weak hash (sum of chars)."""
        return sum(ord(c) for c in text)

    def run_experiment(self):
        print("Experiment: Testing 'TorahHash' collision resistance vs SimpleHash\n")
        
        # Test 1: TorahHash
        hashes = {}
        collisions = 0
        print("--- TorahHash Results ---")
        for word in self.test_words:
            h = self.torah_hash(word.lower())
            print(f"Word: {word:12} | Hash: {h}")
            if h in hashes:
                collisions += 1
                print(f"  [!] COLLISION: {word} with {hashes[h]}!")
            hashes[h] = word
        
        print(f"Total Collisions (TorahHash): {collisions}")

        # Test 2: Simple Sum Hash
        print("\n--- SimpleHash Results ---")
        hashes_s = {}
        collisions_s = 0
        for word in self.test_words:
            h = self.simple_hash(word.lower())
            if h in hashes_s:
                collisions_s += 1
            hashes_s[h] = word
        print(f"Total Collisions (SimpleHash): {collisions_s}")

        # Conclusion
        if collisions < collisions_s:
            print("\nDISCOVERY: TorahHash is superior to SimpleHash!")
            print("It uses positional weighting (inspired by Gematria) to avoid anagram collisions (god/dog).")
        else:
            print("\nResult: TorahHash is comparable to standard methods.")

if __name__ == "__main__":
    lab = TorahHashLab()
    lab.run_experiment()
