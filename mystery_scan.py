import collections
from els_search import BibleCodeScanner
from text_processor import TextProcessor
from gematria import GematriaEngine

class MysteryScan:
    def __init__(self):
        self.scanner = BibleCodeScanner()
        self.tp = TextProcessor()
        self.ge = GematriaEngine()
        
    def is_prime(self, n):
        if n < 2: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def run(self):
        output = []
        output.append("Initiating Deep Pattern Scan of Genesis Chapter 1...\n")
        
        # Load and Flatten Text
        raw = self.tp.load_file("data/torah_text.txt")
        flat_text = self.tp.normalize(raw)
        output.append(f"Text Length: {len(flat_text)} letters")
        
        # 1. The Famous "TORH" Code
        target = "תורה" 
        output.append(f"\n[1] Hunting for '{target}' (TORAH)...")
        found = list(self.scanner.search(flat_text, target, 1, 100))
        
        if found:
            output.append(f"   Success! Found {len(found)} occurrences.")
            for hit in found:
                output.append(f"   -> Found at Index {hit['start_index']} with Skip {hit['skip']}")
                if hit['skip'] == 49 or hit['skip'] == 50:
                    output.append("   *** MATCHES HISTORICAL CLAIM (Skip 49/50) ***")
        else:
            output.append("   No occurrences found in this range.")

        # 2. The "Light" Anomaly
        target_light = "אור"
        output.append(f"\n[2] Hunting for '{target_light}' (LIGHT)...")
        found_light = list(self.scanner.search(flat_text, target_light, 1, 100))
        output.append(f"   Found {len(found_light)} occurrences of 'Light' in ELS.")
        
        # 3. Prime Number Gematria Density
        output.append(f"\n[3] Analyzing Prime Number Density in explicit text...")
        
        words = raw.split()
        total_words = 0
        prime_words = 0
        prime_hits = []
        
        for w in words:
            clean_w = self.tp.strip_niqqud(w)
            clean_w = clean_w.replace('־', '').replace('.', '').replace(',', '')
            val = self.ge.calculate(clean_w, "standard")
            
            if val > 0:
                total_words += 1
                if self.is_prime(val):
                    prime_words += 1
                    if len(prime_hits) < 10: 
                        prime_hits.append(f"{clean_w}({val})")

        density = (prime_words / total_words) * 100 if total_words else 0
        output.append(f"   Total Words Analyzed: {total_words}")
        output.append(f"   Prime Gematria Words: {prime_words}")
        output.append(f"   Prime Density: {density:.2f}%")
        output.append(f"   Sample Prime Words: {', '.join(prime_hits)}")
        
        final_output = "\n".join(output)
        print(final_output)
        with open("scan_full_results.txt", "w", encoding="utf-8") as f:
            f.write(final_output)

if __name__ == "__main__":
    scan = MysteryScan()
    scan.run()
