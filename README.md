# 🎬 YouTube Video Summarizer + Q&A

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-AI-orange?style=for-the-badge&logo=ai&logoColor=white)
![LLaMA](https://img.shields.io/badge/LLaMA_3.3-70B-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An AI-powered web app that summarizes any YouTube video and lets you chat with its content.**

[🚀 Live Demo](https://youtubevideosummarizer-myzblgswtunneuk69m6eig.streamlit.app) · [🐛 Report Bug](https://github.com/haru-bit-code/youtube-summarizer/issues) · [✨ Request Feature](https://github.com/haru-bit-code/youtube-summarizer/issues)

![App Demo](![alt text](image-2.png))

</div>

---

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Future Improvements](#-future-improvements)
- [License](#-license)

---

## 🧠 About The Project

Ever wanted to understand a 1-hour YouTube video in 2 minutes?

This app fetches the transcript of any YouTube video, uses **Groq's LLaMA 3.3 70B** model to generate a clean structured summary, and lets you ask questions about the video in a **ChatGPT-style interface** — all without watching a single second of the video.

> Built as a learning project to demonstrate **API integration**, **LLM prompt engineering**, **RAG (Retrieval Augmented Generation)** concepts, and **Streamlit** web development.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📋 **Instant Summary** | Structured summary with main topic, key points, and takeaway |
| 💬 **Chat with Video** | Ask any question about the video content |
| 📦 **Any Length Video** | Handles long videos via map-reduce chunking |
| 🔍 **Smart Retrieval** | Keyword-based chunk scoring finds the right answer |
| 📄 **Raw Transcript** | View the full extracted transcript |
| 📊 **Video Stats** | Word count and character count of transcript |
| 🎨 **Clean UI** | Dark-themed, responsive Streamlit interface |

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit | Web UI, session state, chat interface |
| **AI Model** | Groq API — LLaMA 3.3 70B | Summarization and Q&A |
| **Transcript** | YouTube Transcript API | Fetching video captions |
| **Language** | Python 3.9+ | Core application logic |
| **Config** | python-dotenv | Environment variable management |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│              Streamlit Web Interface                │
│                    (app.py)                         │
└──────────┬──────────────────┬──────────────────────┘
           │                  │
           ▼                  ▼
   transcript.py         summarizer.py
   ─────────────         ─────────────
   Extract video ID      Chunk transcript
   Fetch captions        Call Groq AI API
   Return text           Return summary/answer
           │                  │
           │                  ▼
           │              qa.py
           │              ──────
           │              Extract keywords
           │              Score chunks
           │              Return best chunk
           │                  │
           ▼                  ▼
    YouTube Servers       Groq AI API
    (caption data)     (LLaMA 3.3 70B)
```

**Design Pattern:** Separation of concerns — each module has one job.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- A free [Groq API key](https://console.groq.com)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/youtube-summarizer.git
cd youtube-summarizer
```

**2. Create a virtual environment**

```bash
python -m venv venv

# Activate it
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up your API key**

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free key at → https://console.groq.com

**5. Run the app**

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📖 Usage

**Step 1** — Paste any YouTube URL into the input box

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Step 2** — Click **✨ Summarize Video** and wait ~10-15 seconds

**Step 3** — Read your structured summary:
```
📌 Main Topic: ...
🔑 Key Points:
  • ...
  • ...
💡 Key Takeaway: ...
```

**Step 4** — Ask questions in the chat interface:
```
You:       "What did he say about climate change?"
Assistant: "According to the transcript, ..."
```

> ⚠️ **Note:** Works best with videos that have English captions enabled.
> TED Talks, lectures, and educational videos work perfectly.

---

## 📁 Project Structure

```
youtube_summarizer/
│
├── app.py                 # Streamlit app — UI and routing
├── transcript.py          # YouTube transcript fetcher
├── summarizer.py          # AI summarization + Q&A logic
├── qa.py                  # Keyword-based chunk retrieval
│
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
│
├── .env                   # API keys — never commit this!
├── .gitignore             # Ignores .env and venv
└── requirements.txt       # Python dependencies
```

---

## ⚙️ How It Works

### 1. Transcript Fetching
The app parses the YouTube URL to extract the video ID, then uses `youtube-transcript-api` to fetch the video's captions as structured text — no video download required.

### 2. Map-Reduce Summarization
Long transcripts are split into **1,500-word chunks**. Each chunk is summarized independently by the AI, then all mini-summaries are combined into one final structured summary. This handles videos of any length.

```
Full Transcript (50,000 words)
        ↓
[Chunk 1] [Chunk 2] [Chunk 3] ...
        ↓
[Summary1] [Summary2] [Summary3] ...
        ↓
    Final Combined Summary ✅
```

### 3. Keyword-Based Q&A Retrieval
When a user asks a question:
1. Stop words are filtered out (`what`, `is`, `the`, etc.)
2. Each transcript chunk is scored by keyword frequency
3. The highest-scoring chunk is sent to the AI with the question
4. AI answers based only on that relevant section

This is a simplified **RAG (Retrieval Augmented Generation)** pipeline.

---

## 🔮 Future Improvements

- [ ] **Vector embeddings** — replace keyword matching with semantic search using `sentence-transformers` + ChromaDB
- [ ] **Multi-language support** — detect and handle non-English transcripts
- [ ] **Transcript caching** — store processed transcripts to avoid repeat API calls
- [ ] **Redis session storage** — support multiple concurrent users
- [ ] **Export feature** — download summary as PDF or Markdown
- [ ] **Timestamp linking** — link Q&A answers back to video timestamps
- [ ] **Playlist support** — summarize entire YouTube playlists

---

## 🐛 Known Limitations

- Only works with videos that have English captions enabled
- In-memory transcript storage resets on server restart
- Keyword matching may miss synonyms (e.g., "car" vs "automobile")
- Very long videos (3h+) may take longer to summarize

---

## 📦 Requirements

```txt
streamlit
flask
youtube-transcript-api==1.0.3
groq
python-dotenv
requests
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

| Variable | Description | Where to Get |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key | [console.groq.com](https://console.groq.com) |

---

## 🛡 Security Notes

- Never commit your `.env` file — it's in `.gitignore`
- Never hardcode API keys in source code
- Use environment variables for all secrets

---

## 📄 License

Distributed under the MIT License.

```
MIT License — feel free to use, modify, and distribute this project.
```

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — for the blazing fast free LLM API
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) — for caption extraction
- [Streamlit](https://streamlit.io) — for the beautiful Python web framework
- [Meta AI](https://ai.meta.com) — for the open-source LLaMA 3.3 model

---

<div align="center">

**Built with ❤️ using Python + Groq AI + Streamlit**

⭐ Star this repo if you found it useful!

</div>
