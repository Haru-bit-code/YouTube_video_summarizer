# transcript.py
# Updated for youtube-transcript-api v1.0+

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import urllib.parse


def extract_video_id(url):
    """
    Takes a full YouTube URL and returns just the video ID.
    Handles: youtube.com/watch?v=..., youtu.be/..., youtube.com/embed/...
    """
    parsed = urllib.parse.urlparse(url)

    if parsed.netloc == "youtu.be":
        return parsed.path.lstrip("/")

    query_params = urllib.parse.parse_qs(parsed.query)

    if "v" in query_params:
        return query_params["v"][0]

    return None


def get_transcript(url):
    """
    Main function: takes a YouTube URL, returns full transcript as string.
    Returns (transcript_text, None) on success
    Returns (None, error_message) on failure
    """

    video_id = extract_video_id(url)

    if not video_id:
        return None, "Invalid YouTube URL. Please check the link."

    try:
        # ✅ NEW WAY (v1.0+): create an instance first, then call fetch()
        ytt_api = YouTubeTranscriptApi()
        fetched  = ytt_api.fetch(video_id)

        # fetched is a FetchedTranscript object — iterate it like a list
        texts = [snippet.text for snippet in fetched]

        full_transcript = " ".join(texts)
        return full_transcript, None

    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video."

    except NoTranscriptFound:
        return None, "No transcript found for this video."

    except Exception as e:
        return None, f"An error occurred: {str(e)}"
