#CLI version

import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
from google.generativeai.types import GenerationConfig  # Import GenerationConfig
import json

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
    Give a summary of the core concept explained in this YouTube transcript. Then, provide {num_of_ideas} practical activities, projects, or exercises that could help someone further explore or apply what they learned. These suggestions should be distinct from any examples in the video.  Format the response as a JSON object with the following structure:

    ```json
    {{
      "summary": "summary of the core concept",
      "ideas": [
        {{
          "idea_title": "title of idea 1",
          "idea_content": "detailed description of idea 1"
        }},
        {{
          "idea_title": "title of idea 2",
          "idea_content": "detailed description of idea 2"
        }},
        // ... more ideas
      ]
    }}
    ```

    Transcript:
    ```
    {transcript}
    ```
    """

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(response_mime_type="application/json") # No schema needed, rely on the prompt
    )


    try:
        response_json = json.loads(response.text)  # Parse the JSON string
        print(json.dumps(response_json, indent=2)) # Pretty print the JSON

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw response: {response.text}") # Print the raw response for debugging



if __name__ == "__main__":
    main()