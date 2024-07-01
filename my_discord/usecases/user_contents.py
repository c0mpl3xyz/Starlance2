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
                for review in review_data:
                    contents.append(ContentView(review_mappings(review), content, bot))
        return contents
    
class GetServerContentView:
    def execute(self, bot):
        from views import ContentView
        response = requests.get(URL + '/content/server')

        contents = []
        JSON = response.json()
        for content_json in JSON:
            content = content_mappings(content_json)
            review_json = requests.get(URL + '/review', json={'review_id': content['review_id']}).json()

            for review in review_json:
                if len(review):
                    contents.append(ContentView(review_mappings(review), content, bot, main=True))
        return contents
    
class GetServerUserContentViews:
    def execute(self, bot, user_id):
        # response = requests.get(URL + '/content/server')
        pass