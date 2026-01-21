import os
import zlib
import struct

class DecoderLab:
    def __init__(self):
        self.filename = "the_hidden_book.bin"

    def run(self):
        if not os.path.exists(self.filename):
            print("Error: Artifact not found.")
            return

        with open(self.filename, 'rb') as f:
            data = f.read()

        print(f"Loaded Artifact: {len(data)} bytes")
        
        # 1. Magic Number Check
        head = data[:4].hex()
        print(f"\n[1] File Header Scan: {head}")
        signatures = {
            "504b0304": "ZIP Archive",
            "1f8b08": "GZIP",
            "25504446": "PDF",
            "89504e47": "PNG Image",
            "4d5a": "Windows Executable (EXE)",
            "7f454c46": "Linux Executable (ELF)"
        }
        found_sig = False
        for sig, name in signatures.items():
            if head.startswith(sig):
                print(f"   [!] MATCH FOUND: {name}")
                found_sig = True
        if not found_sig:
            print("   No standard file signature detected. (Unknown Format)")

        # 2. String Extraction
        print("\n[2] Extracting Strings (ASCII > 4 chars)...")
        found_strings = []
        current_str = ""
        for byte in data:
            if 32 <= byte <= 126: # Printable ASCII
                current_str += chr(byte)
            else:
                if len(current_str) >= 4:
                    found_strings.append(current_str)
                current_str = ""
        
        print(f"   Found {len(found_strings)} strings.")
        if found_strings:
            print(f"   Top 10: {found_strings[:10]}")
            # Save strings
            with open("decoded_strings.txt", "w") as f:
                f.write("\n".join(found_strings))

        # 3. Decompression Attempt
        print("\n[3] Attempting Decompression (Inflate)...")
        try:
            decompressed = zlib.decompress(data)
            print(f"   [SUCCESS] Inflated data to {len(decompressed)} bytes!")
            with open("unzipped_content.bin", "wb") as f:
                f.write(decompressed)
        except zlib.error:
            print("   [FAIL] Not valid zlib compressed data.")

        # 4. Visual Rendering (The "Grid" View)
        # Convert binary data to a grayscale image (PGM format)
        # Width ~ Square root of size
        import math
        size = len(data)
        width = int(math.sqrt(size))
        height = size // width
        
        print(f"\n[4] Rendering Visual Data Map ({width}x{height})...")
        
        # PGM Header: P5 <width> <height> <maxval> <data>
        header = f"P5\n{width} {height}\n255\n".encode('ascii')
        
        # We need to trim data to match width*height
        pixel_data = data[:width*height]
        
        out_img = "visual_decode.pgm"
        with open(out_img, "wb") as f:
            f.write(header + pixel_data)
            
        print(f"   Image saved to '{out_img}'. Open this to see the raw data visualization.")

if __name__ == "__main__":
    lab = DecoderLab()
    lab.run()
