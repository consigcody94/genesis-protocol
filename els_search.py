class BibleCodeScanner:
    def __init__(self):
        pass

    def search(self, text, term, min_skip=1, max_skip=100):
        """
        Searches for a term in the text with equidistant letter skips.
        
        Args:
            text (str): The flattened Hebrew text (no spaces).
            term (str): The search term.
            min_skip (int): Minimum skip distance.
            max_skip (int): Maximum skip distance.
            
        Yields:
            dict: { 'term': term, 'start_index': n, 'skip': d, 'sequence': found_sequence }
        """
        text_len = len(text)
        term_len = len(term)
        
        if term_len == 0 or text_len == 0:
            return

        # Iterate through skips
        # We check both positive (forward) and negative (backward) skips if desired.
        # For this implementation, we allow negative skips if user passes negative range, 
        # or we can just iterate -max to -min and min to max.
        # Let's iterate explicitly through the range provided.
        
        skips = list(range(min_skip, max_skip + 1))
        # Add negative skips if range is positive only? 
        # Usually ELS checks both. Let's strictly follow arguments for now.
        
        for d in skips:
            if d == 0: continue
            
            # Max index for starting depends on skip and length
            # Formula: index = start + (term_len - 1) * d
            # We need 0 <= index < text_len
            
            for n in range(text_len):
                # Calculate the end index for this potential sequence
                # We don't need to generate the whole string to fail early, but in Python slicing is fast.
                
                # Slicing with step [start : end : step]
                # End point for slice is tricky because it's exclusive.
                # start + (term_len * d) is mostly right but needs care for negative d.
                
                try:
                    # Construct candidate manually to be safe or use slice
                    # Slice method:
                    # needed_len = term_len
                    # end_index = n + (d * needed_len)
                    
                    # Python slice is forgiving if it goes out of bounds, it just stops.
                    # We need EXACT length match.
                    
                    candidate = text[n : n + (d * term_len) : d]
                    
                    if len(candidate) == term_len:
                        if candidate == term:
                            yield {
                                'term': term,
                                'start_index': n,
                                'skip': d
                            }
                except Exception:
                    continue
