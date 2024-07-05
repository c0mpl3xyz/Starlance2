import traceback
from googleapiclient.discovery import build
API_KEY = 'AIzaSyDwvMUC7oCE-5lOBJWONytRcIj26Gq_avs'

# Build the YouTube service
youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_video_statistics(video_ids):
    video_ids_batch_size = 50
    start_index = 0
    total_videos = len(video_ids)

    result = []
    while start_index < total_videos:
        end_index = min(start_index + video_ids_batch_size, total_videos)
        batch_ids = video_ids[start_index:end_index]

        request = youtube.videos().list(
            # part='snippet,statistics,contentDetails,status',
            part='statistics,status',
            id=','.join(batch_ids)
        )

        try:
            response = request.execute()
            for item in response['items']:
                video_id = item['id']
                # snippet = item['snippet']
                statistics = item['statistics']
                # content_details = item['contentDetails']
                status = item['status']

                new_dict = statistics | status

                result.append(new_dict)
                # print(f"Video ID: {video_id}")
                # print(f"View Count: {statistics.get('viewCount', 'N/A')}")
                # print(f"Like Count: {statistics.get('likeCount', 'N/A')}")
                # print(f"Dislike Count: {statistics.get('dislikeCount', 'N/A')}")
                # print(f"Comment Count: {statistics.get('commentCount', 'N/A')}")
                # print(f"Duration: {content_details.get('duration', 'N/A')}")
                # print(f"Definition: {content_details.get('definition', 'N/A')}")
                # print(f"Caption: {content_details.get('caption', 'N/A')}")
                # print(f"License: {status.get('license', 'N/A')}")
                # print(f"Privacy Status: {status.get('privacyStatus', 'N/A')}")
                # print(f"Embeddable: {status.get('embeddable', 'N/A')}")
                # print("----------")
        except Exception:
            traceback.print_stack()

        start_index += video_ids_batch_size
    return result

# Example usage
video_ids = ['cQ2Ht_8iRJ4'] # Replace with your list of video IDs
result = get_video_statistics(video_ids)

print(len(result))
print(result[0])