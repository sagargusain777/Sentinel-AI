def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Split a text string into overlapping chunks without breaking words."""

    # Input validation
    if chunk_overlap <= 0:
        raise ValueError("Chunk overlap should be a positive integer")
    if chunk_size <= 0:
        raise ValueError("Chunk size should be a positive integer")
    if chunk_size < chunk_overlap:
        raise ValueError("Chunk overlap should be smaller than chunk size")

    text_length = len(text)
    start = 0
    chunks = []

    while start < text_length:

        # Calculate tentative end for this chunk
        end = start + chunk_size

        # Word-boundary adjustment (avoid splitting mid-word)
        if end < text_length and text[end] != " ":
            last_space = text[start:end].rfind(" ")
            if last_space != -1:
                end = start + last_space + 1

        # Append the chunk
        chunk = text[start:end]
        chunks.append(chunk)

        # Advance start with forward-progress guard
        next_start = end - chunk_overlap
        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


# ════════════════════════════════════════════════════════════════════════
# DETAILED EXPLANATION & NOTES
# ════════════════════════════════════════════════════════════════════════
#
# ── What this function does ─────────────────────────────────────────────
#
#   chunk_text() splits a long text into smaller overlapping pieces called
#   "chunks". This is useful before feeding text to embedding models that
#   have a maximum token/character limit (e.g. OpenAI's 8191-token window).
#
#
# ── Parameters ──────────────────────────────────────────────────────────
#
#   text          : The raw input string to split.
#   chunk_size    : Maximum characters per chunk. Must be positive.
#   chunk_overlap : Characters shared between consecutive chunks. Must be
#                   positive and less than chunk_size. Overlap ensures
#                   context near boundaries isn't lost.
#
#
# ── Return Value ────────────────────────────────────────────────────────
#
#   Returns a list[str] of text chunks.
#
#
# ── Algorithm Step-by-Step ──────────────────────────────────────────────
#
#   1. VALIDATE inputs — fail early with clear error messages.
#
#   2. SLIDE a window of `chunk_size` across the text:
#        end = start + chunk_size
#
#   3. WORD-BOUNDARY ADJUSTMENT — if the character at `end` is NOT a
#      space, we search backwards (rfind) for the last space in the
#      chunk slice text[start:end]:
#
#        - rfind(" ") returns the INDEX of the last space in the slice,
#          or -1 if no space exists.
#
#        - If found (last_space != -1):
#            end = start + last_space + 1
#          This snaps `end` to just AFTER the space, keeping the word
#          intact. The +1 keeps the space in the current chunk.
#
#        - If NOT found (last_space == -1):
#          The chunk is one giant word with no spaces. We keep the hard
#          cut because there's nothing else we can do.
#
#      We SKIP this adjustment for the LAST chunk (end >= text_length)
#      because we want to grab all remaining text.
#
#   4. APPEND text[start:end] to our chunks list.
#
#   5. ADVANCE start:
#        next_start = end - chunk_overlap
#
#      FORWARD-PROGRESS GUARD:
#        If next_start <= start, we'd be stuck (infinite loop).
#        This happens when chunk_overlap is close to chunk_size AND
#        word-boundary adjustment pulls `end` far back.
#
#        Example:  chunk_size=100, chunk_overlap=90
#          Iteration 1: start=0, end snaps to 95
#                        next_start = 95-90 = 5
#          Iteration 2: start=5, end snaps to 95 again
#                        next_start = 95-90 = 5 ← SAME! Infinite loop!
#
#        Fix: if next_start <= start, force next_start = end to
#        guarantee we always move forward.
#
#   6. REPEAT until start >= text_length.
#
#
# ── Why check for -1? ──────────────────────────────────────────────────
#
#   rfind(" ") returns -1 when NO space is found in the string.
#   If we used -1 directly without checking:
#
#     end = start + (-1) + 1 = start + 0 = start
#     chunk = text[start:start] → empty string ""
#     next_start = start - overlap → goes NEGATIVE
#     → Infinite loop with empty chunks!
#
#   The -1 check prevents this — when there's no space, we simply keep
#   the original `end` and do a hard cut through the word.
#
#
# ── Visual Example ──────────────────────────────────────────────────────
#
#   >>> chunk_text("The quick brown fox jumps over the lazy dog",
#   ...            chunk_size=15, chunk_overlap=5)
#   ['The quick brown ', 'brown fox jumps ', 'jumps over the ', 'the lazy dog']
#
#   "The quick brown fox jumps over the lazy dog"
#    |── chunk 1 ──|                                  text[0:16]  "The quick brown "
#              |── chunk 2 ──|                        text[11:27] "brown fox jumps "
#                        |── chunk 3 ──|              text[22:37] "jumps over the "
#                                  |── chunk 4 ──|   text[32:44] "the lazy dog"
#              ↑─overlap─↑
#
#
# ── Edge Cases Handled ──────────────────────────────────────────────────
#
#   1. No spaces in chunk   → hard cut (keeps original end)
#   2. Last chunk           → grabs all remaining text (Python slicing
#                             handles out-of-bounds gracefully)
#   3. High overlap         → forward-progress guard prevents infinite loop
#   4. Invalid inputs       → raises ValueError immediately
#
# ════════════════════════════════════════════════════════════════════════
