class CipherEngine:
    def __init__(self):
        self.alphabet = "אבגדהוזחטיכלמנסעפצקרשת"
        # Standard Atbash Map
        # First maps to Last
        self.atbash_map = {}
        for i in range(len(self.alphabet)):
            self.atbash_map[self.alphabet[i]] = self.alphabet[-(i+1)]
            
        # Albam Map
        # Replaces letter with one 11 positions away (mod 22)
        # Often splits alphabet in half: Aleph-Kaf (1-11) and Lamed-Tav (12-22)
        self.albam_map = {}
        half = len(self.alphabet) // 2
        for i in range(len(self.alphabet)):
            target_idx = (i + half) % len(self.alphabet)
            self.albam_map[self.alphabet[i]] = self.alphabet[target_idx]

    def atbash(self, text):
        """Applies Atbash cipher to the text."""
        result = []
        for char in text:
            if char in self.atbash_map:
                result.append(self.atbash_map[char])
            else:
                result.append(char)
        return "".join(result)

    def albam(self, text):
        """Applies Albam cipher to the text."""
        result = []
        for char in text:
            if char in self.albam_map:
                result.append(self.albam_map[char])
            else:
                result.append(char)
        return "".join(result)
