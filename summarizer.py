# summarizer.py
# PURPOSE: Break transcript into chunks, send to Groq AI, return summary + answers

import os
from groq import Groq
from dotenv import load_dotenv

# Load the .env file so os.getenv() can read our API key
load_dotenv()


def create_groq_client():
    """
    Creates and returns an authenticated Groq API client.
    Reads the API key from the .env file.
    """
    api_key = os.getenv("GROQ_API_KEY")

    # Safety check — if key is missing, give a clear error
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Please add it to your .env file."
        )

    return Groq(api_key=api_key)


def chunk_text(text, chunk_size=1500):
    """
    Splits a long string into smaller chunks of words.

    Why words and not characters?
    Because splitting mid-word creates broken text.
    Splitting by words keeps meaning intact.

    Args:
        text       : the full transcript string
        chunk_size : how many words per chunk (default 1500)

    Returns:
        List of strings, each containing chunk_size words
    """

    # Step 1: Split the full text into individual words
    # "hello world foo" → ["hello", "world", "foo"]
    words = text.split()

    chunks = []

    # Step 2: Walk through words in steps of chunk_size
    # range(0, 10, 3) → 0, 3, 6, 9  (step = 3)
    # range(0, len(words), chunk_size) → 0, 1500, 3000, 4500...
    for i in range(0, len(words), chunk_size):

        # Step 3: Slice chunk_size words starting at position i
        # words[0:1500]  → first 1500 words
        # words[1500:3000] → next 1500 words
        chunk_words = words[i : i + chunk_size]

        # Step 4: Rejoin the words back into a string
        chunk_text_str = " ".join(chunk_words)

        chunks.append(chunk_text_str)

    return chunks


def ask_groq(client, prompt):
    """
    Sends a prompt to Groq AI and returns the response text.

    Args:
        client : authenticated Groq client
        prompt : the instruction + content to send

    Returns:
        AI response as a string
    """

    response = client.chat.completions.create(
        # Model we're using — fast and free on Groq
        model="llama-3.3-70b-versatile",

        # Messages follow the chat format:
        # "system" = instructions for AI's behavior
        # "user"   = the actual content/question
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert assistant that helps users "
                    "understand YouTube videos. You give clear, "
                    "concise, and accurate responses."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        # Max tokens in the response
        # 1024 tokens ≈ 750 words — enough for a good summary
        max_tokens=1024,

        # Temperature controls creativity
        # 0.0 = robotic/factual, 1.0 = creative/random
        # 0.3 = mostly factual with slight natural variation
        temperature=0.3,
    )

    # Navigate the response structure to get the text
    # response.choices → list of possible responses (usually 1)
    # [0]              → take the first (and only) response
    # .message.content → the actual text string
    return response.choices[0].message.content


def summarize_transcript(transcript):
    """
    Main summarization function.
    Takes full transcript → returns complete summary string.

    Strategy:
    - If transcript is short → summarize directly
    - If transcript is long  → chunk it, summarize each chunk,
                               then combine into final summary
    """

    client = create_groq_client()

    # Count words to decide strategy
    word_count = len(transcript.split())

    # SHORT transcript — summarize in one shot
    if word_count <= 1500:
        prompt = f"""Please summarize the following YouTube video transcript.
        
Structure your summary as:
📌 Main Topic: (one sentence)
🔑 Key Points: (3-5 bullet points)
💡 Key Takeaway: (one sentence conclusion)

Transcript:
{transcript}"""

        return ask_groq(client, prompt)

    # LONG transcript — chunk, summarize each, combine
    else:
        chunks = chunk_text(transcript, chunk_size=1500)
        mini_summaries = []

        # Summarize each chunk individually
        for i, chunk in enumerate(chunks):
            prompt = f"""Summarize the key points from this section 
(part {i+1} of {len(chunks)}) of a YouTube video transcript.
Be concise — 3-5 bullet points maximum.

Section:
{chunk}"""

            mini_summary = ask_groq(client, prompt)
            mini_summaries.append(mini_summary)

        # Combine all mini-summaries into one final summary
        combined = "\n\n".join(mini_summaries)

        final_prompt = f"""Below are summaries of different sections 
of a YouTube video. Combine them into ONE cohesive summary.

Structure it as:
📌 Main Topic: (one sentence)
🔑 Key Points: (5-7 bullet points combining all sections)
💡 Key Takeaway: (one sentence conclusion)

Section summaries:
{combined}"""

        return ask_groq(client, final_prompt)


def answer_question(transcript, question):
    """
    Answers a user's question based on the transcript content.

    Strategy:
    - Find the most relevant chunk for the question
    - Send that chunk + question to Groq AI
    - Return the answer
    """

    client = create_groq_client()

    # For short transcripts — use full text
    word_count = len(transcript.split())

    if word_count <= 1500:
        relevant_text = transcript
    else:
        # Find most relevant chunk using keyword matching
        # We import this from qa.py (built in chunk 4)
        from qa import find_relevant_chunk
        relevant_text = find_relevant_chunk(transcript, question)

    prompt = f"""Answer the following question based ONLY on the 
provided video transcript content.

If the answer is not found in the transcript, say:
"I couldn't find information about that in this video."

Be clear, direct, and concise.

Question: {question}

Transcript content:
{relevant_text}"""

    return ask_groq(client, prompt)



# TEMPORARY TEST — delete after testing
if __name__ == "__main__":
    # Use a short sample transcript to save API calls
    sample_transcript = """
    Artificial intelligence is transforming the world. 
    Machine learning allows computers to learn from data.
    Deep learning uses neural networks with many layers.
    Natural language processing helps computers understand text.
    These technologies are being used in healthcare, finance,
    and many other industries to solve complex problems.
    The future of AI looks very promising but also raises
    important ethical questions about privacy and job displacement.
    """

    print("Testing summarizer...")
    print("=" * 50)

    summary = summarize_transcript(sample_transcript)
    print("SUMMARY:")
    print(summary)

    print("\n" + "=" * 50)
    print("Testing Q&A...")

    answer = answer_question(
        sample_transcript,
        "What industries are using AI?"
    )
    print("ANSWER:")
    print(answer)