import os
from analysis_utils import ensure_utf8_stdout
from text_processor import TextProcessor
from gematria import GematriaEngine
from els_search import BibleCodeScanner
from ciphers import CipherEngine

class TorahWorkbenchApp:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.gematria_engine = GematriaEngine()
        self.els_scanner = BibleCodeScanner()
        self.cipher_engine = CipherEngine()
        self.loaded_text = ""
        self.flat_text = ""

    def load_data(self):
        path = os.path.join("data", "torah_text.txt")
        if not os.path.exists(path):
            print(f"Error: Data file not found at {path}")
            return False
        
        raw_text = self.text_processor.load_file(path)
        # Keep a version without vowels for processing
        self.loaded_text = self.text_processor.strip_niqqud(raw_text)
        self.flat_text = self.text_processor.normalize(raw_text)
        print(f"Loaded Text: {len(self.loaded_text)} characters.")
        print(f"Flattened Text (for ELS): {len(self.flat_text)} letters.")
        return True

    def run(self):
        print("Welcome to the Torah Computational Workbench")
        if not self.load_data():
            return

        while True:
            print("\nSelect Mode:")
            print("1. Gematria Calculator")
            print("2. ELS Search (Bible Codes)")
            print("3. Cipher Tools (Atbash/Albam)")
            print("4. Exit")
            
            choice = input("Enter choice: ")
            
            if choice == "1":
                self.mode_gematria()
            elif choice == "2":
                self.mode_els()
            elif choice == "3":
                self.mode_cipher()
            elif choice == "4":
                print("Exiting.")
                break
            else:
                print("Invalid choice.")

    def mode_gematria(self):
        text = input("Enter Hebrew text to calculate: ")
        std_val = self.gematria_engine.calculate(text, "standard")
        ord_val = self.gematria_engine.calculate(text, "ordinal")
        red_val = self.gematria_engine.calculate(text, "reduced")
        
        print(f"Statement: {text}")
        print(f"Standard (Ragil): {std_val}")
        print(f"Ordinal (Siduri): {ord_val}")
        print(f"Reduced (Katan):  {red_val}")

    def mode_els(self):
        term = input("Enter search term (Hebrew): ")
        max_dist = input("Max skip distance (default 50): ")
        max_dist = int(max_dist) if max_dist.isdigit() else 50
        
        print(f"Searching for '{term}' with max skip {max_dist}...")
        # Forward and backward skips in two passes
        results = list(self.els_scanner.search(self.flat_text, term, 1, max_dist))
        results += list(self.els_scanner.search(self.flat_text, term, -max_dist, -1))

        if not results:
            print("No sequences found.")
        else:
            print(f"Found {len(results)} occurrences.")
            for r in results[:10]:
                print(f"Match: Start={r['start_index']}, Skip={r['skip']}")
            if len(results) > 10:
                print(f"... and {len(results) - 10} more.")

    def mode_cipher(self):
        text = input("Enter text to encipher: ")
        atbash = self.cipher_engine.atbash(text)
        albam = self.cipher_engine.albam(text)
        
        print(f"Original: {text}")
        print(f"Atbash:   {atbash}")
        print(f"Albam:    {albam}")

if __name__ == "__main__":
    ensure_utf8_stdout()
    app = TorahWorkbenchApp()
    app.run()
