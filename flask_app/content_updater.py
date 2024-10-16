import requests, os, time
from dotenv import load_dotenv
import logging, traceback
from googleapiclient.discovery import build
from sql_db.conn import ConnectSQL
from sql_db.user import User

SQL_DICT = {
    'host': os.getenv('SQL_HOST'),
    'user': os.getenv('SQL_USER'),
    'password': os.getenv('SQL_PASSWORD'),
    'database': os.getenv('SQL_DATABASE')
}

load_dotenv()
URL = os.getenv('URL')      
API_VERSION = os.getenv('API_VERSION')
APP_ID = os.getenv('APP_ID')
API_PREFIX = os.getenv('API_PREFIX')
PAGE_ID = os.getenv('PAGE_ID')

# IG
IG_URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'
IG_TOKEN = os.getenv('IG_TOKEN')
IG_ID = os.getenv('IG_ID')
IG_PERMISSIONS = ['instagram_manage_insights','instagram_basic','pages_show_list']

# YOUTUBE
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Constants
EPSILON = 1e-8

print(SQL_DICT)
print(IG_URL_PREFIX)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler()])

class ContentUpdater():
    def __init__(self):
        self.ig_processor = IGProcessor()
        self.youtube_processor = YoutubeProcessor()
        self.tiktok_processor = TikTokProcessor()

    def get_jobs(self):
        result = requests.get(URL + '/job/open_jobs')
        return result.json()

    def get_contents_by_job_ids(self, job_ids):
        data = {
            'job_ids': job_ids
        }

        result = requests.get(URL + '/content/job_ids', json=data)
        return result.json()

    def update_content(self, k, data):
        data['content_id'] = k
        requests.put(URL + '/content/status', json=data)

    def update_user_point(self, user_id, data, point_per_view):
        point_ratio = point_per_view / 10.0
        data = {
            'user_id': user_id,
            'points': data['points'] * point_ratio
        }
        requests.put(URL + '/user', json=data)

    def update_job(self, k):
        data = {
            'job_id': k,
            'type': 'Ended'
        }
        requests.put(URL + '/job/status', json=data)

    def content_classifier(self, content_dict: dict):
        classified_contents = {
            'instagram': {},
            'youtube': {},
            'tiktok': {},
        }

        for key, value in content_dict.items():
            if value[7] == 'instagram':
                classified_contents['instagram'][key] = value
            if value[7] == 'youtube':
                classified_contents['youtube'][key] = value
            if value[7] == 'tiktok':
                classified_contents['tiktok'][key] = value

        return classified_contents

    def content_updater(self):
        logging.info('Started updating contents')
        try:
            jobs = self.get_jobs()
            job_ids = [job[0] for job in jobs]
            job_point_dict = {job[0]: job[-1] for job in jobs}
            contents = self.get_contents_by_job_ids(job_ids)
            contents_real_dict = {content[0]: content for content in contents}
            classified_content_dict = self.content_classifier(contents_real_dict)
            ig_result = self.ig_processor.process(classified_content_dict['instagram'].values())
            youtube_result = self.youtube_processor.process(classified_content_dict['youtube'].values())
            # tiktok_result = self.tiktok_processor.process(classified_content_dict['tiktok'].values())

            result = ig_result | youtube_result # | tiktok_result

            job_content_dict = {}
            for job in jobs:
                job_id = job[0]
                # Find all contents that match the job ID
                matching_contents = [content[0] for content in contents if content[2] == job_id]
                job_content_dict[job_id] = matching_contents

            job_budgets = {job[0]: [job[5], False] for job in jobs}
            remove_keys = []
            for k, v in job_content_dict.items():
                if not len(v):
                    remove_keys.append(k)
                    continue
                new_contents = []
                for c_id in v:
                    if c_id in result.keys():
                        new_contents.append({c_id: result[c_id]})
                job_content_dict[k] = new_contents

            for k in remove_keys:
                del job_content_dict[k]
                del job_budgets[k]

            for k, v in job_content_dict.items():
                total = 0
                for v_2 in v:
                    for _, v_2_v in v_2.items():
                        total += v_2_v['total_plays']

                total_views_end = job_budgets[k][0]/job_point_dict[k]
                if total < total_views_end:
                    for v_2 in v:
                        for k_2, v_2_v in v_2.items():
                            v_2_v['active'] = 1
                            self.update_content(k_2, v_2_v)
                else:
                    diff = total - total_views_end
                    for v_2 in v:
                        for k_2, v_2_v in v_2.items():
                            social = contents_real_dict[k_2][7]
                            v_2_v['active'] = 0
                            if  social == 'instagram':
                                total_plays_perc = v_2_v['total_plays'] / (total + EPSILON)
                                initial_perc = v_2_v['initial_plays'] / (v_2_v['total_plays'] + EPSILON)
                                prime_replay_perc = v_2_v['prime_replays'] / (v_2_v['total_plays']  + EPSILON)

                                total_plays_change = (round(diff* total_plays_perc))
                                v_2_v['total_plays'] = v_2_v['total_plays'] - (round(diff* total_plays_perc))
                                v_2_v['initial_plays'] = v_2_v['initial_plays'] - round(total_plays_change * initial_perc)
                                v_2_v['prime_replays'] = v_2_v['prime_replays'] - round(total_plays_change * prime_replay_perc)
                                
                                v_2_v['replays'] = self.ig_processor.calculate_replays(v_2_v['initial_plays'], v_2_v['prime_replays'])
                                v_2_v['points'] = v_2_v['initial_plays'] + v_2_v['replays']
                            
                            if social == 'youtube':
                                total_plays_perc = v_2_v['total_plays'] / (total + EPSILON)
                                total_plays_change = (round(diff* total_plays_perc))
                                v_2_v['total_plays'] = v_2_v['total_plays'] - (round(diff* total_plays_perc))
                                v_2_v['initial_plays'] = v_2_v['total_plays']
                                v_2_v['points'] = v_2_v['total_plays']

                            user_id = contents_real_dict[k_2][3]
                            self.update_content(k_2, v_2_v)
                            self.update_job(k)
                            self.update_user_point(user_id, v_2_v, job_point_dict[k])

            logging.info('Ended updating contents')
        except Exception as e:
            logging.error(traceback.print_stack())
            raise e

class IGProcessor():
    def __init__(self):
        self.access_token = IG_TOKEN
        self.base_url = IG_URL_PREFIX
        self.url_suffix = f'access_token={self.access_token}'
        self.user_id = IG_ID
        self.permissions = IG_PERMISSIONS
    
    def __permission_list(self):
        url = f'{self.base_url}/me/permissions?status=granted&access_token={self.access_token}'
        response = requests.get(url)
        # permissions = [data['permission'] for data in response.json()['data']]
        return response.json()

    def get_permissions(self):
        return self.__permission_list()
    
    def process(self, ig_contents):
        # ig_contents_dict = {self.get_shortcode(content[6]): content[0] for content in ig_contents if self.get_shortcode(content[6]) is not None}
        # ig_result = self.ig_filter_by_shortcodes(ig_contents_dict)

        ig_contents_dict = {content[-1]: content for content in ig_contents if content[-1] is not None}
        ig_result = self.ig_filter_by_ig_content_id(ig_contents_dict)
        return ig_result

    def get_shortcode(self, link):
        link = link.replace('https://www.instagram.com/reel/', '').replace('https://www.instagram.com/p/','')
        splits = link.split('/')
        if len(splits):
            return splits[0]
        return None

    def check_permissions(self):
        token_permissions = self.__permission_list()

        missing_permissions = [permission for permission in self.permissions if permission not in token_permissions]
        result = {
            'valid': len(missing_permissions) == 0,
            'missing_permissions': missing_permissions
        }

        return result

    def get_ig_media_list(self, url=None):
        if url is None:
            url = f'https://graph.facebook.com/v20.0/{IG_ID}?fields=media.limit(100){{shortcode,comments_count,media_product_type,like_count,insights.metric(plays,likes,comments,reach,total_interactions,saved,shares,ig_reels_aggregated_all_plays_count,clips_replays_count){{name,values}}}}&access_token={token}'

        response = requests.get(url)
        return response.json()
    
    def sanitize_shortcodes(self, shortcodes):
        return [shortcode for shortcode in shortcodes if len(shortcode) == 11]
        
    def ig_filter_by_ig_content_id(self, ig_content_id_dict: dict):
        # connection = ConnectSQL().get_connection()
        # try:
        # user = User(connection.cursor())
        # user.get_access_token()
        # connection.close()
        result = {}
        ig_content_ids = list(ig_content_id_dict.keys())
        if not len(ig_content_ids):
            return {}
        
        for key, value in ig_content_id_dict.items():
            if key is None:
                continue
            token_response = requests.get(URL + '/user/user/token', json={'user_id': value[3]})
            
            token = None
            if token_response.status_code == 200:
                token_json = token_response.json()
                if token_json is not None and len(token_json):
                    token = token_json[0]
            
            if token is None:
                #TODO: Do something
                continue
            
            self.access_token = token
            url = f'{IG_URL_PREFIX}/{key}?fields=shortcode,comments_count,media_product_type,like_count,insights.metric(plays,likes,comments,reach,total_interactions,saved,shares,ig_reels_aggregated_all_plays_count,clips_replays_count){{name,values}}&access_token={self.access_token}'

            new_data = {}
            response = requests.get(url)
            if response.status_code == 200:
                JSON = response.json()
                
                for insight in JSON['insights']['data']:
                    if insight['name'] == 'plays':
                        new_data['initial_plays'] = insight['values'][0]['value']

                    if insight['name'] == 'likes':
                        new_data['likes'] = insight['values'][0]['value']

                    if insight['name'] == 'comments':
                        new_data['comments'] = insight['values'][0]['value']

                    if insight['name'] == 'saved':
                        new_data['saves'] = insight['values'][0]['value']

                    if insight['name'] == 'shares':
                        new_data['shares'] = insight['values'][0]['value']

                    if insight['name'] == 'reach':
                        new_data['account_reach'] = insight['values'][0]['value']
                    
                    if insight['name'] == 'total_interactions':
                        new_data['total_interactions'] = insight['values'][0]['value']
                    
                    if insight['name'] == 'ig_reels_aggregated_all_plays_count':
                        new_data['total_plays'] = insight['values'][0]['value']
                    
                    if insight['name'] == 'clips_replays_count':
                        new_data['prime_replays'] = insight['values'][0]['value']

                new_data['replays'] = self.calculate_replays(new_data['initial_plays'], new_data['prime_replays'])
                new_data['points'] = new_data['initial_plays'] + new_data['replays']
                new_data['engagement'] = new_data['total_interactions']
                new_data['engagement_rate'] = new_data['total_interactions'] / (new_data['account_reach'] + EPSILON) * 100.0
            else:
                #TODO: add a last info
                    new_data['initial_plays'] = value[8]
                    new_data['total_plays'] = value[9]
                    new_data['likes'] = value[10]
                    new_data['replays'] = value[11]
                    new_data['saves'] = value[12]
                    new_data['shares'] = value[13]
                    new_data['comments'] = value[14]
                    new_data['account_reach'] = value[15]
                    new_data['total_interactions'] = value[16]
                    new_data['points'] = value[17]
                    new_data['engagement'] = value[18]
                    new_data['engagement_rate'] = value[19]

            result[value[0]] = new_data
        # except:
            # connection.close()
        return result
        
    def ig_filter_by_shortcodes(self, shortcode_dict: dict):
        shortcodes = self.sanitize_shortcodes(list(shortcode_dict.keys()))
        if not len(shortcodes):
            return {}
        
        foundcodes = []
        finished = False
        my_result = {}
        first = True
        next_url = None
        while not finished:
            if first:
                media_dict, next_url = self.get_ig_media_dict()
                first = False
            elif next_url is not None:
                media_dict, next_url = self.get_ig_media_dict(next_url)
            
            for shortcode in shortcodes:
                if shortcode in media_dict.keys():
                    foundcodes.append(shortcode)
                    my_result[shortcode_dict[shortcode]] = media_dict[shortcode]
            
            if set(shortcodes).intersection(set(foundcodes)) == set(shortcodes):
                finished = True

            if next_url is None:
                break

        return my_result

    # def calculate_replays_points(self, points):
    #     return round(points * 0.7 / 1.7)

    # def calculate_initial_plays_points(self, points):
    #     return round(points * 1 / 1.7)

    # def cal_percent(self, a, b):
    #     return a / (b + EPSILON)

    def calculate_replays(self, initial_plays, replays):
        rate = replays / (initial_plays + EPSILON)
        if rate <= 0.7:
            return replays

        return int(initial_plays * 0.7)

    def get_ig_media_dict(self, url=None):
        media = self.get_ig_media_list(url)
        if url is None:
            media = media['media']
        my_data = {}
        for data in media['data']:
            if data['media_product_type'] == 'REELS':
                insights_data = data['insights']['data']
                new_data = {}
                for insight in insights_data:
                    if insight['name'] == 'plays':
                        new_data['initial_plays'] = insight['values'][0]['value']

                    if insight['name'] == 'likes':
                        new_data['likes'] = insight['values'][0]['value']

                    if insight['name'] == 'comments':
                        new_data['comments'] = insight['values'][0]['value']

                    if insight['name'] == 'saved':
                        new_data['saves'] = insight['values'][0]['value']

                    if insight['name'] == 'shares':
                        new_data['shares'] = insight['values'][0]['value']

                    if insight['name'] == 'reach':
                        new_data['account_reach'] = insight['values'][0]['value']
                    
                    if insight['name'] == 'total_interactions':
                        new_data['total_interactions'] = insight['values'][0]['value']
                    
                    if insight['name'] == 'ig_reels_aggregated_all_plays_count':
                        new_data['total_plays'] = insight['values'][0]['value']
                    
                    if insight['name'] == 'clips_replays_count':
                        new_data['prime_replays'] = insight['values'][0]['value']

                new_data['replays'] = self.calculate_replays(new_data['initial_plays'], new_data['prime_replays'])
                new_data['points'] = new_data['initial_plays'] + new_data['replays']
                new_data['engagement'] = new_data['total_interactions']
                new_data['engagement_rate'] = new_data['total_interactions'] / (new_data['account_reach'] + EPSILON) * 100.0
                my_data[data['shortcode']] = new_data
        next_url = None
        if 'next' in media['paging']:
            next_url = media['paging']['next']
        return my_data, next_url

class YoutubeProcessor():
    def __init__(self):
        self.youtube_api_key = ''
        pass

    def process(self, youtube_contents):
        youtube_contents_dict = {self.get_video_id(content[6]): content[0] for content in youtube_contents if self.get_video_id(content[6]) is not None}
        result = self.get_youtube_media_list(youtube_contents_dict)
        return result

    def get_youtube_media_list(self, contents: dict):
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        video_ids_batch_size = 50
        start_index = 0
        video_ids = list(set(contents.keys()))
        total_videos = len(video_ids)

        result = []
        while start_index < total_videos:
            end_index = min(start_index + video_ids_batch_size, total_videos)
            batch_ids = video_ids[start_index:end_index]

            request = youtube.videos().list(
                # part='snippet,statistics,contentDetails,status',
                part='statistics',
                id=','.join(batch_ids)
            )

            try:
                response = request.execute()
                for item in response['items']:

                    statistics = item['statistics']
                    views = int(statistics.get('viewCount', 'N/A'))
                    likes = int(statistics.get('likeCount', 'N/A'))
                    favorites = int(statistics.get('favoriteCount', 'N/A'))
                    comments = int(statistics.get('commentCount', 'N/A'))

                    new_dict = {}
                    new_dict['shortcode'] = item['id']
                    new_dict['total_plays'] = views
                    new_dict['points'] = views
                    new_dict['likes'] = likes
                    new_dict['comments'] = comments 
                    new_dict['engagement'] = round((likes + favorites + comments) / views * 100.0, 2)
                    result.append(new_dict)

            except Exception:
                traceback.print_stack()

            start_index += video_ids_batch_size

        final_result = {}
        for item in result:
            final_result[contents[item['shortcode']]] = item
        return final_result
    
    def get_video_id(self, link: str):
        video_prefixes = [
            'https://www.youtube.com/watch?v=',
            'https://youtu.be/',
            'https://www.youtube.com/watch?v=',
            'https://www.youtube.com/watch?v=',
            'https://www.youtube.com/embed/',
            'https://www.youtube.com/watch?v=',
            'https://www.youtube.com/shorts/'
        ]

        for prefix in video_prefixes:
            link = link.replace(prefix, '')

        splits = link.split('&')
        if len(splits):
            return splits[0]
        return None
    
    def sanitize_video_id(self, ):
        pass

class TikTokProcessor():
    pass

if __name__ == '__main__':
    print(IG_ID)
    print(IG_TOKEN)
    ContentUpdater().content_updater()