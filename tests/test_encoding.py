import struct
import unittest

from master_command_64 import MasterCommand64
from null_hypothesis import (letters_to_digits, pack_base22, shannon_entropy,
                             extract_ascii_strings, riscv_valid_ratio,
                             ALPHABET, SOFIT_MAP, BLOCK_SIZE)


class TestBase22Encoding(unittest.TestCase):
    def setUp(self):
        self.mc = MasterCommand64()

    def test_char_map_covers_all_consonant_forms(self):
        # 22 base letters + 5 final forms = 27 mapped characters
        self.assertEqual(len(self.mc.char_map), 27)
        for sofit, base in SOFIT_MAP.items():
            self.assertEqual(self.mc.char_map[sofit], self.mc.char_map[base])

    def test_process_block_value(self):
        # "בא" = Bet(1), Aleph(0) -> 1*22 + 0 = 22
        self.assertEqual(self.mc.process_block("בא"), 22)

    def test_final_letters_are_encoded(self):
        # Regression: final Mem must contribute a digit, not be dropped
        with_final = self.mc.process_block("אם")   # 0*22 + 12
        with_base = self.mc.process_block("אמ")    # 0*22 + 12
        self.assertEqual(with_final, with_base)
        self.assertEqual(with_final, self.mc.char_map['מ'])

    def test_block_fits_in_64_bits(self):
        # Largest possible 13-letter block must pack into one 64-bit word
        max_block = "ת" * BLOCK_SIZE
        val = self.mc.process_block(max_block)
        self.assertLess(val, 2 ** 64)
        struct.pack('>Q', val)  # must not raise

    def test_pack_base22_matches_master_command(self):
        text = "בראשיתבראאלהיםאתהשמיםואתהארץ"
        digits = letters_to_digits(text)
        packed = pack_base22(digits)
        # Rebuild the same stream through MasterCommand64.process_block
        expected = bytearray()
        for i in range(0, len(text), BLOCK_SIZE):
            expected.extend(struct.pack('>Q', self.mc.process_block(text[i:i + BLOCK_SIZE])))
        self.assertEqual(packed, bytes(expected))

    def test_letters_to_digits_folds_finals(self):
        base_idx = ALPHABET.index('צ')
        self.assertEqual(letters_to_digits("ץ"), [base_idx])


class TestAnalysisHelpers(unittest.TestCase):
    def test_shannon_entropy_constant_is_zero(self):
        self.assertEqual(shannon_entropy(b"\x00" * 100), 0.0)

    def test_shannon_entropy_two_symbols_is_one_bit(self):
        self.assertAlmostEqual(shannon_entropy(b"\x00\x01" * 50), 1.0)

    def test_extract_ascii_strings(self):
        data = b"\x00DNA\xffcode\x01ab"
        self.assertEqual(extract_ascii_strings(data, min_len=3), ["DNA", "code"])

    def test_riscv_valid_ratio(self):
        # 0x13 (OP-IMM) is valid, 0x7F is not
        data = struct.pack('<I', 0x13) + struct.pack('<I', 0x7F)
        self.assertEqual(riscv_valid_ratio(data), 0.5)


if __name__ == '__main__':
    unittest.main()
