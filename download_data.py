import os
import urllib.request

class Downloader:
    def run(self):
        # Map filenames to URL paths
        # URL structure: .../BookName/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json
        # Base URL for Torah is .../Tanakh/Torah
        
        sections = {
            "Torah": ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"],
            "Prophets": ["Joshua", "Judges", "I Samuel", "II Samuel", "I Kings", "II Kings", "Isaiah", "Jeremiah", "Ezekiel", 
                         "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"],
            "Writings": ["Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", 
                         "Daniel", "Ezra", "Nehemiah", "I Chronicles", "II Chronicles"]
        }
        
        base_github = "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/json/Tanakh"
        suffix = "/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json"
        
        if not os.path.exists("data"):
            os.makedirs("data")

        for section, books in sections.items():
            for book in books:
                # Handle spaces in Book Name for URL
                book_url_name = book.replace(" ", "%20")
                url = f"{base_github}/{section}/{book_url_name}{suffix}"
                
                # Filename: lowercase, no spaces
                filename = book.lower().replace(" ", "_") + ".json"
                
                print(f"Downloading {book} ({section}) from {url}...")
                
                dest = os.path.join("data", filename)
                try:
                    urllib.request.urlretrieve(url, dest)
                    size = os.path.getsize(dest)
                    print(f"  -> Saved {filename} ({size} bytes)")
                except Exception as e:
                    print(f"  [ERROR] Failed to download {book}: {e}")
        
        # We don't need the old manual list anymore
        return

if __name__ == "__main__":
    d = Downloader()
    d.run()
