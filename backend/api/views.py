from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer, IdeaSerializer, YoutubeIdeaRequestSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
import google.generativeai as genai
from google.generativeai.types import GenerationConfig  # Import GenerationConfig
import json
import environ
from .models import Idea
from operator import itemgetter

# Create your views here.
class IdeaListCreate(generics.ListCreateAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Idea.objects.filter(thinker=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(thinker=self.request.user)
        else:
            print(serializer.errors)
        return 
    
class IdeaDelete(generics.DestroyAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Idea.objects.filter(thinker=user)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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
    
def thumb_and_title(youtube_url):
    env = environ.Env()
    api_key = env('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    url_data = urlparse(youtube_url)
    query = parse_qs(url_data.query)
    video_id = query.get("v", [None])[0]

    if not video_id:
        return "Invalid YouTube URL. Please provide a URL with a valid video ID."
        
    thumb_request = youtube.videos().list(
        part='snippet',
        id=video_id
    )

    thumb_response=thumb_request.execute()

    thumbnails = thumb_response["items"][0]["snippet"]["thumbnails"]

    thumbnail = thumb_response["items"][0]["snippet"]["thumbnails"]

    if "maxres" in thumbnails:
        thumbnail = thumbnails["maxres"]["url"]
    elif "high" in thumbnails:
        thumbnail = thumbnails["high"]["url"]
    elif "medium" in thumbnails:
        thumbnail = thumbnails["medium"]["url"]
    else:
        thumbnail = thumbnails["default"]["url"]

    title = thumb_response["items"][0]["snippet"]["title"]

    return [thumbnail, title]
    

@api_view(['POST'])
def generate_ideas(request):
    serializer = YoutubeIdeaRequestSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        youtube_url = validated_data['youtube_url']
        num_ideas = validated_data['num_ideas']
        env = environ.Env()
        api_key = env('GOOGLE_API_KEY')

        transcript = get_transcript(youtube_url)
        if "An error occurred" in transcript or "Invalid YouTube URL" in transcript:
            print(transcript)
            return
        
        thumbnail = thumb_and_title(youtube_url)[0]
        title = thumb_and_title(youtube_url)[1]

        # Configure Google Generative AI
        genai.configure(api_key=api_key)

        prompt = f"""
        Give a summary of the core concept explained in this YouTube transcript. Then, provide strictly {num_ideas} practical activities, projects, or exercises that could help someone further explore or apply what they learned. These suggestions should be distinct from any examples in the video.  Format the response as a JSON object with the following structure:

        ```json
        {{
          "thumbnail": {thumbnail},
          "video_title": {title}
          "summary": "summary of the core concept",
          "ideas": [
            {{
              "thumbnail": {thumbnail},
              "video_title": {title},
              "idea_title": "title of idea 1",
              "idea_content": "detailed description of idea 1"
            }},
            {{
              "thumbnail": {thumbnail},
              "video_title": {title},
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

        model = genai.GenerativeModel("gemini-1.5-flash-8b")
        response = model.generate_content(
            prompt,
            generation_config=GenerationConfig(response_mime_type="application/json")
        )


        try:
            response_json = json.loads(response.text)
            return Response(response_json, status=status.HTTP_200_OK)
        except json.JSONDecodeError as e:
            return Response({"error": f"Error decoding JSON: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)