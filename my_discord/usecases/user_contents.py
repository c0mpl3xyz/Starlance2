import requests, os
from mappings.mappings import content_mappings, review_mappings

URL = os.getenv('URL')
class GetUserContentView:
    def execute(self, user_id, bot):
        from views import ContentView
        data = {
                'user_id': user_id,
        }

        response = requests.get(URL + '/content/user', json=data)

        JSON = response.json()
        if not len(JSON):
            return []
        
        contents = []
        for i, content_json in enumerate(JSON):
            content = content_mappings(content_json)
            review_data = requests.get(URL + '/review', json={'review_id': content['review_id']}).json()
            if len(review_data):
                review_data = review_data[0]
            contents.append(ContentView(review_mappings(review_data), content, bot))
        return contents