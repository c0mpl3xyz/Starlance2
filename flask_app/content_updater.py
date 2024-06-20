import requests, os, time
from dotenv import load_dotenv
import logging

load_dotenv()
URL = os.getenv('URL')
load_dotenv()
API_VERSION = os.getenv('API_VERSION')
APP_ID = os.getenv('APP_ID')
API_PREFIX = os.getenv('API_PREFIX')
PAGE_ID = os.getenv('PAGE_ID')

URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'
IG_TOKEN = os.getenv('IG_TOKEN')
IG_ID = os.getenv('IG_ID')
PERMISSIONS = ['instagram_manage_insights', 'instagram_basic', 'pages_show_list']

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler()])

def content_updater_2():
    logging.info('LOGGER-----------------------------------------')

def get_jobs():
    result = requests.get(URL + 'job/open_jobs')
    return result.json()

def get_contents_by_job_ids(job_ids):
    data = {
        'job_ids': job_ids
    }

    result = requests.get(URL + 'content/job_ids', json=data)
    return result.json()

def update_content(k, data):
    data['content_id'] = k
    requests.put(URL + '/content/status', json=data)

def update_user_point(user_id, data, point_per_view=10):
    point_ratio = point_per_view / 10.0
    data = {
        'user_id': user_id,
        'points': data['points']
    }
    requests.put(URL + '/user', json=data)

def update_job(k):
    data = {
        'job_id': k,
        'type': 'Ended'
    }
    requests.put(URL + '/job/status', json=data)

def get_shortcode(link):
    link = link.replace('https://www.instagram.com/reel/', '').replace('https://www.instagram.com/p/','')
    splits = link.split('/')
    if len(splits):
        return splits[0]
    return None

def cal_percent(a, b):
    return a / b

def calculate_replays(initial_plays, replays):
    rate = replays / initial_plays
    if rate <= 0.7:
        return replays

    return int(initial_plays * 0.7)

def calculate_replays_points(points):
    return round(points * 0.7 / 1.7)

def calculate_initial_plays_points(points):
    return round(points * 1 / 1.7)

def content_updater():
    logging.info('Started updating contents')
    try:
        ('Im alive!')
        jobs = get_jobs()
        job_ids = [job[0] for job in jobs]
        contents = get_contents_by_job_ids(job_ids)
        contents_real_dict = {content[0]: content for content in contents}
        contents_dict = {get_shortcode(content[6]): content[0] for content in contents if get_shortcode(content[6]) is not None}

        ig_token = ProIGToken()
        result = ig_token.filter_by_shortcodes(contents_dict)
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
                    total += v_2_v['points']

            total_points = job_budgets[k][0]/10
            if total < total_points:
                for v_2 in v:
                    for k_2, v_2_v in v_2.items():
                        v_2_v['active'] = 1
                        update_content(k_2, v_2_v)
            else:
                diff = total - total_points
                for v_2 in v:
                    for k_2, v_2_v in v_2.items():
                        point_perc = v_2_v['points'] / total
                        initial_perc = v_2_v['initial_plays'] / v_2_v['points']
                        replay_perc = v_2_v['replays'] / v_2_v['points']
                        point_change = (round(diff* point_perc))
                        v_2_v['points'] = v_2_v ['points'] - (round(diff* point_perc))
                        v_2_v['initial_plays'] = v_2_v['initial_plays'] - round(point_change * initial_perc)
                        v_2_v['replays'] = v_2_v['replays'] - round(point_change * replay_perc)
                        v_2_v['active'] = 0
                        update_content(k_2, v_2_v)
                        update_job(k)
                        user_id = contents_real_dict[k_2][3]
                        update_user_point(user_id, v_2_v)

        logging.info('Ended updating contents')
    except Exception as e:
        logging.error(f'Content updating failed: {str(e)}')

class ProIGToken():
    def __init__(self):
        self.access_token = IG_TOKEN
        self.base_url = URL_PREFIX
        self.url_suffix = f'access_token={self.access_token}'
        self.user_id = IG_ID
        self.permissions = PERMISSIONS
    
    def __permission_list(self):
        url = f'{self.base_url}/me/permissions?status=granted&access_token={self.access_token}'
        response = requests.get(url)
        # permissions = [data['permission'] for data in response.json()['data']]
        return response.json()

    def get_permissions(self):
        return self.__permission_list()
    
    def check_permissions(self):
        token_permissions = self.__permission_list()

        missing_permissions = [permission for permission in self.permissions if permission not in token_permissions]
        result = {
            'valid': len(missing_permissions) == 0,
            'missing_permissions': missing_permissions
        }

        return result

    def get_media_list(self, url=None):
        if url is None:
            url = f'https://graph.facebook.com/v20.0/{IG_ID}?fields=media.limit(100){{shortcode,comments_count,media_product_type,like_count,insights.metric(plays,likes,comments,reach,total_interactions,saved,shares,ig_reels_aggregated_all_plays_count,clips_replays_count){{name,values}}}}&access_token={IG_TOKEN}'

        response = requests.get(url)
        return response.json()
    
    def sanity_shortcodes(self, shortcodes):
        return [shortcode for shortcode in shortcodes if len(shortcode) == 11]
        
    def filter_by_shortcodes(self, shortcode_dict: dict):
        shortcodes = self.sanity_shortcodes(list(shortcode_dict.keys()))
        if not len(shortcodes):
            return {}
        
        foundcodes = []
        finished = False
        my_result = {}
        first = True
        next_url = None
        while not finished:
            if first:
                media_dict, next_url = self.get_media_dict()
                first = False
            elif next_url is not None:
                media_dict, next_url = self.get_media_dict(next_url)
            
            for shortcode in shortcodes:
                if shortcode in media_dict.keys():
                    foundcodes.append(shortcode)
                    my_result[shortcode_dict[shortcode]] = media_dict[shortcode]
            
            if set(shortcodes).intersection(set(foundcodes)) == set(shortcodes):
                finished = True

            if next_url is None:
                break

        return my_result

    def get_media_dict(self, url=None):
        media = self.get_media_list(url)
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
                        new_data['replays'] = insight['values'][0]['value']

                new_data['replays'] = calculate_replays(new_data['initial_plays'], new_data['replays'])
                new_data['points'] = new_data['initial_plays'] + new_data['replays']
                new_data['engagement'] = new_data['total_interactions']
                new_data['engagement_rate'] = new_data['total_interactions'] / new_data['account_reach'] * 100.0
                my_data[data['shortcode']] = new_data
        next_url = None
        if 'next' in media['paging']:
            next_url = media['paging']['next']
        return my_data, next_url

if __name__ == '__main__':
    content_updater()