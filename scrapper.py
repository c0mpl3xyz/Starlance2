import requests, os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('GRAPH_API')
media_id = 'C3tEqrVubZC'  # Replace with the actual media ID


# url = f'https://graph.instagram.com/{api-version}/{user-id}/media?access_token={access-token}'
'https://graph.instagram.com/v19.0/17841465259887339/media?fields=comments_count,shortcode,like_count,insights.metric(ig_reels_aggregated_all_plays_count)&limit=1000&&filtering=[{field: "media_product_type",operator:"IN",value:["REELS"]}]'
url = f'https://graph.instagram.com/v19.0/{media_id}?access_token={access_token}'
print(url)
response = requests.get(url)
print(response.content)