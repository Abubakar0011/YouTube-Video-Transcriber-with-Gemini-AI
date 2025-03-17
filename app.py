import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os
from dotenv import load_dotenv

load_dotenv()

os.getenv("Google_API")
genai.configure(api_key=os.getenv("Google_API"))

# model = genai.GenerativeModel("models/gemini-1.5-pro")


def get_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    return None


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([line["text"] for line in transcript])
    except Exception as e:
        return f"Error fetching transcript: {e}"
    

def summarize_text(text):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        response = model.generate_content(
            "Summarize the following text: " + text)
        return response.text
    except Exception as e:
        return f"Error in summarization: {e}"
    

# Streamlit UI
st.title("🎥 YouTube Video Transcriber with Gemini AI")

youtube_url = st.text_input("Enter YouTube Video URL:")
if youtube_url:
    video_id = get_video_id(youtube_url)
    if video_id:
        st.write(f"✅ Extracted Video ID: `{video_id}`")
        
        # Fetch Transcript
        transcript = get_transcript(video_id)
        
        if transcript.startswith("Error"):
            st.error(transcript)
        else:
            st.subheader("📜 Full Transcript")
            st.text_area("Transcript", transcript, height=300)

            # Summarize Transcript
            if st.button("Summarize with Gemini 🤖"):
                summary = summarize_text(transcript)
                st.subheader("📄 Summarized Transcript")
                st.write(summary)
    else:
        st.error("Invalid YouTube URL. Please enter a correct link.")
