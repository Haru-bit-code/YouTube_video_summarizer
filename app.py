# app.py
# YouTube Video Summarizer + Q&A
# Built with Streamlit + Groq AI

import streamlit as st
from dotenv import load_dotenv
from transcript import get_transcript
from summarizer import summarize_transcript, answer_question

# Load environment variables
load_dotenv()

# ─────────────────────────────────────────
# PAGE CONFIGURATION
# Must be the first Streamlit command
# ─────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="🎬",
    layout="centered"
)

# ─────────────────────────────────────────
# HEADER SECTION
# ─────────────────────────────────────────
st.title("🎬 YouTube Video Summarizer")
st.markdown("Paste any YouTube URL to get an instant AI summary and ask questions about the video.")
st.divider()

# ─────────────────────────────────────────
# SESSION STATE SETUP
# ─────────────────────────────────────────
# Streamlit reruns the entire script on every interaction.
# st.session_state is how we preserve data between reruns.
# Think of it like a persistent dictionary that survives reruns.

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "summary" not in st.session_state:
    st.session_state.summary = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ─────────────────────────────────────────
# SECTION 1: URL INPUT + SUMMARIZE
# ─────────────────────────────────────────
st.subheader("📥 Step 1 — Enter YouTube URL")

# Text input box for URL
url = st.text_input(
    label="YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed"
)

# Summarize button
if st.button("✨ Summarize Video", use_container_width=True, type="primary"):

    # Validate URL
    if not url.strip():
        st.error("⚠️ Please enter a YouTube URL first.")

    else:
        # Show a spinner while working — keeps user informed
        with st.spinner("Fetching transcript..."):
            transcript, error = get_transcript(url)

        if error:
            st.error(f"❌ {error}")

        else:
            with st.spinner("AI is summarizing the video..."):
                summary = summarize_transcript(transcript)

            # Save to session state so Q&A section can use them
            st.session_state.transcript = transcript
            st.session_state.summary    = summary

            # Clear old chat when new video is loaded
            st.session_state.chat_history = []

            st.success("✅ Video summarized successfully!")


# ─────────────────────────────────────────
# SECTION 2: DISPLAY SUMMARY
# ─────────────────────────────────────────
if st.session_state.summary:

    st.divider()
    st.subheader("📋 Summary")

    # Display summary in a clean container
    with st.container(border=True):
        st.markdown(st.session_state.summary)

    # Optional — show raw transcript in expander
    with st.expander("📄 View Raw Transcript"):
        st.text(st.session_state.transcript[:3000] + "...")


# ─────────────────────────────────────────
# SECTION 3: Q&A CHAT
# ─────────────────────────────────────────
if st.session_state.transcript:

    st.divider()
    st.subheader("💬 Step 2 — Ask Questions About The Video")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box — appears at bottom like ChatGPT
    question = st.chat_input("Ask anything about the video...")

    if question:
        # Show user's question immediately
        with st.chat_message("user"):
            st.markdown(question)

        # Add to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        # Get AI answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = answer_question(
                    st.session_state.transcript,
                    question
                )
            st.markdown(answer)

        # Add answer to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })


# ─────────────────────────────────────────
# SECTION 4: SIDEBAR — INFO + TIPS
# ─────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ How To Use")
    st.markdown("""
    1. **Paste** a YouTube URL
    2. Click **Summarize Video**
    3. Read your instant summary
    4. **Ask questions** about the video
    """)

    st.divider()

    st.header("💡 Tips")
    st.markdown("""
    - Works best with videos that have **English captions**
    - TED Talks work perfectly
    - Educational videos work great
    - Music videos won't work (no speech)
    """)

    st.divider()

    # Show transcript stats if available
    if st.session_state.transcript:
        st.header("📊 Video Stats")
        word_count = len(st.session_state.transcript.split())
        char_count = len(st.session_state.transcript)
        st.metric("Words in transcript", f"{word_count:,}")
        st.metric("Characters", f"{char_count:,}")

    st.divider()
    st.caption("Built with Streamlit + Groq AI + YouTube Transcript API")