from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    """
    Extract video ID from:
    - https://www.youtube.com/watch?v=ID
    - https://youtu.be/ID
    """
    parsed = urlparse(url)

    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")

    if "youtube.com" in parsed.netloc:
        return parse_qs(parsed.query).get("v", [""])[0]

    return ""


def get_transcript_with_lang(video_id: str):
    """
    Fetch transcript text and its language.
    Prefer Hindi or English captions.
    Fallback to auto-generated captions if needed.
    """
    ytt = YouTubeTranscriptApi()

    transcripts = ytt.list(video_id)

    try:
        # Prefer manually created captions
        transcript = transcripts.find_transcript(['hi', 'en'])
    except Exception:
        # Fallback to auto-generated captions
        transcript = transcripts.find_generated_transcript(['hi', 'en'])

    data = transcript.fetch()

    text = " ".join([t.text for t in data])

    return text, transcript.language_code