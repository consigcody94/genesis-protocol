import sys
import unittest
from text_processor import TextProcessor
from gematria import GematriaEngine
from els_search import BibleCodeScanner
from ciphers import CipherEngine

class TestTorahWorkbench(unittest.TestCase):
    def setUp(self):
        self.tp = TextProcessor()
        self.ge = GematriaEngine()
        self.els = BibleCodeScanner()
        self.ce = CipherEngine()

    def test_text_processor(self):
        # Test normalization
        raw = "בְּרֵאשִׁית בָּרָא"
        expected = "בראשיתברא"
        self.assertEqual(self.tp.normalize(raw), expected)
        print("Text Normalization: PASS")

    def test_gematria(self):
        # 'שלום' - Shin(300) + Lamed(30) + Vav(6) + Mem Sophit(40) = 376
        # Note: Mem Sophit in my engine is mapped to 40 same as Mem.
        word = "שלום"
        val = self.ge.calculate(word, "standard")
        self.assertEqual(val, 376)
        print(f"Gematria Standard ({word}={val}): PASS")
        
        # Ordinal: Shin(21) + Lamed(12) + Vav(6) + Mem(13) = 52
        # Check standard ordinal values:
        # א=1, ב=2 ... י=10, כ=11, ל=12, מ=13, נ=14, ס=15, ע=16, פ=17, צ=18, ק=19, ר=20, ש=21, ת=22
        val_ord = self.ge.calculate(word, "ordinal")
        self.assertEqual(val_ord, 52) 
        print(f"Gematria Ordinal ({word}={val_ord}): PASS")

    def test_ciphers(self):
        # Atbash is its own inverse
        word = "אבג"
        encrypted = self.ce.atbash(word) # תשר
        decrypted = self.ce.atbash(encrypted)
        self.assertEqual(decrypted, word)
        print("Atbash Reversibility: PASS")

    def test_els(self):
        # Create a synthetic text for predictable ELS
        # Search for "ABC" with skip 2
        # Text: "A x B x C" -> "א x ב x ג"
        # Let's use Hebrew: "א1ב2ג"
        text = "א1ב2ג" 
        # But my normalize strips numbers, so let's stick to strict hebrew text in scanner or just manual string
        # The scanner doesn't normalize, the app does.
        text = "אמבמג" # Aleph, Mem, Bet, Mem, Gimel. 
        # Search "אבג" skip 2.
        
        results = list(self.els.search(text, "אבג", 1, 5))
        found = False
        for r in results:
            if r['skip'] == 2 and r['start_index'] == 0:
                found = True
                break
        self.assertTrue(found)
        print("ELS Search: PASS")

if __name__ == '__main__':
    # Run tests manually to print PASS clearly
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestTorahWorkbench)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        if not result.wasSuccessful():
            sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)
