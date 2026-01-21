import json
import os
from text_processor import TextProcessor

class TorahLoader:
    def __init__(self):
        self.tp = TextProcessor()
        # Canonical Order of the Tanakh
        self.books = [
            # Torah
            "data/genesis.json", "data/exodus.json", "data/leviticus.json", "data/numbers.json", "data/deuteronomy.json",
            # Nevi'im (Prophets)
            "data/joshua.json", "data/judges.json", "data/i_samuel.json", "data/ii_samuel.json", 
            "data/i_kings.json", "data/ii_kings.json", "data/isaiah.json", "data/jeremiah.json", "data/ezekiel.json",
            "data/hosea.json", "data/joel.json", "data/amos.json", "data/obadiah.json", "data/jonah.json", 
            "data/micah.json", "data/nahum.json", "data/habakkuk.json", "data/zephaniah.json", "data/haggai.json", 
            "data/zechariah.json", "data/malachi.json",
            # Ketuvim (Writings)
            "data/psalms.json", "data/proverbs.json", "data/job.json", "data/song_of_songs.json", "data/ruth.json", 
            "data/lamentations.json", "data/ecclesiastes.json", "data/esther.json", "data/daniel.json", 
            "data/ezra.json", "data/nehemiah.json", "data/i_chronicles.json", "data/ii_chronicles.json"
        ]
    
    def load_full_torah(self):
        full_text = []
        print("Loading full Torah corpus...")
        
        for book_path in self.books:
            if not os.path.exists(book_path):
                print(f"Warning: {book_path} not found. Skipping.")
                continue
                
            try:
                with open(book_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Sefaria JSON structure usually: { "text": [ ["Chapter 1 vs 1", "vs 2"], ["Chap 2"] ] }
                    # or slightly different depending on export.
                    # Let's inspect structure blindly or safe process
                    
                    text_content = data.get('text', [])
                    for chapter in text_content:
                        if isinstance(chapter, list):
                            for verse in chapter:
                                if isinstance(verse, str):
                                    full_text.append(verse)
            except Exception as e:
                print(f"Error loading {book_path}: {e}")

        combined = " ".join(full_text)
        print(f"Raw Text Loaded: {len(combined)} chars")
        
        normalized = self.tp.normalize(combined)
        print(f"Normalized Stream: {len(normalized)} Hebrew letters")
        return normalized

if __name__ == "__main__":
    loader = TorahLoader()
    text = loader.load_full_torah()
    # verify
    if len(text) > 200000:
        print("Success: Full Torah loaded.")
