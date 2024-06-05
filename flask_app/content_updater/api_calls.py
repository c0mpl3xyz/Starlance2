import requests, os, time
from dotenv import load_dotenv
from pro_ig_token import ProIGToken
load_dotenv()
URL = os.getenv('URL')
def get_jobs():
    result = requests.get(URL + 'job/open_jobs')
    # print(result.json())
    return result.json()

def get_contents_by_job_ids(job_ids):
    data = {
        'job_ids': job_ids
    }

    result = requests.get(URL + 'content/job_ids', json=data)
    # print(result.json())
    return result.json()

def update_content(data):
    requests.put(URL + '/content/status', json=data)

def get_shortcode(link):
    link = link.replace('https://www.instagram.com/reel/', '').replace('https://www.instagram.com/p/','')
    splits = link.split('/')
    if len(splits):
        return splits[0]
    return None

def content_updater():
    try:
        jobs = get_jobs()
        job_ids = [job[0] for job in jobs]
        contents = get_contents_by_job_ids(job_ids)
        contents_dict = {get_shortcode(content[6]): content[0] for content in contents if get_shortcode(content[6]) is not None}

        ig_token = ProIGToken()
        result = ig_token.filter_by_shortcodes(contents_dict)
        for k, v in result.items():
            print(v)
            v['content_id'] = k
            update_content(v)
            pass
        
    except Exception as e:
        raise e


if __name__ == '__main__':
    print(content_updater())