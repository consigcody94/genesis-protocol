import json
import os
import math
import binascii

class CoreConstructor:
    def __init__(self):
        self.output_file = "genesis_protocol_core.json"
        
    def run(self):
        print("Constructing GENESIS PROTOCOL CORE...")
        
        core_data = {
            "meta": {
                "project": "THE GENESIS PROTOCOL",
                "version": "1.0.0",
                "status": "ROOT_OS_DETECTED"
            },
            "metrics": {},
            "findings": {
                "strings": [],
                "clusters": [],
                "anomalies": []
            },
            "structure": {
                "blocks": []
            } # We won't dump full binary, too big. Just stats.
        }
        
        # 1. Load Binary Stats
        bin_path = "tanakh_full.bin"
        if os.path.exists(bin_path):
            size = os.path.getsize(bin_path)
            core_data["metrics"]["total_size_bytes"] = size
            core_data["metrics"]["total_size_bits"] = size * 8
            
            # Recalculate Entropy
            with open(bin_path, 'rb') as f:
                data = f.read()
                
            from collections import Counter
            counts = Counter(data)
            entropy = 0
            for count in counts.values():
                p = count / len(data)
                entropy -= p * math.log2(p)
            core_data["metrics"]["global_entropy"] = round(entropy, 5)
            
            # Header
            core_data["structure"]["header_hex"] = data[:8].hex()
            
            # REAL DATA INJECTION
            # We take the first 1024 bytes (8192 bits) to serve as the "Seed Row" for the simulation.
            # This ensures the visualizer is rendering the ACTUAL Torah data, not random noise.
            seed_bytes = data[:1024] 
            # Convert to a string of "0" and "1"
            bit_string = bin(int.from_bytes(seed_bytes, byteorder='big'))[2:].zfill(len(seed_bytes)*8)
            core_data["structure"]["seed_bits"] = bit_string
        
        # 2. Load Strings
        str_path = "tanakh_strings.txt"
        if os.path.exists(str_path):
            with open(str_path, 'r', encoding='utf-8') as f:
                strings = [line.strip() for line in f.readlines() if len(line.strip()) > 3]
            # Filter for "interesting" ones for the JSON (keep it smallish)
            interesting = ["IPv6", "DNA", "RNA", "AI", "SSH", "ROOT", "USER", "KEY"]
            
            found_interesting = []
            for s in strings:
                for target in interesting:
                    if target in s.upper():
                        found_interesting.append({"term": target, "context": s})
                        
            # Add top 100 raw strings
            core_data["findings"]["strings"] = strings[:100]
            core_data["findings"]["anomalies"] = found_interesting

        # 3. Load Clusters (from future_report text parsing or hardcoded knowns)
        # We know the DNA-CODE-NETWORK cluster.
        core_data["findings"]["clusters"].append({
            "name": "BIO-DIGITAL TRIAD",
            "terms": ["DNA", "CODE", "NETWORK"],
            "location": "Genesis 1 (Indices 623-893)",
            "proximity": "Tight Cluster (<20 chars)"
        })

        # Save Core
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(core_data, f, indent=4)
            
        print(f"Core Structure Assembled: {self.output_file}")
        
        # Create a JS file too so the HTML can load it easily without local server
        with open("genesis_data.js", "w", encoding='utf-8') as f:
            f.write(f"const GENESIS_CORE = {json.dumps(core_data, indent=2)};")
        print("Exported to genesis_data.js for Web Interface.")

if __name__ == "__main__":
    c = CoreConstructor()
    c.run()
