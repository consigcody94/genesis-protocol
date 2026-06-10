import random

from analysis_utils import ensure_utf8_stdout
from els_search import BibleCodeScanner
from text_processor import TextProcessor

class FutureScan:
    def __init__(self):
        self.scanner = BibleCodeScanner()
        self.tp = TextProcessor()

    def scan_text(self, flat_text, targets, output):
        """Scan a letter stream for every target; returns {name: hits}."""
        found_log = {}
        for name, hebrew in targets.items():
            output.append(f"Scanning for '{name}' ({hebrew})...")
            # Scan wide range of skips: 1 to 200, both directions
            results = list(self.scanner.search(flat_text, hebrew, 1, 200))
            results += list(self.scanner.search(flat_text, hebrew, -200, -1))

            if results:
                output.append(f"  -> Found {len(results)} hits.")
                found_log[name] = results
            else:
                output.append("  -> None found.")
        return found_log

    def count_clusters(self, found_log, output=None, max_dist=20):
        """Count term pairs that land within max_dist letters of each other."""
        clusters = 0
        keys = list(found_log.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                term1, term2 = keys[i], keys[j]
                for h1 in found_log[term1]:
                    for h2 in found_log[term2]:
                        dist = abs(h1['start_index'] - h2['start_index'])
                        if dist < max_dist:
                            clusters += 1
                            if output is not None:
                                output.append(f"[!] CLUSTER: '{term1}' and '{term2}' found together!")
                                output.append(f"    {term1}: Index {h1['start_index']}, Skip {h1['skip']}")
                                output.append(f"    {term2}: Index {h2['start_index']}, Skip {h2['skip']}")
                                output.append(f"    Distance: {dist} letters.")
                                output.append("-" * 30)
        return clusters

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
            "CODE": "קוד",        # Qof-Vav-Dalet
            "COMPUTER": "מחשב",   # Mem-Het-Shin-Bet
            "GOLEM": "גולם",      # Gimel-Vav-Lamed-Mem (Ancient robot/AI)
            "WISDOM": "חכמה",     # Het-Kaf-Mem-He (Hokhma - tech/wisdom)
            "NETWORK": "רשת"      # Resh-Shin-Tav (Reshet)
        }

        found_log = self.scan_text(flat_text, targets, output)

        # Cluster Analysis
        output.append("\n--- CLUSTER ANALYSIS ---")
        real_clusters = self.count_clusters(found_log, output)
        output.append(f"Total clusters in Genesis 1: {real_clusters}")

        # NULL CONTROL: identical scan over the same letters, shuffled.
        # Any hit/cluster counts that survive shuffling are expected by
        # chance from the letter frequencies alone, not hidden meaning.
        output.append("\n--- NULL CONTROL (same letters, shuffled, seed=22) ---")
        rng = random.Random(22)
        letters = list(flat_text)
        rng.shuffle(letters)
        shuffled = "".join(letters)

        control_output = []
        control_log = self.scan_text(shuffled, targets, control_output)
        for name in targets:
            real_hits = len(found_log.get(name, []))
            ctrl_hits = len(control_log.get(name, []))
            output.append(f"  {name:<10} real: {real_hits:>3}   shuffled: {ctrl_hits:>3}")
        control_clusters = self.count_clusters(control_log)
        output.append(f"  Clusters   real: {real_clusters:>3}   shuffled: {control_clusters:>3}")

        final_out = "\n".join(output)
        print(final_out)
        with open("future_report.txt", "w", encoding="utf-8") as f:
            f.write(final_out)

if __name__ == "__main__":
    ensure_utf8_stdout()
    scan = FutureScan()
    scan.run()
