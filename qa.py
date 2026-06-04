# qa.py
# PURPOSE: Find the most relevant transcript chunk for a user's question

# These are words that appear everywhere and carry no useful meaning
# Filtering them out makes keyword matching much more accurate
STOP_WORDS = {
    "what", "is", "the", "a", "an", "in", "on", "at", "to",
    "did", "do", "does", "he", "she", "they", "we", "i",
    "about", "for", "with", "this", "that", "how", "why",
    "when", "where", "who", "which", "was", "were", "are",
    "has", "have", "had", "be", "been", "being", "will",
    "would", "could", "should", "may", "might", "can",
    "said", "say", "says", "tell", "told", "from", "of",
    "and", "or", "but", "not", "it", "its", "his", "her"
}


def extract_keywords(text):
    """
    Extracts meaningful keywords from a piece of text.

    Process:
    1. Lowercase everything (so "Climate" and "climate" match)
    2. Split into individual words
    3. Remove punctuation from each word
    4. Filter out stop words
    5. Filter out very short words (1-2 chars — usually not meaningful)

    Args:
        text: any string (question or chunk)
    Returns:
        set of meaningful keyword strings
    """

    # Step 1: Lowercase the text
    text_lower = text.lower()

    # Step 2: Split into words
    words = text_lower.split()

    keywords = set()

    for word in words:
        # Step 3: Remove common punctuation from start and end of word
        # "climate," → "climate"   "change." → "change"
        # strip() removes characters listed in the argument
        cleaned = word.strip(".,!?;:\"'()-[]")

        # Step 4: Skip stop words
        if cleaned in STOP_WORDS:
            continue

        # Step 5: Skip very short words (likely not meaningful)
        if len(cleaned) <= 2:
            continue

        # Step 6: Add to our keyword set
        keywords.add(cleaned)

    return keywords


def score_chunk(chunk, keywords):
    """
    Scores a chunk based on how many question keywords it contains.

    Higher score = more relevant to the question.

    Args:
        chunk    : a string (one piece of the transcript)
        keywords : set of keywords from the user's question
    Returns:
        integer score (count of keyword matches)
    """

    # Convert chunk to lowercase for fair comparison
    chunk_lower = chunk.lower()

    score = 0

    for keyword in keywords:
        # Count how many times this keyword appears in the chunk
        # "climate change climate" → "climate".count = 2
        count = chunk_lower.count(keyword)
        score += count

    return score


def find_relevant_chunk(transcript, question, chunk_size=1500):
    """
    Main function: finds the most relevant part of transcript
    for a given question.

    Args:
        transcript : full transcript string
        question   : user's question string
        chunk_size : words per chunk (must match summarizer.py)
    Returns:
        string — the most relevant chunk of transcript text
    """

    # Step 1: Split transcript into chunks (same logic as summarizer.py)
    words = transcript.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)

    # Edge case: if transcript is very short, return it all
    if len(chunks) == 0:
        return transcript

    # Edge case: only one chunk exists, return it directly
    if len(chunks) == 1:
        return chunks[0]

    # Step 2: Extract keywords from the question
    keywords = extract_keywords(question)

    # Edge case: if no keywords found (question was all stop words)
    # return the first chunk as a fallback
    if not keywords:
        return chunks[0]

    # Step 3: Score every chunk against the keywords
    scores = []

    for i, chunk in enumerate(chunks):
        chunk_score = score_chunk(chunk, keywords)
        scores.append(chunk_score)

        # Debug line — shows scoring in action (remove in production)
        # print(f"Chunk {i+1} score: {chunk_score}")

    # Step 4: Find the index of the highest scoring chunk
    # max(scores) finds the highest score value
    # scores.index(...) finds WHERE that value is in the list
    best_index = scores.index(max(scores))

    # Step 5: Return the best chunk
    return chunks[best_index]


def get_answer_context(transcript, question, chunk_size=1500):
    """
    Returns both the relevant chunk AND neighboring chunks
    for better context.

    Why? Sometimes the answer spans across chunk boundaries.
    Getting the chunk before and after adds safety.

    Args:
        transcript : full transcript string
        question   : user's question
        chunk_size : words per chunk
    Returns:
        string — best chunk + its neighbors joined together
    """

    words = transcript.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)

    if len(chunks) <= 2:
        # Short transcript — return everything
        return transcript

    keywords = extract_keywords(question)

    if not keywords:
        return chunks[0]

    # Score all chunks
    scores = [score_chunk(chunk, keywords) for chunk in chunks]
    best_index = scores.index(max(scores))

    # Collect best chunk + neighbors (with boundary safety)
    # max(0, ...) prevents going below index 0
    # min(len-1, ...) prevents going above last index
    start = max(0, best_index - 1)
    end   = min(len(chunks) - 1, best_index + 1)

    # Join the window of chunks together
    context_chunks = chunks[start : end + 1]
    return " ".join(context_chunks)