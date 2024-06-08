import requests, os
from mappings.mappings import content_mappings, review_mappings

URL = os.getenv('URL')
class GetCompanyContentView:
    def execute(self, server_id, bot):
        from views import ContentView
        data = {
            'server_id': server_id,
        }

        response = requests.get(URL + '/content/company', json=data)

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