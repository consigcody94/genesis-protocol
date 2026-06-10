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
        # Normalization strips niqqud and spaces, keeps letters
        raw = "בְּרֵאשִׁית בָּרָא"
        expected = "בראשיתברא"
        self.assertEqual(self.tp.normalize(raw), expected)

    def test_normalize_keeps_final_forms(self):
        # Final (sofit) letters are Hebrew consonants and must survive
        raw = "שלום עולם"
        self.assertEqual(self.tp.normalize(raw), "שלוםעולם")

    def test_gematria(self):
        # 'שלום' - Shin(300) + Lamed(30) + Vav(6) + Mem Sophit(40) = 376
        word = "שלום"
        self.assertEqual(self.ge.calculate(word, "standard"), 376)
        # Ordinal: Shin(21) + Lamed(12) + Vav(6) + Mem(13) = 52
        self.assertEqual(self.ge.calculate(word, "ordinal"), 52)

    def test_ciphers(self):
        # Atbash is its own inverse
        word = "אבג"
        encrypted = self.ce.atbash(word)
        self.assertEqual(self.ce.atbash(encrypted), word)
        # Albam is its own inverse (shift by 11 twice = 22 = identity)
        self.assertEqual(self.ce.albam(self.ce.albam(word)), word)

    def test_els_positive_skip(self):
        # Aleph, Mem, Bet, Mem, Gimel -> "אבג" appears with skip 2 from index 0
        text = "אמבמג"
        results = list(self.els.search(text, "אבג", 1, 5))
        self.assertTrue(any(r['skip'] == 2 and r['start_index'] == 0
                            for r in results))

    def test_els_negative_skip(self):
        # text = ג ב א; reading backwards from index 2 with skip -1 gives "אב"
        text = "גבא"
        results = list(self.els.search(text, "אב", -5, -1))
        self.assertTrue(any(r['skip'] == -1 and r['start_index'] == 2
                            for r in results))

    def test_els_negative_skip_reaching_index_zero(self):
        # Regression: sequences ending at index 0 were missed because the
        # slice end went negative and wrapped around to the end of the string.
        text = "גבא"
        results = list(self.els.search(text, "בג", -5, -1))
        self.assertTrue(any(r['skip'] == -1 and r['start_index'] == 1
                            for r in results))

    def test_els_no_false_positives_out_of_bounds(self):
        # A skip that would run past the start of the text must not match.
        text = "אב"
        results = list(self.els.search(text, "באג", -5, -1))
        self.assertEqual(results, [])


if __name__ == '__main__':
    unittest.main()
