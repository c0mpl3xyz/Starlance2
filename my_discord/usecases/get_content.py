import requests, os
from mappings.mappings import content_mappings

URL = os.getenv('URL')
class GetContentById():
    def execute(self, content_id):
        data = {
                'content_id': content_id
            }
        
        response = requests.get(URL + '/content', json=data)
        contents = [content_mappings(content) for content in response.json()]

        if len(contents):
            contents = contents[0]
            
        return contents