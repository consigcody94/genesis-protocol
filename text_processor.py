import re

class TextProcessor:
    def __init__(self):
        # Range of Hebrew Unicode characters
        # Aleph: 0x05D0 to Tav: 0x05EA
        self.hebrew_pattern = re.compile(r'[\u05D0-\u05EA]')
        
        # Niqqud and Cantillation marks range: 0x0591 to 0x05C7
        # We want to remove these for specific analysis modes
        self.cleanup_pattern = re.compile(r'[\u0591-\u05C7]')

    def load_file(self, filepath):
        """Loads Hebrew text from a file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def strip_niqqud(self, text):
        """Removes vowels and cantillation marks, keeping only letters."""
        return self.cleanup_pattern.sub('', text)

    def normalize(self, text):
        """
        Removes all non-Hebrew characters (spaces, punctuation, etc.)
        Returns a continuous string of Hebrew letters.
        Examples: 
            Input: "בְּרֵאשִׁית בָּרָא"
            Output: "בראשיתברא"
        """
        # First, strip niqqud just in case, though the character class below might exclude them if narrowly defined.
        # But generally we want letters only.
        
        # Use findall to get all Hebrew letters and join them
        letters = self.hebrew_pattern.findall(text)
        return "".join(letters)

    def flatten_text(self, text):
        """Alias for normalize in the context of ELS which needs a flat string."""
        return self.normalize(text)
