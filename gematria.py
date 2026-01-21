class GematriaEngine:
    def __init__(self):
        # Standard Gematria values (Mispar Ragil)
        self.values = {
            'א': 1, 'b': 0, # Placeholder/Typo safety
            'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
            'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50,
            'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100,
            'ר': 200, 'ש': 300, 'ת': 400
        }
        
        # Ordinal values (Mispar Siduri) 1-22
        # Building it dynamically or statically, let's do static for clarity
        self.ordinal_values = {}
        alphabet = "אבגדהוזחטיכלמנסעפצקרשת"
        for i, char in enumerate(alphabet, 1):
            self.ordinal_values[char] = i
        # Map sophit forms to same ordinal often, or extend. 
        # Standard usage often maps sophit to same as regular.
        # Let's map suffix forms to their regular counterparts for ordinal.
        sophit_map = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}
        for s, r in sophit_map.items():
            if r in self.ordinal_values:
                self.ordinal_values[s] = self.ordinal_values[r]

    def calculate(self, text, method="standard"):
        """
        Calculates Gematria value for a given text.
        Methods:
            - standard: Mispar Ragil (Aleph=1, Tav=400)
            - ordinal: Mispar Siduri (Aleph=1, Tav=22)
            - reduced: Mispar Katan (digit sum, Aleph=1, Tav=4)
        """
        total = 0
        text = text.strip()
        
        for char in text:
            if char in self.values:
                val = 0
                if method == "standard":
                    val = self.values[char]
                elif method == "ordinal":
                    val = self.ordinal_values.get(char, 0)
                elif method == "reduced":
                    # Reduced is sum of digits of standard value, then reduced again until single digit?
                    # Or typically: value % 9 (with 0 becoming 9)?
                    # Mispar Katan usually treats TAV (400) as 4+0+0=4.
                    std_val = self.values[char]
                    val = self.digit_sum(std_val)
                
                total += val
                
        return total

    def digit_sum(self, n):
        """Helper for reduced gematria."""
        s = sum(int(digit) for digit in str(n))
        # Some versions reduce strictly to single digit:
        # while s > 9: s = sum(int(digit) for digit in str(s))
        # But standard Mispar Katan often just takes the zeros off (e.g. 10=1, 20=2, 100=1).
        # Which is effectively what sum of digits does for 10, 100.
        # For complex numbers, it varies. Let's do simple digit sum.
        return s

    def get_breakdown(self, text):
        """Returns a list of values per character for visualization."""
        breakdown = []
        for char in text:
            if char in self.values:
                breakdown.append((char, self.values[char]))
        return breakdown
