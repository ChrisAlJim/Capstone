from googleapiclient.discovery import build

api_key = '[API_KEY]'

youtube = build('youtube', 'v3', developerKey=api_key)

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

for item in vid_response['items']:
    print(item['contentDetails']['duration'])

# print(vid_ids)

# print(pl_response)

