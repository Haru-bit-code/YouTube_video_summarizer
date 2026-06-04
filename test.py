# test_setup.py
# This file tests that all libraries installed correctly

# Test 1: Flask
from flask import Flask
print("✅ Flask imported successfully")

# Test 2: YouTube Transcript API
from youtube_transcript_api import YouTubeTranscriptApi
print("✅ YouTube Transcript API imported successfully")

# Test 3: Groq
from groq import Groq
print("✅ Groq imported successfully")

# Test 4: dotenv
from dotenv import load_dotenv
import os
load_dotenv()  # This reads your .env file
key = os.getenv("GROQ_API_KEY")
if key:
    print("✅ .env file loaded — API key found")
else:
    print("❌ .env file problem — API key not found")

print("\n🎉 Setup complete! Ready to build.")