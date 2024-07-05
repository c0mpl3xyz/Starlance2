import requests

# Replace with your actual access token
access_token = 'YOUR_ACCESS_TOKEN'
video_id = 'YOUR_VIDEO_ID'  # Replace with the actual video ID

# TikTok API endpoint for getting video statistics
url = f'https://open-api.tiktok.com/video/stats/?access_token={access_token}&video_id={video_id}'

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    video_stats = response.json()
    print(video_stats)
else:
    print(f'Error: {response.status_code}')
    print(response.text)