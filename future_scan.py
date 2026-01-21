from els_search import BibleCodeScanner
from text_processor import TextProcessor

class FutureScan:
    def __init__(self):
        self.scanner = BibleCodeScanner()
        self.tp = TextProcessor()

    def run(self):
        output = []
        output.append("Initiating Future-Tech Scan of Genesis Chapter 1...\n")
        
        # Load Text
        raw = self.tp.load_file("data/torah_text.txt")
        flat_text = self.tp.normalize(raw)
        output.append(f"Search Space: {len(flat_text)} characters (Genesis 1)\n")
        
        targets = {
            "ATOM": "אטום",       # Aleph-Tet-Vav-Mem
            "DNA": "דנא",         # Dalet-Nun-Aleph
            "CODE": "קוד",        # Qof-Vxav-Dalet
            "COMPUTER": "מחשב",   # Mem-Het-Shin-Bet
            "GOLEM": "גולם",      # Gimel-Vav-Lamed-Mem (Ancient robot/AI)
            "WISDOM": "חכמה",     # Het-Kaf-Mem-He (Hokhma - tech/wisdom)
            "NETWORK": "רשת"      # Resh-Shin-Tav (Reshet)
        }
        
        found_log = {}

        for name, hebrew in targets.items():
            output.append(f"Scanning for '{name}' ({hebrew})...")
            # Scan wide range of skips: 1 to 200
            results = list(self.scanner.search(flat_text, hebrew, 1, 200))
            
            # Also check backwards (negative skips)
            results_neg = list(self.scanner.search(flat_text, hebrew, -200, -1))
            all_hits = results + results_neg
            
            if all_hits:
                output.append(f"  -> Found {len(all_hits)} hits.")
                found_log[name] = all_hits
            else:
                output.append("  -> None found.")

        # Cluster Analysis
        output.append("\n--- CLUSTER ANALYSIS (The 'Hidden Message') ---")
        
        # Compare every pair of terms
        keys = list(found_log.keys())
        for i in range(len(keys)):
            for j in range(i+1, len(keys)):
                term1 = keys[i]
                term2 = keys[j]
                
                hits1 = found_log[term1]
                hits2 = found_log[term2]
                
                for h1 in hits1:
                    for h2 in hits2:
                        dist = abs(h1['start_index'] - h2['start_index'])
                        
                        if dist < 20:
                            output.append(f"[!] POTENTIAL BREAKTHROUGH: '{term1}' and '{term2}' found together!")
                            output.append(f"    {term1}: Index {h1['start_index']}, Skip {h1['skip']}")
                            output.append(f"    {term2}: Index {h2['start_index']}, Skip {h2['skip']}")
                            output.append(f"    Distance: {dist} letters.")
                            output.append("-" * 30)

        final_out = "\n".join(output)
        print(final_out)
        with open("future_report.txt", "w", encoding="utf-8") as f:
            f.write(final_out)

if __name__ == "__main__":
    scan = FutureScan()
    scan.run()
