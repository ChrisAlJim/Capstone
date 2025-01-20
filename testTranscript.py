#CLI version

import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai

def get_transcript(youtube_url):
    try:
        url_data = urlparse(youtube_url)
        query = parse_qs(url_data.query)
        video_id = query.get("v", [None])[0]  # Safely get the video ID

        if not video_id:
            return "Invalid YouTube URL. Please provide a URL with a valid video ID."

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([segment['text'] for segment in transcript])  # Combine segments into a single string

    except Exception as e:
        return f"An error occurred: {str(e)}"  # Return the error message

def main():
    parser = argparse.ArgumentParser(description="Fetch and process YouTube transcript.")
    parser.add_argument("youtube_url", help="The URL of the YouTube video")
    parser.add_argument("--api_key", help="Your Google Generative AI API key", required=True)
    parser.add_argument("--num_of_ideas", help="Number of ideas you want to get", required=True)
    args = parser.parse_args()

    youtube_url = args.youtube_url
    api_key = args.api_key
    num_of_ideas = args.num_of_ideas

    # Get transcript
    transcript = get_transcript(youtube_url)
    if "An error occurred" in transcript or "Invalid YouTube URL" in transcript:
        print(transcript)
        return

    # Configure Google Generative AI
    genai.configure(api_key=api_key)

    prompt = f"""
    Summarize the core concept explained in this YouTube transcript. Based on this concept, suggest 

    ```
    {num_of_ideas} 
    ```
    practical activities, projects, or exercises that could help someone further explore or apply what they learned. These suggestions should be different from the examples (if any) shown in the video.

    Transcript:
    ```
    {transcript}
    ```
    """

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    print(response.text)

if __name__ == "__main__":
    main()