from googleapiclient.discovery import build
from environ import Env
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


env = Env()
api_key = "AIzaSyC9mb8ZRUqLifAluBIbQ2wNH7ifmYIlc4I"

youtube = build('youtube', 'v3', developerKey=api_key)
youtube_url = "https://www.youtube.com/watch?v=c-QsfbznSXI&t=3478s"
url_data = urlparse(youtube_url)
query = parse_qs(url_data.query)
video_id = query.get("v", [None])[0]  # Safely get the video ID
# transcript = YouTubeTranscriptApi.get_transcript(video_id)
# print(transcript)

thumb_request = youtube.videos().list(
    part='contentDetails',
    id=video_id
)

thumb_response=thumb_request.execute()
items = thumb_response["items"]

urls = items

print(urls)


# # if "maxres" in urls:
# #     print(urls["maxres"])
# # elif "high" in urls:
# #     print(urls["high"])
# # elif "medium" in urls:
# #     print(urls["medium"])
# # else:
# #     print(urls["default"])


# for url in urls:
#     print(urls[url])
#     print(" ")

request = youtube.channels().list(
    part='statistics',
    forUsername='penguinz0'
)

response = request.execute()

pl_request = youtube.playlists().list(
    part='contentDetails, snippet',
    channelId="UCq6VFHwMzcMXbuKyG7SQYIg"
)

pl_response = pl_request.execute()

# for item in pl_response['items']:
#     print(item)


pl_items_request = youtube.playlistItems().list(
    part='contentDetails',
    playlistId='PLRD7N-Zrj2DMUJAlXRGKpeEel-7isQjI1'
)

pl_items_response = pl_items_request.execute()

vid_ids = []
for item in pl_items_response['items']:
    # print(item['contentDetails']['videoId'])
    vid_ids.append(item['contentDetails']['videoId'])

vid_request = youtube.videos().list(
    part="contentDetails",
    id=",".join(vid_ids)
)

vid_response = vid_request.execute()

# for item in vid_response['items']:
#     print(item['contentDetails']['duration'])

# print(vid_ids)

# print(pl_response)



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
    
# print(get_transcript("https://www.youtube.com/watch?v=308KoLSLlCc"))